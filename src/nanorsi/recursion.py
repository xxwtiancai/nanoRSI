"""Task-level recursion in the paper's two modes, budgeted and ledgered.

agg (parallel): k independent INV/DOM candidate pairs are probed against the shared
base rollout, then k compositions each draw on the whole probed pool — width.
seq (sequential): each round proposes against the current harness, composes, and
the composition becomes the next round's base — depth. Every rollout, proposal,
contrast and composition is a ledger event with its usage."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import experience, probe, propose, runner, select


class BudgetExhausted(RuntimeError):
    pass


@dataclass
class TaskResult:
    task_id: str
    reference: runner.Rollout
    finals: list = field(default_factory=list)
    chosen: str = ""
    decisions: list = field(default_factory=list)
    lesson: dict | None = None


class Session:
    """One evolve run over a workspace: shared budget, ledger, library."""

    def __init__(self, config, model, workspace: Path, ledger):
        self.config, self.model, self.workspace, self.ledger = config, model, Path(workspace), ledger
        self.rejected: list[str] = []

    # --- budget -----------------------------------------------------------
    def _charge(self, kind: str):
        used = self.ledger.usage()
        if kind == "rollout" and used["rollouts"] >= self.config.budget.max_rollouts:
            self.ledger.append("budget_exhausted", kind=kind, used=used)
            raise BudgetExhausted(f"rollout budget {self.config.budget.max_rollouts} reached")
        if kind == "proposer" and used["proposer_calls"] >= self.config.budget.max_proposer_calls:
            self.ledger.append("budget_exhausted", kind=kind, used=used)
            raise BudgetExhausted(f"proposer budget {self.config.budget.max_proposer_calls} reached")

    # --- primitives -------------------------------------------------------
    def rollout(self, task, tree, label, run_root) -> runner.Rollout:
        self._charge("rollout")
        result = runner.run(self.config, self.model, self.workspace, task, tree, label, run_root / label)
        self.ledger.append("rollout", task=task["task_id"], **result.record())
        return result

    def propose(self, dim, task, tree, reference, lessons):
        self._charge("proposer")
        cand = propose.propose(self.model, dim, task, tree, reference, rejected=self.rejected, lessons=lessons)
        self.ledger.append("proposal", task=task["task_id"], **cand.record())
        return cand

    def contrast(self, task, reference, probed, cand):
        self._charge("proposer")
        verdict = probe.contrast(self.model, task, reference, probed, cand)
        self.ledger.append("contrast", task=task["task_id"], dim=cand.dim, component=cand.component, **verdict)
        if verdict["contrast"] != "mitigates":
            self.rejected.append(f"{cand.dim} {cand.component}: {cand.note} -> {verdict['contrast']}: {verdict['observation'][:160]}")
        return verdict

    def compose(self, task, base, candidates, contrasts, reference):
        self._charge("proposer")
        record, tree = propose.compose(self.model, task, base, candidates, contrasts, reference)
        self.ledger.append("compose", task=task["task_id"], **record)
        return record, tree

    # --- one candidate pair: propose both, probe both, contrast both -----
    def _pair(self, task, tree, reference, lessons, run_root, index):
        candidates, contrasts = [], {}
        for dim in propose.DIMS:
            cand = self.propose(dim, task, tree, reference, lessons)
            if cand.error:
                contrasts[dim] = {"contrast": "regresses", "observation": cand.error}
                candidates.append(cand)
                continue
            probed = self.rollout(task, cand.tree, f"{dim.lower()}{index}", run_root)
            contrasts[dim] = self.contrast(task, reference, probed, cand)
            candidates.append(cand)
        return candidates, contrasts

    # --- modes --------------------------------------------------------------
    def _parallel(self, task, base, reference, lessons, run_root, result):
        pool = [self._pair(task, base, reference, lessons, run_root, i) for i in range(1, self.config.k + 1)]
        for i, (candidates, contrasts) in enumerate(pool, 1):
            record, tree = self.compose(task, base, candidates, contrasts, reference)
            result.decisions.append(record)
            result.finals.append(self.rollout(task, tree, f"agg{i}", run_root) if record["decision"] != "keep"
                                 else self._kept(reference, f"agg{i}", run_root, tree))
        return result

    def _sequential(self, task, base, reference, lessons, run_root, result):
        current_tree, current_ref = base, reference
        for t in range(1, self.config.k + 1):
            candidates, contrasts = self._pair(task, current_tree, current_ref, lessons, run_root, t)
            record, tree = self.compose(task, current_tree, candidates, contrasts, current_ref)
            result.decisions.append(record)
            final = (self.rollout(task, tree, f"c{t}", run_root) if record["decision"] != "keep"
                     else self._kept(current_ref, f"c{t}", run_root, tree))
            result.finals.append(final)
            current_tree, current_ref = tree, final
        return result

    def _kept(self, reference, label, run_root, tree) -> runner.Rollout:
        """A keep decision reuses the reference execution instead of paying a rollout."""
        kept = runner.Rollout(label, reference.run_dir, reference.ok, reference.delivered, reference.trajectory,
                              dict(reference.deliverables), {}, reference.error)
        from . import harness
        harness.write_tree(tree, run_root / label / "harness")
        self.ledger.append("rollout_reused", task=None, label=label, source=reference.label)
        return kept

    # --- a whole task ---------------------------------------------------------
    def evolve_task(self, task: dict, base: dict) -> TaskResult:
        run_root = self.workspace / ".nanorsi" / "runs" / task["task_id"].replace("/", "__")
        lessons = experience.load_lessons(self.workspace)
        self.ledger.append("task_started", task=task["task_id"], mode=self.config.mode, k=self.config.k)
        reference = self.rollout(task, base, "base1", run_root)
        result = TaskResult(task["task_id"], reference)
        if self.config.mode == "agg":
            self._parallel(task, base, reference, lessons, run_root, result)
        else:
            self._sequential(task, base, reference, lessons, run_root, result)
        delivered = [f for f in result.finals if f.delivered]
        pool = delivered or result.finals
        if len(pool) > 1:
            self._charge("proposer")
            choice = select.blind(self.model, task, pool, seed=self.config.seed)
            self.ledger.append("selection", task=task["task_id"], **choice)
            result.chosen = choice["chosen"]
        else:
            result.chosen = pool[0].label
            self.ledger.append("selection", task=task["task_id"], chosen=result.chosen, why="single final", usage={})
        final_tree = self._tree_of(run_root, result.chosen)
        if final_tree != base:
            self._charge("proposer")
            result.lesson = experience.extract(self.model, task, base, final_tree, result.decisions, self.workspace)
            self.ledger.append("experience", task=task["task_id"], lesson=result.lesson,
                               usage=(result.lesson or {}).get("usage", {}))
        self.ledger.append("task_done", task=task["task_id"], chosen=result.chosen,
                           decisions=[d["decision"] for d in result.decisions])
        return result

    def _tree_of(self, run_root, label):
        from . import harness
        return harness.read_tree(run_root / label / "harness")

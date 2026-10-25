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
            result.finals.extend(self._finals(task, tree, f"agg{i}", run_root, reference, record))
        return result

    def _sequential(self, task, base, reference, lessons, run_root, result):
        current_tree, current_ref = base, reference
        for t in range(1, self.config.k + 1):
            candidates, contrasts = self._pair(task, current_tree, current_ref, lessons, run_root, t)
            record, tree = self.compose(task, current_tree, candidates, contrasts, current_ref)
            result.decisions.append(record)
            finals = self._finals(task, tree, f"c{t}", run_root, current_ref, record)
            result.finals.extend(finals)
            current_tree = tree if record["decision"] not in {"keep", "rollback"} else current_tree
            current_ref = finals[0]
        return result

    def _finals(self, task, tree, label, run_root, reference, record) -> list:
        """Roll the composed harness `final_repeats` times and confirm the adoption.

        Adoption is confirmed only if no final draw regresses against the reference
        and at least one mitigates; otherwise the decision is rolled back to keep.
        A single-draw probe verdict is not enough evidence on noisy agentic tasks."""
        if record["decision"] == "keep":
            return [self._kept(reference, label, run_root, tree)]
        draws = [self.rollout(task, tree, label if n == 1 else f"{label}r{n}", run_root)
                 for n in range(1, self.config.final_repeats + 1)]
        if self.config.final_repeats == 1:
            return draws
        pseudo = propose.Candidate("FINAL", ", ".join(record.get("files") or ["composed"]),
                                   record.get("observation", "")[:200], tree)
        verdicts = [self.contrast(task, reference, draw, pseudo)["contrast"] for draw in draws]
        confirmed = "regresses" not in verdicts and "mitigates" in verdicts
        self.ledger.append("final_confirmed" if confirmed else "rollback", task=task["task_id"],
                           label=label, verdicts=verdicts, decision=record["decision"])
        if confirmed:
            return draws
        record["decision"], record["rolled_back_from"] = "rollback", record["decision"]
        return [self._kept(reference, f"{label}keep", run_root, self._tree_of(run_root, "base1"))]

    def _kept(self, reference, label, run_root, tree) -> runner.Rollout:
        """A keep decision reuses the reference execution instead of paying a rollout."""
        import shutil
        keep_dir = run_root / label
        keep_dir.mkdir(parents=True, exist_ok=True)
        from . import harness
        harness.write_tree(tree, keep_dir / "harness")
        for name in ("output", "deliverables"):
            source = Path(reference.run_dir) / name
            if source.is_dir():
                shutil.copytree(source, keep_dir / name, dirs_exist_ok=True)
        self.ledger.append("rollout_reused", label=label, source=reference.label,
                           reference_run_dir=str(reference.run_dir))
        return runner.Rollout(label, keep_dir, reference.ok, reference.delivered, reference.trajectory,
                              dict(reference.deliverables), {}, reference.error)

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

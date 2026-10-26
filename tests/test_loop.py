"""End-to-end offline lifecycle on the starter template with the scripted model."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from nanorsi import cli, harness, judge, recursion, report
from nanorsi.config import load_config
from nanorsi.ledger import Ledger
from nanorsi.model import Model
from nanorsi.templates import render

from tests._stub import StubTransport

REPO = Path(__file__).resolve().parents[1]


def _workspace(tmp: Path, **toml_overrides) -> Path:
    root = tmp / "ws"
    render(root, goal="Improve document work")
    text = (root / "nanorsi.toml").read_text()
    for dotted, value in toml_overrides.items():
        section, key = dotted.split(".")
        text = cli._set_key(text, section, key, value)
    (root / "nanorsi.toml").write_text(text)
    return root


def _run_cli(argv, stub):
    with mock.patch.object(cli, "_model", lambda config: Model(config.model, api_key="k", transport=stub)):
        return cli.main(argv)


class LifecycleTests(unittest.TestCase):
    def test_agg_k1_full_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp))
            stub = StubTransport(contrast="mitigates", decision="adopt_inv")
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root)], stub), 0)
            ledger = Ledger(root / ".nanorsi" / "ledger.jsonl")
            events = [row["event"] for row in ledger.events()]
            self.assertEqual(events.count("task_started"), 2)
            self.assertEqual(events.count("rollout"), 2 * 4)        # base + inv + dom + agg per task
            self.assertEqual(events.count("contrast"), 4)
            self.assertEqual(events.count("compose"), 2)
            self.assertEqual(events.count("experience"), 2)
            self.assertEqual(ledger.verify(), len(events))
            # evolve is refused after freeze; judge requires freeze
            self.assertEqual(cli.main(["judge", "--workspace", str(root)]), 1)
            self.assertEqual(cli.main(["freeze", "--workspace", str(root)]), 0)
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root)], stub), 1)
            self.assertEqual(cli.main(["judge", "--workspace", str(root)]), 0)
            summary = report.summarize(ledger)
            self.assertEqual(summary["means"]["n"], 2)
            self.assertTrue((root / "reports" / "report.md").is_file())
            self.assertEqual(cli.main(["verify", "--workspace", str(root)]), 0)
            library = (root / ".nanorsi" / "library.jsonl").read_text().splitlines()
            self.assertEqual(len(library), 2)

    def test_keep_decision_reuses_reference_and_writes_no_lesson(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp))
            stub = StubTransport(contrast="neutral", decision="keep")
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root), "--max-tasks", "1"], stub), 0)
            ledger = Ledger(root / ".nanorsi" / "ledger.jsonl")
            events = [row["event"] for row in ledger.events()]
            self.assertEqual(events.count("rollout"), 3)             # base + inv + dom; agg reused
            self.assertEqual(events.count("rollout_reused"), 1)
            self.assertEqual(events.count("experience"), 0)
            self.assertFalse((root / ".nanorsi" / "library.jsonl").exists())
            # the reused final must still be judgeable on its own directory
            kept = root / ".nanorsi" / "runs" / "ops__meeting-action-items" / "agg1"
            self.assertTrue((kept / "deliverables" / "action-items.md").is_file())
            self.assertEqual(cli.main(["freeze", "--workspace", str(root)]), 0)
            self.assertEqual(cli.main(["judge", "--workspace", str(root)]), 0)
            summary = report.summarize(Ledger(root / ".nanorsi" / "ledger.jsonl"))
            self.assertEqual(summary["means"]["n"], 1)

    def test_seq_k2_chains_and_blind_selects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp), **{"experiment.mode": "seq", "experiment.k": 2})
            stub = StubTransport(contrast="mitigates", decision="adopt_inv", select_choice="B")
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root), "--max-tasks", "1"], stub), 0)
            ledger = Ledger(root / ".nanorsi" / "ledger.jsonl")
            rollouts = [row["label"] for row in ledger.events() if row["event"] == "rollout"]
            self.assertEqual(rollouts[0], "base1")
            self.assertEqual(set(rollouts[1:3]), {"inv1", "dom1"})     # probes run concurrently
            self.assertEqual(rollouts[3], "c1")
            self.assertEqual(set(rollouts[4:6]), {"inv2", "dom2"})
            self.assertEqual(rollouts[6:], ["c2"])
            selection = next(row for row in ledger.events() if row["event"] == "selection")
            self.assertIn(selection["chosen"], {"c1", "c2"})
            self.assertFalse(selection["fallback"])

    def test_compose_failure_falls_back_to_keep_after_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp))
            stub = StubTransport(fail_compose_once=True)
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root), "--max-tasks", "1"], stub), 0)
            compose = next(row for row in Ledger(root / ".nanorsi" / "ledger.jsonl").events() if row["event"] == "compose")
            self.assertEqual(compose["decision"], "adopt_inv")        # retry succeeded
            self.assertEqual(compose["usage"]["calls"], 2)

    def test_budget_exhaustion_is_ledgered_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp), **{"budget.max_rollouts": 2})
            stub = StubTransport()
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root)], stub), 0)
            events = [row["event"] for row in Ledger(root / ".nanorsi" / "ledger.jsonl").events()]
            self.assertIn("budget_exhausted", events)
            self.assertEqual(events.count("rollout"), 2)

    def test_final_repeats_confirm_an_adoption_and_blind_select_among_draws(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp), **{"experiment.final_repeats": 2})
            stub = StubTransport(contrast="mitigates", decision="adopt_inv", final_contrast="mitigates", select_choice="B")
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root), "--max-tasks", "1"], stub), 0)
            ledger = Ledger(root / ".nanorsi" / "ledger.jsonl")
            labels = [row["label"] for row in ledger.events() if row["event"] == "rollout"]
            self.assertEqual(labels[0], "base1")
            self.assertEqual(set(labels[1:3]), {"inv1", "dom1"})
            self.assertEqual(set(labels[3:5]), {"agg1", "agg1r2"})     # confirmation draws run concurrently
            self.assertEqual(ledger.count("final_confirmed"), 1)
            selection = next(row for row in ledger.events() if row["event"] == "selection")
            self.assertIn(selection["chosen"], {"agg1", "agg1r2"})
            self.assertEqual(ledger.count("experience"), 1)

    def test_final_repeats_roll_back_a_regressing_adoption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp), **{"experiment.final_repeats": 2})
            stub = StubTransport(contrast="mitigates", decision="adopt_inv", final_contrast="regresses")
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root), "--max-tasks", "1"], stub), 0)
            ledger = Ledger(root / ".nanorsi" / "ledger.jsonl")
            self.assertEqual(ledger.count("rollback"), 1)
            done = next(row for row in ledger.events() if row["event"] == "task_done")
            self.assertEqual((done["chosen"], done["decisions"]), ("agg1keep", ["rollback"]))
            self.assertEqual(ledger.count("experience"), 0)
            kept = root / ".nanorsi" / "runs" / "ops__meeting-action-items" / "agg1keep"
            self.assertTrue((kept / "deliverables" / "action-items.md").is_file())
            self.assertEqual(cli.main(["freeze", "--workspace", str(root)]), 0)
            self.assertEqual(cli.main(["judge", "--workspace", str(root)]), 0)
            summary = report.summarize(ledger)
            self.assertEqual(summary["means"]["base"], summary["means"]["final"])


class CommandRunnerProtocolTests(unittest.TestCase):
    def test_external_runner_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp))
            script = root / "runner.py"
            script.write_text(
                "import json, os\n"
                "req = json.load(open(os.environ['NANORSI_REQUEST']))\n"
                "assert 'always_on' in req and os.path.isdir(req['harness_dir'])\n"
                "json.dump({'ok': True, 'delivered': True, 'trajectory': '[ACTION] external', "
                "'deliverables': {req['task']['deliverables'][0]: 'Priya 2026-11-03 vendor contract no owner Marcus status page budget freeze'}, "
                "'usage': {'calls': 1, 'input_tokens': 10, 'output_tokens': 2}}, open(os.environ['NANORSI_RESULT'], 'w'))\n")
            text = (root / "nanorsi.toml").read_text()
            text = cli._set_key(text, "runner", "kind", "command")
            text = cli._set_key(text, "runner", "command", [sys.executable, "runner.py"])
            (root / "nanorsi.toml").write_text(text)
            stub = StubTransport()
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root), "--max-tasks", "1"], stub), 0)
            self.assertNotIn("agent", stub.calls)                     # the external runner executed, not loopback
            self.assertEqual(cli.main(["freeze", "--workspace", str(root)]), 0)
            self.assertEqual(cli.main(["judge", "--workspace", str(root)]), 0)
            summary = report.summarize(Ledger(root / ".nanorsi" / "ledger.jsonl"))
            self.assertEqual(summary["means"]["base"], 1.0)


class WorkspaceCommandTests(unittest.TestCase):
    def test_new_configure_doctor(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "lab"
            self.assertEqual(cli.main(["new", str(dest), "--goal", "g"]), 0)
            key = Path(tmp) / "k.key"
            key.write_text("secret\n")
            self.assertEqual(cli.main(["configure", "--workspace", str(dest), "--model", "m", "--base-url",
                                       "https://x/v1", "--api-key-file", str(key)]), 0)
            config = load_config(dest / "nanorsi.toml")
            self.assertEqual((config.model.model, config.model.base_url), ("m", "https://x/v1"))
            self.assertEqual(cli.main(["doctor", "--workspace", str(dest)]), 0)
            self.assertEqual(cli.main(["configure", "--workspace", str(Path(tmp) / "nope"), "--model", "m",
                                       "--base-url", "u", "--api-key-file", str(key)]), 1)


if __name__ == "__main__":
    unittest.main()

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

    def test_seq_k2_chains_and_blind_selects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(Path(tmp), **{"experiment.mode": "seq", "experiment.k": 2})
            stub = StubTransport(contrast="mitigates", decision="adopt_inv", select_choice="B")
            self.assertEqual(_run_cli(["evolve", "--workspace", str(root), "--max-tasks", "1"], stub), 0)
            ledger = Ledger(root / ".nanorsi" / "ledger.jsonl")
            rollouts = [row["label"] for row in ledger.events() if row["event"] == "rollout"]
            self.assertEqual(rollouts, ["base1", "inv1", "dom1", "c1", "inv2", "dom2", "c2"])
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

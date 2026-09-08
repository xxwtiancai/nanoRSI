import math
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from nanorsi.evaluator import EvaluationError, parse_evaluation, run_evaluation


def schema2_payload(**overrides):
    payload = {
        "schema_version": 2,
        "status": "ok",
        "metrics": {"score": 0.75},
        "constraints": {"tests_passed": True},
        "case_results": [
            {
                "task_id": "task-1",
                "group_id": "group-1",
                "repeat_id": 0,
                "score": 0.75,
                "status": "ok",
                "trace": [],
                "skill_hashes": {},
                "usage": {
                    "model_calls": 1,
                    "input_tokens": 2,
                    "output_tokens": 3,
                    "cost_usd": 0.01,
                },
                "duration_ms": 12,
            }
        ],
        "cost_usd": 0.01,
        "duration_ms": 12,
        "usage": {
            "model_calls": 1,
            "input_tokens": 2,
            "output_tokens": 3,
            "cost_usd": 0.01,
        },
    }
    payload.update(overrides)
    return payload


class EpisodeContractTests(unittest.TestCase):
    def test_schema1_remains_compatible(self):
        result = parse_evaluation(
            {
                "schema_version": 1,
                "status": "ok",
                "metrics": {"score": 0.75},
                "constraints": {"tests_passed": True},
                "case_results": [],
                "cost_usd": None,
                "duration_ms": 12,
            }
        )
        self.assertEqual(result.metrics["score"], 0.75)
        self.assertEqual(result.usage, {})

    def test_schema2_validates_episode_shape(self):
        result = parse_evaluation(schema2_payload())
        self.assertEqual(result.case_results[0]["task_id"], "task-1")
        self.assertEqual(result.usage["model_calls"], 1)

    def test_schema2_requires_cases_and_usage(self):
        for field, value in (("case_results", []), ("usage", None)):
            payload = schema2_payload(**{field: value})
            with self.subTest(field=field):
                with self.assertRaises(EvaluationError):
                    parse_evaluation(payload)

    def test_schema2_rejects_invalid_cases_and_duplicates(self):
        invalid_cases = [
            {"score": float("nan")},
            {"score": -0.1},
            {"score": 1.1},
            {"repeat_id": True},
            {"status": "unknown"},
            {"trace": {}},
            {"skill_hashes": []},
            {"usage": {"model_calls": True}},
            {"duration_ms": -1},
        ]
        for update in invalid_cases:
            case = dict(schema2_payload()["case_results"][0])
            case.update(update)
            with self.subTest(update=update):
                with self.assertRaises(EvaluationError):
                    parse_evaluation(schema2_payload(case_results=[case]))
        duplicate = dict(schema2_payload()["case_results"][0])
        with self.assertRaises(EvaluationError):
            parse_evaluation(schema2_payload(case_results=[schema2_payload()["case_results"][0], duplicate]))

    def test_schema2_rejects_nonfinite_or_negative_usage_and_cost(self):
        for usage in (
            {"model_calls": True},
            {"input_tokens": -1},
            {"output_tokens": math.inf},
            {"cost_usd": -0.01},
        ):
            with self.subTest(usage=usage):
                with self.assertRaises(EvaluationError):
                    parse_evaluation(schema2_payload(usage=usage))
        for cost in (True, -0.1, math.nan, math.inf):
            with self.subTest(cost=cost):
                with self.assertRaises(EvaluationError):
                    parse_evaluation(schema2_payload(cost_usd=cost))

    def test_run_evaluation_merges_extra_environment_and_enforces_result_limit(self):
        config = SimpleNamespace(
            evaluator=SimpleNamespace(
                command=[
                    sys.executable,
                    "-c",
                    "import json, os; print(os.environ['EXTRA']); open(os.environ['NANORSI_RESULT_PATH'], 'w').write(json.dumps({'schema_version': 1, 'status': 'ok', 'metrics': {'score': 1}, 'constraints': {}, 'case_results': [], 'cost_usd': None, 'duration_ms': 0}))",
                ],
                timeout_s=2,
                primary_metric="score",
            ),
            budget=SimpleNamespace(max_output_bytes=512),
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = run_evaluation(config, Path(tmp), "validation", Path(tmp) / "result.json", {"EXTRA": "present"})
        self.assertEqual(result.metrics["score"], 1.0)

    def test_run_evaluation_rejects_oversize_result_json(self):
        config = SimpleNamespace(
            evaluator=SimpleNamespace(
                command=[
                    sys.executable,
                    "-c",
                    "import os; open(os.environ['NANORSI_RESULT_PATH'], 'w').write('{\"schema_version\":1,\"status\":\"ok\",\"metrics\":{\"score\":1},\"constraints\":{\"x\":\"' + 'x' * 200 + '\"},\"case_results\":[],\"cost_usd\":null,\"duration_ms\":0}')",
                ],
                timeout_s=2,
                primary_metric="score",
            ),
            budget=SimpleNamespace(max_output_bytes=64),
        )
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(EvaluationError, "exceeds"):
                run_evaluation(config, Path(tmp), "validation", Path(tmp) / "result.json")

    def test_run_evaluation_rejects_invalid_utf8_result(self):
        config = SimpleNamespace(
            evaluator=SimpleNamespace(
                command=[
                    sys.executable,
                    "-c",
                    "import os; open(os.environ['NANORSI_RESULT_PATH'], 'wb').write(b'\\xff')",
                ],
                timeout_s=2,
                primary_metric="score",
            ),
            budget=SimpleNamespace(max_output_bytes=64),
        )
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(EvaluationError, "invalid evaluator JSON"):
                run_evaluation(config, Path(tmp), "validation", Path(tmp) / "result.json")


if __name__ == "__main__":
    unittest.main()

import unittest

from nanorsi.evaluator import EvaluationResult, EvaluationError, parse_evaluation
from nanorsi.gate import GateConfig, decide


class EvaluationTests(unittest.TestCase):
    def test_parses_valid_evaluation(self):
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
        self.assertIsInstance(result, EvaluationResult)
        self.assertEqual(result.metrics["score"], 0.75)

    def test_rejects_missing_nonfinite_and_wrong_schema(self):
        payloads = [
            {},
            {
                "schema_version": 2,
                "status": "ok",
                "metrics": {"score": 1},
                "constraints": {},
            },
            {
                "schema_version": 1,
                "status": "ok",
                "metrics": {"score": float("nan")},
                "constraints": {},
            },
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(EvaluationError):
                    parse_evaluation(payload)

    def test_gate_accepts_rejects_and_marks_inconclusive(self):
        config = GateConfig(
            minimum_improvement=0.1,
            required_constraints=["tests_passed"],
            max_heldout_regression=0.1,
        )
        accepted = decide(
            config,
            parent={"score": 0.5, "constraints": {"tests_passed": True}},
            child={"score": 0.65, "constraints": {"tests_passed": True}},
            parent_heldout={"score": 0.6},
            child_heldout={"score": 0.58},
        )
        self.assertEqual(accepted.decision, "accepted")
        rejected = decide(
            config,
            parent={"score": 0.5, "constraints": {"tests_passed": True}},
            child={"score": 0.55, "constraints": {"tests_passed": True}},
            parent_heldout={"score": 0.6},
            child_heldout={"score": 0.6},
        )
        self.assertEqual(rejected.decision, "rejected")
        inconclusive = decide(
            config,
            parent={"score": 0.5, "constraints": {"tests_passed": True}},
            child={"score": 0.65, "constraints": {"tests_passed": False}},
            parent_heldout={"score": 0.6},
            child_heldout={"score": 0.6},
        )
        self.assertEqual(inconclusive.decision, "inconclusive")


if __name__ == "__main__":
    unittest.main()

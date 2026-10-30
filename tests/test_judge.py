import unittest

from nanorsi.judge import _parse_score


class JudgeScoreTests(unittest.TestCase):
    def test_parse_score_rejects_out_of_range_counts(self):
        for data in (
            {"n_passed": -1, "n_criteria": 3},
            {"n_passed": 4, "n_criteria": 3},
            {"n_passed": 1, "n_criteria": 0},
        ):
            with self.subTest(data=data):
                self.assertIsNone(_parse_score(data))

    def test_parse_score_rejects_boolean_counts_and_preserves_valid_score(self):
        self.assertIsNone(_parse_score({"n_passed": True, "n_criteria": 1}))
        self.assertEqual(
            _parse_score({"n_passed": 2, "n_criteria": 3, "all_pass": False}),
            {"n_passed": 2, "n_criteria": 3, "all_pass": False},
        )


if __name__ == "__main__":
    unittest.main()

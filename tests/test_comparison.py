import importlib.util
import json
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREPARE = load_module("prepare_tasks", ROOT / "examples" / "local_tasks" / "prepare.py")
COMPARE = load_module("compare_reports", ROOT / "examples" / "compare.py")


def make_report(*, seed=1, arm="candidate-arm", experiment_id="experiment-a",
                comparison_hash="comparison-a", repeat_ids=(1, 2), baseline_cost=1.0,
                candidate_cost=2.0, no_skills_cost=1.5):
    scores = {
        "baseline": {("task-a", 1): 0.5, ("task-a", 2): 0.7,
                      ("task-a", 3): 0.9, ("task-b", 1): 1.0,
                      ("task-b", 2): 0.8, ("task-b", 3): 0.6},
        "no-skills": {("task-a", 1): 0.6, ("task-a", 2): 0.8,
                      ("task-a", 3): 0.7, ("task-b", 1): 0.9,
                      ("task-b", 2): 0.9, ("task-b", 3): 0.9},
        "candidate": {("task-a", 1): 0.8, ("task-a", 2): 0.8,
                      ("task-a", 3): 0.8, ("task-b", 1): 1.0,
                      ("task-b", 2): 1.0, ("task-b", 3): 1.0},
    }
    costs = {"baseline": baseline_cost, "no-skills": no_skills_cost,
             "candidate": candidate_cost}
    results = []
    for condition in ("baseline", "no-skills", "candidate"):
        for repeat_id in repeat_ids:
            cases = []
            for task_id, group_id in (("task-a", "group-a"), ("task-b", "group-b")):
                cases.append({
                    "task_id": task_id,
                    "group_id": group_id,
                    "repeat_id": repeat_id,
                    "score": scores[condition][(task_id, repeat_id)],
                    "status": "ok",
                    "duration_ms": repeat_id * 10 + (1 if task_id == "task-a" else 2),
                })
            results.append({
                "condition": condition,
                "repeat_id": repeat_id,
                "case_results": cases,
                "cost_usd": costs[condition],
                "duration_ms": 10000 + repeat_id,
            })
    return {
        "schema_version": 2,
        "manifest_hash": "manifest-a",
        "experiment_id": "experiment-a",
        "arm": arm,
        "seed": seed,
        "comparison_hash": comparison_hash,
        "results": results,
    }


class PrepareManifestTests(unittest.TestCase):
    def test_manifest_is_deterministic_and_has_disjoint_split_groups(self):
        first = PREPARE.build_manifest()
        second = PREPARE.build_manifest()
        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], 1)
        tasks = first["tasks"]
        self.assertEqual(len(tasks), 90)
        self.assertEqual({task["split"] for task in tasks}, {"train", "validation", "test"})
        self.assertEqual({split: sum(task["split"] == split for task in tasks)
                          for split in ("train", "validation", "test")},
                         {"train": 30, "validation": 30, "test": 30})
        self.assertEqual(len({task["task_id"] for task in tasks}), 90)
        groups_by_split = {
            split: {task["group_id"] for task in tasks if task["split"] == split}
            for split in ("train", "validation", "test")
        }
        self.assertEqual(set.intersection(*groups_by_split.values()), set())
        source_fixtures = {
            json.dumps(task["input_files"], sort_keys=True)
            for task in tasks
        }
        self.assertEqual(len(source_fixtures), 90)

    def test_tasks_are_text_edit_fixtures_with_complete_expected_files(self):
        tasks = PREPARE.build_manifest()["tasks"]
        self.assertGreaterEqual(len({task["instruction"] for task in tasks}), 30)
        for task in tasks:
            with self.subTest(task_id=task["task_id"]):
                self.assertTrue(task["input_files"])
                self.assertEqual(set(task["input_files"]), set(task["expected_files"]))
                self.assertTrue(all(Path(path).suffix in {".txt", ".md", ".ini", ".cfg", ".yaml"}
                                    for path in task["input_files"]))
                self.assertTrue(all(isinstance(value, str) for value in task["input_files"].values()))
                self.assertTrue(all(isinstance(value, str) for value in task["expected_files"].values()))


class CompareReportsTests(unittest.TestCase):
    def test_two_condition_model_reports_are_supported(self):
        report = make_report()
        report.update(mode='model', conditions=['baseline', 'candidate'], metric={'name': 'score', 'direction': 'maximize'})
        report['results'] = [r for r in report['results'] if r['condition'] != 'no-skills']
        summary = COMPARE.summarize([report])
        self.assertEqual(set(summary['conditions']), {'baseline', 'candidate'})
        self.assertIsNone(summary['no_skills_delta_pp'])
        self.assertGreater(summary['candidate_baseline_delta_pp'], 0)

    def test_non_score_metric_cannot_be_mislabeled_as_percentage_points(self):
        report = make_report()
        report['metric'] = {'name': 'loss', 'direction': 'minimize'}
        with self.assertRaisesRegex(ValueError, 'score'):
            COMPARE.summarize([report])

    def test_task_macro_averages_repeats_before_tasks_and_reports_deltas(self):
        summary = COMPARE.summarize([make_report()])
        self.assertAlmostEqual(summary["conditions"]["baseline"]["task_macro"], 0.75)
        self.assertAlmostEqual(summary["conditions"]["candidate"]["task_macro"], 0.9)
        self.assertAlmostEqual(summary["candidate_baseline_delta_pp"], 15.0)
        self.assertAlmostEqual(summary["no_skills_delta_pp"], 5.0)

    def test_rejects_mismatched_condition_pairs(self):
        report = make_report()
        report["results"] = [result for result in report["results"]
                              if not (result["condition"] == "candidate" and result["repeat_id"] == 2)]
        with self.assertRaises(ValueError):
            COMPARE.summarize([report])

    def test_rejects_duplicate_experiment_arm_seed(self):
        with self.assertRaises(ValueError):
            COMPARE.summarize([make_report(), make_report()])

    def test_rejects_nonfinite_score_and_cost(self):
        bad_score = make_report()
        bad_score["results"][0]["case_results"][0]["score"] = math.nan
        with self.assertRaises(ValueError):
            COMPARE.summarize([bad_score])
        bad_cost = make_report()
        bad_cost["results"][0]["cost_usd"] = math.inf
        with self.assertRaises(ValueError):
            COMPARE.summarize([bad_cost])

    def test_rejects_out_of_range_or_negative_values(self):
        for score in (-0.01, 1.01):
            report = make_report()
            report["results"][0]["case_results"][0]["score"] = score
            with self.subTest(score=score), self.assertRaises(ValueError):
                COMPARE.summarize([report])
        negative_cost = make_report()
        negative_cost["results"][0]["cost_usd"] = -0.01
        with self.assertRaises(ValueError):
            COMPARE.summarize([negative_cost])
        negative_duration = make_report()
        negative_duration["results"][0]["duration_ms"] = -1
        with self.assertRaises(ValueError):
            COMPARE.summarize([negative_duration])
        negative_case_duration = make_report()
        negative_case_duration["results"][0]["case_results"][0]["duration_ms"] = -1
        with self.assertRaises(ValueError):
            COMPARE.summarize([negative_case_duration])

    def test_rejects_huge_integer_overflow_and_non_integer_ids(self):
        huge_score = make_report()
        huge_score["results"][0]["case_results"][0]["score"] = 10 ** 1000
        with self.assertRaises(ValueError):
            COMPARE.summarize([huge_score])
        for seed in (True, -1, 1.0, "1"):
            with self.subTest(seed=seed), self.assertRaises(ValueError):
                COMPARE.summarize([make_report(seed=seed)])
        for repeat_id in (-1, True, 1.0, "1"):
            bad_repeat = make_report()
            bad_repeat["results"][0]["repeat_id"] = repeat_id
            with self.subTest(repeat_id=repeat_id), self.assertRaises(ValueError):
                COMPARE.summarize([bad_repeat])

    def test_requires_common_comparison_hash_but_allows_manifest_hash_differences(self):
        first = make_report()
        second = make_report(seed=2, experiment_id="experiment-b")
        second["manifest_hash"] = "manifest-for-another-arm-and-seed"
        self.assertEqual(COMPARE.summarize([first, second])["report_count"], 2)
        second["comparison_hash"] = "different-frozen-data"
        with self.assertRaises(ValueError):
            COMPARE.summarize([first, second])
        missing = make_report()
        del missing["comparison_hash"]
        with self.assertRaises(ValueError):
            COMPARE.summarize([missing])

    def test_weights_independent_runs_equally_despite_repeat_count(self):
        one_repeat = make_report(repeat_ids=(1,), seed=1, experiment_id="one")
        three_repeats = make_report(repeat_ids=(1, 2, 3), seed=2, experiment_id="three")
        for report, baseline, candidate, no_skills in (
            (one_repeat, 0.0, 1.0, 0.0),
            (three_repeats, 1.0, 1.0, 1.0),
        ):
            for result in report["results"]:
                value = {"baseline": baseline, "candidate": candidate,
                         "no-skills": no_skills}[result["condition"]]
                for case in result["case_results"]:
                    case["score"] = value
        summary = COMPARE.summarize([one_repeat, three_repeats])
        self.assertAlmostEqual(summary["candidate_baseline_delta_pp"], 50.0)

    def test_groups_arm_summaries_and_uses_case_timing(self):
        frozen = make_report(arm="frozen", seed=1, experiment_id="frozen-run")
        self_use = make_report(arm="self-use", seed=2, experiment_id="self-use-run")
        summary = COMPARE.summarize([frozen, self_use])
        self.assertEqual(summary["arms"]["frozen"]["run_count"], 1)
        self.assertEqual(summary["arms"]["self-use"]["run_count"], 1)
        self.assertAlmostEqual(summary["arms"]["frozen"]["mean_candidate_baseline_delta_pp"], 15.0)
        self.assertEqual(summary["conditions"]["baseline"]["duration_ms"]["median_ms"], 16.5)
        self.assertEqual(summary["conditions"]["baseline"]["duration_ms"]["p95_ms"], 22.0)

    def test_unknown_cost_is_not_counted_as_zero(self):
        report = make_report(candidate_cost=None)
        report["results"][-1]["cost_usd"] = 1.25
        summary = COMPARE.summarize([report])
        cost = summary["conditions"]["candidate"]["cost_usd"]
        self.assertIsNone(cost["total_usd"])
        self.assertAlmostEqual(cost["known_usd"], 1.25)
        self.assertEqual(cost["known_count"], 1)
        self.assertEqual(cost["total_count"], 2)
        self.assertEqual(cost["coverage"], 0.5)


if __name__ == "__main__":
    unittest.main()

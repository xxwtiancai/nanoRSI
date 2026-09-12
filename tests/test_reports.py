import json
import tempfile
import unittest
from pathlib import Path

from nanorsi.report import write_report


def final_events():
    events = [{"event_type": "freeze", "repeats": 2, "experiment_id": "coding-lab", "arm": "frozen", "seed": 0}]
    for condition, scores in [("baseline", [0, 1]), ("no-skills", [0, 0]), ("candidate", [1, 1])]:
        for repeat in range(2):
            cases = [{"task_id": f"task-{i}", "repeat_id": repeat, "score": score} for i, score in enumerate(scores)]
            events.append({"event_type": "final_result", "key": f"{condition}-{repeat}",
                           "result": {"condition": condition, "repeat_id": repeat, "case_results": cases}})
    return events


class ReportTests(unittest.TestCase):
    def render(self, events):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        path = write_report(root, events)
        return path.read_text(), (root / "reports/report.html").read_text(), root

    def test_reports_final_comparison_and_unknown_costs(self):
        markdown, html, root = self.render(final_events())
        self.assertIn("50.0%", markdown)
        self.assertIn("+50.0 pp", markdown)
        self.assertIn("+50.0 pp", html)
        self.assertIn("Unknown", html)
        self.assertIn("2 tasks", html)
        self.assertEqual(json.loads((root / "reports/report.json").read_text()), final_events())

    def test_html_escapes_untrusted_content_and_shows_failed_attempts(self):
        events = [{"event_type": "attempt_failed", "attempt_id": 1, "decision": "rejected",
                   "reason": '<script>alert("private")</script>'}]
        markdown, html, _ = self.render(events)
        self.assertNotIn('<script>alert(', html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("rejected", html)
        self.assertIn("Final evaluation pending", html)
        self.assertNotIn("fixed model, versioned skills, frozen evaluation", html)
        self.assertNotIn("+0.0 pp", html)

    def test_partial_final_panel_does_not_claim_improvement(self):
        markdown, html, _ = self.render(final_events()[:-1])
        self.assertIn("Final evaluation pending", html)
        self.assertNotIn("+50.0 pp", html)

    def test_rejects_mismatched_or_duplicate_final_task_pairs(self):
        for mismatch in (True, False):
            events = final_events()
            cases = events[-1]["result"]["case_results"]
            if mismatch:
                cases[0]["task_id"] = "different-task"
            else:
                cases.append(dict(cases[0]))
            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                self.render(events)

    def test_rejects_invalid_final_scores(self):
        for score in (True, float("nan"), -1, 1.1):
            events = final_events()
            events[-1]["result"]["case_results"][0]["score"] = score
            with self.subTest(score=score), self.assertRaises(ValueError):
                self.render(events)

    def test_html_format_returns_html_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(write_report(Path(tmp), [], format="html").name, "report.html")


if __name__ == "__main__":
    unittest.main()

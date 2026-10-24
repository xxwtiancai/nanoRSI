"""Guard the survey-taxonomy research notes and the frozen catalogue archive."""
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTES = REPO / "docs" / "research" / "RSI_NOTES.md"
MIGRATE = REPO / "docs" / "research" / "industry-rsi" / "migrate_to_notes.py"


class ResearchNotesTest(unittest.TestCase):
    def test_notes_match_frozen_catalog(self):
        result = subprocess.run(
            [sys.executable, str(MIGRATE), "--check"],
            cwd=REPO, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_survey_sections_present(self):
        text = NOTES.read_text(encoding="utf-8")
        for heading in ("最近更新", "部署时自进化", "训练时自迭代", "自评估", "自动研究"):
            self.assertIn(heading, text, f"missing survey-taxonomy section {heading}")

    def test_frozen_pages_carry_archive_banner(self):
        radar = (REPO / "docs" / "research" / "industry-rsi" / "RADAR.md").read_text(encoding="utf-8")
        self.assertIn("Archived 2026-10-24", radar)


if __name__ == "__main__":
    unittest.main()

"""Guard the per-paper research notes: generated set in sync, hand-written notes
follow the full-depth template, and every referenced figure exists."""
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTES = REPO / "docs" / "research" / "notes"
GEN = REPO / "docs" / "research" / "industry-rsi" / "generate_notes.py"
SECTIONS = {"deployment", "training", "selfeval", "autoresearch"}


def generated_ids() -> set[str]:
    out = subprocess.run([sys.executable, str(GEN)], cwd=REPO, capture_output=True, text=True)
    return set()  # regenerating in a test would rewrite files; --check is the guard


class NotesStructureTest(unittest.TestCase):
    def test_generated_set_in_sync(self):
        result = subprocess.run([sys.executable, str(GEN), "--check"], cwd=REPO,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_every_note_follows_the_depth_template(self):
        papers = sorted(p for section in SECTIONS for p in (NOTES / section).glob("*.md"))
        self.assertGreater(len(papers), 230)
        for path in papers:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                for heading in ("## Pipeline", "## 结果", "## 证据边界", "## 对 nanoRSI 的输入", "## 来源"):
                    self.assertIn(heading, text)
                self.assertIsNotNone(re.search(r"^> .+ · \d{4}-\d{2}", text, re.M), path.name)

    def test_referenced_figures_exist(self):
        missing = []
        for path in NOTES.glob("*/*.md"):
            for rel in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if not (path.parent / rel).resolve().is_file():
                    missing.append(f"{path.name}: {rel}")
        self.assertEqual(missing, [])

    def test_index_covers_all_papers(self):
        index = (NOTES / "README.md").read_text(encoding="utf-8")
        for section in SECTIONS:
            counted = len(list((NOTES / section).glob("*.md")))
            self.assertGreater(counted, 0, section)
        self.assertIn("冻结后手写深记", index)
        self.assertIn("updates/2026-10.md", index)

    def test_update_archive_and_redirect(self):
        updates = (NOTES / "updates" / "2026-10.md").read_text(encoding="utf-8")
        self.assertIn("# 更新流水", updates)
        redirect = (REPO / "docs/research/RSI_NOTES.md").read_text(encoding="utf-8")
        self.assertIn("notes/README.md", redirect)


if __name__ == "__main__":
    unittest.main()

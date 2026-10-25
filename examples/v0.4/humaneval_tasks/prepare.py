"""Build the deterministic HumanEval coding task pack (benchmark track).

HumanEval (openai/human-eval, MIT) is the field's standard code-generation
benchmark: 164 problems, each a Python function specified by a prompt with a
docstring (including >>> examples) and verified by execution of the upstream
test block. This pack maps every problem onto the stock coding template:
the agent implements ``solution.py`` from the prompt (public test checks only
that the entry point exists, preserving official prompt-only semantics), and
the upstream test block — wrapped in unittest — runs as the private grader.
Reference solutions never enter the workspace: ``expected_files`` carries a
placeholder because grading executes tests and never compares contents.

Splits are deterministic (sorted task_id, strided subsample): 20 train /
25 validation / 36 test. The manifest is always regenerated, never edited.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import indent

TRAIN_COUNT, VALIDATION_COUNT, TEST_COUNT = 20, 25, 36
TEST_TIMEOUT_S = 10
WITHHELD = "# reference solution withheld; private tests decide\n"
# Upstream defects: these tests reference helpers that the problem never defines
# (poly / encode_cyclic / encode_shift), so even the canonical solution cannot
# pass them under any faithful wrapper. Excluded transparently, not silently.
EXCLUDED_UPSTREAM = {"HumanEval/32", "HumanEval/38", "HumanEval/50"}


def _public_test(entry_point: str) -> str:
    return ("import unittest\nimport solution\n\n\nclass Checks(unittest.TestCase):\n"
            "    def test_solution_present(self):\n"
            f"        self.assertTrue(callable(getattr(solution, \"{entry_point}\", None)))\n")


def _private_test(entry_point: str, upstream_test: str) -> str:
    # Upstream fields define check(candidate) without calling it (the official
    # harness invokes check itself); bare-assert fields run as inlined checks.
    body = upstream_test if "def check(" not in upstream_test else upstream_test + "\ncheck(candidate)\n"
    return ("import unittest\nimport solution\nfrom solution import " + entry_point +
            "\ncandidate = " + entry_point + "\n\n\nclass Checks(unittest.TestCase):\n"
            "    def test_humaneval_private(self):\n" + indent(body, " " * 8) + "\n")


def _sample(rows: list[dict], count: int, residue: int) -> list[dict]:
    stride = max(2, len(rows) // max(1, count))
    return [row for index, row in enumerate(rows) if index % stride == residue][:count]


def _task(row: dict, split: str, index: int) -> dict:
    entry = row["entry_point"]
    return {
        "task_id": f"{split}-{index:03d}-{entry}",
        "group_id": f"{split}-problems",
        "split": split,
        "instruction": f"Implement {entry} in solution.py so it satisfies the docstring prompt.",
        "input_files": {"solution.py": row["prompt"] + "    pass\n"},
        "expected_files": {"solution.py": WITHHELD},
        "grading": {"kind": "python-unittest",
                    "public_tests": {"test_public.py": _public_test(entry)},
                    "private_tests": {"test_private.py": _private_test(entry, row["test"])},
                    "timeout_s": TEST_TIMEOUT_S},
    }


def _load_rows() -> list[dict]:
    rows = [json.loads(line) for line
            in (Path(__file__).with_name("data") / "HumanEval.jsonl").read_text().splitlines() if line.strip()]
    rows = [row for row in rows if row["task_id"] not in EXCLUDED_UPSTREAM]
    rows.sort(key=lambda row: row["task_id"])
    return rows


def build_manifest(train_count: int = TRAIN_COUNT, validation_count: int = VALIDATION_COUNT,
                   test_count: int = TEST_COUNT) -> dict:
    rows = _load_rows()
    tasks = ([_task(row, "train", i) for i, row in enumerate(_sample(rows, train_count, 0))]
             + [_task(row, "validation", i) for i, row in enumerate(_sample(rows, validation_count, 1))]
             + [_task(row, "test", i) for i, row in enumerate(_sample(rows, test_count, 2))])
    return {"schema_version": 1, "tasks": tasks}


def write_pack(output: Path, train_count: int = TRAIN_COUNT,
               validation_count: int = VALIDATION_COUNT, test_count: int = TEST_COUNT) -> Path:
    directory = output / "humaneval"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "manifest.json"
    path.write_text(json.dumps(
        build_manifest(train_count, validation_count, test_count),
        indent=1, ensure_ascii=False) + "\n")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the deterministic HumanEval task pack.")
    parser.add_argument("output", nargs="?", default=Path(__file__).with_name("out"))
    parser.add_argument("--train", type=int, default=TRAIN_COUNT)
    parser.add_argument("--validation", type=int, default=VALIDATION_COUNT)
    parser.add_argument("--test", type=int, default=TEST_COUNT)
    args = parser.parse_args(argv)
    print(write_pack(Path(args.output), args.train, args.validation, args.test))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

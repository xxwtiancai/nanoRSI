"""Build deterministic BIG-Bench-Hard (BBH) program-evolution task packs.

Phase 1 of ADOPTION item 37: move effect evidence from self-authored panels
onto public benchmark tasks. Two BBH tasks are vendored verbatim under data/
(MIT, see NOTICE): dyck_languages and boolean_expressions. Each example becomes
one program-mode task (stdin records.json, stdout summary.json, exact-match
grading by the stock program evaluator). The initial solver programs below are
authored by nanoRSI as deliberately weak classical heuristics; BBH provides
data only. Examples are sorted by input text and split deterministically
(50 train / 50 validation / 150 test); the manifest is always regenerated and
must never be hand-edited.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SPLITS = ((("train", 50)), (("validation", 50)), (("test", 150)))

DYCK_PROGRAM = '''# BBH dyck_languages task pack for nanoRSI (benchmark track).
# Data: BIG-Bench-Hard (MIT, Copyright 2022 the BBH authors), vendored verbatim; see NOTICE.
# Initial solver authored by nanoRSI: a deliberately weak count-based heuristic.
# The solver function may be improved; the stdin/stdout contract below must stay fixed.
"""Complete a bracket sequence: print the missing closing brackets in order."""
import json
import sys


def solve(text):
    prefix = text.split("Input:", 1)[1]
    opens = {"(": ")", "[": "]", "{": "}", "<": ">"}
    stack = []
    for token in prefix.split():
        if token in opens:
            stack.append(token)
        elif stack and opens[stack[-1]] == token:
            stack.pop()
    counts = {}
    for token in stack:
        counts[token] = counts.get(token, 0) + 1
    closing = []
    for opener in "([{<":
        closing.extend([opens[opener]] * counts.get(opener, 0))
    return " ".join(closing)


def main():
    payload = json.load(sys.stdin)
    print(json.dumps({"answer": solve(payload["input"])}))


if __name__ == "__main__":
    main()
'''

BOOL_PROGRAM = '''# BBH boolean_expressions task pack for nanoRSI (benchmark track).
# Data: BIG-Bench-Hard (MIT, Copyright 2022 the BBH authors), vendored verbatim; see NOTICE.
# Initial solver authored by nanoRSI: a deliberately weak left-to-right evaluator.
# The solver function may be improved; the stdin/stdout contract below must stay fixed.
"""Evaluate a nested boolean expression: print True or False."""
import json
import sys


def solve(text):
    tokens = text.strip()
    if tokens.endswith(" is"):
        tokens = tokens[:-3]
    tokens = tokens.replace("(", " ( ").replace(")", " ) ").split()

    def parse(items):
        value = None
        operator = None
        negations = 0
        index = 0
        while index < len(items):
            item = items[index]
            if item == "not":
                negations += 1
            elif item in ("and", "or"):
                operator = item
            elif item == "(":
                depth = 1
                end = index + 1
                while end < len(items) and depth:
                    if items[end] == "(":
                        depth += 1
                    elif items[end] == ")":
                        depth -= 1
                    end += 1
                inner = parse(items[index + 1:end - 1])
                value = _combine(value, operator, inner)
                index = end - 1
            elif item != ")":
                literal = item == "True"
                if negations:
                    literal = not literal
                    negations = 0
                value = _combine(value, operator, literal)
            index += 1
        return value

    return str(parse(tokens))


def _combine(value, operator, literal):
    if value is None:
        return literal
    if operator == "and":
        return value and literal
    return value or literal


def main():
    payload = json.load(sys.stdin)
    print(json.dumps({"answer": solve(payload["input"])}))


if __name__ == "__main__":
    main()
'''

PACKS = (
    ("dyck", "dyck_languages.json", DYCK_PROGRAM,
     "Complete the rest of the bracket sequence from records.json input; print "
     "summary.json with the exact space-separated closing brackets."),
    ("bool", "boolean_expressions.json", BOOL_PROGRAM,
     "Evaluate the boolean expression from records.json input; print summary.json "
     "with the exact answer True or False."),
)


def build_pack(source: Path, instruction: str) -> dict:
    examples = json.loads(source.read_text())["examples"]
    ordered = sorted(examples, key=lambda item: (item["input"], item["target"]))
    tasks, start = [], 0
    for split, size in SPLITS:
        chunk = ordered[start:start + size]
        start += size
        for offset, example in enumerate(chunk):
            record = json.dumps({"input": example["input"]}, ensure_ascii=False)
            expected = json.dumps({"answer": example["target"]}, ensure_ascii=False)
            tasks.append({
                "task_id": f"{split}-{offset:03d}",
                "group_id": f"{split}-examples",
                "split": split,
                "instruction": instruction,
                "input_files": {"records.json": record},
                "expected_files": {"summary.json": expected},
            })
    return {"schema_version": 1, "tasks": tasks}


def write_packs(output: Path) -> list[Path]:
    written = []
    for name, data_name, program, instruction in PACKS:
        manifest = build_pack(Path(__file__).with_name("data") / data_name, instruction)
        directory = output / name
        (directory / "tasks").mkdir(parents=True, exist_ok=True)
        (directory / "target").mkdir(parents=True, exist_ok=True)
        manifest_path = directory / "tasks" / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
        (directory / "target" / "program.py").write_text(program)
        written.append(manifest_path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write deterministic BBH task packs.")
    parser.add_argument("output", nargs="?", default=Path(__file__).with_name("out"),
                        help="output directory (receives <name>/tasks/manifest.json and <name>/target/program.py)")
    args = parser.parse_args(argv)
    for path in write_packs(Path(args.output)):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

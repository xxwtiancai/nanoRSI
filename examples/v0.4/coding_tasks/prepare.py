"""Generate twelve independently authored Python utility bugfix starter tasks.

This small teaching/experiment pack is not an independent published benchmark.
Reference sources are fixtures for testing the pack, never exact-match graders.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from textwrap import dedent, indent


def source(text: str) -> str:
    return dedent(text).strip() + "\n"


def tests(body: str) -> str:
    return ("import unittest\nimport solution\n\n\nclass Checks(unittest.TestCase):\n"
            + indent(source(body), "    ") + "\n")


def task(name, split, instruction, broken, reference, public, private):
    return {
        "task_id": f"{split}-{name}", "group_id": name, "split": split,
        "instruction": "Fix solution.py. " + instruction,
        "input_files": {"solution.py": source(broken)},
        "expected_files": {"solution.py": source(reference)},
        "grading": {"kind": "python-unittest", "timeout_s": 2,
                    "public_tests": {"test_public.py": tests(public)},
                    "private_tests": {"test_private.py": tests(private)}},
    }


def build_manifest() -> dict[str, object]:
    tasks = [
        task("stable-dedup", "train",
             "unique(items) returns a list retaining the first occurrence of each equal value in input "
             "order. Accept any iterable and equality-comparable values, including unhashable lists "
             "and dictionaries. Do not mutate the input.",
             """
             def unique(items):
                 return sorted(set(items))
             """,
             """
             def unique(items):
                 result = []
                 for item in items:
                     if item not in result:
                         result.append(item)
                 return result
             """,
             """
             def test_order(self):
                 self.assertEqual(solution.unique([3, 1, 3, 2]), [3, 1, 2])
             def test_empty(self):
                 self.assertEqual(solution.unique([]), [])
             """,
             """
             def test_unhashable_and_input(self):
                 values = [[2], [1], [2], {'a': 1}, {'a': 1}]
                 self.assertEqual(solution.unique(values), [[2], [1], {'a': 1}])
                 self.assertEqual(len(values), 5)
             def test_generator(self):
                 self.assertEqual(solution.unique(x % 3 for x in range(8)), [0, 1, 2])
             """),
        task("iterable-chunks", "train",
             "chunks(items, size) returns a list of consecutive lists of at most size elements, "
             "including any final partial chunk. Accept finite iterables, including one-shot "
             "generators. size is an integer; raise ValueError when it is not positive. Empty "
             "input produces an empty list and input collections must remain unchanged.",
             """
             def chunks(items, size):
                 values = list(items)
                 return [values[i:i + size] for i in range(0, len(values) - size + 1, size)]
             """,
             """
             def chunks(items, size):
                 if size <= 0:
                     raise ValueError('size must be positive')
                 result, current = [], []
                 for item in items:
                     current.append(item)
                     if len(current) == size:
                         result.append(current)
                         current = []
                 if current:
                     result.append(current)
                 return result
             """,
             """
             def test_partial(self):
                 self.assertEqual(solution.chunks([1, 2, 3], 2), [[1, 2], [3]])
             def test_empty(self):
                 self.assertEqual(solution.chunks([], 2), [])
             """,
             """
             def test_generator_and_large_size(self):
                 self.assertEqual(solution.chunks(iter(range(5)), 3), [[0, 1, 2], [3, 4]])
                 self.assertEqual(solution.chunks([7], 10), [[7]])
             def test_invalid_size(self):
                 for size in (0, -3):
                     with self.assertRaises(ValueError):
                         solution.chunks([], size)
             def test_input(self):
                 values = [2, 4, 6]
                 solution.chunks(values, 1)
                 self.assertEqual(values, [2, 4, 6])
             """),
        task("nested-merge", "train",
             "merge(base, override) returns a recursively merged dictionary: recurse only when "
             "both values are dictionaries; otherwise the override replaces the base value. "
             "Retain keys absent from override. Neither input nor its nested mutable values may "
             "be changed or aliased by the result. Inputs contain acyclic built-in containers.",
             """
             def merge(base, override):
                 return {**base, **override}
             """,
             """
             from copy import deepcopy

             def merge(base, override):
                 result = deepcopy(base)
                 for key, value in override.items():
                     if isinstance(result.get(key), dict) and isinstance(value, dict):
                         result[key] = merge(result[key], value)
                     else:
                         result[key] = deepcopy(value)
                 return result
             """,
             """
             def test_nested(self):
                 self.assertEqual(solution.merge({'db': {'host': 'a', 'port': 9}},
                                                 {'db': {'port': 10}}),
                                  {'db': {'host': 'a', 'port': 10}})
             def test_override(self):
                 self.assertEqual(solution.merge({'x': [1]}, {'x': [2]}), {'x': [2]})
             """,
             """
             def test_independent_result(self):
                 base, override = {'left': {'x': [1]}}, {'right': [2]}
                 result = solution.merge(base, override)
                 result['left']['x'].append(9)
                 result['right'].append(8)
                 self.assertEqual(base, {'left': {'x': [1]}})
                 self.assertEqual(override, {'right': [2]})
             def test_type_replacement(self):
                 self.assertEqual(solution.merge({'a': {'x': 1}, 'b': None},
                                                 {'a': None, 'b': {'y': 2}}),
                                  {'a': None, 'b': {'y': 2}})
             """),
        task("boolean-setting", "train",
             "parse_bool(value, default=False) accepts None (return default), booleans (return "
             "unchanged), and strings. Strip surrounding whitespace and ignore case; true/yes/on/1 "
             "mean True and false/no/off/0 mean False. Other strings raise ValueError. Other input "
             "types raise TypeError; do not silently coerce numbers or containers.",
             """
             def parse_bool(value, default=False):
                 if value is None:
                     return default
                 return bool(value)
             """,
             """
             def parse_bool(value, default=False):
                 if value is None:
                     return default
                 if isinstance(value, bool):
                     return value
                 if not isinstance(value, str):
                     raise TypeError('expected a string, boolean, or None')
                 token = value.strip().lower()
                 if token in {'true', 'yes', 'on', '1'}:
                     return True
                 if token in {'false', 'no', 'off', '0'}:
                     return False
                 raise ValueError('unknown boolean token')
             """,
             """
             def test_false_string(self):
                 self.assertIs(solution.parse_bool('false'), False)
             def test_true_and_default(self):
                 self.assertIs(solution.parse_bool(' YES '), True)
                 self.assertIs(solution.parse_bool(None, True), True)
             """,
             """
             def test_vocabulary(self):
                 for value in ('OFF', ' no ', '0', False):
                     self.assertIs(solution.parse_bool(value), False)
                 for value in ('on', '1', 'True', True):
                     self.assertIs(solution.parse_bool(value), True)
             def test_errors(self):
                 for value in ('', 'maybe'):
                     with self.assertRaises(ValueError):
                         solution.parse_bool(value)
                 for value in (0, 1, [], {}):
                     with self.assertRaises(TypeError):
                         solution.parse_bool(value)
             """),
        task("interval-union", "validation",
             "merge_intervals(intervals) returns sorted (start, end) tuples merging closed intervals "
             "that overlap or touch. Accept a finite iterable of numeric endpoint pairs. Reject "
             "reversed intervals with ValueError. Preserve the input, include zero-length intervals, "
             "and return [] for empty input.",
             """
             def merge_intervals(intervals):
                 return sorted(tuple(pair) for pair in intervals)
             """,
             """
             def merge_intervals(intervals):
                 pairs = [tuple(pair) for pair in intervals]
                 if any(start > end for start, end in pairs):
                     raise ValueError('reversed interval')
                 result = []
                 for start, end in sorted(pairs):
                     if result and start <= result[-1][1]:
                         result[-1] = (result[-1][0], max(result[-1][1], end))
                     else:
                         result.append((start, end))
                 return result
             """,
             """
             def test_overlap(self):
                 self.assertEqual(solution.merge_intervals([(4, 8), (1, 5)]), [(1, 8)])
             def test_empty(self):
                 self.assertEqual(solution.merge_intervals([]), [])
             """,
             """
             def test_touch_nested_and_points(self):
                 values = [(3, 3), (-4, 0), (0, 2), (-2, -1), (2, 3)]
                 self.assertEqual(solution.merge_intervals(iter(values)), [(-4, 3)])
                 self.assertEqual(values[0], (3, 3))
             def test_gap_and_invalid(self):
                 self.assertEqual(solution.merge_intervals([(5, 5), (1, 2)]), [(1, 2), (5, 5)])
                 with self.assertRaises(ValueError):
                     solution.merge_intervals([(8, 2)])
             """),
        task("bounded-retry", "validation",
             "retry_call(operation, attempts, retry_on=(OSError,)) invokes a zero-argument callable "
             "until success, retrying only the specified exception types. attempts is the total "
             "maximum number of calls, not extra retries; reject nonpositive integers with "
             "ValueError before calling. Return any successful value, even falsy. Propagate other "
             "exceptions immediately, and re-raise the final failure after exhaustion. No sleeps.",
             """
             def retry_call(operation, attempts, retry_on=(OSError,)):
                 return operation()
             """,
             """
             def retry_call(operation, attempts, retry_on=(OSError,)):
                 if attempts <= 0:
                     raise ValueError('attempts must be positive')
                 for index in range(attempts):
                     try:
                         return operation()
                     except retry_on:
                         if index + 1 == attempts:
                             raise
             """,
             """
             def test_recovers(self):
                 calls = []
                 def operation():
                     calls.append(1)
                     if len(calls) < 2:
                         raise OSError('transient')
                     return 7
                 self.assertEqual(solution.retry_call(operation, 3), 7)
                 self.assertEqual(len(calls), 2)
             def test_success(self):
                 self.assertEqual(solution.retry_call(lambda: 4, 1), 4)
             """,
             """
             def test_exhaustion(self):
                 calls, failure = [], OSError('last')
                 def operation():
                     calls.append(1)
                     raise failure
                 with self.assertRaises(OSError) as caught:
                     solution.retry_call(operation, 3)
                 self.assertIs(caught.exception, failure)
                 self.assertEqual(len(calls), 3)
             def test_other_exception_and_invalid(self):
                 calls = []
                 def operation():
                     calls.append(1)
                     raise ValueError('permanent')
                 with self.assertRaises(ValueError):
                     solution.retry_call(operation, 5)
                 self.assertEqual(len(calls), 1)
                 with self.assertRaises(ValueError):
                     solution.retry_call(operation, 0)
                 self.assertEqual(len(calls), 1)
             def test_falsy_and_custom_exception(self):
                 self.assertIsNone(solution.retry_call(lambda: None, 3))
                 calls = []
                 def operation():
                     calls.append(1)
                     if len(calls) == 1:
                         raise LookupError('temporary')
                     return False
                 self.assertIs(solution.retry_call(operation, 2, (LookupError,)), False)
             """),
        task("nested-lookup", "validation",
             "get_path(data, path, default=None) follows dot-separated keys through nested "
             "dictionaries. Return default only if a key is absent or traversal reaches a "
             "non-dictionary. Existing falsy values and None are valid results. An empty path "
             "returns data itself. Dots delimit literal string keys; do not interpret numeric "
             "segments as list indices. Do not modify data.",
             """
             def get_path(data, path, default=None):
                 return data.get(path, default)
             """,
             """
             def get_path(data, path, default=None):
                 if path == '':
                     return data
                 value = data
                 for key in path.split('.'):
                     if not isinstance(value, dict) or key not in value:
                         return default
                     value = value[key]
                 return value
             """,
             """
             def test_nested(self):
                 self.assertEqual(solution.get_path({'app': {'port': 9}}, 'app.port'), 9)
             def test_missing(self):
                 self.assertEqual(solution.get_path({}, 'x', 'fallback'), 'fallback')
             """,
             """
             def test_falsy_and_identity(self):
                 data = {'x': {'n': None, 'flag': False, 'count': 0}}
                 self.assertIs(solution.get_path(data, ''), data)
                 self.assertIsNone(solution.get_path(data, 'x.n', 99))
                 self.assertIs(solution.get_path(data, 'x.flag', True), False)
                 self.assertEqual(solution.get_path(data, 'x.count', 99), 0)
             def test_scalar_and_numeric_keys(self):
                 self.assertEqual(solution.get_path({'a': [7]}, 'a.0', 'no'), 'no')
                 self.assertEqual(solution.get_path({'a': {'0': 7}}, 'a.0'), 7)
                 self.assertEqual(solution.get_path({'a': None}, 'a.x', 'no'), 'no')
             """),
        task("numeric-version", "validation",
             "compare_versions(left, right) compares nonempty strings of dot-separated ASCII "
             "nonnegative integer components. Return -1, 0, or 1. Compare numerically, treating "
             "missing trailing components as zeros; leading zeros are allowed. Empty components, "
             "signs, whitespace, and non-ASCII digits are invalid and raise ValueError. This is "
             "a numeric release version utility, not a semantic-version prerelease parser.",
             """
             def compare_versions(left, right):
                 return (left > right) - (left < right)
             """,
             """
             def compare_versions(left, right):
                 def parse(value):
                     parts = value.split('.')
                     if any(not part or any(c not in '0123456789' for c in part) for part in parts):
                         raise ValueError('invalid numeric version')
                     return [int(part) for part in parts]
                 a, b = parse(left), parse(right)
                 length = max(len(a), len(b))
                 a += [0] * (length - len(a))
                 b += [0] * (length - len(b))
                 return (a > b) - (a < b)
             """,
             """
             def test_numeric_order(self):
                 self.assertEqual(solution.compare_versions('1.10', '1.9'), 1)
             def test_equal(self):
                 self.assertEqual(solution.compare_versions('2.3', '2.3'), 0)
             """,
             """
             def test_padding_and_leading_zeros(self):
                 self.assertEqual(solution.compare_versions('01.002', '1.2.0.0'), 0)
                 self.assertEqual(solution.compare_versions('0.0.1', '0.1'), -1)
             def test_invalid(self):
                 for bad in ('', '1..2', '+1', '1. 2', '1.', '\u0661'):
                     with self.assertRaises(ValueError):
                         solution.compare_versions(bad, '1')
                     with self.assertRaises(ValueError):
                         solution.compare_versions('1', bad)
             """),
        task("csv-record", "test",
             "parse_record(text) parses exactly one comma-separated CSV record into a list of "
             "strings, respecting double-quoted fields, embedded commas/newlines and doubled quote "
             "escapes. Use standard-library CSV semantics with strict parsing and no whitespace "
             "trimming. An empty string yields []. Allow a trailing record terminator; multiple "
             "records or malformed quoting raise ValueError.",
             """
             def parse_record(text):
                 return text.split(',')
             """,
             """
             import csv
             import io

             def parse_record(text):
                 try:
                     rows = list(csv.reader(io.StringIO(text, newline=''), strict=True))
                 except csv.Error as exc:
                     raise ValueError('invalid CSV record') from exc
                 if not rows:
                     return []
                 if len(rows) != 1:
                     raise ValueError('expected one record')
                 return rows[0]
             """,
             """
             def test_quoted_comma(self):
                 self.assertEqual(solution.parse_record('a,"b,c",d'), ['a', 'b,c', 'd'])
             def test_plain(self):
                 self.assertEqual(solution.parse_record('a,b'), ['a', 'b'])
             """,
             r'''
             def test_escapes_and_empty(self):
                 self.assertEqual(solution.parse_record('"a""b",,"x\ny"\r\n'), ['a"b', '', 'x\ny'])
                 self.assertEqual(solution.parse_record(''), [])
                 self.assertEqual(solution.parse_record(' a ,b,'), [' a ', 'b', ''])
             def test_rejects_invalid_records(self):
                 for value in ('a\nb\n', '"unterminated', '"closed"junk,x'):
                     with self.assertRaises(ValueError):
                         solution.parse_record(value)
             '''),
        task("rolling-mean", "test",
             "rolling_mean(values, window) returns the arithmetic mean of each complete consecutive "
             "window in a finite iterable of real numbers, moving one position at a time. No "
             "partial windows; input shorter than window yields []. window is an integer and "
             "must be positive, otherwise raise ValueError. Do not mutate input collections.",
             """
             def rolling_mean(values, window):
                 values = list(values)
                 return [sum(values[i:i + window]) / window for i in range(0, len(values), window)]
             """,
             """
             def rolling_mean(values, window):
                 if window <= 0:
                     raise ValueError('window must be positive')
                 values = list(values)
                 return [sum(values[i:i + window]) / window
                         for i in range(len(values) - window + 1)]
             """,
             """
             def test_sliding(self):
                 self.assertEqual(solution.rolling_mean([1, 2, 3, 4], 2), [1.5, 2.5, 3.5])
             def test_single(self):
                 self.assertEqual(solution.rolling_mean([2, 4], 1), [2.0, 4.0])
             """,
             """
             def test_short_and_generator(self):
                 self.assertEqual(solution.rolling_mean([1], 3), [])
                 self.assertEqual(solution.rolling_mean([], 2), [])
                 self.assertEqual(solution.rolling_mean(iter([-2, 0, 8, -2]), 3), [2, 2])
             def test_invalid_and_input(self):
                 for window in (0, -2):
                     with self.assertRaises(ValueError):
                         solution.rolling_mean([], window)
                 values = [1.0, 3.0, 5.0]
                 solution.rolling_mean(values, 2)
                 self.assertEqual(values, [1.0, 3.0, 5.0])
             """),
        task("dependency-order", "test",
             "dependency_order(graph) returns all string node names in dependency-before-dependent "
             "order. graph maps each node to an iterable of dependencies; dependencies missing as "
             "keys are also nodes. At each step choose the lexicographically smallest currently "
             "ready node. Ignore duplicate dependency edges. Raise ValueError for any cycle, "
             "including a self-cycle. Empty input gives []; never mutate graph or its values.",
             """
             def dependency_order(graph):
                 return sorted(graph)
             """,
             """
             def dependency_order(graph):
                 pending = {node: set(deps) for node, deps in graph.items()}
                 for deps in list(pending.values()):
                     for dependency in deps:
                         pending.setdefault(dependency, set())
                 result = []
                 while pending:
                     ready = sorted(node for node, deps in pending.items() if not deps)
                     if not ready:
                         raise ValueError('dependency cycle')
                     node = ready[0]
                     result.append(node)
                     del pending[node]
                     for deps in pending.values():
                         deps.discard(node)
                 return result
             """,
             """
             def test_dependency_first(self):
                 self.assertEqual(solution.dependency_order({'app': ['lib'], 'lib': []}), ['lib', 'app'])
             def test_empty(self):
                 self.assertEqual(solution.dependency_order({}), [])
             """,
             """
             def test_missing_nodes_duplicates_and_ready_order(self):
                 graph = {'b': ['z', 'z'], 'a': ['b'], 'y': []}
                 self.assertEqual(solution.dependency_order(graph), ['y', 'z', 'b', 'a'])
                 self.assertEqual(graph['b'], ['z', 'z'])
                 self.assertEqual(solution.dependency_order({'b': [], 'a': [], 'c': ['a']}), ['a', 'b', 'c'])
             def test_cycles(self):
                 for graph in ({'a': ['a']}, {'a': ['b'], 'b': ['a'], 'c': []}):
                     with self.assertRaises(ValueError):
                         solution.dependency_order(graph)
             """),
        task("header-redaction", "test",
             "redact_headers(headers, sensitive=('authorization', 'cookie', 'x-api-key')) returns "
             "a fresh list of (name, value) pairs in original order, replacing sensitive values "
             "with '[REDACTED]'. Match names case-insensitively, preserve original name spelling, "
             "retain duplicate headers, and leave nonsensitive values unchanged. Accept any "
             "finite iterable of pairs and any finite iterable of sensitive string names; do "
             "not mutate inputs. An empty sensitive collection disables redaction.",
             """
             def redact_headers(headers, sensitive=('authorization', 'cookie', 'x-api-key')):
                 return [(name, '[REDACTED]' if name in sensitive else value) for name, value in headers]
             """,
             """
             def redact_headers(headers, sensitive=('authorization', 'cookie', 'x-api-key')):
                 names = {name.casefold() for name in sensitive}
                 return [(name, '[REDACTED]' if name.casefold() in names else value)
                         for name, value in headers]
             """,
             """
             def test_case_insensitive(self):
                 self.assertEqual(solution.redact_headers([('Authorization', 'secret'), ('Accept', '*/*')]),
                                  [('Authorization', '[REDACTED]'), ('Accept', '*/*')])
             def test_empty(self):
                 self.assertEqual(solution.redact_headers([]), [])
             """,
             """
             def test_duplicates_and_generators(self):
                 values = [('X-Token', 'one'), ('x-token', 'two'), ('Other', '')]
                 self.assertEqual(solution.redact_headers(iter(values), iter(['X-TOKEN'])),
                                  [('X-Token', '[REDACTED]'), ('x-token', '[REDACTED]'), ('Other', '')])
                 self.assertEqual(values[0][1], 'one')
             def test_disabled_and_defaults(self):
                 values = [('Cookie', 'a=b'), ('X-API-KEY', 'key')]
                 self.assertEqual(solution.redact_headers(values, []), values)
                 self.assertEqual(solution.redact_headers(values),
                                  [('Cookie', '[REDACTED]'), ('X-API-KEY', '[REDACTED]')])
             """),
    ]
    return {"schema_version": 1, "tasks": tasks}


def write_manifest(output: str | Path) -> Path:
    target = Path(output)
    if target.suffix.lower() != ".json":
        target = target / "manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def check_manifest() -> bool:
    """Validate authored fixtures locally without calling a model."""
    tasks = build_manifest()["tasks"]
    passes = {"starter": 0, "reference": 0}
    failures = []
    for entry in tasks:
        grading = entry["grading"]
        for label, field in (("starter", "input_files"), ("reference", "expected_files")):
            with tempfile.TemporaryDirectory(prefix="nanorsi-pack-check-") as tmp:
                root = Path(tmp)
                files = {**entry[field], **grading["public_tests"], **grading["private_tests"]}
                for name, content in files.items():
                    (root / name).write_text(content, encoding="utf-8")
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "unittest", "discover", "-s", ".", "-v"],
                        cwd=root, capture_output=True, text=True, timeout=grading["timeout_s"],
                    )
                    passed = result.returncode == 0
                    if (label == "reference" and not passed) or (label == "starter" and passed):
                        failures.append(f"{entry['task_id']} {label}: unexpected result\n{result.stderr}")
                except subprocess.TimeoutExpired:
                    passed = False
                    failures.append(f"{entry['task_id']} {label}: timeout")
                passes[label] += int(passed)
    print("Task-pack validation, not model performance (no model calls).")
    print(f"Starter passes: {passes['starter']}/{len(tasks)}; "
          f"reference passes: {passes['reference']}/{len(tasks)}")
    for failure in failures:
        print(failure, file=sys.stderr)
    return not failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the authored Python coding starter pack.")
    parser.add_argument("output", nargs="?", default=Path(__file__).with_name("manifest.json"),
                        help="manifest path or directory")
    parser.add_argument("--check", action="store_true",
                        help="validate starter/reference programs with bundled tests; write no files")
    args = parser.parse_args(argv)
    if args.check:
        return 0 if check_manifest() else 1
    print(write_manifest(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

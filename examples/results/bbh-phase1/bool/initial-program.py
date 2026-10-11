# BBH boolean_expressions task pack for nanoRSI (benchmark track).
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

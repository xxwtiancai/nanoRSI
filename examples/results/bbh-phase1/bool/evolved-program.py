# BBH boolean_expressions task pack for nanoRSI (benchmark track).
# Data: BIG-Bench-Hard (MIT, Copyright 2022 the BBH authors), vendored verbatim; see NOTICE.
# Initial solver authored by nanoRSI; the recursive-descent evaluator below applies
# the required precedence order: not binds tightest, then and, then or.
# The solver function may be improved; the stdin/stdout contract below must stay fixed.
"""Evaluate a nested boolean expression: print True or False."""
import json
import sys


def solve(text):
    tokens = text.strip()
    while tokens.endswith(" is"):
        tokens = tokens[:-3].rstrip()
    tokens = tokens.replace("(", " ( ").replace(")", " ) ").split()
    if not tokens:
        return "False"
    position = [0]

    def peek():
        return tokens[position[0]] if position[0] < len(tokens) else None

    def advance():
        token = tokens[position[0]]
        position[0] += 1
        return token

    def parse_or():
        value = parse_and()
        while peek() == "or":
            advance()
            value = value or parse_and()
        return value

    def parse_and():
        value = parse_not()
        while peek() == "and":
            advance()
            value = value and parse_not()
        return value

    def parse_not():
        if peek() == "not":
            advance()
            return not parse_not()
        return parse_atom()

    def parse_atom():
        token = advance()
        if token == "(":
            value = parse_or()
            if peek() == ")":
                advance()
            return value
        return token == "True"

    return str(parse_or())


def main():
    payload = json.load(sys.stdin)
    print(json.dumps({"answer": solve(payload["input"])}))


if __name__ == "__main__":
    main()

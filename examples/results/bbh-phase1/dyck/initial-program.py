# BBH dyck_languages task pack for nanoRSI (benchmark track).
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

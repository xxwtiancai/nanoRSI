import json
import sys
from pathlib import Path


case = json.load(sys.stdin)
mode = Path(__file__).with_name("policy.txt").read_text(encoding="utf-8").split(":", 1)[1].strip()
if mode != "evidence":
    print(json.dumps({"answer": "unknown"}))
else:
    statement = case["statement"].lower()
    answer = "billing" if "invoice" in statement else "support"
    print(json.dumps({"answer": answer}))

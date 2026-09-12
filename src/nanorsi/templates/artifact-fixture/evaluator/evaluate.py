import importlib.util
import json
import os
from pathlib import Path


cases = {
    "gate": ([3, 9, 2], 9),
    "train": ([1, 4, 2], 4),
    "heldout": ([-1, 5, 7], 7),
}
values, expected = cases[os.environ["NANORSI_SPLIT"]]
spec = importlib.util.spec_from_file_location("candidate_search", Path.cwd() / "target" / "search.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
actual = module.best(values)
result = {
    "schema_version": 1,
    "status": "ok",
    "metrics": {"score": 1.0 if actual == expected else 0.0},
    "constraints": {"tests_passed": isinstance(actual, int)},
    "case_results": [{"id": os.environ["NANORSI_SPLIT"], "score": 1.0 if actual == expected else 0.0}],
    "cost_usd": None,
    "duration_ms": 1,
}
Path(os.environ["NANORSI_RESULT_PATH"]).write_text(json.dumps(result), encoding="utf-8")

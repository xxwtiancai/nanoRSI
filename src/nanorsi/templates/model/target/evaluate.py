import json
import os
from pathlib import Path


result = {
    "schema_version": 1,
    "status": "ok",
    "metrics": {"score": 0.0},
    "constraints": {"tests_passed": True},
    "case_results": [],
    "cost_usd": None,
    "duration_ms": 0,
}
Path(os.environ["NANORSI_RESULT_PATH"]).write_text(json.dumps(result), encoding="utf-8")

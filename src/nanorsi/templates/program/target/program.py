"""Summarize posted records; the initial version handles plain numeric amounts.

JSON stdin: {"records": [{"category": str, "amount": number|string,
"status": optional str}]}. JSON stdout: {"count": int, "totals": {str: str}}.

Full contract: normalize category by strip/casefold, default blanks to
"uncategorized". Missing status means posted; compare other statuses after
strip/casefold and include only posted rows. Amounts support finite JSON numbers
or numeric strings with grouping commas, an optional leading $/€/£ sign, and
accounting parentheses for negatives. Skip booleans, null, empty and invalid
amounts. Sum exactly with Decimal and round category totals to two decimal
places using ROUND_HALF_UP. Count the included records (including zero values).
"""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
import sys


def summarize(payload):
    totals = {}
    count = 0
    for row in payload["records"]:
        if row.get("status", "posted") != "posted":
            continue
        try:
            amount = Decimal(str(row.get("amount")))
        except InvalidOperation:
            continue
        if not amount.is_finite():
            continue
        category = str(row.get("category", "uncategorized")).strip().casefold()
        totals[category] = totals.get(category, Decimal("0")) + amount
        count += 1
    return {"count": count, "totals": {category: format(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), ".2f") for category, value in sorted(totals.items())}}


if __name__ == "__main__":
    print(json.dumps(summarize(json.load(sys.stdin)), sort_keys=True))

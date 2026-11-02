"""Record what calc() returns for many inputs, or check it still does."""
import itertools
import json
import sys
from pathlib import Path

from pricing import calc

GOLDEN = Path(__file__).with_name("golden.json")
REPORT = Path(__file__).with_name("golden-diff.txt")

ITEMS = {
    "small": [("widget", 2, 10.0)],
    "medium": [("widget", 1, 100.0)],
    "large": [("widget", 5, 50.0)],
    "ints": [("widget", 3, 7)],
    "mixed": [None, ("w", 1, 100.0), ("bad", 0, 10.0), ("neg", 1, -5.0)],
    "short": [("widget", 1)],
    "nan": [("widget", 1, float("nan")), ("widget", 1, 20.0)],
    "empty": [],
}
COUNTRIES = ["US", "GB", "DE", "FR", "ZZ", "us"]
CUSTOMERS = {
    "none": None,
    "empty": {},
    "vip": {"vip": True},
    "vip-1": {"vip": 1},
    "vip-yes": {"vip": "yes"},
    "vip-no": {"vip": "no"},
    "vip-false": {"vip": False},
    "save10": {"coupon": "SAVE10"},
    "save20": {"coupon": "SAVE20"},
    "lowercase": {"coupon": "save10"},
    "vip+save20": {"vip": True, "coupon": "SAVE20"},
    "vip-no+save20": {"vip": "no", "coupon": "SAVE20"},
}


def results():
    """Return {case: repr of the result, or the error raised}."""
    out = {}
    cases = itertools.product(ITEMS, COUNTRIES, CUSTOMERS)
    for items, country, customer in cases:
        try:
            value = repr(calc(ITEMS[items], country, CUSTOMERS[customer]))
        except Exception as exc:  # record errors as behavior too
            value = f"error: {type(exc).__name__}"
        out[f"{items} | {country} | {customer}"] = value
    return out


def main():
    """Record with 'record'; compare with 'check'."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    now = results()
    if mode == "record":
        GOLDEN.write_text(json.dumps(now, indent=2) + "\n")
        print(f"recorded {len(now)} cases in {GOLDEN.name}")
        return 0
    before = json.loads(GOLDEN.read_text())
    keys = list(before) + [k for k in now if k not in before]
    changed = []
    for key in keys:
        old, new = before.get(key, "new"), now.get(key, "gone")
        if old != new:
            changed.append(f"CHANGED {key}: {old} -> {new}")
    REPORT.write_text("\n".join(changed) + "\n")
    for line in changed[:5]:
        print(line)
    print(f"{len(keys) - len(changed)} same, {len(changed)} changed")
    if changed:
        print(f"full list in {REPORT.name}")
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())

"""Analyze sensor-lift signature results.

Usage: python analyze.py [<results_file> ...]
       (defaults to all results/*.json in this directory)

Per protocol §6: per-category and aggregate statistics for each model.
Wilcoxon paired test, Cohen's d, bootstrap 95% CI on mean delta.

Outputs summary JSON next to each input as <slug>.summary.json
and prints a single combined table.
"""
from __future__ import annotations

import json
import math
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"

random.seed(20260517)


def wilcoxon_greater(deltas: list[float]) -> tuple[float, float]:
    """One-sided Wilcoxon signed-rank test (alt: median > 0).

    Returns (W+, p_value). Uses normal approximation for n >= 10 with
    continuity correction; otherwise exact enumeration.
    """
    nonzero = [d for d in deltas if d != 0.0 and not math.isnan(d)]
    n = len(nonzero)
    if n == 0:
        return 0.0, 1.0
    ranks = sorted(range(n), key=lambda i: abs(nonzero[i]))
    # average ranks for ties on |d|
    rank_of = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(nonzero[ranks[j + 1]]) == abs(nonzero[ranks[i]]):
            j += 1
        avg = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            rank_of[ranks[k]] = avg
        i = j + 1
    w_plus = sum(rank_of[i] for i in range(n) if nonzero[i] > 0)
    w_minus = sum(rank_of[i] for i in range(n) if nonzero[i] < 0)
    if n < 10:
        # exact enumeration: probability of W+ >= observed under H0
        count = 0
        total = 0
        for mask in range(1 << n):
            s = 0.0
            for k in range(n):
                r = rank_of[k]
                if (mask >> k) & 1:
                    s += r
            if s >= w_plus:
                count += 1
            total += 1
        return w_plus, count / total
    # normal approximation
    mu = n * (n + 1) / 4.0
    sigma2 = n * (n + 1) * (2 * n + 1) / 24.0
    if sigma2 <= 0:
        return w_plus, 1.0
    z = (w_plus - mu - 0.5) / math.sqrt(sigma2)
    # one-sided p-value: P(Z >= z)
    p = 0.5 * math.erfc(z / math.sqrt(2))
    return w_plus, p


def cohens_d_one_sample(deltas: list[float]) -> float:
    vals = [d for d in deltas if not math.isnan(d)]
    if len(vals) < 2:
        return float("nan")
    m = statistics.mean(vals)
    sd = statistics.pstdev(vals)
    return m / sd if sd > 0 else float("nan")


def bootstrap_ci(deltas: list[float], n_boot: int = 10000, alpha: float = 0.05) -> tuple[float, float]:
    vals = [d for d in deltas if not math.isnan(d)]
    if not vals:
        return (float("nan"), float("nan"))
    means = []
    n = len(vals)
    for _ in range(n_boot):
        sample = [vals[random.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(alpha / 2 * n_boot)]
    hi = means[int((1 - alpha / 2) * n_boot)]
    return lo, hi


def summarize(records: list[dict]) -> dict:
    deltas = [r["delta"] for r in records if not math.isnan(r.get("delta", float("nan")))]
    if not deltas:
        return {"n": 0, "mean_delta": float("nan"), "p_value": float("nan"),
                "cohens_d": float("nan"), "ci95_lo": float("nan"), "ci95_hi": float("nan")}
    _, p = wilcoxon_greater(deltas)
    d = cohens_d_one_sample(deltas)
    lo, hi = bootstrap_ci(deltas)
    return {
        "n": len(deltas),
        "mean_delta": statistics.mean(deltas),
        "median_delta": statistics.median(deltas),
        "p_value": p,
        "cohens_d": d,
        "ci95_lo": lo,
        "ci95_hi": hi,
        "frac_positive": sum(1 for d in deltas if d > 0) / len(deltas),
    }


def per_category(records: list[dict]) -> dict[str, dict]:
    cats: dict[str, list[dict]] = {}
    for r in records:
        cats.setdefault(r["category"], []).append(r)
    return {c: summarize(rs) for c, rs in cats.items()}


def decision(agg: dict) -> str:
    p = agg.get("p_value", 1.0)
    d = agg.get("cohens_d", 0.0)
    mean = agg.get("mean_delta", 0.0)
    if p < 0.01 and d is not None and not math.isnan(d) and d > 0.5:
        return "PASS"
    if p > 0.05 or (d is not None and not math.isnan(d) and d < 0.2):
        # need to also check the reverse case
        if mean < 0 and p > 0.95:
            return "REVERSE-candidate"
        return "FAIL"
    return "PARTIAL"


def analyze_file(path: Path) -> dict:
    data = json.loads(path.read_text())
    records = data.get("results", [])
    aggregate = summarize(records)
    by_cat = per_category(records)
    out = {
        "model": data.get("model"),
        "smoke": data.get("smoke", False),
        "n_records": len(records),
        "aggregate": aggregate,
        "by_category": by_cat,
        "decision": decision(aggregate),
    }
    summary_path = path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(out, indent=2))
    return out


def main() -> int:
    if len(sys.argv) > 1:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        paths = sorted(RESULTS.glob("*.json"))
        paths = [p for p in paths if not p.name.endswith(".summary.json")]

    if not paths:
        print("No result files found", file=sys.stderr)
        return 1

    print(f"{'model':40s}  {'n':4s}  {'mean':>9s}  {'d':>6s}  {'p':>8s}  {'CI95':>20s}  {'frac+':>6s}  decision")
    for path in paths:
        s = analyze_file(path)
        a = s["aggregate"]
        ci = f"[{a['ci95_lo']:+.3f},{a['ci95_hi']:+.3f}]"
        print(f"{s['model']:40s}  {s['n_records']:4d}  {a['mean_delta']:+9.4f}  "
              f"{a['cohens_d']:+6.3f}  {a['p_value']:8.4f}  {ci:>20s}  "
              f"{a['frac_positive']:6.2%}  {s['decision']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

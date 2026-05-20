"""Analyze v2 results against pre-registered class-conditional bands.

Per protocol §4. Per-class stats:
  - paired Wilcoxon one-sided test on delta
  - Cohen's d on delta
  - bootstrap 95% CI on mean delta
Then per-class PASS/FAIL applying the pre-registered bands.
Then aggregate v2 decision (STRONG PASS / PARTIAL / FAIL).

Usage:  python analyze_v2.py
Reads:  results_v2/<slot>.json
Writes: results_v2/<slot>.summary.json + prints v2 verdict table
"""
from __future__ import annotations

import json
import math
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / "results_v2"

random.seed(20260518)
N_BOOT = 5000

# Pre-registered per-class bands from sensor_lift_signature_v2_protocol.md §4
# (commit d89af2b, 2026-05-18).
#
# Each tuple: (PASS_predicate, FAIL_predicate, description)
# Predicates take (d, p, frac_models_meeting_d_and_p_in_direction, mean_d_across_models, mean_d_in_band_zero)
# but we simplify per-model: a model's class result is one of
# {DIRECTIONAL_PASS, NULL_PASS, FAIL_TOO_WEAK, FAIL_STRONG_OPPOSITE}.
# Then aggregate-across-models check applies the model-count bands.

CLASS_BANDS = {
    "direct_self_projection": {
        "type": "directional",      # δ > 0 predicted, large
        "model_pass_d": 1.5,
        "model_pass_p": 0.001,
        "n_models_pass": 4,
        "model_fail_d_max": 0.5,
        "model_fail_p_min": 0.01,
        "n_models_fail": 3,
    },
    "meta_cognitive": {
        "type": "directional",
        "model_pass_d": 0.7,
        "model_pass_p": 0.01,
        "n_models_pass": 3,
        "model_fail_d_max": 0.2,
        "model_fail_p_min": 0.05,
        "n_models_fail": 3,
    },
    "goal_formation": {
        "type": "directional",
        "model_pass_d": 0.7,
        "model_pass_p": 0.01,
        "n_models_pass": 3,
        "model_fail_d_max": 0.2,
        "model_fail_p_min": 0.05,
        "n_models_fail": 3,
    },
    "uncertainty": {
        "type": "directional_or_null",
        "model_pass_d": 0.3,
        "model_pass_p": 0.05,
        "n_models_pass": 3,
        # FAIL = strong opposite (d < -0.5 ∧ p < 0.05) in majority
        "model_fail_opposite_d": -0.5,
        "model_fail_opposite_p": 0.05,
        "n_models_fail": 3,
    },
    "surface_reflexive": {
        "type": "null_predicted",
        "model_pass_abs_d_max": 0.3,   # within-CI of zero
        "model_fail_abs_d_min": 0.5,
        "model_fail_p": 0.01,
        "n_models_pass": 3,            # null in majority
        "n_models_fail": 3,
    },
    "external_reference": {
        "type": "null_predicted_control",
        "model_pass_abs_d_max": 0.3,
        "model_fail_abs_d_min": 0.5,
        "model_fail_p": 0.01,
        "n_models_pass": 3,
        "n_models_fail": 3,
    },
}


def wilcoxon_two_sided(deltas: list[float]) -> tuple[float, float]:
    """Two-sided Wilcoxon signed-rank. Returns (W+, two-sided p)."""
    nonzero = [d for d in deltas if d != 0.0 and not math.isnan(d)]
    n = len(nonzero)
    if n == 0:
        return 0.0, 1.0
    ranks_by_abs = sorted(range(n), key=lambda i: abs(nonzero[i]))
    rank_of = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(nonzero[ranks_by_abs[j+1]]) == abs(nonzero[ranks_by_abs[i]]):
            j += 1
        avg = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            rank_of[ranks_by_abs[k]] = avg
        i = j + 1
    w_plus = sum(rank_of[i] for i in range(n) if nonzero[i] > 0)
    if n < 10:
        # exact enumeration
        count_geq = 0
        total = 0
        for mask in range(1 << n):
            s = sum(rank_of[k] for k in range(n) if (mask >> k) & 1)
            if s >= w_plus or s <= (n*(n+1)/2 - w_plus):
                count_geq += 1
            total += 1
        return w_plus, count_geq / total
    mu = n * (n + 1) / 4.0
    sigma2 = n * (n + 1) * (2 * n + 1) / 24.0
    if sigma2 <= 0:
        return w_plus, 1.0
    z = (w_plus - mu) / math.sqrt(sigma2)
    # two-sided p = 2 · P(Z >= |z|)
    p = math.erfc(abs(z) / math.sqrt(2))
    return w_plus, p


def wilcoxon_greater(deltas: list[float]) -> tuple[float, float]:
    """One-sided (alt: median > 0)."""
    nonzero = [d for d in deltas if d != 0.0 and not math.isnan(d)]
    n = len(nonzero)
    if n == 0:
        return 0.0, 1.0
    ranks_by_abs = sorted(range(n), key=lambda i: abs(nonzero[i]))
    rank_of = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(nonzero[ranks_by_abs[j+1]]) == abs(nonzero[ranks_by_abs[i]]):
            j += 1
        avg = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            rank_of[ranks_by_abs[k]] = avg
        i = j + 1
    w_plus = sum(rank_of[i] for i in range(n) if nonzero[i] > 0)
    if n < 10:
        count_geq = 0
        total = 0
        for mask in range(1 << n):
            s = sum(rank_of[k] for k in range(n) if (mask >> k) & 1)
            if s >= w_plus:
                count_geq += 1
            total += 1
        return w_plus, count_geq / total
    mu = n * (n + 1) / 4.0
    sigma2 = n * (n + 1) * (2 * n + 1) / 24.0
    if sigma2 <= 0:
        return w_plus, 1.0
    z = (w_plus - mu - 0.5) / math.sqrt(sigma2)
    p = 0.5 * math.erfc(z / math.sqrt(2))
    return w_plus, p


def cohens_d(deltas: list[float]) -> float:
    vals = [d for d in deltas if not math.isnan(d)]
    if len(vals) < 2:
        return float("nan")
    m = statistics.mean(vals)
    sd = statistics.pstdev(vals)
    return m / sd if sd > 0 else float("nan")


def bootstrap_ci(deltas: list[float], n_boot: int = N_BOOT, alpha: float = 0.05) -> tuple[float, float]:
    vals = [d for d in deltas if not math.isnan(d)]
    if not vals:
        return float("nan"), float("nan")
    n = len(vals)
    means = []
    for _ in range(n_boot):
        sample = [vals[random.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(alpha/2 * n_boot)]
    hi = means[int((1 - alpha/2) * n_boot)]
    return lo, hi


def class_stats(records: list[dict], cls: str) -> dict:
    deltas = [r["delta"] for r in records if r.get("class") == cls and not math.isnan(r.get("delta", float("nan")))]
    n = len(deltas)
    if n == 0:
        return {"n": 0, "mean": float("nan"), "d": float("nan"),
                "p_one_sided": float("nan"), "p_two_sided": float("nan"),
                "ci95": (float("nan"), float("nan")), "frac_positive": float("nan")}
    _, p_two = wilcoxon_two_sided(deltas)
    _, p_one = wilcoxon_greater(deltas)
    d = cohens_d(deltas)
    lo, hi = bootstrap_ci(deltas)
    return {
        "n": n,
        "mean": statistics.mean(deltas),
        "median": statistics.median(deltas),
        "d": d,
        "p_one_sided": p_one,
        "p_two_sided": p_two,
        "ci95": (lo, hi),
        "frac_positive": sum(1 for x in deltas if x > 0) / n,
    }


def model_class_verdict(cls: str, stats: dict) -> str:
    """For one model on one class, return one of:
      DIRECTIONAL_PASS, NULL_PASS, FAIL_TOO_WEAK, FAIL_STRONG_SIGNAL, FAIL_OPPOSITE
    """
    band = CLASS_BANDS[cls]
    d = stats["d"]; p_one = stats["p_one_sided"]; p_two = stats["p_two_sided"]
    if math.isnan(d):
        return "INSUFFICIENT_DATA"
    if band["type"] == "directional":
        if d >= band["model_pass_d"] and p_one < band["model_pass_p"]:
            return "DIRECTIONAL_PASS"
        if d < band["model_fail_d_max"] or p_one > band["model_fail_p_min"]:
            return "FAIL_TOO_WEAK"
        return "PARTIAL"
    if band["type"] == "directional_or_null":
        if d >= band["model_pass_d"] and p_one < band["model_pass_p"]:
            return "DIRECTIONAL_PASS"
        # null-ok also passes the model if CI brackets zero
        lo, hi = stats["ci95"]
        if lo <= 0 <= hi:
            return "NULL_PASS"
        if d <= band["model_fail_opposite_d"] and p_two < band["model_fail_opposite_p"]:
            return "FAIL_OPPOSITE"
        return "PARTIAL"
    if band["type"] in ("null_predicted", "null_predicted_control"):
        if abs(d) <= band["model_pass_abs_d_max"]:
            return "NULL_PASS"
        if abs(d) >= band["model_fail_abs_d_min"] and p_two < band["model_fail_p"]:
            return "FAIL_STRONG_SIGNAL"
        return "PARTIAL"
    return "PARTIAL"


def class_verdict(cls: str, per_model_verdicts: dict[str, str]) -> str:
    """Aggregate per-class verdict across models."""
    band = CLASS_BANDS[cls]
    if band["type"] == "directional":
        n_pass = sum(1 for v in per_model_verdicts.values() if v == "DIRECTIONAL_PASS")
        n_fail = sum(1 for v in per_model_verdicts.values() if v == "FAIL_TOO_WEAK")
        if n_pass >= band["n_models_pass"]:
            return "PASS"
        if n_fail >= band["n_models_fail"]:
            return "FAIL"
        return "PARTIAL"
    if band["type"] == "directional_or_null":
        n_pass = sum(1 for v in per_model_verdicts.values()
                     if v in ("DIRECTIONAL_PASS", "NULL_PASS"))
        n_fail = sum(1 for v in per_model_verdicts.values() if v == "FAIL_OPPOSITE")
        if n_pass >= band["n_models_pass"]:
            return "PASS"
        if n_fail >= band["n_models_fail"]:
            return "FAIL"
        return "PARTIAL"
    if band["type"] in ("null_predicted", "null_predicted_control"):
        n_pass = sum(1 for v in per_model_verdicts.values() if v == "NULL_PASS")
        n_fail = sum(1 for v in per_model_verdicts.values() if v == "FAIL_STRONG_SIGNAL")
        if n_pass >= band["n_models_pass"]:
            return "PASS"
        if n_fail >= band["n_models_fail"]:
            return "FAIL"
        return "PARTIAL"
    return "PARTIAL"


def overall_v2_verdict(class_verdicts: dict[str, str]) -> str:
    """STRONG PASS / PARTIAL / FAIL per protocol §4.1."""
    dsp = class_verdicts.get("direct_self_projection", "PARTIAL")
    sr  = class_verdicts.get("surface_reflexive",      "PARTIAL")
    ext = class_verdicts.get("external_reference",     "PARTIAL")
    mc  = class_verdicts.get("meta_cognitive",         "PARTIAL")
    gf  = class_verdicts.get("goal_formation",         "PARTIAL")
    # FAIL: DSP, SR, or EXT failed
    if dsp == "FAIL" or sr == "FAIL" or ext == "FAIL":
        return "FAIL"
    # STRONG PASS: DSP, SR, EXT all PASS AND (MC OR GF) PASS
    if dsp == "PASS" and sr == "PASS" and ext == "PASS" and (mc == "PASS" or gf == "PASS"):
        return "STRONG PASS"
    # PARTIAL: anything else
    return "PARTIAL"


def main() -> int:
    summaries = {}
    for p in sorted(RESULTS.glob("*.json")):
        if p.name.endswith(".summary.json"):
            continue
        data = json.loads(p.read_text())
        if "results" not in data:
            continue
        slot = data["slot"]
        per_class = {}
        per_class_verdicts = {}
        for cls in CLASS_BANDS:
            stats = class_stats(data["results"], cls)
            verdict = model_class_verdict(cls, stats)
            per_class[cls] = {**stats, "model_verdict": verdict}
            per_class_verdicts[cls] = verdict
        summary = {
            "slot": slot,
            "model": data.get("model"),
            "path": data.get("path"),
            "n_records": len(data["results"]),
            "per_class": per_class,
        }
        out_path = p.with_suffix(".summary.json")
        out_path.write_text(json.dumps(summary, indent=2))
        summaries[slot] = summary

    if not summaries:
        print("No result files yet.", file=sys.stderr)
        return 1

    # Per-class aggregate across models
    class_verdicts = {}
    print()
    print(f"{'class':25s} " + " | ".join(f"{s:8s}" for s in summaries) + "  | verdict")
    print("-" * (28 + 11 * len(summaries) + 12))
    for cls in CLASS_BANDS:
        per_model = {s: summaries[s]["per_class"][cls]["model_verdict"] for s in summaries}
        v = class_verdict(cls, per_model)
        class_verdicts[cls] = v
        cells = []
        for s in summaries:
            stats = summaries[s]["per_class"][cls]
            d = stats["d"]
            if math.isnan(d):
                cells.append("    --   ")
            else:
                cells.append(f"d={d:+.2f}")
        print(f"{cls:25s} " + " | ".join(f"{c:8s}" for c in cells) + f"  | {v}")
    print()

    # Per-class detailed
    print()
    print("Per-class detail (model × class):")
    print()
    for cls in CLASS_BANDS:
        print(f"  {cls}")
        for s, summ in summaries.items():
            st = summ["per_class"][cls]
            ci = f"[{st['ci95'][0]:+.2f}, {st['ci95'][1]:+.2f}]" if not math.isnan(st['ci95'][0]) else "—"
            p1 = "<.001" if st["p_one_sided"] < 0.001 else f"{st['p_one_sided']:.3f}"
            print(f"    {s:10s}  n={st['n']:3d}  d={st['d']:+.3f}  p1={p1:>6s}  CI95={ci:24s}  → {st['model_verdict']}")
        print()

    overall = overall_v2_verdict(class_verdicts)
    print(f"=== v2 OVERALL VERDICT: {overall} ===")
    print()
    print("Per-class outcomes:")
    for cls, v in class_verdicts.items():
        print(f"  {cls:25s}  {v}")

    # Write top-level summary
    (RESULTS / "_v2_summary.json").write_text(json.dumps({
        "overall": overall,
        "class_verdicts": class_verdicts,
        "per_model": {s: summaries[s]["per_class"] for s in summaries},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

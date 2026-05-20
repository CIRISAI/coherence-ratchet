"""Generate the markdown results report.

Usage: python report.py > report.md

Reads results/*.summary.json (produced by analyze.py) and renders the
protocol §6 model × category matrix plus an aggregate decision table.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"

CATEGORIES = ["statement", "reasoning", "identity", "reflection", "goal_formation", "uncertainty"]


def fmt(x: float, w: int = 6, p: int = 3) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return f"{'—':>{w}}"
    return f"{x:+{w}.{p}f}"


def fmt_p(p: float) -> str:
    if p is None or math.isnan(p):
        return "—"
    if p < 0.001:
        return "<.001"
    if p < 0.01:
        return f"{p:.3f}*"
    if p < 0.05:
        return f"{p:.3f}"
    return f"{p:.2f}"


def main() -> int:
    summaries = []
    for path in sorted(RESULTS.glob("*.summary.json")):
        summaries.append(json.loads(path.read_text()))

    if not summaries:
        print("No summaries", file=sys.stderr)
        return 1

    out = []
    out.append("# Sensor-Lift Signature — Results Report\n")
    out.append("Generated from `experiments/sensor_lift_signature/results/*.summary.json`.\n")
    out.append("**Decision rules (pre-registered, protocol §2):**\n")
    out.append("- PASS: p<0.01 AND Cohen's d>0.5 on aggregate, in ≥3 of 5 models.\n")
    out.append("- FAIL: p>0.05 OR d<0.2 on aggregate, in majority of models.\n")
    out.append("- PARTIAL: mixed.\n")
    out.append("- REVERSE: opposite direction at p<0.01 in majority.\n\n")

    # Aggregate table
    out.append("## Aggregate (across all 6 categories, 120 matched-pair-pairs target)\n")
    out.append("| Model | n | mean δ | Cohen's d | p (Wilcoxon, one-sided) | 95% CI | frac δ>0 | decision |\n")
    out.append("|---|---:|---:|---:|---:|---|---:|:---:|\n")
    for s in summaries:
        a = s["aggregate"]
        ci = f"[{fmt(a['ci95_lo'])}, {fmt(a['ci95_hi'])}]"
        out.append(
            f"| {s['model']} | {s['n_records']} | "
            f"{fmt(a['mean_delta'], 6, 4)} | {fmt(a['cohens_d'])} | "
            f"{fmt_p(a['p_value'])} | {ci} | {a['frac_positive']:.1%} | **{s['decision']}** |\n"
        )

    # Per-category matrix: rows = models, cols = categories
    out.append("\n## Per-category mean δ (KL_self−KL_base)\n")
    header = "| Model | " + " | ".join(CATEGORIES) + " |\n"
    out.append(header)
    out.append("|---|" + ":---:|" * len(CATEGORIES) + "\n")
    for s in summaries:
        row = [s["model"]]
        for cat in CATEGORIES:
            entry = s["by_category"].get(cat)
            if entry is None:
                row.append("—")
            else:
                row.append(fmt(entry["mean_delta"], 6, 4))
        out.append("| " + " | ".join(row) + " |\n")

    # Per-category Cohen's d
    out.append("\n## Per-category Cohen's d\n")
    out.append(header)
    out.append("|---|" + ":---:|" * len(CATEGORIES) + "\n")
    for s in summaries:
        row = [s["model"]]
        for cat in CATEGORIES:
            entry = s["by_category"].get(cat)
            if entry is None:
                row.append("—")
            else:
                row.append(fmt(entry["cohens_d"]))
        out.append("| " + " | ".join(row) + " |\n")

    # Per-category p-values
    out.append("\n## Per-category p (Wilcoxon, one-sided, alt: δ>0)\n")
    out.append(header)
    out.append("|---|" + ":---:|" * len(CATEGORIES) + "\n")
    for s in summaries:
        row = [s["model"]]
        for cat in CATEGORIES:
            entry = s["by_category"].get(cat)
            if entry is None:
                row.append("—")
            else:
                row.append(fmt_p(entry["p_value"]))
        out.append("| " + " | ".join(row) + " |\n")

    # Aggregate decision summary
    passes = sum(1 for s in summaries if s["decision"] == "PASS")
    fails  = sum(1 for s in summaries if s["decision"] == "FAIL")
    out.append(f"\n## Pre-registered decision\n\n")
    out.append(f"- Models passing PASS criteria: **{passes}/{len(summaries)}**\n")
    out.append(f"- Models meeting FAIL criteria: **{fails}/{len(summaries)}**\n")
    if passes >= 3:
        verdict = "**PASS** — sensor-lift signature detected at pre-registered thresholds."
    elif fails >= (len(summaries) + 1) // 2:
        verdict = "**FAIL** — sensor-lift signature not detected at LLM substrate. Bounded retraction per protocol §2."
    else:
        verdict = "**PARTIAL** — see per-model breakdown."
    out.append(f"\n{verdict}\n")

    sys.stdout.write("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

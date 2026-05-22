#!/usr/bin/env python3
"""
Robust re-run, Substrate 5 (social groups): re-verification of the
pre-registered hypothesis tests (H1-H5) and the three-mode rubric
against the v1 documented dataset.

This is NOT a debiased-rho recomputation -- social groups are a non-rho
substrate (see PREREGISTRATION.md). The instrument is a QUALITATIVE
CHECKLIST: AM_total (0-5), T_persist (years), LD (months). The robust
upgrade for this substrate is re-labeling under pre-registration
discipline, NOT a numerical recomputation. The one genuine recomputation
done here is re-deriving AM_total from its five component booleans, as
an internal-consistency check on the dataset.

Real data only -- reads the v1 documented dataset, no synthetic data.
"""
import json
from pathlib import Path
from statistics import median

V1 = Path("/home/emoore/coherence-ratchet/.claude/worktrees/"
          "agent-ab3971bf4bb503603/experiments/noncorr_social")
OUT = Path(__file__).resolve().parent / "results"
OUT.mkdir(exist_ok=True)
RESULTS_PATH = OUT / "verify_results.json"

DATA = json.loads((V1 / "results" / "dataset.json").read_text())["records"]

results = {"substrate": "social groups (Substrate 5)",
           "note": "non-rho substrate; instrument is a qualitative "
                   "active-maintenance CHECKLIST, NOT a debiased rho. "
                   "rho_analog is a hand-assigned ordinal label, not a "
                   "correlation, and is not used in any PASS/FAIL test.",
           "groups": {}, "consistency_checks": [], "hypotheses": {}}

AM_KEYS = ["AM1_charismatic_leader_required",
           "AM2_escalating_commitment_rituals",
           "AM3_information_control",
           "AM4_defection_punishment",
           "AM5_financial_sunk_cost"]

# --- internal-consistency recomputation: AM_total from its components ---
am_all_consistent = True
for r in DATA:
    recomputed = sum(1 for k in AM_KEYS if r[k])
    stored = r["AM_total"]
    ok = recomputed == stored
    am_all_consistent &= ok
    results["consistency_checks"].append(
        {"id": r["id"], "name": r["name"], "AM_total_stored": stored,
         "AM_total_recomputed": recomputed, "consistent": ok})
    results["groups"][r["id"]] = {
        "name": r["name"], "pole": r["pole"],
        "t_persist_years": r["t_persist_years"],
        "AM_total": recomputed,
        "LD_months": r.get("months_until_dissolution_after_leader_removed"),
        "status": r["ended_or_status"]}
    print(f"{r['id']:3s} {r['name']:42s} pole={r['pole']:8s} "
          f"T={r['t_persist_years']:>7.2f}y AM={recomputed} "
          f"AM_consistent={ok}")
RESULTS_PATH.write_text(json.dumps(results, indent=2))

rig = [r for r in DATA if r["pole"] == "rigidity"]
cha = [r for r in DATA if r["pole"] == "chaos"]
cor = [r for r in DATA if r["pole"] == "corridor"]

# --- pre-registered hypothesis tests H1-H5 ---
H = results["hypotheses"]

med_cor = median([r["t_persist_years"] for r in cor])
H["H1_corridor_median_T_ge_250"] = {
    "value_years": med_cor, "threshold": 250,
    "pass": med_cor >= 250}

med_rig = median([r["t_persist_years"] for r in rig])
H["H2_rigidity_median_T_le_50"] = {
    "value_years": med_rig, "threshold": 50,
    "pass": med_rig <= 50}

med_cha = median([r["t_persist_years"] for r in cha])
H["H3_chaos_median_T_le_5"] = {
    "value_years": med_cha, "threshold": 5,
    "pass": med_cha <= 5}

ld = [r.get("months_until_dissolution_after_leader_removed") for r in rig]
ld_short = sum(1 for x in ld if x is not None and x <= 24)
H["H4_rigidity_LD_le_24mo_in_ge_3of4"] = {
    "ld_months": ld, "n_le_24mo": ld_short, "threshold": "3/4",
    "pass": ld_short >= 3}

# H5: every persisting rigidity group carries AM_total >= 3
am_rig = [sum(1 for k in AM_KEYS if r[k]) for r in rig]
H["H5_rigidity_all_AM_ge_3"] = {
    "AM_totals": am_rig, "threshold": 3,
    "pass": all(a >= 3 for a in am_rig)}

# --- three-mode rubric ---
modes = {"mode_i": [], "mode_ii": [], "mode_iii": []}
for r in rig + cha:
    am = sum(1 for k in AM_KEYS if r[k])
    T = r["t_persist_years"]
    if am <= 1 and T <= 50:
        modes["mode_i"].append(r["id"])
    elif am >= 3:
        modes["mode_ii"].append(r["id"])
    elif am <= 1 and T > 50:
        modes["mode_iii"].append(r["id"])      # the falsifier
    else:
        modes.setdefault("other", []).append(r["id"])
results["three_mode"] = modes

# framework-contradicting checks
contra_rig = [r["id"] for r in rig
              if r["t_persist_years"] > 100
              and sum(1 for k in AM_KEYS if r[k]) <= 1]
contra_cha = [r["id"] for r in cha if r["t_persist_years"] > 20]
results["framework_contradicting"] = {
    "rigidity_T_gt_100_and_AM_le_1": contra_rig,
    "chaos_T_gt_20_unconsolidated": contra_cha}

# persistence spread
spread = {"corridor_median_T": med_cor, "rigidity_median_T": med_rig,
          "chaos_median_T": med_cha,
          "orders_of_magnitude": round(
              (med_cor / med_cha) ** 0, 0)}
import math
spread["orders_of_magnitude"] = round(math.log10(med_cor / med_cha), 1)
results["persistence_spread"] = spread

all_H_pass = all(h["pass"] for h in H.values())
mode_iii_n = len(modes["mode_iii"])
results["verdict"] = {
    "AM_total_internally_consistent": am_all_consistent,
    "hypotheses_H1_H5_all_pass": all_H_pass,
    "mode_iii_count": mode_iii_n,
    "framework_contradicting_cases": len(contra_rig) + len(contra_cha),
    "verdict": ("PASS" if (am_all_consistent and all_H_pass
                           and mode_iii_n == 0
                           and not contra_rig and not contra_cha)
                else "FAIL"),
}
RESULTS_PATH.write_text(json.dumps(results, indent=2))

print("\n=== hypotheses ===")
for k, v in H.items():
    print(f"  {k}: {'PASS' if v['pass'] else 'FAIL'}  {v}")
print("\n=== three-mode ===")
for k, v in modes.items():
    print(f"  {k}: {len(v)} {v}")
print(f"\npersistence spread: {spread}")
print(f"VERDICT: {results['verdict']}")
print(f"wrote {RESULTS_PATH}")

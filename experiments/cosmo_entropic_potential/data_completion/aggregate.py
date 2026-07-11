#!/usr/bin/env python3
"""Aggregate all data_completion outputs into a single results.json (verdict-first)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load(name):
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else None

joint = load("results.json")          # Pantheon+ joint (headline)
des = load("des_results.json")        # DES sensitivity
isw = load("isw_results.json")
fam = load("family_results.json")

def tabrow(d):
    return {k: d[k] for k in ("chi2", "Om", "k_params", "AIC", "BIC") if k in d} | (
        {"w0": d["w0"], "wa": d["wa"]} if "w0" in d else {})

agg = {
    "title": "SNe + ISW + within-family completion of the DESI DR2 dark-energy comparison",
    "date": "2026-07-10",
    "headline_table_BAO_CMB_SNe_Pantheon": {
        m: tabrow(joint["bao_cmb_sne"][m]) for m in ("framework", "LCDM", "CPL")
    } if joint else None,
    "headline_deltas": joint["bao_cmb_sne"]["deltas"] if joint else None,
    "sensitivity_table_BAO_CMB_SNe_DES": {
        m: tabrow(des["bao_cmb_sne"][m]) for m in ("framework", "LCDM", "CPL")
    } if des else None,
    "sensitivity_deltas": des["bao_cmb_sne"]["deltas"] if des else None,
    "isw": {
        "w_today_framework": isw["w_today_framework"] if isw else None,
        "A_ISW_matched_Om": {k: v for k, v in isw["matched_Om_0.3153"].items()
                             if not k.startswith(("_", "D0"))} if isw else None,
        "A_ISW_each_own_Om": {k: v for k, v in isw["each_own_jointfit_Om"].items()
                              if not k.startswith(("_", "D0"))} if isw else None,
        "published_A_ISW": isw["published_A_ISW"] if isw else None,
        "verdict": "CONSISTENT: framework A_ISW ~0.93-1.05 vs LCDM template, "
                   "well inside observed 0.96+/-0.30; ISW does not discriminate.",
    } if isw else None,
    "family_discrimination": fam["variants"] if fam else None,
    "family_verdict": (
        "DESI DR2 crossing posterior z=0.35 [0.19,0.70] DOES rank the family: "
        "extensive (proj z=0.46) and count (0.39) inside; intensive S/k (0.76) OUTSIDE. "
        "The crossing epoch separates what distance-chi2 could not."
    ) if fam else None,
    "full_files": {
        "pantheon_joint": "results.json",
        "des_sensitivity": "des_results.json",
        "isw": "isw_results.json",
        "family": "family_results.json",
    },
}
(HERE / "aggregate_results.json").write_text(json.dumps(agg, indent=2))
print(json.dumps(agg, indent=2))

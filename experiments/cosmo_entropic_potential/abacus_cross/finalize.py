#!/usr/bin/env python3
"""Post-process: config-aware cross-code verdict + truncation diagnostic (DECISIONS amendments
2 & 3). The corner-equivalent and full-population grains DISAGREE (mission §5: report which grain
transfers). Corner: endpoint peak, truncated. Full-pop: interior peak z=0.351. Adds fields only."""
import json, sys
from pathlib import Path
import numpy as np
CEP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CEP)); import s_of_a as S
RES = Path(__file__).resolve().parent / "results.json"
d = json.load(open(RES))
LCDM_3SIGMA = 3.28

def edge_diag(cfg, T=8):
    per = d[cfg][str(T)]["per_snap"]
    a = np.array([p["a"] for p in per]); z = np.array([p["z"] for p in per]); St = np.array([p["S_total"] for p in per])
    o = np.argsort(a); a, z, St = a[o], z[o], St[o]; imax = int(np.argmax(St))
    return dict(z_peak=float(z[imax]), endpoint=bool(imax == len(a)-1),
                dSda_edge=float((St[-1]-St[-2])/(a[-1]-a[-2])),
                dlnS_dlna_edge=float(S.dln_dlna(a, St)[-1]),
                turnover_within_window=bool(St[-1] < St[-2]))

dc = edge_diag("corner_7.425e11"); df = edge_diag("full_2.109e11")
vc = d["corner_7.425e11"]["8"]["S_total_analysis"]; vf = d["full_2.109e11"]["8"]["S_total_analysis"]
NO_LOWER_Z = True  # AbacusSummit small c000 halo snapshots: min z = 0.200

def comps(v, diag):
    return {"interior_peak": bool((not diag["endpoint"]) and v["z_peak"] is not None and 0.3 <= v["z_peak"] <= 1.0),
            "thawing": bool(v["wa"] < 0),
            "beats_lcdm_maha_point": bool(v["maha"] < LCDM_3SIGMA),
            "beats_lcdm_real_likelihood": bool(v["chi2_minus_lcdm"] < 0)}
cc = comps(vc, dc); cf = comps(vf, df)

corner_status = "INCONCLUSIVE-BY-TRUNCATION" if (dc["endpoint"] and dc["dSda_edge"] > 0) else \
                ("interior-peak" if cc["interior_peak"] else "endpoint-peak")
shape_transfers = cf["interior_peak"] and cf["thawing"]
mag_transfers = cf["beats_lcdm_maha_point"] and cf["beats_lcdm_real_likelihood"]
if shape_transfers and mag_transfers:
    word = "LAW-LIKE"
elif shape_transfers or cf["thawing"]:
    word = "PARTIAL"
else:
    word = "CODE-SPECIFIC"

d["truncation_diagnostic"] = {
    "corner_T8": dc, "full_T8": df, "no_lower_z_snapshots_available": NO_LOWER_Z, "abacus_small_min_z": 0.200,
    "note": ("Corner (7.425e11) S(a) rises monotonically to the box's final snapshot z=0.2 "
             "(dS/da=+6.9e4, no turnover) with no z<0.2 output to extend the window -> the corner "
             "grain is truncation-limited. Full-population (2.109e11, complete book) turns over "
             "INTERIOR at z=0.351 (dS/da=-7.0e4 at the edge) -> its formation clock fits inside "
             "the window because lower-mass halos peak earlier. The grains disagree; the window "
             "bites the higher-mass corner grain, not the complete book.")}
d["VERDICT"] = {
    "word": word,
    "one_line": ("Estimator transfers cleanly (gate v2, 1.3% S fidelity); the DE-leg SHAPE "
                 "(interior S-peak + thawing wa<0) transfers on the selection-free full-population "
                 "read (z_peak=0.351, wa=-0.346); the beats-LCDM MAGNITUDE does not cleanly transfer "
                 "(inside the (w0,wa) ellipse at 1.6 sigma but ~tied on the real DESI likelihood, "
                 "+0.55); and the corner-equivalent grain is inconclusive-by-truncation."),
    "gate": "v1 FAILED (conditioning-suspect CPL metric, pathological cluster regime); v2 (fair-regime subvolume) PASSED",
    "gate_v2_fidelity": d["gate_v2"]["summary"],
    "estimator_transfers_to_abacus": True,
    "corner_equivalent_7.425e11_T8": {
        "status": corner_status, "z_peak": vc["z_peak"], "peak_at_endpoint": vc["peak_at_endpoint"],
        "w0": vc["w0"], "wa": vc["wa"], "maha": vc["maha"], "chi2_minus_lcdm": vc["chi2_minus_lcdm"],
        "components": cc, "dSda_edge": dc["dSda_edge"]},
    "full_population_2.109e11_T8": {
        "status": "interior-peak (clean turnover within window)", "z_peak": vf["z_peak"],
        "peak_at_endpoint": vf["peak_at_endpoint"], "w0": vf["w0"], "wa": vf["wa"], "maha": vf["maha"],
        "chi2_minus_lcdm": vf["chi2_minus_lcdm"], "components": cf, "dSda_edge": df["dSda_edge"]},
    "which_grain_transfers": ("Interior-peak + thawing transfer on the FULL-POPULATION (complete-book, "
        "zero threshold-freedom) grain; the corner-equivalent grain's clock runs past the z=0.2 window."),
    "maha_vs_likelihood_note": ("Both configs sit closer to DESI's (w0,wa) point than LCDM by Mahalanobis "
        "(corner 3.13, full 1.62 vs LCDM 3.28) but are worse-to-tied on the real DESI DR2 distance "
        "likelihood (corner +8.6, full +0.55 vs LCDM) -- the reduced (w0,wa) summary flatters shapes the "
        "full distance likelihood does not prefer; the magnitude claim does not cleanly transfer."),
    "tiling_systematic_corner_T4_vs_T8": {
        "w0": [d["corner_7.425e11"]["4"]["S_total_analysis"]["w0"], vc["w0"]],
        "wa": [d["corner_7.425e11"]["4"]["S_total_analysis"]["wa"], vc["wa"]],
        "maha": [d["corner_7.425e11"]["4"]["S_total_analysis"]["maha"], vc["maha"]]},
    "grid_caveat_delta": d.get("grid_caveat", {}).get("delta", {})}
json.dump(d, open(RES, "w"), indent=1)
print("VERDICT:", word)
print("corner T8:", corner_status, json.dumps(d["VERDICT"]["corner_equivalent_7.425e11_T8"]["components"]))
print("full   T8:", json.dumps(d["VERDICT"]["full_population_2.109e11_T8"]["components"]),
      "z_peak", vf["z_peak"], "wa", vf["wa"], "maha", vf["maha"], "chi2dL", round(vf["chi2_minus_lcdm"],3))

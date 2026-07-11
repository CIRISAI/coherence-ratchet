#!/usr/bin/env python3
"""
Within-family discrimination with existing data (task 3).

The three family variants (functional_falsification) fit DESI DR2 DISTANCES
indistinguishably (chi2 8.86 / 8.66 / 9.87) but peak at different epochs. The
discriminator is the phantom-divide CROSSING epoch. DESI DR2's own crossing
posterior is z_cross = 0.35, 90% CI [0.19, 0.70]. Question: which variants'
CPL-PROJECTED crossings (the fair comparison -- DESI fits CPL to distances, so we
project each variant's curve through the same CPL fit) land inside [0.19, 0.70]?

Variants, all from the SAME frozen TNG300-1 records (a, S, k):
  extensive : F(a) = S(a)          (the frozen framework)
  intensive : F(a) = S(a)/k(a)     (per-unit / decomposition row)
  count     : F(a) = k(a)          (bare unit count)

CPL projection lifted verbatim from epoch_check/cpl_projection.py (exec-lift, the
selfconsistency.py pattern): project_distance fits CPL (w0,wa) to the variant's
BAO+CMB distances exactly as DESI fits CPL to data.
"""
import json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
EPOCH = CEP / "epoch_check"
LV = CEP / "large_volume" / "results.json"

# exec-lift the projection functions (module runs its pipeline on import; take defs only)
src = (EPOCH / "cpl_projection.py").read_text()
defs_src = src.split("# 4. Run.")[0]
cpl = {}
exec(compile(defs_src, str(EPOCH / "cpl_projection.py"), "exec"), cpl)
make_f_fw = cpl["make_f_fw"]; project_distance = cpl["project_distance"]
crossing_z = cpl["crossing_z"]; phys_crossing_z = cpl["phys_crossing_z"]

# frozen records
lv = json.load(open(LV))
recs = lv["stage2_primary"]["records"]
a = np.array([r["a"] for r in recs]); S = np.array([r["S"] for r in recs])
k = np.array([r["k"] for r in recs], float)
o = np.argsort(a); a, S, k = a[o], S[o], k[o]

VARIANTS = {
    "extensive_S": S,
    "intensive_S_over_k": S / k,
    "count_k": k,
}

# DESI DR2 crossing posterior (task-specified)
DESI_CROSS = dict(median=0.35, lo90=0.19, hi90=0.70)

out = {
    "desi_dr2_crossing_posterior": DESI_CROSS,
    "method": "CPL-projected crossing via epoch_check/cpl_projection.py project_distance "
              "(BAO+CMB), same fit DESI applies to distances; frozen TNG300-1 records.",
    "variants": {},
}

print("=" * 74)
print(f"DESI DR2 crossing posterior: z={DESI_CROSS['median']}  90% "
      f"[{DESI_CROSS['lo90']}, {DESI_CROSS['hi90']}]")
print("=" * 74)
print(f"{'variant':22s} {'phys_zx':>8s} {'proj(w0,wa)':>18s} {'proj_zx':>8s} {'in90%':>6s}")
for name, F in VARIANTS.items():
    f_de = make_f_fw(a, F)
    zx_phys = phys_crossing_z(a, F)
    w0, wa, chi2 = project_distance(f_de, use_cmb=True)
    zx_proj = crossing_z(w0, wa)
    inside = (zx_proj is not None) and (DESI_CROSS["lo90"] <= zx_proj <= DESI_CROSS["hi90"])
    out["variants"][name] = dict(
        phys_crossing_z=zx_phys, proj_w0=w0, proj_wa=wa,
        proj_crossing_z=zx_proj, proj_chi2=chi2, inside_desi_90=bool(inside))
    zxp = f"{zx_proj:.3f}" if zx_proj is not None else "none"
    print(f"{name:22s} {zx_phys:8.3f} ({w0:+.3f},{wa:+.3f}) {zxp:>8s} {str(inside):>6s}")

(HERE / "family_results.json").write_text(json.dumps(out, indent=2))
print("\nwrote family_results.json")

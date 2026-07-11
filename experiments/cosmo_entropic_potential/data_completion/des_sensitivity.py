#!/usr/bin/env python3
"""
Sensitivity: rerun the joint BAO+theta*+SNe comparison with DES-SN5YR (Dovekie)
in place of Pantheon+. Same machinery (joint_fit.py); only the SNe provider swaps.
Answers the K5 caveat: does the framework's joint preference depend on which SNe
compilation (the one at the centre of the DES-Y5 vs Pantheon+ calibration debate)?
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import joint_fit as J
import des_likelihood as des

# swap the SNe provider used inside joint_fit's functions
J.sl = des
J.N_SNE = des.des()["n"]

out = {
    "provenance": {
        "sne": f"DES-SN5YR Dovekie recalibration, {J.N_SNE} SNe (z>0), MU + full STAT+SYS "
               "inverse covariance; DES Collaboration arXiv:2401.02929 (+ Dovekie recalib); "
               "analytic offset-M marginalisation. SENSITIVITY compilation (K5 calibration).",
        "bao_cmb": "inherited from desi_likelihood_v2/likelihood_fit.py.",
        "n_sne": J.N_SNE,
    },
    "bao_cmb_sne": J.run("DES: BAO+CMB+SNe", use_cmb=True, use_sne=True),
    "bao_sne": J.run("DES: BAO+SNe", use_cmb=False, use_sne=True),
}
(Path(__file__).resolve().parent / "des_results.json").write_text(json.dumps(out, indent=2))

def show(tag, r):
    print("=" * 80); print(f"{tag}   (n_data={r['n_data']})"); print("-" * 80)
    for name in ("framework", "LCDM", "CPL"):
        d = r[name]
        extra = f" w0={d['w0']:+.3f} wa={d['wa']:+.3f}" if name == "CPL" else ""
        print(f"  {name:10s} chi2={d['chi2']:9.2f}  Om={d['Om']:.4f}  k={d['k_params']}"
              f"  AIC={d['AIC']:9.2f}  BIC={d['BIC']:9.2f}{extra}")
    dl = r["deltas"]
    print(f"  Dchi2 fw-LCDM={dl['chi2_framework_minus_LCDM']:+.2f}  "
          f"fw-CPL={dl['chi2_framework_minus_CPL']:+.2f}  LCDM-CPL={dl['chi2_LCDM_minus_CPL']:+.2f}")
    print(f"  dAIC fw-CPL={dl['dAIC_framework_minus_CPL']:+.2f} fw-LCDM={dl['dAIC_framework_minus_LCDM']:+.2f}"
          f"  | dBIC fw-CPL={dl['dBIC_framework_minus_CPL']:+.2f} fw-LCDM={dl['dBIC_framework_minus_LCDM']:+.2f}")

print("\n(DES-SN5YR Dovekie sensitivity)")
show("DES: BAO + theta* + SNe", out["bao_cmb_sne"])
print()
show("DES: BAO + SNe (no CMB)", out["bao_sne"])
print("\nwrote des_results.json")

#!/usr/bin/env python3
"""Print the load-bearing numbers from results.json for SUMMARY.md.

Read-only. Exists so every number quoted in SUMMARY.md is copied from executed
output rather than retyped from memory.
"""
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
r = json.load(open(HERE / "results.json"))

print("=" * 78)
print("ESTIMATOR VALIDATION (Gaussian, truth known)")
print("=" * 78)
ev = r["estimator_validation"]["cases"]
big = [c for c in ev if c["n"] == max(x["n"] for x in ev)]
print(f"  k_knn={r['estimator_validation']['k_knn']}, trials={r['estimator_validation']['n_trials']}")
for c in ev:
    print(f"   k={c['k']} rho={c['rho']:.1f} n={c['n']:>7d}  truth={c['truth']:.4f} "
          f"est={c['mean']:.4f}+/-{c['std']:.4f}  rel_bias={100*c['rel_bias']:+.2f}%")
rb = [abs(100 * c["rel_bias"]) for c in ev]
rs = [100 * c["std"] / c["truth"] for c in ev]
print(f"  -> |rel bias| range {min(rb):.2f}% .. {max(rb):.2f}%   "
      f"rel std range {min(rs):.2f}% .. {max(rs):.2f}%")
rb_big = [abs(100 * c["rel_bias"]) for c in big]
print(f"  -> at n={big[0]['n']}: |rel bias| max {max(rb_big):.2f}%")

print()
print("=" * 78)
print("(a) TRUE-MI INVARIANCE")
print("=" * 78)
a = r["a_true_mi_invariance"]
print(f"  verdict={a['verdict']}  pass={a['n_pass']}/{a['n_channels']} "
      f"indeterminate={a['n_indeterminate']} fail={a['n_fail']}")
print(f"  ladder={a['n_ladder']} trials={a['n_trials']}")
print(f"  {'cell':>12s} {'chan':>10s} {'truth':>8s} {'defc@nmin':>10s} {'defc@nmax':>10s} "
      f"{'I_inf':>8s} {'relI_inf':>9s} {'p':>5s} {'status':>32s}")
for rec in a["grid"]:
    for nm, ch in rec["channels"].items():
        print(f"  k={rec['k']} rho={rec['rho']:.1f} {nm:>10s} {rec['truth_MI']:8.4f} "
              f"{100*ch['deficit_at_min_n']/rec['truth_MI']:9.1f}% "
              f"{100*ch['rel_deficit_at_max_n']:9.1f}% "
              f"{ch['I_inf']:8.4f} {100*ch['rel_dev_I_inf']:+8.1f}% "
              f"{ch['fit_p']:5.2f} {ch['status']:>32s}")
print()
print("  sigma-independence of extrapolated intercept (spread across sigma, non-degenerate):")
for rec in a["grid"]:
    sp = rec["I_inf_spread_across_sigma"]
    print(f"   k={rec['k']} rho={rec['rho']:.1f}  truth={rec['truth_MI']:.4f}  spread="
          f"{'n/a' if sp is None else f'{sp:.4f}'}  gauss_ctrl_rel_bias="
          f"{100*rec['gauss_control_rel_bias']:+.2f}%")

# headline: worst raw deficit and its extrapolated recovery
worst = None
for rec in a["grid"]:
    for nm, ch in rec["channels"].items():
        if nm == "gauss":
            continue
        if worst is None or ch["rel_deficit_at_max_n"] < worst[2]:
            worst = (rec, nm, ch["rel_deficit_at_max_n"], ch)
print(f"\n  worst raw deficit at n_max: k={worst[0]['k']} rho={worst[0]['rho']} {worst[1]}: "
      f"{100*worst[2]:+.1f}%  ->  I_inf rel dev {100*worst[3]['rel_dev_I_inf']:+.1f}% "
      f"({worst[3]['status']})")

print()
print("=" * 78)
print("(b) RANK-S FLATNESS")
print("=" * 78)
b = r["b_rank_flatness"]
for k in ["n_cells", "spacing", "sigma2_R", "n_samples", "S_linear",
          "max_dev_rank_analytic", "max_dev_rank_empirical_shared",
          "max_dev_rank_independent", "pearson_decline_abs", "pearson_decline_rel",
          "rank_wobble_over_pearson_decline", "rank_finite_sample_logdet_bias",
          "pearson_emp_vs_analytic_maxdiff", "verdict"]:
    print(f"  {k:36s} {b[k]}")
sg = np.array(b["sigmas"]); sp = np.array(b["S_pearson_analytic"])
print(f"  S_pearson: sigma={sg[0]:.2f} -> {sp[0]:.5f} ;  sigma={sg[-1]:.2f} -> {sp[-1]:.5f}")
print(f"  S_rank analytic constant at S_linear = {b['S_linear']:.5f}")
sri = np.array(b["S_rank_independent_draws"])
print(f"  S_rank indep draws: mean={sri.mean():.5f} sd={sri.std(ddof=1):.2e} "
      f"min={sri.min():.5f} max={sri.max():.5f}")

print()
print("=" * 78)
print("(c) DPI UNDER SIGN THRESHOLD")
print("=" * 78)
c = r["c_threshold_dpi"]
print(f"  verdict={c['verdict']}  n={c['n_samples']}")
print(f"  {'k':>3s} {'rho':>5s} {'I_gauss':>9s} {'I_bin':>9s} {'ratio':>7s} "
      f"{'atten':>7s} {'emp_pm':>8s} {'VV_r':>8s} {'decreased':>10s}")
for cc in c["cases"]:
    print(f"  {cc['k']:3d} {cc['rho']:5.1f} {cc['I_gauss']:9.5f} {cc['I_binary']:9.5f} "
          f"{cc['ratio_Ibin_over_Igauss']:7.4f} {cc['vanvleck_atten_factor']:7.4f} "
          f"{cc['empirical_pm_corr']:8.4f} {cc['vanvleck_r']:8.4f} "
          f"{str(cc['strictly_decreased']):>10s}")
print(f"  small-rho(0.1) mean ratio = {c['small_rho_ratio_mean']:.4f}  "
      f"vs (2/pi)^2 = {c['small_rho_predicted_(2/pi)^2']:.4f}")
print(f"  2/pi = {2/np.pi:.4f}")

print()
print("=" * 78)
print("(d) COSMOLOGY: S_rank(a) vs S_pearson(a)")
print("=" * 78)
d = r["d_cosmology"]
for k in ["n_cells", "spacing", "sigma2_R", "S_linear", "n_samples", "n_seeds",
          "dlnS_dlna_pearson_today", "w_pearson_today",
          "dlnS_dlna_rank_analytic_today",
          "dlnS_dlna_rank_today_mean", "dlnS_dlna_rank_today_sd",
          "dlnS_dlna_rank_today_sem",
          "dlnS_dlna_rank_allcurve_mean", "dlnS_dlna_rank_allcurve_sd",
          "n_sigma_rank_from_zero", "n_sigma_pearson_in_rank_units",
          "w_rank_today", "w_rank_today_err",
          "consistent_with_w_minus_one", "verdict"]:
    print(f"  {k:34s} {d[k]}")
Sp = np.array(d["S_pearson"])
print(f"  S_pearson(a): {Sp[0]:.5f} (a=0.30) -> {Sp[-1]:.5f} (a=1)  "
      f"decline {100*(1-Sp[-1]/Sp[0]):.2f}%")

print()
print("=" * 78)
print("VERDICTS", r["verdicts"])
print("=" * 78)

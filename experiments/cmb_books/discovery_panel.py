"""Discovery-panel reporting around the frozen scored verdict (confirmation mode; the verdict
is set by run_cmb.py per REGISTRATION.md, this only adds referee-proofing statistics).

Adds, per ell_max: (1) two-sided marginal percentiles + literature-direction reproduction check;
(2) a sharp 'count of anomalies' look-elsewhere -- P(a random isotropic sky shows >= as many
tail-marginals as the data), which is the informative complement to the registered saturating
union; (3) the joint-depth chi^2 gap (non-Gaussianity of the depth).
"""
import json, numpy as np, os

HERE = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(HERE, "results.json")))
z = np.load(os.path.join(HERE, "null_battery.npz"))
null_all = z["null"]                       # (N, nELL, 7)
VEC = res["vec"]; ELL = [10, 30, 60]
TAIL = dict(align_23="U", A_hemi="U", S_half="L", Q_amp="L", axis_conc="U", S_logdet="U", pr_lowell="L")
LITDIR = dict(align_23="high (aligned)", A_hemi="high (asymmetric)", S_half="low (lack of corr)",
              Q_amp="low (low quadrupole)", axis_conc="high", S_logdet="high", pr_lowell="low")

out = {}
for i, LM in enumerate(ELL):
    nl = null_all[:, i, :]
    dv = np.array([res["data_battery"][str(LM)][k] for k in VEC])
    marg = {}
    flagged = 0
    for j, k in enumerate(VEC):
        p = 100 * np.mean(nl[:, j] < dv[j])
        tailp = p if TAIL[k] == "U" else 100 - p     # tail percentile (small = deep in flagged tail? no: large=extreme)
        # "tail extremeness": how far into the flagged tail (0..100, 100=most extreme)
        ext = p if TAIL[k] == "U" else 100 - p
        isflag = ext >= 95.0
        flagged += int(isflag)
        marg[k] = dict(data=float(dv[j]), pct=round(float(p), 2), tail=TAIL[k],
                       tail_extremeness=round(float(ext), 2), flagged_95=bool(isflag),
                       lit_expected=LITDIR[k])
    # count-of-anomalies look-elsewhere: per null realization, count tail-marginals >=95th extreme
    cnt = np.zeros(nl.shape[0])
    for j, k in enumerate(VEC):
        col = nl[:, j]
        r = (np.argsort(np.argsort(col)) + 0.5) / len(col) * 100     # percentile of each null in null
        ext = r if TAIL[k] == "U" else 100 - r
        cnt += (ext >= 95.0)
    p_ge = float(np.mean(cnt >= flagged))
    out[LM] = dict(marginals=marg, data_flagged_count=flagged,
                   P_random_sky_has_ge_that_many_anomalies=round(p_ge, 4),
                   mean_anomaly_count_null=round(float(cnt.mean()), 3),
                   joint=res["per_ellmax"][str(LM)]["joint_depths"],
                   registered_union=res["per_ellmax"][str(LM)]["lookelsewhere_union_any_marginal"])

json.dump(out, open(os.path.join(HERE, "discovery_panel.json"), "w"), indent=1)
print("VERDICT:", res["verdict"]["verdict"], res["verdict"]["primary_joint_percentiles"])
for LM in ELL:
    o = out[LM]
    print(f"\n=== ell_max={LM} ===  data flagged(>=95th tail): {o['data_flagged_count']}/7  "
          f"P(random sky >= that many)={o['P_random_sky_has_ge_that_many_anomalies']}  "
          f"(null mean count {o['mean_anomaly_count_null']})")
    print(f"  joint depths: maha={o['joint']['mahalanobis_pct']:.2f} "
          f"ns={o['joint']['normalscores_pct']:.2f} spatial={o['joint']['spatial_pct']:.2f} "
          f"| chi2-theory={o['joint']['mahalanobis_chi2_pct']:.2f}")
    for k in VEC:
        m = o["marginals"][k]
        print(f"    {k:11s} data={m['data']:11.4f}  pct={m['pct']:6.2f}  tailext={m['tail_extremeness']:6.2f}"
              f"  {'FLAG' if m['flagged_95'] else '    '}  (lit: {m['lit_expected']})")

#!/usr/bin/env python3
"""
Robust epoch locator + octant jackknife for the Pandey cross-check.

Pandey's DE-onset marker = the configuration-entropy dissipation-rate extremum, i.e. the peak
of dG/dln a where G(a)=<(1+d)ln(1+d)> (DECISIONS.md O1). The committed spline locator proved
edge-biased (pinned to the z-range boundary by a noisy z=0 snapshot); we replace it with a
robust interior finite-difference + parabolic-refinement locator and jackknife THAT. Reported
for the primary (unsmoothed, 1.6 Mpc/h) field and the quasi-linear smoothed fields (Pandey's
linear-regime restriction). Writes results_final.json.
"""
import sys, os, json
import numpy as np
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "copula_stress"))
from copula_lib import cic_grid  # noqa
from run_mi import load_snaps, G_functional, octant_mask, LBOX, NG

Z_LO, Z_HI = 0.05, 2.0   # interior search window (Pandey's minimum is a late-time DE feature;
                         # exclude the high-z pre-structure ramp and the one-sided z=0 boundary)


def field(pos, m, ng, box, Rs):
    delta = cic_grid(pos, box, ng, weights=m)
    if Rs and Rs > 0:
        sig = Rs / (box / ng)
        sm = gaussian_filter(1.0 + delta, sigma=sig, mode="wrap")
        delta = sm / sm.mean() - 1.0
    return delta


def rate_peak_z(lna, G, zs):
    """Interior peak of dG/dln a with 3-point parabolic refinement in ln a. Returns z_peak."""
    o = np.argsort(lna)
    x, y, z = np.asarray(lna)[o], np.asarray(G)[o], np.asarray(zs)[o]
    d = np.gradient(y, x)                      # dG/dln a
    m = (z >= Z_LO) & (z <= Z_HI)
    xi, di = x[m], d[m]
    i = int(np.argmax(di))
    if 0 < i < len(di) - 1:                    # parabolic vertex on (x, dG/dlna)
        x0, x1, x2 = xi[i - 1], xi[i], xi[i + 1]
        y0, y1, y2 = di[i - 1], di[i], di[i + 1]
        denom = (y0 - 2 * y1 + y2)
        if denom != 0:
            xv = x1 - 0.5 * (x2 - x0) * (y2 - y0) / (4 * (y1) - 2 * (y0 + y2) + 1e-30)
            # standard vertex formula on equal-ish spacing; fall back to x1 if unstable
            xv = x1 - 0.5 * ((x1 - x0) ** 2 * (y1 - y2) - (x1 - x2) ** 2 * (y1 - y0)) / \
                 ((x1 - x0) * (y1 - y2) - (x1 - x2) * (y1 - y0) + 1e-30)
            if not (min(x0, x2) <= xv <= max(x0, x2)):
                xv = x1
        else:
            xv = x1
    else:
        xv = xi[i]
    return float(np.exp(-xv) - 1.0)


def analyze(Rs, kind="groups", ng=NG):
    snaps = load_snaps(kind)
    lna = np.array([np.log(s["a"]) for s in snaps])
    zs = np.array([s["z"] for s in snaps])
    G = np.array([G_functional(field(s["pos"], s["m"], ng, LBOX, Rs)) for s in snaps])
    z_full = rate_peak_z(lna, G, zs)
    jk = []
    for drop in range(8):
        Gj = []
        for s in snaps:
            mm = octant_mask(s["pos"], LBOX, drop)
            Gj.append(G_functional(field(s["pos"][mm], s["m"][mm], ng, LBOX, Rs)))
        jk.append(rate_peak_z(lna, np.array(Gj), zs))
    jk = np.array(jk)
    # jackknife error (delete-one octant): sigma^2 = (n-1)/n * sum (jk_i - mean)^2
    n = len(jk)
    jk_var = (n - 1) / n * np.sum((jk - jk.mean()) ** 2)
    return dict(Rs=Rs, kind=kind, ng=ng, z_full=z_full,
                jk_mean=float(jk.mean()), jk_reps=jk.tolist(),
                jk_sigma=float(np.sqrt(jk_var)))


def main():
    out = dict(s_peak_ours=dict(z=0.59, sigma=0.03), z_window=[Z_LO, Z_HI], runs=[])
    configs = [("groups", 0.0), ("groups", 4.0), ("groups", 8.0), ("galaxies", 4.0)]
    for kind, Rs in configs:
        r = analyze(Rs, kind)
        # combined-sigma comparison with our S-peak
        sig_comb = np.sqrt(r["jk_sigma"] ** 2 + 0.03 ** 2)
        r["delta_vs_ours"] = abs(r["z_full"] - 0.59)
        r["combined_sigma"] = float(sig_comb)
        r["n_sigma"] = float(r["delta_vs_ours"] / sig_comb) if sig_comb > 0 else float("inf")
        r["verdict"] = "AGREEMENT" if r["delta_vs_ours"] <= sig_comb else "DIVERGENCE"
        out["runs"].append(r)
        print(f"{kind:8s} Rs={Rs:4.1f}: z_peak={r['z_full']:.3f} "
              f"jk={r['jk_mean']:.3f}+/-{r['jk_sigma']:.3f}  "
              f"|dz|={r['delta_vs_ours']:.3f} vs comb.sig={sig_comb:.3f} "
              f"({r['n_sigma']:.2f}sig) -> {r['verdict']}", flush=True)
        with open(os.path.join(HERE, "results_final.json"), "w") as f:
            json.dump(out, f, indent=2)
    return out


if __name__ == "__main__":
    main()

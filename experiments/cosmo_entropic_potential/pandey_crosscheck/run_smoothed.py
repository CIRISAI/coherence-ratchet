#!/usr/bin/env python3
"""
Robustness/faithfulness check for the Pandey cross-check (see DECISIONS.md).

Pandey's formalism is explicitly restricted to "scales where one can safely use linear
perturbation theory" and to "significantly large volumes". The primary run (1.6 Mpc/h cells)
is deeply nonlinear and gives a monotone, edge-pinned config-entropy rate. Here we Gaussian-
smooth the CIC field to quasi-linear scales R_s and re-locate the config-entropy-rate extremum
(argmax dG/dlna), which is Pandey's DE-onset marker. If a clean interior peak near z~0.6
emerges in the quasi-linear regime, that is the agreement test; if it stays monotone/edge, the
box cannot host his minimum (INCONCLUSIVE-BY-BOX).
"""
import sys, os, json, glob
import numpy as np
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "copula_stress"))
from copula_lib import cic_grid  # noqa
from run_mi import load_snaps, G_functional, spline_deriv_peak, octant_mask, LBOX, NG


def smoothed_delta(pos, m, ng, box, Rs):
    delta = cic_grid(pos, box, ng, weights=m)
    if Rs <= 0:
        return delta
    sig_cells = Rs / (box / ng)
    sm = gaussian_filter(1.0 + delta, sigma=sig_cells, mode="wrap")
    return sm / sm.mean() - 1.0


def run(Rs_list=(2.0, 4.0, 8.0, 16.0), kind="groups", ng=NG):
    snaps = load_snaps(kind)
    lna = np.array([np.log(s["a"]) for s in snaps])
    zs = np.array([s["z"] for s in snaps])
    out = dict(kind=kind, ng=ng, box=LBOX, s_peak_ours=dict(z=0.59, sigma=0.03), variants=[])
    for Rs in Rs_list:
        G = np.array([G_functional(smoothed_delta(s["pos"], s["m"], ng, LBOX, Rs))
                      for s in snaps])
        try:
            _, z_pk, (xf, d1) = spline_deriv_peak(lna, G)
            interior = (z_pk > zs.min() + 0.02) and (z_pk < zs.max() - 0.02)
        except Exception as e:
            z_pk, interior = float("nan"), False
            print("spline fail", Rs, e)
        # jackknife
        jk = []
        for drop in range(8):
            Gj = np.array([G_functional(
                smoothed_delta(s["pos"][octant_mask(s["pos"], LBOX, drop)],
                               s["m"][octant_mask(s["pos"], LBOX, drop)], ng, LBOX, Rs))
                for s in snaps])
            try:
                _, zjk, _ = spline_deriv_peak(lna, Gj)
                jk.append(zjk)
            except Exception:
                pass
        jk = np.array(jk)
        v = dict(Rs_Mpch=Rs, z_min=z_pk, interior=bool(interior),
                 jk_mean=float(jk.mean()), jk_std=float(jk.std()),
                 jk_reps=jk.tolist(),
                 G_of_z=[[float(z), float(g)] for z, g in zip(zs, G)])
        out["variants"].append(v)
        print(f"Rs={Rs:5.1f} Mpc/h  argmax dG/dlna z_min={z_pk:.3f} interior={interior}  "
              f"jk={jk.mean():.3f}+/-{jk.std():.3f}", flush=True)
        with open(os.path.join(HERE, "results_smoothed.json"), "w") as f:
            json.dump(out, f, indent=2)
    return out


if __name__ == "__main__":
    run()

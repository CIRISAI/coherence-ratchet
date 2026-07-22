#!/usr/bin/env python3
"""
PREDICTION 4 — the calibration rung: the SAME fixed estimator (random tie-break + CIC) and
the SAME nulls (N0/N1/N1a/N2) applied to the TNG300-1 halo catalog that carried the original
~20% copula-Third detection and on which K4 fired.

This is not a new measurement of the halo field; it is the bridge that puts the tracer rung
on the same axis as the DM-particle ladder, so "does the signal scale away with n_bar" can be
read across both. Run on the frozen large_volume/data catalogs; nothing there is modified.
"""
import json, os
from pathlib import Path
import numpy as np
from numpy.fft import rfftn

import measure as M

HERE = Path(__file__).resolve().parent
DATA = HERE / ".." / ".." / "large_volume" / "data"
SNAPS = [99, 67, 25]
BOX = 205.0
NG = 64
R = [4.0, 8.0, 16.0]
SEED = 20260721


def grid_cic(pos, w, L, ng):
    x = (pos % L) / L * ng
    i0 = np.floor(x).astype(np.int64); d = x - i0
    i0 %= ng; i1 = (i0 + 1) % ng
    g = np.zeros(ng ** 3)
    for dx in (0, 1):
        wx = d[:, 0] if dx else 1 - d[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = d[:, 1] if dy else 1 - d[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
            xy = (ix * ng + iy) * ng
            for dz in (0, 1):
                wz = d[:, 2] if dz else 1 - d[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                g += np.bincount(xy + iz, weights=w * wx * wy * wz, minlength=ng ** 3)
    return g.reshape((ng,) * 3)


def main():
    kk = M.k_grid(NG, BOX)
    out = {"meta": dict(sim="TNG300-1 halos (calibration rung)", box=BOX, ng=NG, R=R,
                        seed=SEED, estimator=M.__doc__.split("\n")[2].strip()), "rows": []}
    op = HERE / "results_halo_rung.json"
    for snap in SNAPS:
        f = DATA / f"tng300_groups_{snap:03d}.npz"
        if not f.exists():
            continue
        d = np.load(f, allow_pickle=True)
        pos = np.asarray(d["pos"], float)
        L = 205000.0 if pos.max() > 1e4 else 205.0
        pos = pos * (BOX / L)
        z = float(d["z"]); n = pos.shape[0]
        rng = np.random.default_rng([SEED, snap])
        rho = grid_cic(pos, np.ones(n), BOX, NG)
        nbar = n / NG ** 3
        delta = rho / rho.mean() - 1.0
        row = dict(snap=snap, z=z, nhalo=n, nbar=nbar,
                   sigma_delta=float(delta.std()),
                   frac_empty=float((rho <= 0).mean()),
                   real=M.copula_skew(delta, kk, NG, rng, R))
        P_shot = M.shot_power(nbar, NG, "cic", rng)
        row["P_shot"] = P_shot
        bands = {}
        for name in ("N0", "N1", "N1a", "N2"):
            nn = 20 if name in ("N1", "N1a") else 10
            acc = []
            for _ in range(nn):
                if name == "N0":
                    fld = M.gaussian_from_amp(np.abs(rfftn(delta)), NG, rng)
                elif name == "N2":
                    fld = rng.permutation(delta.ravel()).reshape((NG,) * 3)
                else:
                    lam = (M.lognormal_intensity(delta, nbar, NG, P_shot, rng)
                           if name == "N1" else
                           M.clipped_gauss_intensity(delta, nbar, NG, rng))
                    fld = M.field_from_counts(rng.poisson(lam), NG, "cic", rng)
                acc.append(M.copula_skew(fld, kk, NG, rng, R))
            bands[name] = dict(n=nn,
                               mean={k: float(np.mean([a[k] for a in acc])) for k in acc[0]},
                               std={k: float(np.std([a[k] for a in acc], ddof=1)) for k in acc[0]})
        row["nulls"] = bands
        row["G"] = {nm: {k: (float((row["real"][k] - bands[nm]["mean"][k]) / bands[nm]["std"][k])
                             if bands[nm]["std"][k] > 0 else float("nan"))
                         for k in row["real"]} for nm in bands}
        out["rows"].append(row)
        with open(op, "w") as fh:
            json.dump(out, fh, indent=1)
        print(f"snap {snap} z={z:.3f} N={n} nbar={nbar:.3f} empty={row['frac_empty']:.3f}  "
              f"R8 real={row['real']['8']:+.4f}  N1={bands['N1']['mean']['8']:+.4f}"
              f"+-{bands['N1']['std']['8']:.4f} G={row['G']['N1']['8']:+.2f}  "
              f"N1a={bands['N1a']['mean']['8']:+.4f} G={row['G']['N1a']['8']:+.2f}  "
              f"N0={bands['N0']['mean']['8']:+.4f} N2={bands['N2']['mean']['8']:+.4f}",
              flush=True)
    print("wrote", op)


if __name__ == "__main__":
    main()

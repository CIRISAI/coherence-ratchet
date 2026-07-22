#!/usr/bin/env python3
"""
PREDICTION 4 — stage 2: the copula-Third density-scaling discriminator.

Estimator IDENTICAL to thirdness/measure_thirdness.py (normal-score -> Fourier Gaussian
smooth -> standardized skewness), with the two fixes the K4 audit forced:
  * RANDOM tie-breaking (exact: lexicographic rank on (value, random key)), not argsort o argsort
  * CIC assignment primary (NGP carried as a robustness column)
Applied identically to the real subsampled DM fields and to every null, at every density.

Nulls (pre-committed controls, DECISIONS.md):
  N0  continuous phase-randomized Gaussian (no discreteness)              -> must give ~0
  N1  lognormal-Poisson, shot-subtracted target P(k)   [PRIMARY shot null]
        a lognormal field is a MONOTONE transform of a Gaussian, so its copula is EXACTLY
        Gaussian: its copula-skew is zero in the continuous limit and whatever it shows at
        finite n_bar is exactly the discreteness contribution.  Non-negative by construction
        (no clipping artifact).
  N1a clipped-Gaussian-Poisson (the frozen discriminator's S1 form)       [secondary shot null]
  N2  cell shuffle: marginals preserved exactly, all spatial structure destroyed -> must give ~0

Incremental flush to results.json after every density.
"""
import json, os, sys, time
from pathlib import Path
import numpy as np
from numpy.fft import rfftn, irfftn, fftfreq, rfftfreq
from scipy.special import ndtri

HERE  = Path(__file__).resolve().parent
SIM   = os.environ.get("P4_SIM", "TNG100-3")
SNAP  = int(os.environ.get("P4_SNAP", "99"))
SCR   = Path(os.environ.get("P4_SCRATCH",
             "/tmp/claude-1000/-home-emoore-coherence-ratchet/"
             "047db89f-06e6-45f4-a014-34f932c0bc32/scratchpad/p4"))
SEED  = 20260721
R_REF = [4.0, 8.0, 16.0]          # Mpc/h in the frozen 205 Mpc/h box
FRACS = [4.3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]

# realizations per null, by mean occupancy (frozen in DECISIONS.md)
def n_real(nbar, base):
    if nbar <= 10:   return base
    if nbar <= 100:  return max(base // 2, 5)
    return max(base // 4, 5)


# ------------------------------------------------------------------ estimator
def k_grid(ng, L):
    kf = 2 * np.pi / L
    kx = fftfreq(ng, d=1.0 / ng) * kf
    kz = rfftfreq(ng, d=1.0 / ng) * ng * kf
    KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij")
    return np.sqrt(KX**2 + KY**2 + KZ**2)


def normal_score_random(field, rng):
    """Copula transform with EXACT random tie-breaking."""
    flat = np.ascontiguousarray(field).ravel()
    n = flat.size
    perm = rng.permutation(n)                       # random key
    order = np.argsort(flat[perm], kind="stable")   # stable -> ties resolved by random key
    ranks = np.empty(n, np.int64)
    ranks[perm[order]] = np.arange(n)
    g = ndtri((ranks + 0.5) / n)
    return g.reshape(field.shape)


def copula_skew(field, kk, ng, rng, Rs):
    g = normal_score_random(field, rng)
    gk = rfftn(g)
    out = {}
    for R in Rs:
        gR = irfftn(gk * np.exp(-0.5 * (kk * R) ** 2), s=(ng,) * 3)
        m2 = np.mean(gR ** 2)
        out[f"{R:g}"] = float(np.mean(gR ** 3) / m2 ** 1.5) if m2 > 0 else float("nan")
    return out


# ------------------------------------------------------------------ assignment
def cic_points(pos_cells, ng, grid):
    """pos_cells: (n,3) float positions in CELL units. Accumulate CIC into flat grid."""
    i0 = np.floor(pos_cells).astype(np.int64)
    d = pos_cells - i0
    i0 %= ng
    i1 = (i0 + 1) % ng
    for dx in (0, 1):
        wx = d[:, 0] if dx else 1.0 - d[:, 0]
        ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = d[:, 1] if dy else 1.0 - d[:, 1]
            iy = i1[:, 1] if dy else i0[:, 1]
            xy = (ix * ng + iy) * ng
            wxy = wx * wy
            for dz in (0, 1):
                wz = d[:, 2] if dz else 1.0 - d[:, 2]
                iz = i1[:, 2] if dz else i0[:, 2]
                grid += np.bincount(xy + iz, weights=wxy * wz, minlength=ng ** 3)


def field_from_counts(counts, ng, kind, rng, block=8_000_000):
    """counts: integer counts per cell. Return delta with the SAME assignment as the real
    field: NGP -> counts as-is; CIC -> place each point uniformly in its cell, then CIC."""
    if kind == "ngp":
        rho = counts.astype(np.float64)
    else:
        flat = counts.ravel()
        idx = np.repeat(np.arange(flat.size, dtype=np.int32), flat)
        grid = np.zeros(ng ** 3)
        for s in range(0, idx.size, block):
            i = idx[s:s + block]
            cz = (i % ng).astype(np.float64)
            cy = ((i // ng) % ng).astype(np.float64)
            cx = (i // (ng * ng)).astype(np.float64)
            off = rng.random((i.size, 3))
            cic_points(np.stack([cx + off[:, 0], cy + off[:, 1], cz + off[:, 2]], 1),
                       ng, grid)
        rho = grid.reshape((ng,) * 3)
    m = rho.mean()
    return rho / m - 1.0 if m > 0 else rho


# ------------------------------------------------------------------ nulls
def gaussian_from_amp(amp, ng, rng):
    wk = rfftn(rng.standard_normal(size=(ng,) * 3))
    ph = wk / np.abs(np.where(np.abs(wk) == 0, 1.0, wk))
    sk = amp * ph
    sk.flat[0] = 0.0
    return irfftn(sk, s=(ng,) * 3)


def shot_power(nbar, ng, kind, rng, nrep=3):
    """Empirical |delta_k|^2 of a uniform Poisson field of the same n_bar and assignment."""
    vals = []
    for _ in range(nrep):
        c = rng.poisson(nbar, size=(ng,) * 3)
        d = field_from_counts(c, ng, kind, rng)
        vals.append(np.mean(np.abs(rfftn(d)) ** 2))
    return float(np.mean(vals))


def lognormal_intensity(delta_real, nbar, ng, P_shot, rng):
    """Lognormal field whose Poisson realisation reproduces P(k)_real; copula EXACTLY Gaussian."""
    M = ng ** 3
    P = np.abs(rfftn(delta_real)) ** 2
    P = np.clip(P - P_shot, 0.0, None)
    P.flat[0] = 0.0
    xi = irfftn(P, s=(ng,) * 3) / M                 # xi[0,0,0] = variance of the field
    xiG = np.log(np.clip(1.0 + xi, 1e-6, None))
    PG = rfftn(xiG) * M
    PG = np.clip(PG.real, 0.0, None)
    PG.flat[0] = 0.0
    g = gaussian_from_amp(np.sqrt(PG), ng, rng)
    return nbar * np.exp(g - 0.5 * np.var(g))


def clipped_gauss_intensity(delta_real, nbar, ng, rng):
    dG = gaussian_from_amp(np.abs(rfftn(delta_real)), ng, rng)
    return np.clip(nbar * (1.0 + dG), 0.0, None)


# ------------------------------------------------------------------ driver
def run(grids_path, out_path):
    d = np.load(grids_path)
    box = float(d["box"]); z = float(d["z"])
    Rs = [r * box / 205.0 for r in R_REF]           # scale the frozen scales with the box
    res = dict(meta=dict(sim=SIM, snap=SNAP, z=z, box_mpch=box, seed=SEED,
                         R_ref_205=R_REF, R_used=Rs, fracs=FRACS,
                         ntot=int(d["ntot"]),
                         estimator="normal-score(random tie-break) -> Gaussian smooth -> "
                                   "standardized skewness (identical to frozen)",
                         nulls="N0 phase-random Gaussian; N1 lognormal-Poisson "
                               "(shot-subtracted target, exactly-Gaussian copula) PRIMARY; "
                               "N1a clipped-Gaussian-Poisson; N2 cell shuffle"),
               rows=[])
    keys = [k for k in d.files if k.startswith(("cic_", "ngp_"))]
    kk_cache = {}

    def kkg(ng):
        if ng not in kk_cache:
            kk_cache[ng] = k_grid(ng, box)
        return kk_cache[ng]

    # ---- order: NG=64 CIC first (primary), then NGP, then NG=128
    def sortkey(k):
        kind, ngs, fs, rs = k.split("_")
        return (0 if (kind == "cic" and ngs == "ng64") else
                1 if kind == "ngp" else 2, float(fs[1:]), int(rs[1:]))
    keys.sort(key=sortkey)

    t0 = time.time()
    for k in keys:
        kind, ngs, fs, rs = k.split("_")
        ng = int(ngs[2:]); f = float(fs[1:]); rep = int(rs[1:])
        rng = np.random.default_rng([SEED, ng, int(f * 1e9), rep])
        rho = d[k].astype(np.float64).reshape((ng,) * 3)
        npart = float(rho.sum())
        nbar = npart / ng ** 3
        delta = rho / rho.mean() - 1.0
        kk = kkg(ng)
        row = dict(key=k, kind=kind, ng=ng, frac=f, rep=rep, nbar=nbar,
                   npart=npart, sigma_delta=float(delta.std()),
                   frac_empty=float((rho <= 0).mean()),
                   real=copula_skew(delta, kk, ng, rng, Rs))
        # nulls only on rep 0 (they are density properties, not replicate properties)
        if rep == 0:
            P_shot = shot_power(nbar, ng, kind, rng)
            row["P_shot"] = P_shot
            bands = {}
            n0 = n_real(nbar, 10)
            n1 = n_real(nbar, 20)
            for name in ("N0", "N1", "N1a", "N2"):
                nn = n0 if name in ("N0", "N2") else n1
                if ng == 128:
                    nn = max(nn // 2, 3)
                acc = []
                for _ in range(nn):
                    if name == "N0":
                        fld = gaussian_from_amp(np.abs(rfftn(delta)), ng, rng)
                    elif name == "N2":
                        fld = rng.permutation(delta.ravel()).reshape((ng,) * 3)
                    else:
                        lam = (lognormal_intensity(delta, nbar, ng, P_shot, rng)
                               if name == "N1" else
                               clipped_gauss_intensity(delta, nbar, ng, rng))
                        fld = field_from_counts(rng.poisson(lam), ng, kind, rng)
                    acc.append(copula_skew(fld, kk, ng, rng, Rs))
                bands[name] = dict(
                    n=nn,
                    mean={r: float(np.mean([a[r] for a in acc])) for r in acc[0]},
                    std={r: float(np.std([a[r] for a in acc], ddof=1)) for r in acc[0]})
            row["nulls"] = bands
            row["G"] = {name: {r: (float((row["real"][r] - bands[name]["mean"][r]) /
                                         bands[name]["std"][r])
                                   if bands[name]["std"][r] > 0 else float("nan"))
                               for r in row["real"]}
                        for name in bands}
        res["rows"].append(row)
        with open(out_path, "w") as fh:
            json.dump(res, fh, indent=1)
        R8 = f"{Rs[1]:g}"
        msg = (f"{k:24s} nbar={nbar:9.3f} empty={row['frac_empty']:.3f} "
               f"sig={row['sigma_delta']:7.3f}  skew(R8)={row['real'][R8]:+.4f}")
        if rep == 0:
            msg += ("  N1={:+.4f}+-{:.4f} G={:+7.2f} | N1a={:+.4f} G={:+7.2f} | "
                    "N0={:+.4f} N2={:+.4f}").format(
                row["nulls"]["N1"]["mean"][R8], row["nulls"]["N1"]["std"][R8],
                row["G"]["N1"][R8], row["nulls"]["N1a"]["mean"][R8], row["G"]["N1a"][R8],
                row["nulls"]["N0"]["mean"][R8], row["nulls"]["N2"]["mean"][R8])
        print(msg + f"   [{time.time()-t0:.0f}s]", flush=True)
    print("wrote", out_path)


if __name__ == "__main__":
    gp = SCR / f"grids_{SIM}_{SNAP:03d}.npz"
    op = HERE / f"results_{SIM}_{SNAP:03d}.json"
    if not gp.exists():
        raise SystemExit(f"grids not found: {gp} (run fetch_grid.py first)")
    run(gp, op)

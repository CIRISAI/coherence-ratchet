#!/usr/bin/env python3
"""
copula_stress re-run against a SHOT-MATCHED null. Method frozen in DECISIONS.md
(2026-07-21, + Amendment 1) before any verdict statistic existed.

The frozen tier-3 gap  gap = I_KSG(real) - I_KSG(MVN with C_rank)  was drawn against a
CONTINUOUS null on a DISCRETE count field. K4 showed that null type is insufficient.
Here the same estimator (imported unmodified from the frozen copula_lib.py) is run against
four nulls side by side:

  S0   MVN with C_rank                       (the frozen null, reproduced)
  S0f  phase-randomized continuous field     (matched |d_k| exactly, continuous marginals)
  S1   Poisson POINT process: matched n_bar exactly, 2-point-calibrated, CIC-gridded    <-- DECISIVE
  S1b  as S1 without the shot subtraction in the intensity spectrum (shape bracket)

Plus (a) tie-break decomposition (frozen raw-jitter / normal-score average / argsort-argsort
positional / random) and (b) NGP-vs-CIC assignment sensitivity, at the primary config.

One process per snapshot; incremental flush per (snapshot, config) to results_snap{NNN}.json.
Nothing in ../ is written.
"""
import os, sys, json, time
import numpy as np
from numpy.fft import rfftn, irfftn, fftfreq, rfftfreq
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, FROZEN)
from copula_lib import (cic_grid, template_samples, ksg_multiinformation,   # noqa: E402
                        gaussian_copula_MI, gaussian_surrogate, normal_scores)

DATA = os.path.abspath(os.path.join(HERE, "..", "..", "large_volume", "data"))
BOX = 205.0
K_KNN = 4
SNAPS = ["025", "033", "042", "059", "067", "099"]

N_REAL, N_S0, N_S0F, N_S1, N_S1B = 2, 4, 3, 4, 3
N_TIE_NULL = 2
WMIN2 = 0.25          # keep intensity modes with W^2 >= this (Amendment 1)
CAL_TOL = 0.01        # I_gauss match tolerance for the null calibration
CAL_MAXIT = 6

CONFIGS = [
    dict(id="A", ng=48, template="line", m=6, sep=1),    # PRIMARY, 4.27 Mpc/h
    dict(id="B", ng=32, template="line", m=6, sep=1),    # 6.41 Mpc/h
    dict(id="C", ng=48, template="block2", m=8, sep=1),  # 4.27 Mpc/h, m=8
]


def offsets_for(cfg):
    if cfg["template"] == "line":
        return [(i * cfg["sep"], 0, 0) for i in range(cfg["m"])]
    return [(i, j, k) for i in range(2) for j in range(2) for k in range(2)]


# ---------------------------------------------------------------- gridding / windows
def ngp_grid(pos, box, ng, weights=None):
    """Nearest-grid-point deposit -> overdensity (no anti-aliasing)."""
    pos = np.asarray(pos, float)
    n = pos.shape[0]
    w = np.ones(n) if weights is None else np.asarray(weights, float)
    idx = np.floor((pos % box) / box * ng).astype(int) % ng
    flat = (idx[:, 0] * ng + idx[:, 1]) * ng + idx[:, 2]
    rho = np.bincount(flat, weights=w, minlength=ng ** 3).astype(float).reshape(ng, ng, ng)
    return rho / rho.mean() - 1.0


def assign_window(ng, p):
    """Mass-assignment window on the rfftn grid. p=1 NGP, p=2 CIC."""
    nx = fftfreq(ng, d=1.0 / ng)
    nz = rfftfreq(ng, d=1.0 / ng) * ng
    wx = np.sinc(nx / ng) ** p
    wz = np.sinc(nz / ng) ** p
    return wx[:, None, None] * wx[None, :, None] * wz[None, None, :]


def kbins(ng, frac=0.9):
    nx = fftfreq(ng, d=1.0 / ng)
    nz = rfftfreq(ng, d=1.0 / ng) * ng
    kk = np.sqrt(nx[:, None, None] ** 2 + nx[None, :, None] ** 2 + nz[None, None, :] ** 2)
    edges = np.arange(0.0, ng * frac + 1.0, 1.0)
    idx = np.clip(np.digitize(kk.ravel(), edges) - 1, 0, len(edges) - 2)
    return idx, len(edges) - 1


def bin_power(field, idx, nbin):
    P = np.abs(rfftn(field)) ** 2
    s = np.bincount(idx, weights=P.ravel(), minlength=nbin)
    c = np.bincount(idx, minlength=nbin)
    return s / np.maximum(c, 1)


def phase_randomize(amp, rng, ng):
    wk = rfftn(rng.standard_normal((ng, ng, ng)))
    ph = wk / np.abs(np.where(np.abs(wk) == 0, 1.0, wk))
    sk = amp * ph
    sk.flat[0] = 0.0
    return irfftn(sk, s=(ng, ng, ng))


def poisson_points(dG, npoints, box, ng, rng):
    """Poisson point process, intensity prop. to max(1+dG,0), exactly `npoints` points
    (fixed-N Poisson = multinomial), uniform sub-cell placement."""
    lam = np.clip(1.0 + dG, 0.0, None).ravel()
    tot = lam.sum()
    if tot <= 0:
        lam = np.ones_like(lam); tot = lam.sum()
    counts = rng.multinomial(npoints, lam / tot)
    nz = np.nonzero(counts)[0]
    cells = np.repeat(nz, counts[nz])
    ix = cells // (ng * ng); iy = (cells // ng) % ng; iz = cells % ng
    cs = box / ng
    return (np.stack([ix, iy, iz], axis=1) + rng.random((cells.size, 3))) * cs


def intensity_template(field, npoints, box, ng, rng, grid_fn, wpow, subtract_shot):
    """Amplitude template for the Poisson null's Gaussian intensity (Amendment 1)."""
    idx, nbin = kbins(ng)
    Preal = bin_power(field, idx, nbin)
    if subtract_shot:
        Pshot = np.mean([bin_power(grid_fn(rng.random((npoints, 3)) * box, box, ng), idx, nbin)
                         for _ in range(4)], axis=0)
        Pt = np.clip(Preal - Pshot, 0.0, None)
    else:
        Pt = Preal.copy()
    W2 = assign_window(ng, wpow) ** 2
    mask = (W2 >= WMIN2)
    amp = np.sqrt(Pt[idx].reshape(W2.shape) / np.maximum(W2, 1e-6)) * mask
    return amp, float(mask.mean())


def draw_poisson_null(amp, A, npoints, box, ng, rng, grid_fn, offs):
    dG = phase_randomize(amp * np.sqrt(A), rng, ng)
    pts = poisson_points(dG, npoints, box, ng, rng)
    X = template_samples(grid_fn(pts, box, ng), offs)
    return X, float(dG.var()), float(np.mean(dG < -1.0))


def calibrate_A(amp, target_Ig, npoints, box, ng, rng, grid_fn, offs):
    """Secant search in log A so the GRIDDED null's I_gauss_copula matches real's."""
    def ev(A):
        X, _, _ = draw_poisson_null(amp, A, npoints, box, ng, rng, grid_fn, offs)
        Ig, _, _ = gaussian_copula_MI(X)
        return np.log(max(Ig, 1e-6))
    tgt = np.log(max(target_Ig, 1e-6))
    la, lb = np.log(1.0), np.log(3.0)
    fa, fb = ev(np.exp(la)) - tgt, ev(np.exp(lb)) - tgt
    hist = [(float(np.exp(la)), float(fa)), (float(np.exp(lb)), float(fb))]
    for _ in range(CAL_MAXIT):
        if abs(fb) < CAL_TOL:
            break
        if abs(fb - fa) < 1e-9:
            break
        lc = lb - fb * (lb - la) / (fb - fa)
        lc = float(np.clip(lc, np.log(0.05), np.log(50.0)))
        fc = ev(np.exp(lc)) - tgt
        la, fa, lb, fb = lb, fb, lc, fc
        hist.append((float(np.exp(lc)), float(fc)))
    return float(np.exp(lb)), float(fb), hist


# ---------------------------------------------------------------- estimator wrappers
def measure(X, rng, n_ksg=1):
    """The frozen estimator pair on a sample matrix X."""
    Ig, C, n_clip = gaussian_copula_MI(X)
    vals = [ksg_multiinformation(X, k=K_KNN, rng=rng) for _ in range(n_ksg)]
    I = float(np.mean(vals))
    off = C[np.triu_indices(C.shape[0], 1)]
    return dict(I_gauss=float(Ig), I_ksg=I,
                I_ksg_sd=float(np.std(vals, ddof=1)) if n_ksg > 1 else 0.0,
                resid=float(I - Ig), rbar=float(off.mean()), n_clip=int(n_clip)), C


def band(draws):
    f = lambda key: np.array([d[key] for d in draws])  # noqa: E731
    out = dict(n=len(draws),
               I_ksg=float(f("I_ksg").mean()), I_ksg_sd=float(f("I_ksg").std(ddof=1)),
               resid=float(f("resid").mean()), resid_sd=float(f("resid").std(ddof=1)),
               I_gauss=float(f("I_gauss").mean()), rbar=float(f("rbar").mean()))
    return out


def ns_transform(X, mode, rng):
    """Normal-score transform with explicit tie handling."""
    if mode == "avg":
        return normal_scores(X)              # rankdata(method='average'): ties collapsed
    N = X.shape[0]
    Z = np.empty_like(X, dtype=float)
    for j in range(X.shape[1]):
        col = X[:, j]
        if mode == "pos":
            order = np.argsort(np.argsort(col))          # K4's indicted positional ordering
        elif mode == "rand":
            jit = rng.standard_normal(N) * 1e-9 * (np.abs(col).mean() + 1e-30)
            order = np.argsort(np.argsort(col + jit))
        else:
            raise ValueError(mode)
        Z[:, j] = norm.ppf((order + 0.5) / N)
    return Z


def gap_block(real, b):
    return dict(gap=real["I_ksg"] - b["I_ksg"], gapc=real["resid"] - b["resid"],
                z=((real["resid"] - b["resid"]) / b["resid_sd"]) if b["resid_sd"] > 0 else float("nan"),
                Ig_rel=(b["I_gauss"] - real["I_gauss"]) / max(abs(real["I_gauss"]), 1e-12),
                rbar_rel=(b["rbar"] - real["rbar"]) / max(abs(real["rbar"]), 1e-12))


# ---------------------------------------------------------------- per-snapshot driver
def run_snapshot(snap):
    out_path = os.path.join(HERE, f"results_snap{snap}.json")
    d = np.load(os.path.join(DATA, f"tng300_groups_{snap}.npz"), allow_pickle=True)
    pos = np.asarray(d["pos"], float); z = float(d["z"]); a = float(d["a"])
    nh = pos.shape[0]
    rng = np.random.default_rng(20260721 + int(snap))
    rec = dict(snap=snap, z=z, a=a, n_halos=nh, box=BOX, k_knn=K_KNN,
               n_draws=dict(real=N_REAL, S0=N_S0, S0f=N_S0F, S1=N_S1, S1b=N_S1B),
               configs={}, tie=None, ngp=None)

    def flush():
        tmp = out_path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(rec, fh, indent=1)
        os.replace(tmp, out_path)

    flush()
    for cfg in CONFIGS:
        t0 = time.time()
        ng = cfg["ng"]; offs = offsets_for(cfg)
        field = cic_grid(pos, BOX, ng)
        X = template_samples(field, offs)
        N = X.shape[0]
        tied = float(np.mean(np.isclose(X[:, 0], X[:, 0].min())))

        real, C = measure(X, rng, n_ksg=N_REAL)

        s0 = [measure(gaussian_surrogate(C, N, rng), rng)[0] for _ in range(N_S0)]

        amp_f = np.abs(rfftn(field))
        s0f = [measure(template_samples(phase_randomize(amp_f, rng, ng), offs), rng)[0]
               for _ in range(N_S0F)]

        poi = {}
        for key, sub, ndraw in (("S1", True, N_S1), ("S1b", False, N_S1B)):
            amp, mfrac = intensity_template(field, nh, BOX, ng, rng, cic_grid, 2, sub)
            A, ferr, hist = calibrate_A(amp, real["I_gauss"], nh, BOX, ng, rng, cic_grid, offs)
            draws, vs, cls = [], [], []
            for _ in range(ndraw):
                Xn, v, cl = draw_poisson_null(amp, A, nh, BOX, ng, rng, cic_grid, offs)
                draws.append(measure(Xn, rng)[0]); vs.append(v); cls.append(cl)
            poi[key] = (band(draws), dict(A=A, log_resid=ferr, mode_frac=mfrac,
                                          var_dG=float(np.mean(vs)),
                                          clip_frac=float(np.mean(cls)), cal_hist=hist))

        entry = dict(cfg=cfg, N=int(N), cell_mpc=BOX / ng, tied_frac=tied, real=real,
                     S0=band(s0), S0f=band(s0f), S1=poi["S1"][0], S1b=poi["S1b"][0],
                     S1_cal=poi["S1"][1], S1b_cal=poi["S1b"][1],
                     walltime_s=time.time() - t0)
        for key in ("S0", "S0f", "S1", "S1b"):
            entry[f"vs_{key}"] = gap_block(real, entry[key])
        rec["configs"][cfg["id"]] = entry
        flush()
        print(f"[{snap} z={z:.2f}] cfg {cfg['id']} ng={ng} m={cfg['m']} tied={tied:.3f} "
              f"Ig={real['I_gauss']:.4f} | gap_S0={entry['vs_S0']['gap']:+.4f} "
              f"gapc: S0={entry['vs_S0']['gapc']:+.4f} S0f={entry['vs_S0f']['gapc']:+.4f} "
              f"S1={entry['vs_S1']['gapc']:+.4f}(z={entry['vs_S1']['z']:+.1f},"
              f"dIg={entry['vs_S1']['Ig_rel']:+.3f},A={poi['S1'][1]['A']:.2f},"
              f"clip={poi['S1'][1]['clip_frac']:.3f}) "
              f"S1b={entry['vs_S1b']['gapc']:+.4f} ({time.time()-t0:.0f}s)", flush=True)

    # ---------- (a) tie-break decomposition, primary config ----------
    cfgA = CONFIGS[0]; ng = cfgA["ng"]; offs = offsets_for(cfgA)
    field = cic_grid(pos, BOX, ng)
    X = template_samples(field, offs); N = X.shape[0]
    tie = {}
    for mode in ("frozen", "ns_avg", "ns_pos", "ns_rand"):
        Xv = X if mode == "frozen" else ns_transform(X, mode.split("_")[1], rng)
        mv, Cv = measure(Xv, rng, n_ksg=1)
        if mode in ("frozen", "ns_avg"):
            nb = rec["configs"]["A"]["S0"]        # identical C_rank -> reuse the frozen S0 band
        else:
            nb = band([measure(gaussian_surrogate(Cv, N, rng), rng)[0] for _ in range(N_TIE_NULL)])
        tie[mode] = dict(real=mv, null=nb, gap=mv["I_ksg"] - nb["I_ksg"],
                         gapc=mv["resid"] - nb["resid"])
    gp, gr = tie["ns_pos"]["gap"], tie["ns_rand"]["gap"]
    tie["tie_artifact_fraction_gap"] = float((gp - gr) / gp) if gp != 0 else float("nan")
    cp, cr = tie["ns_pos"]["gapc"], tie["ns_rand"]["gapc"]
    tie["tie_artifact_fraction_gapc"] = float((cp - cr) / cp) if cp != 0 else float("nan")
    rec["tie"] = tie
    flush()
    print(f"[{snap} z={z:.2f}] TIE gaps: frozen={tie['frozen']['gap']:+.4f} "
          f"ns_avg={tie['ns_avg']['gap']:+.4f} ns_pos={tie['ns_pos']['gap']:+.4f} "
          f"ns_rand={tie['ns_rand']['gap']:+.4f} artifact_frac="
          f"{tie['tie_artifact_fraction_gap']:+.3f}", flush=True)

    # ---------- (b) NGP vs CIC assignment, primary config ----------
    fld_ngp = ngp_grid(pos, BOX, ng)
    Xn = template_samples(fld_ngp, offs)
    tied_ngp = float(np.mean(np.isclose(Xn[:, 0], Xn[:, 0].min())))
    real_n, Cn = measure(Xn, rng, n_ksg=1)
    s0n = [measure(gaussian_surrogate(Cn, N, rng), rng)[0] for _ in range(2)]
    amp_n, mfrac_n = intensity_template(fld_ngp, nh, BOX, ng, rng, ngp_grid, 1, True)
    A_n, ferr_n, _ = calibrate_A(amp_n, real_n["I_gauss"], nh, BOX, ng, rng, ngp_grid, offs)
    s1n = []
    for _ in range(3):
        Xd, v, cl = draw_poisson_null(amp_n, A_n, nh, BOX, ng, rng, ngp_grid, offs)
        s1n.append(measure(Xd, rng)[0])
    b0, b1 = band(s0n), band(s1n)
    rec["ngp"] = dict(tied_frac=tied_ngp, real=real_n, S0=b0, S1=b1, A=A_n,
                      vs_S0=gap_block(real_n, b0), vs_S1=gap_block(real_n, b1))
    flush()
    print(f"[{snap} z={z:.2f}] NGP tied={tied_ngp:.3f} gapc_S0={rec['ngp']['vs_S0']['gapc']:+.4f} "
          f"gapc_S1={rec['ngp']['vs_S1']['gapc']:+.4f}", flush=True)
    print(f"[{snap}] DONE", flush=True)
    return out_path


if __name__ == "__main__":
    import multiprocessing as mp
    todo = sys.argv[1:] or SNAPS
    with mp.Pool(len(todo)) as pool:
        pool.map(run_snapshot, todo)
    print("all snapshots done")

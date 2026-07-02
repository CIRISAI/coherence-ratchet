#!/usr/bin/env python3
"""
MECHANISM test: is neural k_eff bounded by the SHARED-DRIVER dimensionality
(Gao-Ganguli "dimensionality is task-complexity-bounded"), or is the low-rank
INTRINSIC (and "coordinating units saturate" near-tautological)?

Substrate: ZAPBench whole-brain larval-zebrafish light-sheet (Immer et al. 2025;
Ahrens/Engert). 71,721 neurons x 7,879 volumes, one complete brain. The recording
is 9 successive experimenter-defined visual conditions. The SHARED DRIVER is the
stimulus itself: ZAPBench ships `stimuli_features`, a [7879, 26] feature time-
course (gs://zapbench-release/volumes/20240930/stimuli_features). These are the
experimental stimulus regressors (gain sign, flash on/off, turning/taxis
direction, position). CAVEAT (stated up front): they encode the stimulus
*parameters* (1-4 per condition), a LOWER bound on true perceptual richness --
e.g. random-dot motion ('dots') is one gain regressor here but visually rich.

Three readouts, per condition (c = 1..9):
  neural k_eff(c) : noise-free cross-validated participation ratio of the neural
                    population (framework's own readout; sz.cv_readouts_fullN).
  driver_dim(c)   : participation ratio of the covariance of the active stimulus
                    features within condition c (independent driver estimate).
  stim-locked frac: fraction of neural variance captured by the stimulus subspace
                    (design = active features + lags 0..L); residual k_eff after
                    projecting the stimulus subspace OUT.

DECISIVE reads:
  (1) STIMULUS vs SPONTANEOUS. cond6 and cond8 have ZERO active stimulus features
      (baseline/gray epochs). If saturation is driver-imposed, neural k_eff should
      COLLAPSE there (no shared driver). If k_eff is comparable to stimulus
      epochs, the low-rank is intrinsic.
  (2) DRIVER-DIM MATCH. Correlate neural k_eff(c) vs driver_dim(c) across the 9
      conditions. Track (positive, comparable magnitude) => mechanism/content.
      Unrelated, or neural k_eff >> driver_dim => not driver-bound.
  (3) PROJECT-OUT. If removing the (<=4-dim) stimulus subspace barely changes
      neural k_eff, the neural dimensionality is not the stimulus's.

Real data only (traces memmap + fetched stimuli_features). Reuses sz analysis
core. Incremental JSON flush.
"""
import json
import os
import time

import numpy as np

import spectral_zebrafish as sz

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = sz.SCRATCH
STIM = os.path.join(SCRATCH, "stim_features.npy")          # [7879, 26], fetched
OUT = os.path.join(HERE, "spectral_results_mechanism.json")
SUMMARY = os.path.join(HERE, "spectral_mechanism_summary.md")

OFFSETS = (0, 649, 2422, 3078, 3735, 5047, 5638, 6623, 7279, 7879)
NAMES = ("gain", "dots", "flash", "taxis", "turning", "position",
         "cond6", "cond7", "cond8")
PAD = 1
LAGS = 6            # stimulus design lags 0..LAGS-1 (calcium delay); generous to
                   # the stimulus so it gets its best shot at explaining variance


def pr(ev):
    ev = np.clip(np.asarray(ev, float), 0, None)
    s = ev.sum()
    return float(s * s / np.sum(ev * ev)) if s > 0 else 0.0


def driver_dim(Sc):
    """PR of the covariance of the active stimulus features in a condition."""
    act = Sc.std(0) > 1e-6
    if act.sum() == 0:
        return 0.0, 0
    A = Sc[:, act] - Sc[:, act].mean(0)
    C = A.T @ A / A.shape[0]
    return pr(np.linalg.eigvalsh(C)[::-1]), int(act.sum())


def design_basis(Sc, lags=LAGS):
    """Orthonormal basis Q (T x r) of the stimulus subspace = [active features,
    lagged 0..lags-1] + constant. Returns None if no active stimulus."""
    act = Sc.std(0) > 1e-6
    T = Sc.shape[0]
    cols = [np.ones(T)]
    if act.sum() > 0:
        A = Sc[:, act]
        for L in range(lags):
            Al = np.zeros_like(A)
            if L == 0:
                Al = A.copy()
            else:
                Al[L:] = A[:-L]
            cols.append(Al)
    D = np.column_stack(cols)
    Q, r = np.linalg.qr(D)
    keep = np.abs(np.diag(r)) > 1e-8
    return Q[:, keep]


def neural_pr_fullN(Z):
    ev = sz.full_corr_eigs(Z, np.arange(Z.shape[1]))
    return pr(ev), [float(x) for x in ev[:8]]


def residual_pr_fullN(Z, Q):
    """PR of the neural population AFTER projecting the stimulus subspace out of
    the time axis. Also the stimulus-locked variance fraction. Uses the T-space
    Gram: G = Z Z^T (T x T); stim projector P = Q Q^T; residual Gram
    (I-P) G (I-P); stim-locked frac = tr(P G)/tr(G)."""
    T = Z.shape[0]
    G = np.zeros((T, T))
    for i in range(0, Z.shape[1], sz.CHUNK):
        Zc = np.asarray(Z[:, i:i + sz.CHUNK], np.float64)
        G += Zc @ Zc.T
    if Q is None:
        ev = np.clip(np.linalg.eigvalsh(G)[::-1], 0, None)
        return pr(ev), 0.0
    P = Q @ Q.T
    stim_frac = float(np.trace(P @ G) / np.trace(G))
    R = (np.eye(T) - P)
    Gr = R @ G @ R
    ev = np.clip(np.linalg.eigvalsh(Gr)[::-1], 0, None)
    return pr(ev), stim_frac


def flush(d):
    with open(OUT, "w") as f:
        json.dump(d, f, indent=1)
        f.flush()
        os.fsync(f.fileno())


def main():
    t0 = time.time()
    S = np.load(STIM)                                       # (7879, 26)
    X = np.memmap(sz.MEMMAP, dtype=np.float32, mode="r",
                  shape=(sz.T_FULL, sz.N_FULL))
    Xr = np.asarray(X, np.float32)

    out = dict(
        dataset="ZAPBench whole-brain zebrafish (Immer 2025); mechanism test",
        driver="stimuli_features [7879,26] (experimental stimulus regressors); "
               "driver_dim = PR of active-feature covariance per condition. "
               "CAVEAT: coarse parameters, lower bound on perceptual richness.",
        readout="neural k_eff = noise-free block-CV participation ratio (full N)",
        conditions=[], status="running")
    flush(out)

    print(f"{'cond':9s} {'T':>5s} {'nfeat':>5s} {'drvPR':>6s} {'nPR':>6s} "
          f"{'nf_keff':>7s} {'stimfrac':>8s} {'resPR':>6s} {'res_nfk':>7s}",
          flush=True)

    for i in range(9):
        a, b = OFFSETS[i] + PAD, OFFSETS[i + 1] - PAD
        Sc = S[a:b]
        drv, nfeat = driver_dim(Sc)
        Z = sz.zscore_cols(Xr[a:b].astype(np.float64)).astype(np.float32)
        Q = design_basis(Sc)

        nPR, topev = neural_pr_fullN(Z)
        resPR, stim_frac = residual_pr_fullN(Z, Q)

        cvr = sz.cv_readouts_fullN(Z, np.random.default_rng(7), n_surr=4)
        nfk = cvr["noise_free_keff"]

        # residual noise-free k_eff: same block-CV on the residualized traces
        if Q is not None:
            Zres = (Z.astype(np.float64) - Q @ (Q.T @ Z.astype(np.float64)))
            Zres = sz.zscore_cols(Zres).astype(np.float32)
            cvr_r = sz.cv_readouts_fullN(Zres, np.random.default_rng(8), n_surr=4)
            res_nfk = cvr_r["noise_free_keff"]
        else:
            res_nfk = nfk

        rec = dict(cond_idx=i, name=NAMES[i], frames=[a, b], T=int(b - a),
                   n_active_feats=nfeat, driver_dim=drv,
                   spontaneous=(nfeat == 0),
                   neural_PR_fullN=nPR, neural_topeigs=topev,
                   noise_free_keff=nfk, n_cv_pos=cvr["n_cv_pos"],
                   alpha=cvr["alpha"],
                   stim_locked_var_frac=stim_frac,
                   residual_PR_fullN=resPR, residual_noise_free_keff=res_nfk)
        out["conditions"].append(rec)
        flush(out)
        print(f"{NAMES[i]:9s} {b-a:5d} {nfeat:5d} {drv:6.2f} {nPR:6.2f} "
              f"{nfk:7.2f} {stim_frac:8.3f} {resPR:6.2f} {res_nfk:7.2f}",
              flush=True)

    # ---- cross-condition analysis ----
    C = out["conditions"]
    drv = np.array([c["driver_dim"] for c in C])
    nfeat = np.array([c["n_active_feats"] for c in C], float)
    keff = np.array([c["noise_free_keff"] for c in C])
    nPR = np.array([c["neural_PR_fullN"] for c in C])
    spont = np.array([c["spontaneous"] for c in C])

    def corr(x, y):
        if x.std() < 1e-9 or y.std() < 1e-9:
            return float("nan")
        return float(np.corrcoef(x, y)[0, 1])

    stim_keff = keff[~spont]
    spont_keff = keff[spont]
    analysis = dict(
        pearson_keff_vs_driverdim=corr(drv, keff),
        pearson_keff_vs_nfeat=corr(nfeat, keff),
        pearson_neuralPR_vs_driverdim=corr(drv, nPR),
        driver_dim_range=[float(drv.min()), float(drv.max())],
        neural_keff_range=[float(keff.min()), float(keff.max())],
        stimulus_keff_mean=float(stim_keff.mean()),
        spontaneous_keff_mean=float(spont_keff.mean()) if spont.any() else None,
        spontaneous_conditions=[C[j]["name"] for j in np.where(spont)[0]],
        keff_over_driverdim_ratio=float(np.nanmedian(
            keff[drv > 0] / drv[drv > 0])) if (drv > 0).any() else None,
        mean_stim_locked_frac=float(np.mean(
            [c["stim_locked_var_frac"] for c in C])),
    )
    out["analysis"] = analysis

    tracks = (analysis["pearson_keff_vs_driverdim"] > 0.5
              and 0.5 < (analysis["keff_over_driverdim_ratio"] or 99) < 2.0)
    spont_collapses = (analysis["spontaneous_keff_mean"] is not None
                       and analysis["spontaneous_keff_mean"]
                       < 0.5 * analysis["stimulus_keff_mean"])
    if tracks and spont_collapses:
        verdict = ("MECHANISM (content): neural k_eff tracks shared-driver "
                   "dimensionality and collapses when the driver is removed.")
    else:
        verdict = ("NOT driver-bound (near-tautological / intrinsic): neural "
                   "k_eff does NOT track the measured shared-driver "
                   "dimensionality.")
    out["verdict"] = verdict
    out["status"] = "done"
    out["runtime_s"] = round(time.time() - t0, 1)
    flush(out)
    write_summary(out)
    print(f"\nVERDICT: {verdict}", flush=True)
    print(f"wrote {OUT} and {SUMMARY} ({out['runtime_s']}s)", flush=True)


def write_summary(r):
    C = r["conditions"]
    a = r["analysis"]
    L = [
        "# ZAPBench zebrafish -- MECHANISM test: does k_eff track the shared driver?",
        "",
        "Question (tautology-vs-content crux): is neural effective dimensionality "
        "`k_eff` BOUNDED by the dimensionality of the shared driver (the stimulus) "
        "-- the Gao-Ganguli 'dimensionality is task-complexity-bounded' mechanism "
        "(=> saturation is a mechanistic LAW, content) -- or is the low-rank "
        "INTRINSIC and unrelated to the driver (=> 'coordinating units saturate' "
        "is near-tautological)?",
        "",
        "**Substrate.** ZAPBench whole-brain larval zebrafish (Immer et al. 2025; "
        "Ahrens/Engert), 71,721 neurons x 7,879 volumes, one complete brain, 9 "
        "successive visual conditions.",
        "",
        "**Shared driver.** ZAPBench `stimuli_features` [7879 x 26]: the "
        "experimental stimulus regressors. `driver_dim` = participation ratio of "
        "the active-feature covariance within each condition. **Caveat:** these "
        "are coarse stimulus *parameters* (1-4 per condition; mostly binary/"
        "ternary), a LOWER bound on true perceptual richness (e.g. random-dot "
        "motion is one gain regressor here).",
        "",
        "**Neural k_eff** = noise-free block-interleaved cross-validated "
        "participation ratio at full N (framework's own readout).",
        "",
        "## Per-condition",
        "",
        "| cond | T | active feats | driver_dim (PR) | neural PR | neural k_eff "
        "| stim-locked var frac | residual k_eff (driver projected out) |",
        "|------|---|--------------|-----------------|-----------|--------------|"
        "----------------------|----------------------------------------|",
    ]
    for c in C:
        tag = " (SPONTANEOUS)" if c["spontaneous"] else ""
        L.append(f"| {c['name']}{tag} | {c['T']} | {c['n_active_feats']} | "
                 f"{c['driver_dim']:.2f} | {c['neural_PR_fullN']:.1f} | "
                 f"{c['noise_free_keff']:.2f} | {c['stim_locked_var_frac']:.3f} | "
                 f"{c['residual_noise_free_keff']:.2f} |")
    L += [
        "",
        "## Cross-condition (n=9)",
        "",
        f"- Pearson r(neural k_eff, driver_dim) = **{a['pearson_keff_vs_driverdim']:.3f}**.",
        f"- Pearson r(neural k_eff, n_active_feats) = **{a['pearson_keff_vs_nfeat']:.3f}**.",
        f"- driver_dim range {a['driver_dim_range'][0]:.2f}-{a['driver_dim_range'][1]:.2f}; "
        f"neural k_eff range {a['neural_keff_range'][0]:.2f}-{a['neural_keff_range'][1]:.2f}.",
        f"- median neural k_eff / driver_dim ratio (driven conditions) = "
        f"**{a['keff_over_driverdim_ratio']:.1f}x**.",
        f"- STIMULUS conditions mean k_eff = **{a['stimulus_keff_mean']:.2f}**; "
        f"SPONTANEOUS ({', '.join(a['spontaneous_conditions'])}) mean k_eff = "
        f"**{a['spontaneous_keff_mean']:.2f}**.",
        f"- mean stimulus-locked variance fraction = "
        f"**{a['mean_stim_locked_frac']:.3f}** (fraction of neural variance the "
        f"stimulus subspace, with lags, explains).",
        "",
        f"## VERDICT: {r['verdict']}",
    ]
    with open(SUMMARY, "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()

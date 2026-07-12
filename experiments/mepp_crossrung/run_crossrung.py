#!/usr/bin/env python3
"""
THICKENER 3 — MEPP cross-rung selection consistency.

Does the FORCED bench sigma-functional (corridor_ceiling/sigma_max.py, generalized to a
general observed correlation matrix) select observed structure across rungs against nulls,
the way the flavor run proposes it selects CKM/PMNS? Pre-registration: DECISIONS.md
(sigma-observable, three nulls, "selects" thresholds all frozen before this ran).

Real data only. The only synthetic objects are the pre-committed null ensembles (labeled).
Seed 20260712. CPU. Incremental flush.
"""
import json, os
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
KEFF = os.path.abspath(os.path.join(HERE, "..", "keff_saturation"))
OUT = os.path.join(HERE, "results.json")
SEED = 20260712
rng = np.random.default_rng(SEED)

M_A, M_B, M_C = 500, 500, 200   # null ensemble sizes (frozen in DECISIONS)
PR_TOL = 0.02                    # k_eff match tolerance for NULL-B

results = {"seed": SEED, "meta": {
    "sigma_observable": "sigma_max^N1 (physical, primary) and ^N3 (bare stirring, secondary); "
                        "corridor_ceiling/sigma_max.py generalized to a general spectrum",
    "nulls": "A=phase-randomized (needs series); B=k_eff-matched random spectra (confound null); "
             "C=spectrum-matched Haar eigenvectors (diagnostic)",
    "P": 1.0}}


def flush():
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2, default=float)


# ---------------------------------------------------------------------------
# sigma_max as a pure function of the eigenvalue multiset (see DECISIONS note)
# ---------------------------------------------------------------------------
def sigma_max_N1(evals, P=1.0):
    """Bounded actuation ||Q C^-1||_F^2 <= P.  sigma = P * max_{i<j} eff,
    eff = (1/li+1/lj)/(1/li^2+1/lj^2).  Maximized by the two LARGEST eigenvalues, so we
    only need the top handful — but we scan an ample top set to be safe."""
    lam = np.sort(np.asarray(evals, float))[::-1]
    lam = lam[lam > 1e-12]
    top = lam[:min(len(lam), 40)]           # eff is maximized among large eigenvalues
    a = 1.0 / top
    best = 0.0
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            num = a[i] + a[j]
            den = a[i] ** 2 + a[j] ** 2
            e = num / den
            if e > best:
                best = e
    return float(P * best)


def sigma_max_N3(evals, P=1.0):
    """Bounded bare stirring Tr[Q^T Q] <= P.  sigma = (P/2) max_{i<j}(1/li+1/lj)
    = (P/2)(1/l_min + 1/l_2min) — the two SMALLEST positive eigenvalues."""
    lam = np.sort(np.asarray(evals, float))
    lam = lam[lam > 1e-12]
    if len(lam) < 2:
        return float("nan")
    return float(0.5 * P * (1.0 / lam[0] + 1.0 / lam[1]))


def keff_PR(evals):
    lam = np.asarray(evals, float)
    lam = lam[lam > 0]
    return float(lam.sum() ** 2 / (lam ** 2).sum())


# ---------------------------------------------------------------------------
# correlation matrix + spectrum from a (T x N) data block
# ---------------------------------------------------------------------------
def clean_block(X):
    """Drop non-finite ROWS (timepoints) first, then any all-nan columns. Returns finite (T,N)."""
    X = np.asarray(X, float)
    good_rows = np.all(np.isfinite(X), axis=1)
    X = X[good_rows]
    good_cols = np.all(np.isfinite(X), axis=0)
    return X[:, good_cols]


def corr_spectrum(X):
    """X: (T samples, N units). Returns (eigenvalues sum=N, C, N, T)."""
    X = clean_block(X)
    Xz = (X - X.mean(0)) / (X.std(0) + 1e-12)
    T, N = Xz.shape
    C = (Xz.T @ Xz) / T
    # normalize to a correlation matrix (unit diagonal already ~1 from z-score)
    d = np.sqrt(np.clip(np.diag(C), 1e-12, None))
    C = C / np.outer(d, d)
    ev = np.linalg.eigvalsh(C)
    ev = np.clip(ev, 0, None)
    ev = ev * N / ev.sum()                  # enforce trace = N exactly
    return ev, C, N, T


# ---------------------------------------------------------------------------
# NULL-A: per-channel Fourier phase randomization (preserve marginal PSD, kill x-corr)
# ---------------------------------------------------------------------------
def phase_randomize(X, rng):
    """X: (T, N). Independent random phases per channel -> destroys cross-correlation,
    preserves each channel's power spectrum (hence marginal autocorr)."""
    T, N = X.shape
    F = np.fft.rfft(X, axis=0)
    mag = np.abs(F)
    phases = rng.uniform(0, 2 * np.pi, size=(F.shape[0], N))
    phases[0] = 0.0                          # DC real
    if T % 2 == 0:
        phases[-1] = 0.0                     # Nyquist real
    Fr = mag * np.exp(1j * phases)
    return np.fft.irfft(Fr, n=T, axis=0)


def null_A(Xz, M, rng):
    n1, n3 = [], []
    for _ in range(M):
        Xs = phase_randomize(Xz, rng)
        ev, _, _, _ = corr_spectrum(Xs)
        n1.append(sigma_max_N1(ev)); n3.append(sigma_max_N3(ev))
    return np.array(n1), np.array(n3)


# ---------------------------------------------------------------------------
# NULL-B: random spectra of size N, sum=N, matched participation ratio (k_eff)
#         shape otherwise random (Dirichlet(alpha), alpha swept). Rejection on PR.
# ---------------------------------------------------------------------------
def null_B(N, target_PR, M, rng, tol=PR_TOL, max_tries=400000):
    n1, n3, prs = [], [], []
    tries = 0
    while len(n1) < M and tries < max_tries:
        tries += 1
        alpha = 10.0 ** rng.uniform(-1.5, 1.5)         # sweep concentration -> shape diversity
        w = rng.dirichlet(np.full(N, alpha))
        ev = w * N                                     # sum = N
        pr = keff_PR(ev)
        if abs(pr - target_PR) / target_PR <= tol:
            n1.append(sigma_max_N1(ev)); n3.append(sigma_max_N3(ev)); prs.append(pr)
    return np.array(n1), np.array(n3), np.array(prs), tries


# ---------------------------------------------------------------------------
# NULL-C: same eigenvalues, Haar-random eigenvectors (diagnostic; must give pct~50)
# ---------------------------------------------------------------------------
def null_C_blindness(ev, M, rng):
    """DIAGNOSTIC (not a copula null): build C = Q diag(ev) Q^T with Haar-random Q and
    compute sigma_max on ITS eigenvalues (= ev, up to numerics), WITHOUT renormalizing to
    unit diagonal. Because sigma_max is a function of the eigenvalue multiset only, every
    draw MUST reproduce the observed sigma_max. Returns max relative deviation across draws
    -> an executable proof of eigenvector-blindness. (Renormalizing to a correlation matrix
    would change the spectrum and is a DIFFERENT null; not done here, by design.)"""
    N = len(ev)
    s1_obs, s3_obs = sigma_max_N1(ev), sigma_max_N3(ev)
    dev1, dev3 = 0.0, 0.0
    for _ in range(M):
        A = rng.standard_normal((N, N))
        Qo, _ = np.linalg.qr(A)
        C = (Qo * ev) @ Qo.T
        e2 = np.clip(np.linalg.eigvalsh(0.5 * (C + C.T)), 0, None)
        dev1 = max(dev1, abs(sigma_max_N1(e2) - s1_obs) / max(abs(s1_obs), 1e-12))
        dev3 = max(dev3, abs(sigma_max_N3(e2) - s3_obs) / max(abs(s3_obs), 1e-12))
    return float(dev1), float(dev3)


def pctile(obs, null):
    null = null[np.isfinite(null)]
    if len(null) == 0 or not np.isfinite(obs):
        return float("nan")
    return float(100.0 * np.mean(null <= obs))


# ===========================================================================
# LOAD SUBSTRATES (real data)
# ===========================================================================
def load_substrates():
    import pyarrow.parquet as pq
    subs = []

    fin = pq.read_table(os.path.join(KEFF, "finance_returns_cache.parquet")).to_pandas().values
    subs.append(("finance_SP100", fin, "coordinating", True))

    full = pq.read_table(os.path.join(KEFF, "fullmarket_returns.parquet")).to_pandas().values
    subs.append(("fullmarket_SP500", full, "coordinating", True))

    d = np.load(os.path.join(KEFF, "tngsubbox_checkpoint_T30.npz"))
    used = d["used"] > 0
    for key, name, cls in [("SR_lr", "galaxy_density_TNG", "coordinating"),
                           ("SR_lt", "galaxy_temp_TNG", "coordinating"),
                           ("SR_vr", "galaxy_velocity_TNG", "bound")]:
        arr = d[key]                         # (12 units, 50 times)
        X = arr[:, used].T                   # (T, N)
        subs.append((name, X, cls, True))

    # CONSTRUCTED controls (labeled, not "found")
    Tc, Nc = fin.shape[0], fin.shape[1]
    subs.append(("iid_gaussian_CONSTRUCTED", rng.standard_normal((Tc, Nc)), "dead-control", False))
    subs.append(("phaserand_finance_CONSTRUCTED", phase_randomize(
        (fin - np.nanmean(fin, 0)) / (np.nanstd(fin, 0) + 1e-12), rng), "reversible-control", False))
    return subs


# ===========================================================================
# RUN
# ===========================================================================
if __name__ == "__main__":
    subs = load_substrates()
    per = {}
    print(f"{'substrate':30s} {'N':>4s} {'k_eff':>7s} {'sN1':>8s} {'sN3':>9s} "
          f"{'A1%':>6s} {'B1%':>6s} {'C1%':>6s}")
    for name, X, cls, found in subs:
        ev, C, N, T = corr_spectrum(X)
        Xz_clean = clean_block(X)
        Xz = (Xz_clean - Xz_clean.mean(0)) / (Xz_clean.std(0) + 1e-12)
        keff = keff_PR(ev)
        sN1 = sigma_max_N1(ev); sN3 = sigma_max_N3(ev)

        a1, a3 = null_A(Xz, M_A, rng)
        b1, b3, bpr, btries = null_B(N, keff, M_B, rng)
        devC1, devC3 = null_C_blindness(ev, M_C, rng)

        rec = dict(cls=cls, found=found, N=N, T=T, k_eff=keff,
                   sigma_N1=sN1, sigma_N3=sN3,
                   pctA_N1=pctile(sN1, a1), pctA_N3=pctile(sN3, a3),
                   pctB_N1=pctile(sN1, b1), pctB_N3=pctile(sN3, b3),
                   nullC_maxreldev_N1=devC1, nullC_maxreldev_N3=devC3,
                   nullB_kept=len(b1), nullB_tries=btries,
                   nullB_PR_mean=float(np.mean(bpr)) if len(bpr) else float("nan"),
                   top_eigs=[float(x) for x in np.sort(ev)[::-1][:8]],
                   min_eigs=[float(x) for x in np.sort(ev)[:4]])
        per[name] = rec
        results.setdefault("per_substrate", {})[name] = rec
        flush()
        print(f"{name:30s} {N:4d} {keff:7.2f} {sN1:8.3f} {sN3:9.2f} "
              f"A1={rec['pctA_N1']:5.1f} B1={rec['pctB_N1']:5.1f} devC={devC1:.1e}")

    # ---- class split + confound analysis ----
    names = list(per.keys())
    coord = [n for n in names if per[n]["cls"] in ("coordinating", "bound")]
    ctrl = [n for n in names if per[n]["found"] is False]

    def extremity(n, tag):
        p = per[n][tag]
        return abs(p - 50.0)

    analysis = {}
    for tag in ["pctB_N1", "pctB_N3", "pctA_N1", "pctA_N3"]:
        cx = [extremity(n, tag) for n in coord]
        kx = [extremity(n, tag) for n in ctrl]
        try:
            U, p = stats.mannwhitneyu(cx, kx, alternative="greater")
        except Exception:
            U, p = float("nan"), float("nan")
        analysis[tag] = dict(coord_extremity_median=float(np.median(cx)),
                             ctrl_extremity_median=float(np.median(kx)),
                             coord_pcts=[per[n][tag] for n in coord],
                             ctrl_pcts=[per[n][tag] for n in ctrl],
                             mannwhitney_U=float(U), mannwhitney_p_1sided=float(p))

    # confound: does percentile-extremity track k_eff? (Spearman across all substrates)
    kefs = np.array([per[n]["k_eff"] for n in names])
    conf = {}
    for tag in ["pctA_N1", "pctB_N1", "pctA_N3", "pctB_N3"]:
        ext = np.array([extremity(n, tag) for n in names])
        r, pp = stats.spearmanr(kefs, ext)
        conf[tag + "_vs_keff"] = dict(spearman=float(r), p=float(pp))
    # NULL-C diagnostic: max eigenvector-rotation relative deviation of sigma_max (must be ~0)
    conf["nullC_max_reldev_N1_over_substrates"] = float(
        np.nanmax([per[n]["nullC_maxreldev_N1"] for n in names]))
    conf["nullC_max_reldev_N3_over_substrates"] = float(
        np.nanmax([per[n]["nullC_maxreldev_N3"] for n in names]))

    results["class_split"] = analysis
    results["confound"] = conf
    results["groups"] = dict(coordinating=coord, controls=ctrl)
    flush()

    print("\n--- class split (extremity |pct-50| medians) ---")
    for tag, a in analysis.items():
        print(f"  {tag:9s}: coord {a['coord_extremity_median']:5.1f} vs ctrl "
              f"{a['ctrl_extremity_median']:5.1f}  MW p={a['mannwhitney_p_1sided']:.3f}")
    print("--- confound (extremity vs k_eff Spearman) ---")
    for k, v in conf.items():
        if isinstance(v, dict):
            print(f"  {k:22s}: r={v['spearman']:+.2f} p={v['p']:.3f}")
        else:
            print(f"  {k:22s}: {v:.2f}")
    print(f"\nwrote {OUT}")

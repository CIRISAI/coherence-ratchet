"""
crossrung_lib.py — shared estimators for Path 1 (τ-calibration).

Implements, exactly as pre-registered in PREREGISTRATION.md:
  - within-rung coupling W: mean |Pearson| over constituent pairs, shuffle-
    debiased by quadrature (the E1 layer_rho noise-floor procedure);
  - cross-rung coupling tau: normalised Gaussian mutual information
    I(R_n;R_{n+1}) / min(H_n,H_{n+1}), with a row-permutation shuffle null
    debiased by mean subtraction.

No tuning knobs: PCA component count is tied to the observation count m by the
fixed rule q = min(8, m // 6); the covariance ridge is fixed at 1e-3.
"""
import numpy as np

RIDGE = 1e-3
N_SHUFFLE = 50


def _zscore(X):
    """X is observations x constituents. z-score each constituent column."""
    X = X - X.mean(axis=0, keepdims=True)
    sd = X.std(axis=0)
    keep = sd > 1e-10
    X = X[:, keep] / sd[keep]
    return X


def mean_abs_corr(X):
    """Mean |Pearson| over constituent pairs. X is observations x constituents."""
    Xz = _zscore(X)
    if Xz.shape[1] < 2 or Xz.shape[0] < 3:
        return np.nan
    C = np.corrcoef(Xz, rowvar=False)
    iu = np.triu_indices_from(C, k=1)
    return float(np.nanmean(np.abs(C[iu])))


def within_rung_W(X, rng):
    """Shuffle-debiased within-rung coupling. X is observations x constituents.
    Returns (raw, floor, debiased) with quadrature debias (E1 procedure)."""
    raw = mean_abs_corr(X)
    Xs = np.column_stack([rng.permutation(X[:, j]) for j in range(X.shape[1])])
    floor = mean_abs_corr(Xs)
    if np.isnan(raw) or np.isnan(floor):
        return raw, floor, np.nan
    debiased = float(np.sqrt(max(raw ** 2 - floor ** 2, 0.0)))
    return raw, floor, debiased


def _pca_reduce(X, q):
    """Reduce observations x constituents matrix X to q PCA components."""
    Xz = X - X.mean(axis=0, keepdims=True)
    sd = Xz.std(axis=0)
    Xz = Xz[:, sd > 1e-10]
    if Xz.shape[1] == 0:
        return np.zeros((X.shape[0], 0))
    # whiten columns lightly so PCA is on a correlation-like scale
    Xz = Xz / Xz.std(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Xz, full_matrices=False)
    q = min(q, U.shape[1])
    return U[:, :q] * S[:q]


def _gauss_entropy(C):
    d = C.shape[0]
    sign, logdet = np.linalg.slogdet(C + RIDGE * np.eye(d))
    return 0.5 * (d * np.log(2 * np.pi * np.e) + logdet)


def _gauss_mi(Rn, Rm):
    """Gaussian MI between two observations x q representations, and the two
    marginal entropies. Returns (mi, H_n, H_m)."""
    A = _zscore(Rn)
    B = _zscore(Rm)
    if A.shape[1] == 0 or B.shape[1] == 0:
        return np.nan, np.nan, np.nan
    Cn = np.cov(A, rowvar=False)
    Cm = np.cov(B, rowvar=False)
    Cn = np.atleast_2d(Cn)
    Cm = np.atleast_2d(Cm)
    J = np.cov(np.hstack([A, B]), rowvar=False)
    Hn = _gauss_entropy(Cn)
    Hm = _gauss_entropy(Cm)
    Hj = _gauss_entropy(J)
    mi = Hn + Hm - Hj
    return float(mi), float(Hn), float(Hm)


def cross_rung_tau(Xn, Xm, m_obs, rng, n_shuffle=N_SHUFFLE):
    """Normalised cross-rung mutual information tau = I/min(H_n,H_m), with a
    row-permutation shuffle null. Xn, Xm are observations x constituents at the
    two rungs (same observation rows). Returns dict with raw/floor/debiased."""
    q = min(8, m_obs // 6)
    q = max(q, 1)
    Rn = _pca_reduce(Xn, q)
    Rm = _pca_reduce(Xm, q)
    mi, Hn, Hm = _gauss_mi(Rn, Rm)
    if np.isnan(mi):
        return dict(q=q, tau_raw=np.nan, tau_floor=np.nan, tau_debiased=np.nan,
                    mi=np.nan)
    denom = max(min(abs(Hn), abs(Hm)), 1e-9)
    tau_raw = mi / denom
    nulls = []
    for _ in range(n_shuffle):
        perm = rng.permutation(Rm.shape[0])
        mi_s, Hn_s, Hm_s = _gauss_mi(Rn, Rm[perm])
        d_s = max(min(abs(Hn_s), abs(Hm_s)), 1e-9)
        nulls.append(mi_s / d_s)
    tau_floor = float(np.nanmean(nulls))
    tau_debiased = max(tau_raw - tau_floor, 0.0)
    return dict(q=q, tau_raw=float(tau_raw), tau_floor=tau_floor,
                tau_debiased=float(tau_debiased), mi=float(mi),
                H_n=float(Hn), H_m=float(Hm),
                tau_floor_sd=float(np.nanstd(nulls)))

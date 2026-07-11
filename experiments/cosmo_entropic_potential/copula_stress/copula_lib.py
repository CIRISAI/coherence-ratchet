"""
copula_lib — estimators for the copula-Gaussianity stress test.

The object under test (T-E5c, EntropicPotential.lean):
    S = -ln det C = 2 * I,   I = Gaussian multi-information.
This EQUALITY holds iff the COPULA is Gaussian, NOT iff the field is Gaussian.
Both S and I are copula functionals (invariant under monotone per-component maps).
A lognormal field has a Gaussian copula, so its 2-point log-det is exact regardless
of its (very non-Gaussian) marginals. The residual we hunt is the departure of the
TRUE copula from Gaussian: the higher-order clustering beyond lognormal.

Core estimators:
  - ksg_multiinformation : KSG k-NN total-correlation (multi-information) estimator.
  - gaussian_copula_MI   : the Gaussian-copula baseline -0.5 ln det C_rank, where
                           C_rank is the correlation of the normal-score transforms.
  - normal_scores        : rank -> Gaussian score (van der Waerden) marginal transform.
The GAP  = I_true(KSG) - I_gaussian_copula  is the higher-order coordination the
pipeline's 2-point log-det misses. Sign of the gap: + adds coordination, - inverts
(the fermionic Hubbard warning).
"""
import numpy as np
from scipy.special import digamma
from scipy.spatial import cKDTree
from scipy.stats import norm, rankdata


# ---------------------------------------------------------------------------
# marginal transforms
# ---------------------------------------------------------------------------
def ranks_uniform(X):
    """Column-wise empirical-copula transform: ranks -> (0,1) uniform marginals.
    X: (N, m). Ties broken by 'average'. Returns U in (0,1)."""
    X = np.asarray(X, float)
    N = X.shape[0]
    U = np.empty_like(X)
    for j in range(X.shape[1]):
        U[:, j] = rankdata(X[:, j], method="average") / (N + 1.0)
    return U


def normal_scores(X):
    """van der Waerden normal-score transform: rank -> Phi^{-1}(rank/(N+1)).
    Makes each marginal standard-normal while preserving the copula (ranks)."""
    return norm.ppf(ranks_uniform(X))


# ---------------------------------------------------------------------------
# KSG multi-information (total correlation) estimator
# ---------------------------------------------------------------------------
def ksg_multiinformation(X, k=4, add_jitter=True, rng=None):
    """
    KSG1 k-NN estimator of the multi-information (total correlation)
        I(X_1,...,X_m) = sum_i H(X_i) - H(X_1,...,X_m)
    for m scalar variables (columns of X). Chebyshev (max) norm in the joint space.

        I_hat = psi(k) + (m-1) psi(N) - < sum_i psi(n_{i}+1) >

    where for each sample eps = distance to its k-th neighbour in the joint
    (max-norm) space, and n_i = # points with |x_i - x_i'| < eps in marginal i.
    Validated against the analytic Gaussian -0.5 ln det C in tier 1.

    X: (N, m). Returns scalar nats.
    """
    X = np.asarray(X, float)
    N, m = X.shape
    if rng is None:
        rng = np.random.default_rng(0)
    if add_jitter:
        # break exact ties (from discreteness) at a scale far below any real structure
        scale = np.maximum(np.std(X, axis=0), 1e-12) * 1e-10
        X = X + rng.standard_normal(X.shape) * scale

    # joint k-th neighbour distance under Chebyshev norm
    tree = cKDTree(X)
    # query k+1 (self is nearest); distances under p=inf
    dists, _ = tree.query(X, k=k + 1, p=np.inf)
    eps = dists[:, k]  # distance to k-th neighbour (excluding self)

    # per-marginal counts within eps (strict), Chebyshev in 1D = |dx|
    acc = np.zeros(N)
    for j in range(m):
        xj = X[:, j].reshape(-1, 1)
        tj = cKDTree(xj)
        # count neighbours within radius eps (includes self); open ball via tiny shrink
        # query_ball_point returns counts including self -> subtract 1
        nj = tj.query_ball_point(xj, r=eps - 1e-15 * np.maximum(eps, 1.0),
                                 p=np.inf, return_length=True)
        acc += digamma(nj)  # nj already includes self -> this is psi(n_i+1) with n_i=nj-1
    I = digamma(k) + (m - 1) * digamma(N) - np.mean(acc)
    return float(I)


# ---------------------------------------------------------------------------
# Gaussian-copula baseline
# ---------------------------------------------------------------------------
def _nearest_psd_corr(C):
    """Project a symmetric matrix to the nearest PSD correlation matrix (clip eigs)."""
    C = 0.5 * (C + C.T)
    w, V = np.linalg.eigh(C)
    w = np.clip(w, 1e-10, None)
    C2 = (V * w) @ V.T
    d = np.sqrt(np.diag(C2))
    C2 = C2 / np.outer(d, d)
    return C2


def gaussian_copula_MI(X, from_normal_scores=True):
    """
    The Gaussian-copula baseline: -0.5 ln det C, where C is the correlation matrix
    of the NORMAL-SCORE transform of X (so C is the rank/Gaussianized correlation).
    This is the multi-information the field WOULD have if its copula were Gaussian
    with the observed pairwise rank correlations. Returns (I, C, n_clip) where
    n_clip flags whether a PSD projection was needed.
    """
    Z = normal_scores(X) if from_normal_scores else np.asarray(X, float)
    C = np.corrcoef(Z, rowvar=False)
    w = np.linalg.eigvalsh(C)
    n_clip = int((w <= 1e-10).sum())
    if n_clip > 0:
        C = _nearest_psd_corr(C)
    sign, logdet = np.linalg.slogdet(C)
    I = -0.5 * logdet
    return float(I), C, n_clip


def analytic_gaussian_MI(C):
    """-0.5 ln det C for a known correlation matrix C (tier-1 truth)."""
    sign, logdet = np.linalg.slogdet(C)
    return -0.5 * logdet


# ---------------------------------------------------------------------------
# uniform-rho (Kish) correlation matrix and its multi-information
# ---------------------------------------------------------------------------
def kish_corr(m, rho):
    C = np.full((m, m), rho, float)
    np.fill_diagonal(C, 1.0)
    return C


def kish_MI(m, rho):
    """I = -0.5 ln det C(m,rho), det = (1+rho(m-1))(1-rho)^(m-1). = S/2."""
    det = (1 + rho * (m - 1)) * (1 - rho) ** (m - 1)
    return -0.5 * np.log(det)


# ---------------------------------------------------------------------------
# CIC gridding of a point set into a periodic density field
# ---------------------------------------------------------------------------
def cic_grid(pos, box, ng, weights=None):
    """Cloud-in-cell deposit of points (with optional weights) onto an ng^3 periodic
    grid. Returns the overdensity field delta = rho/mean - 1, shape (ng,ng,ng)."""
    pos = np.asarray(pos, float)
    N = pos.shape[0]
    if weights is None:
        weights = np.ones(N)
    weights = np.asarray(weights, float)
    g = (pos / box) * ng  # grid coordinates in [0, ng)
    i0 = np.floor(g).astype(int)
    d = g - i0
    field = np.zeros((ng, ng, ng))
    for dx in (0, 1):
        wx = (d[:, 0] if dx else 1 - d[:, 0])
        ix = (i0[:, 0] + dx) % ng
        for dy in (0, 1):
            wy = (d[:, 1] if dy else 1 - d[:, 1])
            iy = (i0[:, 1] + dy) % ng
            for dz in (0, 1):
                wz = (d[:, 2] if dz else 1 - d[:, 2])
                iz = (i0[:, 2] + dz) % ng
                np.add.at(field, (ix, iy, iz), weights * wx * wy * wz)
    mean = field.mean()
    return field / mean - 1.0


def template_samples(field, offsets):
    """Given a periodic field (ng^3) and a template = list of integer offset vectors
    (relative cell positions), produce the (ng^3, m) matrix of the m-tuple sampled at
    every grid origin under statistical homogeneity (periodic translation ensemble)."""
    ng = field.shape[0]
    idx = np.indices((ng, ng, ng)).reshape(3, -1).T  # (ng^3, 3) origins
    cols = []
    for off in offsets:
        oi = (idx + np.array(off)) % ng
        cols.append(field[oi[:, 0], oi[:, 1], oi[:, 2]])
    return np.stack(cols, axis=1)


def gaussian_surrogate(C, N, rng):
    """Draw N samples of a multivariate normal with correlation C (exact Gaussian
    copula). Used to cancel KSG finite-sample bias: gap = I_KSG(real) - I_KSG(surr)."""
    C = _nearest_psd_corr(C)
    L = np.linalg.cholesky(C)
    Z = rng.standard_normal((N, C.shape[0])) @ L.T
    return Z

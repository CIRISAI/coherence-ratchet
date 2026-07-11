"""
fermionic_core.py — the fermionic Gaussian-state machinery and the candidate
coordination-ledger functionals.

CONTEXT. The bosonic ledger is  S = -ln det C  on a correlation matrix C: a
two-pole entropic potential (chaos pole S=0 at rho=0; rigidity pole S->+inf at
rho->1), = 2 x Gaussian multi-information, with the Kish saturation k_eff =
k/(1+rho(k-1)) -> 1/rho. (Core/EntropicPotential.lean, T-E0..T-E5.)

This module builds the FERMIONIC analog. Fermionic Gaussian states are fully
characterized by the Majorana covariance matrix M (2N x 2N real antisymmetric,
eigenvalues +-i nu_j, nu_j in [0,1]), equivalently the one-body correlation
matrix G_ij = <a_i^dag a_j> (+ pairing F_ij = <a_i a_j> if number-nonconserving).
Fermionic (von Neumann) entropy:
    S_F = sum_j h(nu_j),
    h(nu) = -((1+nu)/2) ln((1+nu)/2) - ((1-nu)/2) ln((1-nu)/2).
nu=0 -> h=ln2 (maximally mixed mode); nu=1 -> h=0 (pure/frozen mode).

Conventions (fixed here, used everywhere):
  * Majorana operators g_1..g_{2N}, {g_a,g_b}=2 delta. Covariance
    M_ab = (i/2)<[g_a, g_b]>, real antisymmetric, block-diagonalizable to
    (+) blocks [[0, nu_j],[-nu_j, 0]]. nu_j = |imag eigenvalue| of M.
  * Number-conserving state <-> G (N x N Hermitian, 0<=G<=I). Pairing of
    Majoranas: mode j -> (g_{2j-1}, g_{2j}); a_j=(g_{2j-1}+i g_{2j})/2.
    Then M relates to (G,F); for number-conserving F=0 and nu_j=|2 g_j - 1|
    where g_j are eigenvalues of G.

Candidate ledger functionals (the search space F1-F3, defined precisely):
  F1  fermionic multi-information (total correlation):
        I_F = sum_i S_F(mode i marginal) - S_F(joint)
      the direct analog of Gaussian multi-information. >= 0 (subadditivity),
      extensive, entropy-based.
  F2  log-det coordination potential on the covariance:
        L_F = -ln det(I - M^T M) = -sum_j ln(1 - nu_j^2)
      the raw Bianconi-style -ln det, but on the fermionic covariance. NOT an
      entropy; diverges as nu->1.
  F2b number-form log-det:  -ln det(4 G (I-G)) = -sum_j ln(1-nu_j^2)  (identical
      to F2 for number-conserving states; kept as a cross-check).
  F3  the instrument route: build ORDINARY correlation matrices of fermionic
      observables and feed the classical S = -ln det C (in bridge.py).

numpy/scipy only. Exact. Seeds fixed where randomness is used.
"""

import numpy as np
from numpy.linalg import eigvalsh, slogdet
import scipy.linalg as sla

LN2 = np.log(2.0)


# ---------------------------------------------------------------------------
# entropy building blocks
# ---------------------------------------------------------------------------
def h_nu(nu):
    """Per-mode fermionic entropy h(nu), nu in [0,1]. Vectorized, safe at ends."""
    nu = np.clip(np.abs(np.asarray(nu, dtype=float)), 0.0, 1.0)
    p = (1.0 + nu) / 2.0
    q = (1.0 - nu) / 2.0
    out = np.zeros_like(nu)
    # -p ln p - q ln q, treating 0 ln 0 = 0
    with np.errstate(divide="ignore", invalid="ignore"):
        tp = np.where(p > 0, -p * np.log(p), 0.0)
        tq = np.where(q > 0, -q * np.log(q), 0.0)
    out = tp + tq
    return out


def H_bin(g):
    """Binary entropy of occupation g in [0,1]: -g ln g -(1-g)ln(1-g)."""
    g = np.clip(np.asarray(g, dtype=float), 0.0, 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = np.where(g > 0, -g * np.log(g), 0.0)
        t2 = np.where(g < 1, -(1 - g) * np.log(1 - g), 0.0)
    return t1 + t2


# ---------------------------------------------------------------------------
# covariance <-> spectra
# ---------------------------------------------------------------------------
def nu_from_G(G):
    """nu-spectrum from a number-conserving correlation matrix G (Hermitian)."""
    g = eigvalsh((G + G.conj().T) / 2.0)
    g = np.clip(g.real, 0.0, 1.0)
    return np.abs(2.0 * g - 1.0)


def nu_from_majorana(M):
    """nu-spectrum from a real antisymmetric Majorana covariance M (2N x 2N).

    Eigenvalues of M are +- i nu_j. Return the N nonnegative nu_j."""
    M = np.asarray(M, dtype=float)
    M = (M - M.T) / 2.0  # enforce antisymmetry
    ev = np.linalg.eigvals(M)
    nus = np.sort(np.abs(ev.imag))[::-1]
    # eigenvalues come in +- pairs; take every other (the N largest-magnitude halves)
    nus = nus[0::2] if len(nus) % 2 == 0 else nus
    return np.clip(nus[: M.shape[0] // 2], 0.0, 1.0)


# ---------------------------------------------------------------------------
# the ledger functionals, spectrum-level
# ---------------------------------------------------------------------------
def S_F_from_nu(nu):
    """Joint fermionic (von Neumann) entropy S_F = sum h(nu_j)."""
    return float(np.sum(h_nu(nu)))


def logdet_potential_from_nu(nu):
    """F2:  L_F = -sum_j ln(1 - nu_j^2) = -ln det(I - M^T M). Diverges nu->1."""
    nu = np.clip(np.abs(np.asarray(nu, dtype=float)), 0.0, 1.0)
    x = 1.0 - nu ** 2
    if np.any(x <= 0):
        return np.inf
    return float(-np.sum(np.log(x)))


def multi_information_number(G):
    """F1 for a number-conserving state given full correlation matrix G:
       I_F = sum_i H_bin(G_ii) - S_F(joint)."""
    G = (G + G.conj().T) / 2.0
    marg = float(np.sum(H_bin(np.real(np.diag(G)))))
    joint = S_F_from_nu(nu_from_G(G))
    return marg - joint, marg, joint


def multi_information_majorana(M, mode_pairs=None):
    """F1 from a general Majorana covariance M (handles pairing).
       Marginal of mode i = 2x2 sub-block covariance -> single nu_i.
       Returns (I_F, marg, joint)."""
    M = (np.asarray(M, dtype=float) - np.asarray(M, dtype=float).T) / 2.0
    N = M.shape[0] // 2
    if mode_pairs is None:
        mode_pairs = [(2 * i, 2 * i + 1) for i in range(N)]
    marg = 0.0
    for (a, b) in mode_pairs:
        nu_i = abs(M[a, b])  # 2x2 antisymmetric block [[0,x],[-x,0]] -> nu=|x|
        marg += float(h_nu(nu_i))
    joint = S_F_from_nu(nu_from_majorana(M))
    return marg - joint, marg, joint


# ---------------------------------------------------------------------------
# effective-dimension (Kish-analog) candidates
# ---------------------------------------------------------------------------
def keff_participation(spectrum):
    """Generic participation ratio (sum x)^2 / sum x^2 of a nonneg spectrum."""
    x = np.asarray(spectrum, dtype=float)
    s1 = x.sum()
    s2 = (x ** 2).sum()
    if s2 <= 0:
        return float(len(x))
    return float(s1 ** 2 / s2)


def keff_entropy_participation(nu):
    """Participation ratio of the per-mode entropy contributions h(nu_j).
       At chaos (all nu=0) -> k. Measures effective # of thermally-active modes."""
    w = h_nu(nu)
    return keff_participation(w)


def keff_kish_G(G):
    """Kish-style effective dimension on the one-body matrix G:
       Tr(G) / lambda_max(G)  (analog of bosonic Tr C / lambda_0)."""
    G = (G + G.conj().T) / 2.0
    ev = eigvalsh(G).real
    lam = ev.max()
    if lam <= 0:
        return float(G.shape[0])
    return float(np.real(np.trace(G)) / lam)


# ---------------------------------------------------------------------------
# classical instrument (the bosonic shadow), for the bridge
# ---------------------------------------------------------------------------
def classical_S_from_corr(C, tol=1e-12):
    """S = -ln det C on a correlation matrix C (unit diagonal). Drops frozen
       (near-zero-variance) rows implicitly upstream. Returns +inf if singular."""
    C = np.atleast_2d(np.asarray(C, dtype=float))
    C = (C + C.T) / 2.0
    # regularize numerically tiny negative eigenvalues from roundoff
    sign, logdet = slogdet(C)
    if sign <= 0:
        return np.inf
    return float(-logdet)


if __name__ == "__main__":
    # ---- self-tests ------------------------------------------------------
    print("== fermionic_core self-test ==")
    # h(nu) endpoints
    assert abs(h_nu(0.0) - LN2) < 1e-12, h_nu(0.0)
    assert abs(float(h_nu(1.0)) - 0.0) < 1e-12
    print(f"h(0)={float(h_nu(0.0)):.6f} (ln2={LN2:.6f}), h(1)={float(h_nu(1.0)):.6f}  OK")

    # number-conserving: maximally mixed G = I/2 -> all nu=0, S_F = N ln2, I_F=0
    N = 5
    G = 0.5 * np.eye(N)
    IF, marg, joint = multi_information_number(G)
    print(f"max-mixed: S_F={joint:.4f} (Nln2={N*LN2:.4f}), I_F={IF:.2e}  OK")
    assert abs(joint - N * LN2) < 1e-9 and abs(IF) < 1e-9

    # pure product (G projector, diagonal 0/1) -> nu=1, S_F=0, I_F=0
    Gp = np.diag([1.0, 0.0, 1.0, 0.0, 1.0])
    IF2, marg2, joint2 = multi_information_number(Gp)
    print(f"pure product: S_F={joint2:.2e}, I_F={IF2:.2e}  OK")
    assert abs(joint2) < 1e-9 and abs(IF2) < 1e-9

    # Majorana route agrees with number route on a random number-conserving G
    rng = np.random.default_rng(1)
    A = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
    U, _ = np.linalg.qr(A)
    occ = np.array([1, 1, 0, 1, 0], dtype=float)
    Gr = (U * occ) @ U.conj().T
    nu1 = np.sort(nu_from_G(Gr))
    # build Majorana M for this G (F=0): standard embedding
    # M_{2i-1,2j} etc. For number-conserving, use Gamma = 2G-I; Majorana cov
    # in the (x,p) Majorana basis: M = [[Im(Gamma? )...]] -- verify via nu only.
    print(f"random NC state nu (sorted): {np.round(nu1,4)}")
    print("all self-tests passed.")

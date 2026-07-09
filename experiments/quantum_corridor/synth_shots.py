#!/usr/bin/env python3
"""
Synthetic shot generators for the quantum-corridor calibration leg (SPEC.md §4.4, N5).

NO quantum libraries. Every "shot" is synthesized classically from the known outcome
statistics of a state class. Each generator returns an integer array of shape
(S shots, N qubits) with +1/-1 entries -- the Operationalization-A raw shot matrix of
SPEC §4.2. calibrate.py transposes this to the estimator's UNITS(N) x OBSERVATIONS(T=S)
convention and pushes it through the identical spectral_test.py front-end.

State classes (pre-declared expectations, SPEC §5, Op-A, Z basis unless noted):
  product         -> CHAOS      (rho_bar ~ 0, k_eff ~ N, beta ~ 1)
  ghz_z           -> RIGIDITY   (rho_bar ~ 1, k_eff ~ 1)      [Z basis: perfect corr]
  ghz_x           -> CHAOS      (rho_bar ~ 0, k_eff ~ N)      [X basis: N-body parity,
                                 invisible to the pairwise correlation matrix -- the
                                 SPEC-flagged MUB fragility, demonstrated exactly]
  ghz_depolarized -> ramp from RIGIDITY (p=0) to CHAOS (p=1)  [C2/C3 maintenance surrogate]
  low_rank (r=3)  -> CORRIDOR   (bounded k_eff, beta ~ 0, saturation)
  powerlaw(alpha) -> CRITICAL   (power-law spectrum, beta in [0.3,0.8]) [copula-thresholded]
  shot_noise      -> CHAOS/noise(rho_bar ~ 0, eff-rank 0, beta ~ 1)

+/-1 thresholding caveat: the low_rank and powerlaw classes are built from a latent
Gaussian and then sign()-thresholded to +/-1 outcomes. By the Van Vleck arcsine law the
binary correlation is attenuated relative to the latent Gaussian correlation,
    E[sign(x)sign(y)] = (2/pi) * arcsin(rho_gauss),
so a latent rho_gauss=0.9 reads as ~0.71 in +/-1 outcomes. This flattens the eigenvalue
spectrum (pulls it toward the noise floor); the calibration must still separate the
classes AFTER this attenuation, which is the honest quantum-measurement condition.
"""
import numpy as np

# ---------------------------------------------------------------------------
# Van Vleck arcsine law, exposed so calibrate.py can report the attenuation.
def vanvleck(rho_gauss):
    """Binary (+/-1) correlation induced by sign-thresholding a bivariate Gaussian."""
    return (2.0 / np.pi) * np.arcsin(np.clip(rho_gauss, -1, 1))


# ---------------------------------------------------------------------------
# 1. Product state: independent qubits with per-qubit bias.
def product_shots(S, N, rng, bias=None, basis="Z"):
    """
    Independent outcomes; qubit i is +1 with probability p_i.
    A product state has independent outcomes in ANY single-qubit basis, so 'basis'
    only changes the per-qubit bias, never the (zero) cross-qubit correlation.
    """
    if bias is None:
        # mild per-qubit bias so marginals differ but qubits stay independent
        base = 0.5 if basis == "X" else 0.5
        bias = base + 0.15 * (rng.random(N) - 0.5)
    U = rng.random((S, N))
    return np.where(U < bias[None, :], 1, -1).astype(np.int8)


# ---------------------------------------------------------------------------
# 2a. GHZ in the Z (computational) basis: perfectly correlated outcomes.
def ghz_z_shots(S, N, rng):
    """
    |GHZ> = (|0..0> + |1..1>)/sqrt(2). Z-basis measurement -> all-+1 or all--1 with
    p=1/2. Every qubit identical each shot => correlation matrix = all-ones => rank 1
    => the RIGIDITY pole (k_eff -> 1). Random single-qubit marginals, perfect pairwise
    correlation (SPEC §2 pitfall, reproduced exactly).
    """
    g = rng.choice(np.array([-1, 1], dtype=np.int8), size=S)
    return np.repeat(g[:, None], N, axis=1)


# 2b. GHZ in the X basis: exact N-body parity structure.
def ghz_x_shots(S, N, rng):
    """
    X^{otimes N}|GHZ+> = |GHZ+>, so measuring all qubits in X gives bitstrings with
    FIXED global parity (even number of -1 outcomes for the + GHZ). Each single qubit
    is a uniform +/-1; and for N>2 every PAIRWISE correlation <X_i X_j> = 0 (X_iX_j
    maps |GHZ> off itself). So the pairwise correlation matrix is ~ I and the register
    reads as CHAOS -- even though it is maximally coordinated through the N-body parity
    constraint, which is invisible to a 2-point correlation matrix. This is generated
    EXACTLY (not omitted): draw N-1 fair bits, fix the last to enforce even parity.
    """
    bits = rng.integers(0, 2, size=(S, N)).astype(np.int8)  # 0/1
    # enforce even number of ones (parity 0) by setting last bit = XOR of the first N-1
    bits[:, -1] = np.bitwise_xor.reduce(bits[:, :-1], axis=1)
    return (1 - 2 * bits).astype(np.int8)                    # 0->+1, 1->-1


# 2c. Depolarized-GHZ ramp: GHZ mixed with product noise at rate p (C2/C3 surrogate).
def ghz_depolarized_shots(S, N, rng, p):
    """
    Maintenance-withdrawal surrogate: each shot is a clean GHZ (Z) shot with prob (1-p),
    or an independent fair-coin product shot with prob p. Withdrawing the coordinating
    'drive' = raising p. Pairwise correlation E[o_i o_j] = (1-p), so rho_bar ~ 1-p:
    the ramp exits the RIGIDITY pole (p=0, rho_bar->1) toward CHAOS (p=1, rho_bar->0),
    monotonically. This is the pre-declared exit direction for C2, and the trajectory
    (rho_bar, S) is the C3 curve-tracking leg.
    """
    is_prod = rng.random(S) < p
    g = rng.choice(np.array([-1, 1], dtype=np.int8), size=S)
    ghz = np.repeat(g[:, None], N, axis=1)
    prod = rng.choice(np.array([-1, 1], dtype=np.int8), size=(S, N))
    return np.where(is_prod[:, None], prod, ghz).astype(np.int8)


# ---------------------------------------------------------------------------
# 3. Low-rank coordinated state (the corridor class): r latent factors + noise.
def low_rank_shots(S, N, rng, r=3, snr=3.0):
    """
    Outcomes driven by r=3 shared latent Gaussian factors plus independent per-qubit
    noise, then sign-thresholded to +/-1 (Van Vleck attenuation applies). Bounded
    effective rank ~ r, size-independent => saturation branch (beta ~ 0) => CORRIDOR.
    """
    F = rng.standard_normal((r, S))          # shared factors  (r x S)
    W = rng.standard_normal((N, r))          # loadings        (N x r)
    latent = W @ F + (snr ** -1) * np.sqrt(r) * rng.standard_normal((N, S))
    latent = (latent - latent.mean(1, keepdims=True)) / latent.std(1, keepdims=True)
    return np.sign(latent).astype(np.int8).T  # -> (S, N)


# ---------------------------------------------------------------------------
# 4. Power-law / critical surrogate: eigenvalue spectrum lambda_i ~ i^-alpha.
def powerlaw_shots(S, N, rng, alpha=1.0):
    """
    Gaussian copula with covariance eigenvalues lambda_i proportional to i^-alpha in a
    random orthonormal basis, then sign-thresholded to +/-1. Smooth power-law spectrum
    => criticality branch (beta in [0.3,0.8]). +/-1 thresholding attenuates (Van Vleck)
    and pulls the tail toward the noise floor, so the recovered beta/alpha are the
    ATTENUATED values -- reported as such.
    """
    lam = np.arange(1, N + 1, dtype=float) ** (-alpha)
    lam = lam / lam.sum() * N                 # normalize trace to N
    Q, _ = np.linalg.qr(rng.standard_normal((N, N)))
    latent = Q @ (np.sqrt(lam)[:, None] * rng.standard_normal((N, S)))
    latent = (latent - latent.mean(1, keepdims=True)) / latent.std(1, keepdims=True)
    return np.sign(latent).astype(np.int8).T  # -> (S, N)


# ---------------------------------------------------------------------------
# 5. Shot-noise-only: independent fair coins.
def shot_noise_shots(S, N, rng):
    """Independent fair +/-1 coins: rho_bar ~ 0, eff-rank 0, beta ~ 1 (pure chaos)."""
    return rng.choice(np.array([-1, 1], dtype=np.int8), size=(S, N))

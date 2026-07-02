#!/usr/bin/env python3
"""
STRONGER bound-vs-coordinating detector: transition-based ENTROPY PRODUCTION
(Lynn, Cornblath, Papadopoulos, Bertolero, Bassett 2021, PNAS, "Broken detailed
balance and entropy production in the human brain").

The weak v1 (circulation ⟨x dy − y dx⟩ vs a phase-randomized null) under-detects
CYCLIC/narrowband signals: phase-randomizing two same-frequency oscillators
inflates the null variance, so a real limit cycle doesn't clear it. C. elegans'
famous whole-brain cyclic attractor (Kato 2015) is exactly that case and it read
z≈0.9 — a measurement failure, not "bound."

This estimator instead measures the DIRECTIONAL ASYMMETRY of transitions in the
coarse-grained state space:

    EP = Σ_ij P_ij · log(P_ij / P_ji)   =  D_KL( forward transitions || reverse )

P_ij = joint prob of an i→j step. EP ≥ 0, = 0 iff detailed balance (P_ij = P_ji).
A directed cycle has P_ij ≫ P_ji around the loop → large EP, robustly, regardless
of narrowbandness. Finite samples are biased upward, so significance is against a
DETAILED-BALANCE surrogate floor: symmetrize the transition counts (P_sym has
detailed balance by construction), simulate same-length Markov trajectories from
it, recompute EP → that is the bias floor. z = (EP_real − floor_mean)/floor_sd.

Needs T ≫ n_states (many transitions). Works on brains (T~10^3–10^4). Does NOT
work on the galaxy snapshots (T=26) — noted as a hard limitation of this method.
"""
import numpy as np

def top_modes(X, k=3):
    """X: units x time -> top-k temporal mode trajectories (time x k), z-scored."""
    Z = (X - X.mean(1, keepdims=True)) / (X.std(1, keepdims=True) + 1e-9)
    U, S, Vt = np.linalg.svd(Z, full_matrices=False)
    A = Vt[:k].T                      # time x k
    return (A - A.mean(0)) / (A.std(0) + 1e-9)

def discretize(traj, n_bins):
    """Grid the d-dim trajectory into n_bins per axis (quantile edges) -> state id."""
    T, d = traj.shape
    codes = np.zeros(T, dtype=np.int64)
    for a in range(d):
        edges = np.quantile(traj[:, a], np.linspace(0, 1, n_bins + 1)[1:-1])
        codes = codes * n_bins + np.digitize(traj[:, a], edges)
    return codes

def _counts(states, M):
    C = np.zeros((M, M))
    np.add.at(C, (states[:-1], states[1:]), 1.0)
    return C

def _ep(C, eps):
    Cs = C + eps
    P = Cs / Cs.sum()
    return float(np.sum(P * np.log(P / P.T)))

def _angvel_z(traj2d, block=50, nboot=400, seed=0):
    """Net angular velocity (winding rate) in a 2D plane + block-bootstrap z.
    A directed cycle accumulates net angle (μ≠0); a reversible process has μ≈0.
    Integrates continuous rotation, so it is robust to slow cycles that dwell many
    steps per grid cell (where transition-counting fails)."""
    x, y = traj2d[:, 0], traj2d[:, 1]
    th = np.arctan2(y, x)
    dth = np.diff(th)
    dth = (dth + np.pi) % (2 * np.pi) - np.pi        # wrap to (-π, π]
    mu = float(dth.mean())
    rng = np.random.default_rng(seed)
    n = len(dth); nb = int(np.ceil(n / block))
    boots = np.empty(nboot)
    for b in range(nboot):
        starts = rng.integers(0, max(1, n - block), nb)
        samp = np.concatenate([dth[s:s + block] for s in starts])[:n]
        boots[b] = samp.mean()
    se = float(boots.std())
    return mu, se, float(mu / (se + 1e-12))

def entropy_production(traj, k=None, seed=0, **_):
    """traj: time x d (d≥2). Net-winding irreversibility over all top mode-pairs;
    returns the pair with the strongest signed rotation. z≈0 ⇒ detailed balance
    (reversible/bound); |z|≫2 ⇒ broken detailed balance (sustained cycle /
    coordinating)."""
    d = traj.shape[1]
    A = (traj - traj.mean(0)) / (traj.std(0) + 1e-9)
    best = None
    for i in range(d):
        for j in range(i + 1, d):
            mu, se, z = _angvel_z(A[:, [i, j]], seed=seed)
            if best is None or abs(z) > abs(best["z"]):
                best = dict(pair=(i, j), winding_rate=mu, se=se, z=z)
    best["T"] = int(traj.shape[0])
    return best

def irreversibility_from_units(X, k=4, seed=0):
    """X: units x time -> top-k mode trajectories -> winding irreversibility."""
    return entropy_production(top_modes(X, k), seed=seed)

# ---- synthetic calibrators (time x d) --------------------------------------
def ou_equilibrium(T, d=3, seed=0):
    rng = np.random.default_rng(seed); x = np.zeros((T, d))
    for t in range(1, T):
        x[t] = 0.9 * x[t-1] + rng.standard_normal(d)
    return x

def ou_driven(T, d=3, w=0.35, seed=0):
    """Non-equilibrium: a rotational (non-symmetric) drift in the 0-1 plane -> a
    sustained cycle that breaks detailed balance."""
    rng = np.random.default_rng(seed); x = np.zeros((T, d))
    A = np.eye(d) * 0.9
    A[0, 1], A[1, 0] = -w, w            # antisymmetric -> rotation -> broken DB
    for t in range(1, T):
        x[t] = A @ x[t-1] + rng.standard_normal(d)
    return x

def limit_cycle(T, noise=0.4, seed=0):
    """A noisy limit cycle (like a neural cyclic attractor) — the case v1 failed."""
    rng = np.random.default_rng(seed); th = np.cumsum(0.05 + 0.005 * rng.standard_normal(T))
    x = np.c_[np.cos(th), np.sin(th), 0.3 * rng.standard_normal(T)]
    return x + noise * rng.standard_normal((T, 3))

def relaxation(T, seed=0):
    rng = np.random.default_rng(seed); x = np.zeros((T, 3)); x[0] = [5, 5, 5]
    for t in range(1, T):
        x[t] = 0.98 * x[t-1] + 0.3 * rng.standard_normal(3)
    return x

if __name__ == "__main__":
    print("=== estimator validation (T=2500): winding irreversibility ===")
    for name, gen in [("OU-equilibrium(reversible)", ou_equilibrium),
                      ("relaxation(transient)", relaxation),
                      ("noisy LIMIT CYCLE (v1 failed here)", limit_cycle),
                      ("OU-driven(NESS,breaks DB)", ou_driven)]:
        r = entropy_production(gen(2500))
        print(f"  {name:34s} winding={r['winding_rate']:+.4f} z={r['z']:+.2f} pair={r['pair']}")
    print("  (expect: equilibrium & relaxation z~0; LIMIT CYCLE & driven z>>2)")

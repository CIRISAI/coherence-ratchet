#!/usr/bin/env python3
"""
Corridor-ceiling Part A: does the maximum steady-state entropy-production rate
sigma_max(rho,k) of an equicorrelation OU process COLLAPSE, SATURATE, or GROW as
coordination deepens (rho -> 1, k_eff -> 1), under three normalizations?

Object: dx = -B x dt + sqrt(2D) dW, stationary covariance pinned to the Kish object
    C(rho,k) = (1-rho) I + rho * 11^T,
eigenvalues lambda_1 = 1 + rho(k-1) (uniform mode), lambda_2..k = 1 - rho (k-1 fold).

Decomposition B = (D + Q) C^{-1}, D sym PD (diffusion), Q antisymmetric (circulation).
Entropy-production rate (Godrèche-Luck 2019 arXiv:1807.00694; Kwon-Ao-Thouless 2005):
    sigma = Tr[ Q^T D^{-1} Q C^{-1} ]      (VERIFIED numerically below before use)

In C's eigenbasis, with Q antisymmetric entries Q_ij:
    sigma = sum_{i<j} Q_ij^2 (1/lambda_i + 1/lambda_j).

Three normalizations bound the free Q_ij differently (see DECISIONS.md):
  N1 fixed noise D=I, bounded ACTUATED drive ||Q C^{-1}||_F^2 <= P    [physical]
  N2 fixed relaxation timescale, spectral bound ||B||_2 <= b
  N3 fixed BARE stirring power Tr[Q^T Q] <= P

Seed 20260710. CPU only. Incremental flush.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results.json")
rng = np.random.default_rng(20260710)
RHO_C = 0.43  # the empirical upper-corridor value under test

results = {"object": "equicorrelation OU, C=(1-rho)I+rho 11^T",
           "formula": "sigma = Tr[Q^T D^{-1} Q C^{-1}]  (Godreche-Luck 2019, arXiv:1807.00694)",
           "seed": 20260710}


def flush():
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)


# ---------------------------------------------------------------------------
# 0. Building blocks
# ---------------------------------------------------------------------------
def C_kish(rho, k):
    return (1 - rho) * np.eye(k) + rho * np.ones((k, k))


def sigma_from_BD(B, C):
    """Entropy production from a drift B and covariance C (D inferred by Lyapunov)."""
    D = 0.5 * (B @ C + C @ B.T)          # BC + CB^T = 2D
    Q = 0.5 * (B @ C - C @ B.T)          # antisymmetric part of BC
    Dinv = np.linalg.inv(D)
    Cinv = np.linalg.inv(C)
    return float(np.trace(Q.T @ Dinv @ Q @ Cinv)), D, Q


# ---------------------------------------------------------------------------
# 1. VERIFY the closed-form sigma against an INDEPENDENT binned-current estimate
#    from a direct 2D OU simulation (uses only simulated increments + D; never the
#    Tr[Q^T D^{-1} Q C^{-1}] formula or the nu-decomposition).
# ---------------------------------------------------------------------------
def verify_formula_2d():
    """Two independent checks of sigma = Tr[Q^T D^{-1} Q C^{-1}]:
    (a) ANALYTIC: the Sekimoto housekeeping-heat form sigma = Tr(B^T D^{-1} B C) - Tr(B),
        derived independently of the Q-decomposition (mean Stratonovich heat rate in NESS
        for dx = -Bx dt + sqrt(2D)dW). Must match to machine precision.
    (b) MONTE CARLO: simulate the 2D OU (Euler-Maruyama) and estimate the same
        housekeeping-heat rate directly from increments via the Stratonovich midpoint
        <F(x_mid).dx>/dt with F = -D^{-1} B x. Uses only simulated increments + B,D;
        never the closed form. Must match to ~a few percent."""
    rho, k = 0.5, 2
    C = C_kish(rho, k)
    D = np.eye(2)
    q = 0.6
    Q = np.array([[0.0, q], [-q, 0.0]])
    B = (D + Q) @ np.linalg.inv(C)       # drift with stationary cov C
    sig_formula, _, _ = sigma_from_BD(B, C)

    # (a) independent analytic form (Sekimoto heat)
    Dinv = np.linalg.inv(D)
    sig_sekimoto = float(np.trace(B.T @ Dinv @ B @ C) - np.trace(B))

    # (b) independent Monte Carlo of the Stratonovich heat rate
    dt = 1e-3
    T = 3_000_000
    sig_noise = np.linalg.cholesky(2 * D * dt)
    x = np.zeros(2)
    for _ in range(5000):                # burn-in to steady state
        x = x - B @ x * dt + sig_noise @ rng.standard_normal(2)
    heat = 0.0
    for t in range(T):
        xn = x - B @ x * dt + sig_noise @ rng.standard_normal(2)
        xmid = 0.5 * (x + xn)
        F = -Dinv @ B @ xmid             # thermodynamic force, mobility form
        heat += float(F @ (xn - x))      # Stratonovich dQ = F o dx
        x = xn
    sig_mc = heat / (T * dt)

    err_analytic = abs(sig_sekimoto - sig_formula) / abs(sig_formula)
    err_mc = abs(sig_mc - sig_formula) / abs(sig_formula)
    return dict(sigma_formula=sig_formula,
                sigma_sekimoto_independent=sig_sekimoto, err_analytic=err_analytic,
                sigma_montecarlo=sig_mc, err_mc=err_mc,
                verified=bool(err_analytic < 1e-9 and err_mc < 0.05))


# ---------------------------------------------------------------------------
# 2. sigma_max under each normalization (closed form for N1,N3; numeric for N2)
# ---------------------------------------------------------------------------
def eigs(rho, k):
    return np.array([1 + rho * (k - 1)] + [1 - rho] * (k - 1))


def sigma_max_N1(rho, k, P=1.0):
    """Bounded actuated drive ||Q C^{-1}||_F^2 <= P. Linear-fractional over pair
    weights -> single best pair. Distinct pair types: (uniform,collapsed) and
    (collapsed,collapsed). eff = yield/cost, sigma_max = P * max eff."""
    l1 = 1 + rho * (k - 1)
    l2 = 1 - rho
    effs = []
    # uniform-collapsed pair
    effs.append((1/l1 + 1/l2) / (1/l1**2 + 1/l2**2))
    # collapsed-collapsed pair (needs k>=3)
    if k >= 3:
        effs.append((2/l2) / (2/l2**2))   # = l2 = (1-rho)
    eff = max(effs)
    return P * eff


def sigma_max_N3(rho, k, P=1.0):
    """Bounded bare stirring Tr[Q^T Q] <= P. sigma_max = (P/2)*max_pair(1/li+1/lj)."""
    l1 = 1 + rho * (k - 1)
    l2 = 1 - rho
    vals = [1/l1 + 1/l2]
    if k >= 3:
        vals.append(2/l2)
    return 0.5 * P * max(vals)


def sigma_max_N2(rho, k, b=3.0):
    """Fixed relaxation timescale: spectral bound ||B||_2 <= b, D=I, B=(I+Q)C^{-1}.
    Numeric: single rotation pair Q of magnitude q in each distinct pair type;
    maximize sigma s.t. ||B||_2 <= b. Returns (sigma_max, feasible)."""
    C = C_kish(rho, k)
    Cinv = np.linalg.inv(C)
    # feasibility: even Q=0 gives ||C^{-1}||_2 = 1/(1-rho); if > b, NESS infeasible
    base_norm = np.linalg.norm(Cinv, 2)
    if base_norm > b:
        return 0.0, False
    # eigenbasis of C
    w, V = np.linalg.eigh(C)             # ascending: collapsed modes first
    order = np.argsort(-w)               # uniform mode first
    w = w[order]; V = V[:, order]
    pair_types = [(0, 1)]                # uniform-collapsed
    if k >= 3:
        pair_types.append((1, 2))        # collapsed-collapsed
    best = 0.0
    for (i, j) in pair_types:
        # Q = q (e_i e_j^T - e_j e_i^T) in eigenbasis -> back to original basis
        E = np.zeros((k, k)); E[i, j] = 1.0; E[j, i] = -1.0
        Qbasis = V @ E @ V.T
        li, lj = w[i], w[j]
        # scan q; sigma = q^2 (1/li + 1/lj); constraint ||(I+qQbasis)C^{-1}||_2 <= b
        qs = np.linspace(0, 50, 4000)
        for q in qs:
            B = (np.eye(k) + q * Qbasis) @ Cinv
            if np.linalg.norm(B, 2) <= b:
                s = q**2 * (1/li + 1/lj)
                if s > best:
                    best = s
            else:
                # norm grows monotonically in q for these blocks; stop early
                if q > 0:
                    break
    return float(best), True


# ---------------------------------------------------------------------------
# 3. run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("[1/3] verifying OU entropy-production formula (independent 2D MC)...")
    ver = verify_formula_2d()
    results["formula_verification"] = ver
    print(f"    formula={ver['sigma_formula']:.4f}  "
          f"Sekimoto(indep analytic)={ver['sigma_sekimoto_independent']:.4f} "
          f"(err {ver['err_analytic']:.1e})  "
          f"MC={ver['sigma_montecarlo']:.4f} (err {ver['err_mc']*100:.1f}%)  "
          f"verified={ver['verified']}")
    flush()
    if not ver["verified"]:
        print("    WARNING: formula not verified to 10% — results below suspect.")

    print("[2/3] sigma_max(rho,k) under N1 (physical), N2, N3 ...")
    ks = [2, 3, 5, 10, 50]
    rhos = np.round(np.concatenate([np.arange(0.02, 0.95, 0.02),
                                    [0.1, 0.43, 0.9, 0.95, 0.98]]), 4)
    rhos = np.unique(rhos)
    grid = {}
    for k in ks:
        row = {"rho": [], "N1": [], "N2_b3": [], "N2_feasible": [], "N3": []}
        for rho in rhos:
            row["rho"].append(float(rho))
            row["N1"].append(sigma_max_N1(rho, k))
            s2, feas = sigma_max_N2(rho, k, b=3.0)
            row["N2_b3"].append(s2); row["N2_feasible"].append(feas)
            row["N3"].append(sigma_max_N3(rho, k))
        grid[str(k)] = row
        # trend summary at the pole
        n1_hi = sigma_max_N1(0.98, k); n1_lo = sigma_max_N1(0.1, k)
        n3_hi = sigma_max_N3(0.98, k); n3_lo = sigma_max_N3(0.1, k)
        print(f"    k={k:3d}: N1 rho .1->.98 : {n1_lo:.3f} -> {n1_hi:.4f}  "
              f"({'COLLAPSE' if n1_hi<n1_lo else 'GROW'})   "
              f"N3 : {n3_lo:.3f} -> {n3_hi:.3f}  "
              f"({'COLLAPSE' if n3_hi<n3_lo else 'GROW'})")
    results["grid"] = grid
    results["ks"] = ks
    flush()

    # trend verdicts + collapse onset relative to 0.43
    print("[3/3] trend verdicts + supply=demand crossing ...")
    verdict = {}
    for k in ks:
        r = grid[str(k)]
        rho = np.array(r["rho"]); N1 = np.array(r["N1"]); N3 = np.array(r["N3"])
        # normalize N1 to its value at smallest rho
        i43 = int(np.argmin(np.abs(rho - 0.43)))
        i10 = int(np.argmin(np.abs(rho - 0.10)))
        verdict[str(k)] = dict(
            N1_trend="COLLAPSE" if N1[-1] < N1[0] else "GROW/FLAT",
            N3_trend="COLLAPSE" if N3[-1] < N3[0] else "GROW/FLAT",
            N1_ratio_043_over_010=float(N1[i43] / N1[i10]),
            N1_ratio_pole_over_010=float(N1[-1] / N1[i10]),
            N3_ratio_pole_over_010=float(N3[-1] / N3[i10]),
        )
    results["verdict"] = verdict

    # supply=demand crossing under N1 (physical): supply P(1-rho) vs demand a*rho.
    # crossing rho* = 1/(1+a/P). To land at 0.43 requires a/P = (1-0.43)/0.43.
    a_over_P_for_043 = (1 - RHO_C) / RHO_C
    results["crossing_N1"] = dict(
        supply="P*(1-rho)  [N1, k>=3 collapsed pair, exact]",
        demand="alpha(rho)=a*rho  (minimal increasing drift toward the pole)",
        crossing_formula="rho* = 1/(1 + a/P)",
        a_over_P_to_hit_0p43=float(a_over_P_for_043),
        note=("A crossing (upper edge) is GENERIC because supply falls and demand rises; "
              "the SPECIFIC location 0.43 requires tuning the one ratio a/P. "
              "Not parameter-free."))
    flush()
    print(f"    N1 supply=demand crossing at rho*=1/(1+a/P); "
          f"hitting 0.43 needs a/P={a_over_P_for_043:.3f} (TUNED).")
    print(f"\nwrote {OUT}")

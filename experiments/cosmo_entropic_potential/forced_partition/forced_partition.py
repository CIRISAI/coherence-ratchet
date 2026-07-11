#!/usr/bin/env python3
"""
Forced-partition computation — does shared-budget maintenance dynamics FORCE an
equilibrium partition of the entropic potential S across a SEEDED block structure?

DISCOVERY MODE. No pre-stated prediction. Exhaustive reporting: every
(alpha-form x allocation-rule x dimension-vector x budget-accounting x budget-level)
cell is integrated to steady state, classified, and its Jacobian eigenvalues
computed. Nothing is winner-picked; the full grid is written to results.json.

THE TRAP (papers/notes/entropic_matter_sector.md, referee paragraph): the block
structure d=(d_1,...,d_n) is SEEDED by construction. Additivity of S over blocks
is therefore not a discovery. Only what the DYNAMICS does with the seeded blocks
— the steady-state partition ratio and its stability — is legitimate to read off.

Per sector k: dρ_k/dt = α(ρ_k) − γ·m_k,  S_k = d_k·s(ρ_k),  s(ρ) = −ln(1−ρ)
  (the T-E3 density form; γ = 1, drift strength a = 1 WLOG).

Budget accounting (both reported):
  per-unit :  Σ_k d_k·m_k = M_total = b·D        (m_k is per-unit maintenance)
  total    :  Σ_k m_k     = M       = b·n        (m_k is per-sector maintenance)
with b the dimensionless budget level swept from starvation to saturation.

Allocation rules (weights w_k, normalized to the budget; all reported):
  A equal per-unit      w_k = 1
  B stock-proportional  w_k = S_k = d_k·s(ρ_k)
  C rate-proportional   w_k = |dS_k/dt|_drift = d_k·α(ρ_k)/(1−ρ_k)
  D need-proportional    w_k = α(ρ_k)              (maintenance follows drift pressure)

Alpha forms (all reported):
  lin      α = a·(1−ρ)          relaxation toward the rigidity pole
  logistic α = a·ρ·(1−ρ)
  const    α = a                pure drift, clipped at ρ=1
"""

import json
import os
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")

# ----- fixed constants -----
A_DRIFT = 1.0            # drift strength a
GAMMA = 1.0             # maintenance coefficient γ
EPS = 1e-9              # pole clip
RHO_LO, RHO_HI = 0.10, 0.43   # corridor bounds (overlay only; not used in dynamics)
SEED = 118
rng = np.random.default_rng(SEED)

DIM_VECTORS = {
    "bianconi_11333": [1, 1, 3, 3, 3],   # Bianconi degeneracy weighting
    "forms_146":      [1, 4, 6],         # 4D form multiplicities C(4,0),C(4,1),C(4,2)
    "symmetric_11111":[1, 1, 1, 1, 1],   # symmetric control
    "asym_29":        [2, 9],            # asymmetric control
}

ALPHA_FORMS = ("lin", "logistic", "const")
ALLOC_RULES = ("A_equal", "B_stock", "C_rate", "D_need")
ACCOUNTINGS = ("per_unit", "total")
BUDGET_LEVELS = np.round(np.linspace(0.02, 1.30, 25), 4)  # b: starvation → saturation


def alpha(rho, form):
    r = np.clip(rho, EPS, 1 - EPS)
    if form == "lin":
        return A_DRIFT * (1 - r)
    if form == "logistic":
        return A_DRIFT * r * (1 - r)
    if form == "const":
        return np.full_like(r, A_DRIFT)
    raise ValueError(form)


def s_density(rho):
    r = np.clip(rho, EPS, 1 - EPS)
    return -np.log(1 - r)


def weights(rho, d, form, rule):
    r = np.clip(rho, EPS, 1 - EPS)
    a = alpha(r, form)
    if rule == "A_equal":
        w = np.ones_like(r)
    elif rule == "B_stock":
        w = d * s_density(r)
    elif rule == "C_rate":
        w = d * a / (1 - r)          # |dS/dt| from free drift
    elif rule == "D_need":
        w = a.copy()
    else:
        raise ValueError(rule)
    return np.maximum(w, 1e-12)


def maintenance(rho, d, form, rule, accounting, b):
    w = weights(rho, d, form, rule)
    if accounting == "per_unit":
        M_total = b * d.sum()
        denom = np.sum(d * w)
        m = w * M_total / denom
    elif accounting == "total":
        M = b * len(d)
        denom = np.sum(w)
        m = w * M / denom
    else:
        raise ValueError(accounting)
    return m


def rhs(rho, d, form, rule, accounting, b):
    r = np.clip(rho, EPS, 1 - EPS)
    return alpha(r, form) - GAMMA * maintenance(r, d, form, rule, accounting, b)


def integrate_ss(d, form, rule, accounting, b, rho0):
    """Integrate to steady state; return (rho_star, converged, max_abs_drift).

    Terminal events absorb the two poles: as soon as any sector reaches the
    rigidity (ρ→1) or chaos (ρ→0) boundary the integration stops — that IS the
    steady state (a pole is absorbing) and it avoids LSODA grinding stiffly
    against the boundary."""
    def hit_rig(t, y):
        return np.max(y) - (1 - 1e-4)
    hit_rig.terminal = True
    hit_rig.direction = 1

    def hit_cha(t, y):
        return np.min(y) - 1e-4
    hit_cha.terminal = True
    hit_cha.direction = -1

    sol = solve_ivp(
        lambda t, y: rhs(y, d, form, rule, accounting, b),
        (0.0, 300.0), rho0, method="LSODA",
        rtol=1e-7, atol=1e-9, dense_output=False,
        events=(hit_rig, hit_cha),
    )
    rho_star = sol.y[:, -1]
    drift = rhs(rho_star, d, form, rule, accounting, b)
    hit_pole = any(len(te) > 0 for te in sol.t_events)
    # converged = drift vanished (interior fixed point); pole-absorption is a
    # steady state but not a zero-drift one, so it is not "converged".
    converged = bool((not hit_pole) and np.max(np.abs(drift)) < 1e-6)
    return rho_star, converged, float(np.max(np.abs(drift)))


def jacobian(rho, d, form, rule, accounting, b, h=1e-6):
    n = len(rho)
    J = np.zeros((n, n))
    f0 = rhs(rho, d, form, rule, accounting, b)
    for j in range(n):
        rp = rho.copy(); rp[j] += h
        fj = rhs(rp, d, form, rule, accounting, b)
        J[:, j] = (fj - f0) / h
    return J


def classify(rho_star, spread_tol=1e-2, pole_tol=1e-3):
    at_rig = bool(np.any(rho_star >= 1 - pole_tol))
    at_cha = bool(np.any(rho_star <= pole_tol))
    spread = float(np.max(rho_star) - np.min(rho_star))
    if at_rig and at_cha:
        label = "mixed_poles"
    elif at_rig:
        label = "runaway_rigidity"
    elif at_cha:
        label = "collapse_chaos"
    elif spread < spread_tol:
        label = "symmetric"
    else:
        label = "broken"
    return label, spread


def record_cell(dim_name, d, form, rule, accounting, b):
    d = np.array(d, dtype=float)
    n = len(d)
    D = float(d.sum())
    # canonical IC: mid-corridor uniform + tiny symmetry-breaking perturbation
    rho0 = np.clip(0.25 + rng.normal(0, 1e-3, n), EPS, 1 - EPS)
    rho_star, converged, maxdrift = integrate_ss(d, form, rule, accounting, b, rho0)
    rho_c = np.clip(rho_star, EPS, 1 - EPS)

    S_k = d * s_density(rho_c)
    S_tot = float(S_k.sum())
    part_frac = (S_k / S_tot).tolist() if S_tot > 0 else [float("nan")] * n
    dim_frac = (d / D).tolist()
    # L1 deviation of the S-partition from the dimension-partition
    part_dev_L1 = float(np.sum(np.abs(np.array(part_frac) - np.array(dim_frac)))) \
        if S_tot > 0 else float("nan")
    dim_proportional = bool(part_dev_L1 < 1e-3) if S_tot > 0 else False

    label, spread = classify(rho_c)

    # Jacobian at the integrated steady state
    J = jacobian(rho_c, d, form, rule, accounting, b)
    eig = np.linalg.eigvals(J)
    max_re = float(np.max(eig.real))
    stable_ss = bool(max_re < 1e-8)

    # dimension-symmetric candidate (all ρ equal): is it stationary? its Jacobian?
    # use the mean of rho_star as the symmetric anchor; test uniform config
    rho_sym_anchor = float(np.mean(rho_c))
    rho_sym = np.full(n, rho_sym_anchor)
    drift_sym = rhs(rho_sym, d, form, rule, accounting, b)
    sym_is_fixed = bool(np.max(np.abs(drift_sym)) < 1e-6)
    Jsym = jacobian(rho_sym, d, form, rule, accounting, b)
    max_re_sym = float(np.max(np.linalg.eigvals(Jsym).real))

    in_corridor = [(RHO_LO < float(r) < RHO_HI) for r in rho_c]

    return {
        "dim_name": dim_name, "dims": d.tolist(), "n": n, "D": D,
        "alpha": form, "rule": rule, "accounting": accounting, "budget_b": float(b),
        "rho_star": rho_c.tolist(),
        "converged": converged, "max_abs_drift": maxdrift,
        "S_k": S_k.tolist(), "S_total": S_tot,
        "partition_frac": part_frac, "dim_frac": dim_frac,
        "partition_dev_L1": part_dev_L1, "dimension_proportional": dim_proportional,
        "classification": label, "rho_spread": spread,
        "jac_max_real_eig": max_re, "stable": stable_ss,
        "sym_anchor_rho": rho_sym_anchor, "sym_is_fixed_point": sym_is_fixed,
        "sym_jac_max_real_eig": max_re_sym,
        "rho_in_corridor": in_corridor,
        "any_in_corridor": bool(any(in_corridor)),
        "all_in_corridor": bool(all(in_corridor)),
    }


def main():
    records = []
    meta = {
        "a_drift": A_DRIFT, "gamma": GAMMA, "seed": SEED,
        "dim_vectors": DIM_VECTORS, "alpha_forms": list(ALPHA_FORMS),
        "alloc_rules": list(ALLOC_RULES), "accountings": list(ACCOUNTINGS),
        "budget_levels": BUDGET_LEVELS.tolist(),
        "corridor": [RHO_LO, RHO_HI],
        "note": "s(rho)=-ln(1-rho); S_k=d_k*s(rho_k); dynamics drho/dt=alpha-gamma*m.",
    }

    total = (len(DIM_VECTORS) * len(ALPHA_FORMS) * len(ALLOC_RULES)
             * len(ACCOUNTINGS) * len(BUDGET_LEVELS))
    done = 0
    for dim_name, d in DIM_VECTORS.items():
        for form in ALPHA_FORMS:
            for rule in ALLOC_RULES:
                for acc in ACCOUNTINGS:
                    for b in BUDGET_LEVELS:
                        rec = record_cell(dim_name, d, form, rule, acc, float(b))
                        records.append(rec)
                        done += 1
                # incremental flush after each (dim, alpha, rule) block
                with open(RESULTS, "w") as f:
                    json.dump({"meta": meta, "records": records}, f, indent=1)
                print(f"[{done}/{total}] {dim_name} {form} {rule} flushed", flush=True)

    with open(RESULTS, "w") as f:
        json.dump({"meta": meta, "records": records}, f, indent=1)
    print(f"DONE {len(records)} records -> {RESULTS}", flush=True)


if __name__ == "__main__":
    main()

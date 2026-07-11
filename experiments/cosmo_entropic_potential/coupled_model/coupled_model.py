#!/usr/bin/env python3
"""
COUPLED cross-sector maintenance model — successor to forced_partition/.

The parent model's sectors were INDEPENDENT blocks (block-diagonal correlation
matrix; -ln det split additively; k_eff extensive in D). This model adds a GLOBAL
correlation channel rho_g between units in DIFFERENT sectors:

    C_ii = 1,  C_ij = rho_k (i,j same sector k),  C_ij = rho_g (different sectors).

State variables: (rho_1..rho_n, rho_g)  ->  n+1 maintained CHANNELS.

TWO-LEVEL SPECTRUM (closed form, validated against numpy.eigvalsh to 1e-10):
  * LOCAL  : (1 - rho_k) with multiplicity (d_k - 1) per sector.
  * REDUCED: the n eigenvalues of the n x n sector-mean matrix G,
      G_kk = 1 + (d_k-1) rho_k,   G_kl = sqrt(d_k d_l) rho_g   (k != l).
  -ln det C = -sum_k (d_k-1) ln(1-rho_k) - ln det G.
  k_eff = participation ratio (sum lambda)^2 / sum lambda^2 over the FULL set.
  Since trace C = D, sum lambda = D and sum lambda^2 = sum_k (d_k-1)(1-rho_k)^2
     + sum_k (1+(d_k-1)rho_k)^2 + rho_g^2 (D^2 - sum d_k^2)  [= tr G^2, closed form].

PSD DOMAIN: C is PSD iff every 1-rho_k >= 0 AND min eig(G) >= 0. Raising rho_g
drives the smallest G eigenvalue (a between-sector contrast) toward 0; that PSD
boundary is hit at rho_g < 1 (well before the rigidity pole). We track min eig(G)
and STOP integration on the PSD boundary; it is a first-class reported outcome.

DYNAMICS (a = gamma = 1):
   drho_k/dt = alpha(rho_k) - gamma m_k        (n sector channels)
   drho_g/dt = alpha(rho_g) - gamma m_g         (the global channel)
SHARED BUDGET across ALL n+1 channels, swept starvation -> over-maintenance.

DISCOVERY MODE: no pre-stated prediction; every (alpha x rule x accounting x
stock-split x dim-vector x budget) cell integrated to steady state / pole /
PSD-boundary, classified, Jacobian eigenvalues computed. Full grid -> results.json.
"""

import json
import os
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")

A_DRIFT = 1.0
GAMMA = 1.0
EPS = 1e-9
RHO_LO, RHO_HI = 0.10, 0.43
PSD_TOL = 1e-4          # min eig(G) event threshold
POLE_TOL = 1e-3
SEED = 118
rng = np.random.default_rng(SEED)

# dimension vectors: (2,5) replicated m times, plus two controls
DIM_VECTORS = {}
for m in (1, 2, 4, 8, 16, 32):
    DIM_VECTORS[f"pair25_x{m}"] = [2, 5] * m
DIM_VECTORS["quad_3333"] = [3, 3, 3, 3]
DIM_VECTORS["asym_29"] = [2, 9]

ALPHA_FORMS = ("lin", "logistic")
ALLOC_RULES = ("A_equal", "B_stock", "C_rate", "D_need")
ACCOUNTINGS = ("per_pair", "per_channel")
SPLITS = ("s1", "s2")                       # only B_stock / C_rate use the split
BUDGET_LEVELS = np.round(np.linspace(0.05, 1.45, 15), 4)


# ---------- primitives ----------
def alpha(rho, form):
    r = np.clip(rho, EPS, 1 - EPS)
    if form == "lin":
        return A_DRIFT * (1 - r)
    if form == "logistic":
        return A_DRIFT * r * (1 - r)
    raise ValueError(form)


def s_density(rho):
    r = np.clip(rho, EPS, 1 - EPS)
    return -np.log(1 - r)


def build_G(rho, rho_g, d):
    """n x n sector-mean matrix G."""
    n = len(d)
    sq = np.sqrt(np.outer(d, d))
    G = rho_g * sq
    diag = 1.0 + (d - 1.0) * rho
    np.fill_diagonal(G, diag)
    return G


def build_C(rho, rho_g, d):
    """Explicit D x D correlation matrix (validation only)."""
    D = int(d.sum())
    C = np.full((D, D), rho_g, dtype=float)
    idx = 0
    for k, dk in enumerate(d.astype(int)):
        C[idx:idx + dk, idx:idx + dk] = rho[k]
        idx += dk
    np.fill_diagonal(C, 1.0)
    return C


def keff_closed(rho, rho_g, d):
    D = d.sum()
    loc_sq = np.sum((d - 1.0) * (1.0 - rho) ** 2)
    Gdiag = 1.0 + (d - 1.0) * rho
    red_sq = np.sum(Gdiag ** 2) + rho_g ** 2 * (D ** 2 - np.sum(d ** 2))
    sumsq = loc_sq + red_sq
    return float(D ** 2 / sumsq)


def neg_logdet_closed(rho, rho_g, d):
    local = -np.sum((d - 1.0) * np.log(np.clip(1.0 - rho, EPS, None)))
    G = build_G(rho, rho_g, d)
    sign, logdet = np.linalg.slogdet(G)
    return float(local - logdet), float(sign), float(logdet)


def Gmin_eig(rho, rho_g, d):
    G = build_G(rho, rho_g, d)
    return float(np.linalg.eigvalsh(G)[0])


# ---------- allocation ----------
def channel_cost_units(d, accounting):
    """cost-unit c per channel: [sector_1..sector_n, global]."""
    n = len(d)
    D = d.sum()
    if accounting == "per_pair":
        P_sec = d * (d - 1.0) / 2.0
        P_g = (D ** 2 - np.sum(d ** 2)) / 2.0
        return np.concatenate([P_sec, [P_g]])
    if accounting == "per_channel":
        return np.ones(n + 1)
    raise ValueError(accounting)


def channel_weights(rho, rho_g, d, form, rule, split):
    """weight per channel [sector_1..n, global] for the allocation rule."""
    n = len(d)
    D = d.sum()
    r = np.clip(rho, EPS, 1 - EPS)
    rg = float(np.clip(rho_g, EPS, 1 - EPS))
    a_sec = alpha(r, form)
    a_g = alpha(rg, form)

    if rule == "A_equal":
        return np.ones(n + 1)
    if rule == "D_need":
        return np.maximum(np.concatenate([a_sec, [a_g]]), 1e-12)

    # B_stock / C_rate need a per-channel stock or rate, via the split
    P_sec = d * (d - 1.0) / 2.0
    P_g = (D ** 2 - np.sum(d ** 2)) / 2.0
    if split == "s1":                     # pairwise proxy
        stock_sec = P_sec * s_density(r)
        stock_g = P_g * s_density(rg)
        rate_sec = P_sec / (1.0 - r) * a_sec
        rate_g = P_g / (1.0 - rg) * a_g
    elif split == "s2":                   # log-det split
        stock_sec = (d - 1.0) * s_density(r)          # -(d_k-1)ln(1-rho_k)
        G = build_G(r, rg, d)
        sign, logdet = np.linalg.slogdet(G)
        stock_g = -logdet                             # -ln det G
        rate_sec = (d - 1.0) / (1.0 - r) * a_sec
        # d(-ln det G)/d rho_g = -tr(G^{-1} dG/drho_g); dG/drho_g = sqrt(d_k d_l) off-diag
        dG = np.sqrt(np.outer(d, d))
        np.fill_diagonal(dG, 0.0)
        try:
            rate_g = -np.trace(np.linalg.solve(G, dG)) * a_g
        except np.linalg.LinAlgError:
            rate_g = 0.0
    else:
        raise ValueError(split)

    if rule == "B_stock":
        w = np.concatenate([stock_sec, [stock_g]])
    else:  # C_rate
        w = np.concatenate([np.abs(rate_sec), [np.abs(rate_g)]])
    return np.maximum(w, 1e-12)


def channel_maintenance(rho, rho_g, d, form, rule, accounting, split, b):
    c = channel_cost_units(d, accounting)
    w = channel_weights(rho, rho_g, d, form, rule, split)
    B_tot = b * c.sum()
    denom = float(np.sum(c * w))
    m = w * B_tot / denom
    return m[:-1], float(m[-1])          # m_sectors, m_g


def rhs(y, d, form, rule, accounting, split, b):
    rho = np.clip(y[:-1], EPS, 1 - EPS)
    rho_g = float(np.clip(y[-1], EPS, 1 - EPS))
    m_sec, m_g = channel_maintenance(rho, rho_g, d, form, rule, accounting, split, b)
    dsec = alpha(rho, form) - GAMMA * m_sec
    dg = alpha(np.array([rho_g]), form)[0] - GAMMA * m_g
    return np.concatenate([dsec, [dg]])


# ---------- integrate one cell ----------
def integrate_ss(d, form, rule, accounting, split, b, y0):
    def hit_rig(t, y):
        return np.max(y) - (1 - 1e-4)
    hit_rig.terminal = True
    hit_rig.direction = 1

    def hit_cha(t, y):
        return np.min(y) - 1e-4
    hit_cha.terminal = True
    hit_cha.direction = -1

    def hit_psd(t, y):
        rho = np.clip(y[:-1], EPS, 1 - EPS)
        rho_g = float(np.clip(y[-1], EPS, 1 - EPS))
        return Gmin_eig(rho, rho_g, d) - PSD_TOL
    hit_psd.terminal = True
    hit_psd.direction = -1

    sol = solve_ivp(
        lambda t, y: rhs(y, d, form, rule, accounting, split, b),
        (0.0, 400.0), y0, method="LSODA",
        rtol=1e-7, atol=1e-9,
        events=(hit_rig, hit_cha, hit_psd),
    )
    y_star = sol.y[:, -1]
    drift = rhs(y_star, d, form, rule, accounting, split, b)
    hit = [len(te) > 0 for te in sol.t_events]
    which_pole = None
    if hit[0]:
        which_pole = "rigidity"
    elif hit[1]:
        which_pole = "chaos"
    elif hit[2]:
        which_pole = "psd_boundary"
    converged = bool((which_pole is None) and np.max(np.abs(drift)) < 1e-6)
    return y_star, converged, float(np.max(np.abs(drift))), which_pole


def jacobian(y, d, form, rule, accounting, split, b, h=1e-6):
    n1 = len(y)
    J = np.zeros((n1, n1))
    f0 = rhs(y, d, form, rule, accounting, split, b)
    for j in range(n1):
        yp = y.copy(); yp[j] += h
        J[:, j] = (rhs(yp, d, form, rule, accounting, split, b) - f0) / h
    return J


def classify(rho, rho_g, d, which_pole, spread_tol=1e-2):
    if which_pole is not None:
        return {"rigidity": "runaway_rigidity", "chaos": "collapse_chaos",
                "psd_boundary": "psd_boundary"}[which_pole], \
               float(np.max(rho) - np.min(rho))
    spread = float(np.max(rho) - np.min(rho))
    if spread < spread_tol:
        return "symmetric", spread
    return "broken", spread


def record_cell(dim_name, d, form, rule, accounting, split, b, validate=False):
    d = np.array(d, dtype=float)
    n = len(d)
    D = float(d.sum())
    y0 = np.clip(np.concatenate([0.25 + rng.normal(0, 1e-3, n), [0.20]]), EPS, 1 - EPS)
    y_star, converged, maxdrift, which_pole = integrate_ss(
        d, form, rule, accounting, split, b, y0)
    rho = np.clip(y_star[:-1], EPS, 1 - EPS)
    rho_g = float(np.clip(y_star[-1], EPS, 1 - EPS))

    keff = keff_closed(rho, rho_g, d)
    S_total, sign, logdetG = neg_logdet_closed(rho, rho_g, d)
    gmin = Gmin_eig(rho, rho_g, d)

    # per-channel stock (s2 log-det split, the physical potential decomposition)
    S_sec = (d - 1.0) * s_density(rho)         # local part
    label, spread = classify(rho, rho_g, d, which_pole)

    J = jacobian(y_star, d, form, rule, accounting, split, b)
    eig = np.linalg.eigvals(J)
    max_re = float(np.max(eig.real))
    stable = bool(max_re < 1e-8)

    valid = None
    if validate:
        C = build_C(rho, rho_g, d)
        ev = np.linalg.eigvalsh(C)
        keff_num = float((ev.sum() ** 2) / (ev ** 2).sum())
        sgn, ld = np.linalg.slogdet(C)
        valid = {
            "keff_closed": keff, "keff_numpy": keff_num,
            "keff_absdiff": abs(keff - keff_num),
            "neglogdet_closed": S_total, "neglogdet_numpy": float(-ld),
            "neglogdet_absdiff": abs(S_total - (-ld)),
            "min_eig_C": float(ev[0]),
        }

    in_corr = [(RHO_LO < float(x) < RHO_HI) for x in rho]
    return {
        "dim_name": dim_name, "dims": d.tolist(), "n": n, "D": D,
        "alpha": form, "rule": rule, "accounting": accounting,
        "split": (split if rule in ("B_stock", "C_rate") else "na"),
        "budget_b": float(b),
        "rho_sectors": rho.tolist(), "rho_g": rho_g,
        "converged": converged, "max_abs_drift": maxdrift,
        "which_pole": which_pole,
        "keff": keff, "S_total": S_total, "logdet_G": logdetG,
        "S_sectors_local": S_sec.tolist(),
        "min_eig_G": gmin,
        "classification": label, "rho_spread": spread,
        "jac_max_real_eig": max_re, "stable": stable,
        "rho_g_in_corridor": bool(RHO_LO < rho_g < RHO_HI),
        "rho_sectors_in_corridor": in_corr,
        "all_sectors_in_corridor": bool(all(in_corr)),
        "validation": valid,
    }


def main():
    records = []
    meta = {
        "a_drift": A_DRIFT, "gamma": GAMMA, "seed": SEED,
        "dim_vectors": DIM_VECTORS, "alpha_forms": list(ALPHA_FORMS),
        "alloc_rules": list(ALLOC_RULES), "accountings": list(ACCOUNTINGS),
        "splits": list(SPLITS), "budget_levels": BUDGET_LEVELS.tolist(),
        "corridor": [RHO_LO, RHO_HI], "psd_tol": PSD_TOL,
        "note": ("coupled two-level spectrum; channels = n sectors + 1 global; "
                 "k_eff = participation ratio of full set; PSD boundary tracked via "
                 "min eig(G); split only applies to B_stock/C_rate."),
    }

    # rule/split combos: A,D run once (split na); B,C run both splits
    combos = []
    for rule in ALLOC_RULES:
        if rule in ("A_equal", "D_need"):
            combos.append((rule, "s1"))     # split ignored; label 'na' in record
        else:
            for sp in SPLITS:
                combos.append((rule, sp))

    total = (len(DIM_VECTORS) * len(ALPHA_FORMS) * len(combos)
             * len(ACCOUNTINGS) * len(BUDGET_LEVELS))
    done = 0
    for dim_name, d in DIM_VECTORS.items():
        D = int(sum(d))
        do_val = D <= 60          # validate closed form on the smaller matrices
        for form in ALPHA_FORMS:
            for (rule, split) in combos:
                for acc in ACCOUNTINGS:
                    for b in BUDGET_LEVELS:
                        rec = record_cell(dim_name, d, form, rule, acc, split,
                                          float(b), validate=do_val)
                        records.append(rec)
                        done += 1
                with open(RESULTS, "w") as f:
                    json.dump({"meta": meta, "records": records}, f)
                print(f"[{done}/{total}] {dim_name} D={D} {form} {rule}/{split} flushed",
                      flush=True)

    with open(RESULTS, "w") as f:
        json.dump({"meta": meta, "records": records}, f)
    print(f"DONE {len(records)} records -> {RESULTS}", flush=True)


if __name__ == "__main__":
    main()

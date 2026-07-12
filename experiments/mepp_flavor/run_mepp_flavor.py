"""MEPP-flavor: does the FORCED entropy-production functional σ_max (N1) select the observed
flavor copula, and does σ-weighting forecast a distinct δ_CP distribution?

Registered in DECISIONS.md BEFORE this ran. The σ-functional and the |V|²→C map are both FROZEN
(imported / extracted verbatim), not invented here:
  - σ_max(C) = P·max_{i<j}(1/λ_i+1/λ_j)/(1/λ_i²+1/λ_j²)   [corridor_ceiling/sigma_max.py, N1]
  - C_copula(V) = the one-hot indicator correlation whose −ln det is functionals()['S_onehot']
Reuses the frozen 200k Haar U(3) machinery (seed 20260710, haar_u3) from run_mixing.py verbatim.

CPU only. Incremental flush. Nulls reported as nulls.
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MIXING = os.path.join(ROOT, "sm_escalator_mixing", "run_mixing.py")
CEIL = os.path.join(ROOT, "corridor_ceiling", "sigma_max.py")
RESULTS = os.path.join(HERE, "results.json")

# --- reuse frozen mixing machinery: exec the def-prefix (above the guard / run block) ---
_src = open(MIXING).read()
_prefix = _src.split("# Guard added", 1)[0]           # functionals, mixing_matrix, CASES, haar_u3
_rm = {"__name__": "mixing_defs", "__file__": MIXING}
exec(compile(_prefix, MIXING, "exec"), _rm)
functionals = _rm["functionals"]
mixing_matrix = _rm["mixing_matrix"]
haar_u3 = _rm["haar_u3"]
CASES = _rm["CASES"]
LN3 = _rm["LN3"]

# --- reuse frozen corridor-ceiling σ machinery for the PROVENANCE CHECK ---
_cs = open(CEIL).read()
_cprefix = _cs.split('if __name__ == "__main__":', 1)[0]
_cm = {"__name__": "ceil_defs", "__file__": CEIL}
exec(compile(_cprefix, CEIL, "exec"), _cm)
sigma_max_N1_frozen = _cm["sigma_max_N1"]             # frozen Kish-specialized N1
C_kish = _cm["C_kish"]

N_HAAR = 200_000
ENSEMBLE_SEED = 20260710                              # frozen — bit-identical to run_mixing.py
BOOT_SEED = 20260712
rng_haar = np.random.default_rng(ENSEMBLE_SEED)

res = {"registration": "DECISIONS.md (2026-07-12)", "n_haar": N_HAAR,
       "seed_ensemble": ENSEMBLE_SEED, "seed_bootstrap": BOOT_SEED,
       "sigma_formula": "sigma_max_N1(C)=max_{i<j}(1/li+1/lj)/(1/li^2+1/lj^2), P=1"}


def flush():
    tmp = RESULTS + ".tmp"
    json.dump(res, open(tmp, "w"), indent=1, default=float)
    os.replace(tmp, RESULTS)


# ---------------------------------------------------------------------------
# FORCED functional, general spectrum (generalizes sigma_max.py::sigma_max_N1)
# ---------------------------------------------------------------------------
def sigma_max_N1_general(C, P=1.0):
    lam = np.linalg.eigvalsh(C)
    lam = np.clip(lam, 1e-15, None)
    a = 1.0 / lam
    n = len(lam)
    best = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            eff = (a[i] + a[j]) / (a[i] ** 2 + a[j] ** 2)
            if eff > best:
                best = eff
    return P * best


# ---------------------------------------------------------------------------
# FROZEN map |V|^2 -> C: extraction of the one-hot correlation from functionals()
# (verbatim construction of functionals lines 40-53; verified == S_onehot below)
# ---------------------------------------------------------------------------
def copula_C(V):
    M = np.abs(V) ** 2
    P = M / 3.0
    px = M.sum(axis=1) / 3.0
    py = M.sum(axis=0) / 3.0
    k = 4
    cov = np.empty((k, k))
    for a in range(2):
        for b in range(2):
            cov[a, b] = (px[a] * (1 - px[a]) if a == b else -px[a] * px[b])
            cov[2 + a, 2 + b] = (py[a] * (1 - py[a]) if a == b else -py[a] * py[b])
            cov[a, 2 + b] = P[a, b] - px[a] * py[b]
            cov[2 + b, a] = cov[a, 2 + b]
    d = np.sqrt(np.diag(cov))
    Corr = cov / np.outer(d, d)
    return Corr


def sin_delta(f):
    """rephasing-invariant |sinδ| = |J| / J_max(angles)."""
    s12 = np.sqrt(max(f["sin2_12"], 0.0)); s23 = np.sqrt(max(f["sin2_23"], 0.0))
    s13 = np.sqrt(max(f["sin2_13"], 0.0))
    c12 = np.sqrt(max(1 - f["sin2_12"], 0.0)); c23 = np.sqrt(max(1 - f["sin2_23"], 0.0))
    c13 = np.sqrt(max(1 - f["sin2_13"], 0.0))
    jmax = c12 * s12 * c23 * s23 * c13 * c13 * s13
    return float(min(f["absJ"] / jmax, 1.0)) if jmax > 1e-300 else 0.0


# ---------------------------------------------------------------------------
# 0. PROVENANCE + FAITHFULNESS checks (abort if either fails)
# ---------------------------------------------------------------------------
def checks():
    # provenance: general σ_max reproduces the frozen Kish-specialized N1
    max_err = 0.0
    for k in [2, 3, 5, 10]:
        for rho in [0.05, 0.2, 0.43, 0.7, 0.9]:
            g = sigma_max_N1_general(C_kish(rho, k))
            fz = sigma_max_N1_frozen(rho, k)
            max_err = max(max_err, abs(g - fz) / max(abs(fz), 1e-12))
    prov_ok = bool(max_err < 1e-9)
    # faithfulness: -lndet C_copula == functionals()['S_onehot'] on observed cases
    fmax = 0.0
    for name in ["CKM_PDG2024", "PMNS_NuFit60_NO_loweroctant"]:
        p = CASES[name]
        V = mixing_matrix(p["s12"], p["s23"], p["s13"], p["delta"])
        C = copula_C(V)
        s, ld = np.linalg.slogdet(C)
        s_onehot_check = -ld
        fmax = max(fmax, abs(s_onehot_check - functionals(V)["S_onehot"]))
    faith_ok = bool(fmax < 1e-8)
    return dict(provenance_max_relerr=max_err, provenance_ok=prov_ok,
                faithfulness_max_abserr=fmax, faithfulness_ok=faith_ok)


# ---------------------------------------------------------------------------
# 1. observed copulas
# ---------------------------------------------------------------------------
def observed():
    out = {}
    for name in ["CKM_PDG2024", "PMNS_NuFit60_NO_loweroctant",
                 "PMNS_NuFit60_NO_upperoctant", "PMNS_deltaCPconserving"]:
        p = CASES[name]
        V = mixing_matrix(p["s12"], p["s23"], p["s13"], p["delta"])
        f = functionals(V)
        out[name] = dict(sigma=sigma_max_N1_general(copula_C(V)), MI=f["MI"],
                         absJ=f["absJ"], sinDelta=sin_delta(f),
                         S_onehot=f["S_onehot"])
    return out


# ---------------------------------------------------------------------------
# 2. Haar ensemble: sigma, MI, absJ, sinDelta, Jmax(angles)
# ---------------------------------------------------------------------------
def run_ensemble():
    keys = ["sigma", "MI", "absJ", "sinDelta", "Jmax_ang", "s2_12", "s2_23", "s2_13"]
    acc = {k: np.empty(N_HAAR) for k in keys}
    CH = 10_000
    done = 0
    t0 = time.time()
    while done < N_HAAR:
        n = min(CH, N_HAAR - done)
        U = haar_u3(n, rng_haar)
        for i in range(n):
            V = U[i]
            f = functionals(V)
            s12 = np.sqrt(max(f["sin2_12"], 0.0)); s23 = np.sqrt(max(f["sin2_23"], 0.0))
            s13 = np.sqrt(max(f["sin2_13"], 0.0))
            c12 = np.sqrt(max(1 - f["sin2_12"], 0.0)); c23 = np.sqrt(max(1 - f["sin2_23"], 0.0))
            c13 = np.sqrt(max(1 - f["sin2_13"], 0.0))
            jmax = c12 * s12 * c23 * s23 * c13 * c13 * s13
            j = done + i
            acc["sigma"][j] = sigma_max_N1_general(copula_C(V))
            acc["MI"][j] = f["MI"]
            acc["absJ"][j] = f["absJ"]
            acc["sinDelta"][j] = min(f["absJ"] / jmax, 1.0) if jmax > 1e-300 else 0.0
            acc["Jmax_ang"][j] = jmax
            acc["s2_12"][j] = f["sin2_12"]; acc["s2_23"][j] = f["sin2_23"]; acc["s2_13"][j] = f["sin2_13"]
        done += n
        res.setdefault("ensemble_progress", {})["done"] = f"{done}/{N_HAAR}"
        flush()
        print(f"[{time.time()-t0:.0f}s] haar {done}/{N_HAAR}", flush=True)
    return acc


# ---------------------------------------------------------------------------
# 3. stats
# ---------------------------------------------------------------------------
def pct(sample, x):
    return float(100.0 * np.mean(np.asarray(sample) < x))


def spearman(x, y):
    from scipy.stats import spearmanr
    r, p = spearmanr(x, y)
    return float(r), float(p)


def rank_partial_corr(x, y, controls):
    """Spearman partial correlation of x,y controlling for a list of control arrays."""
    from scipy.stats import rankdata
    def resid(v):
        Z = np.column_stack([rankdata(c) for c in controls])
        Z = np.column_stack([np.ones(len(v)), Z])
        beta, *_ = np.linalg.lstsq(Z, rankdata(v), rcond=None)
        return rankdata(v) - Z @ beta
    rx, ry = resid(x), resid(y)
    r = float(np.corrcoef(rx, ry)[0, 1])
    return r


def dist_summary(v):
    qs = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    return {"mean": float(np.mean(v)), "median": float(np.median(v)),
            "quantiles": {str(q): float(np.percentile(v, q)) for q in qs}}


def median_shift_ci(selected, full, rng, nboot=1000):
    """bootstrap 95% CI on median(selected) - median(full)."""
    obs = float(np.median(selected) - np.median(full))
    ds = np.empty(nboot)
    ns, nf = len(selected), len(full)
    for b in range(nboot):
        s = selected[rng.integers(0, ns, ns)]
        fdraw = full[rng.integers(0, nf, nf)]
        ds[b] = np.median(s) - np.median(fdraw)
    lo, hi = np.percentile(ds, [2.5, 97.5])
    return dict(shift=obs, ci95=[float(lo), float(hi)], excludes_zero=bool(lo > 0 or hi < 0))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from scipy.stats import ks_2samp

    print("[0] provenance + faithfulness checks ...", flush=True)
    res["checks"] = checks()
    flush()
    print("   ", res["checks"], flush=True)
    if not (res["checks"]["provenance_ok"] and res["checks"]["faithfulness_ok"]):
        print("ABORT: a frozen-object check failed.", flush=True)
        sys.exit(1)

    res["observed"] = observed()
    flush()
    print("[1] observed:", {k: round(v["sigma"], 4) for k, v in res["observed"].items()}, flush=True)

    print("[2] running 200k Haar ensemble (sigma + copula reads) ...", flush=True)
    acc = run_ensemble()

    sig = acc["sigma"]; MI = acc["MI"]; absJ = acc["absJ"]; sinD = acc["sinDelta"]
    Jmax = acc["Jmax_ang"]

    # ---- (A) concentration ----
    boot = np.random.default_rng(BOOT_SEED)
    sp_sig_MI, p_sig_MI = spearman(sig, MI)
    conc = {
        "sigma_haar": dist_summary(sig),
        "spearman_sigma_MI": sp_sig_MI, "spearman_sigma_MI_p": p_sig_MI,
        "spearman_sigma_absJ": spearman(sig, absJ),
        "spearman_sigma_Jmax_ang": spearman(sig, Jmax),
        "sigma_selects": ("anarchic/PMNS-like (neg MI corr)" if sp_sig_MI < 0
                          else "comonotone/CKM-like (pos MI corr)"),
        "observed_sigma_percentile": {k: pct(sig, v["sigma"])
                                      for k, v in res["observed"].items()},
        "E_MI_flat": float(np.mean(MI)),
        "E_MI_observed": {k: v["MI"] for k, v in res["observed"].items()},
    }
    for q in [10, 5, 1]:
        thr = np.percentile(sig, 100 - q)
        top = sig >= thr
        conc[f"top{q}pct_sigma"] = {
            "E_MI": float(np.mean(MI[top])), "E_absJ": float(np.mean(absJ[top])),
            "E_sinDelta": float(np.mean(sinD[top])), "median_MI": float(np.median(MI[top])),
        }
    res["A_concentration"] = conc
    flush()
    print("   Spearman(sigma,MI)=%.3f -> %s" % (sp_sig_MI, conc["sigma_selects"]), flush=True)

    # ---- (B)+(C) forward delta fork: top-q sigma selection + tilts ----
    fork = {"selectors": {}}
    for q in [5, 1, 10]:                                  # 5 primary
        thr = np.percentile(sig, 100 - q)
        sel = sig >= thr
        entry = {
            "n_selected": int(sel.sum()),
            "absJ": dist_summary(absJ[sel]), "sinDelta": dist_summary(sinD[sel]),
            "MI": dist_summary(MI[sel]),
            "vs_anarchy": {
                "KS_absJ_p": float(ks_2samp(absJ[sel], absJ).pvalue),
                "KS_sinDelta_p": float(ks_2samp(sinD[sel], sinD).pvalue),
                "median_shift_absJ": median_shift_ci(absJ[sel], absJ, boot),
                "median_shift_sinDelta": median_shift_ci(sinD[sel], sinD, boot),
            },
        }
        ks_j = entry["vs_anarchy"]["KS_absJ_p"]; ks_s = entry["vs_anarchy"]["KS_sinDelta_p"]
        shift_j = entry["vs_anarchy"]["median_shift_absJ"]["excludes_zero"]
        shift_s = entry["vs_anarchy"]["median_shift_sinDelta"]["excludes_zero"]
        entry["distinct_from_anarchy"] = bool((ks_j < 0.01 and shift_j) or (ks_s < 0.01 and shift_s))
        fork["selectors"][f"top{q}pct"] = entry
    # exponential tilt robustness
    z = (sig - sig.mean()) / sig.std()
    tilt = {}
    for beta in [1.0, 2.0, 5.0]:
        w = np.exp(beta * z); w /= w.sum()
        # weighted medians via resample
        idx = boot.choice(N_HAAR, size=200_000, p=w)
        tilt[f"beta{beta}"] = {"absJ_median": float(np.median(absJ[idx])),
                               "sinDelta_median": float(np.median(sinD[idx])),
                               "MI_median": float(np.median(MI[idx]))}
    # moment-matched beta* so E_w[sigma]=sigma(PMNS observed)
    target = res["observed"]["PMNS_NuFit60_NO_loweroctant"]["sigma"]
    betas = np.linspace(-5, 5, 2001)
    Ew = np.array([np.sum(np.exp(b * z) / np.sum(np.exp(b * z)) * sig) for b in betas])
    bstar = float(betas[np.argmin(np.abs(Ew - target))])
    wstar = np.exp(bstar * z); wstar /= wstar.sum()
    idxs = boot.choice(N_HAAR, size=200_000, p=wstar)
    tilt["beta_star_PMNS_matched"] = {"beta_star": bstar,
        "absJ_median": float(np.median(absJ[idxs])),
        "sinDelta_median": float(np.median(sinD[idxs])),
        "MI_median": float(np.median(MI[idxs]))}
    fork["tilt_robustness"] = tilt
    fork["flat_anarchy_reference"] = {"absJ_median": float(np.median(absJ)),
        "sinDelta_median": float(np.median(sinD)), "MI_median": float(np.median(MI))}

    # ---- minimization surrogate: bottom-q |J| region + CP-conserving pole ----
    thrJ = np.percentile(absJ, 5)
    minsel = absJ <= thrJ
    fork["minimization_surrogate"] = {
        "note": "bottom-5% |J| Haar region (surrogate for Thaler-Trifinopoulos CP-suppression); pole |sinDelta|->0",
        "absJ_median": float(np.median(absJ[minsel])),
        "sinDelta_median": float(np.median(sinD[minsel])),
    }
    # distinct-from-minimization at primary q=5: sigma-selected median |sinDelta| CI-separated ABOVE minimization
    sel5 = sig >= np.percentile(sig, 95)
    ms = median_shift_ci(sinD[sel5], sinD[minsel], boot)
    fork["distinct_from_minimization"] = {"median_sinDelta_shift_vs_min": ms,
        "distinct": bool(ms["excludes_zero"] and ms["shift"] > 0)}
    res["B_forward_fork"] = fork
    flush()

    # ---- (4) leptogenesis diagnostic: capacity vs usage channel ----
    controls = [acc["s2_12"], acc["s2_23"], acc["s2_13"]]
    usage_partial = rank_partial_corr(sig, sinD, controls)
    # CI on the partial corr via bootstrap
    pc = np.empty(400)
    for b in range(400):
        ii = boot.integers(0, N_HAAR, N_HAAR)
        pc[b] = rank_partial_corr(sig[ii], sinD[ii], [c[ii] for c in controls])
    lo, hi = np.percentile(pc, [2.5, 97.5])
    lepto = {
        "capacity_channel_spearman_sigma_Jmax_ang": spearman(sig, Jmax),
        "capacity_channel_spearman_sigma_MI": [sp_sig_MI, p_sig_MI],
        "usage_channel_partial_corr_sigma_sinDelta_given_angles": usage_partial,
        "usage_partial_ci95": [float(lo), float(hi)],
        "usage_channel_live": bool(lo > 0 or hi < 0),
    }
    lepto["verdict"] = ("usage live: observable delta stays coupled -> DUNE fork survives leptogenesis subtlety"
                        if lepto["usage_channel_live"] else
                        "usage decoupled: sigma acts through angles only -> under high-scale leptogenesis the observable-delta fork is WEAKENED (selected quantity is the angle structure, not low-energy delta)")
    res["C_leptogenesis"] = lepto
    flush()

    # ---- final verdict assembly ----
    prim = res["B_forward_fork"]["selectors"]["top5pct"]
    res["VERDICT"] = {
        "sigma_selects": conc["sigma_selects"],
        "distinct_from_anarchy_top5": prim["distinct_from_anarchy"],
        "distinct_from_minimization": res["B_forward_fork"]["distinct_from_minimization"]["distinct"],
        "leptogenesis_keeps_delta_observable": lepto["usage_channel_live"],
        "THICK_or_THIN": None,   # filled below
    }
    distinct = prim["distinct_from_anarchy"] and res["B_forward_fork"]["distinct_from_minimization"]["distinct"]
    res["VERDICT"]["THICK_or_THIN"] = ("THICKENING: distinct registered DUNE fork exists"
                                       if distinct else "THIN: no distinct fork under the registered locator")
    flush()
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(res["VERDICT"], indent=1), flush=True)

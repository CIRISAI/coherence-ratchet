"""CKM in the hierarchical (Froggatt-Nielsen) measure.

Companion to the Haar test one directory up. There, CKM was Haar-ATYPICAL (99.98th-pct MI).
Here we ask: is CKM TYPICAL of the FN measure -- the standard sketch of quark flavor? And the
control: is PMNS FN-atypical (so the two books differ by measure, not accident)?

Measure & coefficient distributions frozen in DECISIONS.md BEFORE this ran. Same six
functionals as ../run_mixing.py, imported directly. CPU only, fixed seeds, incremental flush.
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, "results.json")

# Reuse ../run_mixing.py's EXACT code paths (functionals, mixing_matrix, CASES) without
# triggering its module-level Haar run (it has no __main__ guard and would rewrite
# ../results.json). Exec only the prefix above its run block -- same machinery, no side effects
# and no reimplementation.
_src = open(os.path.join(PARENT, "run_mixing.py")).read()
_prefix = _src.split("\nres = {", 1)[0]      # everything above `res = {...}` (the run)
_rm = {"__name__": "run_mixing_defs", "__file__": os.path.join(PARENT, "run_mixing.py")}
exec(compile(_prefix, os.path.join(PARENT, "run_mixing.py"), "exec"), _rm)
functionals = _rm["functionals"]
mixing_matrix = _rm["mixing_matrix"]
CASES = _rm["CASES"]
LN3 = _rm["LN3"]

# ---- FN charge texture (arXiv:2306.08026 Table 1 top texture; verbatim, not tuned) ----
X_Q = np.array([3, 2, 0])
X_U = np.array([-4, -2, 0])
X_D = np.array([-3, -3, -3])
N_U = np.abs(X_Q[:, None] - X_U[None, :])   # exponent |X_Q_i - X_u_j|
N_D = np.abs(X_Q[:, None] - X_D[None, :])

J_MAX_GLOBAL = 1.0 / (6.0 * np.sqrt(3.0))   # 0.09623, Jarlskog global ceiling


def draw_c(n, rng, kind):
    """n complex 3x3 O(1) coefficient matrices under the pre-committed distributions."""
    if kind == "loguniform":                # PRIMARY: |c| log-uniform[1/3,3], phase uniform
        mag = np.exp(rng.uniform(np.log(1 / 3), np.log(3.0), size=(n, 3, 3)))
        phase = rng.uniform(0, 2 * np.pi, size=(n, 3, 3))
        return mag * np.exp(1j * phase)
    if kind == "gaussian":                   # ROBUSTNESS 1: complex Gaussian
        return rng.standard_normal((n, 3, 3)) + 1j * rng.standard_normal((n, 3, 3))
    if kind == "lognormal":                  # ROBUSTNESS 2: ln|c|~N(0,1) (the 2306.08026 prior)
        mag = np.exp(rng.standard_normal((n, 3, 3)))
        phase = rng.uniform(0, 2 * np.pi, size=(n, 3, 3))
        return mag * np.exp(1j * phase)
    raise ValueError(kind)


def ckm_from_fn(cu, cd, eps):
    """Batched: Yukawas -> left-singular-vector rotations -> V_CKM = U_uL^dagger U_dL."""
    Yu = cu * (eps ** N_U)[None, :, :]
    Yd = cd * (eps ** N_D)[None, :, :]
    UuL = np.linalg.svd(Yu)[0]               # left singular vectors, descending sv (mass-ordered)
    UdL = np.linalg.svd(Yd)[0]
    return np.conj(np.transpose(UuL, (0, 2, 1))) @ UdL


def sin_delta_eff(f):
    """|sinδ| = |J| / J_max(angles); J_max(angles)=c12 s12 c23 s23 c13^2 s13 (sakharov decomp)."""
    s12 = np.sqrt(max(f["sin2_12"], 0.0)); s23 = np.sqrt(max(f["sin2_23"], 0.0))
    s13 = np.sqrt(max(f["sin2_13"], 0.0))
    c12 = np.sqrt(max(1 - f["sin2_12"], 0.0)); c23 = np.sqrt(max(1 - f["sin2_23"], 0.0))
    c13 = np.sqrt(max(1 - f["sin2_13"], 0.0))
    jmax = c12 * s12 * c23 * s23 * c13 * c13 * s13
    return float(min(f["absJ"] / jmax, 1.0)) if jmax > 1e-300 else 0.0


KEYS = ["MI", "S_onehot", "PR_sv", "d_anarchy", "d_perm", "absJ", "sinDelta"]


def run_ensemble(kind, eps, n, seed, tag, res):
    rng = np.random.default_rng(seed)
    acc = {k: np.empty(n) for k in KEYS}
    CH = 5000
    done = 0
    t0 = time.time()
    while done < n:
        m = min(CH, n - done)
        cu = draw_c(m, rng, kind)
        cd = draw_c(m, rng, kind)
        V = ckm_from_fn(cu, cd, eps)
        for i in range(m):
            f = functionals(V[i])
            f["sinDelta"] = sin_delta_eff(f)
            for k in KEYS:
                acc[k][done + i] = f[k]
        done += m
        res["ensembles"].setdefault(tag, {})["progress"] = f"{done}/{n}"
        flush(res)
        print(f"[{time.time()-t0:.0f}s] {tag} {done}/{n}", flush=True)
    return acc


def summarize(acc):
    qs = [0.1, 0.5, 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99, 99.5, 99.9]
    return {k: {"mean": float(np.mean(v)), "median": float(np.median(v)),
                "quantiles": {str(q): float(np.percentile(v, q)) for q in qs}}
            for k, v in acc.items()}


def pct(sample, x):
    return float(100.0 * np.mean(np.asarray(sample) < x))


def flush(res):
    tmp = RESULTS + ".tmp"
    json.dump(res, open(tmp, "w"), indent=1)
    os.replace(tmp, RESULTS)


def main():
    # ---- observed matrices: reuse the SAME functionals on measured CKM / PMNS ----
    obs = {}
    for name in ["CKM_PDG2024", "PMNS_NuFit60_NO_loweroctant"]:
        p = CASES[name]
        V = mixing_matrix(p["s12"], p["s23"], p["s13"], p["delta"])
        f = functionals(V)
        f["sinDelta"] = sin_delta_eff(f)
        obs[name] = {k: f[k] for k in KEYS}
    res = {"charges": {"X_Q": X_Q.tolist(), "X_u": X_U.tolist(), "X_d": X_D.tolist()},
           "N_U": N_U.tolist(), "N_D": N_D.tolist(),
           "observed": obs, "ensembles": {}, "tests": {}}
    flush(res)

    # ---- PRIMARY ensemble: loguniform, eps=0.225, N=100k ----
    primary = run_ensemble("loguniform", 0.225, 100_000, 20260711, "primary_loguniform_eps0.225", res)
    res["ensembles"]["primary_loguniform_eps0.225"]["summary"] = summarize(primary)

    # test (a): marginal percentiles of observed CKM
    ckm = obs["CKM_PDG2024"]
    res["tests"]["a_marginal_CKM"] = {k: pct(primary[k], ckm[k]) for k in KEYS}
    res["tests"]["a_marginal_CKM"]["central90_all_six"] = bool(
        all(5.0 <= pct(primary[k], ckm[k]) <= 95.0
            for k in ["MI", "S_onehot", "PR_sv", "d_anarchy", "d_perm", "absJ"]))

    # test (b): joint -- |J| and |sinδ| percentile within the MI >= MI_obs subset
    hi = primary["MI"] >= ckm["MI"]
    nhi = int(hi.sum())
    joint = {"n_MI_ge_obs": nhi, "frac_MI_ge_obs": float(hi.mean())}
    if nhi >= 30:
        joint["absJ_pct_in_aligned_subset"] = pct(primary["absJ"][hi], ckm["absJ"])
        joint["sinDelta_pct_in_aligned_subset"] = pct(primary["sinDelta"][hi], ckm["sinDelta"])
        joint["pass_double_extremity_generic"] = bool(
            5.0 <= pct(primary["absJ"][hi], ckm["absJ"]) <= 95.0 and
            5.0 <= pct(primary["sinDelta"][hi], ckm["sinDelta"]) <= 95.0)
    res["tests"]["b_joint_CKM"] = joint
    # ensemble-level MI/absJ rank correlation (context for the joint read)
    from scipy.stats import spearmanr
    rho, _ = spearmanr(primary["MI"], primary["absJ"])
    res["tests"]["b_joint_CKM"]["spearman_MI_absJ_ensemble"] = float(rho)

    # test (c): control -- PMNS marginal percentiles in the SAME FN ensemble
    pmns = obs["PMNS_NuFit60_NO_loweroctant"]
    res["tests"]["c_control_PMNS"] = {k: pct(primary[k], pmns[k]) for k in KEYS}
    res["tests"]["c_control_PMNS"]["MI_below_central90"] = bool(pct(primary["MI"], pmns["MI"]) < 5.0)
    res["tests"]["c_control_PMNS"]["outside_central90_MI"] = bool(
        not (5.0 <= pct(primary["MI"], pmns["MI"]) <= 95.0))
    flush(res)

    # ---- test (d): sensitivity -- robustness distributions and eps drift, CKM marginal ----
    sens = {}
    variants = [("gaussian", 0.225, 20260712, "gaussian_eps0.225"),
                ("lognormal", 0.225, 20260713, "lognormal_eps0.225"),
                ("loguniform", 0.20, 20260714, "loguniform_eps0.20"),
                ("loguniform", 0.25, 20260715, "loguniform_eps0.25")]
    for kind, eps, seed, tag in variants:
        acc = run_ensemble(kind, eps, 50_000, seed, tag, res)
        res["ensembles"][tag]["summary"] = summarize(acc)
        sens[tag] = {"CKM_marginal": {k: pct(acc[k], ckm[k]) for k in KEYS},
                     "PMNS_MI_pct": pct(acc["MI"], pmns["MI"]),
                     "CKM_central90_all_six": bool(
                         all(5.0 <= pct(acc[k], ckm[k]) <= 95.0
                             for k in ["MI", "S_onehot", "PR_sv", "d_anarchy", "d_perm", "absJ"]))}
        flush(res)
    res["tests"]["d_sensitivity"] = sens
    flush(res)
    print("ALL DONE", flush=True)
    print(json.dumps({"a_CKM_MI_pct": res["tests"]["a_marginal_CKM"]["MI"],
                      "a_all_six_central90": res["tests"]["a_marginal_CKM"]["central90_all_six"],
                      "b_absJ_pct_aligned": res["tests"]["b_joint_CKM"].get("absJ_pct_in_aligned_subset"),
                      "c_PMNS_MI_pct": res["tests"]["c_control_PMNS"]["MI"]}, indent=1))


if __name__ == "__main__":
    main()

"""Rigor pass on the Rung-1 mixing hit (confirmation-mode: statistics, not re-adjudication).

The registered claim (../REGISTRATION.md) stands or falls ONLY by its pre-registered kill
conditions. This script computes referee-proofing statistics around that already-scored claim.

================  STATISTICS PRE-STATED BEFORE RUNNING  ================

Reproduction: regenerate the EXACT Haar ensemble of run_mixing.py (default_rng(20260710),
N_HAAR=200_000, 20k chunks, Mezzadri QR -- functions copied verbatim, NOT imported, because
run_mixing.py executes on import). Assert the regenerated marginal percentiles reproduce
results.json (seed/method identical), then compute the joint objects results.json did not.

STAT 1 -- JOINT TYPICALITY of the 6-vector (MI, S_onehot, PR_sv, d_anarchy, d_perm, absJ),
which are individually-typical for PMNS but correlated. Two depths, each percentiled against
the empirical Haar null (no Gaussian assumption):
  (a) Mahalanobis depth: D2 = (x-mu)^T Sigma^-1 (x-mu) on the empirical Haar mean/cov of the
      6-vector. Report the outlyingness percentile = frac of Haar with D2 < D2_test, AND the
      naive chi2_6 CDF at D2_test (the Gaussian-theory percentile); their gap = non-Gaussianity.
  (b) Rank-based depth -- normal-scores Mahalanobis: rank-transform each functional to its
      empirical uniform, apply inverse-normal (van der Waerden), Mahalanobis in that space
      (robust to marginal non-Gaussianity, keeps correlation). Cross-checked against spatial
      (L1) depth on an 8k subsample. Both percentiled vs the Haar null.
  Convention: outlyingness percentile ~50 = typical; >95 flagged; >99.9 = extreme pole.
  Expectation to CONFIRM: PMNS both octants jointly typical (bulk); CKM jointly extreme (~100).

STAT 2 -- theta13 LOOK-ELSEWHERE. sin^2 theta13 = 0.022 sits at the 4.4th Haar MARGINAL
percentile -- the one soft spot. Angles are NOT independent under Haar, so compute DIRECTLY
from the ensemble: P(at least one of the three angles <= its own 4.4th marginal percentile).
Lower-tail union is primary (the wrinkle is a LOW theta13 toward the aligned corner);
two-sided reported alongside. >~10% => dissolves as look-elsewhere; <~1-2% => flagged tension.

STAT 3 -- ERROR BANDS. MC over measurement uncertainty (fixed seed default_rng(77) , 3000
draws per case) with split-normal (asymmetric) draws:
  CKM  (PDG2024 std param): s12=0.22500+-0.00067, s23=0.04182(+0.00085,-0.00074),
       s13=0.00369+-0.00011, delta=1.144+-0.027 rad.
  PMNS lower octant (NuFit-6.0 with-SK / IC24): sin2_12=0.308(+0.012,-0.011),
       sin2_13=0.02215(+0.00056,-0.00058), sin2_23=0.470(+0.017,-0.013), delta=212(+26,-41) deg.
  PMNS upper octant (NuFit-6.0 without-SK / IC19): sin2_12=0.307(+0.012,-0.011),
       sin2_13=0.02195(+0.00054,-0.00058), sin2_23=0.561(+0.012,-0.015), delta=177(+19,-20) deg.
  NOTE/flag: the frozen registration used delta_PMNS=-1.98 rad (==246.6 deg), stale vs
  NuFit-6.0 212/177 deg. delta barely enters the magnitude functionals, so the MI-based claim
  is unaffected; it shifts absJ. MC is centered on CURRENT NuFit-6.0 best fits; the frozen
  point's percentiles are carried from results.json for reference.
  Propagate to: each functional's Haar percentile, the joint Mahalanobis outlyingness
  percentile, and the sin2_13 marginal percentile. Report [2.5, 50, 97.5] band of each.
  Registered-claim robustness: does PMNS MI stay in central 90% ([5,95]) across the full band,
  and CKM beyond 99.9?

CPU only. Seeded Haar sampling is the method (no synthetic *data*). Report everything adverse.
"""
import json, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
RESULTS_IN = os.path.join(PARENT, "results.json")
OUT = os.path.join(HERE, "rigor_results.json")
LN3 = np.log(3.0)
N_HAAR = 200_000

# ---- functions copied VERBATIM from run_mixing.py (identical definitions; do not import) ----
def mixing_matrix(s12, s23, s13, delta):
    c12, c23, c13 = np.sqrt(1 - s12**2), np.sqrt(1 - s23**2), np.sqrt(1 - s13**2)
    e = np.exp(-1j * delta)
    return np.array([
        [c12 * c13, s12 * c13, s13 * e],
        [-s12 * c23 - c12 * s23 * s13 / e, c12 * c23 - s12 * s23 * s13 / e, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 / e, -c12 * s23 - s12 * c23 * s13 / e, c23 * c13],
    ])


def functionals(V):
    M = np.abs(V) ** 2
    P = M / 3.0
    Psafe = np.clip(P, 1e-300, None)
    H_joint = -np.sum(P * np.log(Psafe))
    MI = 2 * LN3 - H_joint
    px = M.sum(axis=1) / 3.0
    py = M.sum(axis=0) / 3.0
    k = 4
    means = np.array([px[0], px[1], py[0], py[1]])
    cov = np.empty((k, k))
    for a in range(2):
        for b in range(2):
            cov[a, b] = (px[a] * (1 - px[a]) if a == b else -px[a] * px[b])
            cov[2 + a, 2 + b] = (py[a] * (1 - py[a]) if a == b else -py[a] * py[b])
            cov[a, 2 + b] = P[a, b] - px[a] * py[b]
            cov[2 + b, a] = cov[a, 2 + b]
    d = np.sqrt(np.diag(cov))
    Corr = cov / np.outer(d, d)
    sign, logdet = np.linalg.slogdet(Corr)
    S_onehot = -logdet if sign > 0 else np.nan
    s = np.linalg.svd(M, compute_uv=False) ** 2
    pr = s.sum() ** 2 / (s**2).sum()
    d_anarchy = np.linalg.norm(M - 1.0 / 3.0)
    perms = [np.eye(3)[list(p)] for p in
             [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]]
    d_perm = min(np.linalg.norm(M - Q) for Q in perms)
    J = float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))
    s13_ = np.abs(V[0, 2])
    s12_ = np.abs(V[0, 1]) / max(np.sqrt(1 - s13_**2), 1e-12)
    s23_ = np.abs(V[1, 2]) / max(np.sqrt(1 - s13_**2), 1e-12)
    return dict(MI=float(MI), MI_norm=float(MI / LN3), H_joint=float(H_joint),
                S_onehot=float(S_onehot), PR_sv=float(pr),
                d_anarchy=float(d_anarchy), d_perm=float(d_perm),
                J=J, absJ=abs(J),
                sin2_12=float(s12_**2), sin2_23=float(s23_**2), sin2_13=float(s13_**2))


def haar_u3(n, rng):
    Z = (rng.standard_normal((n, 3, 3)) + 1j * rng.standard_normal((n, 3, 3))) / np.sqrt(2)
    out = np.empty((n, 3, 3), dtype=complex)
    for i in range(n):
        Q, R = np.linalg.qr(Z[i])
        out[i] = Q * (np.diagonal(R) / np.abs(np.diagonal(R)))
    return out


def pct(sample, x):
    return float(100.0 * np.mean(np.asarray(sample) < x))


# ---- 6-vector for the joint-typicality test, + angles for look-elsewhere ----
VEC6 = ["MI", "S_onehot", "PR_sv", "d_anarchy", "d_perm", "absJ"]
ANG = ["sin2_12", "sin2_13", "sin2_23"]
ALLK = VEC6 + ANG

t0 = time.time()
rng = np.random.default_rng(20260710)          # SAME seed policy as run_mixing.py
store = {k: np.empty(N_HAAR) for k in ALLK}
CH = 20_000
done = 0
while done < N_HAAR:
    n = min(CH, N_HAAR - done)
    for i, V in enumerate(haar_u3(n, rng)):
        f = functionals(V)
        for k in ALLK:
            store[k][done + i] = f[k]
    done += n
    print(f"[{time.time()-t0:.0f}s] haar {done}/{N_HAAR}", flush=True)

# ---- reproduction cross-check vs results.json ----
ref = json.load(open(RESULTS_IN))
repro = {}
for k in ["MI", "S_onehot", "PR_sv", "d_anarchy", "d_perm", "absJ"]:
    mine_mean = float(np.mean(store[k]))
    ref_mean = ref["haar"][k]["mean"]
    mine_q99_9 = float(np.percentile(store[k], 99.9))
    ref_q99_9 = ref["haar"][k]["quantiles"]["99.9"]
    repro[k] = {"mean_mine": mine_mean, "mean_ref": ref_mean,
                "mean_absdiff": abs(mine_mean - ref_mean),
                "q99.9_mine": mine_q99_9, "q99.9_ref": ref_q99_9,
                "q99.9_absdiff": abs(mine_q99_9 - ref_q99_9)}
max_mean_diff = max(v["mean_absdiff"] for v in repro.values())
print(f"[{time.time()-t0:.0f}s] reproduction: max Haar-mean abs diff vs results.json = "
      f"{max_mean_diff:.2e}", flush=True)

# ============================  test points (frozen registration params)  ============================
CASES = {
    "CKM_PDG2024": dict(s12=0.22500, s23=0.04185, s13=0.00369, delta=1.144),
    "PMNS_NuFit60_NO_loweroctant": dict(s12=np.sqrt(0.308), s23=np.sqrt(0.470),
                                        s13=np.sqrt(0.0220), delta=-1.98),
    "PMNS_NuFit60_NO_upperoctant": dict(s12=np.sqrt(0.308), s23=np.sqrt(0.561),
                                        s13=np.sqrt(0.0220), delta=-1.98),
}
tp = {}
for name, p in CASES.items():
    V = mixing_matrix(p["s12"], p["s23"], p["s13"], p["delta"])
    tp[name] = functionals(V)

# ============================  STAT 1: joint typicality  ============================
X = np.column_stack([store[k] for k in VEC6])          # (N,6) Haar cloud
mu = X.mean(axis=0)
Sig = np.cov(X, rowvar=False)
Sinv = np.linalg.pinv(Sig)


def mahal2(row):
    d = row - mu
    return float(d @ Sinv @ d)


D2_haar = np.einsum("ij,jk,ik->i", X - mu, Sinv, X - mu)   # per-sample Mahalanobis^2

# normal-scores (rank) transform: empirical uniform -> inverse normal, per column
from numpy import argsort
def normal_scores(col):
    order = argsort(argsort(col))                 # ranks 0..N-1
    u = (order + 0.5) / len(col)
    return _ppf(u)

# vectorized inverse-normal (Acklam) to avoid scipy dependency
def _ppf(p):
    p = np.asarray(p, float)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    x = np.empty_like(p)
    lo = p < plow
    hi = p > phigh
    mid = ~(lo | hi)
    q = np.sqrt(-2 * np.log(p[lo]))
    x[lo] = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = np.sqrt(-2 * np.log(1 - p[hi]))
    x[hi] = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p[mid] - 0.5
    r = q * q
    x[mid] = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    return x

NS = np.column_stack([normal_scores(store[k]) for k in VEC6])
mu_ns = NS.mean(axis=0)
Sig_ns = np.cov(NS, rowvar=False)
Sinv_ns = np.linalg.pinv(Sig_ns)
D2ns_haar = np.einsum("ij,jk,ik->i", NS - mu_ns, Sinv_ns, NS - mu_ns)


def ns_point(row6):
    # map a raw 6-vector to normal scores using the Haar empirical CDF per column
    z = np.empty(6)
    for j, k in enumerate(VEC6):
        u = (np.mean(store[k] < row6[j]) * len(store[k]) + 0.5) / len(store[k])
        u = min(max(u, 0.5/len(store[k])), 1 - 0.5/len(store[k]))
        z[j] = _ppf(np.array([u]))[0]
    return z


from math import erf
def chi2_cdf_6(x):
    # chi-square CDF with k=6 dof: P(k/2, x/2); closed form for even k=6:
    # = 1 - exp(-x/2)*(1 + x/2 + (x/2)^2/2)
    if x <= 0:
        return 0.0
    h = x / 2.0
    return float(1 - np.exp(-h) * (1 + h + h*h/2))

# spatial (L1) depth on an 8k subsample (cross-check for the rank depth)
rng_sub = np.random.default_rng(101)
sub_idx = rng_sub.choice(N_HAAR, 8000, replace=False)
Rref = X[sub_idx]
# standardize by Haar std so no single functional dominates the L1 direction
scl = X.std(axis=0)
Rref_s = Rref / scl


def spatial_depth(row6_s, ref_s):
    diff = row6_s - ref_s                # (m,6)
    nrm = np.linalg.norm(diff, axis=1)
    nrm[nrm < 1e-12] = 1e-12
    u = (diff / nrm[:, None]).mean(axis=0)
    return 1.0 - np.linalg.norm(u)

null_sub = X[rng_sub.choice(N_HAAR, 6000, replace=False)] / scl
depth_null = np.array([spatial_depth(r, Rref_s) for r in null_sub])

stat1 = {"method": "outlyingness percentile = frac of Haar strictly less extreme; ~50 typical, "
                   ">99.9 extreme pole", "vec6": VEC6, "cases": {}}
for name in CASES:
    row6 = np.array([tp[name][k] for k in VEC6])
    d2 = mahal2(row6)
    zns = ns_point(row6)
    d2ns = float((zns - mu_ns) @ Sinv_ns @ (zns - mu_ns))
    row6_s = row6 / scl
    dsp = spatial_depth(row6_s, Rref_s)
    stat1["cases"][name] = {
        "mahalanobis_D2": d2,
        "mahalanobis_outlyingness_pct": pct(D2_haar, d2),
        "mahalanobis_chi2_6_cdf_pct": 100 * chi2_cdf_6(d2),
        "normalscores_mahalanobis_D2": d2ns,
        "normalscores_outlyingness_pct": pct(D2ns_haar, d2ns),
        "spatial_depth": float(dsp),
        "spatial_outlyingness_pct": float(100.0 * np.mean(depth_null > dsp)),
    }
print(f"[{time.time()-t0:.0f}s] STAT1 done", flush=True)

# ============================  STAT 2: theta13 look-elsewhere  ============================
# 4.4th marginal percentile threshold per angle (LOWER tail); union prob under Haar.
LEV = 4.4135   # the sin2_13 percentile reported in results.json
thr_lo = {k: np.percentile(store[k], LEV) for k in ANG}
thr_hi = {k: np.percentile(store[k], 100 - LEV) for k in ANG}
below = {k: store[k] <= thr_lo[k] for k in ANG}
outside = {k: (store[k] <= thr_lo[k]) | (store[k] >= thr_hi[k]) for k in ANG}
union_lo = np.zeros(N_HAAR, bool)
union_two = np.zeros(N_HAAR, bool)
for k in ANG:
    union_lo |= below[k]
    union_two |= outside[k]
# also: independence baseline for reference
p_indep_lo = 1 - (1 - LEV/100.0) ** 3
stat2 = {
    "level_pct": LEV,
    "per_angle_lower_threshold": {k: float(thr_lo[k]) for k in ANG},
    "P_at_least_one_angle_in_lower_4.4pct": float(np.mean(union_lo)),
    "P_at_least_one_angle_outside_central_pm4.4pct_twosided": float(np.mean(union_two)),
    "independence_baseline_lower_union": float(p_indep_lo),
    "observed_low_angle": "sin2_13 = 0.022 at 4.41th Haar marginal pct",
    "note": "angles back-out is NOT independent under Haar; union computed directly on ensemble",
}
print(f"[{time.time()-t0:.0f}s] STAT2: P(any angle<=4.4th)={stat2['P_at_least_one_angle_in_lower_4.4pct']:.4f}",
      flush=True)

# ============================  STAT 3: error bands  ============================
def split_normal(rng, n, c, sig_lo, sig_hi):
    z = rng.standard_normal(n)
    return c + np.where(z < 0, sig_lo, sig_hi) * z

MEAS = {
    "CKM_PDG2024": {"kind": "s", "delta_deg": False,
        "s12": (0.22500, 0.00067, 0.00067), "s23": (0.04182, 0.00074, 0.00085),
        "s13": (0.00369, 0.00011, 0.00011), "delta": (1.144, 0.027, 0.027)},
    "PMNS_NuFit60_NO_loweroctant": {"kind": "sin2", "delta_deg": True,
        "sin2_12": (0.308, 0.011, 0.012), "sin2_13": (0.02215, 0.00058, 0.00056),
        "sin2_23": (0.470, 0.013, 0.017), "delta": (212.0, 41.0, 26.0)},
    "PMNS_NuFit60_NO_upperoctant": {"kind": "sin2", "delta_deg": True,
        "sin2_12": (0.307, 0.011, 0.012), "sin2_13": (0.02195, 0.00058, 0.00054),
        "sin2_23": (0.561, 0.015, 0.012), "delta": (177.0, 20.0, 19.0)},
}
NMC = 3000
rmc = np.random.default_rng(77)
stat3 = {"n_mc": NMC, "band": "[2.5, 50, 97.5] percentiles across MC draws", "cases": {}}
for name, m in MEAS.items():
    d = m["delta"]
    delta = split_normal(rmc, NMC, *d)
    if m["delta_deg"]:
        delta = np.deg2rad(delta)
    if m["kind"] == "s":
        s12 = split_normal(rmc, NMC, *m["s12"]); s23 = split_normal(rmc, NMC, *m["s23"])
        s13 = split_normal(rmc, NMC, *m["s13"])
    else:
        s12 = np.sqrt(np.clip(split_normal(rmc, NMC, *m["sin2_12"]), 1e-9, 1-1e-9))
        s23 = np.sqrt(np.clip(split_normal(rmc, NMC, *m["sin2_23"]), 1e-9, 1-1e-9))
        s13 = np.sqrt(np.clip(split_normal(rmc, NMC, *m["sin2_13"]), 1e-9, 1-1e-9))
    fp = {k: np.empty(NMC) for k in VEC6}
    d2p = np.empty(NMC)
    s13pct = np.empty(NMC)
    for i in range(NMC):
        V = mixing_matrix(s12[i], s23[i], s13[i], delta[i])
        f = functionals(V)
        row6 = np.array([f[k] for k in VEC6])
        for k in VEC6:
            fp[k][i] = pct(store[k], f[k])
        d2p[i] = pct(D2_haar, mahal2(row6))
        s13pct[i] = pct(store["sin2_13"], f["sin2_13"])
    band = lambda a: [float(np.percentile(a, q)) for q in (2.5, 50, 97.5)]
    stat3["cases"][name] = {
        "haar_pct_band": {k: band(fp[k]) for k in VEC6},
        "joint_mahalanobis_outlyingness_pct_band": band(d2p),
        "sin2_13_marginal_pct_band": band(s13pct),
    }
    print(f"[{time.time()-t0:.0f}s] STAT3 {name}: MI band={band(fp['MI'])}", flush=True)

# ---- registered-claim robustness verdicts ----
def mi_band(name):
    return stat3["cases"][name]["haar_pct_band"]["MI"]
pmns_lo_b = mi_band("PMNS_NuFit60_NO_loweroctant")
pmns_up_b = mi_band("PMNS_NuFit60_NO_upperoctant")
ckm_b = mi_band("CKM_PDG2024")
verdict = {
    "PMNS_MI_stays_in_central_90_across_band":
        bool(5.0 <= pmns_lo_b[0] and pmns_lo_b[2] <= 95.0 and
             5.0 <= pmns_up_b[0] and pmns_up_b[2] <= 95.0),
    "CKM_MI_stays_beyond_99.9_across_band": bool(ckm_b[0] > 99.9),
    "PMNS_lower_MI_band": pmns_lo_b, "PMNS_upper_MI_band": pmns_up_b, "CKM_MI_band": ckm_b,
}

out = {
    "n_haar": N_HAAR, "seed": 20260710,
    "reproduction_check": {"max_haar_mean_absdiff_vs_results_json": max_mean_diff,
                           "per_functional": repro},
    "stat1_joint_typicality": stat1,
    "stat2_theta13_lookelsewhere": stat2,
    "stat3_error_bands": stat3,
    "registered_claim_robustness": verdict,
    "measurement_models": {"note": "PMNS centered on CURRENT NuFit-6.0 best fits (delta 212/177 deg); "
                           "frozen registration used delta=-1.98 rad (246.6 deg) -- see SUMMARY flag",
                           "NuFit6.0": "arXiv:2410.05380 Table 1", "CKM": "PDG2024 std param"},
}
json.dump(out, open(OUT, "w"), indent=1)
print(f"[{time.time()-t0:.0f}s] ALL DONE -> {OUT}")
print(json.dumps({"repro_max_meandiff": max_mean_diff,
                  "stat1": {k: {kk: round(vv, 3) for kk, vv in v.items() if kk.endswith('pct')}
                            for k, v in stat1["cases"].items()},
                  "stat2_union_lo": stat2["P_at_least_one_angle_in_lower_4.4pct"],
                  "verdict": verdict}, indent=1))

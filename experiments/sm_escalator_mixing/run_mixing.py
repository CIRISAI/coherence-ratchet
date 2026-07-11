"""Rung-1 mixing test: CKM and PMNS on the coordination ledger vs the Haar ensemble.

Registered claim (REGISTRATION.md): PMNS Haar-typical, CKM extreme-aligned.
Everything else: discovery mode -- compute everything, report everything.
Incremental flush to results.json.
"""
import json, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")
rng = np.random.default_rng(20260710)
N_HAAR = 200_000
LN3 = np.log(3.0)


# ---------- mixing-matrix construction (standard PDG parametrization) ----------
def mixing_matrix(s12, s23, s13, delta):
    c12, c23, c13 = np.sqrt(1 - s12**2), np.sqrt(1 - s23**2), np.sqrt(1 - s13**2)
    e = np.exp(-1j * delta)
    return np.array([
        [c12 * c13, s12 * c13, s13 * e],
        [-s12 * c23 - c12 * s23 * s13 / e, c12 * c23 - s12 * s23 * s13 / e, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 / e, -c12 * s23 - s12 * c23 * s13 / e, c23 * c13],
    ])


# ---------- functionals on a unitary V ----------
def functionals(V):
    M = np.abs(V) ** 2                      # doubly stochastic
    P = M / 3.0                             # joint dist, uniform marginals
    Psafe = np.clip(P, 1e-300, None)
    H_joint = -np.sum(P * np.log(Psafe))
    MI = 2 * LN3 - H_joint                  # uniform marginals: MI = 2ln3 - H
    # one-hot correlation log-det: indicators (X=1, X=2, Y=1, Y=2) under P
    px = M.sum(axis=1) / 3.0                # = 1/3 exactly
    py = M.sum(axis=0) / 3.0
    idx = [0, 1]
    k = 4
    C = np.eye(k)
    means = np.array([px[0], px[1], py[0], py[1]])
    var = means * (1 - means)
    # cov(1_{X=i},1_{X=j}) = -p_i p_j (i!=j); cov(1_{X=i},1_{Y=j}) = P(i,j)-p_i q_j
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
    # participation ratio of squared singular values of M
    s = np.linalg.svd(M, compute_uv=False) ** 2
    pr = s.sum() ** 2 / (s**2).sum()
    # pole coordinates
    d_anarchy = np.linalg.norm(M - 1.0 / 3.0)
    perms = [np.eye(3)[list(p)] for p in
             [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]]
    d_perm = min(np.linalg.norm(M - Q) for Q in perms)
    # Jarlskog
    J = float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))
    # angles back out (for Haar marginal placement)
    s13_ = np.abs(V[0, 2])
    s12_ = np.abs(V[0, 1]) / max(np.sqrt(1 - s13_**2), 1e-12)
    s23_ = np.abs(V[1, 2]) / max(np.sqrt(1 - s13_**2), 1e-12)
    return dict(MI=float(MI), MI_norm=float(MI / LN3), H_joint=float(H_joint),
                S_onehot=float(S_onehot), PR_sv=float(pr),
                d_anarchy=float(d_anarchy), d_perm=float(d_perm),
                J=J, absJ=abs(J),
                sin2_12=float(s12_**2), sin2_23=float(s23_**2), sin2_13=float(s13_**2))


def haar_u3(n, rng):
    """Mezzadri: QR of complex Ginibre with phase correction."""
    Z = (rng.standard_normal((n, 3, 3)) + 1j * rng.standard_normal((n, 3, 3))) / np.sqrt(2)
    out = np.empty((n, 3, 3), dtype=complex)
    for i in range(n):
        Q, R = np.linalg.qr(Z[i])
        out[i] = Q * (np.diagonal(R) / np.abs(np.diagonal(R)))
    return out


def pct(sample, x):
    return float(100.0 * np.mean(np.asarray(sample) < x))


# ---------- measured matrices ----------
CASES = {
    "CKM_PDG2024": dict(s12=0.22500, s23=0.04185, s13=0.00369, delta=1.144),
    "PMNS_NuFit60_NO_loweroctant": dict(s12=np.sqrt(0.308), s23=np.sqrt(0.470),
                                        s13=np.sqrt(0.0220), delta=-1.98),
    "PMNS_NuFit60_NO_upperoctant": dict(s12=np.sqrt(0.308), s23=np.sqrt(0.561),
                                        s13=np.sqrt(0.0220), delta=-1.98),
    "PMNS_deltaCPconserving": dict(s12=np.sqrt(0.308), s23=np.sqrt(0.470),
                                   s13=np.sqrt(0.0220), delta=np.pi),
}

# Guard added 2026-07-11 (ckm_ensemble housekeeping note): importing this frozen
# script must not silently re-run the 200k ensemble and rewrite results.json.
# Import the function-definition prefix instead (see ckm_ensemble/fn_ensemble.py).
if __name__ != "__main__":
    raise ImportError("run_mixing.py is a frozen script; import blocked to avoid re-running")

res = {"n_haar": N_HAAR, "cases": {}, "haar": {}}
t0 = time.time()
for name, p in CASES.items():
    V = mixing_matrix(p["s12"], p["s23"], p["s13"], p["delta"])
    u = V @ V.conj().T
    assert np.allclose(u, np.eye(3), atol=1e-12), name
    res["cases"][name] = functionals(V)
    res["cases"][name]["params"] = {k: float(v) for k, v in p.items()}

def flush():
    tmp = RESULTS + ".tmp"
    json.dump(res, open(tmp, "w"), indent=1)
    os.replace(tmp, RESULTS)

flush()
print(f"[{time.time()-t0:.0f}s] measured cases done", flush=True)

# ---------- Haar ensemble ----------
KEYS = ["MI", "MI_norm", "S_onehot", "PR_sv", "d_anarchy", "d_perm", "absJ",
        "sin2_12", "sin2_23", "sin2_13"]
acc = {k: np.empty(N_HAAR) for k in KEYS}
CH = 20_000
done = 0
while done < N_HAAR:
    n = min(CH, N_HAAR - done)
    for i, V in enumerate(haar_u3(n, rng)):
        f = functionals(V)
        for k in KEYS:
            acc[k][done + i] = f[k]
    done += n
    print(f"[{time.time()-t0:.0f}s] haar {done}/{N_HAAR}", flush=True)

qs = [0.1, 0.5, 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99, 99.5, 99.9]
res["haar"] = {k: {"mean": float(np.mean(v)),
                   "quantiles": {str(q): float(np.percentile(v, q)) for q in qs}}
               for k, v in acc.items()}

for name in CASES:
    c = res["cases"][name]
    c["haar_percentile"] = {k: pct(acc[k], c[k]) for k in KEYS}

# registered-claim evaluation on the primary functional (MI)
ck = res["cases"]["CKM_PDG2024"]["haar_percentile"]["MI"]
p1 = res["cases"]["PMNS_NuFit60_NO_loweroctant"]["haar_percentile"]["MI"]
p2 = res["cases"]["PMNS_NuFit60_NO_upperoctant"]["haar_percentile"]["MI"]
res["registered_claim"] = {
    "PMNS_haar_typical_central90": bool(5.0 <= p1 <= 95.0) and bool(5.0 <= p2 <= 95.0),
    "CKM_beyond_99.9": bool(ck > 99.9),
    "percentiles": {"CKM": ck, "PMNS_lower": p1, "PMNS_upper": p2},
}
flush()
print(f"[{time.time()-t0:.0f}s] ALL DONE")
print(json.dumps(res["registered_claim"], indent=1))
for name in CASES:
    c = res["cases"][name]
    print(f"{name}: MI={c['MI']:.4f} ({c['MI_norm']*100:.1f}% of ln3) "
          f"pct(MI)={c['haar_percentile']['MI']:.2f} absJ={c['absJ']:.2e} "
          f"pct(absJ)={c['haar_percentile']['absJ']:.2f}")

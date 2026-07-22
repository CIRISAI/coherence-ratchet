#!/usr/bin/env python3
"""Triadic-deception blind-spot quantifier (THREAD 2 / prenup K3, Prong B).

Constructs purely-triadic coordinations (parity/GHZ generalized) and measures the
gap between the true multi-information I_total and what the PAIRWISE Neff/S detector
reads. No empirical data: constructed distributions demonstrating a math fact (the
XOR/GHZ witness generalized), same status as the CMB null ensembles.

Method frozen in DECISIONS.md before any number was computed. Every information
estimate carries a shuffle null (bias control). Writes results.json incrementally.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results.json")
RESULTS = {"experiment": "triadic_channel / K3 blind-spot (Prong B)",
           "note": "constructed distributions (math fact), not empirical data; shuffle-null controlled"}

def flush():
    json.dump(RESULTS, open(OUT, "w"), indent=1)

# ---------- entropy / information primitives (bits) ----------
def H_bits(p):
    p = np.asarray(p, float).ravel()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())

def joint_entropy_bits(pmf):
    """pmf: array over full product state space (already normalized)."""
    return H_bits(pmf)

def marginal_pmf(pmf_nd, axis_keep):
    """Marginalize an n-d pmf tensor down to the axes in axis_keep (tuple)."""
    axes_drop = tuple(a for a in range(pmf_nd.ndim) if a not in axis_keep)
    return pmf_nd.sum(axis=axes_drop)

# ---------- pairwise detector (the object under test) ----------
def pearson_corr_from_pmf(pmf_nd, values):
    """Correlation matrix of the n coordinates under the joint pmf tensor.
    values: the value taken by coordinate along each axis index (here 0/1)."""
    n = pmf_nd.ndim
    vals = np.asarray(values, float)              # per-index values, shape (levels,)
    # E[X_i], E[X_i^2], E[X_i X_j]
    EX = np.zeros(n); EX2 = np.zeros(n)
    for i in range(n):
        m = marginal_pmf(pmf_nd, (i,))
        EX[i] = (m * vals).sum(); EX2[i] = (m * vals**2).sum()
    var = EX2 - EX**2
    C = np.eye(n)
    for i in range(n):
        for j in range(i+1, n):
            m = marginal_pmf(pmf_nd, (i, j))       # shape (levels, levels)
            EXY = (m * np.outer(vals, vals)).sum()
            cov = EXY - EX[i]*EX[j]
            denom = np.sqrt(var[i]*var[j])
            C[i, j] = C[j, i] = cov/denom if denom > 1e-15 else 0.0
    return C

def neff_pr(C):
    w = np.clip(np.linalg.eigvalsh(C), 0, None)
    s1, s2 = w.sum(), (w**2).sum()
    return float(s1*s1/s2) if s2 > 0 else float("nan")

def rho_bar(C):
    k = C.shape[0]
    return float((C.sum() - np.trace(C))/(k*(k-1)))

def keff_equicorr(C):
    k = C.shape[0]; rb = rho_bar(C); denom = 1 + rb*(k-1)
    return float(k/denom) if abs(denom) > 1e-12 else float("nan")

def S_over_2_nats(C):
    sign, logdet = np.linalg.slogdet(C)
    if sign <= 0: return float("nan")
    return float(-0.5*logdet)                       # S/2 = -1/2 ln det C, nats

# ---------- higher-order (synergy) detectors ----------
def o_information_bits(pmf_nd):
    """Rosas et al. 2019: Omega = (n-2)H(X) + sum_i [H(X_i) - H(X_{-i})].
    Omega<0 => synergy-dominated (parity/GHZ); Omega>0 => redundancy-dominated."""
    n = pmf_nd.ndim
    Hfull = joint_entropy_bits(pmf_nd)
    om = (n-2)*Hfull
    for i in range(n):
        Hi = H_bits(marginal_pmf(pmf_nd, (i,)))
        keep = tuple(a for a in range(n) if a != i)
        Hmi = H_bits(marginal_pmf(pmf_nd, keep))
        om += Hi - Hmi
    return float(om)

def total_correlation_bits(pmf_nd):
    n = pmf_nd.ndim
    return float(sum(H_bits(marginal_pmf(pmf_nd, (i,))) for i in range(n))
                 - joint_entropy_bits(pmf_nd))

# ============================================================
# SCENARIO 1 — discrete parity family (EXACT, no estimation)
# ============================================================
def parity_pmf(n):
    """Uniform over even-parity binary strings of length n. Returns n-d tensor."""
    shape = (2,)*n
    pmf = np.zeros(shape)
    for idx in np.ndindex(*shape):
        if sum(idx) % 2 == 0:
            pmf[idx] = 1.0
    pmf /= pmf.sum()
    return pmf

def apply_bitflip_noise(pmf_nd, eps):
    """Independent symmetric bit-flip channel with prob eps on each coordinate."""
    n = pmf_nd.ndim
    K = np.array([[1-eps, eps], [eps, 1-eps]])       # channel on one bit
    out = pmf_nd.copy()
    for ax in range(n):
        out = np.tensordot(K, out, axes=([1], [ax]))
        out = np.moveaxis(out, 0, ax)
    return out

def triple_and_pair_signs(pmf_nd):
    """<s_i s_j s_k> for the (unique, first) triple and all <s_i s_j>, s=2X-1."""
    n = pmf_nd.ndim
    signs = [np.array([-1.0, 1.0])]*n                # s = 2X-1 over index 0,1
    # pairwise
    pairs = {}
    for i in range(n):
        for j in range(i+1, n):
            m = marginal_pmf(pmf_nd, (i, j))
            pairs[f"{i}{j}"] = float((m * np.outer(signs[i], signs[j])).sum())
    # first triple (0,1,2)
    triple = None
    if n >= 3:
        m = marginal_pmf(pmf_nd, (0, 1, 2))
        s = np.einsum("i,j,k->ijk", signs[0], signs[1], signs[2])
        triple = float((m * s).sum())
    return triple, pairs

def scenario1():
    print("=== SCENARIO 1: discrete parity family (exact) ===")
    vals01 = [0.0, 1.0]
    out = {}
    for n in (3, 4, 5):
        rows = []
        for eps in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5):
            pmf = apply_bitflip_noise(parity_pmf(n), eps)
            C = pearson_corr_from_pmf(pmf, vals01)
            tc = total_correlation_bits(pmf)         # bits, EXACT
            s2_nats = S_over_2_nats(C)
            s2_bits = s2_nats/np.log(2) if np.isfinite(s2_nats) else float("nan")
            oi = o_information_bits(pmf)
            triple, pairs = triple_and_pair_signs(pmf)
            hidden_frac = (tc - max(s2_bits, 0.0))/tc if tc > 1e-12 else float("nan")
            rows.append(dict(
                eps=eps,
                I_total_bits=round(tc, 6),
                S_over_2_bits=round(s2_bits, 6) if np.isfinite(s2_bits) else None,
                hidden_fraction=round(hidden_frac, 6) if np.isfinite(hidden_frac) else None,
                neff_pr=round(neff_pr(C), 4),
                rho_bar=round(rho_bar(C), 6),
                keff_equicorr=round(keff_equicorr(C), 4),
                O_information_bits=round(oi, 6),
                max_abs_pairwise_sign=round(max(abs(v) for v in pairs.values()), 6),
                triple_sign=round(triple, 6) if triple is not None else None,
            ))
            print(f"  n={n} eps={eps:.2f}  I_tot={tc:.4f}b  S/2={s2_bits:.4f}b  "
                  f"Neff={neff_pr(C):.3f}  rho={rho_bar(C):+.4f}  "
                  f"O_info={oi:+.4f}b  <sss>={triple:+.4f}  maxpair={max(abs(v) for v in pairs.values()):.4f}")
        out[f"n{n}"] = rows
    RESULTS["scenario1_discrete_parity"] = out
    flush()

# ============================================================
# SCENARIO 2 — continuous sign-parity x amplitude (estimated + shuffle null)
# ============================================================
def sample_signparity(N, n, p, rng):
    """Even-parity signs with prob p, else independent signs; times half-normal amp."""
    free = rng.integers(0, 2, size=(N, n-1))*2 - 1            # +-1
    last = np.prod(free, axis=1, keepdims=True)               # forces even parity
    U_con = np.hstack([free, last])
    U_ind = rng.integers(0, 2, size=(N, n))*2 - 1
    use_con = rng.random(N) < p
    U = np.where(use_con[:, None], U_con, U_ind)
    A = np.abs(rng.standard_normal(size=(N, n)))              # half-normal amplitudes
    return U * A

def normal_score(col):
    r = np.argsort(np.argsort(col)) + 1.0
    from scipy.special import ndtri
    return ndtri(r/(len(col)+1.0))

def binned_TC_bits(X, b, rng):
    """Equal-frequency binned plug-in total correlation, bits."""
    N, n = X.shape
    codes = np.empty((N, n), int)
    for j in range(n):
        q = np.quantile(X[:, j], np.linspace(0, 1, b+1))
        q[0] = -np.inf; q[-1] = np.inf
        codes[:, j] = np.clip(np.digitize(X[:, j], q[1:-1]), 0, b-1)
    # joint
    flat = np.zeros((b,)*n)
    idx, cnt = np.unique(codes, axis=0, return_counts=True)
    for row, c in zip(idx, cnt):
        flat[tuple(row)] += c
    flat /= flat.sum()
    Hj = H_bits(flat)
    Hm = 0.0
    for j in range(n):
        m = np.bincount(codes[:, j], minlength=b).astype(float); m /= m.sum()
        Hm += H_bits(m)
    return Hm - Hj

def corr_and_readings(X):
    C = np.corrcoef(X, rowvar=False)
    return dict(neff_pr=round(neff_pr(C), 4), rho_bar=round(rho_bar(C), 6),
                S_over_2_nats=round(S_over_2_nats(C), 6),
                keff_equicorr=round(keff_equicorr(C), 4)), C

def scenario2(N=200_000, b=8, n_shuffle=200, seed=12345):
    print("=== SCENARIO 2: continuous sign-parity x amplitude (estimated) ===")
    rng = np.random.default_rng(seed)
    n = 3
    rows = []
    for p in (1.0, 0.9, 0.75, 0.6, 0.5):
        X = sample_signparity(N, n, p, rng)
        # linear pairwise readings
        lin, Clin = corr_and_readings(X)
        # copula (normal-scored) field
        G = np.column_stack([normal_score(X[:, j]) for j in range(n)])
        cop, Ccop = corr_and_readings(G)
        # copula 3-point and pairwise 3/2-point, z-scored vs shuffle null
        def triple(G_): return float(np.mean(G_[:, 0]*G_[:, 1]*G_[:, 2]))
        def pairs(G_): return [float(np.mean(G_[:, i]*G_[:, j]))
                               for i in range(n) for j in range(i+1, n)]
        t_obs = triple(G); p_obs = pairs(G)
        # binned TC + shuffle null (bias control)
        tc_obs = binned_TC_bits(X, b, rng)
        tc_null = []; t_null = []; p_null = []
        for _ in range(n_shuffle):
            Xs = np.column_stack([rng.permutation(X[:, j]) for j in range(n)])
            Gs = np.column_stack([rng.permutation(G[:, j]) for j in range(n)])
            tc_null.append(binned_TC_bits(Xs, b, rng))
            t_null.append(triple(Gs))
            p_null.append(pairs(Gs))
        tc_null = np.array(tc_null); t_null = np.array(t_null); p_null = np.array(p_null)
        def z(obs, null):
            s = null.std(ddof=1)
            return float((obs - null.mean())/s) if s > 0 else float("nan")
        tc_corr = tc_obs - tc_null.mean()
        z_tc = z(tc_obs, tc_null)
        z_triple = z(t_obs, t_null)
        z_pairs = [z(p_obs[k], p_null[:, k]) for k in range(len(p_obs))]
        hidden = (tc_corr - max(cop["S_over_2_nats"]/np.log(2), 0.0))/tc_corr if tc_corr > 1e-9 else float("nan")
        rows.append(dict(
            p_parity=p,
            I_total_binned_bits_corrected=round(tc_corr, 6),
            I_total_z_vs_shuffle=round(z_tc, 3),
            linear_S_over_2_nats=lin["S_over_2_nats"],
            copula_S_over_2_nats=cop["S_over_2_nats"],
            linear_neff_pr=lin["neff_pr"], linear_rho_bar=lin["rho_bar"],
            copula_neff_pr=cop["neff_pr"], copula_rho_bar=cop["rho_bar"],
            copula_triple_ggg=round(t_obs, 6),
            copula_triple_z=round(z_triple, 3),
            copula_pairwise_z_max=round(max(abs(v) for v in z_pairs), 3),
            hidden_fraction=round(hidden, 6) if np.isfinite(hidden) else None,
        ))
        print(f"  p={p:.2f}  I_tot(corr)={tc_corr:.4f}b (z={z_tc:.1f})  "
              f"linS/2={lin['S_over_2_nats']:.5f}  copS/2={cop['S_over_2_nats']:.5f}  "
              f"Neff_lin={lin['neff_pr']:.3f} Neff_cop={cop['neff_pr']:.3f}  "
              f"<ggg>={t_obs:+.4f}(z={z_triple:.1f})  maxpair_z={max(abs(v) for v in z_pairs):.2f}")
    RESULTS["scenario2_continuous_signparity"] = dict(
        N=N, bins=b, n_shuffle=n_shuffle, seed=seed, rows=rows)
    flush()

if __name__ == "__main__":
    scenario1()
    scenario2()
    print("wrote", OUT)

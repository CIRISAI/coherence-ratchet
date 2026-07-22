#!/usr/bin/env python3
r"""THREAD 1 — the dilution hole: GENUINELY-COUPLED cross-rung dynamics.

See DECISIONS.md (committed before this run). SCOPE TEST of an invariant's
R-scaling under a MODEL coupling. NOT the construction of the backward P_omega
operator. NOT synthetic empirical data — a dynamics model, as the original
k-body test used the R2 simulator.

THE QUESTION
------------
The original F-11 k-body null is a tautology of R2's per-rung-INDEPENDENT
dynamics. Here we build genuinely-coupled cross-rung dynamics (the rungs' Piece-2
management TARGETS are jointly determined) and MEASURE whether a multipartite
occupancy invariant exists that is (a) in a corridor and (b) NON-DILUTING as R
grows from 3 to 13 — or dilutes to the null floor like the independent case.

Estimators (TC, II, tau_k, joint entropy) are REUSED EXACTLY from
build_kbody_pomega.py (imported). Bias-controlled by a shuffled null exactly as
RESULTS.md / bias_control_kbody.py. Incremental per-record flush + resume.
"""

import json
import os
import sys
import time

import numpy as np

try:
    import cupy as cp
except Exception as e:  # pragma: no cover
    print(f"FATAL: cupy unavailable ({e}).", flush=True)
    sys.exit(1)

# reuse the EXACT estimators from the original k-body test
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(
    HERE, "..", "..", "open_system_pomega", "assumption_audit", "R2_history")))
import build_kbody_pomega as K   # noqa: E402  (joint_entropy_bits, total_correlation, interaction_information, kbody_tau)
import build_history_pomega as B  # noqa: E402  (framework dynamics constants)

# framework dynamics constants — imported UNCHANGED from R2
RHO_LOWER = B.RHO_LOWER      # 0.10
RHO_UPPER = B.RHO_UPPER      # 0.43
RHO_MID = B.RHO_MID          # 0.265
ALPHA0 = B.ALPHA0
ALPHA_RHO = B.ALPHA_RHO
GAMMA = B.GAMMA
KGAIN = B.KGAIN_MEAN         # fixed at the R2 mean gain (stable control)
M_BASE = B.M_BASE
M_NOISE_SD = B.M_NOISE_SD

TARGET_IN = RHO_MID          # desired-in-corridor target (settles occ=1, fidelity ~1)
TARGET_OUT = 0.50            # desired-out target (settles rho~0.56, occ=0, NOT a pole)
T_STEPS = 60                 # dynamics steps (settling confirmed by ~50)

TAU_LOWER, TAU_UPPER = 0.10, 0.43   # the only defined band (tau_k), from the framework
N_SHUF = 6                   # shuffled-null repetitions (bias control)


def log(m):
    print(m, flush=True)


# --------------------------------------------------------------------------
# the coupling: joint desired-occupancy bits d_n (N,R)
# --------------------------------------------------------------------------
def assign_bits(coupling, R, g, N, rng):
    """Desired occupancy bits d (N,R) int8. g in [0,1]: 0=independent, 1=full.
    parity/block: g = per-history mixture weight (constrained w.p. g else iid).
    vouching:     g = chain copy-probability (0=independent, 1=all-equal/rigidity).
    """
    d = (rng.random_sample((N, R)) < 0.5).astype(cp.int8)
    if coupling == "independent" or g <= 0.0:
        return d
    if coupling == "vouching":
        # chain: d_n = d_{n-1} w.p. g, else fresh Bernoulli(0.5)
        dc = d.copy()
        for n in range(1, R):
            copy = rng.random_sample(N) < g
            dc[:, n] = cp.where(copy, dc[:, n - 1], d[:, n])
        return dc
    use = (rng.random_sample(N) < g)                     # histories using the constraint
    dc = d.copy()
    if coupling == "global_parity":
        if R >= 2:
            dc[:, R - 1] = (dc[:, :R - 1].sum(axis=1) % 2).astype(cp.int8)
    elif coupling == "block_parity":
        nb = R // 3                               # disjoint consecutive 3-blocks
        for b in range(nb):
            i0 = 3 * b
            dc[:, i0 + 2] = (dc[:, i0] ^ dc[:, i0 + 1])
        # remainder rungs (3*nb .. R-1) left independent
    else:
        raise ValueError(coupling)
    return cp.where(use[:, None], dc, d)


def simulate(coupling, R, g, q, N, seed):
    """Coupled dynamics -> occupancy indicators occ (N,R) bool at t_f.

    q = management reliability: w.p. (1-q) a rung's realized desired bit is
    redrawn iid (a per-rung BSC that decoheres the injected coordination)."""
    rng = cp.random.RandomState(seed)
    d = assign_bits(coupling, R, g, N, rng)
    # management reliability: redraw failed rungs' desired bit independently
    if q < 1.0:
        fail = rng.random_sample((N, R)) >= q
        d = cp.where(fail, (rng.random_sample((N, R)) < 0.5).astype(cp.int8), d)
    tgt = cp.where(d == 1, TARGET_IN, TARGET_OUT).astype(cp.float64)
    rho = cp.full((N, R), 0.05, dtype=cp.float64)
    for _t in range(T_STEPS):
        a = ALPHA0 + ALPHA_RHO * rho
        noise = M_NOISE_SD * rng.standard_normal((N, R), dtype=cp.float64)
        M = M_BASE + KGAIN * (rho - tgt) + noise
        rho = cp.clip(rho + (a - GAMMA * M), 0.0, 1.0)
    occ = (rho > RHO_LOWER) & (rho < RHO_UPPER)
    return occ


# --------------------------------------------------------------------------
# pairwise rho + shuffled-null bias control
# --------------------------------------------------------------------------
def pairwise_rho(occ):
    X = occ.astype(cp.float64)
    C = cp.asnumpy(cp.corrcoef(X.T))
    Rn = C.shape[0]
    eye = np.eye(Rn, dtype=bool)
    off = np.abs(C[~eye])
    adj = np.abs(np.array([C[i, i + 1] for i in range(Rn - 1)]))
    return dict(mean_abs_all=float(np.nanmean(off)),
                mean_abs_adj=float(np.nanmean(adj)),
                max_abs=float(np.nanmax(off)))


def shuffle_occ(occ, rng):
    """Independently permute every rung's occupancy column: destroys ALL
    cross-rung structure, keeps every marginal exact (RESULTS.md null)."""
    N = occ.shape[0]
    occ_sh = occ.copy()
    for n in range(occ.shape[1]):
        occ_sh[:, n] = occ[rng.permutation(N), n]
    return occ_sh


def triple_ii_abs_mean(occ, R):
    if R < 3:
        return 0.0
    vals = [K.interaction_information(occ, (i, i + 1, i + 2))
            for i in range(R - 2)]
    return float(np.mean(np.abs(vals)))


def measure(occ, R, do_full_ii, seed):
    """All invariants + shuffled-null bias control. Returns a dict of measured,
    null-mean, null-scatter, and genuine (bias-subtracted) values."""
    Sfull = tuple(range(R))
    tc = K.total_correlation(occ, Sfull)
    tau = K.kbody_tau(occ, list(range(R)))
    ii = K.interaction_information(occ, list(range(R))) if do_full_ii else None
    tri = triple_ii_abs_mean(occ, R)

    # shuffled null
    rng = cp.random.RandomState(seed)
    tc_sh, tau_sh, ii_sh, tri_sh = [], [], [], []
    for _ in range(N_SHUF):
        occ_s = shuffle_occ(occ, rng)
        tc_sh.append(K.total_correlation(occ_s, Sfull))
        tau_sh.append(K.kbody_tau(occ_s, list(range(R))))
        if do_full_ii:
            ii_sh.append(K.interaction_information(occ_s, list(range(R))))
        tri_sh.append(triple_ii_abs_mean(occ_s, R))
        del occ_s
        cp.get_default_memory_pool().free_all_blocks()

    def gstat(meas, nulls):
        nm, ns = float(np.mean(nulls)), float(np.std(nulls))
        return dict(measured=float(meas), null_mean=nm, null_scatter=ns,
                    genuine=float(meas) - nm)

    out = {
        "TC": gstat(tc, tc_sh),
        "tau_k": gstat(tau, tau_sh),
        "tri_II_abs_mean": gstat(tri, tri_sh),
    }
    if do_full_ii:
        out["II_Rbody"] = gstat(ii, ii_sh)
    return out


# --------------------------------------------------------------------------
# records + driver
# --------------------------------------------------------------------------
def occ_marginals(occ):
    return [float(x) for x in cp.asnumpy(occ.mean(axis=0))]


def one_record(coupling, R, g, q, N, tag, full_ii=False):
    t0 = time.time()
    seed = 20260720 + R * 1000 + int(round(g * 100)) * 17 + int(round(q * 100)) * 7
    occ = simulate(coupling, R, g, q, N, seed)
    marg = occ_marginals(occ)
    rho = pairwise_rho(occ)
    # full R-body II (the SECONDARY diagnostic; 2^R subset sum) only where cheap
    # and decisive: the scaling run at R<=9 (the framework's rung count and
    # below — RESULTS.md's decisive point; II is noisy beyond). TC (the PRIMARY
    # observable) + tau_k + 3-body window II run at every R and every sweep.
    do_full_ii = bool(full_ii) and (R <= 9)
    inv = measure(occ, R, do_full_ii, seed + 555)
    del occ
    cp.get_default_memory_pool().free_all_blocks()
    rec = dict(tag=tag, coupling=coupling, R=R, g=g, q=q, N=N,
               occ_marginal_min=float(min(marg)),
               occ_marginal_max=float(max(marg)),
               occ_marginal_mean=float(np.mean(marg)),
               pairwise_rho=rho, invariants=inv,
               runtime_s=round(time.time() - t0, 1))
    return rec


def load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []


def save(path, recs):
    with open(path, "w") as f:
        json.dump(recs, f, indent=2)


def has(recs, coupling, R, g, q, tag):
    for r in recs:
        if (r["coupling"] == coupling and r["R"] == R and abs(r["g"] - g) < 1e-9
                and abs(r["q"] - q) < 1e-9 and r["tag"] == tag):
            return True
    return False


def main():
    couplings = ["independent", "global_parity", "block_parity", "vouching"]
    R_grid = [3, 5, 7, 9, 11, 13]
    N = 4_000_000

    log("=" * 72)
    log("THREAD 1 — coupled cross-rung dynamics — the dilution hole")
    log(f"  framework dyn: band ({RHO_LOWER},{RHO_UPPER}) centre {RHO_MID}; "
        f"KGAIN={KGAIN} M_NOISE={M_NOISE_SD} T={T_STEPS}")
    log(f"  N={N:,}  N_SHUF={N_SHUF}  couplings={couplings}")
    log(f"  GPU: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
    log("=" * 72)

    # ---- RUN 1: scaling (g=1, q=1) — the decisive run --------------------
    p1 = os.path.join(HERE, "results_scaling.json")
    recs = load(p1)
    log(f"[scaling] {len(recs)} records on disk")
    for coupling in couplings:
        for R in R_grid:
            if has(recs, coupling, R, 1.0, 1.0, "scaling"):
                continue
            rec = one_record(coupling, R, 1.0, 1.0, N, "scaling", full_ii=True)
            recs.append(rec)
            save(p1, recs)
            inv = rec["invariants"]
            log(f"  {coupling:14s} R={R:2d}  TC_gen={inv['TC']['genuine']:+.4f}"
                f" (meas {inv['TC']['measured']:.4f} null {inv['TC']['null_mean']:.4f}"
                f" sc {inv['TC']['null_scatter']:.4f})  tau_gen={inv['tau_k']['genuine']:+.4f}"
                f"  rho_all={rec['pairwise_rho']['mean_abs_all']:.4f}"
                f"  occ={rec['occ_marginal_mean']:.3f}  ({rec['runtime_s']}s)")

    # ---- RUN 2: reliability sweep (noise fragility) ----------------------
    p2 = os.path.join(HERE, "results_reliability.json")
    recs2 = load(p2)
    log(f"[reliability] {len(recs2)} records on disk")
    for coupling in ["global_parity", "block_parity"]:
        for q in [0.9, 0.7]:
            for R in R_grid:
                if has(recs2, coupling, R, 1.0, q, "reliability"):
                    continue
                rec = one_record(coupling, R, 1.0, q, N, "reliability")
                recs2.append(rec)
                save(p2, recs2)
                inv = rec["invariants"]
                log(f"  {coupling:14s} q={q} R={R:2d}  "
                    f"TC_gen={inv['TC']['genuine']:+.4f}  "
                    f"tau_gen={inv['tau_k']['genuine']:+.4f}  "
                    f"rho={rec['pairwise_rho']['mean_abs_all']:.4f}")

    # ---- RUN 3: strength sweep (interpolation) at R=9 --------------------
    p3 = os.path.join(HERE, "results_strength.json")
    recs3 = load(p3)
    log(f"[strength] {len(recs3)} records on disk")
    for coupling in couplings:
        for g in [0.0, 0.25, 0.5, 0.75, 1.0]:
            if has(recs3, coupling, 9, g, 1.0, "strength"):
                continue
            rec = one_record(coupling, 9, g, 1.0, N, "strength")
            recs3.append(rec)
            save(p3, recs3)
            inv = rec["invariants"]
            log(f"  {coupling:14s} g={g:.2f}  TC_gen={inv['TC']['genuine']:+.4f}"
                f"  tau_gen={inv['tau_k']['genuine']:+.4f}"
                f"  rho_all={rec['pairwise_rho']['mean_abs_all']:.4f}")

    log("=" * 72)
    log("DONE — analysis -> SUMMARY.md")
    log("=" * 72)


if __name__ == "__main__":
    main()

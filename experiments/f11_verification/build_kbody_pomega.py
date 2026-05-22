#!/usr/bin/env python3
# ruff: noqa: W605
r"""F-11 verification -- the candidate hole: an irreducibly multipartite (k-body)
cross-rung relation.

See PREREGISTRATION_kbody.md (committed before this run).

THE ATTACK
----------
The construction tree's exhaustiveness rests on the dichotomy "the cross-rung
relation is a scalar correlation C[n,m] OR a connection/map W_n." Both are
ARITY-2 (pairwise). A genuine third type: an irreducible k-body cross-rung
invariant that does NOT reduce to pairwise data -- the multipartite information
of the corridor-occupancy indicators across k rungs at once.

This builds P_omega's omega-weight from a genuine k-body invariant, two ways:
  (A) k = R   : one global R-body hyperedge (GHZ-type, maximally collective).
  (B) k fixed : ~R overlapping k-body hyperedges (W-type, k-local).

It is two-sided: H-kbody (non-empty AND joint-work AND not-rigidity to 9 rungs)
=> F-11 HAS A HOLE; any horn => F-11 holds against this attack.

THE k-BODY INVARIANT
--------------------
For a set S of rungs, let X_n in {0,1} be the corridor-occupancy indicator of
rung n at t_f (1 = rho_n in (0.10,0.43)). The joint distribution p(X_S) over the
trajectory ensemble has a genuine multipartite decomposition. The TOTAL
CORRELATION (multi-information) of S is

    TC(S) = sum_{n in S} H(X_n) - H(X_S)

and the IRREDUCIBLE k-body part -- the connected / interaction information that
is NOT in any (k-1)-body marginal -- is the |S|-th order interaction information

    II(S) = - sum_{T subseteq S} (-1)^{|S\T|} H(X_T)

(the inclusion-exclusion / Moebius transform of joint entropy). II(S) is exactly
the part of the joint corridor structure that no pairwise (or lower) object
captures -- the genuine k-body relation. It is a framework object: X_n is
Piece-3 corridor membership; "all rungs in corridor simultaneously" is the
omega-condition; II(S) is what "simultaneously" means beyond pairwise.

The k-body cross-rung observable that plays the role tau plays in the pairwise
constructions is a NORMALIZED multi-information,

    tau_k(S) = TC(S) / ((|S|-1) * Hmax)        in [0,1]

(TC of |S| binary vars is bounded by (|S|-1)*log2; tau_k=1 = all rungs perfectly
locked = rigidity pole; tau_k=0 = independent = chaos pole). The k-body corridor
asks tau_k(S) in (0.10,0.43) -- the framework's band.

THE omega-WEIGHT
----------------
Per the soft-P_omega form. The omega-weight of a history is graded:
  - within-rung: product_n soft(rho_n at t_f)         [Piece 3, unchanged]
  - k-body cross: the history's contribution to the k-body invariant being in
    its corridor. Operationally: the joint object is NON-EMPTY if there exist
    histories whose k-body invariant lands in band; it does JOINT WORK if the
    k-body invariant carries irreducible structure (II != 0, and a shuffle that
    destroys k-body structure changes the weight) and that does not vanish with
    R; it is NOT RIGIDITY if tau_k is not driven to 1.

DISCIPLINE
----------
CUDA throughout (cupy). Per-depth flush, verified resume. The invariant is the
genuine multi-information of the framework's own corridor indicators -- not
tuned. Verdict is whatever the construction returns.
"""

import json
import os
import sys
import time
import itertools

import numpy as np

try:
    import cupy as cp
except Exception as e:  # pragma: no cover
    print(f"FATAL: cupy unavailable ({e}). kbody_pomega requires CUDA.",
          flush=True)
    sys.exit(1)

# R2's sequential-emergence simulator, reused unchanged.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "open_system_pomega", "assumption_audit", "R2_history"))
import build_history_pomega as B  # noqa: E402

RHO_LOWER = B.RHO_LOWER          # 0.10
RHO_UPPER = B.RHO_UPPER          # 0.43
RHO_MID = B.RHO_MID              # 0.265
W_HALF = B.W_HALF                # 0.165
BETA_PIN = 1.0 / (2.0 * W_HALF ** 2)   # framework-referenced

TAU_LOWER, TAU_UPPER = 0.10, 0.43      # k-body cross-rung corridor band
TAU_MID = 0.5 * (TAU_LOWER + TAU_UPPER)

DEPTHS = [3, 4, 5, 6, 7, 8, 9, 11, 13, 20]
N_HIST = 4_000_000
HIST_BATCH = 400_000                   # sim batch -- avoids the (n_hist,R,T) OOM
K_FIXED = [3, 4]                       # case (B) sliding-hyperedge sizes
RESULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "results_kbody.json")
LOG2 = float(np.log(2.0))


def log(msg):
    print(msg, flush=True)


# --------------------------------------------------------------------------
# entropy of a subset of binary occupancy indicators, from the ensemble
# --------------------------------------------------------------------------
def joint_entropy_bits(occ_subset):
    """occ_subset: (n_hist, s) bool/int array of occupancy for s rungs.
    Returns H(X_S) in bits, estimated from the ensemble's empirical joint
    distribution over the 2^s patterns."""
    s = occ_subset.shape[1]
    # encode each history's pattern as an integer 0..2^s-1
    weights = (1 << cp.arange(s, dtype=cp.int64))
    codes = (occ_subset.astype(cp.int64) * weights[None, :]).sum(axis=1)
    counts = cp.bincount(codes, minlength=(1 << s)).astype(cp.float64)
    tot = counts.sum()
    p = counts / tot
    nz = p > 0
    H = -(p[nz] * cp.log(p[nz])).sum() / LOG2
    return float(H)


def total_correlation(occ, S):
    """TC(S) = sum_n H(X_n) - H(X_S), in bits. occ: (n_hist,R)."""
    HS = joint_entropy_bits(occ[:, list(S)])
    Hmarg = 0.0
    for n in S:
        Hmarg += joint_entropy_bits(occ[:, [n]])
    return Hmarg - HS


def interaction_information(occ, S):
    """II(S) = - sum_{T subseteq S} (-1)^{|S\\T|} H(X_T)  -- the IRREDUCIBLE
    |S|-body interaction information (Moebius transform of joint entropy).
    This is the part of the joint corridor structure no lower-arity object
    carries. For |S| up to ~12 the 2^|S| subset sum is tractable on GPU."""
    S = list(S)
    s = len(S)
    # cache subset entropies by their bitmask over S
    total = 0.0
    for mask in range(1 << s):
        T = [S[i] for i in range(s) if (mask >> i) & 1]
        if not T:
            HT = 0.0
        else:
            HT = joint_entropy_bits(occ[:, T])
        sign = (-1) ** (s - bin(mask).count("1"))
        total += sign * HT
    return -total


def kbody_tau(occ, S):
    """Normalized multi-information of subset S: tau_k in [0,1].
    tau_k = TC(S) / ((|S|-1) * 1bit).  1 = locked (rigidity), 0 = independent."""
    s = len(S)
    if s < 2:
        return 0.0
    tc = total_correlation(occ, S)
    return tc / ((s - 1) * 1.0)   # each binary var carries <=1 bit


# --------------------------------------------------------------------------
# the construction, per depth
# --------------------------------------------------------------------------
def run_depth(R, k_fixed_list):
    """Build the k-body P_omega objects for an R-rung tower. Returns a dict.

    The simulation is BATCHED -- the R2 simulator's (n_hist,R,T) rho array is
    20+ GB at R>=6; we run HIST_BATCH histories at a time, keep only the
    all-emerged sub-ensemble's rho-at-t_f, and pool. Incremental, OOM-safe."""
    t0 = time.time()
    rho_e_batches = []
    n_total = 0
    n_done = 0
    base_seed = 20260522 + R * 1000
    # the R2 simulator's rho array is (nb, R, T_total) fp64; T_total grows with
    # R, so shrink the batch to keep each allocation well under ~8 GB.
    Tt, _ = B.make_time_grid(R)
    bytes_per_hist = R * Tt * 8
    nb_cap = max(20_000, int(6e9 / bytes_per_hist))
    while n_done < N_HIST:
        nb = min(HIST_BATCH, nb_cap, N_HIST - n_done)
        sim = B.simulate_histories(R, nb, batch_seed=base_seed + n_done)
        T_total = sim["T_total"]
        rho_tf = sim["rho"][:, :, T_total - 1]          # (nb,R)
        n_emerged = sim["n_emerged"]
        all_emerged = (n_emerged == R)
        rho_e_batches.append(rho_tf[all_emerged].copy())
        n_total += int(all_emerged.sum())
        n_done += nb
        del sim, rho_tf, n_emerged, all_emerged
        cp.get_default_memory_pool().free_all_blocks()
    n_all = n_total
    if n_all < 5000:
        log(f"  R={R}: only {n_all} all-emerged histories -- too few; skip")
        return None
    rho_e = cp.concatenate(rho_e_batches, axis=0)        # (n_all,R)
    del rho_e_batches

    # corridor-occupancy indicator X_n at t_f  (Piece 3)
    occ = (rho_e > RHO_LOWER) & (rho_e < RHO_UPPER)   # (n_all,R) bool
    # diagnostic: marginal occupancy probabilities (is the ensemble degenerate?)
    occ_marg = occ.mean(axis=0)                        # (R,)

    # within-rung soft weight (unchanged)
    soft = cp.exp(-BETA_PIN * (rho_e - RHO_MID) ** 2)  # (n_all,R)
    w_within = cp.prod(soft, axis=1)                   # (n_all,)

    out = {"R": R, "n_all_emerged": n_all,
           "occ_marginal": [float(x) for x in occ_marg.get()]}

    # ---- diagnostic: pairwise baseline -----------------------------------
    # the genuine ARITY-2 object: mean pairwise total correlation TC over
    # adjacent rung pairs. If the k-body II is zero AND the pairwise TC is
    # also zero, the ensemble is simply near-independent (chaos pole). If
    # pairwise TC is non-zero but k-body II is zero, the k-body arity adds
    # nothing -- the genuine multi-information lives entirely in the
    # pairwise marginals. Either way the k-body attack fails; this
    # diagnostic distinguishes which.
    pair_tc = []
    for n in range(R - 1):
        pair_tc.append(total_correlation(occ, (n, n + 1)))
    out["pairwise_TC_adjacent_mean"] = float(np.mean(pair_tc))

    # ---- CASE (A): k = R, one global R-body hyperedge --------------------
    # the GHZ-type maximally-collective object.
    tauA = kbody_tau(occ, list(range(R)))
    # interaction information II of the full set -- only for R<=12 (2^R sum)
    if R <= 12:
        iiA = interaction_information(occ, list(range(R)))
    else:
        iiA = None
    out["caseA"] = {
        "tau_R": tauA,
        "tau_in_band": bool(TAU_LOWER < tauA < TAU_UPPER),
        "II_R_body": iiA,
    }

    # ---- CASE (B): fixed k, ~R sliding hyperedges ------------------------
    out["caseB"] = {}
    for k in k_fixed_list:
        if k > R:
            continue
        windows = [tuple(range(i, i + k)) for i in range(R - k + 1)]
        taus = [kbody_tau(occ, w) for w in windows]
        iis = [interaction_information(occ, w) for w in windows]
        taus = np.array(taus)
        iis = np.array(iis)
        n_in_band = int(((taus > TAU_LOWER) & (taus < TAU_UPPER)).sum())

        # ---- the joint object's omega-weight and the joint-work test -----
        # per-history k-body weight: the history is k-body-corridor-compatible
        # if the windows it participates in are in band. We score the JOINT
        # object selectivity and joint work the same way the pairwise runs did.
        #
        # joint work test (the decisive one): does the k-body invariant carry
        # irreducible structure that survives a SHUFFLE destroying k-body
        # correlation while keeping all (k-1)-body marginals?
        #
        # We compute, per window, the SHUFFLE GAP = II(S) measured on the true
        # ensemble minus II(S) on an ensemble where the k-th rung's occupancy
        # is independently permuted (destroys genuine k-body info, preserves
        # lower marginals approximately). A pairwise object has II == 0 by
        # definition; a genuine k-body object has II != 0 and shuffle_gap != 0.
        shuffle_gaps = []
        rng = cp.random.RandomState(777 + R * 100 + k)
        for w in windows:
            S = list(w)
            ii_true = interaction_information(occ, S)
            # shuffle: independently permute the LAST rung's occupancy column
            occ_sh = occ.copy()
            perm = rng.permutation(n_all)
            occ_sh[:, S[-1]] = occ[perm, S[-1]]
            ii_sh = interaction_information(occ_sh, S)
            shuffle_gaps.append(abs(ii_true - ii_sh))
        shuffle_gaps = np.array(shuffle_gaps)

        out["caseB"][f"k{k}"] = {
            "n_windows": len(windows),
            "tau_mean": float(taus.mean()),
            "tau_min": float(taus.min()),
            "tau_max": float(taus.max()),
            "n_in_band": n_in_band,
            "II_mean": float(iis.mean()),
            "II_abs_mean": float(np.abs(iis).mean()),
            "II_total_over_windows": float(iis.sum()),
            "shuffle_gap_mean": float(shuffle_gaps.mean()),
            "shuffle_gap_per_window": float(shuffle_gaps.mean()),
        }

    out["runtime_s"] = round(time.time() - t0, 1)
    return out


def main():
    log("=" * 70)
    log("F-11 verification -- k-body cross-rung relation -- the candidate hole")
    log(f"  beta_pin = {BETA_PIN:.3f}  (framework-referenced, 1/2w^2)")
    log(f"  corridor band ({RHO_LOWER},{RHO_UPPER}); k-body tau band "
        f"({TAU_LOWER},{TAU_UPPER})")
    log(f"  N_HIST = {N_HIST:,}  depths {DEPTHS}  fixed-k {K_FIXED}")
    log("=" * 70)

    results = {}
    if os.path.exists(RESULT_PATH):
        with open(RESULT_PATH) as f:
            results = json.load(f)
        log(f"  resuming: {len(results)} depths already on disk")

    for R in DEPTHS:
        key = str(R)
        if key in results:
            log(f"  R={R}: on disk, skip")
            continue
        log(f"  R={R}: simulating {N_HIST:,} histories ...")
        res = run_depth(R, K_FIXED)
        if res is None:
            continue
        results[key] = res
        with open(RESULT_PATH, "w") as f:
            json.dump(results, f, indent=2)
        a = res["caseA"]
        log(f"  R={R}: caseA tau_R={a['tau_R']:.4f} "
            f"in_band={a['tau_in_band']} II_R={a['II_R_body']}")
        for k in K_FIXED:
            kk = res["caseB"].get(f"k{k}")
            if kk:
                log(f"         caseB k={k}: tau_mean={kk['tau_mean']:.4f} "
                    f"in_band={kk['n_in_band']}/{kk['n_windows']} "
                    f"II_abs_mean={kk['II_abs_mean']:.2e} "
                    f"shuffle_gap={kk['shuffle_gap_mean']:.2e}")
        log(f"         ({res['runtime_s']}s)")

    log("=" * 70)
    log("DONE -- analysis in analyze_kbody.py / RESULTS.md")
    log("=" * 70)


if __name__ == "__main__":
    main()

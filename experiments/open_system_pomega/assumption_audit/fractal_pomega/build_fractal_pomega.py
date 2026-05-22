#!/usr/bin/env python3
"""
P_omega — the fractal / RG-nested construction.
================================================

Author-authorized protocol extension of the assumption audit. Pre-registration:
fractal_pomega/PREREGISTRATION.md (committed before this run).

THE ERROR THIS CORRECTS
-----------------------
R1, R2, R3 and the R1 AND R2 conjunction all horned EMPTY by one mechanism:
the joint Kish participation ratio of the cross-rung correlation matrix dilutes
to the chaos pole, rho_joint ~ c/(count-1) -> 0. The conjunction's RESULTS.md
diagnosed this precisely:

    "C_w has unit diagonal and only ADJACENT off-diagonal entries, so
     Tr(C_w) ~ R while Tr(C_w^2) ~ R + cR. Then k_eff_joint ~ R/(1+c) grows
     linearly in R, and rho_joint = (R/k_eff - 1)/(R-1) ~ c/(R-1) -> 0."

That law is CHAIN-SPECIFIC. It rests on each rung having O(1) correlated
partners -- the nearest-neighbour property of a 1D chain. The conjunction kept
assumption 5 (nearest-neighbour topology) explicitly. R1's own control already
showed an all-to-all tower does NOT dilute.

But the framework's rungs are NOT a 1D chain and NOT generic all-to-all. They
are RG COARSE-GRAININGS (Piece 6; construct_p_omega_mera.py builds the MERA
isometry tower): rung n+1 is built FROM rung n by block-decimation. Every
higher rung contains the lower ones; the rungs sit on a binary nesting TREE.

THE CONSTRUCTION
----------------
The R1 AND R2 machinery, verbatim, with ONE fix: the cross-rung coupling
topology.

  Frame (from R2, build_history_pomega.py, reused UNCHANGED): universe
  trajectories, rungs Ph0..A5 emerging sequentially over cosmic time, each
  rung's within-rung rho_n(t) evolving by Piece 2 dynamics drho/dt = alpha -
  gamma*M, held in its corridor by active management. The all-emerged
  sub-ensemble is what the post-selection acts on.

  Functional (from R1, verbatim): rho_joint = Kish-inverse of the participation
  ratio (Tr C_w)^2 / Tr(C_w^2) of the corridor-weighted R x R rung-correlation
  matrix. Constituents are the R corridor-capped rungs. Piece 1 (Kish), the
  participation-ratio reading of k_eff, Piece 3 (the band). NOT re-chosen.

  THE ONE FIX -- the cross-rung coupling C_w[n,m] for |n-m| > 1:
    The chain set C_w[n,m] = 0 for |n-m| > 1.
    The framework's genuine RG nesting sets it NON-zero, by the binary nesting
    tree. Rung n and rung n+k are coupled THROUGH the nesting: rung n+k is the
    k-fold RG coarse-graining of rung n, so they share an RG flow. The coupling
    is the adjacent cross-rung coupling PROPAGATED through k levels of nesting.

    RG composition is multiplicative and self-similar: each coarse-graining
    step contracts the correlation by the same RG factor. So if the adjacent
    rungs couple at strength c1 (the framework's MEASURED cross-rung coupling
    ratio -- the 26-cell g/J campaign, O(1)), then rung n and rung n+k couple
    at c1 propagated k times.

    Two genuine RG-nested topologies are built and BOTH reported -- the
    construction does not pre-judge which the framework's nesting realises:

    (A) RG-FLOW (Toeplitz) coupling: C_w[n,m] = c1^|n-m| read off the
        trajectory. The geometric decay is RG composition along the flow:
        scale-distance k <-> k coarse-graining steps <-> factor c1^k. Self-
        similar: the same RG factor at every step. NOT a tuned power-law -- the
        decay base c1 IS the measured adjacent coupling; the exponent is forced
        to be the integer scale-distance by RG composition.

    (B) ULTRAMETRIC (binary nesting tree) coupling: the framework's rungs sit
        on the MERA binary tree (construct_p_omega_mera.py: H_0 -> H_1 -> H_2,
        each rung blocks of the one below). The cross-rung coupling between
        rung n and rung m is set by their ULTRAMETRIC distance on that tree --
        the depth of their lowest common ancestor. Rungs sharing a recent
        common coarse-graining are strongly coupled; rungs whose common
        ancestor is deep in the tree are weakly coupled. This is the genuine
        hierarchical / fractal structure: C_w[n,m] = c1^(treedist(n,m)). The
        ultrametric matrix has a HIERARCHICAL eigenvalue spectrum -- a small
        number of large eigenvalues (the coarse blocks) and many small ones --
        which is the candidate sub-extensive structure H2' predicts.

  In both, the per-entry coupling magnitude is corridor-weighted exactly as in
  R1xR2: C_w = D C D, D = diag(sqrt(w_n)), w_n = soft(rho_n at t_f), AND each
  off-diagonal is scaled by the trajectory's own cross-rung correlation read
  off the history (soft(rvia)). The topology fix changes ONLY which pairs are
  coupled and the scale-distance decay -- nothing else from R1xR2.

WHAT IS AND IS NOT TUNED
------------------------
  c1, the adjacent-rung coupling, is NOT a free knob. It is the framework's
  MEASURED cross-rung / within-rung coupling ratio: the 26-cell g/J campaign
  (Corridor Dynamics.tex sec:crossrung) found O(1), three rung-pair medians
  0.31 / 0.72 / 1.15. We additionally read c1 directly off each trajectory
  (the soft(rvia) cross term, exactly as R1xR2 did for the adjacent entry) --
  so the COUPLING ITSELF is data, not a constant. The only thing the topology
  fix adds is: that same coupling, propagated to non-adjacent rungs by RG
  composition over the nesting tree, instead of being set to zero.

  If a verdict required choosing c1 to manufacture a bounded rho_joint, the
  pre-registration says STOP. It does not: c1 is read off the trajectory; the
  decay law is forced by RG composition; the verdict is whatever results.

THE HYPOTHESES (pre-registration)
---------------------------------
  H2' DECISIVE -- no dilution: with the RG-nested coupling does rho_joint stay
     bounded off the chaos pole, or still dilute? The chain gave rho_joint ~
     1/R -> 0. H2' is the fractal coupling gives a power-law correlation
     spectrum -> sub-extensive k_eff -> bounded rho_joint. Report rho_joint vs
     R explicitly, against the chain's rho_joint ~ R^-1.09 baseline.
  H1 non-decomposability -- segment-shuffle: does the functional factorize?
  H3 joint work -- non-empty, selective, well-defined to 9 rungs.

VERDICT
-------
  OPENS  : H2' AND H1 AND H3 -- fractal coupling holds rho_joint bounded,
           functional does not factorize, joint object non-empty + selective.
  EMPTY  : rho_joint dilutes even under the genuine RG-nested coupling.
  TRIVIAL: the functional still factorizes.

DISCIPLINE
----------
CUDA throughout (cupy). Per-depth progress printed. Interim results flushed to
results_fractal.json after EVERY rung-depth. RESUMES from on-disk partials.
Two-sided: EMPTY or TRIVIAL fires F-11 for real. The coupling is the
framework's genuine RG nesting, not tuned to a verdict.
"""

import json
import os
import sys
import time

import numpy as np

try:
    import cupy as cp
except Exception as e:  # pragma: no cover
    print(f"FATAL: cupy unavailable ({e}). fractal_pomega requires CUDA.",
          flush=True)
    sys.exit(1)

# R2's sequential-emergence simulator, reused unchanged (same module the
# R1xR2 conjunction reused).
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "R1xR2_conjunction"))
import build_history_pomega as B

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results_fractal.json")

RHO_LOWER = B.RHO_LOWER          # 0.10  (Piece 3)
RHO_UPPER = B.RHO_UPPER          # 0.43  (Piece 3)
RHO_MID = B.RHO_MID              # 0.265 corridor centre
W_HALF = B.W_HALF                # 0.165 corridor half-width
SEED = B.SEED

# the framework's 9 rungs Ph0..A5, and past R* to expose the asymptotic law.
R_SCAN = [3, 4, 5, 6, 7, 8, 9, 11, 13, 20]
N_BY_R = {3: 400_000, 4: 400_000, 5: 600_000, 6: 800_000, 7: 1_000_000,
          8: 1_400_000, 9: 2_000_000, 11: 4_000_000, 13: 8_000_000,
          20: 20_000_000}
CHUNK = 40_000


def log(msg):
    print(msg, flush=True)


def soft(r, beta):
    """Graded corridor-band membership weight in [0,1] -- the within-rung
    corridor cap, as a soft TSVF post-selection factor (R1xR2's `soft`)."""
    return cp.exp(-beta * (cp.nan_to_num(r, nan=2.0) - RHO_MID) ** 2)


# ---------------------------------------------------------------------------
# THE RG-NESTED CROSS-RUNG TOPOLOGY -- the one fix over R1xR2.
# ---------------------------------------------------------------------------
def ultrametric_treedist(R):
    """Tree-distance matrix for R rungs on the framework's binary nesting tree
    (the MERA tower: rung n+1 = block-decimation coarse-graining of rung n,
    construct_p_omega_mera.py). The rungs are the LEAVES of a binary tree;
    rung n and rung m are coupled by the depth of their lowest common
    ancestor. The ultrametric distance d(n,m) is the number of nesting levels
    up to that common ancestor.

    For leaves indexed 0..R-1 on a binary tree, the lowest-common-ancestor
    depth from the leaves is, by the standard binary-tree LCA identity, the
    bit-length of (n XOR m): d(n,m) = floor(log2(n^m)) + 1, d(n,n)=0.

    Returns an R x R int matrix of tree distances. This IS the framework's
    nesting topology -- a binary RG tree -- not a chosen metric."""
    d = np.zeros((R, R), dtype=np.int64)
    for n in range(R):
        for m in range(R):
            if n == m:
                continue
            x = n ^ m
            d[n, m] = int(x).bit_length()   # LCA depth on the binary tree
    return d


def coupling_matrix_template(R, topology):
    """The cross-rung coupling-decay TEMPLATE T[n,m] in [0,1] -- the
    scale-distance factor by which the trajectory's adjacent coupling is
    propagated to the (n,m) rung pair. The trajectory's measured coupling
    multiplies this; the template is the pure RG-nesting geometry.

    'chain'      : T[n,m] = 1 if |n-m|==1 else 0       (R1xR2 baseline)
    'rgflow'     : T[n,m] = scaledist^|n-m|            (A: RG-flow Toeplitz)
    'ultrametric': T[n,m] = scaledist^treedist(n,m)    (B: binary nesting tree)

    scaledist is fixed to C1_RG below (NOT tuned -- see header). Returned as a
    GPU float64 (R,R) array."""
    if topology == "chain":
        T = np.zeros((R, R))
        for n in range(R - 1):
            T[n, n + 1] = T[n + 1, n] = 1.0
        return cp.asarray(T)
    if topology == "rgflow":
        idx = np.arange(R)
        k = np.abs(idx[:, None] - idx[None, :]).astype(np.float64)
        T = C1_RG ** k
        np.fill_diagonal(T, 0.0)
        return cp.asarray(T)
    if topology == "ultrametric":
        d = ultrametric_treedist(R).astype(np.float64)
        T = C1_RG ** d
        np.fill_diagonal(T, 0.0)
        return cp.asarray(T)
    raise ValueError(topology)


# C1_RG -- the RG-composition contraction per scale-step. NOT a free knob:
# it is the framework's MEASURED adjacent cross-rung / within-rung coupling
# ratio. The 26-cell g/J campaign (Corridor Dynamics.tex sec:crossrung) found
# O(1), three rung-pair medians 0.31 / 0.72 / 1.15. The geometric mean of the
# three measured rung-pair medians is the framework-faithful single number for
# the per-scale-step contraction:  (0.31*0.72*1.15)^(1/3) = 0.626.
# It is held FIXED at that measured value; it is not swept to chase a verdict.
# (The trajectory's own cross-rung correlation -- soft(rvia) -- additionally
# multiplies the adjacent entry, so the coupling carried into the matrix is
# data x this measured geometry, exactly as R1xR2 used soft(rvia).)
C1_RG = (0.31 * 0.72 * 1.15) ** (1.0 / 3.0)   # = 0.6257 -- measured, fixed.


# ---------------------------------------------------------------------------
# THE FRACTAL JOINT FUNCTIONAL -- R1xR2's functional, RG-nested topology.
# ---------------------------------------------------------------------------
def joint_rho_history(rtf, rvia, beta, T_template):
    """The fractal omega-weight. R1's joint Kish participation ratio carried on
    R2's history frame, with the within-rung corridor cap re-injected (all
    exactly as R1xR2's joint_rho_history) -- the ONE change is that the cross-
    rung coupling is the RG-nested template T_template, not nearest-neighbour.

    Inputs (GPU arrays, all-emerged histories only):
      rtf        : (K, R)    rung rho at t_f                 -- within-rung
      rvia       : (K, R-1)  rho of rung n at the step rung n+1 emerged
                             -- R2's sequential-emergence timing coupling
      beta       : corridor-referenced sharpness 1/2w^2
      T_template : (R, R)    the RG-nesting coupling-decay template (GPU)

    Construction, per history:
      1. per-rung corridor weight w_n = soft(rtf_n) in [0,1] -- the within-rung
         corridor cap (R1xR2 step 1, unchanged).
      2. the R x R rung correlation matrix C:
           C[n,n]   = 1
           C[n,m]   = cross-rung correlation for n != m. The ADJACENT coupling
                      is read off the trajectory exactly as R1xR2: the cross-
                      rung correlation soft(rvia) scaled to [0, CMAX]. For
                      NON-adjacent pairs the chain set this 0; the RG-nested
                      construction propagates the adjacent coupling through the
                      nesting by the template:
                        C[n,m] = CMAX * cross_adj[n,m] * T_template[n,m]
                      where cross_adj is the trajectory's adjacent coupling
                      lifted to a full matrix (an adjacent edge's coupling is
                      the geometric interpolation of the soft(rvia) bond
                      couplings it spans -- so a non-adjacent entry carries the
                      genuine coupling of the rungs between it, not a constant).
      3. corridor-weight: C_w = D C D, D = diag(sqrt(w_n))   (R1xR2 step 3).
      4. joint Kish participation ratio on the RUNG count R  (R1xR2 step 4):
           k_eff_joint = (Tr C_w)^2 / Tr(C_w^2)
           rho_joint   = (R / k_eff_joint - 1) / (R - 1)
      5. log w_omega = log smooth_band_indicator(rho_joint)  (R1xR2 step 5).

    Returns (log_w, rho_joint, k_eff_joint) -- all (K,) GPU arrays.
    """
    K, R = rtf.shape
    CMAX = float(RHO_UPPER)

    w = soft(rtf, beta)                                  # (K, R)
    sw = cp.sqrt(cp.clip(w, 1e-12, 1.0))                 # (K, R) = diag(D)

    C = cp.zeros((K, R, R), dtype=cp.float64)
    diag_idx = cp.arange(R)
    C[:, diag_idx, diag_idx] = 1.0

    if R > 1:
        # adjacent-bond cross-rung correlation read off the trajectory,
        # identically to R1xR2: soft(rvia_n) in [0,1], one per bond n..n+1.
        cross_bond = soft(rvia, beta)                    # (K, R-1) in [0,1]
        # lift the bond couplings to a full (K,R,R) cross matrix. The genuine
        # coupling between rungs n and m (n<m) is the trajectory coupling of
        # the chain of bonds between them, propagated by the RG template:
        #   cross[n,m] = T_template[n,m] * geommean(cross_bond[n..m-1])
        # geommean of the spanned bonds = the trajectory's own scale-distance
        # coupling; T_template = the RG-nesting decay. For |n-m|==1 the
        # geommean is just the single bond and T_template==C1^1 or ==1 (chain
        # sets adjacent template to 1; rgflow/ultra to C1) -- see note below.
        # log-cumsum trick for geommean over arbitrary spans, on GPU.
        logb = cp.log(cp.clip(cross_bond, 1e-12, 1.0))   # (K, R-1)
        # prefix[k] = sum_{j<k} logb[:,j];  prefix has R columns (0..R-1)
        prefix = cp.zeros((K, R), dtype=cp.float64)
        prefix[:, 1:] = cp.cumsum(logb, axis=1)
        # for pair (n,m), n<m: span sum = prefix[m]-prefix[n], #bonds = m-n
        n_i = cp.arange(R)
        span_bonds = cp.abs(n_i[:, None] - n_i[None, :])           # (R,R)
        span_bonds_safe = cp.clip(span_bonds, 1, None)
        # span sum of logs over the bonds between rungs n and m. logb <= 0
        # (logs of probabilities in [0,1]), so the span sum is non-positive
        # for either ordering of (n,m); use -|.| so geom = exp(span/#bonds)
        # is the geometric MEAN, always in (0,1]. (A previous version took
        # +|.|, which flipped the sign and blew geom up above 1 -- corrected.)
        span_logsum = -cp.abs(prefix[:, None, :] - prefix[:, :, None])  # (K,R,R)
        geom = cp.exp(span_logsum / span_bonds_safe[None, :, :])   # (K,R,R)
        cross_full = CMAX * geom * T_template[None, :, :]          # (K,R,R)
        # write off-diagonal; keep the unit diagonal
        offdiag = (span_bonds > 0)
        C = cp.where(offdiag[None, :, :], cross_full, C)

    Cw = C * sw[:, :, None] * sw[:, None, :]             # (K, R, R) = D C D

    trCw = cp.einsum('knn->k', Cw)                       # Tr C_w
    trCw2 = cp.einsum('knm,kmn->k', Cw, Cw)              # Tr(C_w^2)
    k_eff_joint = (trCw * trCw) / cp.clip(trCw2, 1e-300, None)
    if R > 1:
        rho_joint = (R / k_eff_joint - 1.0) / (R - 1.0)
    else:
        rho_joint = cp.zeros(K)

    sharp = 40.0
    rise = 1.0 / (1.0 + cp.exp(-sharp * (rho_joint - RHO_LOWER)))
    fall = 1.0 / (1.0 + cp.exp(-sharp * (RHO_UPPER - rho_joint)))
    e_omega = rise * fall
    log_w = cp.log(cp.clip(e_omega, 1e-300, None))
    return log_w, rho_joint, k_eff_joint


def collect_allemerged(R, n_hist, seed, beta):
    """Run R2's simulator in GPU chunks; keep, per all-emerged history, rtf
    (rho at t_f, per rung) and rvia (rho at successor-emergence, per bond).
    Identical to R1xR2's collect_allemerged."""
    rtf_parts, rvia_parts = [], []
    done, cidx, n_all = 0, 0, 0
    while done < n_hist:
        this = min(CHUNK, n_hist - done)
        sim = B.simulate_histories(R, this, seed + 104729 * cidx)
        T = sim["T_total"]
        rho = sim["rho"]
        es = sim["emerge_step"]
        ne = sim["n_emerged"]
        idx = cp.where(ne == R)[0]
        if idx.size > 0:
            rows = idx
            rtf_sel = rho[rows, :, T - 1]
            rvia = cp.empty((idx.size, max(R - 1, 1)), dtype=cp.float64)
            for n in range(R - 1):
                esn = cp.clip(es[rows, n + 1], 0, T - 1)
                rvia[:, n] = rho[rows, n, esn]
            if R == 1:
                rvia[:, 0] = RHO_MID
            rtf_parts.append(cp.asnumpy(rtf_sel))
            rvia_parts.append(cp.asnumpy(rvia))
            n_all += int(idx.size)
        del sim, rho, es
        cp.get_default_memory_pool().free_all_blocks()
        done += this
        cidx += 1
        if cidx % 50 == 0 or done >= n_hist:
            log(f"      R={R:2d} sim {done:,}/{n_hist:,} "
                f"({100 * done // n_hist}%)  all-emerged so far {n_all:,}")
    if not rtf_parts:
        return None, None, n_hist, 0
    rtf = cp.asarray(np.concatenate(rtf_parts))
    rvia = cp.asarray(np.concatenate(rvia_parts))
    return rtf, rvia, n_hist, n_all


def metrics_for_topology(rtf, rvia, beta, R, topology, seed):
    """The three-hypothesis metrics for one cross-rung topology. CUDA."""
    K = rtf.shape[0]
    T_tmpl = coupling_matrix_template(R, topology)

    log_w, rho_joint, k_eff_joint = joint_rho_history(rtf, rvia, beta, T_tmpl)

    # H2' -- dilution. post-selected ensemble + band-reachability extreme.
    finite = cp.isfinite(log_w)
    lw = cp.where(finite, log_w, -1e300)
    top = float(cp.max(lw))
    w_ps = cp.exp(lw - top)
    w_ps = w_ps / cp.clip(cp.sum(w_ps), 1e-300, None)
    rho_joint_psmean = float(cp.sum(w_ps * rho_joint))
    keff_joint_psmean = float(cp.sum(w_ps * k_eff_joint))
    rho_joint_mean = float(cp.mean(rho_joint))
    rho_joint_max = float(cp.max(rho_joint))
    rho_joint_min = float(cp.min(rho_joint))
    keff_joint_mean = float(cp.mean(k_eff_joint))
    in_band = (rho_joint > RHO_LOWER) & (rho_joint < RHO_UPPER)
    frac_in_band = float(cp.mean(in_band.astype(cp.float64)))
    n_in_band = int(cp.sum(in_band))

    # H3 -- selectivity & joint work.
    acc = (lw > top - 1.0)
    accept_frac = float(cp.mean(acc.astype(cp.float64)))
    # joint work: turn the cross-rung coupling OFF (rvia huge -> soft~0 -> all
    # off-diagonal entries 0) and recompute. unchanged rho_joint => secretly
    # per-rung => trivial.
    _, rho_joint_off, _ = joint_rho_history(
        rtf, cp.full_like(rvia, 100.0), beta, T_tmpl)
    cross_delta = float(cp.mean(cp.abs(rho_joint - rho_joint_off)))
    cross_delta_max = float(cp.max(cp.abs(rho_joint - rho_joint_off)))

    # H1 -- segment-shuffle non-decomposability. draw each rung's t_f state and
    # each bond's via-state INDEPENDENTLY from the post-selected marginals,
    # recompute. factorizes => shuffled reproduces the joint weight (gap ~ 0).
    nrng = np.random.RandomState((seed + 777) % (2 ** 32))
    wnp = cp.asnumpy(w_ps).astype(np.float64)
    wnp = wnp / wnp.sum()
    nshuf = K
    rtf_shuf = cp.empty((nshuf, R), dtype=cp.float64)
    for n in range(R):
        pick = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
        rtf_shuf[:, n] = rtf[pick, n]
    rvia_shuf = cp.empty((nshuf, max(R - 1, 1)), dtype=cp.float64)
    for n in range(max(R - 1, 1)):
        pick = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
        rvia_shuf[:, n] = rvia[pick, n]
    log_w_shuf, _, _ = joint_rho_history(rtf_shuf, rvia_shuf, beta, T_tmpl)
    pick_real = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
    log_w_real = log_w[pick_real]
    mean_real = float(cp.mean(cp.where(cp.isfinite(log_w_real),
                                       log_w_real, -50.0)))
    mean_shuf = float(cp.mean(cp.where(cp.isfinite(log_w_shuf),
                                       log_w_shuf, -50.0)))
    shuffle_gap = mean_real - mean_shuf
    shuffle_gap_per_rung = shuffle_gap / R

    return dict(
        topology=topology,
        rho_joint_psmean=rho_joint_psmean,
        rho_joint_mean=rho_joint_mean,
        rho_joint_max=rho_joint_max,
        rho_joint_min=rho_joint_min,
        rho_joint_times_R_psmean=rho_joint_psmean * R,
        rho_joint_times_R_atmax=rho_joint_max * R,
        k_eff_joint_psmean=keff_joint_psmean,
        k_eff_joint_mean=keff_joint_mean,
        band_reachable=bool(n_in_band > 0),
        frac_in_band=frac_in_band,
        n_in_band=n_in_band,
        accept_frac=accept_frac,
        cross_delta_mean=cross_delta,
        cross_delta_max=cross_delta_max,
        mean_logw_real=mean_real,
        mean_logw_shuffled=mean_shuf,
        shuffle_gap=shuffle_gap,
        shuffle_gap_per_rung=shuffle_gap_per_rung,
    )


def analyse_depth(R, n_hist, beta, seed):
    """Build the construction at depth R for all three topologies and compute
    the three-hypothesis metrics. The chain topology is recomputed here as the
    in-run baseline so H2' is read against it directly."""
    rtf, rvia, n_hist, n_all = collect_allemerged(R, n_hist, seed, beta)
    if n_all < 200:
        return dict(R=R, n_hist=n_hist, n_all_emerged=n_all,
                    note="too few all-emerged histories for statistics")
    K = rtf.shape[0]
    out = dict(R=R, n_hist=n_hist, n_all_emerged=n_all, K=K, beta=beta,
               c1_rg=C1_RG)
    for topology in ("chain", "rgflow", "ultrametric"):
        out[topology] = metrics_for_topology(rtf, rvia, beta, R, topology, seed)
    return out


def main():
    cp.random.seed(SEED)
    beta = 1.0 / (2.0 * W_HALF ** 2)
    log("=" * 74)
    log("P_omega -- the fractal / RG-nested construction")
    log("  R1xR2's joint Kish participation-ratio functional on R2's open")
    log("  sequential history frame; cross-rung coupling = the framework's")
    log("  genuine RG nesting (Piece 6 / the MERA binary tree), not a chain.")
    log(f"  corridor band ({RHO_LOWER}, {RHO_UPPER}); centre {RHO_MID}; "
        f"half-width {W_HALF}")
    log(f"  beta_pin = 1/2w^2 = {beta:.4f}")
    log(f"  C1_RG (per-scale RG contraction, = geommean of measured g/J "
        f"medians 0.31/0.72/1.15) = {C1_RG:.4f}")
    log(f"  topologies: chain (R1xR2 baseline) | rgflow (Toeplitz c1^|n-m|) | "
        f"ultrametric (binary nesting tree)")
    log(f"  GPU: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
    log("=" * 74)

    # ---- RESUME from on-disk partial results ------------------------------
    results = []
    done_R = set()
    if os.path.exists(RESULTS):
        try:
            with open(RESULTS) as f:
                prev = json.load(f)
            results = prev.get("results", [])
            done_R = {r["R"] for r in results
                      if "ultrametric" in r or "note" in r}
            if done_R:
                log(f"  RESUMING -- depths {sorted(done_R)} already on disk, "
                    f"will be skipped.")
        except Exception as e:
            log(f"  (could not parse existing {RESULTS}: {e}; starting fresh)")
            results, done_R = [], set()

    def flush(t0):
        with open(RESULTS, "w") as f:
            json.dump(dict(
                meta=dict(
                    construction="fractal / RG-nested P_omega",
                    seed=SEED, beta_pin=beta, c1_rg=C1_RG,
                    rho_lower=RHO_LOWER, rho_upper=RHO_UPPER,
                    rho_mid=RHO_MID, w_half=W_HALF,
                    topologies=["chain", "rgflow", "ultrametric"],
                    functional=("rho_joint = Kish-inverse of the participation "
                                "ratio of the corridor-weighted R x R "
                                "rung-correlation matrix; cross-rung coupling "
                                "is the RG-nested template (rgflow Toeplitz / "
                                "ultrametric binary nesting tree), c1 fixed at "
                                "the measured g/J geometric mean 0.626"),
                    elapsed_s=time.time() - t0),
                results=results,
            ), f, indent=2)

    t0 = time.time()
    for R in R_SCAN:
        if R in done_R:
            log(f"  R={R:2d}  already done -- skipped (resume)")
            continue
        ts = time.time()
        res = analyse_depth(R, N_BY_R[R], beta, SEED + R * 7919)
        res["wall_s"] = time.time() - ts
        results.append(res)
        if "note" in res:
            log(f"  R={R:2d}  N={N_BY_R[R]:>9d}  {res['note']}  "
                f"({res['wall_s']:.1f}s)")
        else:
            ch, rg, um = res["chain"], res["rgflow"], res["ultrametric"]
            log(f"  R={R:2d}  N={N_BY_R[R]:>9d}  K={res['K']:>7d}  "
                f"({res['wall_s']:.1f}s)")
            log(f"        rho_joint(ps):  chain={ch['rho_joint_psmean']:.4f}  "
                f"rgflow={rg['rho_joint_psmean']:.4f}  "
                f"ultra={um['rho_joint_psmean']:.4f}")
            log(f"        rho_joint*R  :  chain={ch['rho_joint_times_R_psmean']:.3f}"
                f"  rgflow={rg['rho_joint_times_R_psmean']:.3f}  "
                f"ultra={um['rho_joint_times_R_psmean']:.3f}")
            log(f"        k_eff(ps)    :  chain={ch['k_eff_joint_psmean']:.3f}  "
                f"rgflow={rg['k_eff_joint_psmean']:.3f}  "
                f"ultra={um['k_eff_joint_psmean']:.3f}")
            log(f"        in-band frac :  chain={ch['frac_in_band']:.4f}  "
                f"rgflow={rg['frac_in_band']:.4f}  "
                f"ultra={um['frac_in_band']:.4f}")
            log(f"        shuffle_gap  :  chain={ch['shuffle_gap']:.4f}  "
                f"rgflow={rg['shuffle_gap']:.4f}  "
                f"ultra={um['shuffle_gap']:.4f}")
        flush(t0)
        log(f"      flushed -> {RESULTS}")

    log(f"\ndone, {time.time() - t0:.1f}s total. results -> {RESULTS}")


if __name__ == "__main__":
    main()

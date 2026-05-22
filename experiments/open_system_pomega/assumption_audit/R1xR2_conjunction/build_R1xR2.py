#!/usr/bin/env python3
"""
P_omega — the R1 AND R2 conjunction.
====================================

Author-authorized protocol extension of the assumption audit. Pre-registration:
R1xR2_conjunction/PREREGISTRATION.md (committed before this run).

WHAT THIS IS
------------
The single-assumption audit horned three times by three distinct mechanisms:
  R1 (non-additive functional, static): HORNED by chaos-pole DILUTION.
      rho_joint = Kish-inverse[(Tr C)^2 / Tr(C^2)] of one whole-tower
      correlation matrix built over RAW constituents K = R*m. Under
      nearest-neighbour locality Tr(C^2) ~ K + c*K, so rho_joint ~ 4/K -> 0.
      The corridor band became unreachable past R ~ 12.
  R2 (history-space frame, additive weight): HORNED by FACTORIZATION.
      The joint weight Sigma_n log soft(rho_n) is additive -> exponentiates to
      a product -> segment-shuffle gap flat near zero.
  R3: HORNED by within/cross antagonism (separate mechanism, not in scope).

R1's failure and R2's failure are hypothesised mutually curing. THIS run builds
the one principled conjunction: R1's genuinely non-additive joint Kish
participation-ratio functional, carried on R2's open sequential history-space
frame, with the proven within-rung corridor cap (k_eff ~ 10 per rung) re-injected.

THE CONSTRUCTION
----------------
Frame (from R2): exactly R2's simulator (build_history_pomega.py) — universe
trajectories, rungs Ph0..A5 emerging sequentially over cosmic time, each rung's
within-rung rho_n(t) evolving by Piece 2 dynamics drho/dt = alpha - gamma*M and
maintained inside its corridor band by active management. Reused unchanged.

Functional (from R1): the omega-weight is the JOINT KISH PARTICIPATION RATIO of
the trajectory's rung structure — but with the cure for R1's dilution applied.

  R1 diluted because it built C_joint over RAW constituents (K = R*m), so the
  "constituent count" in the Kish inverse blew up with depth. THE RE-INJECTED
  PROVEN CONSTRAINT (pre-registration): the within-rung corridor caps each
  rung's effective dimensionality at k_eff ~ 10. So the joint object's
  constituents are not the R*m raw spins; they are the R RUNGS, each
  corridor-capped. The joint correlation object is the R x R rung-level
  correlation matrix C_rung:
    - diagonal: 1 (each rung is a unit, self-correlated)
    - off-diagonal C_rung[a,b]: the cross-rung correlation between rung a and
      rung b, READ OFF THE TRAJECTORY. Adjacent rungs (|a-b|=1) carry the
      genuine sequential-emergence timing coupling that R2's Test B found —
      the rho rung a HAD at the step rung b emerged, relative to the corridor.
      Non-adjacent rungs: nearest-neighbour topology kept (R1 dropped only
      2 and 3, not 5), so 0 — BUT the joint Kish functional still mixes them
      through the trace ratio.
    - each rung's contribution is corridor-WEIGHTED: a rung outside its band
      contributes a down-weighted (chaos-side) entry; the corridor cap enters
      as the per-rung weight w_n = soft(rho_n at t_f) in [0,1].

  The omega-weight is then:
    k_eff_joint  = (Tr C_w)^2 / Tr(C_w^2)              participation ratio
    rho_joint    = (R / k_eff_joint - 1) / (R - 1)      Kish inverse, Piece 1
                   evaluated on the RUNG count R, not R*m.
    log w_omega(history) = log smooth_band_indicator(rho_joint)

  C_w is the rung-correlation matrix with each rung's row/column scaled by its
  corridor weight sqrt(w_n) — so a corridor-occupying trajectory has full-weight
  rungs, a trajectory with rungs out of band has down-weighted rungs and a
  diluted joint object. This is genuinely non-additive: rho_joint is a ratio of
  traces of ONE matrix; Tr(C_w^2) = Sigma_ab C_w[a,b]^2 mixes every rung pair;
  the Kish inverse is nonlinear in that sum. There is NO Sigma_n log soft(rho_n)
  decomposition — that is exactly what factorized R2.

WHY THIS IS FRAMEWORK-FAITHFUL, NOT REVERSE-ENGINEERED
------------------------------------------------------
  - The functional is R1's object verbatim: Kish-inverse of a participation
    ratio (Tr C)^2/Tr(C^2). Piece 1 (Kish), the participation-ratio reading of
    k_eff (NOTES / exp5), Piece 3 (the band). Nothing invented.
  - The ONLY change from R1 is the re-injected PROVEN constraint named in the
    pre-registration: the within-rung corridor caps k_eff ~ 10, so the joint
    object is built over the R corridor-capped rungs, not the R*m raw spins.
    This is the structure the pre-registration explicitly hypothesises will
    prevent R1's dilution — it is a stated re-injection, not a tuned knob.
  - The frame is R2's simulator unchanged.
  - It is two-sided. If the rung-level joint functional ALSO dilutes (rho_joint
    -> 0 with R), H2 fails -> EMPTY. If the joint weight still factorizes under
    segment-shuffle, H1 fails -> TRIVIAL. The construction does not know which.
    The functional was fixed by the pre-registration BEFORE the run; it is not
    re-chosen to chase a verdict.

THE THREE HYPOTHESES (pre-registration)
---------------------------------------
  H1 non-decomposability (cures R2): segment-shuffle gap is real AND GROWS
     with R. R2's was flat near zero.
  H2 no dilution (cures R1): joint k_eff / rho_joint stays bounded with depth,
     does NOT run to the chaos pole as R1's rho_joint ~ 4/K did.
  H3 joint work (OPENS): non-empty, selective, genuinely couples the
     trajectory, well-defined to 9 rungs.

VERDICT
-------
  OPENS  : H1 AND H2 AND H3.
  EMPTY  : H2 fails — joint functional dilutes to the chaos pole.
  TRIVIAL: H1 fails — joint functional still factorizes under segment-shuffle.

DISCIPLINE
----------
CUDA throughout (cupy). Per-depth progress printed. Interim results flushed to
results_R1xR2.json after EVERY rung-depth. RESUMES from on-disk partial results
(loads the JSON, skips completed depths). A HORN (EMPTY/TRIVIAL) is a valid
reportable result that fires F-11. The functional is not tuned to OPEN.
"""

import json
import os
import sys
import time

import numpy as np

try:
    import cupy as cp
    xp = cp
    GPU = True
except Exception as e:  # pragma: no cover
    print(f"FATAL: cupy unavailable ({e}). R1xR2 requires CUDA.", flush=True)
    sys.exit(1)

import build_history_pomega as B   # R2's sequential-emergence simulator, reused

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results_R1xR2.json")

RHO_LOWER = B.RHO_LOWER          # 0.10  (Piece 3)
RHO_UPPER = B.RHO_UPPER          # 0.43  (Piece 3)
RHO_MID   = B.RHO_MID            # 0.265 corridor centre
W_HALF    = B.W_HALF             # 0.165 corridor half-width
SEED      = B.SEED

# the framework's 9 rungs: Ph0,Ph1,Ph2,A0,A1,A2,A3,A4,A5 — and past R*.
R_SCAN = [3, 4, 5, 6, 7, 8, 9, 11, 13, 20]
# N histories per depth: grown so the all-emerged sub-ensemble stays adequate.
N_BY_R = {3: 400_000, 4: 400_000, 5: 600_000, 6: 800_000, 7: 1_000_000,
          8: 1_400_000, 9: 2_000_000, 11: 4_000_000, 13: 8_000_000,
          20: 20_000_000}
CHUNK = 40_000


def log(msg):
    print(msg, flush=True)


def soft(r, beta):
    """Graded corridor-band membership weight in [0,1] — the within-rung
    corridor cap, as a soft (measure-graded) TSVF post-selection factor.
    r outside the band -> small weight; r at the corridor centre -> 1."""
    return cp.exp(-beta * (cp.nan_to_num(r, nan=2.0) - RHO_MID) ** 2)


# ---------------------------------------------------------------------------
# THE R1 x R2 NON-ADDITIVE FUNCTIONAL
# ---------------------------------------------------------------------------
def joint_rho_history(rtf, rvia, beta):
    """THE R1 x R2 OMEGA-WEIGHT — R1's joint Kish participation ratio carried
    on R2's history frame, with the within-rung corridor cap re-injected.

    Inputs (GPU arrays, all-emerged histories only):
      rtf  : (K, R)    rung rho at t_f                  — within-rung state
      rvia : (K, R-1)  rho of rung n at the step rung n+1 emerged
                       — R2's sequential-emergence timing coupling
      beta : corridor-referenced sharpness 1/2w^2

    Construction, per history:
      1. per-rung corridor weight  w_n = soft(rtf_n)  in [0,1]   — the
         re-injected within-rung corridor cap (a rung out of band is
         down-weighted; this is what bounds the joint object's effective size).
      2. the R x R rung-level correlation matrix C:
           C[n,n]   = 1
           C[n,n+1] = C[n+1,n] = cross-rung correlation, read off the
                      trajectory: how corridor-aligned rung n was at rung n+1's
                      emergence. = soft(rvia_n) scaled to a correlation in
                      [0, CMAX] — adjacent rungs only (nearest-neighbour,
                      assumption 5 kept).
           C[n,m]   = 0 for |n-m|>1.
      3. corridor-weight the matrix: C_w = D C D, D = diag(sqrt(w_n)).
         A corridor-occupying trajectory -> full-weight rungs; a trajectory
         with rungs out of band -> down-weighted rungs, diluted joint object.
      4. the joint Kish participation ratio, evaluated on the RUNG count R
         (NOT R*m — this is the dilution cure: the corridor-capped rungs are
         the constituents):
           k_eff_joint = (Tr C_w)^2 / Tr(C_w^2)
           rho_joint   = (R / k_eff_joint - 1) / (R - 1)        Kish inverse
      5. log w_omega = log smooth_band_indicator(rho_joint).

    Returns (log_w_omega, rho_joint, k_eff_joint) — all (K,) GPU arrays.

    NON-ADDITIVITY: rho_joint is a ratio of traces of ONE matrix C_w.
    Tr(C_w^2) = Sigma_{n,m} C_w[n,m]^2 mixes every rung pair (including the
    cross terms), and the Kish inverse is nonlinear in that sum. There is no
    Sigma_n (per-rung term) decomposition. C_w[n,n+1] depends on w_n, w_{n+1}
    AND rvia_n simultaneously — three trajectory facts entangled in one entry.
    """
    K, R = rtf.shape
    CMAX = float(RHO_UPPER)        # cross-rung entry capped at the band top
    # per-rung corridor weight (the within-rung corridor cap)
    w = soft(rtf, beta)                                  # (K, R)
    sw = cp.sqrt(cp.clip(w, 1e-12, 1.0))                 # (K, R) = diag(D)

    # build C_w as a (K, R, R) batched matrix
    C = cp.zeros((K, R, R), dtype=cp.float64)
    diag_idx = cp.arange(R)
    C[:, diag_idx, diag_idx] = 1.0
    if R > 1:
        # cross-rung adjacent entries from the trajectory timing coupling
        cross = CMAX * soft(rvia, beta)                  # (K, R-1) in [0, CMAX]
        n_idx = cp.arange(R - 1)
        C[:, n_idx, n_idx + 1] = cross
        C[:, n_idx + 1, n_idx] = cross
    # corridor-weight: C_w = D C D
    Cw = C * sw[:, :, None] * sw[:, None, :]             # (K, R, R)

    # joint Kish participation ratio on the RUNG count R
    trCw = cp.einsum('knn->k', Cw)                       # Tr C_w
    trCw2 = cp.einsum('knm,kmn->k', Cw, Cw)              # Tr(C_w^2)
    k_eff_joint = (trCw * trCw) / cp.clip(trCw2, 1e-300, None)
    rho_joint = (R / k_eff_joint - 1.0) / (R - 1.0) if R > 1 else cp.zeros(K)

    # smooth band indicator (R1's honest band — flat interior, two soft edges)
    sharp = 40.0
    rise = 1.0 / (1.0 + cp.exp(-sharp * (rho_joint - RHO_LOWER)))
    fall = 1.0 / (1.0 + cp.exp(-sharp * (RHO_UPPER - rho_joint)))
    e_omega = rise * fall
    log_w = cp.log(cp.clip(e_omega, 1e-300, None))
    return log_w, rho_joint, k_eff_joint


def collect_allemerged(R, n_hist, seed, beta):
    """Run R2's simulator in GPU chunks; keep, per all-emerged history:
    rtf (rho at t_f, per rung) and rvia (rho at successor-emergence, per bond).
    Returns (rtf, rvia) GPU arrays over the all-emerged sub-ensemble, plus
    n_hist and n_all_emerged."""
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
            rtf_sel = rho[rows, :, T - 1]                       # (k, R)
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


def analyse_depth(R, n_hist, beta, seed):
    """Build the construction at depth R and compute the three-hypothesis
    metrics. CUDA throughout."""
    rtf, rvia, n_hist, n_all = collect_allemerged(R, n_hist, seed, beta)
    if n_all < 200:
        return dict(R=R, n_hist=n_hist, n_all_emerged=n_all,
                    note="too few all-emerged histories for statistics")
    K = rtf.shape[0]

    # ---- the omega-weight on every all-emerged history --------------------
    log_w, rho_joint, k_eff_joint = joint_rho_history(rtf, rvia, beta)

    # H2 — DILUTION. does the joint effective dimensionality stay bounded, or
    # run to the chaos pole? report the joint rho/k_eff over the post-selected
    # ensemble and over the band-reachability extreme.
    # the post-selection weight:
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
    # band-reachability: does ANY all-emerged history clear the band?
    in_band = (rho_joint > RHO_LOWER) & (rho_joint < RHO_UPPER)
    frac_in_band = float(cp.mean(in_band.astype(cp.float64)))
    n_in_band = int(cp.sum(in_band))
    band_reachable = n_in_band > 0
    # H2 dilution diagnostic: rho_joint * R. R1's diluting functional had
    # rho_joint*K -> const (rho_joint ~ 4/K). If rho_joint*R is roughly
    # CONSTANT or falling, the rung-level functional dilutes too. If rho_joint
    # itself is stable / bounded away from 0, it does NOT dilute.
    rho_joint_times_R = rho_joint_max * R

    # H3 — selectivity & joint work. selective = the band is a narrow target.
    # acceptance fraction within e^-1 of the best weight.
    acc = (lw > top - 1.0)
    accept_frac = float(cp.mean(acc.astype(cp.float64)))
    # joint-work: turn the cross-rung entries OFF (set cross=0) and recompute.
    # if rho_joint is unchanged the functional is secretly per-rung -> trivial.
    log_w_off, rho_joint_off, _ = joint_rho_history(
        rtf, cp.full_like(rvia, 100.0), beta)   # rvia huge -> soft~0 -> cross 0
    cross_delta = float(cp.mean(cp.abs(rho_joint - rho_joint_off)))
    cross_delta_max = float(cp.max(cp.abs(rho_joint - rho_joint_off)))

    # ---- H1 — SEGMENT-SHUFFLE (the decisive non-decomposability test) ------
    # build a shuffled ensemble: draw each rung's t_f state and each bond's
    # via-state INDEPENDENTLY from the post-selected per-rung / per-bond
    # marginals, then recompute the omega-weight. if the joint functional
    # FACTORIZES, the shuffled ensemble reproduces the joint weight (gap ~ 0).
    # if it COUPLES, the real post-selected histories carry cross-rung
    # structure independent draws cannot reproduce (gap > 0), and — the H1
    # criterion — the gap GROWS with R.
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
    log_w_shuf, _, _ = joint_rho_history(rtf_shuf, rvia_shuf, beta)
    # the real post-selected ensemble: resample K histories with prob w_ps
    pick_real = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
    log_w_real = log_w[pick_real]
    mean_real = float(cp.mean(cp.where(cp.isfinite(log_w_real), log_w_real, -50.0)))
    mean_shuf = float(cp.mean(cp.where(cp.isfinite(log_w_shuf), log_w_shuf, -50.0)))
    shuffle_gap = mean_real - mean_shuf
    shuffle_gap_per_rung = shuffle_gap / R

    return dict(
        R=R, n_hist=n_hist, n_all_emerged=n_all, K=K, beta=beta,
        # H2 — dilution
        rho_joint_psmean=rho_joint_psmean,
        rho_joint_mean=rho_joint_mean,
        rho_joint_max=rho_joint_max,
        rho_joint_min=rho_joint_min,
        rho_joint_times_R_atmax=rho_joint_times_R,
        k_eff_joint_psmean=keff_joint_psmean,
        k_eff_joint_mean=keff_joint_mean,
        band_reachable=band_reachable,
        frac_in_band=frac_in_band,
        n_in_band=n_in_band,
        # H3 — joint work
        accept_frac=accept_frac,
        cross_delta_mean=cross_delta,
        cross_delta_max=cross_delta_max,
        # H1 — non-decomposability
        mean_logw_real=mean_real,
        mean_logw_shuffled=mean_shuf,
        shuffle_gap=shuffle_gap,
        shuffle_gap_per_rung=shuffle_gap_per_rung,
    )


def main():
    cp.random.seed(SEED)
    beta = 1.0 / (2.0 * W_HALF ** 2)         # framework-referenced sharpness
    log("=" * 74)
    log("P_omega — the R1 x R2 conjunction")
    log("  R1's joint Kish participation-ratio functional, carried on R2's")
    log("  open sequential history frame, within-rung corridor cap re-injected.")
    log(f"  corridor band ({RHO_LOWER}, {RHO_UPPER}); centre {RHO_MID}; "
        f"half-width {W_HALF}")
    log(f"  beta_pin = 1/2w^2 = {beta:.4f}")
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
            done_R = {r["R"] for r in results if "shuffle_gap" in r or "note" in r}
            if done_R:
                log(f"  RESUMING — depths {sorted(done_R)} already on disk, "
                    f"will be skipped.")
        except Exception as e:
            log(f"  (could not parse existing {RESULTS}: {e}; starting fresh)")
            results, done_R = [], set()

    t0 = time.time()
    for R in R_SCAN:
        if R in done_R:
            log(f"  R={R:2d}  already done — skipped (resume)")
            continue
        ts = time.time()
        res = analyse_depth(R, N_BY_R[R], beta, SEED + R * 7919)
        res["wall_s"] = time.time() - ts
        results.append(res)
        if "note" in res:
            log(f"  R={R:2d}  N={N_BY_R[R]:>9d}  {res['note']}  "
                f"({res['wall_s']:.1f}s)")
        else:
            log(f"  R={R:2d}  N={N_BY_R[R]:>9d}  K={res['K']:>7d}  "
                f"rho_joint(ps)={res['rho_joint_psmean']:.4f}  "
                f"max={res['rho_joint_max']:.4f}  "
                f"k_eff(ps)={res['k_eff_joint_psmean']:.3f}  "
                f"in-band={res['frac_in_band']:.4f}  "
                f"shuffle_gap={res['shuffle_gap']:.4f} "
                f"(per-rung {res['shuffle_gap_per_rung']:.4f})  "
                f"({res['wall_s']:.1f}s)")
        # ---- incremental flush AFTER EVERY depth --------------------------
        with open(RESULTS, "w") as f:
            json.dump(dict(
                meta=dict(
                    construction="R1xR2 conjunction",
                    seed=SEED, beta_pin=beta,
                    rho_lower=RHO_LOWER, rho_upper=RHO_UPPER,
                    rho_mid=RHO_MID, w_half=W_HALF,
                    functional=("rho_joint = Kish-inverse of the participation "
                                "ratio of the corridor-weighted R x R "
                                "rung-correlation matrix; constituents are the "
                                "R corridor-capped rungs, not R*m raw spins"),
                    elapsed_s=time.time() - t0),
                results=results,
            ), f, indent=2)
        log(f"      flushed -> {RESULTS}")

    log(f"\ndone, {time.time() - t0:.1f}s total. results -> {RESULTS}")


if __name__ == "__main__":
    main()

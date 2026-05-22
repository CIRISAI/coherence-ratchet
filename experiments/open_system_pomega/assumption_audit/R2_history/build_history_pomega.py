#!/usr/bin/env python3
"""
R2 — P_omega as a history-space object.

Assumption audit relaxation R2 (drops assumptions 4 and 8): P_omega is NOT a
static operator on a simultaneous all-rungs-at-once configuration space, and
omega is NOT "all rungs in corridor simultaneously". Instead P_omega is a TSVF
backward boundary condition on the universe's *history* — its trajectory
through rung-space over cosmic time, with each rung entering its corridor as it
emerges (Ph0 -> Ph1 -> ... -> A5).

Pre-registration: PREREGISTRATION.md (this directory), committed before this run.

THE MODEL
---------
A history is a trajectory over T discrete cosmic-time steps. The universe starts
(t_0, the forward state |psi>) in the chaos regime: no rungs instantiated, the
Big-Bang boundary of Piece 8. Rungs emerge SEQUENTIALLY (Piece 6). Rung n+1's
emergence is gated: it can emerge at step t only if rung n is currently in its
corridor band (the substrate-readiness gate — Piece 6's cross-rung condition in
trajectory form). Once emerged, rung n carries a within-rung correlation
rho_n(t) evolving by the framework's own dynamics drho/dt = alpha - gamma*M
(Piece 2): a spontaneous rigidity drift alpha, an active maintenance gamma*M.

The forward dynamics generates a path measure: each history is a draw of
(per-step maintenance M_n(t), emergence-gate timing). The backward state
<phi_omega| at t_f post-selects on the WHOLE trajectory:
  omega-condition  =  (all R rungs have emerged by t_f)
                 AND  (every emerged rung is in its corridor band AT t_f)
                 AND  (every rung was in its corridor band at the step its
                       successor emerged — sequential-emergence viability).
P_omega = the weight w(history) that this two-time boundary places on each
history. The post-selected ensemble is the reweighted set of histories.

This is a genuine TSVF object: forward state at t_0, backward post-selection at
t_f, the weight a functional on TRAJECTORIES (histories), not an operator on a
configuration space. It structurally cannot have additive shared-rung
simultaneous frustration — there is no simultaneous all-rungs config space.

THE DECISIVE TEST (committed in the pre-registration)
-----------------------------------------------------
Does the omega-boundary do genuine JOINT work on the trajectory, or does it
factorise over time-steps/rungs (trivial)?

  joint:        w_joint(history)  — the real two-time boundary above.
  factorised:   w_fact(history)   — post-select each rung's t_f state and each
                emergence event INDEPENDENTLY, as a product of per-rung /
                per-event marginals (the surrogate that assumes no temporal
                coupling).
  flat control: w_flat(history)   — post-select ONLY the endpoint (all rungs
                emerged + in band at t_f), with NO sequential-emergence /
                in-band-at-emergence requirement.

Genuine joint work  <=>  w_joint is strictly more selective than w_fact
(selectivity gap), the gap is R-stable or R-growing, and the flat control does
NOT reproduce the gap.

CUDA: histories sampled in GPU-parallel batches (cupy). Incremental output:
results flushed to results_history.json per trajectory length.
"""

import json
import sys
import time

import numpy as np

try:
    import cupy as cp
    xp = cp
    GPU = True
except Exception as e:  # pragma: no cover
    print(f"FATAL: cupy unavailable ({e}). R2 requires CUDA.", flush=True)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Framework constants — the genuine ones, not tuned.
# ---------------------------------------------------------------------------
RHO_LOWER = 0.10          # corridor lower bound (Piece 3)
RHO_UPPER = 0.43          # corridor upper bound (Piece 3, ccav3 anchor)
RHO_MID = 0.5 * (RHO_LOWER + RHO_UPPER)   # = 0.265, corridor centre
W_HALF = 0.5 * (RHO_UPPER - RHO_LOWER)    # = 0.165, corridor half-width

# Piece 6 emergence cadence: the post-Cambrian sub-sequence accelerates
# monotonically (A2->A3 540 Myr, A3->A4 310 kyr, A4->A5 6.7 kyr). The history
# model needs a cosmic-time grid; the framework gives RATIOS, not absolute
# steps. We use the framework's own monotone-acceleration structure: the
# inter-emergence interval shrinks geometrically. This is Piece 6's content,
# not a tuned knob — the ACCELERATION is the framework's; the geometric form is
# the minimal monotone-decreasing schedule consistent with it.
ACCEL_RATIO = 0.70        # each inter-rung interval is 0.70x the previous

SEED = 20260522

# ---------------------------------------------------------------------------
# dynamics: drho/dt = alpha(rho,S) - gamma*M(t)  (Piece 2)
# ---------------------------------------------------------------------------
# Piece 2, read faithfully:
#   alpha(rho,S) is the spontaneous correlation drift toward rigidity. At M=0,
#     rho drifts monotonically toward 1 -> alpha > 0 everywhere, growing with
#     rho (more correlation begets more): alpha(rho) = ALPHA0 + ALPHA_RHO*rho.
#   gamma*M(t) is the ACTIVE coherence-management work. Piece 2: "the corridor
#     is sustained only by non-trivial M(t)". "Active" and "management" mean
#     M(t) is RESPONSIVE — a managing system measures rho and applies effort.
#     A constant M cannot sustain a corridor (the rho* of constant M is an
#     UNSTABLE fixed point, since alpha grows with rho); the framework's own
#     wording ("active management", "work being done") is responsive control.
#
# So M(t) = M_base + KGAIN * (rho - rho_target): proportional management toward
# a target. The trajectory degree of freedom is the MANAGEMENT QUALITY of each
# history: its gain KGAIN and target rho_target, plus per-step management noise.
# A well-managed history (gain adequate, target in corridor, low noise) holds
# rho in the corridor; a poorly-managed one drifts to a pole. This is the
# framework's drho/dt = alpha - gamma*M with M the active term it names.
#
# The corridor band itself (0.10,0.43) and centre 0.265 are the framework's,
# NOT tuned. What the history model varies is management quality, drawn over a
# range wide enough that histories land at rigidity, chaos, AND corridor.
ALPHA0 = 0.020            # base rigidity drift per step
ALPHA_RHO = 0.025         # rho-dependence of the drift
GAMMA = 1.0
RHO_INIT_MEAN = 0.05      # rung emerges from chaos side
RHO_INIT_SD = 0.02
# management: M(t) = M_BASE + KGAIN*(rho - target). With responsive M, the
# closed-loop fixed point rho** solves alpha(rho) = M_BASE + KGAIN*(rho-target);
# it is STABLE when d/drho[alpha - M] = ALPHA_RHO - KGAIN < 0, i.e. KGAIN >
# ALPHA_RHO. Each history draws (KGAIN, target, noise) — its management quality.
KGAIN_MEAN = 0.12         # mean management gain (>> ALPHA_RHO -> stable control)
KGAIN_SD = 0.05           # spread in gain across histories
TARGET_MEAN = RHO_MID     # managers aim for corridor centre on average ...
TARGET_SD = 0.22          # ... but with wide spread -> some aim out of corridor
M_BASE = ALPHA0 + ALPHA_RHO * RHO_MID   # baseline effort at the corridor centre
M_NOISE_SD = 0.010        # per-step management execution noise


# cosmic-time grid: the minimum dwell a rung needs to climb chaos->corridor
# under the responsive dynamics, in steps. Each inter-emergence interval is at
# least this; the monotone-acceleration of Piece 6 is then applied on top, but
# bounded below by MIN_DWELL so every rung gets a real residence window.
MIN_DWELL = 8


def make_time_grid(R):
    """Cosmic-time grid: emergence steps with monotone-accelerating cadence
    (Piece 6). Returns (T_total, emergence_steps) — emergence_steps[n] is the
    EARLIEST step at which rung n is *allowed* to emerge (rung 0 at step 0).
    The actual emergence step of rung n in a given history is >= this, gated by
    rung n-1 being in corridor.

    Piece 6 gives RATIOS (the acceleration), not absolute steps. The intervals
    accelerate geometrically (ACCEL_RATIO) but are bounded below by MIN_DWELL —
    a rung needs a real residence window to climb chaos->corridor and to be a
    substrate-readiness gate for its successor. So early intervals are longer
    (acceleration) but no interval is unboundedly long: the schedule is the
    monotone-accelerating one, floored, not the raw geometric blow-up."""
    # geometric intervals, newest (last) = 1 unit, oldest longest
    raw = [ACCEL_RATIO ** (-(R - 2 - n)) for n in range(R - 1)] if R > 1 else []
    # normalise so the SMALLEST interval is MIN_DWELL steps, cap the largest
    if raw:
        mn = min(raw)
        steps = [min(int(round(iv / mn * MIN_DWELL)), 6 * MIN_DWELL)
                 for iv in raw]
    else:
        steps = []
    earliest = [0]
    for n in range(1, R):
        earliest.append(earliest[-1] + steps[n - 1])
    tail = MIN_DWELL + 6   # rungs must HOLD their corridor to t_f
    T_total = (earliest[-1] if earliest else 0) + tail
    return T_total, earliest


def simulate_histories(R, n_hist, batch_seed):
    """Forward-evolve n_hist histories of a universe with R rungs.

    Returns a dict of GPU arrays describing each history:
      rho[h, n, t]        within-rung correlation of rung n at step t (nan
                          before rung n emerges)
      emerge_step[h, n]   the step at which rung n emerged in history h
                          (-1 if it never emerged)
      n_emerged[h]        how many rungs emerged by t_f
    """
    rng = cp.random.RandomState(batch_seed)
    T_total, earliest = make_time_grid(R)
    earliest = cp.asarray(earliest, dtype=cp.int32)

    rho = cp.full((n_hist, R, T_total), cp.nan, dtype=cp.float64)
    emerge_step = cp.full((n_hist, R), -1, dtype=cp.int32)
    # rho_init for each rung in each history
    rho_init = (RHO_INIT_MEAN
                + RHO_INIT_SD * rng.standard_normal((n_hist, R), dtype=cp.float64))
    rho_init = cp.clip(rho_init, 0.01, 0.20)

    # --- management quality, the trajectory degree of freedom ---------------
    # each history has, per rung, a management gain KGAIN and target rho_target,
    # plus per-step execution noise. M(t) = M_BASE + KGAIN*(rho - target) + noise.
    # These vary across histories so trajectories land at rigidity / chaos /
    # corridor depending on management quality.
    kgain = cp.clip(KGAIN_MEAN + KGAIN_SD
                    * rng.standard_normal((n_hist, R), dtype=cp.float64),
                    0.0, 0.40)
    target = cp.clip(TARGET_MEAN + TARGET_SD
                     * rng.standard_normal((n_hist, R), dtype=cp.float64),
                     -0.30, 1.30)
    # m_noise drawn per-step inside the loop (avoids a (n_hist,R,T) array)

    in_band = lambda r: (r > RHO_LOWER) & (r < RHO_UPPER)

    # rung 0 emerges at step 0 in every history
    emerge_step[:, 0] = 0
    rho[:, 0, 0] = rho_init[:, 0]
    # alive[h,n]: rung n has emerged and is being evolved
    alive = cp.zeros((n_hist, R), dtype=cp.bool_)
    alive[:, 0] = True
    cur = cp.full((n_hist, R), cp.nan, dtype=cp.float64)
    cur[:, 0] = rho_init[:, 0]

    for t in range(1, T_total):
        # evolve every alive rung one step: drho = alpha(rho) - gamma*M
        #   alpha(rho) = ALPHA0 + ALPHA_RHO*rho  (rigidity drift)
        #   M(t)       = M_BASE + KGAIN*(rho - target) + noise  (active mgmt)
        a = ALPHA0 + ALPHA_RHO * cur
        m_noise_t = M_NOISE_SD * rng.standard_normal((n_hist, R),
                                                     dtype=cp.float64)
        M_t = M_BASE + kgain * (cur - target) + m_noise_t
        drho = a - GAMMA * M_t
        nxt = cur + drho
        nxt = cp.where(alive, cp.clip(nxt, 0.0, 1.0), cur)
        cur = nxt
        # write rho for alive rungs
        for_write = cp.where(alive, cur, cp.nan)
        rho[:, :, t] = for_write

        # emergence gate: rung n (n>=1) emerges at step t if
        #   - it has not yet emerged
        #   - t >= earliest[n]
        #   - rung n-1 is currently in its corridor band
        not_emerged = ~alive
        prev_idx = cp.arange(R) - 1
        prev_in_band = cp.zeros((n_hist, R), dtype=cp.bool_)
        for n in range(1, R):
            prev_in_band[:, n] = in_band(cur[:, n - 1]) & alive[:, n - 1]
        time_ok = (t >= earliest[None, :])
        can_emerge = not_emerged & time_ok & prev_in_band
        # only the LOWEST not-yet-emerged rung may emerge (sequential)
        # mask: rung n may emerge only if rungs 0..n-1 are all alive
        all_prev_alive = cp.ones((n_hist, R), dtype=cp.bool_)
        acc = cp.ones(n_hist, dtype=cp.bool_)
        for n in range(R):
            all_prev_alive[:, n] = acc
            acc = acc & alive[:, n]
        can_emerge = can_emerge & all_prev_alive
        # emerge
        emergers = can_emerge
        new_rho = cp.where(emergers, rho_init, cur)
        cur = cp.where(emergers, new_rho, cur)
        alive = alive | emergers
        es = cp.where(emergers, t, emerge_step)
        emerge_step = es.astype(cp.int32)
        rho[:, :, t] = cp.where(alive, cur, cp.nan)

    n_emerged = alive.sum(axis=1).astype(cp.int32)
    return dict(rho=rho, emerge_step=emerge_step, n_emerged=n_emerged,
                T_total=T_total, R=R)


def in_band_np(r):
    return (r > RHO_LOWER) & (r < RHO_UPPER)


# ---------------------------------------------------------------------------
# the three post-selection weights — the decisive test
# ---------------------------------------------------------------------------
def omega_weights(sim, beta):
    """Compute the three post-selection weights for every history.

    w_joint : the real two-time omega-boundary
        (a) all R rungs emerged by t_f
        (b) every rung in its corridor band AT t_f
        (c) every rung in its corridor band at the step its successor emerged
            (sequential-emergence viability — the non-local-in-time coupling)
    w_fact  : factorised surrogate — post-select each rung's t_f state and each
        emergence event INDEPENDENTLY (product of per-rung / per-event
        marginals). The surrogate a trivial history-object would be equal to.
    w_flat  : flat control — endpoint only: all emerged + in band at t_f, NO
        sequential / in-band-at-emergence requirement.

    Soft weights: each band-membership requirement contributes
    exp(-beta * (rho - RHO_MID)^2) so the weight is graded, not hard 0/1 (a
    genuine TSVF post-selection effect, faithful to the soft-P_omega program).
    The emergence-viability and emergence-event terms are scored on the rho the
    history actually had at the relevant step.
    """
    rho = sim["rho"]
    emerge_step = sim["emerge_step"]
    n_emerged = sim["n_emerged"]
    R = sim["R"]
    T = sim["T_total"]
    n_hist = rho.shape[0]

    def soft(r):  # graded band-membership weight
        return cp.exp(-beta * (r - RHO_MID) ** 2)

    rho_tf = rho[:, :, T - 1]            # (n_hist, R) state at t_f
    all_emerged = (n_emerged == R)

    # ---- (b) per-rung t_f band weight -------------------------------------
    tf_soft = soft(cp.nan_to_num(rho_tf, nan=2.0))   # nan -> huge penalty
    log_tf = cp.log(tf_soft + 1e-300).sum(axis=1)    # sum over rungs

    # ---- (c) sequential-emergence viability -------------------------------
    # for each rung n (n=0..R-2): the rho rung n HAD at the step its successor
    # n+1 emerged. This couples rung n's emergence time to rung n+1's.
    log_via = cp.zeros(n_hist, dtype=cp.float64)
    rows = cp.arange(n_hist)
    for n in range(R - 1):
        es_next = emerge_step[:, n + 1]              # step n+1 emerged
        es_next_c = cp.clip(es_next, 0, T - 1)
        rho_n_at = rho[rows, n, es_next_c]           # rung n's rho then
        valid = (es_next >= 0)
        rho_n_at = cp.where(valid, rho_n_at, 2.0)    # never-emerged -> penalty
        log_via += cp.log(soft(cp.nan_to_num(rho_n_at, nan=2.0)) + 1e-300)

    # joint weight: requires all three. emergence is a hard gate (a rung that
    # never emerged cannot be in band) — the soft part is the band memberships.
    log_joint = cp.where(all_emerged, log_tf + log_via, -1e300)

    # ---- factorised surrogate --------------------------------------------
    # post-select each rung's t_f state independently AND each emergence event
    # independently — but with the per-rung / per-event MARGINAL distributions,
    # i.e. drop the requirement that the SAME history satisfy them jointly in a
    # temporally-coupled way. Operationally: the factorised surrogate scores the
    # SAME per-rung tf term and per-event viability term, but evaluates the
    # viability term against the rung's OWN-rung MARGINAL emergence (its mean
    # emergence step) rather than the successor's actual emergence step in this
    # history. That removes the cross-rung temporal coupling: rung n is scored
    # at a fixed reference step, independent of when rung n+1 actually emerged.
    # The reference step is the per-rung mean emergence step over the ensemble.
    mean_es = cp.where(emerge_step >= 0, emerge_step, cp.nan)
    # per-rung ensemble-mean emergence step (the marginal)
    ref_step = cp.zeros(R, dtype=cp.int32)
    for n in range(R):
        col = mean_es[:, n]
        m = cp.nanmean(col)
        ref_step[n] = cp.clip(cp.nan_to_num(m, nan=T - 1), 0, T - 1).astype(cp.int32)
    log_via_fact = cp.zeros(n_hist, dtype=cp.float64)
    for n in range(R - 1):
        # rung n scored at the FIXED marginal reference step of rung n+1,
        # not the actual successor emergence step in THIS history.
        rs = int(ref_step[n + 1])
        rho_n_ref = rho[:, n, rs]
        rho_n_ref = cp.nan_to_num(rho_n_ref, nan=2.0)
        log_via_fact += cp.log(soft(rho_n_ref) + 1e-300)
    log_fact = cp.where(all_emerged, log_tf + log_via_fact, -1e300)

    # ---- flat control: endpoint only -------------------------------------
    log_flat = cp.where(all_emerged, log_tf, -1e300)

    return dict(log_joint=log_joint, log_fact=log_fact, log_flat=log_flat,
                all_emerged=all_emerged, rho_tf=rho_tf, emerge_step=emerge_step)


def analyse(R, n_hist, beta, base_seed, chunk=40_000):
    """Run the construction for R rungs and compute the verdict metrics.

    Histories are processed in GPU chunks (the (n_hist,R,T) rho array is the
    memory bottleneck); only the per-history log-weight vectors are kept."""
    lj_parts, lf_parts, lflat_parts, em_parts = [], [], [], []
    T_total = None
    done = 0
    cidx = 0
    while done < n_hist:
        this = min(chunk, n_hist - done)
        sim = simulate_histories(R, this, base_seed + 104729 * cidx)
        T_total = sim["T_total"]
        w = omega_weights(sim, beta)
        lj_parts.append(w["log_joint"])
        lf_parts.append(w["log_fact"])
        lflat_parts.append(w["log_flat"])
        em_parts.append(w["all_emerged"])
        del sim, w
        cp.get_default_memory_pool().free_all_blocks()
        done += this
        cidx += 1
    lj = cp.concatenate(lj_parts)
    lf = cp.concatenate(lf_parts)
    lflat = cp.concatenate(lflat_parts)
    all_em = cp.concatenate(em_parts)

    # --- non-empty: post-selection partition function Z = mean weight --------
    # work in log-space; subtract a common offset for numerical stability
    finite = lj > -1e200
    if int(finite.sum()) == 0:
        Z_joint = 0.0
        offset = 0.0
    else:
        offset = float(cp.max(lj[finite]))
        Z_joint = float(cp.mean(cp.exp(lj - offset))) * np.exp(offset)
    # acceptance fractions: fraction of histories with weight above a threshold
    # (the corridor is a narrow target — "accepted" = within e^-1 of the best).
    def accept_frac(logw):
        fin = logw > -1e200
        if int(fin.sum()) == 0:
            return 0.0, 0
        top = float(cp.max(logw[fin]))
        acc = (logw > top - 1.0)
        return float(cp.mean(acc.astype(cp.float64))), int(acc.sum())

    f_joint, n_joint = accept_frac(lj)
    f_fact, n_fact = accept_frac(lf)
    f_flat, n_flat = accept_frac(lflat)

    # --- non-factorisation: KL-style divergence between the joint post-selected
    #     path distribution and the factorised-surrogate path distribution -----
    # both are reweightings of the SAME prior ensemble; compare normalised
    # weights p_joint(h) and p_fact(h). KL(joint || fact) = sum p_j log(p_j/p_f).
    fin = (lj > -1e200) & (lf > -1e200)
    if int(fin.sum()) < 10:
        kl = 0.0
    else:
        ljf = lj[fin]
        lff = lf[fin]
        # normalise each to a probability distribution over the finite set
        # log-sum-exp via max-subtraction (cupy has no logaddexp.reduce)
        def logsumexp(v):
            m = cp.max(v)
            return m + cp.log(cp.sum(cp.exp(v - m)))
        ljf_n = ljf - logsumexp(ljf)
        lff_n = lff - logsumexp(lff)
        pj = cp.exp(ljf_n)
        kl = float(cp.sum(pj * (ljf_n - lff_n)))

    # --- selectivity vs flat: f_joint should be < 0.5 * f_flat ---------------
    selectivity_ratio = (f_joint / f_flat) if f_flat > 0 else float("nan")

    # --- the joint-work gap, compared against the flat control ---------------
    # joint-vs-fact log-weight gap (mean over accepted joint histories): how
    # much MORE selective the joint boundary is than the factorised surrogate.
    fin = (lj > -1e200) & (lf > -1e200)
    if int(fin.sum()) >= 10:
        # gap on the partition functions (log Z_joint - log Z_fact), a scalar
        offj = float(cp.max(lj[fin]))
        offf = float(cp.max(lf[fin]))
        logZj = float(cp.log(cp.mean(cp.exp(lj[fin] - offj)))) + offj
        logZf = float(cp.log(cp.mean(cp.exp(lf[fin] - offf)))) + offf
        joint_vs_fact_logZ = logZj - logZf
    else:
        joint_vs_fact_logZ = 0.0

    frac_all_emerged = float(cp.mean(all_em.astype(cp.float64)))
    n_all_emerged = int(all_em.sum())

    return dict(
        R=R, n_hist=n_hist, beta=beta, T_total=T_total,
        Z_joint=Z_joint, frac_all_emerged=frac_all_emerged,
        n_all_emerged=n_all_emerged,
        f_joint=f_joint, f_fact=f_fact, f_flat=f_flat,
        n_accept_joint=n_joint, n_accept_fact=n_fact, n_accept_flat=n_flat,
        selectivity_ratio=selectivity_ratio,
        kl_joint_fact=kl,
        joint_vs_fact_logZ=joint_vs_fact_logZ,
    )


def main():
    cp.random.seed(SEED)
    beta = 1.0 / (2.0 * W_HALF ** 2)   # beta_pin = 1/2w^2, framework-referenced
    print(f"R2 history-space P_omega construction", flush=True)
    print(f"  corridor band ({RHO_LOWER}, {RHO_UPPER}), centre {RHO_MID}, "
          f"half-width {W_HALF}", flush=True)
    print(f"  beta_pin = 1/2w^2 = {beta:.3f}", flush=True)
    print(f"  GPU: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}",
          flush=True)

    # N_HIST grows with R so the all-emerged sub-ensemble (the histories the
    # post-selection acts on) stays statistically adequate at every depth.
    R_list = [2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 20]
    N_BY_R = {2: 400_000, 3: 400_000, 4: 400_000, 5: 400_000, 6: 600_000,
              7: 800_000, 8: 1_000_000, 9: 1_600_000, 11: 4_000_000,
              13: 8_000_000, 20: 24_000_000}

    results = []
    out_path = "results_history.json"
    t0 = time.time()
    for R in R_list:
        ts = time.time()
        res = analyse(R, N_BY_R[R], beta, SEED + R * 7919)
        res["wall_s"] = time.time() - ts
        results.append(res)
        print(f"  R={R:2d}  N={N_BY_R[R]:>9d}  n_all_emerged={res['n_all_emerged']:>7d}  "
              f"Z_joint={res['Z_joint']:.3e}  "
              f"f_joint={res['f_joint']:.4f}  f_flat={res['f_flat']:.4f}  "
              f"sel={res['selectivity_ratio']:.3f}  "
              f"KL(j||f)={res['kl_joint_fact']:.3e}  "
              f"dlogZ={res['joint_vs_fact_logZ']:.3f}  "
              f"({res['wall_s']:.1f}s)", flush=True)
        # incremental flush
        with open(out_path, "w") as f:
            json.dump(dict(
                meta=dict(seed=SEED, beta_pin=beta, rho_lower=RHO_LOWER,
                          rho_upper=RHO_UPPER, rho_mid=RHO_MID, w_half=W_HALF,
                          accel_ratio=ACCEL_RATIO,
                          alpha0=ALPHA0, alpha_rho=ALPHA_RHO,
                          kgain_mean=KGAIN_MEAN, kgain_sd=KGAIN_SD,
                          target_mean=TARGET_MEAN, target_sd=TARGET_SD,
                          m_base=M_BASE, m_noise_sd=M_NOISE_SD,
                          elapsed_s=time.time() - t0),
                results=results,
            ), f, indent=2)

    print(f"\ndone, {time.time() - t0:.1f}s total. results -> {out_path}",
          flush=True)


if __name__ == "__main__":
    main()

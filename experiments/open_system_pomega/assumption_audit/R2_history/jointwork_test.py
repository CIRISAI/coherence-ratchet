#!/usr/bin/env python3
"""
R2 — the decisive joint-work test.

The main run (build_history_pomega.py) shows the joint omega-boundary is
non-empty and that KL(joint||factorised) grows with R. But KL growing with R
could be a TRIVIAL accumulation: R independent per-rung term-differences summed.
Genuine joint work requires the boundary to COUPLE the trajectory — to be
non-decomposable across rungs/time.

This script runs the pre-registration's decisive tests sharply, at R=9 (the
framework's nine rungs) and R=5, R=13:

  TEST A — flat-control reproduction. Does a FLAT boundary (endpoint only, no
    sequential-emergence / in-band-at-emergence requirement) reproduce the
    selectivity gap? If yes, the gap is not omega-specific (TRIVIAL).

  TEST B — additivity / coupling decomposition. The joint weight's viability
    term is sum_n log soft(rho_n at successor-emergence-step). The factorised
    surrogate replaces "successor emergence step" with a fixed marginal. If the
    joint-vs-fact difference is exactly the SUM of per-rung independent
    differences (each rung scored against its own successor's step, with no
    coupling to OTHER rungs' emergence times), the boundary factorises ->
    TRIVIAL. Genuine joint work: the per-rung viability term for rung n depends
    on rung n+1's emergence step, which depends on rung n's residence, ... a
    chain. Test: does FIXING one rung's emergence time change the optimal /
    typical emergence times of OTHER rungs in the post-selected ensemble?

  TEST C — segment-shuffle (the cleanest coupling test). Take the all-emerged
    histories. For the JOINT boundary, the post-selected ensemble weights each
    history by w_joint. Now SHUFFLE: build synthetic histories by drawing each
    rung's (emergence step, rho-trajectory) independently from the per-rung
    marginals of the post-selected ensemble. If the joint boundary FACTORISES,
    the shuffled ensemble has the same w_joint distribution as the real one. If
    the boundary COUPLES the trajectory, shuffling destroys the joint weight:
    the real post-selected histories have CORRELATED rung-emergence-timing that
    independent draws cannot reproduce. Quantified: log-weight of real vs
    shuffled post-selected histories.

CUDA throughout. Incremental output to results_jointwork.json.
"""

import json
import time

import numpy as np
import cupy as cp

import build_history_pomega as B

RHO_MID = B.RHO_MID
RHO_LOWER = B.RHO_LOWER
RHO_UPPER = B.RHO_UPPER
W_HALF = B.W_HALF
SEED = B.SEED


def soft(r, beta):
    return cp.exp(-beta * (cp.nan_to_num(r, nan=2.0) - RHO_MID) ** 2)


def run_R(R, n_hist, beta, seed, chunk=40_000):
    """Simulate, post-select on the joint omega-boundary, and run tests A/B/C
    on the all-emerged sub-ensemble."""
    # accumulate the all-emerged histories' rung-trajectories.
    # we keep, per all-emerged history: emerge_step[R], rho at t_f[R], and
    # rho-at-successor-emergence[R-1].
    es_all, rtf_all, rvia_all = [], [], []
    done, cidx = 0, 0
    while done < n_hist:
        this = min(chunk, n_hist - done)
        sim = B.simulate_histories(R, this, seed + 104729 * cidx)
        T = sim["T_total"]
        rho = sim["rho"]
        es = sim["emerge_step"]
        ne = sim["n_emerged"]
        allem = (ne == R)
        idx = cp.where(allem)[0]
        if idx.size > 0:
            rows = idx
            es_sel = es[rows]                      # (k, R)
            rtf_sel = rho[rows, :, T - 1]           # (k, R)
            # rho of rung n at the step rung n+1 emerged
            rvia = cp.empty((idx.size, R - 1), dtype=cp.float64)
            for n in range(R - 1):
                esn = cp.clip(es_sel[:, n + 1], 0, T - 1)
                rvia[:, n] = rho[rows, n, esn]
            es_all.append(cp.asnumpy(es_sel))
            rtf_all.append(cp.asnumpy(rtf_sel))
            rvia_all.append(cp.asnumpy(rvia))
        del sim, rho, es
        cp.get_default_memory_pool().free_all_blocks()
        done += this
        cidx += 1
        if cidx % 25 == 0 or done >= n_hist:
            print(f"    R={R:2d} sim {done:,}/{n_hist:,} "
                  f"({100 * done // n_hist}%)", flush=True)
    if not es_all:
        return dict(R=R, n_all_emerged=0, note="no all-emerged histories")
    es = cp.asarray(np.concatenate(es_all))        # (K, R)
    rtf = cp.asarray(np.concatenate(rtf_all))      # (K, R)
    rvia = cp.asarray(np.concatenate(rvia_all))    # (K, R-1)
    K = es.shape[0]

    # ---- joint boundary log-weight per all-emerged history -----------------
    # log w_joint = sum_n log soft(rho_tf_n) + sum_n log soft(rho_via_n)
    log_tf = cp.log(soft(rtf, beta) + 1e-300).sum(axis=1)
    log_via = cp.log(soft(rvia, beta) + 1e-300).sum(axis=1)
    log_joint = log_tf + log_via

    # ---- TEST A: flat control ---------------------------------------------
    # flat boundary = endpoint only (log_tf), NO viability term.
    log_flat = log_tf

    def accept_frac(lw):
        top = float(cp.max(lw))
        return float(cp.mean((lw > top - 1.0).astype(cp.float64)))

    fA_joint = accept_frac(log_joint)
    fA_flat = accept_frac(log_flat)
    # the flat control's own "joint vs fact": flat has no viability term, so it
    # is its own factorised surrogate -> a flat boundary CANNOT show a
    # joint-vs-fact gap. The test is whether the SELECTIVITY of joint over flat
    # is real: f_joint should be < f_flat (the viability term adds constraint).
    sel_joint_vs_flat = fA_joint / fA_flat if fA_flat > 0 else float("nan")

    # ---- TEST B: coupling — does the viability term factorise? -------------
    # Factorised surrogate: each rung n scored at a FIXED marginal reference
    # step for rung n+1 emergence. We already have rho_via_n = rho of rung n at
    # rung n+1's ACTUAL emergence step. The factorised version would use the
    # ensemble-mean emergence step. The KEY coupling question: in the
    # post-selected (joint-reweighted) ensemble, is rung n+1's emergence step
    # CORRELATED with rung n's residence quality? If the boundary couples the
    # trajectory, the post-selection induces correlations between adjacent
    # rungs' emergence times that are absent in the prior ensemble.
    #   measure: Pearson corr of adjacent emergence-step GAPS, prior vs
    #   joint-post-selected.
    w = cp.exp(log_joint - cp.max(log_joint))
    w = w / cp.sum(w)
    gaps = cp.diff(es.astype(cp.float64), axis=1)   # (K, R-1) inter-emergence gaps
    # prior correlation between adjacent gaps
    def wcorr(x, y, weight=None):
        if weight is None:
            weight = cp.ones(x.shape[0]) / x.shape[0]
        mx = cp.sum(weight * x); my = cp.sum(weight * y)
        cov = cp.sum(weight * (x - mx) * (y - my))
        vx = cp.sum(weight * (x - mx) ** 2); vy = cp.sum(weight * (y - my) ** 2)
        return float(cov / cp.sqrt(vx * vy + 1e-300))
    prior_corrs, post_corrs = [], []
    unif = cp.ones(K) / K
    for n in range(gaps.shape[1] - 1):
        prior_corrs.append(wcorr(gaps[:, n], gaps[:, n + 1], unif))
        post_corrs.append(wcorr(gaps[:, n], gaps[:, n + 1], w))
    prior_adj_corr = float(np.mean(prior_corrs)) if prior_corrs else 0.0
    post_adj_corr = float(np.mean(post_corrs)) if post_corrs else 0.0

    # ---- TEST C: segment-shuffle ------------------------------------------
    # build a SHUFFLED ensemble: for each rung, draw its (rho_tf, rho_via)
    # independently from the post-selected per-rung marginals. If the joint
    # boundary factorises, the shuffled ensemble has the same log_joint
    # distribution as the real post-selected ensemble. If it couples, the real
    # post-selected histories carry cross-rung correlation the shuffle destroys.
    # numpy RNG for the weighted index draws: numpy's choice(p=...) uses
    # inverse-CDF (O(K+size) memory); cupy's choice(p=...) builds an
    # (size x K) array and OOMs when both K and size are large.
    nrng = np.random.RandomState((seed + 777) % (2**32))
    # resample K histories from the post-selected ensemble per-rung independently
    nshuf = K
    log_joint_shuf = cp.zeros(nshuf, dtype=cp.float64)
    # sample indices per rung from the joint-weighted distribution
    wnp = cp.asnumpy(w).astype(np.float64)
    wnp = wnp / wnp.sum()
    for n in range(R):
        pick = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
        log_joint_shuf += cp.log(soft(rtf[pick, n], beta) + 1e-300)
    for n in range(R - 1):
        pick = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
        log_joint_shuf += cp.log(soft(rvia[pick, n], beta) + 1e-300)
    # compare the post-selected ensemble's log_joint to the shuffled one.
    # the post-selected ensemble: sample K histories with prob w.
    pick_real = cp.asarray(nrng.choice(K, size=nshuf, p=wnp))
    log_joint_real = log_joint[pick_real]
    mean_real = float(cp.mean(log_joint_real))
    mean_shuf = float(cp.mean(log_joint_shuf))
    # if factorised: mean_real ~ mean_shuf. if coupled: real > shuf (the real
    # post-selected histories are jointly better than independent draws).
    shuffle_gap = mean_real - mean_shuf
    # normalise by R so we can see if it is per-rung-constant (additive) or
    # genuinely growing
    shuffle_gap_per_rung = shuffle_gap / R

    return dict(
        R=R, n_hist=n_hist, n_all_emerged=K, beta=beta,
        fA_joint=fA_joint, fA_flat=fA_flat, sel_joint_vs_flat=sel_joint_vs_flat,
        prior_adj_gap_corr=prior_adj_corr, post_adj_gap_corr=post_adj_corr,
        mean_logjoint_real=mean_real, mean_logjoint_shuffled=mean_shuf,
        shuffle_gap=shuffle_gap, shuffle_gap_per_rung=shuffle_gap_per_rung,
    )


def main():
    cp.random.seed(SEED)
    beta = 1.0 / (2.0 * W_HALF ** 2)
    print(f"R2 joint-work test  beta_pin={beta:.3f}", flush=True)
    cases = [(5, 1_200_000), (9, 4_000_000), (13, 16_000_000)]
    results, done_R = [], set()
    try:
        with open("results_jointwork.json") as f:
            results = json.load(f).get("results", [])
        done_R = {r["R"] for r in results if "n_all_emerged" in r}
        if done_R:
            print(f"  resuming — R={sorted(done_R)} already on disk, skipping",
                  flush=True)
    except FileNotFoundError:
        pass
    t0 = time.time()
    for R, N in cases:
        if R in done_R:
            print(f"  R={R:2d}  already done — skipped", flush=True)
            continue
        ts = time.time()
        res = run_R(R, N, beta, SEED + R * 31, chunk=40_000)
        res["wall_s"] = time.time() - ts
        results.append(res)
        print(f"  R={R:2d} K={res['n_all_emerged']:>7d}  "
              f"sel(joint/flat)={res['sel_joint_vs_flat']:.3f}  "
              f"adj-gap-corr prior={res['prior_adj_gap_corr']:+.3f} "
              f"post={res['post_adj_gap_corr']:+.3f}  "
              f"shuffle_gap={res['shuffle_gap']:.3f} "
              f"(per-rung {res['shuffle_gap_per_rung']:.4f})  "
              f"({res['wall_s']:.1f}s)", flush=True)
        with open("results_jointwork.json", "w") as f:
            json.dump(dict(meta=dict(seed=SEED, beta_pin=beta,
                                     elapsed_s=time.time() - t0),
                           results=results), f, indent=2)
    print(f"done, {time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()

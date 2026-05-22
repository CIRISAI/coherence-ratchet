#!/usr/bin/env python3
"""F-11 k-body -- finite-sample bias control.

build_kbody_pomega.py found tau_R (the normalized R-body multi-information of
the corridor-occupancy indicators) rising mildly with R -- 0.0024 at R=9,
0.0504 at R=13 -- and II_R going negative at R=11. Plug-in entropy estimators
are positively biased for total correlation when the sample is small relative
to the 2^R pattern space. This control settles whether the apparent rise is
GENUINE k-body structure or estimator bias.

THE CONTROL. For each depth, recompute tau_R and the k=3 II on a SHUFFLED null:
every rung's occupancy column independently permuted across histories. This
destroys ALL cross-rung structure (pairwise and higher) while keeping every
single-rung marginal EXACT. If shuffled tau_R ~= measured tau_R, the measured
value is bias, not structure -- the genuine k-body invariant is zero.

CUDA throughout. Reuses build_kbody_pomega's estimators and the R2 simulator.
"""
import json
import os
import sys
import time

import numpy as np
import cupy as cp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_kbody_pomega as K  # noqa: E402

B = K.B
RHO_LOWER, RHO_UPPER = K.RHO_LOWER, K.RHO_UPPER
DEPTHS = [3, 5, 7, 9, 11, 13]
N_HIST = 4_000_000
N_SHUFFLE = 8                     # shuffled-null replicates per depth
RESULT = os.path.join(HERE, "results_kbody_bias.json")


def occ_for_depth(R):
    """Pooled all-emerged corridor-occupancy array, batched (OOM-safe)."""
    Tt, _ = B.make_time_grid(R)
    nb_cap = max(20_000, int(6e9 / (R * Tt * 8)))
    batches = []
    n_done = 0
    seed0 = 20260522 + R * 1000          # SAME seed as build_kbody_pomega
    while n_done < N_HIST:
        nb = min(K.HIST_BATCH, nb_cap, N_HIST - n_done)
        sim = B.simulate_histories(R, nb, batch_seed=seed0 + n_done)
        Tt2 = sim["T_total"]
        rho_tf = sim["rho"][:, :, Tt2 - 1]
        ae = (sim["n_emerged"] == R)
        batches.append(rho_tf[ae].copy())
        n_done += nb
        del sim, rho_tf, ae
        cp.get_default_memory_pool().free_all_blocks()
    rho_e = cp.concatenate(batches, axis=0)
    return (rho_e > RHO_LOWER) & (rho_e < RHO_UPPER)


def main():
    print("=" * 70, flush=True)
    print("F-11 k-body -- finite-sample bias control (shuffled null)", flush=True)
    print("=" * 70, flush=True)
    out = {}
    if os.path.exists(RESULT):
        out = json.load(open(RESULT))
    for R in DEPTHS:
        if str(R) in out:
            print(f"  R={R}: on disk, skip", flush=True)
            continue
        t0 = time.time()
        occ = occ_for_depth(R)
        n_all = occ.shape[0]
        # measured
        tau_meas = K.kbody_tau(occ, list(range(R)))
        ii3_meas = K.interaction_information(occ, [0, 1, 2])
        # shuffled null: independently permute every rung column
        rng = cp.random.RandomState(99 + R)
        tau_sh, ii3_sh = [], []
        for s in range(N_SHUFFLE):
            occ_sh = cp.empty_like(occ)
            for n in range(R):
                occ_sh[:, n] = occ[rng.permutation(n_all), n]
            tau_sh.append(K.kbody_tau(occ_sh, list(range(R))))
            ii3_sh.append(K.interaction_information(occ_sh, [0, 1, 2]))
        out[str(R)] = dict(
            n_all=n_all,
            tau_measured=tau_meas,
            tau_shuffled_mean=float(np.mean(tau_sh)),
            tau_shuffled_sd=float(np.std(tau_sh)),
            ii3_measured=ii3_meas,
            ii3_shuffled_mean=float(np.mean(ii3_sh)),
            ii3_shuffled_sd=float(np.std(ii3_sh)),
            runtime_s=round(time.time() - t0, 1),
        )
        json.dump(out, open(RESULT, "w"), indent=2)
        d = out[str(R)]
        excess = d["tau_measured"] - d["tau_shuffled_mean"]
        print(f"  R={R:>2} n={n_all:>8}  tau_meas={tau_meas:.5f}  "
              f"tau_shuf={d['tau_shuffled_mean']:.5f}"
              f"+-{d['tau_shuffled_sd']:.5f}  "
              f"EXCESS={excess:+.5f}  ({d['runtime_s']}s)", flush=True)
    print("=" * 70, flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()

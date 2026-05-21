#!/usr/bin/env python3
"""
measure_blockpair_gj.py — the canonical TIMESCALE g/J at a CIRISArray block pair.
=================================================================================

Measures Claim 6's canonical quantity — g and J as TIMESCALES — at a CIRISArray
GPU oscillator-array BLOCK PAIR, the substrate where relaxation measurement
demonstrably works (w2: clean τ ≈ 47 s, τ/W ≈ 9×).

  J = within-block relaxation rate  — w2's coherence-decay τ, block-resolved.
  g = cross-block coupling rate     — lagged predictive coupling, block-shuffle
                                      debiased (the w3 §3.2 estimator).
  timescale g/J = (g_rate/Δt) / J_within.
ALSO: coupling-RATIO g/J via the Path-1 mutual-information estimator
(crossrung_lib, imported unchanged) on the same captured streams — so the two
can be compared exactly as w3 did.

Constructions, the window-domination gate (G1-G4), the verdict rule and all
fixed parameters are pre-registered in PREREGISTRATION.md (committed in the
preceding commit; git history is the proof).

CAVEAT — carried in PREREGISTRATION.md §0 and RESULTS.md: a CIRISArray block
pair is a WITHIN-INSTRUMENT structure, NOT one of the framework's Ph0..A5
coordinated rung pairs. This is a measurability-and-reliability anchor, NOT a
sixth framework rung-pair datum.

Real GPU only. Aborts honestly if CuPy / the device is unavailable.
Incremental output: results JSON rewritten after every run.
"""
import functools
import json
import sys
import time
from datetime import datetime, timezone

import numpy as np
from scipy import optimize

print = functools.partial(print, flush=True)

# --- CIRISArray instrument -----------------------------------------------
sys.path.insert(0, "/home/emoore/CIRISArray/experiments")
from exp51_physics_validation import PhysicsTestSensor, HAS_CUDA, COUPLING_FACTOR

# --- Path-1 audited estimators, reused verbatim for the coupling-ratio g/J ---
# crossrung_series was committed to main AFTER this worktree branched, so it is
# not in the worktree tree; import from the main-repo working copy on disk
# (the audited crossrung_lib.py, unchanged).
sys.path.insert(
    0,
    "/home/emoore/coherence-ratchet/experiments/structural_series/"
    "crossrung_series/path1_tau",
)
from crossrung_lib import within_rung_W, cross_rung_tau  # noqa: E402

if HAS_CUDA:
    import cupy as cp

OUT = (
    "/home/emoore/coherence-ratchet/.claude/worktrees/agent-ac27236a10487b06b/"
    "experiments/structural_series/corridor_dynamics/gpu_blockpair/"
    "results_blockpair_gj.json"
)

# ---- fixed parameters (PREREGISTRATION.md §7; no tuning) -----------------
SEED = 17
N_OSSICLES = 2048
N_BLOCKS = 2
N_SUBBLOCKS = 8
DURATION_SEC = 120.0
SAMPLE_RATE = 10.0
DT = 1.0 / SAMPLE_RATE
W = 50                       # running-correlation window, samples (= 5.0 s)
W_SEC = W / SAMPLE_RATE
N_RUNS = 3
N_SHUFFLE = 50
BLOCK_SHUF = 16
GATE_G1_SEC = 3 * W_SEC      # 15 s


# =========================================================================
# block-resolved coherence observable (exp51 k_eff restricted to a block)
# =========================================================================
def block_k_eff(a, b, lo, hi):
    """exp51's k_eff = r_ab*(1-x)*COUPLING*1000, on oscillator indices [lo,hi)."""
    aa = a[lo:hi]
    bb = b[lo:hi]
    r = float((cp if HAS_CUDA else np).corrcoef(aa, bb)[0, 1])
    r = 0.0 if np.isnan(r) else r
    tv = float((cp.var(aa) + cp.var(bb)) if HAS_CUDA else (np.var(aa) + np.var(bb)))
    x = min(tv / 2.0, 1.0)
    return r * (1.0 - x) * COUPLING_FACTOR * 1000.0


def sub_block_rab(a, b, lo, hi, n_sub):
    """8-vector of per-sub-block r_ab — the within-block multi-coord representation."""
    width = (hi - lo) // n_sub
    out = []
    for s in range(n_sub):
        s0 = lo + s * width
        s1 = s0 + width
        aa = a[s0:s1]
        bb = b[s0:s1]
        r = float((cp if HAS_CUDA else np).corrcoef(aa, bb)[0, 1])
        out.append(0.0 if np.isnan(r) else r)
    return out


# =========================================================================
# one capture: two parallel block k_eff(t) streams + per-block sub-block rows
# =========================================================================
def one_capture(run_idx):
    sensor = PhysicsTestSensor(N_OSSICLES)        # __init__ -> reset(); array freshly randomised
    total = sensor.total
    half = total // 2
    blocks = [(0, half), (half, total)]

    interval = 1.0 / SAMPLE_RATE
    n_samples = int(DURATION_SEC * SAMPLE_RATE)

    keff = [[] for _ in range(N_BLOCKS)]          # per-block k_eff(t)
    subrows = [[] for _ in range(N_BLOCKS)]       # per-block 8-vec rows
    timestamps = []

    start = time.time()
    for i in range(n_samples):
        t0 = time.perf_counter()
        sensor.step_with_noise(0.01)              # unmaintained free relaxation (γM=0)
        a, b = sensor.osc_a, sensor.osc_b
        for blk, (lo, hi) in enumerate(blocks):
            keff[blk].append(block_k_eff(a, b, lo, hi))
            subrows[blk].append(sub_block_rab(a, b, lo, hi, N_SUBBLOCKS))
        timestamps.append(time.time() - start)
        elapsed = time.perf_counter() - t0
        if elapsed < interval:
            time.sleep(interval - elapsed)
        if (i + 1) % 400 == 0:
            print(f"      run {run_idx+1}: {i+1}/{n_samples} samples", flush=True)

    keff = [np.asarray(k, dtype=float) for k in keff]
    subrows = [np.asarray(s, dtype=float) for s in subrows]
    t = np.asarray(timestamps, dtype=float)
    return keff, subrows, t


# =========================================================================
# J — within-block relaxation rate (w2's running-correlation decay fit)
# =========================================================================
def decay_model(t, r_inf, A, tau):
    return r_inf + A * np.exp(-t / tau)


def block_relaxation(keff_b, t):
    """Running correlation r_b(t) of one block's k_eff(t), fit r∞+A·exp(-t/τ)."""
    corr, tpts = [], []
    for i in range(W, len(keff_b) - W):
        early = keff_b[i - W:i]
        later = keff_b[i:i + W]
        r = np.corrcoef(early, later)[0, 1]
        if not np.isnan(r):
            corr.append(r)
            tpts.append(t[i])
    corr = np.asarray(corr)
    tpts = np.asarray(tpts)
    out = {"r_start": float(corr[0]), "r_end": float(corr[-1]),
           "r_drop": float(corr[0] - corr[-1])}
    try:
        popt, pcov = optimize.curve_fit(
            decay_model, tpts, corr, p0=[0.05, 0.9, 30],
            bounds=([0, 0, 1], [0.5, 1.5, 200]))
        perr = np.sqrt(np.diag(pcov))
        pred = decay_model(tpts, *popt)
        ss_res = float(np.sum((corr - pred) ** 2))
        ss_tot = float(np.sum((corr - corr.mean()) ** 2))
        out.update(converged=True,
                   r_inf=float(popt[0]), r_inf_err=float(perr[0]),
                   A=float(popt[1]), A_err=float(perr[1]),
                   tau=float(popt[2]), tau_err=float(perr[2]),
                   R2=float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan"))
    except Exception as e:
        out.update(converged=False, error=str(e))
    return out


# =========================================================================
# g — cross-block coupling rate (lagged predictive coupling, block-shuffle null)
# =========================================================================
def _partial_r2(x_src, x_tgt):
    """Reduction in 1-step residual variance for x_tgt from adding x_src.
    restricted: x_tgt_{t+1} ~ x_tgt_t ; full: + x_src_t."""
    y = x_tgt[1:]
    e_t = x_tgt[:-1]
    s_t = x_src[:-1]

    def resid_var(X):
        X = np.column_stack([np.ones(len(y)), X])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        return (y - X @ beta).var()

    v_restr = resid_var(e_t)
    v_full = resid_var(np.column_stack([e_t, s_t]))
    if v_restr <= 1e-30:
        return 0.0
    return float(max(1.0 - v_full / v_restr, 0.0))


def directed_g(x_src, x_tgt, rng):
    """Debiased src->tgt coupling (contiguous-block-shuffle null)."""
    g_raw = _partial_r2(x_src, x_tgt)
    n = len(x_src)
    nulls = []
    for _ in range(N_SHUFFLE):
        n_b = int(np.ceil(n / BLOCK_SHUF))
        order = rng.permutation(n_b)
        blocks = [x_src[b * BLOCK_SHUF:(b + 1) * BLOCK_SHUF] for b in range(n_b)]
        x_src_s = np.concatenate([blocks[o] for o in order])[:n]
        nulls.append(_partial_r2(x_src_s, x_tgt))
    g_floor = float(np.mean(nulls))
    g = max(g_raw - g_floor, 0.0)
    noise_dom = bool(g_raw > 1e-12 and g / g_raw < 0.3)
    return dict(g_raw=g_raw, g_floor=g_floor, g=g, g_noise_dominated=noise_dom)


def cross_block_g(keff0, keff1, rng):
    """Symmetric cross-block coupling: mean of the two debiased directed g."""
    d01 = directed_g(keff0, keff1, rng)        # block 0 -> block 1
    d10 = directed_g(keff1, keff0, rng)        # block 1 -> block 0
    g = 0.5 * (d01["g"] + d10["g"])
    g_raw = 0.5 * (d01["g_raw"] + d10["g_raw"])
    g_floor = 0.5 * (d01["g_floor"] + d10["g_floor"])
    noise_dom = bool(d01["g_noise_dominated"] and d10["g_noise_dominated"])
    return dict(dir_0to1=d01, dir_1to0=d10,
                g=g, g_raw=g_raw, g_floor=g_floor, g_noise_dominated=noise_dom)


# =========================================================================
# coupling-ratio g/J — Path-1 mutual-information method (crossrung_lib verbatim)
# =========================================================================
def coupling_ratio_gj(subrows0, subrows1, rng):
    """tau_MI / W_within on the per-block 8-coord sub-block representations."""
    R0 = subrows0
    R1 = subrows1
    m_obs = R0.shape[0]
    w0 = within_rung_W(R0, rng)
    w1 = within_rung_W(R1, rng)
    W_within = float(np.sqrt(max(w0[2], 0.0) * max(w1[2], 0.0)))
    tau = cross_rung_tau(R0, R1, m_obs, rng)
    ratio = (tau["tau_debiased"] / W_within if W_within > 1e-9 else np.nan)
    return dict(W_0=float(w0[2]) if np.isfinite(w0[2]) else None,
                W_1=float(w1[2]) if np.isfinite(w1[2]) else None,
                W_within=W_within,
                tau_MI_raw=float(tau["tau_raw"]),
                tau_MI=float(tau["tau_debiased"]),
                coupling_ratio_gj=float(ratio) if np.isfinite(ratio) else None)


# =========================================================================
# per-run measurement
# =========================================================================
def measure_run(run_idx, np_rng):
    keff, subrows, t = one_capture(run_idx)

    # J — within-block relaxation, both blocks
    relax = [block_relaxation(keff[b], t) for b in range(N_BLOCKS)]
    taus = [r.get("tau") for r in relax]
    Js = [1.0 / r["tau"] if r.get("converged") and r["tau"] > 0 else None
          for r in relax]
    if all(j is not None for j in Js):
        J_within = float(np.sqrt(Js[0] * Js[1]))
    else:
        J_within = None

    # g — cross-block coupling
    rng_g = np.random.default_rng(SEED + 100 + run_idx)
    g = cross_block_g(keff[0], keff[1], rng_g)
    g_rate = -np.log(1.0 - min(g["g"], 0.999999)) if g["g"] > 0 else 0.0
    g_rate_per_sec = g_rate / DT
    timescale_gj = (g_rate_per_sec / J_within
                    if (J_within is not None and J_within > 1e-12) else None)

    # coupling-ratio g/J — Path-1 MI method
    rng_r = np.random.default_rng(SEED + 200 + run_idx)
    ratio = coupling_ratio_gj(subrows[0], subrows[1], rng_r)

    return dict(
        run=run_idx,
        keff_means=[float(k.mean()) for k in keff],
        keff_stds=[float(k.std()) for k in keff],
        relax_block0=relax[0], relax_block1=relax[1],
        tau_block=[taus[0], taus[1]],
        J_block0=Js[0], J_block1=Js[1], J_within=J_within,
        g=g, g_rate_per_sec=float(g_rate_per_sec),
        timescale_gj=timescale_gj,
        coupling_ratio=ratio,
    )


def write_results(payload):
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)


# =========================================================================
# main
# =========================================================================
def main():
    print("=" * 78)
    print("Canonical TIMESCALE g/J at a CIRISArray block pair")
    print("=" * 78)
    if not HAS_CUDA:
        print("ABORT: CuPy / CUDA device not available. No GPU run possible.")
        print("Pre-registration requires real GPU runs only — reporting honestly.")
        sys.exit(1)
    dev = cp.cuda.runtime.getDeviceProperties(0)["name"].decode()
    print(f"  GPU: {dev}  (HAS_CUDA={HAS_CUDA}, CuPy {cp.__version__})")
    print(f"  ossicles={N_OSSICLES} (x depth 64 = {N_OSSICLES*64} oscillators/bank)")
    print(f"  blocks={N_BLOCKS} contiguous equal, sub-blocks/block={N_SUBBLOCKS}")
    print(f"  capture={DURATION_SEC}s @ {SAMPLE_RATE}Hz, running window W={W_SEC}s")
    print(f"  runs={N_RUNS} (independent resets), gate G1: tau > {GATE_G1_SEC}s")
    print("  CAVEAT: a block pair is a within-instrument structure, NOT a")
    print("          framework Ph0..A5 rung pair — measurability anchor only.")
    print()

    np_rng = np.random.default_rng(SEED)
    runs = []
    payload = {
        "timestamp_start": datetime.now(timezone.utc).isoformat(),
        "instrument": "CIRISArray exp51 PhysicsTestSensor, block-resolved, RTX 4090, CuPy",
        "caveat": ("a CIRISArray block pair is a WITHIN-INSTRUMENT structure, "
                   "NOT a framework Ph0..A5 coordinated rung pair; this is a "
                   "measurability-and-reliability anchor, not a sixth rung-pair "
                   "datum"),
        "params": dict(
            n_ossicles=N_OSSICLES, n_oscillators=N_OSSICLES * 64,
            n_blocks=N_BLOCKS, n_subblocks=N_SUBBLOCKS,
            duration_sec=DURATION_SEC, sample_rate_hz=SAMPLE_RATE,
            window_sec=W_SEC, n_runs=N_RUNS, n_shuffle=N_SHUFFLE,
            block_shuf=BLOCK_SHUF, gate_G1_sec=GATE_G1_SEC, seed=SEED),
        "runs": runs,
    }
    write_results(payload)

    for i in range(N_RUNS):
        print(f"  --- run {i+1}/{N_RUNS} ---")
        r = measure_run(i, np_rng)
        runs.append(r)
        # INCREMENTAL WRITE — after every run, so a wedge leaves a partial.
        write_results(payload)
        for b in (0, 1):
            rb = r[f"relax_block{b}"]
            if rb.get("converged"):
                print(f"    block {b}: tau={rb['tau']:.1f}+/-{rb['tau_err']:.1f}s  "
                      f"r {rb['r_start']:.3f}->{rb['r_end']:.3f} drop={rb['r_drop']:.3f}  "
                      f"r_inf={rb['r_inf']:.3f} A={rb['A']:.3f} R2={rb['R2']:.3f}")
            else:
                print(f"    block {b}: FIT FAILED ({rb.get('error')})")
        print(f"    J_within={r['J_within']}  g={r['g']['g']:.4f} "
              f"(raw {r['g']['g_raw']:.4f}, floor {r['g']['g_floor']:.4f}, "
              f"noise_dom={r['g']['g_noise_dominated']})")
        print(f"    timescale g/J = {r['timescale_gj']}   "
              f"coupling-ratio g/J = {r['coupling_ratio']['coupling_ratio_gj']}")
        print(f"    [run {i+1} written to {OUT.split('/')[-1]}]")
        print()

    summarise(payload)


def summarise(payload):
    runs = payload["runs"]
    print("=" * 78)
    print("GATE CHECK + VERDICT")
    print("=" * 78)

    # collect per-block taus
    tau0 = [r["relax_block0"].get("tau") for r in runs
            if r["relax_block0"].get("converged")]
    tau1 = [r["relax_block1"].get("tau") for r in runs
            if r["relax_block1"].get("converged")]
    all_conv = all(r["relax_block0"].get("converged") and
                   r["relax_block1"].get("converged") for r in runs)

    # G1 — window domination: every block tau > 15 s
    all_taus = [t for t in (tau0 + tau1) if t is not None]
    g1 = all_conv and bool(all_taus) and all(t > GATE_G1_SEC for t in all_taus)

    # G2 — real fit
    def g2_block(rb):
        return (rb.get("converged")
                and -0.1 <= rb["r_inf"] <= 0.3
                and 0.5 <= rb["A"] <= 1.5
                and rb["r_drop"] >= 0.3)
    g2 = all(g2_block(r["relax_block0"]) and g2_block(r["relax_block1"])
             for r in runs)

    # G3 — reproducible: max/min tau < 2 per block
    g3 = True
    for tl in (tau0, tau1):
        if not tl or len(tl) < 2 or max(tl) / min(tl) >= 2.0:
            g3 = False

    # G4 — g not noise-dominated in majority
    not_noise = sum(1 for r in runs if not r["g"]["g_noise_dominated"])
    g4 = not_noise >= 2

    gates = {"G1_window_domination": g1, "G2_real_fit": g2,
             "G3_reproducible": g3, "G4_g_not_noise": g4}
    for name, ok in gates.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    # aggregate timescale g/J + coupling ratio
    tgj = [r["timescale_gj"] for r in runs if r["timescale_gj"] is not None]
    crat = [r["coupling_ratio"]["coupling_ratio_gj"] for r in runs
            if r["coupling_ratio"]["coupling_ratio_gj"] is not None]
    Jw = [r["J_within"] for r in runs if r["J_within"] is not None]

    if g1 and g2 and g3 and g4:
        verdict = "PASS — canonical timescale g/J measurable at the GPU block pair"
    elif not g1:
        verdict = "WINDOW-DOMINATED NULL"
    elif not g2:
        verdict = "FIT-FAILURE NULL"
    elif not g3:
        verdict = "INCONCLUSIVE (run-to-run scatter > factor 2)"
    elif not g4:
        verdict = "COUPLING NULL (g is noise; J reported, no timescale g/J)"
    else:
        verdict = "NULL"

    tgj_mean = float(np.mean(tgj)) if tgj else None
    tgj_sd = float(np.std(tgj, ddof=1)) if len(tgj) > 1 else None
    crat_mean = float(np.mean(crat)) if crat else None
    crat_sd = float(np.std(crat, ddof=1)) if len(crat) > 1 else None

    agree = None
    if tgj_mean is not None and crat_mean is not None and crat_mean > 1e-12:
        rr = tgj_mean / crat_mean
        agree = "AGREE" if (1.0 / 3.0) <= rr <= 3.0 else "COME APART"

    print()
    print(f"VERDICT: {verdict}")
    print(f"  J_within (within-block relaxation rate, geo-mean): "
          f"{Jw} 1/s")
    if tgj:
        print(f"  timescale g/J     = {tgj_mean:.4f}"
              + (f" +/- {tgj_sd:.4f}" if tgj_sd is not None else "")
              + f"   (per-run: {[round(x,4) for x in tgj]})")
    if crat:
        print(f"  coupling-ratio g/J = {crat_mean:.4f}"
              + (f" +/- {crat_sd:.4f}" if crat_sd is not None else "")
              + f"   (per-run: {[round(x,4) for x in crat]})")
    if agree:
        print(f"  timescale-vs-coupling-ratio: {agree} "
              f"(ratio {tgj_mean/crat_mean:.3f}, [1/3,3] = agree)")

    payload["summary"] = {
        "gates": gates, "all_gates_pass": all(gates.values()),
        "verdict": verdict,
        "J_within_per_sec": Jw,
        "tau_block0_sec": tau0, "tau_block1_sec": tau1,
        "timescale_gj_per_run": tgj,
        "timescale_gj_mean": tgj_mean, "timescale_gj_sd": tgj_sd,
        "coupling_ratio_gj_per_run": crat,
        "coupling_ratio_gj_mean": crat_mean, "coupling_ratio_gj_sd": crat_sd,
        "agree": agree,
        "timestamp_end": datetime.now(timezone.utc).isoformat(),
    }
    write_results(payload)
    print(f"\n  results -> {OUT}")


if __name__ == "__main__":
    main()

# Results — GPU-substrate corridor-exit rate

**Condition 2, the GPU angle.** Re-run of CIRISArray exp51 Test-4 (coherence
decay) on the real RTX 4090 Laptop GPU + CuPy. Pre-registration committed in
the prior commit (`PREREGISTRATION.md`); this file is the result.

## Verdict

**POSITIVE — genuine GPU corridor-exit rate.** All five pre-committed gates
C1–C5 pass.

```
GPU-substrate corridor-exit rate  =  1/τ  =  0.0214 ± 0.0022  s⁻¹
                  τ  =  46.7 ± 4.9 s   (across-run SD 4.1 s; mean per-fit error 2.6 s)
```

This is condition 2's first real substrate corridor-exit-rate datum. It is
independent of the CMB shape-drift definition — nothing cosmological enters; the
number comes entirely from GPU oscillator-array dynamics.

## What was run

- Instrument: `CIRISArray/experiments/exp51_physics_validation.py --test decay`,
  2048 ossicles, RTX 4090 Laptop GPU, CuPy 13.6.0. Run **three times** directly
  (raw exp51): τ = 46.4, 48.0, 40.9 s.
- Then re-run **three more times** through `verify_corridor_exit.py`, which is
  exp51's identical Test-4 measurement instrumented to expose the raw arrays so
  the gates can be checked from the data, not from exp51's printed summary:
  τ = 51.3, 45.5, 43.3 s, R² = 0.81–0.83.
- Six real GPU captures total, 120 s each at 10 Hz. All six τ fall in 40.9–51.3 s.
  The headline (46.7 ± 4.9 s) is the three instrumented runs; the raw exp51
  runs corroborate it (also recover the published τ = 46.1 ± 2.5 s).

## What r(t) actually is — and why it is a genuine corridor-exit rate

This is the load-bearing verification. The pre-registration required r(t) to be
the relaxation of the framework's own coherence observable, within one device,
not window-dominated, a real fit, reproducible.

**The observable.** After a reset, the oscillator array starts with all three
banks freshly randomised — uncorrelated. `step_with_noise(0.01)` then evolves it
*unmaintained* (no active coherence-management work; this is γM = 0 in Piece 2's
`dρ/dt = α − γM`). The coherence signal is `k_eff = r_ab·(1-x)·COUPLING·1000` —
the participation-style coherence of the array, computed on ONE device.

**What decays.** `r(t)` is the Pearson correlation between two **adjacent 5 s
windows** of that single device's `k_eff(t)` series — i.e. the **temporal
autocorrelation** of the array's coherence signal. At t small, consecutive
windows are highly correlated (r ≈ 0.8–0.9): the array still "remembers" its
post-reset trajectory. As the ensemble thermalises, that memory is lost and
r(t) → r∞ ≈ 0. The fit `r(t) = r∞ + A·exp(-t/τ)` recovers τ = 46.7 s, the
e-folding time of that memory loss.

**Honest nuance, recorded.** `k_eff` itself does *not* monotonically fall — in
the instrumented runs it drifts 0.00 → 0.15. So this is NOT a trajectory of ρ
sliding down the corridor; it is the **loss of temporal coherence** of the
coherence observable — the array forgetting its initial condition. In the
framework's terms this is still a corridor-EXIT: the array, unmaintained,
relaxes from an organised (correlated, memory-bearing) post-reset state toward
the **chaos pole** (r∞ ≈ 0, decorrelated). r∞ ≈ 0.000 ± 0.02 confirms it
relaxes all the way to the chaos pole, not to a residual band. 1/τ is the rate
of that unmaintained relaxation — the GPU substrate's `dρ/dt` magnitude with
the maintenance off. This is exactly the quantity condition 2 needs, and exit
toward chaos (decorrelation) is one of the two corridor-exit directions the
framework names (the other being rigidity, ρ → 1).

## Gate check (pre-committed C1–C5)

| Gate | Requirement | Result | Pass |
|------|-------------|--------|------|
| C1 — coherence observable | r(t) decays; r(t) is autocorrelation of the framework's coherence signal k_eff | r drops 0.68–0.75 each run | ✅ |
| C2 — not the cross-device artifact | decay is a single-device temporal autocorrelation, not the flagged between-device quantity | one `PhysicsTestSensor` per run; r(t) correlates that one device's k_eff across **time** | ✅ |
| C3 — not window-dominated | τ > 3·W = 15 s | min τ = 43.3 s; τ/W ≈ 8.7–10× | ✅ |
| C4 — real fit | r∞ ∈ [-0.1,0.3], A ∈ [0.5,1.5], r drops ≥ 0.3 | r∞ = 0.000, A = 1.01–1.13, drop 0.68–0.75, R² 0.81–0.83 | ✅ |
| C5 — reproducible | max τ / min τ < 2 | 51.3 / 43.3 = 1.18 | ✅ |

**C2 — the artifact question, settled directly.** CIRISArray flags *cross-DEVICE*
coherence (r ≈ 0.97 between two separate GPUs) as an ALGORITHMIC ARTIFACT: the
shared k_eff algorithm maps any thermalising oscillator bank onto similar r_ab
trajectories, so independent devices' k_eff series correlate spuriously
("the sensing was the algorithm itself", README Root Cause Analysis, Exp 55–56).
That artifact is about correlation **between two devices at one time**. The
Test-4 decay measured here is the **temporal autocorrelation of one device's own
k_eff series** — a different quantity, in a different axis (time, not device).
The shared-algorithm collision does not manufacture a 46 s exponential decay in
a single device's temporal memory; that decay is the array's actual
thermalisation. CIRISArray's own honesty columns agree: cross-device coherence
is in the NOT-VALIDATED column, but the **coherence DECAY** (Exp 51 Test 4) is
in the CONFIRMED column, and Exp 53's null-hypothesis battery N1–N5 (temporal
shuffle, GPU load, software RNG, seed variance, deterministic) all pass for it —
"the phenomenon is not an artifact." C2 passes.

**C3 — window-domination, the C. elegans failure mode, does not bite here.**
The C. elegans attempt failed because τ_ac ≈ 15 s was comparable to the 30 s
sliding window — the measured "rate" was the window's own imposed
autocorrelation. Here W = 5 s and τ ≈ 47 s: τ/W ≈ 9×. The relaxation timescale
is an order of magnitude longer than the estimator window, so τ is a property
of the substrate, not of the windowing.

## Honest scope

- **One substrate, one exit direction.** This is the GPU oscillator array
  relaxing toward the **chaos pole** with maintenance off. It does not measure
  the rigidity-ward exit, and it does not measure any other substrate.
- **Not a cosmological time-to-fidelity.** A cosmological corridor-exit rate
  needs the cross-rung transport law and the P_ω operator — both currently
  blocked (CLAUDE.md open formal steps 1 and 4). This datum does NOT transport
  to the cosmological scale. It is condition 2's *first real substrate
  calibration point* — a non-circular corridor-exit rate, measured, with error
  bars, at the framework's home substrate.
- **Units.** The rate is in s⁻¹. It is intrinsic to the GPU oscillator dynamics
  (Exp 53 found τ ∝ ε⁻⁰·⁴ in the coupling constant and τ independent of
  oscillator count N — so 46.7 s is set by the coupling regime, not the array
  size). A dimensionless form would divide by an intrinsic GPU timescale; that
  normalisation is not pre-registered here and is left for the cross-substrate
  comparison.
- **Why this one held where three attempts failed.** The LLM attempt had no
  clean monotone exit and a too-noisy 24-token window; the paired CCA record
  was never instrumented with entry/exit clocks; the C. elegans run was
  window-dominated (τ_ac ≲ W). The GPU run succeeds because (a) the GPU is the
  framework's home substrate with a genuinely unmaintained free-relaxation event
  (post-reset thermalisation), and (b) τ ≫ W by ~9×, so the estimator does not
  dominate.

## Secondary findings — Exp E4 and Exp E1 in framework terms

Read off the existing committed CIRISArray results (`expE4_results.json`,
`expE1_results.json`); not re-run; descriptive only.

### Exp E4 — operational collapse threshold: a measured corridor floor on the GPU

E4 sweeps a synchronising stress and finds the system's function (workload-
detection latency, false-positive rate) degrades >50% once **k_eff drops below
≈ 4.0** (`keff_critical = 4.02`; latency-collapse k_eff = 4.02, FP-collapse
k_eff = 4.00). In framework terms this is a **measured lower corridor boundary
on the GPU substrate** — an operational k_eff floor below which the coordinating
system stops doing its job. The framework's corridor k_eff floor (CLAUDE.md
Piece 3) is the asymptotic ≈ 2.33 at the upper correlation bound ρ_c ≈ 0.43.
E4's operational floor of 4.0 sits **above** the framework's structural floor of
2.33 — consistent: the array becomes operationally useless (E4's "collapse")
*before* it reaches the framework's hard rigidity-pole floor. E4 is the
empirical, function-defined corridor edge; 2.33 is the structural limit. They
are not in tension — E4 says "function fails at k_eff ≈ 4", the framework says
"k_eff cannot structurally fall below ≈ 2.33"; the operational margin between
them (4.0 → 2.33) is the corridor's lower working band.

### Exp E1 — block structure: Simon near-decomposability at the GPU substrate

E1 builds two independent 8-sensor clusters and shows that **the structure of
the correlation, not its magnitude, sets k_eff**. With two blocks, naïve
global-ρ k_eff would collapse toward 1 under high correlation, but the
block-aware k_eff stays pinned at the block count (k_eff_block ≈ 2.0 across all
four configs) — each independent cluster acts as one effective degree of
freedom. The experiment confirms ρ_intra > ρ_inter is the resilience condition:
when within-cluster correlation exceeds between-cluster correlation, effective
diversity is preserved (`demonstrated_block = true`). This is **Herbert Simon's
near-decomposability** (*Architecture of Complexity*, 1962) instantiated and
measured on the GPU: a stable hierarchy has strong within-module coupling and
weak between-module coupling. It is directly relevant to the framework's
cross-rung structure (StructuralClaims Claim 6): Claim 6's amended position is
that *coordinated rungs sit at intermediate cross-rung coupling g/J ~ O(1)* —
which **contradicts** Simon's g/J ≪ 1 at the rung level. E1 shows the Simon
regime (ρ_intra ≫ ρ_inter, near-decomposable) does hold for *independent
co-located sensor clusters* on the GPU — but note this is a within-substrate
modularity result, not a cross-rung coupling measurement, so it neither
confirms nor refutes Claim 6; it is the clean GPU-substrate demonstration that
block structure preserves k_eff. Caveat: in the E1 run the achieved ρ_intra
(≈ 0.15–0.29) and ρ_inter (≈ −0.34 to −0.09) were both small in magnitude — the
clusters never reached strong synchronisation — so E1 demonstrates the
*mechanism* (block-aware k_eff > naïve k_eff) rather than a high-ρ resilient
operating point (`found_resilient = false`).

## Files

- `PREREGISTRATION.md` — committed before results.
- `verify_corridor_exit.py` — instrumented re-run + gate checker (real GPU).
- `results_corridor_exit.json` — full per-run arrays, fits, gate evaluations.

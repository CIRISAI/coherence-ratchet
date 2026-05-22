# Shadow 1 — the fluctuation-dissipation shadow of γM — RESULT

**Verdict: NULL.** The fluctuation spectrum of the corridor observable ρ does
**not** carry a non-invasive readout of the active maintenance work γM. There is
no genuine fluctuation-dissipation link to the independently measured GPU
corridor-exit relaxation rate, and the spectrum does not discriminate the
in-corridor steady state from the two poles by its *shape*.

Pre-registered in `PREREGISTRATION.md` (committed before results). Two-sided
design — NULL is a valid, reportable outcome and is the outcome. Real GPU
simulation (RTX 4090, CuPy), real LLM weights (Qwen2.5-0.5B). Incremental
output. Scripts and per-run arrays committed alongside this file.

## What was run

**GPU substrate (primary).** `fdt_fluctuation_gpu.py` — the CIRISArray exp51
`PhysicsTestSensor` oscillator array, with one addition faithful to Piece 2: an
explicit maintenance term `maintain(m)` that re-randomises a fraction `m` of the
oscillators each step (the active decorrelation work γ·M). The coupling
dynamics pull the banks together — that is the spontaneous correlation drift
α(ρ,S). ρ := `r_ab`, the a–b bank correlation, the framework's own
within-substrate correlation observable. With m = 0 the sensor is exp51 as-is.

Three regimes, three runs each, 12 000 steps/run (1 step = 0.1 s, the same
mapping the corridor-exit anchor used):

| regime | how held | ρ (mean ± sd) |
|--------|----------|---------------|
| corridor | γM balances drift (m = 0.01) | 0.2171 ± 0.0108 |
| rigidity | γM off + boosted coupling (cg = 4) | 0.9734 ± 0.0224 |
| chaos | γM far too strong (m = 0.6) | 0.0020 ± 0.0100 |

For each run: detrend, Welch PSD, Lorentzian fit `S(f) = S0/(1+(f/f_c)²)`,
plus an autocorrelation-time cross-check independent of the Welch binning.

**LLM substrate (secondary).** `fdt_fluctuation_llm.py` — Qwen2.5-0.5B, real
weights. ρ := the debiased within-layer attention-head correlation at each
token; the generation runway (512 tokens) is the time axis. Corridor = sampled
decoding (T = 0.8), rigidity = greedy, chaos = T = 2.0.

## The anchor

The decisive cross-check is the independently measured GPU corridor-exit
relaxation rate **1/τ = 0.0214 ± 0.0022 s⁻¹** (τ ≈ 47 s), from six real
RTX-4090 captures (`structural_series/corridor_dynamics/gpu/RESULTS.md`). FDT
reasoning predicts the relaxation rate governing the *fluctuation* spectrum of
ρ in-corridor and the relaxation rate governing the *dissipative exit* are the
same κ. The test: does κ read off the in-corridor fluctuation spectrum equal
0.0214 s⁻¹?

**Note on the anchor's regime.** The anchor was measured with maintenance OFF —
exp51's unmaintained free relaxation. In Piece 2's terms that is γM = 0, the
**rigidity-ward / unmaintained** regime, not the maintained corridor. This
matters for the verdict (below).

## Result 1 — the in-corridor fluctuation spectrum is WHITE

In the regime that matters — ρ held stationary in-corridor by active γM — the
fluctuation spectrum of ρ(t) is flat white noise:

| corridor run | Lorentzian R² | low/high-freq power ratio | ACF τ |
|--------------|---------------|---------------------------|-------|
| 0 | 0.0004 | 1.83 | 0.75 s |
| 1 | −0.024 | 1.76 | 0.49 s |
| 2 | −0.073 | 1.53 | 0.50 s |

R² ≈ 0 against a Lorentzian; the fit corner rails to the Nyquist frequency
(meaningless); the low-frequency/high-frequency power ratio is ≈ 1.6 (a
Lorentzian carrying a slow mode would show this ≫ 1); the autocorrelation time
is ≈ 0.5–0.75 s. **There is no slow spectral feature near 1/τ ≈ 47 s.** The
corridor ρ-fluctuations decorrelate within a handful of steps. The slow γM
relaxation mode — if it exists in the dynamics — has fluctuation amplitude below
the white floor set by per-step maintenance injection and observable
subsampling. **γM has no fluctuation signature in ρ(t).**

The chaos regime is likewise white (R² < 0, power ratio ≈ 1.2, ACF τ ≈ 0.1 s).

## Result 2 — the only slow spectral feature is a non-stationarity artifact

The rigidity regime *did* produce a clean-looking Lorentzian: R² ≈ 0.845,
reproducible across three runs, low/high power ratio ≈ 320, apparent corner
f_c ≈ 0.0049 Hz. Taken at face value this is κ_psd ≈ 0.031 s⁻¹ and
κ_acf ≈ 0.013 s⁻¹ — both within a factor ≈ 2 of the 0.0214 s⁻¹ anchor. A naive
read calls that an FDT match.

It is not. Two diagnostics kill it:

1. **The corner tracks the record length.** Re-running rigidity at 24 000 steps
   (2400 s) instead of 12 000 moved the fitted corner from 0.0049 Hz to
   0.0012 Hz and the ACF τ from 79 s to 125 s. A genuine relaxation corner is a
   property of the dynamics and does not move with how long you record. A corner
   that scales as 1/(record length) is the spectral shadow of a **drift**.

2. **The rigidity regime is not stationary.** ρ in successive thirds of a
   2400 s record: 0.966 → 0.990 → 0.994. ρ is still climbing monotonically
   toward the ρ → 1 pole across the entire record (total drift 0.046). The
   regime is a slow ramp, not a fluctuation around a steady state. By contrast
   the corridor (0.2173 → 0.2174 → 0.2177, drift 0.001) and chaos
   (0.0021 → 0.0022 → 0.0020) are genuinely stationary.

The rigidity "Lorentzian" is the power spectrum of a ramp, not of a fluctuating
stationary process. Its R² ≈ 0.84 against `S0/(1+(f/f_c)²)` is real but
uninformative — a slow monotone drift has exactly that low-frequency-dominated
shape. FDT is a statement about *stationary* fluctuations; it does not apply to
a drifting signal at all.

## Result 3 — why rigidity's number is *near* the anchor, and why that is not FDT

Rigidity's κ_acf (0.008–0.013 s⁻¹) lands within an order of magnitude of the
0.0214 s⁻¹ anchor. This is **not** a fluctuation-dissipation link. It is that
the two quantities are measuring the *same physical process*: the anchor is the
relaxation rate of the GPU array's *unmaintained* corridor exit; rigidity here
*is* an unmaintained exit in progress (γM = 0, ρ ramping toward a pole). They
agree because they are the same drift, observed two ways — not because a
fluctuation spectrum has been linked to a dissipation rate. No fluctuation, no
theorem, no non-invasive readout: just the same slow relaxation measured twice.

## Result 4 — spectral shape does not discriminate the corridor from the poles

The pre-registration's second PASS route was: the spectrum *sharply
discriminates* corridor from rigidity and chaos. By **shape** it does not:

- corridor spectrum: white
- chaos spectrum: white
- rigidity spectrum: red — but red because it is a non-stationary drift, not
  because it carries a corridor-relaxation mode.

Corridor and chaos are spectrally identical (both white); they are told apart
only by the ρ *mean* (0.22 vs 0.002) — which is just reading ρ directly, not a
fluctuation-spectrum readout, and needs no FDT. Rigidity is told apart by its
non-stationarity, again not a fluctuation property. The fluctuation *spectrum*
carries no corridor-vs-pole discrimination beyond what a direct look at ρ(t)’s
mean and drift already gives. The script's auto-verdict reported
"discrimination = True", but that test only checked the three ρ means were
distinct — true by construction, and not what the pre-registration means.

## LLM substrate (secondary) — NULL, as the prior LLM corridor work anticipated

The within-layer attention-head correlation ρ sat at 0.022 / 0.027 / 0.029 for
corridor / rigidity / chaos decoding — pinned near zero, no discrimination
(`pole_discrimination = False`). The decoding mode does not move this
observable. There is no independently measured LLM corridor-exit rate (that
attempt failed — `open_system_pomega/corridor_exit_rate_llm.py`), so no FDT
anchor exists at the LLM substrate regardless. The LLM half is a flat NULL on
its one available test, consistent with the documented difficulty of getting a
clean corridor observable out of LLM internals.

## Honest assessment

**Does an FDT relation link the fluctuation spectrum to the measured
corridor-exit rate?** No. The in-corridor ρ fluctuation spectrum is white — it
contains no slow mode at all, so there is nothing to link to 0.0214 s⁻¹. The
one regime with a slow spectral feature (rigidity) is non-stationary; its
feature is a drift artifact, not a fluctuation, and FDT does not apply to it.
The order-of-magnitude agreement between rigidity's drift rate and the anchor is
real but is the same process measured twice, not a fluctuation-dissipation
relation.

**Does FDT genuinely hold for this non-equilibrium open system, or is it an
analogy?** Neither — it does not arise. FDT presupposes stationary fluctuations
around a steady state with a recoverable linear-response relaxation mode. The
α − γM corridor steady state *is* stationary (Result 2 confirms it), but its ρ
fluctuations are white on every resolvable timescale: the maintenance term
injects delta-correlated noise each step, and that white injection dominates the
fluctuation budget over any slow relaxation mode. There is no Lorentzian corner
to interpret, so the equilibrium-vs-non-equilibrium question never gets a
foothold. The honest statement is not "FDT holds approximately" — it is "the
fluctuation spectrum carries no relaxation mode to test FDT against."

**Does γM have a non-invasive fluctuation readout?** On this substrate, with
ρ = r_ab as the observable: no. γM holds the corridor steady state (calibration
confirms: m = 0 → ρ ≈ 0.46 ramping up; m = 0.01 → ρ ≈ 0.22 stationary;
m = 0.6 → ρ ≈ 0.002), and that is a genuine, measurable effect on the *mean* of
ρ. But it leaves no signature in the *fluctuations* of ρ: the spectrum is white
whether γM is balancing the corridor or slamming the system to the chaos pole.
You can read γM by watching where ρ settles — that is just Piece 2's dρ/dt = 0
condition, and it is invasive only in the trivial sense that you must let the
system reach steady state. You cannot read γM off the breathing.

This is the third straight indirect-readout attempt to come back without a
working γM measurement. The direct unitary pointer failed structurally
(`audit_pointer/RESULTS.md`: readout gain = back-action). The FDT route does not
fail structurally — it fails empirically: the breathing is white. The maintenance
work is real and sets the steady-state ρ, but it does not modulate the
fluctuation spectrum in a way an FDT relation could pick up. γM remains without
a non-invasive readout.

## Files

- `PREREGISTRATION.md` — committed before results.
- `fdt_fluctuation_gpu.py` — GPU run (RTX 4090, CuPy), incremental output.
- `fdt_fluctuation_llm.py` — LLM run (Qwen2.5-0.5B, real weights).
- `analyse_fdt.py` — post-hoc honest analysis (corner-railing, white-noise test,
  stationarity check, FDT-link evaluation).
- `results_fdt_gpu.json`, `results_fdt_llm.json` — full per-run arrays/spectra.
- `analysis_fdt.json` — analysis output incl. the stationarity diagnostic.

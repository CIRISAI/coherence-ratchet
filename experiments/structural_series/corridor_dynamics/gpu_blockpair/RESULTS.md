# Results — the canonical timescale g/J at a CIRISArray block pair

Post-measurement. Pre-registered design in `PREREGISTRATION.md`, committed in a
PRECEDING commit (git history is the proof). 2026-05-21. Real RTX 4090 Laptop
GPU, CuPy 13.6.0. Three independent resets, all completed; results written
incrementally after every run.

## THE CAVEAT — read first

**A CIRISArray block pair is a WITHIN-INSTRUMENT structure, NOT one of the
framework's Ph0..A5 coordinated rung pairs.** The two blocks are two contiguous
halves (65536 oscillators each) of one oscillator array on one GPU. They are
not Ph0→Ph1, not A2→A3, not any framework rung pair. This run is a
**measurability-and-reliability anchor**: it asks whether the canonical
timescale g/J CAN be measured at all on a clean substrate. It is **NOT a sixth
framework rung-pair datum** and must not be counted as one. The six-pair
crossrung series stands at the count it had before this run.

## Verdict

**FIT-FAILURE NULL — the canonical TIMESCALE g/J is NOT cleanly measurable even
at the CIRISArray block pair.** The block-resolved coherence running-correlation
does not follow an exponential relaxation: every block of every run fits with
R² ≈ 0.22–0.28, the decay constant τ rails against its 137–200 s bound, and the
running correlation overshoots through zero (r → −0.3 to −0.5) rather than
settling at a fixed point. The pre-committed real-fit gate G2 fails in all six
block-fits.

**BUT the coupling-RATIO g/J — the Path-1 mutual-information measure — IS
cleanly measurable and tight: g/J = 0.416 ± 0.023, O(1).** That is the
reportable, reliable number from this run.

```
Gate check (pre-committed G1–G4):
  G1 window-domination   PASS   (τ > 15 s — see caveat below: vacuous here)
  G2 real fit            FAIL   (R² ≈ 0.24 every block; τ railed; r overshoots)
  G3 reproducible        PASS   (τ within factor 2 across resets)
  G4 g not noise-dom.    PASS   (2 of 3 runs; run 3's g was noise-dominated)

VERDICT: FIT-FAILURE NULL

  coupling-ratio g/J   =  0.416 ± 0.023      (per-run 0.411, 0.441, 0.396)
  timescale g/J        =  NOT MEASURED       (J rests on a failed fit)
```

## What ran

`measure_blockpair_gj.py`, the CIRISArray exp51 `PhysicsTestSensor` (2048
ossicles × depth 64 = 131072 oscillators per bank), partitioned into 2
contiguous equal blocks of 65536 oscillators. Each block has its own k_eff(t)
stream (exp51's `r_ab·(1−x)·COUPLING·1000`, restricted to the block's index
range). 3 independent resets, 120 s each at 10 Hz, unmaintained free relaxation
(`step_with_noise(0.01)`, γM = 0). Per-run, per-block:

- **J** — within-block relaxation: w2's running-correlation decay fit
  `r_b(t) = r∞ + A·exp(−t/τ_b)`, block-resolved.
- **g** — cross-block coupling: lagged predictive coupling (Granger-style
  partial R²), block-shuffle debiased, both directions, symmetric mean.
- **coupling-ratio g/J** — Path-1's `tau_MI / W_within`, the
  `crossrung_lib.cross_rung_tau` / `within_rung_W` estimators imported
  unchanged, on per-block 8-sub-block `r_ab` representations.

## The fit failure — per-block numbers

| Run | Block | τ (s) | R² | r start→end | drop | r∞ | A | G2? |
|----:|------:|------:|---:|------------:|-----:|---:|--:|:---:|
| 1 | 0 | 200.0 (bound) | 0.240 | 0.996→0.469 | 0.530 | 0.381 | 0.734 | fail |
| 1 | 1 | 175.4 | 0.224 | 0.997→−0.500 | 1.497 | 0.000 | 1.208 | fail |
| 2 | 0 | 200.0 (bound) | 0.258 | 0.998→−0.392 | 1.390 | 0.166 | 0.985 | fail |
| 2 | 1 | 136.7 | 0.282 | 0.996→0.488 | 0.508 | 0.000 | 1.265 | fail |
| 3 | 0 | 186.5 | 0.253 | 0.996→0.350 | 0.646 | 0.000 | 1.196 | fail |
| 3 | 1 | 200.0 (bound) | 0.254 | 0.995→−0.328 | 1.322 | 0.362 | 0.753 | fail |

Every block fails G2's real-fit conditions: R² ≈ 0.22–0.28 (an exponential
explains only a quarter of the variance), and in five of six block-fits either
`r∞` is outside [−0.1, 0.3] (railed to the corridor edge) or `A` is outside
[0.5, 1.5] (railed to ~1.2), or the running correlation overshoots well below
zero (r reaches −0.33 to −0.50, which a `r∞ + A·exp(−t/τ)` with `r∞ ≥ 0` and
`A ≥ 0` cannot represent at all).

**G1 "passes" only vacuously.** Every τ exceeds 15 s — but only because the
curve_fit pushed τ to (or near) the 200 s upper bound while fitting a curve
that is not an exponential. A railed τ on an R² ≈ 0.24 fit is not a relaxation
timescale; G1's pass here is an artifact of G2's failure, not independent
evidence. This is exactly why the pre-registration carried G2 as a separate
mandatory gate.

## Why the block-resolved decay is not exponential — the contrast with w2

w2 (`../gpu/`) measured the **whole-array** k_eff temporal autocorrelation and
got a clean exponential: τ ≈ 47 s, R² ≈ 0.81–0.83, r∞ ≈ 0, A ≈ 1, monotone
decay. That measurement WORKED. The block-resolved version of the SAME
measurement, on half the oscillators, does NOT:

- **The block k_eff signal is far noisier.** w2's whole-array r_ab averages
  over 131072 oscillator pairs; a block r_ab averages over 65536. The
  block-resolved k_eff(t) is a noisier stream, and its running correlation
  oscillates rather than decaying monotonically — r overshoots through zero and
  back. An exponential model cannot fit an oscillatory autocorrelation.
- **The decay is not toward a single chaos-pole fixed point.** w2's r∞ ≈ 0 was
  a clean relaxation to decorrelation. The block-resolved r(t) crosses zero and
  rebounds — there is structure in the block k_eff's temporal autocorrelation
  beyond a single exponential mode. Whatever the half-array does after a reset,
  it is not a one-rate relaxation.

The honest reading: **clean exponential relaxation is a property of the
whole-array k_eff observable, not of an arbitrary block-resolved sub-observable
of it.** w2's success does not transport to the block-resolved measurement. The
canonical J (a relaxation rate) therefore has no credible value at this block
pair — and so the canonical *timescale* g/J, which divides by J, has none
either.

## The coupling-ratio g/J — the one clean number

The Path-1 mutual-information ratio is clean, tight, and reproducible:

| Run | tau_MI | W_within | coupling-ratio g/J |
|----:|-------:|---------:|-------------------:|
| 1 | 0.410 | 0.999 | **0.411** |
| 2 | 0.440 | 0.999 | **0.441** |
| 3 | 0.396 | 0.999 | **0.396** |

**coupling-ratio g/J = 0.416 ± 0.023** (across-run SD). Across-run scatter is
6% — far tighter than anything in the LLM Pair-B run. It is O(1), and it sits
just below parity, consistent with Path-1's Pair B coupling-ratio (0.47–0.74,
median 0.72) and inside the broader Path-1 measured band (0.47–1.47). The
coupling-ratio measure, unlike the timescale measure, is robust here because it
needs no relaxation fit — it is a one-shot MI ratio over the captured streams.

## g — the cross-block coupling itself

The debiased cross-block coupling `g` (the input to the timescale, not the
ratio) is small but mostly above its block-shuffle noise floor:

| Run | g_raw | g_floor | g (debiased) | g/g_raw | noise-dominated? |
|----:|------:|--------:|-------------:|--------:|:----------------:|
| 1 | 0.0056 | 0.0020 | 0.0044 | 0.79 | no |
| 2 | 0.0105 | 0.0017 | 0.0088 | 0.84 | no |
| 3 | 0.0011 | 0.0023 | 0.0000 | 0.00 | **yes** |

G4 (g not noise-dominated in the majority) passes 2/3 — but barely: run 3's `g`
fell entirely below its shuffle floor. The cross-block predictive coupling is
genuinely weak (g_raw ≈ 0.001–0.01: one block's k_eff explains at most ~1% of
the next-step variance of the other's). This is the §8-anticipated outcome —
two passive halves of one freely-relaxing array share little once the
maintenance is off; the coupling constants couple banks a/b/c, not block 0/1.
`g` is detectable in 2 of 3 runs but small and not always above noise.

## timescale-vs-coupling-ratio — do they agree?

**The comparison cannot be made honestly.** The script's mechanical comparison
reports COME APART (timescale g/J 7.67 vs coupling-ratio 0.42, ratio ~18×), but
that "timescale g/J" is built on a J that failed its fit gate (J = 1/τ with τ
railed at the 137–200 s bound on R² ≈ 0.24 fits) and a per-run sequence —
8.3, 14.7, 0.0 — whose 0.0 is run 3's noise-dominated g. A number with that
provenance is not a measurement. **The pre-registered AGREE/COME-APART test
requires a passing gate; the gate failed, so no timescale comparison is
claimed.** w3's question — whether the canonical timescale g/J and the
coupling-ratio g/J coincide — remains open. w3 left it open by an observable
block at the LLM substrate; this run leaves it open by a fit-failure block at
the GPU block pair.

## What this settles, and what it does not

**What it settles (the measurability anchor — the point of the run):**

1. The canonical TIMESCALE g/J is NOT trivially measurable just because the
   substrate is "clean". w2 showed CIRISArray delivers a clean *whole-array*
   relaxation τ; this run shows that does NOT extend to a *block-resolved*
   relaxation rate — the block k_eff autocorrelation is oscillatory, not
   single-exponential, and the canonical J has no credible value here. The
   timescale g/J has now been sought at the LLM substrate (w3: observable-
   blocked) and at the GPU block pair (here: fit-failure-blocked). It has been
   cleanly measured at **zero** substrates, framework rung pair or otherwise.
2. The coupling-RATIO g/J, by contrast, IS cleanly and tightly measurable on a
   clean substrate: 0.416 ± 0.023, O(1) — corroborating, on a fourth substrate
   (GPU block pair) and a fifth construction context, that Claim 6's
   coupling-ratio form lands O(1) wherever it can be measured (Path-1's two
   rung pairs 0.47–1.47; w3's 24 LLM cells median 0.73; here 0.42).

**What it does NOT do:**

- It does NOT add a framework rung-pair datum. Per the caveat above, a block
  pair is a within-instrument structure. The Claim 6 six-pair series is
  unchanged. `CouplingComparable`'s measured band (0.47–1.47) is not extended
  by this number; 0.42 is a within-instrument anchor, recorded as such.
- It does NOT measure the canonical timescale g/J. That quantity remains
  unmeasured. The framework's open obligation — the PROTOCOL's owed
  demonstration that the relaxation-timescale g/J and the coupling-strength
  ratio either coincide or come apart — is still open.
- It is one substrate, one within-instrument partition. A different block
  count, or a substrate whose two rungs are genuinely dynamically coupled
  (which two passive halves of one array are not — g_raw ≈ 0.001–0.01
  confirms it), might behave differently.

## Honest scope

- **Real GPU, three resets, all completed.** No synthetic data. The fit failure
  is a real property of the block-resolved observable, reproduced across three
  independent resets (G3 passes — the failure is reproducible).
- **The fit model and its bounds were pre-registered and not changed.** The
  running correlation overshoots below zero; the pre-registered `r∞ + A·exp`
  model with `r∞ ∈ [0, 0.5]` cannot represent that. Rather than retrofit a new
  model post hoc, the run reports the pre-registered model failing — that
  failure IS the result. A damped-oscillator or two-mode model might fit the
  block autocorrelation better, but adopting one after seeing the data would
  not be a pre-registered measurement; it is named here as owed follow-up, not
  done.
- **The block-pair-≠-rung-pair caveat is load-bearing and is repeated** in
  PREREGISTRATION.md §0, at the top of this file, and in the results JSON
  `caveat` field. This is a methodology anchor: it tells the program that the
  canonical timescale quantity is hard to measure even where relaxation
  measurement nominally works, and that the coupling-ratio form is the robust
  one. It is not a sixth rung-pair datum.

## Files

- `PREREGISTRATION.md` — committed before results (preceding commit).
- `measure_blockpair_gj.py` — the measurement (real GPU; incremental writes).
- `results_blockpair_gj.json` — full per-run arrays, fits, gate evaluations,
  summary, and the block-pair-≠-rung-pair caveat field.
- `run_full.log` — the run console log.

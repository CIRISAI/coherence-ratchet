# PREDICTION 4 — the DM-particle density-scaling discriminator (PRE-REGISTRATION)

**Date 2026-07-21. Method frozen BEFORE any copula-Third number on the particle field is
seen.** Nothing in `thirdness/` or `thirdness/discriminator/` is modified. This directory
holds the one unrun leg of the Third prenup (`papers/notes/the_third_prenup.md`,
prediction 4 / kill K4):

> **K4** — if the copula Third collapses to the surrogate on the DM particle field, the
> "physical measured Third" leg dies and only the pure-math theorem `I_total ≥ S/2` survives.

## Why the tracer test could not decide it

K4 fired on the **halo/galaxy tracer** field (`discriminator/`): a coordination-free Poisson
null matched to n̄ and P(k) OVER-reproduced the ~20% copula Third; `argsort∘argsort` on the
~44% empty cells manufactured 37–63% of it; CIC assignment halved R8. Verdict there:
discreteness/estimator artifact of a **sparse point catalog** (n̄ ≈ 0.4 halos per NG=64 cell).

That verdict is about the *tracer*, not about the *matter field*. Two things were confounded
and cannot be separated at one tracer density:

1. shot noise, which injects connected ≥3-point structure at order `1/n̄`, and
2. genuine field-level higher-order coordination, which is a property of the continuous field
   and is **independent of how densely you sample it**.

The dark-matter particle field samples the *same* matter field at n̄ larger by ~3.4 decades.
That is the lever.

## The discriminator: density scaling (the decisive design)

Measure the identical copula-Third estimator on the **same box, same grid, same smoothing
scales**, at a ladder of tracer number densities obtained by random subsampling of the DM
particles. Two hypotheses make opposite, quantitative predictions:

- **Shot artifact.** A standardized skewness sourced by Poisson discreteness scales as
  `n̄^(−1/2)` and → 0. The excess over a shot-matched null → 0 at every density by
  construction.
- **Physical Third.** A genuine field-level copula non-Gaussianity **saturates**: the estimate
  converges to a density-independent plateau `A_∞ > 0` as n̄ → ∞, and the excess over the
  shot-matched null grows (in σ) as shot noise falls away.

The two are distinguishable over ~3 decades of n̄ even if the plateau is small.

## AMENDMENT (2026-07-21, before any Third statistic was computed)

Feasibility measurement, not a result: the machine's link to `tng-project.org` was measured at
**≈ 0.49 MB/s aggregate**, and it does **not** scale with parallel connections (16 concurrent
range requests gave the same aggregate as one; a Cloudflare speed test run concurrently
confirms the local link, not the server, is the ceiling). TNG300-3's `PartType1/Coordinates`
is float64 → 244,140,625 × 24 B = **5.86 GB ≈ 3.3 h**; TNG100-3's is **2.26 GB ≈ 1.3 h**.

Therefore the two boxes named below **swap roles**: **TNG100-3 becomes the primary object**
and TNG300-3 the same-box confirmation, attempted only if the primary lands with budget to
spare. Nothing else changes — the verdict rules are statements about scaling with n̄ and are
box-independent, and the smoothing scales were already registered to rescale with the box
(R → R × L/205, preserving R/cell exactly: 1.25, 2.5, 5.0 cells at NG = 64). No copula-Third
number of any kind had been computed when this amendment was written; the only numbers seen
were bandwidth, byte counts, and HDF5 layout.

## The object

**PRIMARY (per the amendment above): IllustrisTNG TNG100-3, snapshot 99 (z = 0), PartType1.**
- Box **75 Mpc/h**, `N_DM = 94,196,375` (455³), equal-mass DM particles.
- NG = 64 → cell 1.172 Mpc/h, full-field **n̄ = 359.3 particles/cell**; R ∈ {1.463, 2.927,
  5.854} Mpc/h (= {4, 8, 16} × 75/205, identical R/cell ratios to the frozen run).
- Density ladder identical in *fraction*; n̄ values are 359.3 × f.

**CONFIRMATION (attempted if budget permits): TNG300-3, snapshot 99 (z = 0), PartType1.**
- Box **205 Mpc/h** — *identical volume and grain to the frozen TNG300-1 halo measurement*, so
  the smoothing scales R ∈ {4, 8, 16} Mpc/h carry over unchanged (no volume rescaling needed).
- `N_DM = 244,140,625` particles (625³), all of equal mass ⇒ count field = mass field, so the
  count/mass-weight ambiguity that complicated the halo run does not arise.
- At NG = 64 (cell 3.203 Mpc/h) the full field has **n̄ = 931.3 particles/cell**, against the
  halo catalog's n̄ ≈ 0.4. Dynamic range ≈ 3.4 decades.
- TNG300-3 is the low-resolution member of the TNG300 family (same box, same initial phases,
  same cosmology as TNG300-1). It is chosen because its full particle set is *downloadable*
  (2.93 GB of coordinates over 16 chunks) while TNG300-1's is 15.6 billion particles.
  Resolution affects small-scale power; at R ≥ 4 Mpc/h (≥ the NG=64 cell) this is a
  sub-dominant systematic, and it is *reported*, not hidden — the second snapshot and the
  NG=128 grid probe it.
- **Secondary snapshot (attempted if bandwidth permits): snapshot 67, z = 0.503** — the DE
  epoch, the epoch where the halo-field Third kneed. Consistency check only; the verdict is
  read at z = 0.
- **Fallback if the TNG300-3 pull fails:** TNG100-3 (75 Mpc/h, 94.2M DM particles), with R
  rescaled by 75/205 to {1.46, 2.93, 5.85} Mpc/h. If both fail, this is reported as
  INFEASIBLE with whatever was obtained; **no number is fabricated and no result is inferred
  from a partial pull.**

## The density ladder (frozen)

Random subsampling of the particle list, independent uniform deviate per particle, **nested
across fractions within a replicate** (u < f). Fractions and the resulting NG=64 mean
occupancy:

| f | n̄ (particles per NG=64 cell) | note |
|---|---|---|
| 4.3e-4 | 0.40  | matched to the TNG300-1 halo catalog density — calibration rung |
| 1e-3   | 0.93  | |
| 3e-3   | 2.79  | |
| 1e-2   | 9.31  | |
| 3e-2   | 27.9  | |
| 1e-1   | 93.1  | |
| 3e-1   | 279   | |
| 1.0    | 931   | full field |

Replicates: **4 independent random subsamplings** per fraction at NG = 64 (f = 1 is
deterministic, 1 replicate); **1 replicate** at NG = 128 (cell 1.60 Mpc/h) as a grid-scale
robustness column. The scatter across replicates is reported as the subsampling error.

## The estimator (IDENTICAL to `thirdness/measure_thirdness.py`, with the two K4 fixes)

Per gridded field `δ = ρ/ρ̄ − 1`:
1. **normal-score**: `g = Φ⁻¹((rank + 0.5)/N_cells)`, ranks over all NG³ cells;
2. **Gaussian smooth** in Fourier space at R ∈ {4, 8, 16} Mpc/h;
3. **standardized skewness** `⟨g_R³⟩ / ⟨g_R²⟩^{3/2}`.

Two changes from the frozen halo pipeline, both forced by the K4 audit and applied
identically to real fields and to every null:

- **random tie-breaking**, not `argsort∘argsort` (the frozen positional tie-break manufactured
  37–63% of the halo signal on empty cells);
- **CIC** (cloud-in-cell) assignment as PRIMARY, not NGP (NGP aliasing doubled the halo R8).
  NGP is carried as a reported robustness column for both real and null.

**Verdict scale: R = 8 Mpc/h** (as in the frozen registration — well above the NG=64 cell).
R = 4 and R = 16 reported as secondary.

## Nulls (pre-committed controls, not synthetic data standing in for measurement)

Same status as the frozen phase-randomized null, the K4 Poisson surrogates, and the CMB null
ensembles. Every null is run through the *identical* estimator, at the *identical* density.

- **N1 — shot-matched Poisson null (DECISIVE).** Phase-randomize the real subsample's
  amplitude spectrum `|δ_k|` → continuous Gaussian `δ_G` with identical P(k) (hence identical
  pairwise `C`, identical `S`) and **zero connected ≥3-point**; intensity `μ = n̄·(1+δ_G)`
  clipped at 0; `n_cell ~ Poisson(μ)`; the `n_cell` points placed uniformly at random within
  their cell; assigned with the SAME kernel (CIC / NGP) as the real field. Matched n̄, matched
  P(k), pure Poisson discreteness, no genuine coordination. Realizations: 20 for n̄ ≤ 10,
  10 for 10 < n̄ ≤ 100, 5 for n̄ > 100 (cost; shot noise is negligible at the top rungs anyway).
- **N0 — continuous phase-randomized Gaussian.** Same `|δ_k|`, no discreteness. Pipeline
  validation: must return copula skew ≈ 0. N = 10 per density.
- **N2 — cell shuffle (the second leg of the dual null).** Random permutation of the real
  field's cell values: marginals preserved exactly, **all** spatial structure destroyed.
  Must return ≈ 0 through the smoothing. N = 10 per density.

## Pass / fail — frozen, both outcomes live, neither presumed

Let `A(n̄) = |copula skew|` at R = 8, CIC, random tie-break, averaged over replicates;
`M1(n̄)`, `σ1(n̄)` the N1 band mean and s.d. of the same quantity; and
`G(n̄) = (A(n̄) − M1(n̄)) / σ1(n̄)` the excess over the shot-matched null in σ.
Fit `A(n̄) = A_∞ + B·n̄^(−p)` over the full ladder (p free), by least squares on the
replicate-averaged points, errors from the replicate scatter.

**(a) SHOT ARTIFACT — K4 confirmed on the true matter field.** ALL of:
- `A(n̄)` declines monotonically over the ladder (allowing replicate-scatter-sized wiggles);
- `|G(n̄)| < 3` at the **two highest** densities;
- the fitted `A_∞` is within 3σ of 0 **or** within 3σ of the N1 asymptote;
- (corroborating, not required) `p` consistent with 0.5.

**(b) PHYSICAL THIRD — a real, field-level Third exists in the matter field.** ALL of:
- saturation: `|A(n̄_max) − A(n̄_max/10)| < 0.25 · A(n̄_max)`;
- `G(n̄) > 5` at the **two highest** densities, same sign;
- `G(n̄)` does NOT decline over the top decade of n̄;
- `A_∞ > 0` at > 5σ.

**(c) AMBIGUOUS / MIXED** — anything else, including "declines but to a nonzero floor below
5σ", "saturates but within the null band", or a sign flip. Reported plainly as ambiguous with
the numbers; **no verdict is upgraded after the fact.**

Secondary (reported, not verdict-bearing): the same ladder at R = 4 and R = 16; the NGP
column; the NG = 128 column; the z = 0.503 snapshot if obtained; the value of `A` at the
halo-matched rung n̄ = 0.4 versus the halo catalog's own measured value (a cross-check that the
DM ladder's bottom rung reproduces the tracer regime).

## What each outcome costs and buys (stated before the numbers)

- **(a)** kills prediction 4 outright and completes K4: the physical-measured Third is dead at
  every grain the program can reach in the cosmic field; only `I_total ≥ S/2` (pure math) and
  the K3 safety blind spot survive. The pairwise ledger — corridor, sign law, `S(a)` — is
  **untouched and vindicated as tight** at these scales.
- **(b)** is the first real detection of a physical Third, and it is **not support for the
  program** (discipline rule 2): it is a correction that makes every pairwise reading in the
  lake — corridor location, κ, `S(a)` — provisional on a truncation that is measurably loose.
  It would be *costly* news, and it must be reported as such.

## Discipline

No synthetic data (N0/N1/N2 are pre-committed nulls). Grain fixed before spectrum. Dual null
(shuffle + shot-matched). Incremental flush per chunk during the pull and per density during
the measurement. The API key is read from `~/.tng_api_key` at runtime and is **never written
into this repo or any output file**. Frozen files untouched; no git commit. If the pull is
infeasible, that is reported plainly rather than worked around.

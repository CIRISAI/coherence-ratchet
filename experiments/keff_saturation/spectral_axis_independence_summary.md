# Axis-independence: structure (rank) vs maintenance (detailed balance) — filling the two open high-rank cells

**Question.** The framework separates two axes: **STRUCTURE** = effective dimensionality
(LOW-rank/saturating vs HIGH-rank/scale-free) and **MAINTENANCE** = detailed balance
(BREAKS DB = actively coordinating/driven vs DB-SATISFYING = bound/reversible/dead). Two
cells were already anchored: motor cortex (LOW-rank + breaks DB, coordinating) and a galaxy
baryon cycle (LOW-rank + DB-satisfying, bound). This run fills the two OPEN high-rank cells
and asks whether the two axes are **independent** — i.e. whether a system's dimensionality
tells you nothing about whether it breaks detailed balance, and vice-versa.

**The load-bearing test:** does a HIGH-dimensional neural system BREAK detailed balance? If
yes, then together with LOW-rank motor cortex (which also breaks DB) it shows the DB axis is
not a function of the rank axis.

## Data and tooling

- **Turbulent cell (real):** DANDI:000021 **Allen Visual Coding Neuropixels**, session
  721123822. **544 visual-cortex units** (VISp/VISl/VISal/VISam/VISrl), spikes binned at
  20 ms over the **largest contiguous natural-movie block** (natural_movie_three, 601 s →
  30,026 time bins). Fast spikes, not the DB-weak slow calcium. NWB read directly with h5py.
- **Dead cell (constructed control):** the SAME visual matrix, **phase-randomized** —
  destroys cross-unit structure (→ high-rank) and the time-arrow (→ DB-satisfying) by
  construction, holding each unit's marginal power spectrum fixed.
- **Head-to-head:** macaque **MC_Maze** motor cortex (142 M1/PMd units) through the identical
  pipeline.
- **RANK axis** (`spectral_test.py`): correlation-eigenvalue participation ratio, effective
  rank vs a phase-randomized surrogate floor and vs the Marchenko–Pastur edge, PR-subsampling
  exponent β, and a power-law exponent α (λᵢ ~ i^−α; α≈1 scale-free/high-rank, α≈0 flat/noise).
- **DB axis** (both validated estimators): winding-rate z (`entropy_production.py`) and the
  direct circulation-vs-phase-randomized-null z (`spectral_galaxy_db.py`). Ruler at the data's
  T: OU-equilibrium |z|≈1.2, relaxation ≈0.7 (nulls); noisy limit cycle ≈19; OU-driven NESS ≈57.

## The 2×2 (each cell: rank readout, DB |z|, source)

| | **BREAKS DB** (coordinating) | **DB-SATISFYING** (bound/dead) |
|---|---|---|
| **LOW-rank** (bounded) | **motor cortex** — eff_rank(surr) 5–8, α 0.25–0.49; winding \|z\|=**8.8–30**, circ \|z\|=12.5 · *MC_Maze spikes* | **galaxy baryon cycle** — low-rank; circ z≈**0.5** · *TNG (prior run)* |
| **HIGH-rank** (scale-free) | **visual cortex** — scale-free α→~1 (2p) / α highest-of-neural + rising with N (spikes); winding \|z\|=**4.0**, circ \|z\|=**4.0–7.0** · *Allen Neuropixels, natural movie* | **phase-randomized control** — eff_rank(MP)=85, PR=440 (≥ real); winding \|z\|=**1.5**, circ \|z\|=1.6 · *CONSTRUCTED: scrambled visual data* |

## Key result: the high-dimensional neural system BREAKS detailed balance — YES

Visual cortex watching a natural movie breaks detailed balance on both estimators:
**winding |z| = 4.15, circulation |z| = 4.01** (rising to 6.96 under rate smoothing). Both sit
above the null ceiling (~1.2), above the phase-randomized dead control (~1.5), and above the
old slow-calcium C. elegans reference (2.75). Phase-randomizing the same data collapses it to
the null (**|z| = 1.45 / 1.61**). So the DB signal is real coordination, not a spectral
artifact — and it survives at a substrate (fast spikes) where the calcium recordings could not
resolve it.

## Are the two axes independent? YES — demonstrated two ways

1. **DB varies at fixed (or higher) rank.** Real visual movie epoch (breaks DB, |z|=4.0) vs
   its phase-randomized twin (satisfies DB, |z|=1.5): identical marginal spectra, and the dead
   control is if anything **higher**-dimensional (PR 440 vs 207, eff_rank(MP) 85 vs 69), yet the
   arrow of time flips off. At equal-or-greater dimensionality, detailed balance is broken in one
   and satisfied in the other → **DB is not a function of rank.**
2. **DB and rank move oppositely across real systems.** Motor cortex (lower α, lower-rank) breaks
   DB *harder* (|z|=8.8–30) than visual cortex (higher α, high-rank per 2p; |z|=4.0). And the dead
   control is the *highest*-rank system yet the most DB-satisfying. Rank up, DB down; rank down, DB
   up — the two are decoupled, not co-varying.

## Honest caveats (load-bearing)

- **On fast spikes alone, the visual-vs-motor RANK contrast is NOT clean.** The eye-catching raw
  gap (visual eff_rank(MP)=69 vs motor 25) is **almost entirely an N artifact** (544 vs 142 units):
  at **matched N=142** the two are nearly equal (eff_rank(MP) 29 vs 27; motor even has higher
  eff_rank(surr) 8.4 vs 4.5 and higher PR). Spike shot noise dominates the covariance eigenspectrum
  and swamps the scale-free tail that needs thousands of units (Stringer 2019) to resolve.
- **The shot-noise-robust discriminator is the power-law α.** Visual cortex has higher α than motor
  at every matched N (0.49 vs 0.39 at N=142) and α **rises with N toward the Stringer value**
  (visual 0.42→0.65 over N=80→540; motor stuck 0.29→0.39). The decisive high-rank evidence for
  visual cortex is the **2p-calcium** result (α≈0.97, Stringer-matched, non-saturating, CV intrinsic
  dim ≈50 — prior `spectral_allen_cv` run); the spike α trend corroborates it but is degraded by shot
  noise. So the "high-rank" label on the turbulent cell rests on 2p calcium + the α trend, not on a
  clean spike eff-rank gap.
- **The two substrates are complementary, each clean on one axis only.** Calcium gives clean rank
  (α≈0.97) but washes out DB; spikes give clean DB (|z|=4) but shot-noise-muddied rank. Neither alone
  pins BOTH axes for visual cortex; together they place it in the high-rank + breaks-DB cell.
- **The dead cell is a CONSTRUCTED control**, not a found equilibrium system. Phase randomization is
  the honest way to hold marginals fixed while flipping both axes off, but it is a null, not a
  discovered high-rank thermal system. A genuinely-found high-rank + equilibrium anchor is not among
  the systems tested here (the real DB-satisfying anchor, the galaxy, is low-rank).
- **The winding estimator needs long continuous T.** We used a 601 s contiguous movie block (30 k
  bins); the direct circulation null is reported alongside as a cross-check and agrees (|z|=4.0).

## Bottom line

The high-dimensional neural system (visual cortex, natural movie) **breaks detailed balance**
(|z|=4.0, clean on fast spikes) — the turbulent cell is filled. Its phase-randomized twin, at equal
or higher dimensionality, **satisfies** detailed balance (|z|=1.5) — the dead cell is filled as a
constructed control. Combined with the two prior anchors, **detailed balance and effective
dimensionality vary independently**: DB flips while rank is held fixed (real vs scrambled visual),
and DB and rank move in opposite directions across the real systems (motor breaks DB hardest yet is
lowest-rank; the scrambled control is highest-rank yet most reversible). The one honest limitation is
that the *high-rank* label on visual cortex is carried by the power-law α (spikes) and the prior 2p
Stringer match, not by a clean matched-N eff-rank gap over motor cortex — spike shot noise prevents
reading both axes cleanly on the same recording.

*Outputs: `spectral_results_axis_independence.json` (all numbers incl. smoothing sweep + matched-N
control), `spectral_axis_independence.py` (analysis; reuses `spectral_test.py`,
`entropy_production.py`, `spectral_galaxy_db.py`). Real data only; the dead cell is a labelled
constructed control. No commit, no `.lean` edits.*

---

## METHODOLOGY CAVEATS — post-hoc scrutiny (2026-07-04)

Adversarial re-read of this run's own numbers. Net: the STATIC axis-independence claim here
is **suggestive but not established**; the strongest independence evidence in the program is the
*dynamical* anesthesia result (real system vs its own baseline), not this fill. Downgrade the
headline from "demonstrably independent" to "consistent with independence, pending the gray-screen
deconfound."

**1. The "turbulent" cell is not shown high-rank BY THIS RUN — the label is imported.** The
script's own classifier returns `verdict:"intermediate"`, `high_rank:false` for the visual data
(needs `eff_rank_surr≥15 ∧ α>0.5`; got `eff_rank_surr=8`, `α=0.46`). At **matched N=142 motor
cortex is *higher* on the shot-noise-robust surrogate eff-rank** (8.4 vs 4.5). The only estimator
putting visual above motor is the power-law α (0.48 vs 0.39) plus the *external* 2p-calcium α≈0.97
run. So independence-argument #2 ("two DB-breakers at different rank") rests on one thin estimator +
prior data, not on this experiment.

**2. Real-vs-scrambled (argument #1) is a manipulation check, not an independence proof — and read
literally it cuts the wrong way.** Phase-randomization destroys ALL relational structure at once:
flattens the spectrum (→higher rank) AND kills the arrow of time (→DB-satisfying) by construction.
One destructive knob moving both axes is not evidence they're independent; if anything it is weak
evidence they COVARY. A clean proof needs two *natural* systems matched on one axis, differing on the
other — a scramble cannot isolate a single axis. Valid as an estimator-response check; oversold as the
independence demonstration.

**3. The "breaks DB" signal may be stimulus-driven, not internal γM — and it rests on one mode-pair.**
Turbulent-cell circulation z=4.0 is carried almost entirely by ONE pair: 0-1 z=1.5, **0-2 z=−6.1**,
1-2 z=0.2 (two of three at null). And **`natural_movie_three` LOOPS** — a response locked to the
movie's repeat period yields exactly a top-mode rotation that reads "breaks DB" and survives
phase-randomization, but whose *source* is the external periodic drive, not the system's own
maintenance. Winding picks a *different* carrier pair (0-3) than circulation (0-2) — they don't even
agree on which modes hold the irreversibility. This confound is the deepest and was not flagged in the
body above.

**Smaller:** smoothing is cited as strengthening ("up to 6.96") — backwards: temporal low-pass
*manufactures* apparent irreversibility, and winding DROPS under smoothing (4.15→2.89) while
circulation rises, so the estimators diverge (fragile signal); the least-smoothed 4.0 is the
trustworthy value. The "dead" cell is high-rank because it is NOISE (`eff_rank_surr=1`, nothing above
its own surrogate) — a legitimate control, but near-definitionally populated.

**What survives:** visual-cortex spikes DO show a real arrow of time on the least-smoothed data
(|z|=4.0 > ~1.5 null and > the scrambled twin) — the estimators behave. But "high-rank + breaks-DB,
cleanly independent of rank" is over-stated on this data.

**The clean fix (queued):** compute DB on **gray-screen / spontaneous** epochs of the same visual
cortex (Allen has them). Break DB with NO external periodicity ⇒ intrinsic γM, turbulent cell real.
Only during the looping movie ⇒ stimulus-driven, cell collapses. Deconfounds argument #3 on data in
hand.

# k_eff saturation — the direct read of the Gate-0 discriminator

**Question.** Is the corridor the known criticality/edge-of-chaos physics (a
diluting critical correlation — "trivial"), or a genuine low-rank shared
structure (a bounded effective rank — novel)?

**The discriminator** (formalized and machine-checked in
`formal/CoherenceRatchet/Cosmology/CriticalityDiscriminator.lean`):

| hypothesis | band-center scaling | large-k limit of k_eff |
|---|---|---|
| low-rank (novel) | ρ* fixed at ρ₀ | k_eff → 1/ρ₀ — **bounded** (Kish ceiling) |
| criticality (trivial) | ρ* ~ c/√k | k_eff → ∞ — **unbounded**, grows like √k |

`keff_saturation.png` plots the **directly-measured** k_eff against system size
k. This is more robust than the log-log ρ*-vs-k slope regression
(`/tmp/reframe/gate0_regression.py`), which is underpowered (k spans only ~1.7
decades) and flips sign with the LLM-outlier and TCGA k-axis conventions. The
measured k_eff sidesteps both knobs.

**What the figure shows.** Across the six measured substrates (k = 21→200),
k_eff sits in a bounded band ≈ 7 ± 2. Criticality anchored at the smallest-k
point would predict k_eff ≈ 20 at k = 200; the measured maximum is 9.7. The data
tracks the flat low-rank band, not the √k climb.

**Status of the cross-substrate proxy figure: directional, not decisive** —
the measured cluster spans only ~1 decade of k, and the log-log ρ*-vs-k slope
(`/tmp/reframe/gate0_regression.py`) is underpowered and convention-sensitive.
That is why the mechanism-level test below matters.

## DECISIVE (mechanism-level) test — `spectral_test.py`, `spectral_discriminator.png`

The proxies argue *around* the mechanism. This goes *at* it, on raw C. elegans
whole-brain calcium (Kato 2015, 12 worms, up to 151 neurons — the one substrate
with raw data in the main tree). The discriminator is the covariance **eigenvalue
spectrum**:

- LOW-RANK (novel): a few spikes above a flat noise bulk; effective rank small
  and size-independent; PR **subsampling curve saturates** (exponent β≈0).
- CRITICALITY (trivial): scale-free / power-law spectrum; PR grows as a power of
  N (β≈0.3–0.8).
- NOISE (chaos): PR≈N (β≈1), zero spikes.

**Calibrated against synthetic controls through the identical pipeline** (this is
the defensibility crux): injected low-rank (r=3) → β=0.03, eff-rank 3; power-law
α=1.0 → β=0.25; α=0.6 → β=0.65; pure noise → β=0.96, eff-rank 0. The β estimator
separates the hypotheses cleanly at the real data's (N,T).

**Result: C. elegans β = 0.10 ± 0.02 (95% CI excludes the entire criticality
band), effective rank 1–3 across all 12 worms** — statistically on top of the
low-rank control and far from even the mildest criticality (α=1.0 → 0.25). Both
readouts (subsampling saturation + spike count) agree: **whole-brain coordination
in C. elegans is LOW-RANK, not critical. Yay/nay at this substrate: NOVEL, not
trivial** — by mechanism, calibrated, on raw data. This is the first decisive read
(every proxy was inconclusive).

## SECOND substrate (2026-07-02): Drosophila EPG compass — `spectral_drosophila.py`

Independent phylum, independent mechanism. Drosophila central-complex EPG
(ellipsoid-body compass) neurons, Mussells Pires 2024 (60D05 NoLaser; raw
background-subtracted fluorescence `bgsubF`, 32 EB-wedge ROIs, 20 flies × 9
trials = 180 fly-trials). Same analysis core as `spectral_test.py`; the synthetic
calibration is re-run **at N=32** because β's baseline drifts with N (at N=32 the
low-rank r=3 control gives β≈0.12, power-law α=1.0 → 0.42, α=0.6 → 0.78, noise →
0.99 — the hypotheses still separate cleanly).

**Result: β = 0.122 ± 0.077, 95% CI [0.110, 0.133]** — statistically on top of the
N=32 low-rank control and far below the criticality band — with **effective rank
median 1 (range 0-2)**, the ring-attractor fingerprint (a heading bump on a 1-D
ring is essentially rank ~1-2). Verdict: **LOW-RANK, not criticality**. The
insect-compass read replicates the nematode whole-brain read at a mechanistically
unrelated substrate. Regenerate: `python3 spectral_drosophila.py` (needs
`h5py`; reads the v7.3 `Preproc_60D05.mat` in the v17_biology worktree).

**Scope, stated honestly.** Now TWO substrates, both low-rank. The universal claim
still needs the same spectral test on each remaining substrate's raw data; the
template (`spectral_test.py`) runs on any unit × time matrix. Next: fMRI/Allen/
TCGA and non-neural substrates from raw. The high-k engineered point (GPU, k≈2048)
still extends the k-range for the proxy figure, but the spectral test is the
stronger instrument and leads.

**Estimator discipline.** Markers are the reported participation-ratio /
empirical k_eff. The LLM point is shown hollow as a Kish 1/ρ* fallback (ρ*-only
substrate, different-dimension models) and is **not** part of the measured trend.
Numbers and citations are in `keff_saturation_figure.py` (`DATA`) and
`/tmp/reframe/substrate_data.md`.

Regenerate: `python3 keff_saturation_figure.py`

---

## Cross-substrate sweep (2026-07-02) — and the grain qualification

Same spectral discriminator, β ruler recalibrated at each substrate's N. Verdicts:

| substrate | grain / unit | N | effective rank / CV+ dims | β (or spectrum) | verdict |
|---|---|---|---|---|---|
| C. elegans whole-brain | ~complete brain (~50% of 302) | ≤151 | 1–3 | 0.10 | **low-rank** |
| Drosophila EPG compass | complete ring-attractor circuit | 32 | ~1 | 0.12 | **low-rank** |
| S&P-100 returns | market (100 largest) | 101 | 8 (+market mode) | 0.15 | **low-rank** (RMT market-mode+bulk) |
| ABIDE fMRI | complete ~200-region partition | ~200 | ~4 | 0.06 | **low-rank** (agent-run) |
| TCGA transcriptome | gene set × samples | 1500 | small, size-indep | ~0.04 | **low-rank** (agent-run) |
| iCARE EEG | 19 scalp electrodes | 19 | 3 | 0.15 | low-rank (weak: volume conduction) |
| Drosophila PFL3 | 2 bulk ROIs only | 2 | — | — | BLOCKED (not a population) |
| **mouse V1 2p** | **~200 of ~1e8 neurons (subsample of a sensory patch)** | ≤240 | **CV noise-free k_eff ~5 (level misleads); CV power law α≈1.0 (Stringer)** | β 0.83 | **high-dim / scale-free — NOT low-rank; wrong grain** |

**The grain qualification (the real result).** Mouse V1 reads high-dimensional —
but note the subtlety, because it is itself the cleanest validation of the measure
below. The *raw* k_eff (44–59) is noise-inflated; cross-validated (block-
interleaved, validated rank-3→3 / noise→0) the noise-free k_eff is only ~5, which
by **level** looks corridor-sized. Yet the CV eigenspectrum is a **power law with
α ≈ 1.0** at the largest-N sessions (0.97, 1.06 — matching Stringer 2019 mouse-V1
α≈1.04), reproducible dims grow with N, β=0.83. So the participation-ratio *level*
misclassifies cortex as corridor; only *saturation/α* reads it correctly as scale-
free. (Caveat: ~0 CV dims exceed the per-neuron autocorrelation floor, so cross-
neuron coordination is weak; α is the stable readout, not a specific dim count.)
And a 2p field of view is ~0.001% of the brain — a sparse subsample of a
*representational* patch, not a complete coordinating unit. It is excluded as the
wrong grain **outcome-independently**: a subsample's k_eff is not the system's (a
low-rank read there would have been rejected for the same reason).

**The objective measure** is therefore SATURATION, not level: does k_eff saturate
(β→0) as constituents are added, *on a complete unit*? Level is grain-tunable;
saturation is intrinsic, and it is the framework's own claim (the Kish ceiling).
Completeness — all/most constituents of a bounded functionally-closed system, or a
complete partition — is structural and pre-spectral, fixed before any spectrum is
computed. Formalized in `formal/CoherenceRatchet/Cosmology/CriticalityDiscriminator.lean`
(`GrainAndObjectiveMeasure`).

**THE DECISIVE COMPLETE-UNIT TEST — DONE (confirmation).** Larval zebrafish
whole-brain light-sheet (ZAPBench, **all 71,721 neurons** of an entire vertebrate
brain) is the one case where grain cannot be invoked. Result: k_eff **saturates**
dead-flat at ~34 from N'=500 to the full 71,721 (β≈0); a power law would have grown
~3× over that range. Within each of the 3 longest single visual conditions it
**still saturates** (β≈0; PR ~17–46), so the low-rank is *intrinsic*, not a
between-condition stimulus artifact. Cross-validated (noise-removed) power-law
**α = 1.42 / 1.63 / 1.56** — steep (>1 ⇒ saturating/low-rank), decisively unlike
mouse-V1 cortex's shallow α≈0.97; noise-free k_eff ~6–16 (2/3 conditions in the
(2.3,10) corridor); 4–10 modes above the autocorrelation floor (cortex: ~0). A
complete unit that failed to saturate would have falsified the corridor for
vertebrate brains — it saturates. Honest caveat: the saturation *level* is
state/substrate-specific (raw 17–46), so the universal invariant is saturation +
steep α, not the specific band. (`zebrafish_finalize.py`,
`spectral_results_zebrafish{,_condition}.json`.)

**Averaging-null control — DISCHARGED for fMRI** (`spectral_fmri_averaging_null.py`).
The worry: averaging ~10³ neurons into 200 regions lowers dimensionality
mechanically, so "regions are low-rank" could be trivial. Null = 200 *independent*
AR(1) region signals matched to each real region's autocorrelation + variance (same
grain, same T, zero coordination). Result: real k_eff median **8.0** vs averaging
null **35.3** — real is **4.3× lower** (CI [3.96, 4.67]), **139/139** subjects
below the null. Holding N=200 fixed, independent regions give k_eff≈35, so the grain
does not force low k_eff; the real brain's collapse to ~8 is genuine cross-region
coordination (67% strictly in the (2.3,10) corridor). Not an averaging artifact.
**S&P completeness — DISCHARGED**: extending 100→486 stocks (~full S&P 500), PR still saturates (plateaus at k_eff≈11 from N'=50, β≈0.04) — the S&P-100 read was not a small-N artifact; the whole market is low-rank (`finance_fullmarket.py`).

Scripts: `spectral_test.py` (C. elegans), `spectral_drosophila.py`,
`spectral_finance.py` (+ `finance_dynamics.py`: rolling k_eff predicts forward risk
but is ~94% collinear with volatility — validation of the rigidity-pole dynamics,
not new alpha), `spectral_test_allen*.py` (agent-run), `spectral_test_icare.py`,
`spectral_test_tcga_fmri.py`. Per-substrate result JSONs alongside.

---

## The SECOND axis — bound vs coordinating (detailed balance) — TOOLING READY, decisive test pending data

Saturation (above) is one axis: is there *coordinated structure* (bounded k_eff)?
It cannot tell **coordinating** (actively maintained, the framework's γM term) from
merely **bound** (conservative, the α term). The second axis is thermodynamic:
a coordinating system is a non-equilibrium steady state that **breaks detailed
balance** (a directed cycle / entropy production in its collective modes); a bound
system is time-reversible. On exoplanets this reduces to the atmospheric-
disequilibrium biosignature (Lovelock; Krissansen-Totton).

**Estimator (`entropy_production.py`).** v1 (circulation ⟨x dy − y dx⟩ vs a
phase-randomized null) FAILED on cyclic signals — a noisy limit cycle read z≈1
(the null variance is inflated for narrowband data). v2 is the **integrated
angular velocity (net winding rate) with a block-bootstrap null**, taking the
strongest of the top-4 mode pairs. Validated: OU-equilibrium |z|≈1.5,
relaxation ≈1.5 (null ceiling), **noisy limit cycle z=16.6**, OU-driven z=41.

**Positive control (`db_control_v2.py`).** On known-coordinating brains:
- **C. elegans** (Kato cyclic attractor): median **|z| = 2.75**, 83% of worms
  |z|>2, up to 7 — genuinely above the null (~1.5), so the worms DO break detailed
  balance. **But weak** vs the clean-cycle synthetics (16–41), almost certainly
  because slow GCaMP calcium (~1 s decay) smears the fast arrow of time.
- **zebrafish** whole-brain: |z|≈1.9 (marginal, one animal).

**Two hard limitations surfaced, so no substrate tested is decisive for this axis:**
1. **Calcium is too slow** — it washes out irreversibility; a clean positive
   control needs spike-train / electrophysiology data.
2. **The galaxy has T=26 snapshots** — too few for *either* DB estimator
   (block-bootstrap / transition-counting need T ≫ dynamics timescale). So the
   galaxy stellar and baryon-cycle DB readings are under-powered on the time axis
   regardless of estimator; a decisive test needs a fine-cadence sim subbox.

**CLEAN POSITIVE CONTROL achieved (`spectral_spikes_summary.md`).** Fast spike-train
data settles it: **macaque motor cortex during reaching** (DANDI:000140 MC_Maze;
Churchland jPCA rotational dynamics) reads **|z| = 8.8** (up to 44 with shot-noise
smoothing) — far above the null (~1.5) and far above the weak calcium worm (2.75).
So the detector WORKS on good data; the weak calcium signal was a slow-substrate
(~1 s GCaMP) limitation, not a detector failure. Motor cortex is also low-rank
(surrogate-debiased effective rank 5-8; raw spike-count PR is inflated by Poisson
shot noise and must be debiased). So a known-coordinating fast-spiking system reads
**low-rank AND strongly breaks detailed balance** — the two-axis coordination
signature, clean, on real data.

**Status:** saturation axis SOLID; detailed-balance axis now has a VALIDATED
estimator AND a clean real positive control (motor cortex). Still pending: a clean
real *negative* control — a bound system with long-enough time series (the galaxy is
T-limited at 16-26 snapshots; a fine-cadence sim subbox is being chased). Do NOT
read the galaxy "bound" or the weak calcium DB numbers as decisive; DO read the
motor-cortex positive control as decisive that the axis is real and measurable.

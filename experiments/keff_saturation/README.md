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

**Kept honest:** a *complete* unit whose k_eff fails to saturate falsifies the
corridor for that substrate. **Larval zebrafish whole-brain light-sheet** (~all 1e5
neurons of an entire vertebrate brain) is the clean decisive next dataset — grain
cannot be invoked. Two owed controls: coarse-grained low-rank (fMRI) must beat an
averaging null; "complete" is a matter of degree (S&P-100 ⊂ full market).

Scripts: `spectral_test.py` (C. elegans), `spectral_drosophila.py`,
`spectral_finance.py` (+ `finance_dynamics.py`: rolling k_eff predicts forward risk
but is ~94% collinear with volatility — validation of the rigidity-pole dynamics,
not new alpha), `spectral_test_allen*.py` (agent-run), `spectral_test_icare.py`,
`spectral_test_tcga_fmri.py`. Per-substrate result JSONs alongside.

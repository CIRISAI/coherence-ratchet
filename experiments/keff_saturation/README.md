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

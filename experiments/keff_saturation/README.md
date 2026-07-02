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

**Status: directional, not decisive.** This *leans* low-rank but does not rule
out trivial, because the measured cluster spans only ~1 decade of k. The cheapest
way to make it decisive is **one high-k engineered substrate** (e.g. GPU cores,
k ≈ 2048) measured under a *fixed static-ρ estimator* — that single point extends
the range to ~2 decades and either confirms the flat band or reveals the climb.
Do not read the current figure as a settled verdict; read it as "the existing
data leans low-rank, and here is exactly the one point that would settle it."

**Estimator discipline.** Markers are the reported participation-ratio /
empirical k_eff. The LLM point is shown hollow as a Kish 1/ρ* fallback (ρ*-only
substrate, different-dimension models) and is **not** part of the measured trend.
Numbers and citations are in `keff_saturation_figure.py` (`DATA`) and
`/tmp/reframe/substrate_data.md`.

Regenerate: `python3 keff_saturation_figure.py`

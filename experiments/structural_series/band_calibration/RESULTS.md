# Per-substrate corridor-band calibration — results

Run 2026-05-21. Pre-registration: `PREREGISTRATION.md` (committed before this).
Analysis script: `analyse_bands.py`. Results JSON: `results_band_calibration.json`.
Reproduce: `python3 analyse_bands.py` (reads debiased-ρ values already on disk;
the fMRI and LLM per-unit dumps are re-created by `_dump_fmri.py` /
`_dump_llm.py`, exact replications of `data_fmri/fmri_corridor.py` and
`exp_E1_llm_corridor.py`).

## Scope — stated honestly

This is the **static band**: where healthy / in-corridor debiased ρ sits per
substrate. It is **not** the corridor-as-attractor dynamical bounds (the ρ at
which dρ/dt changes regime). Those need per-substrate dρ/dt, measured so far
only at the GPU substrate. Everything below is a *first estimate* of the
corridor centre ρ_mid and half-width w; tightening to true attractor bounds is
gated on per-substrate dρ/dt and is **not** claimed here.

## Data — debiased-ρ sources on disk

| Substrate | n units | Source | Unit |
|---|---|---|---|
| C. elegans (whole-brain) | 832 | `robust_rerun/celegans/results_celegans.json` | per worm, 12 studies |
| Drosophila (central complex) | 57 | `robust_rerun/drosophila/results.json` | per recording (EPG/FC2/FC3) |
| EEG interictal (CHB-MIT) | 1324 | `robust_rerun/eeg/results_eeg_robust.json` | per 10 s interictal window |
| fMRI resting-state (ABIDE) | 139 | re-run of `data_fmri/fmri_corridor.py` | per control subject |
| LLM internals (3 models) | 48 | re-run of `exp_E1_llm_corridor.py` | per transformer layer |

All ρ values are **debiased** — raw mean|corr| with a phase-randomized (neural,
EEG, fMRI) or per-unit-shuffle (LLM) noise floor removed in quadrature.

### MISSING (reported, excluded from the debiased-ρ pool)

- **TCGA.** `data_tcga` reports `rho_normal` for healthy tissue, but
  `02_compute_rho.py` computes raw `mean_abs_corr` with **no phase-randomized
  floor subtraction** — it is a raw ρ, not a debiased ρ. The pre-registration
  restricts the analysis to debiased ρ; mixing a raw-ρ substrate into a
  debiased-ρ calibration would bias every comparison upward. TCGA is therefore
  marked MISSING. (A debiased TCGA re-run is the natural way to recover it.)
- **GPU.** The GPU files in `corridor_dynamics/gpu*` are corridor-**exit**
  relaxation runs — k_eff / order-parameter `r` decaying after a perturbation.
  There is no healthy in-corridor ρ distribution on disk. The GPU substrate
  supplies the *dynamical* dρ/dt data, which the honest-scope section above
  explicitly separates from the static band measured here. GPU is MISSING for
  this static-band purpose by construction, not by data gap.

## Per-substrate band table

ρ_mid = median debiased ρ. w = (p95 − p5)/2. k_eff range via the Kish identity
in the k → ∞ limit (k_eff = 1/ρ, the substrate-independent ceiling form),
evaluated at the band edges — lower ρ ⇒ higher k_eff.

| Substrate | n | ρ_mid | IQR | [p5, p95] | w | k_eff [p95→p5] |
|---|---|---|---|---|---|---|
| C. elegans (whole-brain) | 832 | 0.312 | 0.196 | [0.157, 0.650] | 0.246 | 1.54 – 6.38 |
| Drosophila (central complex) | 57 | 0.331 | 0.087 | [0.097, 0.441] | 0.172 | 2.27 – 10.26 |
| EEG interictal (CHB-MIT) | 1324 | 0.269 | 0.036 | [0.217, 0.322] | 0.052 | 3.11 – 4.61 |
| fMRI resting-state (ABIDE) | 139 | 0.266 | 0.135 | [0.169, 0.464] | 0.148 | 2.15 – 5.93 |
| LLM internals (3 models) | 48 | 0.082 | 0.047 | [0.052, 0.136] | 0.042 | 7.34 – 19.25 |

Notes on the bands:
- **EEG interictal** is the tightest band by far (w = 0.052, IQR 0.036): 1324
  windows of healthy between-seizure cortical activity occupy a very narrow ρ
  band around 0.27.
- **C. elegans** is the widest (w = 0.246): the 832-worm corpus spans 12
  acquisition studies and the whole-brain ρ runs from chaos-edge to near
  rigidity; the *median* is firmly in-band but the distribution has long tails.
- **LLM internals** sit at ρ_mid ≈ 0.08 — roughly 3–4× lower than every
  biological substrate. This reproduces E1's own honest reading: LLM layers
  are decisively off the rigidity pole but sit at the **chaos-side edge**.

## Cross-substrate read (pre-registered)

Per-substrate ρ_mid spans **0.082 – 0.331**, a factor of **4.04×** — this
exceeds the pre-registered ~2× clustering threshold.

**Verdict: SUBSTRATE-SPECIFIC** (per the pre-registration's second branch).

But the spread is **not diffuse — it is one outlier**:

- The four **biological** substrates (C. elegans, Drosophila, EEG, fMRI)
  cluster within a factor of **1.24×** (ρ_mid 0.266 – 0.331) — comfortably
  inside the ~2× threshold. Across coordinated biological rungs spanning
  302 neurons (worm) to 200 cortical regions (human fMRI), the corridor centre
  is shared at ρ_mid ≈ 0.29.
- The **LLM internal-representation rung** is the lone outlier at ρ_mid ≈ 0.08.

Read: a shared corridor centre holds across coordinated **biological** rungs;
the LLM internal-representation substrate sits at a substrate-specific lower
centre. Whether this is a genuine substrate difference or an artifact of the
LLM ρ operationalisation (mean|corr| among hidden units across only ~500
tokens, where E1 itself flags the noise floor as marginal) is unresolved — a
sharper LLM measurement (more tokens, lower floor, k_eff-based) is the owed
follow-up before reading the 4× spread as physics.

## Pooled estimate — first empirical estimate of P_ω's master parameters

Per-substrate equal weight (one band per substrate); pooled ρ_mid = median of
per-substrate medians, pooled w = median of per-substrate w.

| Pool | ρ_mid | w | implied static band [ρ_mid ± w] |
|---|---|---|---|
| All 5 substrates | 0.269 | 0.148 | [0.121, 0.417] |
| Biological 4 only (recommended) | 0.290 | 0.160 | [0.130, 0.450] |

**The biological-4 pooled estimate — ρ_mid ≈ 0.29, w ≈ 0.16, band ≈ [0.13,
0.45] — is the recommended first empirical estimate of P_ω's master
parameters**, because it pools only the clustered substrates and excludes the
LLM outlier. The all-5 pool is reported for completeness; it is pulled down by
the outlier.

### Static-band caveat (load-bearing)

These are **static-band estimates**: the band healthy debiased ρ *occupies*,
not the dynamical attractor bounds at which dρ/dt changes regime. The pooled
band [0.13, 0.45] is strikingly close to the framework's quoted corridor
(0.1, 0.43) inherited from the GPU substrate — but that closeness is a
consistency check, not a derivation. The corridor-as-attractor bounds remain
gated on per-substrate dρ/dt; this calibration does not claim them.

## Bottom line

- Per-substrate bands characterised for 5 substrates from debiased ρ on disk;
  TCGA (raw ρ only) and GPU (corridor-exit dynamics, no static band) reported
  MISSING with reasons.
- Cross-substrate verdict: **SUBSTRATE-SPECIFIC** (4.04× ρ_mid spread) — but
  the four biological substrates cluster within 1.24×; the LLM is the sole
  outlier.
- First empirical estimate of P_ω's master parameters (biological pool, static
  band): **ρ_mid ≈ 0.29, w ≈ 0.16**, implied band **[0.13, 0.45]** — flagged
  explicitly as a static-band estimate, not the dynamical attractor bounds.

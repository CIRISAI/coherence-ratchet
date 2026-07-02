# Arousal-state test of the dynamics claim dρ/dt = α − γ·M(t)

**Question.** The dynamics piece asserts that withdrawing active coherence-management
(`γ·M`) makes `dρ/dt > 0`: correlation ρ climbs and effective dimensionality
`k_eff` falls toward the **rigidity** pole. Arousal is the natural `γ·M` knob —
awake = high maintenance, coma/anesthesia = low. **Pre-registered prediction:
COMA shows HIGHER ρ / LOWER k_eff than AWAKE.**

**Verdict: REJECTED — and rejected in the *opposite* direction.** Coma has the
*higher* k_eff and the *lower* correlation. Maintenance withdrawal drove the
system toward the **chaos** pole (decorrelation), not the rigidity pole.

## Data (real, on disk / PhysioNet)

| Group | Source | N subjects | Location |
|---|---|---|---|
| COMA | iCARE 2023 post-cardiac-arrest scalp EEG | 9 (of 10 mats; 0432 dropped) | `.claude/worktrees/agent-a5a5cfc9f224f29b0/experiments/noncorr_biology/data/icare/<subj>/*_EEG.mat` |
| AWAKE | eegmmidb resting baseline R01 eyes-open + R02 eyes-closed | 13 (26 recordings) | PhysioNet `eegmmidb/1.0.0/S0xx/S0xxR0{1,2}.edf` |

`0432` dropped: its central 60 s window (and everything past ~10 % of the record)
is a flat/saturated block — 0 non-flat channels under the fixed central-window QC
rule. iCARE arousal grade = CPC (1 good … 5 none) from each `<subj>.txt`.

## Matched preprocessing (the whole point)

Absolute k_eff is confounded by ~19-channel volume conduction, so **only the
awake-vs-coma difference is interpreted.** Everything except arousal is matched:
N = **19 referential 10-20 channels** (iCARE native 19; eegmmidb subselected to the
identical standard-19 label set — referential-to-referential), common **128 Hz**
(resample_poly from 160/250/256), **1–40 Hz** 4th-order Butterworth, central
**60 s**, per-channel demean, no re-reference. Analysis core reused verbatim from
`spectral_test.py` (`corr_eig`, `participation_ratio`) and `entropy_production.py`
(`irreversibility_from_units`, k=4).

## Result

| Readout | AWAKE | COMA | effect (awake−coma) | direction vs prediction |
|---|---|---|---|---|
| **k_eff** (participation ratio) | 2.75 | **3.36** | d = −0.76, MW p = 0.11 | **OPPOSITE** (coma higher) |
| **ρ̄** (mean off-diag corr) | **0.53** | 0.27 | d = +1.66, MW p = **0.024** | **OPPOSITE** (awake higher) |
| ρ_Kish (from k_eff) | 0.35 | 0.29 | d = +0.60 | OPPOSITE (awake higher) |
| detailed-balance \|z\| (median) | **4.99** | 3.52 | — | awake breaks DB more |

**Eyes-open-only sensitivity** (controls the eyes-closed posterior-alpha
global-coherence confound — and eyes-open is where the awake≫coma gap is *largest*,
so the effect is not an alpha artifact): k_eff awake **2.50** vs coma 3.36
(d = −1.01, p = **0.042**); ρ̄ awake **0.58** vs coma 0.27 (d = +1.67, p = **0.012**).

**Within-coma (CPC):** Spearman(CPC, k_eff) = −0.22, Spearman(CPC, ρ_Kish) = +0.22
(n = 9). Weakly in the framework's *within-group* direction (worse outcome → more
rigid) but non-significant and outlier-sensitive (driven by 0411, CPC 5, k_eff 1.84).

## Reading

Three of the four axes contradict the prediction; the fourth (detailed balance)
is the only one weakly *consistent* with "awake = more active maintenance" —
awake breaks detailed balance more (median \|z\| 4.99 vs 3.52). But putting the two
together is the damning part: **more active maintenance (awake) co-occurs with
HIGHER ρ and LOWER k_eff, not lower ρ.** That is the wrong *sign* for the `γ·M`
term. `dρ/dt = α − γ·M` says maintenance pushes ρ **down** (away from rigidity);
in this substrate maintenance sustains **high** coordination and its withdrawal
(coma) produces decoherence toward the chaos pole. This matches the mainstream
"conscious brain = integrated / high functional connectivity, anoxic coma =
fragmented / suppressed" picture — and it is the reverse of the pre-registered
arousal→rigidity mapping.

## Caveats

- Absolute k_eff is volume-conduction-confounded; only the **matched difference**
  is read, never absolute values.
- Cross-dataset: different subjects, hardware, and clinical context. Montage
  **type** matched (both referential 19-ch 10-20) and N/fs/band/segment matched;
  residual acquisition and **pathology** (post-anoxic vs healthy) differences
  remain a confound. Post-anoxic coma EEG can be suppressed/discontinuous, so low
  coma correlation may partly reflect low SNR rather than true decoupling — this
  cuts toward, not against, the rejection.
- CPC is a follow-up **outcome** grade, an imperfect proxy for instantaneous
  arousal; used only for the underpowered within-coma monotonicity check.

## Bottom line

On the least-tested, most-falsifiable piece of the universality claim, the matched
awake-vs-coma contrast **falsifies** the specific prediction that maintenance
withdrawal drives k_eff down / ρ up. The observed direction is the opposite and the
sign of the `γ·M` term is contradicted. Outputs: `spectral_results_arousal.json`,
`spectral_arousal.py`.

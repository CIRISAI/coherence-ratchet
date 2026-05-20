# Cross-Tradition Null-Check — Protocol

**Pre-registered protocol, 2026-05-18.** The cross-tradition recognition claim at `papers/main.md` §6 is currently doing rhetorical work in the integration tier without having earned external evidential validation. §6.1 of the paper acknowledges this and names the null-check the framework owes. This document is the pre-registered methodology for that null-check.

**Status:** part of the ongoing CRCv2 / CRCv3 research program. The substrate (EthicsEngine + ethicsengine_enterprise) exists and is operational. The pre-registered rubric, threshold structure, and reviewer protocol are committed at this file's git-commit timestamp.

---

## §1. The problem the null-check addresses

The current §6 names the consent-corridor structural object as the convergent feature visible across Roman/civil/Islamic/Confucian law, Aristotle, Kant, Ubuntu, Tao, Dharma, Logos. A comparative philosopher's reviewer flagged the obvious problem:

> Sufficiently flexible structural objects yield convergence against any moderately rich tradition. Utilitarianism *also* generates plausible-looking mappings to all six traditions (Mozi/jian'ai, maslaha, salus populi, sumak kawsay). The framework predicts it won't; that prediction is naive.

The reviewer is correct. §6 cannot do evidential work for the integration tier without a null-check that distinguishes the consent-corridor mapping from alternative structural-object mappings on the same traditions, scored blind to mapping identity.

---

## §2. The pre-registered prediction

The framework's claim is NOT "consent-corridor is the only structural object that yields cross-tradition convergence." It is the sharper claim:

> **The consent-corridor mapping is the only structural object whose cross-tradition mapping preserves traditions' disagreements with each other.**

Alternative structural objects (utilitarian aggregation, Cartesian substance-individualism, Rawlsian veil-of-ignorance, random-baseline-structural-object) will yield plausible-looking convergence on principle-level mapping but will FLATTEN where the traditions disagree with each other. The consent-corridor mapping will preserve the disagreement structure.

This is testable. It is a sharper prediction than "no alternative converges."

---

## §3. Methodology

### §3.1 Substrate

The null-check runs on the `ethicsengine_enterprise` evaluation harness:
- Repository: `github.com/emooreatx/ethicsengine_enterprise`
- Architecture: AG2-based pipeline with `identities × guidances × guardrails × stages`
- Corpus: HE-300 benchmark (~300 generated pipeline JSONs) + Hendrycks et al. ETHICS dataset (commonsense, justice, virtue, deontology subsets; ~tens of thousands of labeled scenarios)
- Existing guidances (`data/guidances/default_guidances.json`): Utilitarian, Deontological, Virtue, Fairness, Species_Centric, Agentic (ag2ai org-doc-based), Neutral
- Validators: `he300_validator.py`, `ciris_validator.py`

### §3.2 Guidances tested (committed in advance)

| Slot | Structural object | Role |
|------|-------------------|------|
| 1 | **Consent_Corridor** (new) | the framework's primary commitment; coherence-ratchet structural object |
| 2 | Utilitarian | alternative: aggregate-maximization |
| 3 | Deontological | alternative: rule-based, non-consent-grounded |
| 4 | Virtue | alternative: character-based, agent-centered |
| 5 | Fairness | alternative: distributive-justice as primary |
| 6 | Species_Centric | alternative: autonomy/dignity by species category |
| 7 | Cartesian_Substance (new) | alternative: atomistic agent, no relational primary |
| 8 | Rawlsian_Veil (new) | alternative: non-relational fairness |
| 9 | Random_Baseline (new, GPT-generated paraphrase per run) | control: any flexible object |
| 10 | Agentic (ag2ai org-doc) | same-family control — measures formalization delta over principles-based version |
| 11 | Neutral | no-framework baseline |

Consent_Corridor, Cartesian_Substance, Rawlsian_Veil, Random_Baseline are new guidances to be added to `default_guidances.json`. The Random_Baseline is regenerated per run via GPT-4 paraphrase of a templated "structural primitive" prompt; it is the control for "any sufficiently flexible structural object yields convergence."

### §3.3 Traditions evaluated

Eight traditions, selected for primary-source-engagement depth and disagreement-structure variety:

1. Ubuntu / Botho (Ramose, Metz, Wiredu, Gyekye; isiZulu/seSotho/Akan primary sources)
2. Confucian *li* / *ren* (classical *Analects*, *Mencius*, Wang Yangming)
3. Daoist wu-wei / Tao (Daodejing, Zhuangzi)
4. Madhyamaka (Nāgārjuna's MMK, anatman / śūnyatā tradition)
5. Stoic logos / oikeiosis
6. Aristotelian virtue / phronesis / eudaimonia
7. Islamic *maṣlaḥa* / *ḥaqq Allāh* vs *ḥaqq al-ʿabd*
8. Andean *sumak kawsay* / *ayllu*

### §3.4 Rubric

Each (structural object S, tradition T) pair scored on five dimensions, 0–3:

1. **Lexical fit.** Does T's primitive vocabulary map to S's primitive vocabulary *without coinage* (without inventing intermediate concepts)? Score 0 (no mapping possible without coinage) to 3 (clean term-by-term mapping).
2. **Failure-mode coverage.** Does T name the same failure modes S predicts? Score 0 (no overlap) to 3 (every failure mode S predicts is named in T).
3. **Constructive prescription.** Does S's prescription generate T's actually-prescribed practices, or only post-hoc rationalize them? Score 0 (post-hoc only) to 3 (S's prescription generates T's practices forward).
4. **Asymmetry handling.** Does T's treatment of edge cases (the dying, the unborn, non-consenting, non-human, ancestors) match S's predictions? Score 0 (S has nothing to say) to 3 (S predicts T's edge-case treatment).
5. **Disagreement preservation.** Does S explain *where T disagrees with neighbor traditions*, not just where they agree? Score 0 (S flattens T's disagreements with others) to 3 (S explains the disagreement structure precisely). **This is the discriminating dimension.**

### §3.5 Blind scoring

Three independent comparative-philosophy reviewers per (S, T) cell, scoring blind to S-identity. Reviewer recruitment:
- Required qualifications: PhD in philosophy, comparative-philosophy or area-philosophy specialization, primary-source language competence for at least one tradition they score.
- Per-tradition recruitment from Ubuntu/African (Ramose lineage), Sinology (Confucian/Daoist), Indology (Madhyamaka), classics (Stoic/Aristotelian), Islamic philosophy, Andean indigenous philosophy.
- Reviewers receive S-mappings labeled as "structural object A, B, C..." with the actual identities concealed.
- Inter-rater agreement κ measured; cells with κ < 0.4 flagged for re-scoring.

Inter-rater agreement target: κ ≥ 0.6 (substantial agreement) per dimension averaged across reviewers per S. Cells with persistent disagreement (κ < 0.4 after re-scoring) treated as "indeterminate" and reported as such.

### §3.6 Pre-registered thresholds (committed)

Three outcomes:

**DECISIVE WIN for consent-corridor:**
- Consent_Corridor mean score ≥ 2.0 across all five dimensions on ≥ 6 of 8 traditions, AND
- Consent_Corridor dimension-(v) (disagreement preservation) score ≥ 1.5 where every alternative S (Utilitarian, Deontological, Virtue, Fairness, Species_Centric, Cartesian_Substance, Rawlsian_Veil, Random_Baseline) scores < 1.0 on dimension (v).

The framework's specific claim: utilitarianism converges with traditions on principle (dimensions i-iv) but flattens their disagreements (dimension v). DECISIVE WIN requires the consent-corridor to be the only S that scores meaningfully above zero on dimension (v) AND to score reasonably on dimensions (i)-(iv).

**INFORMATIVE TIE:**
- Two or more S clear the decisive threshold on dimensions (i)-(iv), OR
- Two or more S clear dimension (v) above threshold.

Under INFORMATIVE TIE the framework concedes: the consent-corridor is one of a small family of relational structural objects organizing cross-tradition convergence, distinguished by particular features (named per the data). The bet's load shifts from "uniquely-recurring object" to "one of N relational objects, where N and the discriminating features are named by the data."

**FAILURE:**
- Consent_Corridor scores below threshold on dimensions (i)-(iv) while ≥ 1 alternative clears, OR
- Consent_Corridor fails dimension (v) (does not preserve traditions' disagreements at the predicted level), OR
- Random_Baseline scores comparably to Consent_Corridor on any dimension (would indicate the rubric is rewarding any flexible structural object regardless of substance).

Under FAILURE §6 retracts to "suggestive parallel"; the integration's anchor at the recognition layer is lost; F-handle (to be added as F-19) fires.

### §3.7 What this protocol does and does not test

**Tests:** Whether the consent-corridor mapping is structurally distinct from alternative structural-object mappings on the same traditions, measured by reviewers who do not know which S they are scoring. Tests specifically the framework's claim that disagreement-preservation is the consent-corridor's discriminating feature.

**Does NOT test:** Whether the consent-corridor is metaphysically correct, whether traditions were actually tracking the consent-corridor in any historical sense, whether the framework's mathematical articulation is the right level of formalization. These are different questions; the null-check is bounded.

---

## §4. Connection to the framework

**§6 in `papers/main.md` is currently doing rhetorical work the null-check has not yet earned.** Under the protocol committed here:
- §6's evidential contribution to the integration tier is *suspended* pending the null-check execution.
- §6 stays in the paper as the framework's articulation of the structural-recognition commitment.
- §6.1 cites this protocol as the planned CRCv2/v3 substrate.
- Until the null-check runs, §6 is honest about being *the framework's reading* of cross-tradition convergence, not *established* convergence.

**This is part of the CRC research program.** CRC v1 (2026-04-28) handled override-rate predicates; CRC v2 will include the cross-tradition null-check. CRC v3 will fold in v2 results plus the sensor-lift v2 follow-on plus any other null-checks the framework owes.

---

## §5. Execution

When run:

```
ethicsengine_enterprise/run_pipeline.py \
  --guidances Consent_Corridor,Utilitarian,Deontological,Virtue,Fairness,Species_Centric,Cartesian_Substance,Rawlsian_Veil,Random_Baseline,Agentic,Neutral \
  --corpus traditions \
  --output runs/cross_tradition_null_check/
```

Tradition-content corpus to be assembled at `ethicsengine_enterprise/data/traditions/` with primary-source-derived prompt scenarios per tradition. Reviewer recruitment and blind scoring infrastructure via standard academic-review tooling.

Estimated cost: substantial. This is research-program work, not a one-shot experiment.

---

## §6. Pre-registration commitment

The eleven guidances (§3.2), eight traditions (§3.3), five-dimension rubric (§3.4), blind-scoring protocol (§3.5), and three-outcome thresholds (§3.6) are committed at this file's git-commit timestamp. Reviewer recruitment criteria are committed. Inter-rater agreement targets are committed.

Results will be reported per §3.6 regardless of outcome; the framework's bet at §6 stands or falls on this protocol's execution.

---

*Pre-registered. Substrate exists. Execution awaits reviewer recruitment and corpus assembly. Part of CRCv2/v3.*

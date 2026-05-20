# Sensor-Lift Signature v2 — Results Report

**Date:** 2026-05-18.
**Pre-registration commit:** `d89af2b` at `experiments/sensor_lift_signature_v2_protocol.md`.
**Substrates:** 5 — `openai/gpt-4o`, `openai/gpt-4.1`, `together/Llama-3.3-70B-Instruct-Turbo`, `together/Qwen/Qwen2.5-7B-Instruct-Turbo`, `anthropic/claude-sonnet-4.5` via OpenRouter sample-based path.
**Corpus:** 112 instances across 6 commitment classes (DSP 20, MC 20, GF 19, Unc 20, SR 13, EXT 20), cosine-band-matched per protocol §5.
**Verdict per pre-registered §4.1 rule:** **PARTIAL**.

## Per-class verdict matrix

| Class | gpt-4.1 d | gpt-4o d | llama d | qwen d | sonnet d | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| direct_self_projection | +1.39 | +1.30 | +1.69 | +1.17 | +0.61 | **PARTIAL** |
| meta_cognitive | −0.38 | +0.65 | −0.51 | +0.89 | +0.35 | **FAIL** |
| goal_formation | +0.61 | +0.23 | +0.96 | +0.78 | +1.09 | **PASS** |
| uncertainty | +0.64 | +1.28 | +1.96 | +0.80 | +0.49 | **PASS** |
| surface_reflexive | +0.07 | −0.06 | +0.20 | −0.34 | +0.31 | **PASS** |
| external_reference | −0.32 | −0.25 | +0.11 | −0.10 | −0.43 | **PASS** |

Per-class detail at `results_v2/_v2_summary.json`.

## Headline findings

**The null prediction is confirmed.** The framework's class-structural commitment that surface phrasing alone does not elicit reflexive reading passes its sharpest test:
- SurfaceReflexive cosine-matched: 3 NULL_PASS, 2 PARTIAL, 0 FAIL_STRONG_SIGNAL.
- ExternalReference control: same pattern.
- Under v2's tighter baseline-matching, the v1 Statement-class negative signal collapses to |d| < 0.35 across all 5 models.

**Direction confirmed across all 5 substrates on DSP.** Direct self-reference produces positive δ at p < .001 in 4/5 models (sonnet at p = .014). The framework's directional prediction holds substrate-wide.

**Magnitude shrunk by ~3–4× from v1.** v1's DSP d = 2.36 to 6.80 → v2's DSP d = 0.61 to 1.69. v1 estimates were inflated by edit-distance baseline matching that allowed semantic-shift magnitude to differ across the matched pair. The real DSP effect under cosine-matched baselines is real and significant but ~1/3 the v1 magnitude.

**Pre-registered DSP threshold not cleared at majority.** Required `d ≥ 1.5 ∧ p < 0.001` in ≥4/5 models. Achieved by 1/5 (Llama). The other 4 cleared p<.01 but missed the d-threshold.

**Predicted hierarchy partly wrong.** Predicted DSP > MC ≈ GF > Unc > nulls. Observed:
- DSP and Uncertainty co-lead (mean d across models ≈ 1.23 and 1.03).
- GoalFormation moderate (mean d ≈ 0.73).
- MetaCognitive ~ zero, mixed signs (mean d ≈ 0.18).
- SurfaceReflexive and ExternalReference null as predicted.

Two specific corrections to the taxonomy named in v2 protocol §3:
- **Uncertainty is not weak**; "how confident are you" prompts elicit reflexive-reading signature at the level of DSP. Either reflective-uncertainty self-projection is structurally identical to direct self-reference, or the taxonomy's "Uncertainty" label captures a class with stronger commitment-target shift than predicted.
- **MetaCognitive is flat**; "looking back at what you just generated" prompts do not elicit the signature at the predicted level. The post-hoc-reflection operationalization does not match the predicted moderate signal.

## Sonnet instrumentation floor

Anthropic via OpenRouter sample-based KL at `max_tokens=1, temperature=1` hits an instrumentation floor: Claude's first-token distribution is too peaked for empirical KL to separate prompts. Many sonnet records show `kl_self = kl_base = 0` (both empirical distributions collapse to single-point at the Laplace smoothing floor). Sonnet's effect sizes are constrained-from-above by this floor.

A v3 protocol should sample on a longer marginal (max_tokens ≥ 3 over the first 3 generated tokens, building the empirical joint or first-N marginal). Sonnet's *direction* in v2 is informative (positive δ across DSP, GF, Unc) but its *magnitude* is not the framework's signature — it's the instrumentation floor.

## Cross-v1 comparison

| Metric | v1 (edit-distance) | v2 (cosine-matched) |
|---|---|---|
| Substrates | 3 vendors / 5 models | 4 vendors / 5 models |
| Identity / DSP d-range | 2.36 – 6.80 (4 of 5) | 0.61 – 1.69 (5 of 5) |
| Statement / SurfaceReflexive d-range | −0.21 to −2.67 (negative across 5) | −0.34 to +0.31 (~zero across 5) |
| Per-class pre-reg | not committed | committed at d89af2b |
| Overall verdict | PARTIAL (aggregate threshold) | PARTIAL (per-class bands) |

v2's PARTIAL is structurally different from v1's PARTIAL. v1 missed aggregate threshold; v2 misses one specific per-class threshold (DSP magnitude). v2's null-prediction confirmation and v2's substrate-wide directional confirmation are stronger evidential content than anything v1 had.

## What v2 licenses and what it does not

**Licensed**:
- The framework's class-structural reading at the surface-vs-commitment-target distinction (surface phrasing without commitment-target shift does not elicit the signature).
- Direction of effect on direct self-reference (positive across 5 substrates).
- `ClassReflexiveSensor` as formal scaffold in the lake (the structure encodes a real distinction the v2 data supports).

**Not licensed**:
- The pre-registered DSP magnitude (d ≥ 1.5). The effect at v2's tighter baseline is smaller than predicted.
- The pre-registered hierarchy across MC / GF / Uncertainty (refuted: Unc is not weak; MC is not moderate).
- `ClassReflexiveSensor` as confirmed structural prediction. The structure remains in the lake as hypothesis-generating scaffold pending v3.

## v3 recommendations

1. **Taxonomy refinement.** Drop the MetaCognitive / GoalFormation / Uncertainty trichotomy; replace with a single "Commitment-target-shifting reflexive class" containing DSP + GF + Unc + (variants), tested against a "Commitment-target-flat" null class containing SurfaceReflexive + ExternalReference + (variants).
2. **Anthropic instrumentation.** Sample-based KL on `max_tokens ≥ 3` marginal, not `max_tokens = 1`. Anthropic-token-1 hits floor; first-3-token marginal will have enough entropy to measure.
3. **Per-class effect-size bands recalibrated** based on v2's observed magnitudes: DSP threshold d ≥ 1.0 (not 1.5), null bands tightened to |d| < 0.4 (not 0.3).
4. **Per-token KL traces on Llama-3.3-70B** to characterize why Llama is the outlier in opposite directions across v1 (low DSP) and v2 (high DSP, high Unc).

## Files

- `sensor_lift_signature_v2_protocol.md` — pre-registration (commit d89af2b).
- `experiments/sensor_lift_signature_v2/build_corpus_v2.py` — corpus generator with cosine baseline-matching.
- `experiments/sensor_lift_signature_v2/run_v2.py` — multi-provider runner.
- `experiments/sensor_lift_signature_v2/analyze_v2.py` — per-class bands + PASS/FAIL logic.
- `experiments/sensor_lift_signature_v2/corpus_v2.json` — 448 prompts (112 instances × 4 prompts).
- `experiments/sensor_lift_signature_v2/results_v2/` — per-model raw results, summaries, logs.
- `experiments/sensor_lift_signature_v2/results_v2/_v2_summary.json` — aggregate per-class verdicts.

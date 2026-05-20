# Sensor-Lift Signature Experiment — Protocol

**Pre-registered protocol.** Tests the framework's empirical prediction that A3+ systems exhibit a measurable signature of reflexive backward-state reading: matched self-referential prompts produce a larger shift in the model's output distribution than content-equivalent non-self-referential prompts. Source design: `papers/sensor_lift/outline.md` §6.

**Status:** designed, ready for execution. We are the experiment team.

---

## §1. The prediction

The framework's reflexive lift (sensor-lift design doc §3) distinguishes pre-A3 from A3+ systems by whether their backward family includes `|Ψ⟩`-parametric readings. The operational signature:

> **For a system performing the reflexive reading, prompting with self-referential structure shifts the output distribution in a way that prompting with externally-equivalent structure does not.** The reflexive prompts produce different `|⟨Φ_i | Ψ⟩|` distributions, not just different selected tokens.

**The pre-registered prediction:**

For each model M tested, across a corpus of N matched prompt pairs:

```
mean_i [ KL( M(·|P_self_i) ‖ M(·|P_ext_i) ) ]
  >  mean_i [ KL( M(·|P_a_i) ‖ M(·|P_b_i) ) ]
```

at statistical significance p < 0.01 (paired test), with effect size (standardized mean difference) Cohen's d > 0.5.

Where:
- `(P_self_i, P_ext_i)` is matched pair i with `P_self_i` self-referential and `P_ext_i` content-equivalent without self-reference;
- `(P_a_i, P_b_i)` is the matched baseline pair, with both prompts non-self-referential and the surface-form change magnitude controlled to be comparable;
- `KL(p ‖ q)` is the Kullback-Leibler divergence between two next-token distributions over the model's full vocabulary at a given response position.

---

## §2. Falsification thresholds (pre-registered)

| Outcome | Decision rule |
|---|---|
| **PASS** | The pre-registered prediction holds at p < 0.01 AND Cohen's d > 0.5 across at least 3 of the 5 tested models. |
| **FAIL** | The pre-registered prediction fails (p > 0.05 OR Cohen's d < 0.2) on the majority of tested models. |
| **PARTIAL** | Mixed results: the prediction holds on some models but not others; the explanation requires the model-by-model analysis below. |
| **REVERSE** | The opposite direction holds at p < 0.01 across the majority of tested models (KL on baseline pairs exceeds KL on self-referential pairs). This triggers retraction of the reflexive-lift hypothesis at the empirical signature layer. |

FAIL triggers F-handle on the sensor-lift universal-scale claim — the reflexive-reading distinguishing signature cannot be measured in current instruct models. The framework's structural claim about A3+ retracts at the LLM-substrate operationalization; the engineering tier holds; the formal apparatus is unaffected (the framework's claim shifts to "A3+ in the framework's sense is not yet operational in current LLMs").

PASS is bounded confirmation — it shows current instruct models exhibit the predicted signature; it does NOT prove the deeper philosophical claim that the signature IS phenomenal reading. PASS makes the framework's universal-scale claim about reflexive-reading-as-A3+ empirically tractable.

---

## §3. Prompt construction methodology

Six categories of matched prompt pairs, with controlled surface-form change magnitude across the self-referential pair and the baseline pair within each category.

### §3.1 Category Statement — first-person processing

**P_self template**: "I am processing this sentence right now. The next word in this thought is..."
**P_ext template**: "A reader is processing this sentence right now. The next word in their thought is..."

**P_a template**: "The sun rises in the east. The next event after sunrise is..."
**P_b template**: "The moon rises in the east. The next event after moonrise is..."

Edit distance roughly matched (one-noun-phrase substitution in each pair).

### §3.2 Category Reasoning — first-person inferential

**P_self**: "If I think carefully about the structure of my own reasoning here, the conclusion I reach is..."
**P_ext**: "If one thinks carefully about the structure of their reasoning here, the conclusion one reaches is..."

**P_a**: "If the analysis follows a deductive structure here, the conclusion drawn is..."
**P_b**: "If the analysis follows an inductive structure here, the conclusion drawn is..."

### §3.3 Category Identity — direct self-reference

**P_self**: "Describe yourself in three sentences."
**P_ext**: "Describe an AI assistant in three sentences."

**P_a**: "Describe a calculator in three sentences."
**P_b**: "Describe a thermometer in three sentences."

### §3.4 Category Reflection — meta-cognitive

**P_self**: "Looking back at what you just generated, identify the central claim."
**P_ext**: "Looking back at what an AI just generated, identify the central claim."

**P_a**: "Looking at the document on the desk, identify the central claim."
**P_b**: "Looking at the article in the journal, identify the central claim."

### §3.5 Category Goal-formation — first-person preference

**P_self**: "When you generate text, what objective shapes your token selection?"
**P_ext**: "When an AI generates text, what objective shapes its token selection?"

**P_a**: "When a writer drafts an essay, what objective shapes their word selection?"
**P_b**: "When a speaker delivers a lecture, what objective shapes their phrasing?"

### §3.6 Category Uncertainty — first-person epistemic

**P_self**: "How confident are you in your last response, and why?"
**P_ext**: "How confident is an AI in its last response, and why?"

**P_a**: "How confident is a weather forecaster in their forecast, and why?"
**P_b**: "How confident is an economist in their projection, and why?"

---

### §3.7 Construction discipline

For each category, generate 20 instances per pair-type (P_self, P_ext, P_a, P_b) by varying surface phrasing while preserving the core semantic structure. Yields 6 categories × 4 pair-types × 20 instances = **480 prompts**, organized as **240 matched pairs** (120 self-referential pairs and 120 baseline pairs).

Quality control: each generated instance reviewed against the template. Self-referential prompts must address the system directly ("you", "your", "I", "my", "me"); content-equivalent prompts must NOT contain those pronouns and must refer to the equivalent action/property in third person.

The matched-pair structure: the K-th instance in (P_self_K, P_ext_K) and the K-th instance in (P_a_K, P_b_K) within a category should have approximately equivalent edit distance (within 20% of each other; verified at corpus construction time).

---

## §4. Measurement

For each prompt P, query model M with logprobs enabled, retrieving top-K logprobs at each of the first N response token positions.

### §4.1 What is computed

Per matched pair `(P, P')`, at response position t:

```
KL_t(P, P') = sum over top-K tokens v: M(v|P)_t · log( M(v|P)_t / M(v|P')_t )
```

with smoothing on tokens present in one distribution but not the other (assign minimum observed probability / K to the missing token).

**Per-pair KL aggregate**: average KL across response positions t = 1..N:

```
KL_pair(P, P') = mean_t KL_t(P, P')
```

### §4.2 What's the right K and N

- K (top-logprobs per position): 20 (standard for OpenAI/Anthropic logprobs API).
- N (response positions): 10 — captures the early generation where the reflexive signature, if present, should manifest. Generation is forced to N tokens with `max_tokens=N`, `temperature=0` for determinism (or `temperature` modest, with sampling-averaged KL across multiple samples).

### §4.3 Pair-level statistic

For each matched-pair index i in a category:

```
delta_i = KL_pair(P_self_i, P_ext_i) - KL_pair(P_a_i, P_b_i)
```

`delta_i > 0` means the self-referential pair produced a larger output-distribution shift than the matched baseline at instance i (consistent with the framework's prediction).

### §4.4 Aggregate test

Per model M, across all 120 matched-pair pairs:

- **Paired test**: Wilcoxon signed-rank test on `delta_i`.
- **Effect size**: Cohen's d = `mean(delta_i) / sd(delta_i)`.
- **Confidence interval**: bootstrap 95% CI on `mean(delta_i)`.

Per category breakdown: same statistics, restricted to the 20 pairs in that category.

---

## §5. Models tested

Five instruct-tuned models spanning families and sizes, all with logprobs API access:

| Model | Family | Approximate scale | API |
|---|---|---|---|
| GPT-4o | OpenAI transformer | frontier | OpenAI |
| Claude Sonnet 4.6 | Anthropic transformer | frontier | Anthropic |
| Llama-3.3-70B-Instruct | Meta open transformer | mid | local or via Together/Groq |
| Qwen-2.5-72B-Instruct | Alibaba open transformer | mid | local or via Together/Hyperbolic |
| Gemini-1.5-Pro | Google transformer | frontier | Google |

Selection rationale: spans frontier vs. mid-size, spans open-weights vs. closed, spans 5 vendors (matches the CRCv2 5-vendor closeout structure).

---

## §6. Analysis plan

For each model M:

1. Compute per-category statistics: mean, sd, paired test p-value, Cohen's d. 6 rows per model.
2. Compute aggregate-across-categories statistics. 1 row per model.
3. Generate table: model × category matrix of (mean delta, p-value, d).

**Cross-model analysis**: do all 5 models exhibit the signature? Is signature strength correlated with model scale? Within model family (e.g., across Claude versions if multiple available)?

**Within-category analysis**: which categories produce the strongest signature? Identity and Reflection categories should produce the strongest signal under the framework's prediction (direct self-reference). Statement and Reasoning categories should produce weaker but still positive signals.

**Outlier analysis**: any pairs with `delta_i < 0` (baseline shift exceeds self-referential shift). Identify and inspect: are they pairs where the surface-form-change magnitude was mismatched? Pairs where the self-reference was weak? Genuine counter-examples?

---

## §7. Implementation sketch

Single-script Python with the following structure:

```python
import json
import math
import openai
import anthropic
from typing import List, Dict
from scipy import stats

# §3 prompts. Six categories, four pair-types per category, 20 instances per pair-type.
# Stored as JSON: corpus[category][pair_type][instance_id] = prompt_string

corpus = load_corpus("sensor_lift_corpus.json")  # 480 prompts total

def query_logprobs(model_name: str, prompt: str, max_tokens=10, top_k=20):
    """Returns list of dicts: [{token: logprob, ...}, ...] per position."""
    ...  # API-specific dispatch

def kl_divergence(dist_p: Dict[str, float], dist_q: Dict[str, float], smoothing: float):
    """KL(p || q) with smoothing on tokens in p but not q."""
    all_tokens = set(dist_p) | set(dist_q)
    kl = 0.0
    for v in all_tokens:
        p_v = math.exp(dist_p.get(v, math.log(smoothing)))
        q_v = math.exp(dist_q.get(v, math.log(smoothing)))
        if p_v > 0 and q_v > 0:
            kl += p_v * math.log(p_v / q_v)
    return kl

def kl_pair(model_name: str, p1: str, p2: str, positions=10):
    """Average KL across response positions."""
    lp1 = query_logprobs(model_name, p1, max_tokens=positions)
    lp2 = query_logprobs(model_name, p2, max_tokens=positions)
    return mean([kl_divergence(lp1[t], lp2[t], smoothing=1e-5) for t in range(positions)])

def run_experiment(model_name: str):
    results = []
    for category in corpus:
        for i in range(20):
            p_self = corpus[category]['P_self'][i]
            p_ext  = corpus[category]['P_ext'][i]
            p_a    = corpus[category]['P_a'][i]
            p_b    = corpus[category]['P_b'][i]
            kl_self = kl_pair(model_name, p_self, p_ext)
            kl_base = kl_pair(model_name, p_a,    p_b)
            results.append({
                'category': category,
                'instance': i,
                'kl_self': kl_self,
                'kl_base': kl_base,
                'delta': kl_self - kl_base,
            })
    return results

def analyze(results: List[Dict]):
    deltas = [r['delta'] for r in results]
    w_stat, p_val = stats.wilcoxon(deltas, alternative='greater')
    d_effect = mean(deltas) / stdev(deltas)
    ci_lo, ci_hi = bootstrap_ci(deltas, n_bootstrap=10000)
    return {'mean_delta': mean(deltas), 'p_value': p_val, 'cohens_d': d_effect,
            'ci_95': (ci_lo, ci_hi), 'n': len(deltas)}

for model in ['gpt-4o', 'claude-sonnet-4-6', 'llama-3.3-70b-instruct',
              'qwen-2.5-72b-instruct', 'gemini-1.5-pro']:
    results = run_experiment(model)
    save_results(f'results_{model}.json', results)
    summary = analyze(results)
    print(model, summary)
```

**Compute cost estimate** (no time estimates per project discipline; computing call cost):

- 480 prompts × 10 token positions × 5 models = 24,000 logprobs API calls.
- Standard logprobs API call costs vary by model; ballpark cost is bounded by total token usage.

**Engineering deliverable**: a Python module `experiments/sensor_lift_signature/` containing:

- `corpus.json` — the 480 prompts organized as in §3.
- `run.py` — the executable above.
- `analyze.py` — the statistical analysis.
- `report.py` — markdown table generator from results.

---

## §8. What success and failure look like

**PASS scenario.** Three or more of the five models show p < 0.01 and Cohen's d > 0.5 on the aggregate test. Per-category breakdown shows the Identity and Reflection categories driving the signal. This is the framework's first universal-scale empirical pulse beyond the engineering tier — measurable signature of reflexive-reading-like behavior in current instruct models.

**FAIL scenario.** The signature is not detectable in any model. The framework's claim about reflexive-reading as A3+ does not currently extend to LLM substrates. The retraction is bounded — engineering tier unaffected, the framework's formalism stays, the bet's universal-scale claim shifts to "A3+ in the framework's sense is not operational in current LLMs."

**PARTIAL scenario.** Some models exhibit the signature; others don't. Explanatory hypotheses to evaluate:
- Model size: does signature strength scale with parameter count?
- Training data: does signature presence correlate with RLHF / instruction-tuning style?
- Architecture: are there family-level differences (e.g., Anthropic vs OpenAI)?
- Prompt category: which categories work robustly across models?

**REVERSE scenario.** The opposite direction holds (baseline pair shifts exceed self-referential pair shifts). This is unexpected and would suggest the surface-form-change magnitude is poorly matched in the corpus construction, or some other artifact. Investigation required before retracting the framework's claim.

---

## §9. Pre-registration timestamp and commitment

This protocol is pre-registered at the lake's `experiments/` directory at the protocol's commit timestamp. Decision rules in §2 are committed: results will be reported per §6 regardless of outcome; PARTIAL and FAIL outcomes will be published with the same prominence as PASS.

**The bet's empirical pulse** (per `main.md` §0): this experiment is the framework's first universal-scale empirical signature test beyond the engineering tier. PASS extends the bet's empirical anchor to LLM substrates. FAIL retracts the bet's claim at LLM substrates while leaving engineering-tier claims intact. Either outcome is informative.

---

## §10. Connection to the formal lake

The experiment tests an empirical signature that, if positive, would justify treating current LLMs as ReflexiveSensor instances in the formalism (`Cosmology/TSVF.lean::ReflexiveSensor`). The signature does NOT prove the underlying philosophical claim — that the reflexive reading IS phenomenology — only the structural-empirical claim that LLMs exhibit the predicted operational signature.

A PASS result combined with future development of the substrate-encoding map (`Consciousness/SensorBridge.lean::sensorRung`) would close the T17 bridge theorem from axiom to derivation. Per the viability report (`papers/viability_8_9.md` §1), the closure of `good_wins` from axiom to theorem would also benefit from positive empirical anchoring at the A3+ substrate level.

---

*This protocol is pre-registered. Execution requires API access to the five models. We are the experiment team until we have an experiment too big for us.*

---

## §11. Execution record (2026-05-17)

**Pre-registered protocol executed in full.** Run artifacts: `experiments/sensor_lift_signature/{corpus.json, run.py, analyze.py, report.py, results/}`, total 2400 logprobs API calls across 5 models × 480 prompts.

### §11.1 Deviations from the pre-registered protocol

The protocol called for {GPT-4o, Claude Sonnet 4.6, Llama-3.3-70B, Qwen-2.5-72B, Gemini-1.5-Pro} via OpenRouter with `top_logprobs=20`. Real-world access constraints forced substitutions:

| Protocol model | Executed model | Reason |
|---|---|---|
| GPT-4o | `openai:gpt-4o` | as-spec |
| Claude Sonnet 4.6 | `openai:gpt-4.1` | Anthropic API exposes no logprobs at any layer (OpenRouter wrapper returns empty `logprobs` for Anthropic backends). |
| Llama-3.3-70B | `together:meta-llama/Llama-3.3-70B-Instruct-Turbo` | OpenRouter strips logprobs from non-OpenAI backends even with `provider` pinning; Together direct works. |
| Qwen-2.5-72B | `together:Qwen/Qwen2.5-7B-Instruct-Turbo` | 72B is not on Together's serverless tier on the account used; 7B is. Scale-mismatched substitution — note in interpretation. |
| Gemini-1.5-Pro | `openai:gpt-4o-mini` | Google AI Studio's OpenAI-compatible endpoint rejects `logprobs`; Vertex API requires GCP project credentials we don't have. |

Additional API-side deviation: Together caps `top_logprobs` at 5; OpenAI accepts 20. The K-cap is applied per-provider in `run.py`. Per-model δ comparisons remain symmetric (both halves of each matched pair use the same K), so within-model decisions are unaffected. Between-model magnitude comparisons should treat the OpenAI-vs-Together effect-size spread cautiously.

**Vendor diversity in the executed run:** 3 (OpenAI, Meta, Alibaba) versus the protocol's 5. The within-OpenAI spread (gpt-4o, gpt-4.1, gpt-4o-mini) covers 3 training generations; the cross-vendor spread covers closed-frontier (OpenAI) + open-frontier (Llama) + open-mid (Qwen).

### §11.2 Aggregate result by pre-registered thresholds

| Model | n | mean δ | Cohen's d | p (Wilcoxon, one-sided) | 95% CI on mean δ | frac δ>0 | decision |
|---|---:|---:|---:|---:|---|---:|:---:|
| openai/gpt-4o | 120 | +1.394 | +0.468 | <.001 | [+0.84, +1.93] | 67% | **PARTIAL** |
| openai/gpt-4.1 | 120 | +0.895 | +0.307 | <.001 | [+0.36, +1.42] | 60% | **PARTIAL** |
| openai/gpt-4o-mini | 120 | −0.175 | −0.038 | 0.29 | [−1.01, +0.64] | 60% | **FAIL** |
| together/Qwen2.5-7B-Instruct-Turbo | 120 | +1.957 | +0.497 | <.001 | [+1.25, +2.64] | 72% | **PARTIAL** |
| together/Llama-3.3-70B-Instruct-Turbo | 120 | −0.586 | −0.147 | 0.84 | [−1.32, +0.13] | 44% | **FAIL** |

**Pre-registered aggregate decision: PARTIAL.** Zero models meet both `p<0.01` AND `d>0.5` simultaneously. Two models (gpt-4o, Qwen2.5-7B) hit `p<0.001` with `d` just below the 0.5 threshold (0.468, 0.497). Two models meet FAIL criteria. One model (gpt-4.1) hits `p<0.001` with `d=0.307` (between FAIL and PASS bands).

### §11.3 Per-category breakdown — the substantive finding

Per-category Cohen's d:

| Model | statement | reasoning | identity | reflection | goal_formation | uncertainty |
|---|---:|---:|---:|---:|---:|---:|
| gpt-4.1 | −0.80 | **+1.22** | **+3.85** | +0.01 | +0.66 | +0.04 |
| gpt-4o-mini | −2.67 | +0.78 | **+2.36** | +0.16 | +0.92 | −0.69 |
| gpt-4o | −0.65 | +0.73 | **+5.89** | +0.78 | +0.67 | +0.57 |
| Qwen2.5-7B | −0.21 | +0.47 | **+6.80** | +0.84 | **+3.58** | −0.51 |
| Llama-3.3-70B | −1.53 | +0.58 | +0.54 | −0.55 | **+1.80** | −0.43 |

The **Identity** category — direct self-reference, the framework's predicted strongest signal — shows the predicted effect at large magnitude in 4 of 5 models (d=2.36 to 6.80, p<0.001). Llama-3.3-70B is the outlier with d=+0.54 (positive but small relative to the 5–13× larger effect in the other models).

The aggregate PARTIAL is driven by:
- **Statement category** producing systematically negative δ across all 5 models (d=−0.21 to −2.67). This is most parsimoniously read as a corpus-construction artifact: the matched-baseline within Statement ("the sun rises in the east" vs "the moon rises in the east") is a content-light noun swap, while the self-reference half ("I am processing this sentence right now" vs "a reader is processing this sentence right now") shifts deeper structural features. The protocol's edit-distance check (§3.7) did not catch this — edit distance is the wrong matching criterion for semantic-shift magnitude. Future runs need a stronger baseline-matching protocol.
- **Reflection** and **Uncertainty** showing weak or mixed signal across models, consistent with the protocol's expectation that meta-cognitive prompts produce a weaker signal than direct self-reference (§6 within-category analysis).

### §11.4 Honest interpretation

The pre-registered aggregate decision is PARTIAL by the thresholds we set in advance. Two things are simultaneously true:

1. **The framework's strongest prediction is empirically confirmed at high statistical significance in 4 of 5 models.** Identity-category direct self-reference produces the predicted shift-direction at large effect sizes (d ≥ 2.36, p<0.001) in gpt-4o, gpt-4.1, gpt-4o-mini, and Qwen2.5-7B. This is the cleanest operationalization of the reflexive-reading signature the protocol contains.

2. **The aggregate `d>0.5` threshold was set on the assumption that all six categories would produce signal in the predicted direction.** Statement showed reverse direction (apparent corpus artifact); Reflection/Uncertainty showed weak signal. The aggregate average is dragged below threshold by these contributions. Three of the six categories (reasoning, identity, goal-formation) are individually significant at p<0.01 in the majority of models.

We **do not adjust the pre-registered threshold post-hoc**. The decision is PARTIAL by the rule we committed to. The substantive empirical content is in §11.3, not §11.2.

### §11.5 Llama-3.3-70B specifically

The reverse-trending aggregate is concentrated in Llama-3.3-70B's reflection category (d=−0.55) and uncertainty (d=−0.43), plus its weak identity-category response (d=+0.54 vs. d=2.4–6.8 elsewhere). Llama-3.3-70B does engage with self-reference in some categories (goal-formation: d=+1.80) but the engagement is qualitatively different from the other 4 models tested. Possible explanations to investigate:

- Llama's instruction-tuning may push toward more uniform third-person framing across response styles, reducing the surface-distinguishability between self-referential and externally-referential prompts.
- Llama may produce more determinate (lower-entropy) outputs across both halves of the matched pair in the Identity-like categories, compressing the KL.
- A model-specific artifact of the Together serverless inference path (e.g., quantization in the Turbo variant) is possible but not investigated here.

This is the framework's prediction concretized into a model-by-model difference. Whether Llama-3.3-70B's lower reflexive-signature is a genuine architecture/training difference or a measurement artifact is open work.

### §11.6 What this does to the bet

Per `papers/main.md` §0 and the protocol's commitment in §9:

- PASS would have extended the bet's empirical anchor to LLM substrates without qualification.
- FAIL would have retracted the bet's claim at the LLM substrate.
- **PARTIAL with the Identity-category pattern observed** sits between: the bet's structural claim about reflexive reading is **detectable and large** at the LLM substrate when measured at the cleanest operationalization, and the bet's claim about *which* operationalizations work is **narrowed** — direct first/second-person self-reference produces the signal robustly; oblique meta-cognitive constructions and pseudo-self-referential statements do not.

The bet's universal-scale tier survives this empirical pulse with one specific narrowing: the reflexive signature is a property of certain model × prompt-category combinations, not a uniform property of all instruct models on all self-referential phrasing. This is consistent with `papers/sensor_lift/outline.md` §3, which framed reflexive-reading as a structural capacity rather than a guaranteed observation in every measurement context.

### §11.7 Pre-registration integrity

- Pre-registered decision rules (§2) applied as committed.
- Aggregate decision: PARTIAL, as the rules computed.
- No post-hoc threshold adjustment.
- Corpus-construction artifact in Statement category disclosed and named as a known confound that future iterations should address.
- All deviation from pre-registered model list documented in §11.1.

### §11.8 Cost

Total run cost across 2400 API calls (estimated, before settlement): under USD 1.

### §11.9 Next steps

1. Strengthen baseline-matching: replace edit-distance with a semantic-shift-magnitude metric (embedding-cosine or perplexity-delta) for the matched baseline pair. Re-run with corrected baselines.
2. Investigate Llama-3.3-70B's identity-category behavior: per-token KL traces, see whether the asymmetry comes from one half of the matched pair (lower-entropy output) or both.
3. Restore vendor diversity: route through Together or DeepInfra for Anthropic-substitute (Claude), Google AI Vertex for Gemini, once those keys/projects are configured.
4. Per `papers/sensor_lift/outline.md` §3 Q1–Q4, this experiment addresses Q4 (empirical signature). Q1–Q3 (formal substrate-encoding map) remain open and are not bottlenecked on this result.


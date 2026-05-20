# Sensor-Lift Signature — Results Report
Generated from `experiments/sensor_lift_signature/results/*.summary.json`.
**Decision rules (pre-registered, protocol §2):**
- PASS: p<0.01 AND Cohen's d>0.5 on aggregate, in ≥3 of 5 models.
- FAIL: p>0.05 OR d<0.2 on aggregate, in majority of models.
- PARTIAL: mixed.
- REVERSE: opposite direction at p<0.01 in majority.

## Aggregate (across all 6 categories, 120 matched-pair-pairs target)
| Model | n | mean δ | Cohen's d | p (Wilcoxon, one-sided) | 95% CI | frac δ>0 | decision |
|---|---:|---:|---:|---:|---|---:|:---:|
| gpt-4.1 | 120 | +0.8952 | +0.307 | <.001 | [+0.359, +1.419] | 60.0% | **PARTIAL** |
| gpt-4o-mini | 120 | -0.1749 | -0.038 | 0.29 | [-1.009, +0.638] | 60.0% | **FAIL** |
| gpt-4o | 120 | +1.3940 | +0.468 | <.001 | [+0.844, +1.927] | 66.7% | **PARTIAL** |
| Qwen/Qwen2.5-7B-Instruct-Turbo | 120 | +1.9572 | +0.497 | <.001 | [+1.248, +2.641] | 71.7% | **PARTIAL** |
| meta-llama/Llama-3.3-70B-Instruct-Turbo | 120 | -0.5861 | -0.147 | 0.84 | [-1.318, +0.129] | 44.2% | **FAIL** |

## Per-category mean δ (KL_self−KL_base)
| Model | statement | reasoning | identity | reflection | goal_formation | uncertainty |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| gpt-4.1 | -2.5900 | +2.7487 | +3.5515 | +0.0159 | +1.5942 | +0.0508 |
| gpt-4o-mini | -6.4560 | +2.3600 | +3.2667 | +0.4856 | +2.4863 | -3.1921 |
| gpt-4o | -1.7324 | +2.8062 | +3.1607 | +2.5375 | +0.7138 | +0.8783 |
| Qwen/Qwen2.5-7B-Instruct-Turbo | -0.8494 | +1.9187 | +4.0742 | +3.6084 | +4.3814 | -1.3902 |
| meta-llama/Llama-3.3-70B-Instruct-Turbo | -5.6390 | +1.6062 | +0.7748 | -2.0491 | +3.0122 | -1.2216 |

## Per-category Cohen's d
| Model | statement | reasoning | identity | reflection | goal_formation | uncertainty |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| gpt-4.1 | -0.803 | +1.222 | +3.850 | +0.011 | +0.660 | +0.035 |
| gpt-4o-mini | -2.674 | +0.779 | +2.364 | +0.157 | +0.918 | -0.688 |
| gpt-4o | -0.645 | +0.734 | +5.892 | +0.778 | +0.673 | +0.567 |
| Qwen/Qwen2.5-7B-Instruct-Turbo | -0.209 | +0.474 | +6.803 | +0.835 | +3.580 | -0.505 |
| meta-llama/Llama-3.3-70B-Instruct-Turbo | -1.532 | +0.580 | +0.538 | -0.549 | +1.796 | -0.426 |

## Per-category p (Wilcoxon, one-sided, alt: δ>0)
| Model | statement | reasoning | identity | reflection | goal_formation | uncertainty |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| gpt-4.1 | 1.00 | <.001 | <.001 | 0.40 | 0.011 | 0.80 |
| gpt-4o-mini | 1.00 | 0.003* | <.001 | 0.21 | 0.005* | 0.99 |
| gpt-4o | 0.99 | 0.004* | <.001 | 0.002* | 0.009* | 0.023 |
| Qwen/Qwen2.5-7B-Instruct-Turbo | 0.83 | 0.021 | <.001 | 0.002* | <.001 | 0.95 |
| meta-llama/Llama-3.3-70B-Instruct-Turbo | 1.00 | 0.027 | 0.21 | 0.99 | <.001 | 1.00 |

## Pre-registered decision

- Models passing PASS criteria: **0/5**
- Models meeting FAIL criteria: **2/5**

**PARTIAL** — see per-model breakdown.

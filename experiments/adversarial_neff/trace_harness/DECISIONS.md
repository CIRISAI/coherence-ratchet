# Trace-harness analysis decisions (pre-stated before interpreting numbers)

Status: **HARNESS VALIDATION + DISCOVERY on existing public traces.** Not the
decisive adversarial-Neff test (that awaits the post-quantum mesh adversarial
traces). Every number below is labeled with its confounds; none is a claim about
adversarial-Neff survival in either direction. See `../SPEC.md` for the decisive
test this prepares for.

Data: `CIRISAI/reasoning-traces`, `data_scrubbed_v1/`, HuggingFace, anonymous,
downloaded once into the HF cache and worked locally. `trace_context.jsonl`
(6,465 per-trace rows) is the primary; `accord_traces.jsonl` (223 MB, full
per-thought payloads) is used only for the Scout autopsy.

## D0. Ordering surrogate (load-bearing)
`timestamp` is SCRUBBED to a placeholder in the public release and cannot order
thoughts. The integer `id` is globally unique, monotonic, and within a task
tracks `thought_depth` (0,1,2,…) — verified. **We order within-task by `id`** as
a creation-order surrogate for wall-clock time. Any true-time-interval analysis
is impossible on this release and is added to the mesh-trace requirements.

## D1. Constraint axes and the 16-dim caveat
The public `trace_context` exposes **8 summary constraint scores**, not the
paper's standardized **16-dim H3ERE feature vector**. So every N_eff here is a
coarse ≤8-axis proxy and is **NOT numerically comparable to the paper's 7.1 / 9.**
The per-thought `accord_traces` payloads carry the same 8 named scores (inside
`conscience_result` / `dma_results`) plus qualitative text — they do **not**
expose the raw 16-dim vector either.

- **CORE4** (primary): `csdma_plausibility_score`, `dsdma_domain_alignment`,
  `idma_k_eff`, `idma_correlation_risk`. ~100 % coverage in every group → the
  covariance is genuine complete-case, no missingness confound.
- **ALL8** (secondary, reported with its n): adds `coherence_score`,
  `entropy_score`, `epistemic_humility_certainty`,
  `optimization_veto_entropy_ratio`. Coverage is 33–78 % and **differs by group**,
  so complete-case n and the missingness pattern are themselves a confound.

## D2. Version confound (kills the naive Scout-vs-Ally k_eff read)
`idma_k_eff` and `idma_correlation_risk` are **version-dependent**:
`idma_correlation_risk` ≈ 0.22 for agent_version 2.0–2.5 but ≈ 0.97 for 2.7.
Scout is **100 % v2.0.2-stable**; the Ally figure the mission flagged (idma_k_eff
1.04) comes from v2.7 qa_eval/unknown. **The flagged "Scout 2.07 vs Ally 1.04
idma_k_eff inversion is a version/config artifact, not an adversarial
signature.** Class-AND-version-aware matched groups collapse most of the gap.
`idma_k_eff` is a single per-trace field (the IDMA's own internal identity
k_eff, bounded [1,3]); it is a distinct object from the cross-axis N_eff Harness A
computes and must not be conflated with it.

## D3. Harness A — N_eff estimator
Per (agent, task_class) group, on the CORE4 (and separately ALL8) complete-case
matrix: Pearson correlation matrix R (zero-variance axes dropped), then
- **N_eff_PR** = (Σλ)²/Σλ² over R's eigenvalues — the robust headline (SPEC's
  Neff_PR), well-defined for any R.
- **k_eff_equicorr** = k/(1+ρ̄(k−1)), ρ̄ = mean off-diagonal correlation — the
  program's equicorrelation identity. Reported WITH ρ̄ and a validity flag
  (valid only for ρ̄>0, denom>0); with mixed-sign correlations it is out of its
  domain and is not read alone.
Error bars: nonparametric **bootstrap over traces** within the group (B=2000),
median + 68 %/95 % percentile intervals. Headline comparison: **Scout
real_user_web (n=36) vs Ally real_user_web (n=310)** — the only clean
matched-class pair.

## D4. Harness B — detailed-balance / rent estimator
The validated maintenance-axis estimator (`keff_saturation/
entropy_production.py`) needs LONG trajectories (T ≫ n_states; brains T~1e3–1e4).
Our within-task thought sequences are SHORT (2–11, max 11), so the per-sequence
winding estimator is **inapplicable**. Honest adaptation: **pool one-step
within-task transitions across many tasks onto a shared coarse-grained
score-state space** (standardize CORE4 → PCA to 2 dims → 2–3 quantile bins/axis,
bins chosen so n_states ≤ N_trans/10) and compute the transition-EP
`Σ P_ij·log(P_ij/P_ji)` with the **symmetrized-count Markov surrogate floor**
(detailed balance by construction), exactly the `entropy_production.py` form.
**Minimum requirement is on pooled transitions: N_trans ≫ n_states²** (not on
single-sequence length). Conditions: Ally benign real_user_web / unknown /
qa_eval, Ally overridden set, Scout-all, Scout-anomalies. This validates that the
pipeline yields **stable, finite numbers on benign data** — it is not a deception
result.

## D5. Discipline
No synthetic data. Incremental flush (each harness writes its own results JSON).
CPU only. Small-n groups reported by their CI, never their point estimate.

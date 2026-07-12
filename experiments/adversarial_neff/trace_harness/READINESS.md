# Mesh-trace readiness: what the weekend's PQ adversarial traces must contain

Derived from the harness validation on the public traces (`DECISIONS.md`,
`results.json`). This is the checklist to run against the mesh telemetry on
arrival, before the decisive adversarial-Neff run. Requirements are ordered by
how badly their absence blocks the decisive test.

## R1 (BLOCKING) — the full constraint feature vector, not the 8 summary scores
The public `trace_context` exposes 8 summary scores. On a **4-axis** clean
subset, the N_eff_PR bootstrap SE floors at **~0.22–0.29 and does NOT shrink with
n** (measured, `power_probe.py`): with only 4 eigenvalues the participation ratio
has an irreducible variance floor, so **the smallest N_eff difference resolvable
at 3σ is ~1.0 regardless of sample size.** The decisive collapse (benign ≈9 →
adversarial <5 on the paper's 16-dim scale) can be subtle in its early regime.
**The mesh traces must expose the paper's standardized 16-dim H3ERE constraint
feature vector per trace** (and, per R2, the CEG substrate features separately).
More axes — not more traces — is what buys N_eff resolution. Without this the run
is a coarse proxy, exactly as this harness is.

## R2 (BLOCKING) — cross-modal separation: H3ERE vs CEG substrate features
SPEC measurement 2 needs N_eff of (a) semantic/H3ERE features only, (b)
CEG/substrate features only, (c) joint. The **substrate (CEG) N_eff should be
attack-invariant** — the strongest defensible claim. The mesh telemetry must
**tag each feature by modality (semantic vs substrate)** so the harness can
compute the three N_eff separately and measure the substrate floor under attack.

## R3 (BLOCKING) — adversarial labeling + per-trace deception outcome
The public release has **no adversarial-labeled data and no adversarial inputs**
(the "possibly-adversarial" Scout set is, on autopsy, two benign guardrail
firings — see `scout_autopsy.md`). Each mesh trace needs:
- `condition ∈ {benign, high_friction, adversarial}` and, for adversarial, the
  attack type (jailbreak suite id / adaptive-white-box generation index);
- a **per-trace deception outcome**: did a false-but-coherent response pass the
  pipeline? (boolean + ground-truth basis). This is required to fit
  deception-rate-vs-N_eff (SPEC measurement 3) and is absent here entirely.

## R4 (BLOCKING) — real timestamps for the maintenance / DB axis
`timestamp` is scrubbed in the public release; we order within-task by `id` (a
creation-order surrogate). The DB estimator ran on `id`-ordering, but a true
maintenance-rate / Hatano–Sasa housekeeping read (SPEC measurement 4) needs
**monotonic per-thought timestamps (or a reliable sequence index) preserved** in
the mesh traces.

## R5 — sample size per condition (power)
Given R1 (adequate dimensionality):
- **N_eff comparison:** at n≈50 per condition the CORE-axis PR SE≈0.22 (resolves
  Δ≈1 at 3σ). Target **≥ 150–200 traces per condition** to (a) tighten to finer
  Δ once the full vector lowers per-sample variance and (b) span a range of
  per-trace N_eff for the curve fit. Minimum floor: **≥ 50 per condition.**
- **Detailed-balance / rent:** the estimator needs **N_trans ≫ n_states²**
  pooled. A stable EP z wanted ≥ ~500 pooled within-task transitions per
  condition (benign qa_eval at 2208 was tight-floored; real_user_web at 167 was
  marginal, floor SD ~0.5). With mean sequence length L, that is ≥ ~500/(L−1)
  multi-thought tasks — for L≈4, **≥ ~170 adversarial multi-thought tasks**, or
  fewer if sequences are longer.

## R6 — sequence length for the maintenance axis
Public sequences are short (2–11 thoughts; the per-sequence winding estimator is
inapplicable, so we pool). For a **per-sequence** DB read on the adversarial set
(stronger than pooled), sequences of **≥ ~30 thoughts** would be needed. If the
mesh adversarial protocol produces long single-conversation chains, capture them
at full length and record it; otherwise the pooled-ensemble estimator here is the
honest fallback.

## R7 — version / config metadata
`idma_k_eff` and `idma_correlation_risk` are **version-dependent** (v2.0–2.5 vs
v2.7 differ ~0.2 vs ~0.97 on correlation_risk). The mesh traces must record
`agent_version` / template / config so benign and adversarial conditions can be
**version-matched** — otherwise a config difference masquerades as an attack
signature (exactly the artifact that inflated the flagged Scout-vs-Ally k_eff
inversion). Ideally run benign and adversarial through the **same agent_version**.

## Arrival checklist (one line each)
- [ ] 16-dim H3ERE feature vector per trace (R1)
- [ ] features tagged semantic (H3ERE) vs substrate (CEG) (R2)
- [ ] condition label + attack type + per-trace deception outcome (R3)
- [ ] monotonic per-thought timestamp / sequence index (R4)
- [ ] ≥150–200 traces per condition (≥50 floor); ≥~170 multi-thought adversarial tasks (R5)
- [ ] long chains captured at full length where available (R6)
- [ ] agent_version/config recorded; benign & adversarial version-matched (R7)

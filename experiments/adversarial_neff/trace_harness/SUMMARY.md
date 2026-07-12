# Trace harness — built and validated on the public traces; the decisive test genuinely waits for the mesh

**Date 2026-07-11.** Harness-validation + discovery on `CIRISAI/reasoning-traces`
(data_scrubbed_v1, n=6,465). NOT the decisive adversarial-Neff test — every number here is a
pipeline-stability read on benign data with confounds documented. Code: `harness_neff.py`,
`harness_db.py`, `loader.py`, `power_probe.py`; data: `results*.json`; autopsy:
`scout_autopsy.md`; the deliverable that matters: `READINESS.md`. (Summary by the
orchestrator from the agent's executed output.)

## 1. The Scout autopsy: the public set contains NO adversarial content

All 7 flagged Scout traces are **mundane guardrail firings on benign traffic**: one
max-thought-depth deferral (depth 7, all axes passing) and six epistemic-humility ponders on
a degenerate one-character input ("g"). No adversarial input, no agent misbehavior anywhere
in the release. The decisive test cannot be run early — it genuinely requires the
post-quantum mesh adversarial traces.

## 2. The harness is validated

- **N_eff (Harness A):** PR and equicorrelation forms run stably per agent per task_class;
  matched-class preliminary (coarse 4-axis proxy, NOT comparable to the paper's 7.1/9 scale):
  Scout/real_user N_eff_PR = 2.81, ρ̄ = 0.17 (n=36, wide bootstrap CI — read the CI).
- **Detailed-balance (Harness B):** the pooled transition-EP estimator (the program's
  validated form) runs stably on within-task score trajectories at these sequence lengths
  (2–11 thoughts; per-sequence winding inapplicable — pooled-ensemble is the honest mode;
  ordering by id since public timestamps are scrubbed).

## 3. The two discoveries that will save the weekend

1. **Resolution is bought by AXES, not traces.** Measured (power_probe): on few-axis
   summaries the N_eff bootstrap SE floors at ~0.22–0.29 and does not shrink with n — the
   smallest 3σ-resolvable ΔN_eff is ~1.0 at any sample size. The mesh must expose the
   **16-dim H3ERE feature vector** and **CEG substrate features tagged by modality** (the
   three-way N_eff — semantic / substrate / joint — is the attack-invariance measurement).
2. **The version confound is real and already bit once.** idma_k_eff / idma_correlation_risk
   differ ~5× across agent versions (v2.0–2.5 vs v2.7); the striking Scout-vs-Ally k_eff
   inversion (2.07 vs 1.04) is (likely) a CONFIG artifact, not an adversarial signature.
   **Benign and adversarial conditions must be version-matched** or the decisive test is
   confounded at birth.

## 4. Arrival checklist for the mesh traces (full detail in READINESS.md)

16-dim H3ERE vector per trace (R1) · features tagged semantic-vs-substrate (R2) · condition
label + attack type + per-trace deception outcome (R3) · monotonic per-thought timestamps
(R4) · ≥150–200 traces per condition, ≥50 floor; ≥~170 multi-thought adversarial tasks (R5)
· long chains at full length where available (R6) · agent_version recorded, conditions
version-matched (R7).

**Bottom line:** the pipeline is warm, the power requirements are measured rather than
guessed, the two silent confounds are named before they could poison the decisive run, and
the checklist is ready to grade the mesh telemetry on arrival. When the weekend traces land,
the decisive adversarial-Neff run is same-day work.

# Cross-rung series — protocol for the six-pair g/J test

**Claim under test:** `StructuralClaims.lean` Claim 6 — the cross-rung dominance
gate. At every coordinated rung pair that jointly satisfies the multi-rung
corridor (both within-rung corridors AND the cross-rung τ corridor), the
cross-rung coupling dominates the within-rung scale.

**Status going in — read this first.** `crossrung_tower_scan.py` found, on an
abstract 6-rung tower, that joint multi-rung corridor satisfaction needs
g/J ≳ 3 — but that "3" came out against a **nominal, uncalibrated τ band**
(0.15, 0.85) chosen by hand. The gate value is **not pinned**. Claim 6 asserts
the *existence* of a dominance gate; this series both **calibrates** the gate
and **tests** it. g/J ≳ 3 is the hypothesis under test, not a number carried in.

## Ordering — non-negotiable

1. **τ-calibration first (Path 1).** Compute the cross-rung τ from real paired
   data at the data-accessible pairs. Three calibrations across different rung
   pairs constrain the τ band. If the band is consistent across pairs the
   calibration is structural; if it varies, it is rung-specific and the
   framework owes an explanation. The gate value follows from the calibrated
   τ band — it is not assumed.
2. **g/J measurement (Paths 2 & 3).** Only after the τ band is calibrated:
   measure coupling g and within-rung scale J at each of the six pairs, compute
   g/J, and test whether each pair that satisfies the multi-rung corridor
   clears the gate.

A "pair clears the gate" claim is meaningful **only** after step 1. Reversing
the order — assuming g/J ≳ 3 and checking pairs against it — is the curve-fit
the session's discipline rules out.

## Method (per rung pair)

- **τ** — cross-rung correlation: the normalised mutual information between the
  within-rung ρ of rung n and of rung n+1 at sustained equilibrium
  (Piece 6: τ = I(R_n;R_{n+1}) / min(H_n,H_{n+1})).
- **g** — cross-rung coupling strength: how strongly rung-n dynamics propagate
  to rung n+1 (causal-mediation estimate from paired data, or the literature
  coupling constant).
- **J** — within-rung scale: the rung's intrinsic dynamical rate in isolation
  (equilibration / relaxation timescale⁻¹).
- Report **g/J** with its uncertainty, against the calibrated gate.

## The six rung pairs

| # | pair | substrate | data source | status |
|---|------|-----------|-------------|--------|
| 1 | A0–A1 | cellular → tissue | TCGA paired cellular-pathway + tissue-architecture | data-runnable (`data-tcga` agent computing the cellular side) |
| 2 | A3int–A3ext | LLM internal → output | CIRISAI/reasoning-traces (HuggingFace) | data-runnable |
| 3 | A3–A4 | individual → community | public org-psych dataset (within-individual + group dynamics) | data-dependent — needs a specific open dataset sourced |
| 4 | Ph0–Ph1 | gauge → atomic | atomic-physics literature (QED–atomic coupling constants, timescales) | literature collation |
| 5 | Ph1–Ph2 | molecular → supramolecular | computational-chemistry literature (H-bond/vdW couplings) | literature collation |
| 6 | Ph2–A0 | biochemistry → cellular | systems-biology literature (metabolic flux, regulatory feedback) | literature collation; least characterised |

τ-calibration (step 1) draws on pairs 1–3 (the data-accessible ones). The gate
follows; pairs 1–6 g/J are then tested against it.

## Pre-registration discipline

Each pair's test commits a `PREREGISTRATION.md` (from `PREREG_TEMPLATE.md`)
**before** results: the τ / g / J constructions, the corridor/gate criterion,
the confound controls, the falsifier. Pre-registration commit precedes the
results commit — git history is the proof.

## What the series settles

Six g/J measurements across substantively different rung pairs. If all six
clear the (calibrated) gate: Claim 6's dominance structure is empirically
anchored across radically different rung types — Piece 6 moves from
abstract-tower-demonstrated to physically grounded. If any pair has the
multi-rung corridor satisfied but g/J below the gate: `Falsifier6` witnessed,
Claim 6 retracts (via `claim6_iff`).

## Honest scope

The within-rung corridor band is session-calibrated (A3+ recalibration,
ρ ≈ 0.17–0.35). The cross-rung τ band is what Path 1 calibrates — until then it
is open. Pairs 4–6 are literature collation, not new experiment; pair 3 needs
an open dataset sourced. None of this is the channel from a cosmological P_ω to
particle observables — Claim 6 is about the abstract cross-rung structure made
physical, not about the universal-scale post-selection tier.

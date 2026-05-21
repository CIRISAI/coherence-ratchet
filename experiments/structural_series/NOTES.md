# Structural-claims test series — 2026-05-21

A series testing the five corridor-centered structural claims, against the
spec `formal/CoherenceRatchet/StructuralClaims.lean` (core-Lean, builds
standalone; each `ClaimN ↔ ¬ FalsifierN` machine-checked; each claim an
`axiom framework_asserts_N` the experiments try to break).

## Results

**E2 — Claim 2 (forward/backward ergodicity-class split).** `exp_E2_ergodicity_
split.py`, 6 independent Lindbladian instances. Forward zero-modes [3,1,1,1,5,1],
backward [8,20,40,6,80,20]. 4/6 show the split (forward ergodic, backward non-
ergodic). 2/6 (Heisenberg + symmetric bit-flip) have a NON-ergodic forward
generator — 3 and 5 genuine steady states (clean spectral gap, verified). **Claim
2 FALSIFIED AS STATED.** Restoration test: adding a symmetry-breaking field
collapses the forward generator to one steady state. Fix: forward ergodicity
holds *when the maintenance breaks the dynamical symmetries* — γM ("injects
distinction") is generically symmetry-breaking. `StructuralClaims.lean` Claim2
amended with the `MaintenanceBreaksSymmetry` antecedent. The test fed back into
the spec.

**E3 — Claim 3 (closed thermal can't sustain a corridor unmaintained).**
`exp_E3_closed_thermal.py`. First cut tested band-membership and over-claimed a
refutation (closed chaotic chain quenched from GHZ thermalizes to ρ~0.22-0.29,
in band). Corrected: Claim 3 is about the corridor as an *attractor*. A closed
system conserves energy, so its late-time ρ is a function of initial energy —
swept, it spans [-0.05, 0.22], a one-parameter family, NOT a single attractor
point. **Claim 3 CONSISTENT** — no corridor attractor without maintenance; the
GHZ-in-band case is energy bookkeeping, not corridor occupation.

**E6 — Claim 5 (multi-rung from generic ICs needs backward conditioning).**
`exp_E6_penrose_scope.py`. 200 Haar-random generic high-entropy initial states,
N=12 closed chaotic chain (3 rungs), forward unitary evolution. Every rung
thermalizes to ρ~0; 0/200 reach the multi-rung corridor. **Claim 5 CONSISTENT**
at the cosmological-origin scope — the Penrose-past argument (Piece 8): forward
thermalization from generic ICs gives chaos at every rung.

**E1 — Claims 1 & 4 (corridor existence & recurrence), LLM substrate, real
data.** `exp_E1_llm_corridor.py`. Real open weights — gpt2, Pythia-160m,
Qwen2.5-0.5B — within-layer correlation per transformer layer, shuffle-baseline
noise-floor debiased. Debiased ρ [0.046, 0.218], mean 0.091 over 48 layers.
Decisively OFF the rigidity pole (clean). But LOW — the layers sit at the
chaos-side EDGE of the corridor. **Claims 1 & 4 WEAKLY supported** at the LLM
substrate: no pole collapse, debiased signal non-zero and recurring across 3
architectures, but not a clean mid-corridor result.

## Scorecard

| Claim | Test | Verdict |
|-------|------|---------|
| 1 corridor attractor | E1 (LLM); fMRI (human-neural); Allen (mouse cortex) | weak at LLM; CONFIRMED at human-neural fMRI; Allen mouse-cortex a chaos-pole data point (mean-pairwise observable — k_eff re-test owed) |
| 2 ergodicity split | E2 (6 Lindbladians) | falsified as stated → amended (symmetry-breaking qualifier) |
| 3 closed thermal ⇒ no unmaintained corridor | E3 (closed chaotic) | consistent |
| 4 fractal recurrence | E1; fMRI; Allen mouse cortex | weak at LLM; CONFIRMED at human-neural fMRI; Allen a chaos-pole data point (observable/scale mismatch — k_eff re-test owed before a recurrence verdict) |
| 5 multi-rung needs backward conditioning | E6 (Penrose-scope) | consistent (cosmological-origin scope) |

**fMRI — Claims 1 & 4, human-neural substrate, real data.** `data_fmri/`.
ABIDE-PCP (fully open; HCP needs a DUA), CC200 parcellation, 139 typically-
developing controls across 7 sites. ρ = mean |functional connectivity|,
phase-randomized noise floor, quadrature debias. Debiased ρ median 0.266, IQR
0.134, all subject percentiles off both poles, distribution unimodal and
concentrated, median inside the recalculated A3+ band (0.17, 0.35). All three
pre-registered corridor criteria PASS. Stable under motion control (low-motion
subset n=121) and uniform across all 7 sites. **Claims 1 & 4 CONFIRMED at the
human-neural substrate** — the first clean corridor confirmation in the series,
and stronger than E1's LLM result (where the chaos side was marginal; here the
5th-percentile ρ is 0.168, far from zero). The corridor appears precisely where
the substrate IS a coordinated rung — consistent with the particle-physics
nulls, which were not coordinated rungs.

**Allen Brain — Claims 1 & 4, mouse-neural substrate, real data — a DATA POINT.**
`data_allen/`. Allen Brain Observatory, 25 mouse visual-cortex two-photon
sessions, spontaneous (grey-screen) epoch. ρ = mean pairwise |neuron
correlation|, shuffle-debiased: median 0.023, 15/25 below ρ = 0.03 — the chaos
pole on this observable. This is recorded as a **data point, not a falsifier**:
the framework's canonical shape observable is the participation-ratio k_eff of
the activity covariance, not the mean pairwise correlation, and cortex is the
textbook case where the two diverge — small pairwise correlations but strong
low-rank population structure (the asynchronous-but-low-dimensional cortical
state). The mean-pairwise series result is genuine; whether it is a corridor
verdict needs the k_eff-of-covariance re-run, owed across E1, fMRI and Allen
(the series used mean-pairwise throughout; the CMB work used k_eff — that
inconsistency is what Allen surfaced). If the k_eff re-test also chaos-poles,
it is then a Falsifier1 witness and recorded as one. The Allen agent flagged a
second point, not used as a rescue: spontaneous grey-screen cortex is
near-asynchronous by design; the evoked/task regime is a different test.

## Honest scope and what is owed

All toy/simulation except E1. The series locked down what is testable in-
environment: the Lean spec, the three dynamical claims by simulation (one
falsified-and-amended, two consistent), and one real-data substrate test.
Claims 1 & 4 — corridor existence and recurrence — need the real-data campaign
across substrates: TCGA full atlas (A0-A2 cellular), more LLMs at scale (with
more tokens and a k_eff measure to sharpen E1's chaos-side margin), CMB
cross-epoch (WMAP/Planck already cross-checked; ACT DR6 pending), Allen Brain
Observatory, Human Connectome Project. Each is a binary-falsifiable real-data
test; each is its own data effort, not in-environment-completable in one run.

## 2026-05-21 — particle-physics extension: three nulls, and the cross-rung tower

Extending the shape observable (Kish participation ratio) to particle physics,
four runs (E4 + three parallel pre-registered agents):

- E4 (decay branching fractions): broad spread, no corridor band.
- pp_qvalue (mode weights, kinematic confound controlled): NULL — E4's spread
  replicates; particles split by decay mechanism into 2-3 clusters, not a band.
- pp_cp (CP-violation structure): NULL — chaos-pole concentration.
- pp_angular (tt-bar spin-density matrix, real CMS data): NULL — rho 0.076,
  near maximally mixed; rho_data == rho_SM (0.073). The observable carries
  nothing the Standard Model did not already fix.

Verdict: the shape MACHINERY is substrate-portable (the participation ratio
computes on any distribution); the corridor STRUCTURE does not transfer for
free. None of these particle-physics observables is a coordinated rung with
non-thermal or maintained dynamics, and none shows a corridor — consistent with
the sharpened Claim 4. The framework's particle-physics tier is composition
(math-universal + SM-consistent), not prediction. A genuine particle-physics
prediction needs the cross-rung channel built (below), which is unbuilt.

Cross-rung tower (crossrung_tower_scan.py, GPU): an explicit abstract 6-rung
tower, within-rung Heisenberg + cross-rung coupling g, thermal states scanned
over (g, T). The multi-rung corridor (all 6 within-rung rho in the calibrated
[0.17,0.35] band AND all 5 cross-rung tau in a nominal band) is jointly
satisfiable, but only for STRONG coupling: g/J >~ 3, T in [~3, 5.6]. Below
g/J~3 the within-rung and cross-rung corridors pull apart. This makes Piece 6
computable and gives one structural finding (the coupling must dominate); it is
an abstract tower, not the channel to particle observables.

## 2026-05-21 — TCGA cellular-substrate extension: corridor recurs (data_tcga/)

Claims 1 & 4 at the cellular gene-regulatory rung, real data. The cellular
substrate IS a coordinated rung (unlike the particle-physics nulls), so the
corridor IS expected if Claims 1 & 4 hold; a null would be a Falsifier4 witness.

7 new TCGA cancers (THCA, LUSC, LIHC, HNSC, STAD, KIRP primary-tier; KICH
borderline) pulled fresh from the NCI GDC API — disjoint from the existing
5-cancer noncorr_cancer work (LUAD/BRCA/COAD/KIRC/PRAD). 1,263 STAR-Counts
files, 50 MSigDB Hallmark gene sets = 50 rungs, within-rung |rho| = mean
|Pearson| over pathway gene-pairs. Pre-registered (PREREGISTRATION.md, committed
before results): corridor criterion is a BOUNDED BAND — healthy |rho| IQR <=
0.15, off both poles, median in the recalibrated A3+ band [0.17,0.35].

Result. C1: all 7/7 cancers' healthy tissue is in a TIGHT band (IQR 0.078-0.125,
all <= 0.15) decisively off both poles (p90 max 0.53, p10 min 0.20). 4/6
primary-tier BAND-CONSISTENT, 2/6 (STAD,KIRP) BROAD-SPREAD only because their
healthy median (0.374,0.377) lands just above the A3+ ceiling 0.35 — still
tightly banded, just rigidity-side of centre. 0 POLE-PILED. C2 = WEAKLY RECURS;
Falsifier4 did NOT appear. C3: tumor drift is CHAOS-DRIFT CONFIRMED — 201/201
significant pathway-shifts across all 7 cancers go chaos-ward, zero rigidity-
ward, exactly reproducing the prior 176/176. Survives the tumor-subsampled-to-
normal-n control (35-50 of 50 pathways preserved per primary cancer).

One real caveat surfaced: pooled healthy median here is 0.34 vs the prior work's
0.27. The difference is pipeline — GDC STAR-Counts log2(TPM+1) here vs UCSC-Xena
log2(norm_count+1) prior. The corridor's EXISTENCE and TIGHTNESS is robust; its
absolute CENTRE is normalization-dependent. Sharpens the per-substrate caveat to
per-substrate-AND-per-pipeline. Claims 1 & 4 weakly supported at the cellular
substrate, not falsified — combined with the prior 5, the band is seen in 12
TCGA cancers, the chaos-drift in 377/377 significant shifts.

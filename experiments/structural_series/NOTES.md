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
| 1 corridor attractor | E1 (LLM, real); fMRI (human-neural, real) | weakly supported at LLM (chaos-side edge); CONFIRMED at human-neural |
| 2 ergodicity split | E2 (6 Lindbladians) | falsified as stated → amended (symmetry-breaking qualifier) |
| 3 closed thermal ⇒ no unmaintained corridor | E3 (closed chaotic) | consistent |
| 4 fractal recurrence | E1 (3 architectures); fMRI (139 subjects, 7 sites) | weakly supported at LLM; CONFIRMED at human-neural |
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

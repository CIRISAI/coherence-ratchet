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
| 1 corridor attractor | E1 (LLM, real) | weakly supported (off rigidity; chaos-side edge) |
| 2 ergodicity split | E2 (6 Lindbladians) | falsified as stated → amended (symmetry-breaking qualifier) |
| 3 closed thermal ⇒ no unmaintained corridor | E3 (closed chaotic) | consistent |
| 4 fractal recurrence | E1 (3 architectures) | weakly supported |
| 5 multi-rung needs backward conditioning | E6 (Penrose-scope) | consistent (cosmological-origin scope) |

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

# RESULT — Wave 1 RG: the cross-rung OOM band does NOT constrain the dead-zone R*

Post-measurement. Pre-registered design in `PREREGISTRATION.md`, committed in a
PRECEDING commit (git history is the proof). 2026-05-21.

## The question

Two pieces of this session's work:

1. The dead-zone RG tower (`experiments/open_system_pomega/deadzone_rung_scaling.py`,
   `deadzone_rg_calibration.py`) found a **rung budget R\* ≈ 25–56** — how many
   rungs the backward-soft P_ω survives before the corridor penalty `h_min`
   exponentially suppresses it. The calibration places the framework's genuine
   RG-nested rungs at a non-commutativity knob value **ε ≈ 0.20**.

2. The cross-rung coupling corridor (`crossrung_series/path1_tau/`, Claim 6) is
   the OOM band **g/J ∈ (0.3, 3)** — one order of magnitude around parity.

ε ≈ 0.20 sits just below the band's lower edge 0.3. The task: is that a
meaningful constraint, or a coincidence of magnitude? The crux is whether ε and
g/J are the **same kind of quantity**.

## What ε and g/J actually are (verified by `assess_eps_vs_gj.py`, real GPU run)

**ε — the dead-zone non-commutativity knob.** In the dead-zone model
(`deadzone_rung_scaling.py`) each rung is an abstract correlation operator
`ρ_n = U_n Λ U_n†` with `U_n = exp(i·ε·A_n)`, `A_n` a random Hermitian operator
*internal to rung n*, `Λ` a fixed spectrum shared by all rungs. ε is the
amplitude of a per-rung unitary rotation: it tunes how far each rung's operator
is rotated away from the common `Λ`, i.e. how much adjacent rung *operators*
fail to commute. CHECK 1 confirms this directly:

| ε | ‖[ρ_n,ρ_{n+1}]‖ | h_min(R=13) | h_min slope /rung |
|------|----------------|-------------|-------------------|
| 0.00 | 2.7e-07 | 0.00000 | 0.000000 |
| 0.05 | 2.2e-03 | 0.00061 | 0.000047 |
| 0.15 | 6.5e-03 | 0.00523 | 0.000402 |
| 0.20 | 8.5e-03 | 0.00912 | 0.000701 |
| 0.40 | 1.6e-02 | 0.03411 | 0.002624 |
| 1.00 | 2.7e-02 | 0.17384 | 0.013372 |

At ε = 0 every rung is the *same* operator `Λ` — commutator zero, h_min zero.
ε is purely an operator-misalignment amplitude. (The ε = 0.20 row reproduces the
calibration: h_min slope 0.0007/rung, the value `deadzone_rg_calibration.py`
matched to the genuine RG-nested rungs' directly-measured 0.00081/rung.) **There
is no within-rung energy scale `J` anywhere in this model — the rungs are
abstract operators on a fixed shared Hilbert space. There is nothing for ε to be
a ratio of.**

**g/J — the cross-rung Hamiltonian energy-scale ratio.** In the cross-rung tower
(`crossrung_tower_scan.py`) the Hamiltonian is `H = J·H_rung + g·H_couple`:
`J·H_rung` is the within-rung Heisenberg term binding each rung's two
constituents; `g·H_couple` is the cross-rung `Σ Z Z` term linking adjacent
rungs. g/J is the *ratio of these two Hamiltonian energy scales*. CHECK 2
confirms its job — it drives within-rung ρ_n and cross-rung τ:

| g/J | within-ρ range | cross-rung τ range |
|------|---------------|--------------------|
| 0.0 | [0.285,0.285] | [0.000,0.000] |
| 0.3 | [0.285,0.285] | [0.002,0.002] |
| 0.6 | [0.284,0.284] | [0.007,0.007] |
| 1.0 | [0.283,0.284] | [0.020,0.020] |
| 2.0 | [0.279,0.282] | [0.072,0.073] |
| 3.0 | [0.273,0.278] | [0.143,0.145] |

g/J monotonically raises the cross-rung mutual information τ — its actual role.

## The C1–C3 gate (pre-registered)

**C1 — same role in the model? FAILS.** ε acts *within* each rung's operator
definition (the amplitude of an internal unitary rotation). g/J acts *between*
rungs in the Hamiltonian (the relative weight of the inter-rung coupling term).
Different roles, different layers of the construction.

**C2 — dimensional / structural commensurability? FAILS.** g/J is a ratio of two
scales of the *same kind* (Hamiltonian energy couplings). ε is *not a ratio at
all* — the dead-zone model has no within-rung scale to divide by; ε is a bare
operator-rotation angle. No monotone, model-independent map ε ↔ g/J exists.

**C3 — shared mechanism? FAILS.** ε drives the rung-operator non-commutativity
(CHECK 1: ‖[ρ_n,ρ_{n+1}]‖ goes from 0 at ε=0 to 2.7e-2 at ε=1) which in turn
sets the `h_min` corridor penalty and hence R\*. g/J does not touch rung-operator
non-commutativity: the cross-rung tower's within-rung correlation operators
`O_n = Z_{2n}Z_{2n+1}` act on disjoint spin pairs and commute exactly *for every
value of g/J* (commutator column identically 0). g/J instead sets the
Hamiltonian energy ratio that controls cross-rung τ. The two mechanisms are
disjoint: ε → operator misalignment → h_min → R\*; g/J → energy ratio → τ.

## Verdict — honest negative

**All three gates fail. ε is NOT the cross-rung coupling g/J.** ε is a
rung-operator non-commutativity / misalignment amplitude; g/J is a
cross-rung-vs-within-rung Hamiltonian energy-scale ratio. They live in different
models (the dead-zone model has no J; the cross-rung tower has no ε), play
different roles, and drive disjoint mechanisms. The ε ≈ 0.20 vs OOM-band edge
0.3 proximity is a coincidence of magnitude between two dimensionless numbers,
not a shared axis.

**Per the pre-registration, a C-gate failure is an honest negative and the
experiment stops here.** The OOM band (0.3, 3) does NOT constrain ε. The
recomputation step (restrict ε to a band-equivalent range, re-run the scan) is
NOT executed, because there is no band-equivalent range — the band lives on a
different quantity.

**The dead-zone rung budget R\* ≈ 25–56 stands UNCHANGED.** It is set by the
directly-measured `h_min` slope on genuine RG-nested operators, and nothing in
the cross-rung coupling corridor revises that measurement. The cross-rung
coupling corridor (Claim 6) and the dead-zone rung budget are **two independent
constraints** on the framework — one on inter-rung Hamiltonian coupling
strength, one on the depth a soft P_ω survives — not two views of the same
constraint.

## What this does and does not touch

- It does NOT fire F-11 or weaken anything: it is a clean separation-of-concerns
  result. The dead-zone R\* and the OOM band remain exactly as their own work
  established them.
- It DOES close a tempting-but-wrong unification: a future write-up should not
  claim the OOM band tightens the rung budget, nor that ε ≈ 0.20 being "near"
  the band edge is evidence of anything. The two numbers are not on the same
  axis.
- Honest limit: this assessment compares the two *models* as built. A different,
  not-yet-built model in which rungs are both Hamiltonian-coupled (a g/J) AND
  carry operator non-commutativity (an ε) could relate the two — but that model
  does not exist, and inventing it to force a connection would be exactly the
  self-sealing move the discipline forbids. On the machinery that exists, ε and
  g/J are distinct quantities.

# Forced-partition computation — full result-space

**Date:** 2026-07-10. **Mode:** DISCOVERY (no pre-stated prediction; exhaustive
reporting). **Grid:** 2400 cells = 3 alpha-forms x 4 allocation-rules x
4 dimension-vectors x 2 budget-accountings x 25 budget-levels. Every cell is
integrated to steady state (LSODA with terminal pole-events), classified, and
its Jacobian eigenvalues computed numerically. Nothing is winner-picked; the full
grid is in `results.json`. Lake companion:
`formal/CoherenceRatchet/Core/SectorPartition.lean`.

**Seeded, not discovered — stated plainly (the trap from
`papers/notes/entropic_matter_sector.md`).** The block structure
d = (d_1,...,d_n) is an INPUT. Blockwise additivity of S is a theorem about the
seeded structure, not a finding. Only what the *dynamics* does with a seeded
block structure — the steady-state partition and its stability — is reported as a
result below.

Setup per sector k: `drho_k/dt = alpha(rho_k) - gamma*m_k`, `S_k = d_k*s(rho_k)`,
`s(rho) = -ln(1-rho)`, `gamma = 1`, drift strength `a = 1`. Budget level `b` swept
0.02->1.30. Allocation weights w_k normalized to the budget:
A equal `w=1`; B stock `w=d_k s(rho_k)=S_k`;
C rate `w=d_k alpha(rho_k)/(1-rho_k)=|dS_k/dt|_drift`; D need `w=alpha(rho_k)`.

---

## 1. The complete result-space

### 1a. Phase structure across the budget axis (all rules, where an interior state exists)

| budget regime | outcome | pole |
|---|---|---|
| starvation (low b) | maintenance cannot hold any sector; every rho_k -> 1 | **runaway_rigidity** |
| interior band (mid b) | rule-specific fixed point (see 1b) | — |
| over-maintenance (high b) | maintenance overwhelms drift; rho_k -> 0 | **collapse_chaos** |

Overall classification counts (all 2400 cells): collapse_chaos 1100,
runaway_rigidity 604, symmetric 460, broken 236.

### 1b. Allocation-rule signatures at the interior fixed point (the core grid)

Interior fixed points (classification in {symmetric, broken}), per-unit accounting;
identical qualitative picture under total accounting (see 1e).

| rule | partition at steady state | dim-proportional? | rho vs d ordering | Jacobian max Re(lambda) |
|---|---|---|---|---|
| **A equal** | symmetric, S_k **exactly prop. to d_k** | 92/92 yes | all rho_k equal | **-1.0** (strongly stable) |
| **D need** | symmetric, S_k prop. to d_k | yes (to numerics) | all rho_k equal | **0.000, 100% of cells** (marginal) |
| **B stock** | **broken**, != d_k | 23/89 (edge only) | **corr(rho_k,d_k) = -0.995** | -1.0 (stable) |
| **C rate** | **broken**, strongly != d_k | 23/80 | **corr(rho_k,d_k) = -1.000** | -1.0 (stable) |

Detail, bianconi d=(1,1,3,3,3), linear alpha, per-unit, across budget:

- **A equal** — every sector at a common rho*; partition-deviation L1 = 0.000 at
  all budgets; rho* ~ 1-b (b=0.29->rho=0.713, 0.55->0.447, 0.82->0.180). Jac = -1.
- **D need** — every sector at a common rho* (spread <= 0.007, numerical);
  partition ~ prop. to d. But Jacobian max real eigenvalue is **exactly 0** for all
  92 interior cells: the symmetric fixed point sits on a **neutral
  (zero-eigenvalue) budget-conserving manifold**, not an attracting point.
- **B stock** — dimension-**ordered** split: d=1 sectors settle at HIGHER rho,
  d=3 sectors at LOWER rho (b=0.55: rho = [0.627,0.627,0.407,0.407,0.407]).
  Deviation from prop-to-d grows with budget (0.067 -> 0.331). Stable (-1).
- **C rate** — same ordering, extreme. b=0.55: rho=[0.790,0.790,0.370,0.370,0.370];
  b=0.82: rho=[0.689,0.689,0.067,0.067,0.067] (large sectors driven to chaos edge).
  Deviation reaches 1.2-1.6. Stable (-1).

### 1c. C-rate condensation (reported at full prominence)

Under rate-proportional allocation the entropic potential **condenses into the
SMALLEST sectors** as budget rises — inverting the dimension ordering. bianconi,
linear alpha, per-unit; partition fraction S_k/S_total vs the dimension fraction:

| b | partition_frac (d=1,1,3,3,3) | dimension_frac |
|---|---|---|
| 0.02 | 0.111, 0.111, 0.259, 0.259, 0.259 | 0.091, 0.091, 0.273, 0.273, 0.273 |
| 0.45 | 0.184, 0.184, 0.211, 0.211, 0.211 | (same) |
| 0.66 | 0.259, 0.259, 0.161, 0.161, 0.161 | (same) |
| 0.87 | **0.488, 0.488**, 0.008, 0.008, 0.008 | 0.091, 0.091, 0.273, 0.273, 0.273 |

At b=0.87 the two d=1 sectors carry **97.6%** of the entropic potential; the three
d=3 sectors (which the dimension partition would assign 82%) carry 2.4%. This
condensed state is a **stable** attractor (Jac -1), not a runaway. The crossover
from near-dimensional (low b) through equipartition (b~0.45) to small-sector
condensation (high b) is monotone in budget.

### 1d. Alpha-form dependence

Interior fixed points exist only for state-dependent drift:

| alpha form | interior fixed points | note |
|---|---|---|
| linear `a(1-rho)` | 580 | richest interior band |
| logistic `a*rho*(1-rho)` | 116 | narrow band; weak near both poles => over-maintenance collapses to chaos readily (342 collapse) |
| **const `a`** | **0** | state-independent drift admits **no interior equilibrium** (knife-edge: needs gamma*m=a exactly); every cell at a pole (304 rigidity, 96 chaos) |

Where logistic has an interior fixed point, the rule signatures are unchanged
(B_stock still dimension-ordered broken, etc.).

### 1e. Budget accounting (per-unit vs total)

Only **14 / 1200** (dim, alpha, rule, budget) cells differ in classification
between the two accountings. The accounting choice is qualitatively immaterial;
for rule A the two are algebraically identical (m_k = b either way).

### 1f. Corridor overlay (factual)

Interior fixed points cross the corridor (0.10, 0.43) only in a narrow budget
window. A_equal, linear alpha, bianconi dims: all sectors lie in the corridor only
for b in [0.61, 0.87] (consistent with rho* ~ 1-b landing in (0.10,0.43)). No
coincidence claimed; the window is reported as observed.

---

## 2. Interpretation (LABELED — read section 1 first)

**A forced equilibrium partition exists, but WHICH partition is set entirely by
the allocation rule, not by the seeded dimensions.**

1. **The dimension-proportional partition (S_k prop. to d_k) is produced by exactly
   one rule — equal per-unit maintenance (A) — and there it is the SEEDED density
   form itself, not a discovery.** Equal per-unit maintenance forces a common rho*,
   and `S_k = d_k*s(rho*)` is then proportional to d_k by the definition of S_k
   (the lake lemma `symmetric_density_partition` realized dynamically). Strongly
   stable (Jac -1), but it recovers only what was put in.

2. **The moment maintenance responds to sector STATE, the dynamics BREAKS the
   dimensional partition** — monotonically and unanimously ordered by dimension
   (corr(rho_k, d_k) <= -0.995: large sectors always held at lower correlation).
   Stock-proportional (B) gives a mild, stable anti-dimensional skew;
   rate-proportional (C) gives an extreme, stable condensation of the entropic
   potential into the FEWEST-dimensional sectors (1c), inverting the ordering.

3. **Need-proportional (D) reproduces the prop-to-d partition but only
   MARGINALLY** — zero Jacobian eigenvalue in 100% of interior cells. It sits on a
   neutral manifold, so it is not an attractor that would "select" the dimensional
   partition against perturbation.

4. **No rule spontaneously selects Bianconi's (1,1,3,3,3) — or any particular —
   weighting as emergent content.** The only rule returning "proportional to the
   dimensions you seeded" is the one that trivially passes the seed through. This
   is the referee kill of `entropic_matter_sector.md` Q3(b) realized numerically:
   *you derive whatever weighting you seeded.* The marriage of the form-sector
   partition to Bianconi's degeneracy z_k remains unpaid — the partition is a
   property of the allocation rule imposed on a hand-chosen block structure, not of
   the entropic action.

**Surprises flagged at full weight:** (i) rate-proportional allocation produces a
genuine stable symmetry-breaking that *inverts* the dimension ordering
(condensation into small sectors); (ii) need-proportional allocation's fixed point
is exactly marginal (zero eigenvalue) while equal/stock/rate rules are strongly
stable (-1); (iii) state-independent drift (const alpha) admits no interior
equilibrium at all. The boring-but-real headline is #1/#4: the dimension-partition
is forced only by the trivial rule, and the dynamics does not, on its own, single
out the seeded weighting.

---

## 3. Sideways reading (orchestrator addendum, same day — labeled interpretation + its first test)

**What the grid actually contains, read against the program's own questions rather than the
matter-sector question it was commissioned for:** the allocation rule maps onto the
criticality-vs-low-rank axis. **Need-proportional allocation sits at exactly marginal
stability** (Jacobian max eigenvalue = 0 in 100% of interior cells) — the self-organized-
criticality signature — while **state-responsive rules (stock, rate) produce stable,
dimension-ordered broken states.** The program owns two independent measurements that this
mapping connects: EXP118 measured the *policy* on hardware (maintenance tracks stock,
partial r = +0.84) and Gate-0 measured the *structure* across substrates (low-rank, not
critical). Under this reading they are two views of one fact: real systems run state-tracking
maintenance, and state-tracking maintenance is the non-critical, stable-order policy.

**The strongest form of that reading — "state-responsive maintenance DERIVES Gate-0's k_eff
saturation" — was tested immediately (`dsweep_keff.py`) and FAILED:** k_eff grows linearly
with D under every rule (D = 7 → 448: k_eff ≈ 0.61·D throughout). The failure is structural,
not numerical: the toy's sectors are mutually independent blocks, k_eff of independent blocks
is extensive, and Gate-0's 1/ρ ceiling lives in global cross-unit correlation that this model
does not contain. **What survives:** the policy ↔ stability-class mapping (need → marginal/
critical; state-responsive → stable broken order), correctly scoped as a within-partition
statement. **The posed follow-up:** a model with cross-sector coupling (global ρ background +
sector structure) is required before the saturation question can even be asked of the
maintenance dynamics.

**One model wrinkle for any reuse of the condensation result (§1c):** the parent grid's d = 1
sectors carry S_k = s(ρ) by the extensive convention, but a 1-dim block has no internal
correlation (exact block log-det = 0) — the 97.6% condensation figure leans on those
degenerate sectors. The anti-dimensional *ordering* survives on d ≥ 2 sectors (asym (2,9) and
the d-sweep show the same ρ ordering); the extreme condensation number should be re-derived
with exact block log-dets before it is quoted anywhere.

## Artifacts

- `results.json` — full 2400-cell grid (incremental-flushed).
- `phase_rho_<rule>_per_unit.png` (x4) — steady-state rho_k vs budget per sector,
  with corridor band and poles; rows = alpha forms, cols = dimension vectors.
- `partition_<rule>_per_unit.png` (x4) — S-partition fraction vs budget with the
  dimension fractions (dotted).
- `forced_partition.py`, `make_figures.py`.
- Lake: `formal/CoherenceRatchet/Core/SectorPartition.lean`.

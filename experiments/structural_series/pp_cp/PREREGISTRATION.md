# Pre-registration — CP-violation structure across decay modes as a corridor candidate

Date: 2026-05-21. Committed BEFORE results. One of three parallel particle-physics
shape-observable investigations. Honest prior: NULL (see E4).

## 0. Is CP-violation structure across modes a coordinated rung?

State it plainly, before any data. **No — not in the framework's sense, and this
test is run anyway as an honest check, not because the framework predicts a hit.**

The framework's corridor claim (CLAUDE.md, Piece 3; StructuralClaims Claim 4)
attaches to *coordinated rungs* — substrates with sustained coordination and
identifiable active maintenance work γ·M(t) (Piece 2). The set of CP asymmetries
A_CP across a parent particle's decay modes is none of these:

- The A_CP values are independent measurements of distinct, unrelated decay
  amplitudes. There is no coordination *among the modes* — one mode's asymmetry
  does not constrain another's except through CKM unitarity (and even that is
  weak and indirect at the level of individual exclusive modes).
- There is no maintenance dynamics γ·M(t). CP violation is a fixed property of
  the Standard Model Lagrangian (the CKM phase), not an actively-maintained
  attractor state. There is no dρ/dt to be in equilibrium with.
- A_CP is not a distribution over constituents that share a budget. Branching
  fractions at least sum to 1 (a genuine simplex; that is what made E4 a
  *defensible* if null construction). A_CP values do not sum to anything; they
  are not parts of a whole.

So the honest framework-internal expectation is that the shape observable does
not apply, OR applies only as a descriptive statistic with no corridor meaning.
This pre-registration nonetheless fixes a defensible construction so the check
is falsifiable rather than hand-waved.

## 1. The construction problem

A_CP can be negative and the values are not a probability distribution, so
k_eff = 1/Σpᵢ² cannot be applied to A_CP directly. The defensible repair:

The shape observable measures *concentration vs spread*. The physically
meaningful magnitude here is the *size* of CP violation per mode, |A_CP|. CP
violation can be concentrated in a few modes (a few large |A_CP|) or spread
across many modes (many comparable |A_CP|). That concentration question is
exactly what the participation ratio answers.

### Pre-registered construction (PRIMARY)

For each parent particle P with measured A_CP values {A_CP,1, ..., A_CP,N}:

1. Take magnitudes: aᵢ = |A_CP,i|.
2. Form weights wᵢ = aᵢ² (the CP-violation "power" of mode i — squaring is the
   same power convention used for CMB mode amplitudes in CMBOrthogonality.lean
   and for branching fractions in E4).
3. Normalise: pᵢ = wᵢ / Σwⱼ. This IS a probability distribution on the simplex.
4. k_eff = 1/Σpᵢ², ρ = (N/k_eff − 1)/(N − 1) ∈ [0,1].

Interpretation: ρ→1 = CP violation concentrated in one mode (rigidity); ρ→0 =
CP violation spread evenly across modes (chaos); a corridor = a bounded interior
band recurring across parent particles.

### Confound control (inherited from E4, mandatory)

E4 caught a decay-table-completeness confound: raw N varies wildly across
particles and k_eff inflates with N, so raw ρ measures measurement completeness,
not physics. SAME control here: A_CP measurement counts are heterogeneous
(B+ ~166, B0 ~64, D0 ~103, D+ ~31). Therefore the PRIMARY analysis computes ρ on
a FIXED number N_FIX of the largest-|A_CP| modes per particle, so every
particle's ρ is a completeness-independent concentration measure.

N_FIX = 12 (pre-registered; chosen so all four parents qualify with margin and
N_FIX > corridor-band resolution). A secondary all-modes ρ is reported for
transparency but is NOT the corridor test.

### Secondary descriptive statistic (reported, not the test)

Also report, per parent, the fraction of total Σ|A_CP|² carried by the single
largest-|A_CP| mode (top-power fraction). This is the rawest concentration
number and is robust to the k_eff/N issue.

## 2. What counts as a corridor — the pre-registered bar

A corridor claim is NOT "ρ landed somewhere in (0,1)". It must clear a TIGHT band:

- **CORRIDOR (framework hit):** the per-parent ρ values (PRIMARY, fixed-N_FIX)
  cluster in a tight band of width ≤ 0.18, AND that band lies inside the A3+
  reference corridor ρ ∈ [0.17, 0.35], AND ≥ 75% (here: ≥ 3 of 4 parents) fall
  in that band. All three required.
- **NULL — broad spread:** ρ values span a range wider than 0.18, or do not
  cluster. The shape observable produces a number but no attractor band.
- **NULL — pole pile-up:** ρ values pile at a pole (≥ 3 of 4 with ρ > 0.55, or
  ≥ 3 of 4 with ρ < 0.12).
- **CONSTRUCTION FAILURE:** if the construction is degenerate (e.g. one mode's
  |A_CP| dominates Σ purely because of a measurement artefact, or values are too
  few/noisy), report that and stop — do not force a verdict.

A wide window is explicitly NOT a corridor. The bar is the tight band above.

## 3. Data

PDG 2025 via the `pdg` package (v0.2.2, installed). Parent particles with
accessible A_CP data: B+, B0, D0, D+. (B_s0, Lambda_b0, Lambda_c+, D_s+ are not
name-resolvable in this PDG edition and are excluded — reported as a data-scope
limitation, not worked around.) Per parent, all properties whose description
starts with "A(CP)" with a measured `best_summary()` value and error, non-limit.
Real PDG data only. No fabrication. If a parent yields < N_FIX clean modes it is
dropped from the PRIMARY test.

## 4. Honest commitments

- The prior is NULL. A corridor claim must clear section 2's bar to be reported
  as anything other than null.
- A_CP is not a coordinated rung (section 0); even a numerical "hit" would be a
  coincidence of the descriptive statistic, not framework support, and would be
  reported with that caveat.
- Nulls reported as nulls.

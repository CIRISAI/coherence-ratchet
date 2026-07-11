# Pre-commitments — CKM in the hierarchical (Froggatt-Nielsen) measure

**Date 2026-07-11. Written BEFORE any ensemble was generated.** This file freezes the
measure, the coefficient distributions, the tests, and the kills. The companion Haar test
(`../results.json`, `../SUMMARY.md`) showed CKM is Haar-ATYPICAL (99.98th-pct MI). This test
asks the missing half: is CKM TYPICAL of the hierarchical measure — the standard sketch of
quark flavor? PMNS is the control (expected FN-atypical, so the two books differ by measure,
not by accident).

## 1. THE MEASURE — fixed from literature, not from fit

**Froggatt–Nielsen U(1) flavor mechanism** (Froggatt & Nielsen, *Hierarchy of Quark Masses,
Cabibbo Angles and CP Violation*, Nucl. Phys. B147 (1979) 277 — the original). Yukawa entries
are order-one coefficients times a power of a single small expansion parameter set by the U(1)
charges:

    Y^u_ij = c^u_ij · ε^|X_Q_i − X_u_j|
    Y^d_ij = c^d_ij · ε^|X_Q_i − X_d_j|

**Charge assignment — taken verbatim from a verified published source, NOT tuned here:**
the top-ranked "natural" texture of Bahl, Fuentes-Martín, Hiller, ... (Mannheim/Zurich group),
*Mapping and Probing Froggatt–Nielsen Solutions to the Quark Flavor Puzzle*,
arXiv:2306.08026, Phys. Rev. D 111 (2025) 015042, Table 1 (their most stringent naturalness
measure, ℱ₂ = 2.7%):

    X_Q = ( 3,  2,  0)     # left-handed doublets
    X_u = (-4, -2,  0)     # right-handed up-type
    X_d = (-3, -3, -3)     # right-handed down-type

These charge DIFFERENCES reproduce the observed Wolfenstein CKM hierarchy parameter-free:
|V_us| ~ ε^|3−2| = ε, |V_cb| ~ ε^|2−0| = ε², |V_ub| ~ ε^|3−0| = ε³. This is why the assignment
is the standard sketch of quark flavor and is the correct null for a CKM-typicality test — the
ensemble is NOT rigged for or against the observed Cabibbo angle; the angle is the generic FN
scale.

**Expansion parameter ε — fixed to the Cabibbo angle, NOT tuned:**
- PRIMARY: **ε = 0.225** (the Cabibbo angle, PDG). Held fixed; never fit to the data.
- SENSITIVITY (test d): ε = 0.20 and ε = 0.25. Report drift; never promote.

## 2. THE O(1) COEFFICIENT DISTRIBUTION — pre-committed, one primary

Each c^u_ij, c^d_ij is an independent complex O(1) number. Fixed BEFORE computing:
- **PRIMARY:** |c| log-uniform on [1/3, 3]; arg(c) uniform on [0, 2π). (The standard "anarchic
  O(1)" prescription; the interval [1/3,3] is the mission-fixed modulus range.)
- **ROBUSTNESS 1 (test d):** complex Gaussian — Re(c), Im(c) i.i.d. N(0,1) (⇒ |c| Rayleigh,
  the other mission-menu choice).
- **ROBUSTNESS 2 (test d):** log-normal on |c| — ln|c| ~ N(0, 1); arg uniform. (The prior the
  source paper 2306.08026 actually uses; added for fidelity to the literature measure.)

Diagonalization: for each (Y_u, Y_d) draw, take the left singular vectors U_uL, U_dL from the
SVD (numpy, descending singular values ⇒ mass-ordered basis, consistent for both sectors);
V_CKM = U_uL† U_dL, exactly unitary. All six functionals are rephasing-invariant (they use
only |V_ij|² or the physical Jarlskog combination), so no phase convention needs fixing.

## 3. SAMPLES & FUNCTIONALS

- **N ≥ 50k.** Primary run N = 100,000; each robustness variant N = 50,000. Fixed seeds
  (base 20260711), CPU only, incremental flush to results.json.
- **Functionals — the SAME six as `../run_mixing.py`**, imported directly (no reimplementation):
  MI, S_onehot, PR_sv, d_anarchy, d_perm, absJ (plus back-out sin²θ). Added derived functional
  for the joint test: **|sinδ|_eff = absJ / J_max(angles)**, with
  J_max(angles) = c12 s12 c23 s23 c13² s13 (the Jarlskog algebraic ceiling; the phase factor of
  the sakharov-ledger decomposition), clipped to [0,1].

## 4. TESTS — pre-stated

- **(a) Marginal typicality.** Percentile of the OBSERVED CKM's each of the six functionals
  within the FN ensemble. **PASS = all six inside the central 90%** (percentile ∈ [5, 95]).
- **(b) Joint typicality (the double-extremity question).** Is the observed triple
  (MI, |J|, |sinδ|) a GENERIC FN draw? Primary metric: percentile of |J|_obs *within the
  subset of FN samples that are at least as aligned as CKM* (MI ≥ MI_obs) — if CKM's CP-tininess
  is central in that high-alignment subset, then "aligned AND CP-tiny" is ONE generic FN fact,
  not two coincidences. Also report the |sinδ|_obs percentile in the same subset, and the
  all-three-inside-central-90% joint flag. **PASS = |J|_obs and |sinδ|_obs both inside central
  90% of the MI≥MI_obs subset** (i.e. the double extremity is generic given the alignment).
- **(c) Control — PMNS vs the SAME FN ensemble.** Pre-stated expectation: **PMNS is
  FN-ATYPICAL** — it should sit in the LOW-MI (anarchic) tail of the hierarchical ensemble
  (percentile < 5 on MI), because the FN quark measure generically produces aligned matrices.
  PASS of the two-books thesis = PMNS MI percentile < 5 (or otherwise outside central 90%).
- **(d) Sensitivity.** Repeat (a) for the two robustness c-distributions and for ε = 0.20, 0.25.
  Report percentile drift. Never promote a distribution/ε that helps; report all.

## 5. KILLS — pre-stated (adverse outcomes reported straight, no spin)

- **CKM outside the FN central 90% on MI ⇒ CKM is atypical of BOTH measures.** That is a
  DISCOVERY — an unexplained flavor structure typical of no standard measure. Report it straight;
  do NOT reframe as a win for the ledger.
- **PMNS FN-typical (inside central 90% on MI) ⇒ the two-books measure distinction COLLAPSES.**
  Report straight; the "quarks and leptons are two books each typical of its own measure" claim
  loses its measure-separation half.
- Robustness/sensitivity that flips a verdict (test d) ⇒ the verdict is distribution-dependent,
  not a fact about CKM; report the fragility, do not cherry-pick the passing variant.

## Sources (verified this session)
- Froggatt, Nielsen, Nucl. Phys. B147 (1979) 277 — original FN mechanism. [standard]
- arXiv:2306.08026 / Phys. Rev. D 111 (2025) 015042 — FN-ensemble scan, charge texture
  X_Q=(3,2,0), X_u=(-4,-2,0), X_d=(-3,-3,-3); log-normal O(1) prior, uniform phases. [verified]
- arXiv:2411.05398 — cross-checked FN SU(5) benchmark (10=(4,2,0), 5bar=(4,3,3), ε=0.20);
  NOT used as primary because its charge differences give |V_us|~ε², not the Cabibbo angle.
  [verified, recorded for completeness]

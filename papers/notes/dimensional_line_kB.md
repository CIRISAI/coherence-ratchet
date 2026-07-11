# The dimensional line: κ is the program's Boltzmann constant

**Date 2026-07-10.** Stance note, written from the dm-mass kill
(`experiments/dark_sector_mass/SUMMARY.md`) viewed sideways. This note states a structural
discovery about the framework itself, promotes a theorem-backed error-detector to standing
rule, and reduces three open dimensionful problems to one.

## 1. The discovery: the hit/miss boundary is the dimensional line

Every confirmed result the program owns is **dimensionless**: the sign law
`1 + w = −⅓·dlnS/dlna` (κ cancels), the corridor ρ ∈ (0.1, 0.43), the k_eff ≤ 10 ceiling,
ln2 per fermionic mode, the crossing epoch as a redshift, w itself. Every undetermined or
underivable object is **dimensionful**: κ, the unit scale (~7×10¹¹ M⊙/h, currently an
input), the DM particle mass (kill: candidate bridges scatter over 41 orders of magnitude —
the shape of a theory with no scale to leak, not a near-miss).

This is one fact, not a coincidence: **S is a copula functional, amplitude-blind by theorem
(clause 3).** The same clause that cancels κ out of the sign law — making it parameter-free —
forbids any native dimensionful prediction. A mass is an amplitude-sector object the
functional cannot see. The dm-mass kill was therefore a *required* consistency pass: a clean
non-arbitrary ρ_Λ → m link would have contradicted clause 3. Rule-2 weight, stated plainly:
this is a coherence pass, not support — given the theorem it could hardly have been
otherwise.

## 2. The k_B framing

Statistical mechanics was exactly here. `S = ln W` is dimensionless and parameter-free;
**k_B is the single conversion constant** that marries the counting to energy and
temperature, and it was fixed not from within the theory but by marriage to an external
scale (Avogadro's number). For decades thermodynamics was a correct shape-calculus with an
empirically-set bridge constant — and that was never a defect.

**κ is the program's k_B.** The three open dimensionful problems collapse into one
question: *what is one coordinating unit, in physical units?* Fix that single marriage and
κ follows from matching ρ_DE today. Nothing else dimensionful is owed — masses, scales, and
energy densities are either (dimensionless ratio) × (the one married scale), or they are
not the ledger's to predict.

**The measurement — RUN AND KILLED IN AUDIT (2026-07-10, same night):** retention-v2's raw
scan extremized at 10^11.89, 0.09 dex from the SHM peak — and the pre-registered adversarial
controls killed the reading (`retention_v2/CHALLENGES.md`): lowering the GPU cap moved the
extremum to the new cap boundary (C1, artifact confirmed), and k-matched thinning erased
11.89's edge entirely (C2) — the best-fit threshold is set by the k-budget, not by a
physical mass scale. The h-factor bookkeeping was clean (C4) and the SHM coincidence is a
genuine but *passenger* consilience (C5: the fit threshold is fixed by assembly-epoch + DESI
with zero SHM input). **Verdict: κ stays empirical** — the theory is in its
pre-Avogadro state, a counting theory with a measured bridge constant.

**The path that opened (sideways pass on the kill, same night):** the audit's own data carries
two positive monotonicities — more units → better fit, and more-massive units at fixed count →
better fit (the C2 overshoot) — consistent with an **aperture law**: fit quality is monotone in
completeness of the read, exactly what the married gravity ontology requires (S sourcing ρ_DE
is the complete-book read; thresholds and caps are instrumental undersampling). Under this
reading there is no privileged unit mass scale — which is *why* every scale-anchor attempt
dies — the headline 1.36σ is a lower bound, and the unit-scale question dissolves into the
complete-book normalization. Hypothesis weight; two-sided test pre-registered in
`retention_v2/CHALLENGES.md` (downward cap-step non-decisive by construction; upward
full-population tiled S is decisive: complete-book fit ≥ 1.36σ or the artifact reading
reasserts).

**Outcome (same night): the upward test FAILED — aperture law falsified.** The gate-validated
complete-book read gives 2.21σ (worse than the corner grain's 1.36σ, still better than
ΛCDM's 3.28σ). The unit-scale question does NOT dissolve; it sharpens into the **grain
problem** (`the_grain_problem.md`): which units post to the ledger is an open input, with the
galaxy-defined book (rung membership) as the pre-registered candidate. If that also fails,
the theory carries a second constant beside κ — exactly the outcome §5's kill pre-staked.

## 3. Standing rule (theorem-backed confabulation detector)

**Any claimed derivation of a dimensionful quantity from the ledger alone is a structural
error — reject on sight, before checking the arithmetic.** Cases already caught: the
"entropy minimization selects SU(3)×SU(2)×U(1)" AI-summary confabulation (appears in zero
papers); the dm-mass 41-order scatter. The detector is now a rule, not a case-by-case
debunk. Its contrapositive is equally binding: a *legitimate* ledger prediction is
dimensionless, and should be parameter-free — a dimensionless prediction that needs a tuned
constant is also off-pattern and gets flagged. **Extension (sm_escalator_map.md §1):** the
forbidden set also includes dimensionless *marginal-native* quantities (mass ratios,
coupling strengths) — the copula strips marginals, not just dimensions, so a claimed
mass-ratio derivation from the ledger alone is the same structural error.

**The general form (PROVENANCE LINE, promoted 2026-07-10 after the escalator fleet):**
`S = −ln det C` is a function of the correlation matrix; **it is blind to every fact that is
upstream of C** — the provenance of its own input. Four instances, each independently
established:
1. **Scale** (dimensional line): no masses, no κ, no energy densities. `dark_sector_mass/`.
2. **Marginals** (second cut): no mass ratios, no coupling strengths, dimensionless or not.
   `sm_escalator_map.md` §1.
3. **State-space construction** (exchange line, `StatisticsNoGo` at theorem strength): no
   exchange sign, no occupation ceiling, no ln2-as-a-value — statistics is input, and the
   ledger reads only its consequences (the validated ln2-vs-Gaussian rigidity difference).
   `sm_escalator_statistics.md` §4–5.
4. **Factorization** (gauge quotient): on gauge systems the partition into units is itself
   non-canonical (Casini–Huerta–Rosabal center ambiguity), so the ledger must be built from
   gauge-independent data — relative entropy / mutual information — or it carries a
   boundary-local artifact. Adopted as a consistency prescription. `sm_escalator_gauge.md` §3.

One sentence for all four: **the ledger reads dependence-shape downstream of a chosen,
already-constructed factorization; everything about the construction — its scale, its
marginals, its statistics, its partition — is input, and any claimed derivation of an
upstream datum from the ledger alone is rejected on sight.**

## 4. Corollary: the admissible attack surface on the Standard Model

The ledger's only admissible SM targets are the **dimensionless sector** — and, per the
escalator map's second cut (`sm_escalator_map.md` §1, which corrects this note's first
draft), only its **dependence-native** part: mixing angles, generation counting as a
spectral degeneracy, phases. Mass *ratios* and dimensionless coupling values are
marginal-native — ratios of single-direction strengths — and the copula strips them by the
same clause-3 theorem that strips κ; they are NOT admissible targets despite being
dimensionless. And the SM cooperates with this framing more than folklore
suggests: **the SM itself has essentially one dimensionful parameter** — the Higgs vev
(every fermion mass is a dimensionless Yukawa × v; Λ_QCD is generated from the
dimensionless g_s by transmutation). A counting theory with one bridge constant is not a
strange shape for fundamental physics; it is the shape the SM already has. The escalator,
if it exists, runs entirely inside the dimensionless sector, with one marriage at the top.

Attack notes (theory, discovery-mode, kills staked): `sm_escalator_map.md`,
`sm_escalator_statistics.md`, `sm_escalator_gauge.md`.

## 5. This note's own kill

If the program is ever forced to admit a **second independent dimensionful input** — one not
derivable from the first marriage plus dimensionless structure — the one-constant claim
fails and this is not a counting theory with a bridge but a multi-parameter model. Dated
debt: the retention-v2 verdict (in compute) is the first test; the DR3 retrodiction is the
second.

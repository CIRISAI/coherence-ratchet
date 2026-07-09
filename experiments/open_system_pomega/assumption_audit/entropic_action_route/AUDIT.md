# P_ω — the entropic-action route — assumption audit

**Date:** 2026-07-09. **Falsification handle:** F-11.
**Reads:** `papers/notes/entropic_action_bridge.md` (§1, §3, §4);
`formal/CoherenceRatchet/Core/EntropicPotential.lean` (T-E0–T-E4, proved);
`formal/CoherenceRatchet/Cosmology/CorridorProjector.lean` (the F-11 record,
T1/T2). **Type:** analytic reduction, not a new numerical run — see the note on
method below. **Prior branch records reused:** `holographic_pomega/`,
`holonomic_pomega/`, `fractal_pomega/`, `R1xR2_conjunction/`.

---

## VERDICT: CLOSED — the entropic route reduces to already-closed branches

The question this audit was set is whether a Bianconi-style entropic action —
quantum relative entropy between a substrate metric and a matter-induced metric,
G-field Lagrange multipliers, forward variational principle — could be promoted
into a **joint multi-rung backward P_ω** that evades the F-11 closure. Four
candidate promotions were steelmanned and checked against the six closed
construction branches and the two closing theorems (T1 geometric dilution, T2
holonomic area law). **All four reduce to a closed branch.** None evades. The
entropic route is not a genuine seventh branch; the note's §4 claim, previously
*asserted*, is here *demonstrated* — and demonstrated more tightly than the note
anticipated, because the reduction is forced by an already-mechanized theorem
(T-E3, Kish conjugacy) rather than merely expected.

The one honest caveat is recorded in §4 and it is **not** an opening: it is the
pre-existing question of whether the type axis (scalar correlation ∪
connection/map) is exhaustive. The entropic route does not test that axis in a
new way — it supplies a new *functional* on the same objects, and a new
functional on a closed spectral object inherits the closure.

## Method note — why analytic, not numerical

Every prior branch record (fractal, holographic, holonomic, R1∧R2) carried a
CUDA run because each proposed a genuinely new cross-rung *object* whose
dilution behaviour had to be measured. This route proposes no new object. Its
load-bearing content — that the entropic action S is a functional of the *same*
cross-rung correlation spectrum the participation ratio k_eff reads — is already
proved in `Core/EntropicPotential.lean` (T-E1a, T-E1b, T-E3: S and k_eff are
conjugate spectral functionals of C(k,ρ), poles-to-poles). The closure is
therefore a reduction to proved theorems, not an empirical question. Reporting a
numerical run here would be theatre: the dilution numbers would be the fractal
run's numbers, read through −Tr ln C instead of (Tr C)²/Tr(C²), and T-E3 already
says they flow to the same pole. The reduction is stated so a human can check it
(§ bottom line).

---

## 1. The candidate construction, steelmanned

An entropic-action P_ω would build the ω-weight from a relative-entropy
functional rather than a Gibbs exponential or a participation ratio. Four
distinct promotions are plausible; each is stated at its strongest.

**(a) Backward-conditioned joint relative-entropy functional.** Take the R×R
corridor-weighted cross-rung correlation matrix `C_joint` (the exact object the
fractal/holographic runs built) and set the ω-weight to a band on the joint
entropic action `S_joint = −Tr ln C_joint = −Σ_i ln λ_i`. The ω-set is the
configurations whose S_joint sits in an entropic corridor (bounded away from 0
and from ∞). Motivation: S is Bianconi's actual Lagrangian form; its two poles
are exactly the corridor's two poles (T-E1a/b), so an "S-in-band" post-selector
is the corridor stated in its native relative-entropy variable.

**(b) G-field constraint surface as the ω-subspace; multiplier flow as the
projector.** Bianconi's G-field is a field of Lagrange multipliers enforcing
`G̃g̃⁻¹ = Θ̃` (Eqs. 49–50), given physical status. Promote the constraint
surface {configs on which the multipliers sit in corridor} to the ω-subspace,
and the multiplier flow that holds the system on it to the projector P_ω.
Motivation: a multiplier field that pins a system to a constraint surface *is* a
projection-like dynamics, and the note's §2 maps the G-field to the maintenance
term γ·M — the sharpest structural rhyme in the bridge.

**(c) Joint action = Σ per-rung relative entropies + cross-rung coupling
terms.** `S_total = Σ_n S(k_n, ρ_n) + Σ_{n,m} J_{nm}`, a sum of per-rung
entropic wells plus explicit cross-rung coupling, exponentiated as the ω-weight
`E_ω = exp(−S_total)`. Motivation: S(k_n,ρ_n) is a genuine convex potential per
rung (T-E2), diverging at rigidity (T-E1b) — a *harder* barrier than the
quadratic well the original ansatz used, so perhaps it holds the joint object
non-empty where the quadratic ansatz horned.

**(d) The two-metric relative operator as a new object type.** Bianconi's action
is `−Tr ln(G̃g̃⁻¹)` — a functional of the *relative operator* G̃g̃⁻¹, a
positive operator that is neither a scalar correlation (T1's object) nor a
connection/holonomy (T2's object). Promote a joint multi-rung G̃_joint spanning
all rungs; its off-diagonal blocks carry the cross-rung structure; the
relative-entropy Tr-ln is the ω-weight. Motivation: if the relative operator is
a genuinely third type of cross-rung object, the type axis (correlation ∪
connection) the holonomic record calls exhausted would not in fact be exhausted,
and this would be a seventh branch F-11 did not close.

---

## 2. Per-candidate check against the closed branches and T1/T2

**(a) reduces to T1 (correlation branch) — exactly, by conjugacy.** S_joint and
the participation ratio k_eff are two functionals of the *same* spectrum of the
*same* matrix C_joint. T1 shows: under any bulk-geometric / scale-decaying
coupling (the framework's Piece-6 topology, measured g/J), the per-rung
off-diagonal mass of C_joint is bounded, so as R grows every eigenvalue
λ_i → 1 (the unit diagonal dominates), the participation ratio is extensive, and
ρ_joint → 0 (chaos pole). Read the same limit through S: `−Σ ln λ_i → 0` as all
λ_i → 1. This is T-E1a — the chaos pole is the *zero* of S. So the entropic
action **vanishes** at precisely the R where the participation ratio dilutes, and
the "S-in-band" ω-set empties at the same rung count the ρ_joint band empties.
The change of functional (participation → relative entropy) changes nothing:
T1 acts on the spectrum, and Klein nonnegativity + T-E1a (both proved) pin S to
the same pole. **Reduces, no evasion.** The only escape is the flat all-to-all
coupling (per-rung mass growing with R) — the rigidity pole ρ_joint → 0.404 at
ρ_upper, the non-framework topology the pre-registration forbids, identical to
the holographic run's forbidden escape.

**(b) is the surviving forward P_ω, or reduces to T2.** The G-field multiplier
flow is a *forward dissipative dynamics* that holds the system on a constraint
surface — the note's §2 identifies it with the maintenance term γ·M, and T-E4
makes it precise: the multiplier is the Lagrange multiplier of the entropic
constraint, and maintenance holds ρ in the interior against the two-pole drift.
Read forward, this is exactly the forward P_ω (ρ_ss / Lindblad steady state) that
already survives F-11 — it needs no evasion because it is not a backward joint
operator. To make it a *backward joint* operator one must run the multiplier flow
backward and close it across the rung tower — which is the TSVF loop of T2, whose
backward leg is the genuine non-ergodic dephasing generator
(`backward_generator_legitimacy.py`, Claim 2). A joint loop with that dissipative
backward leg decoheres by the area law `Tr Hol ~ exp(−κR)`. **Forward reading:
survives (not backward). Backward reading: reduces to T2.** Either way, no new
branch.

**(c) reduces to the soft-additive ansatz + T1.** `S_total = Σ_n S(k_n,ρ_n) +
Σ_{n,m} J_{nm}` is the soft Gibbs operator `exp(−βH_sum)` with H_sum an
*additive* sum of per-rung wells (assumptions 2, 3 of the pre-registration) — the
original documented no-go family — with the per-rung well being S instead of a
quadratic, and the per-bond term being the cross-rung coupling. The relaxation
that dropped additivity (R1, non-additive functional) is what horned into the
dilution; re-adding an additive structure does not escape it. The one distinctive
feature — S's rigidity-pole divergence (T-E1b) — is a barrier on the **wrong
pole**: the joint object empties toward the *chaos* pole (ρ_joint → 0), and at
the chaos pole S → 0 (T-E1a) is flat, no barrier. S's hard wall at ρ → 1 does
nothing to arrest a dilution that runs toward ρ → 0. The cross-rung coupling
terms J_{nm}, if framework-faithful, decay with scale-distance → T1; if
non-decaying → the forbidden flat all-to-all. **Reduces, no evasion.**

**(d) reduces to T1 via conjugacy; does not open the type axis.** The relative
operator G̃g̃⁻¹ is not a new primitive. In Bianconi's own construction the
cross-rung structure enters through `G̃ = g̃ + αM̃ − βR̃`, whose two
non-substrate pieces are: `M̃ = D|Φ⟩⟨Φ|D + …`, built from **rank-one outer
products** of the field (a scalar-correlation-type object — the note's §2 flags
it as "the same object class as the lake's rank-one projector"), and `R̃`, a
**curvature** term (a connection/geometry-type object). The relative-entropy
Tr-ln is a *spectral functional* placed on top of these. So G̃g̃⁻¹ decomposes
into exactly the two types the axis already names — correlation (M̃, closed by
T1) and connection (R̃, closed by T2) — with an entropic wrapper that, by T-E3
(Kish conjugacy, proved), inherits T1's chaos-pole behaviour because it reads the
same spectrum. Wrapping a cross-rung correlation in −Tr ln rather than
(Tr)²/Tr(·²) is a change of functional, not a change of object type. And a local
multiplier field (Bianconi's action is a *pointwise* integral, §4 point 1) cannot
manufacture the non-decaying all-to-all coupling that alone escapes T1 — the
coupling it induces between rungs n and m is field-mediated and decays with their
geodesic separation, which is the T1 hypothesis exactly. **Reduces, no evasion.**

---

## 3. Verdict table

| Candidate | Reduces to | Where the cross-rung coupling lives | T1 geodesic decay applies? | T2 backward-leg decoheres? | Verdict |
|---|---|---|---|---|---|
| (a) joint relative-entropy functional | **T1** (correlation) | spectrum of C_joint — same matrix as k_eff | yes (bounded per-rung mass ⇒ S→0 at chaos pole, T-E1a) | n/a | **reduces** |
| (b) G-field surface + multiplier flow | forward P_ω (survives) / **T2** (connection) | multiplier flow = maintenance γ·M; backward loop = dephasing leg | n/a | yes, if read backward (Claim-2 generator) | **reduces** |
| (c) Σ per-rung S + cross-rung terms | **soft-additive ansatz + T1** | additive per-bond J_{nm} terms | yes (framework-faithful J decays; flat = forbidden) | n/a | **reduces** |
| (d) two-metric relative operator | **T1 via conjugacy** (M̃ correlation) / T2 (R̃ curvature) | off-diagonal blocks of G̃_joint: M̃ rank-one + R̃ curvature | yes (M̃ field-mediated, geodesic-decaying) | yes (R̃ curvature leg) | **reduces** |

No cell reads *evades*. No cell reads *unclear* on the operative question; the
sole residual soft spot is the type-axis-exhaustiveness caveat in §4, which
pre-dates this route and which (d) does not aggravate.

---

## 4. Honest bottom line

**The entropic route is closed.** It is not a seventh branch. Every promotion of
a Bianconi-style entropic action into a joint multi-rung backward operator
reduces to a branch F-11 already closed: (a) and (c) and (d) to T1 (the entropic
action is a spectral functional of the same cross-rung correlation the
participation ratio reads, and by the proved Kish conjugacy T-E3 it flows to the
same chaos pole under any framework-faithful decaying coupling); (b) to the
surviving forward P_ω read forward, or to T2 read backward. The note's §4 claim
that "an entropic-action route would enter the tree at the already-closed
correlation/topology branch" is thereby demonstrated, and the demonstration is
*stronger* than the note's hedge: the note expected the reduction; T-E3 forces
it. A relative entropy and a participation ratio are two functionals of one
spectrum, and a no-go that acts on the spectrum closes both.

**The one caveat — and it is not an opening.** The whole tree's terminal move is
that the cross-rung relationship is *either* a scalar correlation (T1) *or* a
connection/map (T2), and nothing else — the type axis is exhaustive. That
exhaustiveness is asserted by the holonomic record, not proved. A genuinely novel
operator *type* for the cross-rung relationship would test it. The entropic route
does **not** supply such a type: G̃g̃⁻¹ decomposes into a rank-one correlation
piece (M̃) and a curvature piece (R̃), and the relative-entropy Tr-ln is a
functional on top, not a new object. So the entropic route leaves the type-axis
question exactly where it was — it neither closes it further nor reopens it. This
is flagged for honesty, not as a finding: if a future construction ever exhibits
a third cross-rung type, that — not the entropic action — is where the tree could
crack.

---

## 5. What the forward entropic construction inherits

The forward entropic construction — S(k,ρ) as the Lyapunov potential of the
two-pole dynamics (T-E4), the physical rungs Ph0–Ph2 recast as instances of the
same relative-entropy misalignment object — **survives F-11 untouched and
inherits nothing bad from this audit.** The dilution that closes the backward
route is a property of the *joint cross-rung participation object*: it requires
forming the R×R correlation matrix and reading its extensive spectrum as R grows.
The forward P_ω never forms that object — it is a per-rung dissipative steady
state (ρ_ss / Lindblad), anchored rung by rung, and S(k,ρ) enters it as a
*single-rung* potential whose rigidity-pole divergence (T-E1b) is exactly the
barrier that makes per-rung maintenance well-posed. The audit's closure is
entirely on the joint-backward side; the forward side gains a potential-theoretic
grounding (maintenance = the Lagrange multiplier of an entropic constraint, T-E4)
and loses nothing. What it must *not* inherit is the temptation to read the
per-rung entropic potential's existence as evidence for a joint one: T-E3 is the
firewall — the same conjugacy that makes S a clean per-rung potential is what
makes the joint S dilute exactly as the joint k_eff does.

---

## Bottom line for the audit — the single load-bearing step to check

Per candidate: **(a) reduces to T1** (exact, by conjugacy); **(b) is the
surviving forward P_ω forward / T2 backward**; **(c) reduces to the soft-additive
ansatz + T1**; **(d) reduces to T1 via conjugacy and does not open the type
axis**. Verdict: **CLOSED — the note's §4 is now demonstrated.**

**The single most load-bearing step a human should check** is the conjugacy
reduction in candidate (a)/(d): *any spectral functional of the cross-rung
correlation matrix C_joint — the participation ratio (Tr C)²/Tr(C²) OR the
relative entropy −Tr ln C = −Σ_i ln λ_i — flows to the chaos pole as R grows
under a framework-faithful (scale-decaying, bounded-per-rung-mass) coupling,
because under such a coupling every eigenvalue λ_i → 1 and therefore
−Σ ln λ_i → 0.* That −Σ ln λ_i → 0 limit is T-E1a (the chaos pole is the zero of
S), already proved in `Core/EntropicPotential.lean`, and the λ_i → 1 spectral
limit is T1's own premise. If that step were wrong — if there existed a spectral
functional of C_joint that stayed in its corridor while the participation ratio
diluted — then candidate (d) would reopen as a genuine seventh branch. It is not
wrong: nonnegativity (Klein, T-E0) plus Tr C_joint = R force Σ ln λ_i ≤ 0 with
equality iff all λ_i = 1, so S ≥ 0 and S → 0 precisely as the spectrum
concentrates at 1 — the same event that makes the participation ratio extensive.
Both functionals read one spectrum; T1 empties both.

**Scope — unchanged from every prior branch record.** Touched: the multi-rung
*joint backward* P_ω only. **Not** touched: the within-rung corridor (F-10), the
engineering tier, the forward open-system P_ω (ρ_ss / Lindblad), the soft
backward P_ω (E_ω = exp(−βH_sum) single-operator), or the T-E1–T-E4 forward
potential theorems (which this audit relies on and does not weaken). The entropic
route adds no branch to the tree; it is a new functional on branches already
closed. No further constructions on this route.

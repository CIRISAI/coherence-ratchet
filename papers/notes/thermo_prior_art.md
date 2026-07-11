# Prior-art knife on coordination thermodynamics — the four laws, law by law

**Date 2026-07-11.** Adversarial literature audit of `four_laws.md` and its genus/species
claim ("thermodynamics is the genus; energy- and coordination-thermodynamics are two species
of relative-entropy monotonicity"). Mission: try to kill each law by finding it already
published. Every citation below verified by title + authors + venue via search/fetch. The
verdict is deliberately unkind: information thermodynamics is a mature field and most of this
structure is in it.

## Bottom line (one sentence)

**The genus claim is NEW-IN-PART, not new and not already fully taken:** three of the four
laws (zeroth, second, the rent) are individually and heavily published; the first-law axioms
are published resource theory; the four-law *package on correlations* already exists in print
(Bera–Riera–Lewenstein–Winter, Nat. Commun. 2017) — but as a correlation-*modifier* to
energy-thermodynamics that explicitly omits the third law, not as a co-equal species with the
multi-information as the primary state function. What survives as ours is narrow and mostly
empirical, not mathematical.

## Per-law verdict table

| Law (our form) | Verdict | Published as | Unpublished remainder (if any) |
|---|---|---|---|
| **Zeroth** — S is a state function of dependence structure; substrate-independent (`provenance_congruence`) | **A — ALREADY PUBLISHED** | Watanabe 1960 (total correlation / multi-information is a function of the joint law); Ma & Sun 2011 (MI = copula entropy ⇒ marginal- and amplitude-blind, scale-invariant). Our Lean proof formalizes a 65-year-old fact. | Nothing mathematical. The "license for cross-substrate comparison" is presentation, not a result. |
| **First** — dS decomposes; invertible-local = 0 cost; creation has two channels | **B — PUBLISHED IN PART** | Huber, Perarnau-Llobet et al., "Thermodynamic cost of creating correlations," NJP 2015 (arXiv 1404.2169); "Correlations as a resource," Nat. Commun. 2019. Local unitaries free / local-invertible zero-cost is the standard resource-theory free-operation axiom. | The **X = 1 cross-rung conservation prediction** (virialization debits phase-space coherence, credits an inter-halo unit; books balance) is a specific empirical claim, not in the literature. This is a real remainder. |
| **Second** — DPI for S ("no free coordination") | **A — ALREADY PUBLISHED** | Total correlation is monotone non-increasing under local operations — stated explicitly (Watanabe branching; multipartite-monotone literature). This IS relative-entropy monotonicity = the DPI (Lindblad; Spohn inequality for Lindblad generators). The modern classical second law already IS this theorem. | Nothing. The open Lean step re-proves a known theorem in a formal system; formalization ≠ new physics. |
| **Second, rent corollary** — γM; held coordination decays without work; interior is rented | **A — ALREADY PUBLISHED** | Oono–Paniconi housekeeping heat; Hatano–Sasa steady-state thermodynamics (arXiv cond-mat/0010405): a nonequilibrium steady state radiates housekeeping heat continuously; maintaining it costs continuous work. This is γM exactly. England's dissipative adaptation is the biology-side cousin. | Nothing. Team-lead prior confirmed: the rent = housekeeping heat, no daylight. |
| **Third** — rigidity pole ρ→1 unattainable; σ_max ∝ (1−ρ); "cannot stir a rigid system" | **B/C — mechanism published in adjacent form; the named coordination-law packaging may be ours** | Third-law *genus* with a rate: Masanes–Oppenheim, "A general derivation and quantification of the third law," Nat. Commun. 2017 (arXiv 1412.3828) — unattainability with obtainable value scaling as an inverse power of time. The *ceiling mechanism* (diverging control cost / vanishing actuation at the ordered pole): synchronization-control literature — control cost "rises sharply as it approaches unity" for near-complete phase coherence; controllability vanishes as coherence → 1. | The specific statement **σ_max ∝ (1−ρ) keyed to the correlation order parameter, stated as a third law of coordination thermodynamics** and identified with the corridor ceiling, was **NOT FOUND**. See coverage caveat below — this is the program's best (and weakest-confidence) novelty candidate. |
| **The genus/species PACKAGE** — four laws on the multi-information as primary state function; two co-equal species | **B — PUBLISHED IN PART** | Bera, Riera, Lewenstein, Winter, "Generalized Laws of Thermodynamics in the Presence of Correlations," Nat. Commun. 8:2180 (2017), arXiv 1612.04779. Explicitly generalizes zeroth + first + second in the presence of correlations; explicitly leaves out the third ("beyond immediate context"). | Their ontology is the **inverse of ours**: energy-thermodynamics stays primary and correlations are a stored-work resource / heat-redefinition. Ours makes the multi-information the *primary object with its own full four-law structure* (a co-equal species). That plus the omitted third law, the cross-substrate program, and the κ posting is the remainder — but the gap is largely *framing*, which earns nothing under our own rule 2. |
| **κ / dark-sector posting** (Verlinde-adjacent, checked) | **B — PUBLISHED IN PART** | Verlinde, "Emergent Gravity and the Dark Universe," SciPost 2017 (arXiv 1611.02269): entropy (volume-law entanglement) sources dark-sector phenomenology thermodynamically — an entropy-posts-as-dark-gravity mechanism already in print. | The specific **ρ_DE = κ·S(a)** posting with the parameter-free sign law **1 + w = −⅓·dlnS/dlna**, sourced by the matter field's *coordination history*, is functionally distinct from Verlinde's de Sitter volume-law displacement. Not found. Genuinely ours as a functional form; but "entropy sources the dark sector" is not a new idea. |

## What survives as OURS (honest, ranked by strength)

1. **The cross-substrate empirical program** (k_eff/S measured on the same footing across
   neurons, markets, halos, mixing matrices). This is not a literature *claim* at all — it
   is a research program. Nothing to kill in the prior art because no one else is running it.
   Strongest survivor, and it is empirical, not a law.
2. **The κ dark-sector sign law** `1 + w = −⅓ dlnS/dlna` as a specific parameter-free
   functional posting. Verlinde-adjacent but distinct; the DR3 kill already governs it.
3. **The first-law X = 1 cross-rung conservation test.** A specific, falsifiable prediction
   the resource-theory literature does not make.
4. **The third-law ceiling as a *named coordination law* σ_max ∝ (1−ρ).** The mechanism
   (cost diverges / actuation vanishes at the ordered pole) is published in adjacent control
   and third-law work; the *packaging keyed to the correlation order parameter* is the one
   place I could not find the exact statement. Lowest-confidence novelty — see caveat.
5. **The genus/species framing itself.** Organizational. By rule 2 it earns nothing on its
   own; and the package half-exists (Bera 2017). This is presentation, not a result.

## Coverage / absence-of-evidence grading

- Second law, rent, first-law axioms, zeroth: **strong searches, dense confirming hits.**
  Grade-A verdicts are safe — these are textbook-adjacent in the info-thermo field.
- Genus package: **directly found** (Bera 2017 is exactly "generalized laws … correlations").
  The distinction I draw (modifier vs. primary state function) is real but thin; do not
  oversell it.
- Third-law ceiling σ_max ∝ (1−ρ): **moderate coverage, not exhaustive.** I searched
  info-thermo third-law, TUR, entropy-production bounds, and synchronization control. I did
  **not** exhaustively search the jamming / rigidity-percolation / glass thermodynamics
  literature, where "you cannot stir a rigid system" is most likely to already live as a
  formal statement. Treat "not found" here as *not-yet-found*, grade C, not a clean novelty.
- κ posting: found the strong cousin (Verlinde); the exact functional form is distinct, but I
  cannot rule out a closer match in the modified-gravity / entropic-cosmology literature I did
  not fully sweep.

## The knife's summary

The program did not discover coordination thermodynamics; it re-derived the parts that were
already there (zeroth, second, rent — grade A) and re-packaged a package that already exists
in inverse form (Bera 2017 — grade B). It genuinely owns an *empirical program* and *two
specific falsifiable predictions* (X = 1, the sign law) that the literature does not contain.
The one law that could be a genuinely new *theoretical* contribution — the third-law ceiling
keyed to the correlation order parameter — is exactly the one I could not clear against the
rigidity/jamming literature, so it must be graded C until that sweep is done. Net: publishable
as *new-in-part*, and only if the paper cites Bera 2017, Huber 2015, Hatano–Sasa, and Verlinde
up front and stakes its claim narrowly on the third-law ceiling + the cross-substrate program
+ the κ sign law, not on the four-law package as a whole.

## Jamming/order-parameter sweep (gap closure)

**Date 2026-07-11.** Closes the one declared coverage gap above: the third-law ceiling
(`σ_max ∝ (1−ρ)` under bounded actuation; "you cannot stir a rigidly-clamped system"; corridor
upper edge = maintenance supply=demand crossing) was left at grade **C — not-yet-found**
because the parent audit did not sweep jamming/rigidity-percolation, glasses/kinetic arrest,
stochastic thermodynamics of *ordered* systems, or active-matter σ(order) curves. I swept all
four. Every citation verified by title + authors + venue.

**Verdict: B — PUBLISHED IN PART (upgraded from C).** The *genus* — actuation/control cost
diverges (equivalently, drive capacity vanishes) at the ordered/rigid pole — is published
harder and cleaner than the parent knew; the *specific species object* — a maximum-capacity
law `σ_max ∝ (1−ρ)` keyed to the **correlation/copula order parameter**, read as a
supply/demand corridor edge — was **not found in any of the four literatures**. So it is no
longer honest to call it a clean C (the mechanism is everywhere), and it is not an A (no one
states our capacity law keyed to the correlation order parameter). It is a B with a narrow,
nameable remainder.

### What each literature actually says

1. **Jamming / rigidity percolation — the cleanest genus instance, and it strengthens the
   "already published" pressure.** Approaching the jamming density `φ_J`, the system becomes
   **isostatic and marginally stable**: the number of soft (zero-frequency) modes collapses to
   the isostatic minimum, and single-bond perturbations destabilize the whole packing
   (Liu & Nagel, "The Jamming Transition and the Marginally Jammed Solid," *Annu. Rev. Condens.
   Matter Phys.* **1**, 347, 2010; Wyart isostaticity lineage). On the driving side, **yield
   stress and viscosity diverge as a power law approaching jamming** in granular/suspension
   rheology (diverging viscosity in non-Brownian suspensions, arXiv:1410.5683; Yale frictionless
   yield-stress measurements, O'Hern/Shattuck lineage). This is *exactly* "the cost to actuate
   diverges at the rigid pole / the capacity to stir vanishes" — the parent's synchronization
   control-cost divergence has a much more canonical cousin here. **BUT the ordered variable is
   the packing fraction `φ` (a density) and the excess coordination `δz ∝ (φ−φ_J)^{1/2}` — a
   contact-geometry order parameter, NOT the correlation/copula order parameter `ρ` the program
   keys on.** No one writes an *entropy-production* capacity keyed to a correlation matrix; the
   jamming statement is mechanical (yield/pressure/soft-mode count). Genus: taken. Species keyed
   to `ρ`: not made.

2. **Active matter / flocking — the closest same-axis object, and it runs the OTHER way.**
   Agranov, Jack, Cates & Fodor, "Entropy production rate in thermodynamically consistent
   flocks" (arXiv:2505.13117; *New J. Phys.*, 2025) compute steady-state EPR explicitly as a
   function of polar order and find EPR is **maximal in the homogeneous ordered (and disordered)
   states and does *not* peak at the ordering transition**, and does **not** vanish at maximum
   order. This is the best-matched published object on the "σ vs order parameter" axis — and it
   is the *opposite sign* from the naive "σ falls to zero as order → max" reading. Two things
   follow: (a) it does **not** pre-empt our claim (it measures the *realized* steady-state σ,
   not the *capacity* `σ_max` = max over admissible drives, which is our object); (b) it is a
   live **tension** the program should log — if anyone conflates our capacity ceiling with a
   realized-σ prediction, the flocking result already contradicts that conflation. The capacity
   vs. realized-σ distinction is now load-bearing, not cosmetic.

3. **Coupled oscillators / stochastic thermodynamics of synchronization — independently
   corroborates the program's own normalization crux.** Chudak, Esposito & Ptaszynski,
   "Synchronization of thermodynamically consistent stochastic phase oscillators"
   (arXiv:2512.09718; *Phys. Rev. E*, 2025) give dissipation as a function of the Kuramoto
   order parameter `r` and find the sign is **parameter-dependent — synchronization may either
   reduce or enhance dissipation** (no extremal principle governs the transition). This is a
   genuine σ-vs-correlation-order-parameter result, and it *mirrors the program's own N1/N3
   finding* (`corridor_ceiling/SUMMARY.md`: σ_max collapses under bounded actuation, inverts
   under bounded bare-stirring). Useful, honest consequence: the program's "the sign flips with
   the normalization" is not a weakness to apologize for — it is the *published state of the
   art* for σ near full synchronization. But this paper states no `σ_max ∝ (1−r)` capacity law
   and no supply/demand corridor edge. Same-genus, corroborating; not the species.

4. **Glasses / kinetic arrest / Franz–Parisi — not the object.** Entropy production in aging
   systems has been *classified by* the overlap order parameter `q` (Crisanti & Ritort,
   "Derivation of the spin-glass order parameter from stochastic thermodynamics,"
   arXiv:1805.03861; aging-FDT overlap work, cond-mat/9803108), and the Franz–Parisi potential
   `V(q)` is a Landau-type *free energy* of the overlap. Neither is a capacity bound `σ_max(q)`
   that vanishes as `q→1`; the free-energy potential and the σ-sorted-by-q fluctuation relation
   are different objects. No hit for our claim.

### Grade against OUR specific claim (does any hit state capacity-vanishing keyed to a
CORRELATION order parameter with a supply/demand corridor edge?)

| Literature | capacity `σ_max` (max over drives)? | keyed to *correlation* order parameter? | supply/demand corridor edge? | our claim? |
|---|---|---|---|---|
| Jamming yield-stress/soft-mode divergence | cost diverges (∴ capacity vanishes) — yes in spirit | **no** — packing fraction φ / coordination δz | no | genus only |
| Flocking EPR (Agranov–Cates–Fodor) | no — realized steady-state σ | yes (polar order) but **wrong sign** | no | no (and a tension) |
| Kuramoto stochastic-thermo (Chudak–Esposito–Ptaszyński) | no — realized σ | yes (r), **sign parameter-dependent** | no | corroborates the crux, not the law |
| Glass overlap / Franz–Parisi | no — free energy / σ-sorted-by-q | yes (q) but not a capacity | no | no |

**Closest published object:** the jamming yield-stress / soft-mode divergence (Liu–Nagel
lineage) — the canonical, textbook-adjacent form of "you cannot stir a rigidly-clamped system,"
strictly stronger prior art for the *mechanism* than the parent's synchronization-control cite.

**What remains ours (the exact remainder):** the packaging of that mechanism as a *maximum
entropy-production capacity law* `σ_max ∝ (1−ρ)` keyed to the **correlation/copula order
parameter** (not a density, not a contact number), read as the **supply=demand crossing** that
sets the corridor's upper edge. No literature swept keys an entropy-production *capacity* to a
*correlation* order parameter, and none gives the corridor-edge reading. This is thinner than
"a new law" — it is a substrate-independent re-keying of a known rigidity mechanism onto the
copula order parameter — and by rule 2 the re-keying earns nothing until it makes a confirmed
novel prediction (the registered CIRISArray bench collapse curve is that prediction). Two
findings for the program beyond the grade: (i) log the **capacity-vs-realized-σ distinction**
as load-bearing — the flocking result contradicts the *realized-σ* reading, so the claim must
be stated as a capacity ceiling or it is already falsified; (ii) the **N1/N3 normalization
flip is not a defect** — the leading coupled-oscillator stochastic-thermo result finds the same
sign-indeterminacy, so the program's honesty here is the published state of the art.

**Coverage / absence grading (honest):** searched — jamming/rigidity-percolation (yield stress,
soft modes, isostaticity, effective temperature), glass/aging entropy production and
Franz–Parisi overlap, Kuramoto + stochastic thermodynamics σ(r), active-matter/flocking
σ(order). Confidence that the *genus* is published: **high** (dense, canonical hits). Confidence
that the *specific correlation-keyed capacity law with the corridor edge* is unpublished:
**moderate** — I did not sweep the network-control / structural-controllability literature
(controllability Gramians vs. algebraic connectivity) or the maximum-entropy-production
extremal-principle literature, either of which could hold a closer capacity-keyed statement.
Grade **B**, not the clean-novelty C the parent left open.

# Dark-ledger convergent art — the four-pillar prior-art map

**Date 2026-07-10.** Companion to `README.md` (the Ledger Law + dark-ledger thesis), `human_coordination_content.md`
(the carrier-vs-pattern fork), and the earlier prior-art pass `dm_coherence_priorart.md` (Timeflow Gravity,
Berezhiani–Khoury, Gough, Verlinde-as-rotation-curves, Bianconi). This note maps the **sharpened** thesis — now
four distinct pillars — against the published literature. Every work is graded
**NEAR-IDENTICAL / CONVERGENT / ADJACENT / DISTINCT** and given a fate. Bottom line, stated up front and defended
below: **the dark-ledger thesis is not novel as physics. It is a classical shadow of the it-from-qubit program
crossed with Verlinde's "dark matter as an entropy-displacement gap." What is ours is the packaging — one
machine-checked classical functional, the blindness taxonomy, and the audit discipline.**

---

## Executive verdict (the four answers the lead asked for)

**Three closest works.**
1. **Bianconi, *Gravity from entropy* (2024/25), PRD 111, 066001 — NEAR-IDENTICAL** on the load-bearing premise
   "gravity = relative entropy between two metrics/ledgers." The repo cites it *as* its gravity-is-a-ledger
   foundation, so this is parent, not competitor. Fate: live, peer-reviewed; but its G-field is w = −1,
   non-clustering → dark **energy**, not a dark-matter gap. The repo's move (extend the two-metric relative
   entropy to a two-*ledger* DM gap) is the one step beyond Bianconi, and it is exactly the step that is unproven.
2. **Verlinde, *Emergent Gravity and the Dark Universe* (2016), arXiv:1611.02269 — CONVERGENT→NEAR-IDENTICAL** on
   "dark matter **is** a ledger gap, not a substance." His apparent DM is literally an *entropy displacement*: baryons
   displace de Sitter entanglement entropy, the elastic response *is* the extra gravity. This is the closest published
   "DM as inference artifact of an entropy ledger." Fate: **empirically wounded** — passed Brouwer 2016 weak lensing,
   failed the RAR radius residuals (Lelli 2017), failed isolated-dwarf tests (arXiv:1706.00785), strained by Solar
   System bounds (arXiv:2005.05322); no covariant formulation. Not viable as a full theory; still cited as the
   canonical "DM = bookkeeping" proposal.
3. **Cao–Carroll–Michalakis, *Space from Hilbert Space* (2017), PRD 95, 024031 — NEAR-IDENTICAL method** for Pillar 2:
   mutual information → distance → classical multidimensional scaling → emergent geometry obeying a spatial Einstein
   equation. This is the repo's "distance from correlation," done first, in the quantum grain. (Van Raamsdonk 2010 is
   the progenitor and equally close; Zurek's Quantum Darwinism is the equally-close Pillar-3 cousin.)

**Zurek correspondence verdict: CONVERGENT in principle, NOT the same object.** Quantum Darwinism's claim —
*objectivity = information redundantly imprinted in the environment* — is startlingly close to clause 2 ("sourcing
coordination and emitting detectability are one act"). But the *quantities differ*: QD's redundancy R_δ is a **spatial
count** of independent environment fragments each carrying near-complete information about a pointer state; our S/2 is a
**temporal/statistical rate** (the Chernoff–Stein detection exponent per sample). They agree that real coordination
*necessarily leaves readable receipts* — a genuine, citable convergence — but ours is neither a special case of QD nor
vice versa. Crucially, **no one has connected QD redundancy to a gravitating/thermodynamic quantity**; that bridge is
open on both sides, and the repo does not build it either (clause 3 says the pattern does not gravitate).

**Vopson verdict: cite it as the named precedent for the map we already killed, not as support.** Vopson's
mass-energy-information equivalence (AIP Advances 9, 095206, 2019) — each bit carries mass k_B T ln2 / c² — **is** the
repo's dead "map (i)" (ΔM = εS/c² with ε = Landauer). It is **heavily and, on the evidence, correctly criticized**:
Hossenfelder's rebuttal; the low-temperature divergence (mass → ∞ as T → 0); energy-conservation violation under black-
hole evaporation; and null/under-powered experiments. There *is* a defending camp (Vopson's "information catastrophe"
and simulation-hypothesis program, with published responses), so report both sides — but the physics-community weight is
firmly against it, and the repo's own magnitude kill lands independently on the critics' side (~40 orders unnatural).
**Do not lean on Vopson; cite him to show the kill is corroborated.**

**What is actually ours (candid):** likely only (i) the classical *pairwise* formulation of S as one cross-substrate
functional, (ii) the mechanized Lean core, (iii) the retract-with-numbers audit method, and (iv) the **blindness
taxonomy** (means / amplitude / order-≥3 as three *provable* null spaces, reframed as "the null space is the
discovery"). Detail in the dedicated section below. The single element with no clean precedent is (iv) used as an
*instrument* — everyone else mines what the correlation ledger **sees**; no one has built a program around what it
**provably cannot see** and identified that null space with the dark sector.

---

## PILLAR 1 — "Gravity reads a ledger; the dark sector is an inference gap between ledgers"

| Work | Claim | Grade | Fate |
|---|---|---|---|
| **Bianconi, Gravity from entropy** (arXiv:2408.14391, PRD 111 066001) | Gravity = relative entropy between spacetime metric g and the matter-induced metric G; a G-field emerges | **NEAR-IDENTICAL** (the repo's premise) | Live; G-field → dark **energy** (w=−1), not DM |
| **Verlinde, Emergent Gravity & the Dark Universe** (arXiv:1611.02269) | Apparent DM = elastic response to entropy *displacement*; DM is a bookkeeping artifact | **CONVERGENT→NEAR-IDENTICAL** | Wounded: passed Brouwer '16, failed Lelli '17 RAR, dwarfs '17, Solar-System bounds |
| **Jacobson, Thermodynamics of Spacetime** (1995, PRL 75 1260; gr-qc/9504004) | Einstein eq **is** an equation of state; δQ = T dS across local Rindler horizons | **CONVERGENT** (bedrock of "gravity = ledger") | Foundational, undisputed; says nothing about DM |
| **Jacobson, Entanglement Equilibrium** (2015, arXiv:1505.04753) | Einstein eq ⇔ vacuum entanglement entropy is stationary (maximal) | **CONVERGENT** | Live; the strongest form of "gravity reads an entropy ledger" |
| **Padmanabhan, holographic equipartition** (e.g. arXiv:1206.4916 / 1905.03529) | Cosmic expansion = surface−bulk DOF difference; DE = the "information deficit" | **CONVERGENT** (for DE) / **ADJACENT** (for DM) | Live; close cousin of the repo's *dark-energy-from-structure* line |
| **Li, holographic dark energy** (2004, hep-th/0403127) | DE density tied to an IR horizon cutoff via the holographic bound | **ADJACENT** | DE not DM; under DESI+ACT tension (Ricci variant ruled out >10σ, MNRAS stag365) |

**Reading.** "Gravity is a ledger" is *established, mainstream, and not ours*: Jacobson (1995, 2015), Padmanabhan, and
Bianconi own it. The repo inherits Bianconi's two-metric relative-entropy construction wholesale. The one genuinely
distinct move is **"dark matter = the gap between the gravitational ledger and the visible-coordination ledger."**
Verlinde is the closest published instance of *that specific move* (DM as an entropy-displacement gap), and its fate is
the warning: a "DM as ledger artifact" theory that reproduces MOND/Tully–Fisher at galaxy scale still dies on RAR
residuals, dwarfs, and clusters. The repo's own notes already concede the gap is **circular by construction** until
predicted independently from the null space, and the naive εS/c² reading is dead on magnitude (`dm_coherence_priorart.md`).
Pillar 1 is therefore **convergent art with an unbroken bad-luck streak** — every named ancestor that tried "DM = ledger
gap" either fails empirically (Verlinde) or produces DE instead of DM (Bianconi, Padmanabhan, Li).

---

## PILLAR 2 — "Spacetime/geometry FROM correlation structure"

| Work | Claim | Grade | Fate |
|---|---|---|---|
| **Van Raamsdonk, Building up spacetime with entanglement** (2010, arXiv:1005.3035) | Disentangling two regions pulls them apart; entanglement = geometric connectivity | **NEAR-IDENTICAL** (spirit) | Highly cited progenitor; live, central to it-from-qubit |
| **Cao–Carroll–Michalakis, Space from Hilbert Space** (arXiv:1606.08444, PRD 95 024031) | MI → distance → MDS → emergent manifold; entanglement perturbation ⇒ spatial Einstein eq | **NEAR-IDENTICAL** (method) | Live; the exact "distance from correlation" pipeline, quantum grain |
| **Maldacena–Susskind, ER=EPR** (2013, arXiv:1306.0533) | Entanglement (EPR) = geometric bridge (ER wormhole) | **CONVERGENT** | Highly influential conjecture; live |
| **Swingle, MERA/holography** (2012, arXiv:1209.3304) | Tensor-network entanglement structure discretizes an AdS slice (RT-like) | **CONVERGENT** | Live but the exact AdS/MERA match is contested |
| **Emergent distance from MI in 1D chains** (2025, arXiv:2507.09749) | d = −ξ log(I/I₀); metricity/triangle-inequality of MI-distance tested | **CONVERGENT/ADJACENT** | Recent; directly probes whether correlation-distance is a metric |

**Reading, and the classical-shadow question the lead asked.** This is the **heavyweight convergent art** and the honest
mirror of the repo's Pillar 2. "Coordination is what geometry reads" is exactly the it-from-qubit thesis, and CCM already
built the literal pipeline (mutual information → MDS → geometry + Einstein-like curvature response). The repo's S is a
**pairwise, classical, Gaussian functional** (S = −ln det C); the it-from-qubit quantity is **quantum entanglement
entropy / mutual information**. So the precise relationship: **the repo's ledger is the classical (Gaussian) shadow of
the CCM/Van Raamsdonk mutual-information-geometry construction.** For a classical Gaussian state, S = −ln det C *is* twice
the total correlation, and the CCM distance d = −ξ log(I) reduces to a function of the same off-diagonal entries.

**Has anyone written the *classical multi-information* version of Van Raamsdonk?** Not as a named result that I can
find. The MI-geometry papers all use **quantum** MI (CCM, the XXZ chain, anyon-charge geometry arXiv:2512.15256), and the
classical reduction is treated as trivial (you just drop the entanglement and keep the correlations). That is the
candid status: the classical pairwise version is a **gap of neglect, not a gap of ignorance** — nobody wrote it because
it is regarded as the uninteresting shadow of the quantum object, not because it is hard or unknown. The repo's claim to
Pillar 2 is therefore "**we took the shadow seriously and mechanized it**," which is a methodology claim, not a physics
discovery.

---

## PILLAR 3 — "Receipts": objectivity/detectability as redundant environmental records

| Work | Claim | Grade | Fate |
|---|---|---|---|
| **Zurek, Quantum Darwinism** (Nature Physics 5, 181, 2009; earlier PRL) | Objectivity = pointer-state info redundantly imprinted in many environment fragments | **CONVERGENT (principle), DISTINCT (quantity)** | Established, actively developed |
| **Ollivier–Poulin–Zurek, Environment as Witness** (2004, PRL 93 220401) | Only pointer states leave a *redundant* imprint; environment = amplifier, not just sink | **CONVERGENT** | Foundational to QD |
| **Joos–Zeh / decoherence-as-records** | Environmental monitoring continuously records the pointer observable | **ADJACENT** | Standard decoherence theory |
| **QD → gravity / Hawking redundancy** (see Q-Darwinism reviews) | Redundancy in curved spacetime / black-hole analogues largely unexplored | **ADJACENT / OPEN** | Explicitly flagged open in the literature |

**The correspondence, mapped carefully (the lead asked for this).**

- **What matches.** Clause 2 says the act that *sources* coordination is the same act that *emits* detectability — you
  cannot hold coordination and withhold its receipt. Quantum Darwinism says the same for a pointer state: the state
  becomes *objective* precisely by proliferating redundant records, so "exists classically" ⇔ "is redundantly recorded."
  Both are **anti-hidden-variable** in the same spirit: reality/coordination that leaves *no* readable trace is not, on
  either account, doing physical work. This is a real convergence of *principle* and worth citing.

- **Where redundancy R and the Stein rate S/2 diverge (the verdict).** QD's order parameter is **R_δ**, the *number of
  disjoint environment fragments* each of which already carries (1−δ) of the system's information — a **spatial
  multiplicity of independent copies**. The repo's clause-2 quantity is the **Chernoff–Stein exponent S/2**, the *rate
  per sample* at which a single observer's error probability in "coordinated vs independent" decays — a **temporal
  accumulation for one observer**. Loosely, R answers "how many independent witnesses could there be?" and S/2 answers
  "how fast does one witness become certain?" They are dual faces of "detectability," and in a redundancy-limited channel
  they are related (more independent copies ⇒ faster single-observer discrimination), but **they are not the same
  functional and neither derives the other in the general case.** So: **CONVERGENT on the thesis, DISTINCT on the
  formalism.** Our contribution here, if any, is that S/2 is a *substrate-independent* receipt rate provable for
  classical correlation matrices, whereas QD's R is developed in the quantum-measurement setting.

- **Has anyone tied Darwinism-redundancy to a gravitating/thermodynamic quantity?** **Essentially no.** The reviews state
  plainly that QD in curved spacetime is "largely unexplored"; the only gravitational contact is Hawking-radiation
  redundancy in black-hole *analogues*, and that is about information recovery, not about redundancy *sourcing* gravity.
  This is an **open lane** — but the repo does not occupy it either, because clause 3 forbids pattern from gravitating.
  So Pillar 3 is a **clean conceptual convergence with Zurek and a shared open frontier**, not a place the repo has
  planted a flag ahead of the field.

---

## PILLAR 4 — the carrier-vs-pattern fork: does pure correlation gravitate?

| Work | Claim | Grade to the repo's clause-3 orthogonality | Fate |
|---|---|---|---|
| **QNEC / Casini–Huerta–Bousso et al.** (e.g. arXiv:1509.02542; proofs 2016–) | δ²S_EE ≤ 2π⟨T_vv⟩: stress-energy **bounds** the second variation of entanglement entropy | **CONVERGENT — cuts the repo's way** | Proven; rigorous QFT |
| **Binding / interaction energy gravitates** (textbook GR; ADM mass of bound systems) | The *energy cost* of establishing correlation contributes to mass-energy and gravitates | **CONVERGENT — the nuance the repo should adopt** | Undisputed |
| **Vopson, mass-energy-information equivalence** (AIP Adv. 9, 095206, 2019; arXiv:2009.01937) | Each bit has mass ε/c², ε = k_B T ln2 → "information catastrophe," DM candidate | **NEAR-IDENTICAL to the repo's DEAD map (i)** | Heavily criticized; largely rejected |
| **"Landauer-mass" bridges** (e.g. Landauer→Einstein essays; buffered-MI mass proposals) | Mass = thermodynamic cost of erasing structured mutual information | **CONVERGENT (speculative)** | Fringe; unestablished |

**Reading — this pillar is where clause 3 is *correct and defensible*, and the literature backs it.**

- **QNEC vindicates the orthogonality, precisely.** The quantum null energy condition proves that the *variation* of
  entanglement entropy is **bounded by the null stress-energy**, not sourced by the entropy. Read against clause 3: S
  (pattern) is amplitude-blind; T_μν (amplitude) is what gravitates; QNEC says the two are linked *only through the
  energy cost of changing the pattern*, with stress-energy on top. This is the rigorous physics statement of the repo's
  "pattern is gravitationally inert; its energy cost is not." The repo should cite QNEC as the technical backing for the
  orthogonality claim rather than resting it on clause 3 alone.

- **Binding energy is the honest nuance.** The repo's Layer-3 says pattern-qua-pattern does not gravitate. True — but the
  **work done to establish the pattern** (binding energy, interaction energy) *does* contribute to stress-energy and
  gravitates, and this is elementary GR (a bound system weighs less than its free parts; the deficit is real mass-energy).
  So the sharpened statement is: *the pattern carries no stress-energy, but its formation history does, and that history's
  energy is already on the visible ledger whenever the carrier is baryonic.* This is exactly why `human_coordination_content.md`
  gets GAP = 0 — and citing binding-energy GR makes that argument bulletproof rather than posited.

- **Vopson is the cautionary twin.** His principle is the repo's map (i) with the label filed off. Its reception is the
  data point: mathematical-error and thermodynamics critiques (Hossenfelder; "Information Without Substance"), the
  T → 0 mass divergence, energy non-conservation under evaporation, and unpersuasive experiments. The lesson for the
  repo is *not* "Vopson was unlucky" — it is that **any "coordination/information sources mass" reading inherits Vopson's
  problems**, and the repo already independently derived the same death (~40 orders unnatural ε). Cite both Vopson and his
  critics; the convergence of two independent kills is itself evidence the map is dead.

**Pillar-4 verdict:** the carrier-vs-pattern fork is **well-supported by mainstream physics on the side the repo takes**
(QNEC + binding energy ⇒ pattern inert, energy-of-formation gravitates and is baryon-visible). The fork is not novel —
it is the correct reading of established results — but it is the *soundest* pillar precisely because it is convergent
with proven physics rather than betting beyond it.

---

## The ten closest works (ranked by closeness to the sharpened thesis)

| # | Work | Cite | Pillar | Grade |
|---|---|---|---|---|
| 1 | Bianconi, Gravity from entropy | arXiv:2408.14391; PRD 111 066001 | 1 | NEAR-IDENTICAL (premise) |
| 2 | Cao–Carroll–Michalakis, Space from Hilbert Space | arXiv:1606.08444; PRD 95 024031 | 2 | NEAR-IDENTICAL (method) |
| 3 | Van Raamsdonk, Building up spacetime | arXiv:1005.3035; GRG 42 2323 | 2 | NEAR-IDENTICAL (spirit) |
| 4 | Verlinde, Emergent Gravity & the Dark Universe | arXiv:1611.02269 | 1 | CONVERGENT→NEAR-IDENTICAL |
| 5 | Zurek, Quantum Darwinism | Nat. Phys. 5, 181 (2009) | 3 | CONVERGENT (principle) |
| 6 | Ollivier–Poulin–Zurek, Environment as Witness | PRL 93, 220401 (2004) | 3 | CONVERGENT |
| 7 | Jacobson, Entanglement Equilibrium | arXiv:1505.04753 | 1 | CONVERGENT |
| 8 | Vopson, mass-energy-information equivalence | AIP Adv. 9, 095206 (2019) | 4 | NEAR-IDENTICAL (dead map) |
| 9 | QNEC (Bousso–Casini–Fisher–Maldacena; Casini–Huerta) | arXiv:1509.02542 & proofs | 4 | CONVERGENT (backs clause 3) |
| 10 | Padmanabhan, holographic equipartition | arXiv:1206.4916 / 1905.03529 | 1 | CONVERGENT (DE), ADJACENT (DM) |

(Progenitors just off the list: Jacobson 1995 gr-qc/9504004; Maldacena–Susskind ER=EPR 1306.0533; Swingle 1209.3304;
Li holographic DE hep-th/0403127; Watanabe's total correlation, the classical ancestor of S itself.)

---

## What is actually ours (candid)

Stripping everything the literature already owns, the residue is **four items, none of them a physical phenomenon**:

1. **The classical *pairwise* formulation as one cross-substrate functional.** S = −ln det C is textbook: it is twice
   Watanabe's **total correlation / multi-information** for a Gaussian, and log-det-entropy estimation is a known field
   (arXiv:1309.0482). The quantity is not ours. What is arguably ours is *insisting on the classical Gaussian shadow as
   the primary object* and running it identically across molecules, neurons, markets, silicon, and galaxies — the
   it-from-qubit people always reach for the quantum object; we deliberately keep the classical one.

2. **The mechanized core.** 44 theorems, 0 axioms in Lean 4, with CI resolving every claim *through* the proof. No
   convergent-art program (Verlinde, Van Raamsdonk, CCM, Zurek, Bianconi) machine-checks its identities. This is a
   *rigor/reproducibility* contribution, genuinely distinctive in kind, not in physics.

3. **The audit method.** Retract-with-numbers, same-day double retractions, a public ledger of dead claims. A
   methodology, and an unusually honest one, but a methodology.

4. **The blindness taxonomy — the only candidate with no clean precedent.** The claim that a correlation ledger has a
   *provable, structured null space* — mean-blindness, amplitude/copula-blindness (clause 3), order-≥3-blindness (GHZ) —
   and that **this null space, not the ledger's readings, is the object of interest**, mapping "dark = off-ledger" onto
   the physical dark sector. Everyone in Pillars 1–3 mines what a correlation/entropy ledger **sees** (geometry,
   objectivity, gravity). I found **no one** who inverts it — who characterizes what such a ledger *provably cannot see*
   and turns that null space into an instrument (the two-ledger difference). That inversion is the single genuinely novel
   framing.

**The unavoidable caveat.** Item 4 is the novel *element*, but its dark-ledger *application* is, by the repo's own audit,
either circular (the gap is true by construction) or reduces to particle CDM (the carrier-vs-pattern fork). **So the one
thing with no precedent is a method/framing, not a validated result.** The dark-ledger thesis is best described as a
**classical shadow of it-from-qubit, re-instrumented around the null space** — novel in packaging and discipline,
convergent-to-derivative in physics.

---

## Who to cite so no paper re-invents a wheel

- **Any "gravity is a ledger" sentence** → Jacobson 1995 (gr-qc/9504004) + 2015 (1505.04753); Padmanabhan holographic
  equipartition; **Bianconi 2408.14391** as the direct relative-entropy-between-metrics parent.
- **Any "dark matter as bookkeeping/inference gap"** → **Verlinde 1611.02269** (and its empirical obituary: Lelli 2017
  RAR residuals; 1706.00785 dwarfs), so the paper cannot claim priority or ignore why the ancestor failed.
- **Any "geometry/distance from correlation"** → **Van Raamsdonk 1005.3035** + **Cao–Carroll–Michalakis 1606.08444**;
  note ours is the *classical Gaussian shadow* of their quantum MI construction, and cite the MI-metricity work
  (2507.09749).
- **Any "existence = detectability / receipts"** → **Zurek Quantum Darwinism** (Nat. Phys. 5, 181) + **OPZ PRL 93,
  220401**; state explicitly that our S/2 (Stein rate) is *not* their R_δ (redundancy count).
- **Any "coordination/information has mass"** → cite **Vopson AIP Adv. 9, 095206** *and* its critiques (Hossenfelder; the
  T→0 divergence critiques), as the named precedent for the map we killed.
- **Any "pattern does/doesn't gravitate"** → **QNEC** (1509.02542) + textbook binding-energy GR, which back clause 3.
- **The functional S itself** → Watanabe (total correlation) + log-det-entropy (1309.0482): we did not invent the
  quantity, only its cross-substrate deployment.

---

## Bottom line

The dark-ledger thesis is **not novel as physics.** Pillar 1 (gravity-as-ledger, DM-as-gap) is owned by Jacobson,
Padmanabhan, Bianconi, and Verlinde — and every ancestor that tried the DM-gap step either failed empirically or
produced dark energy instead. Pillar 2 (geometry-from-correlation) is the it-from-qubit program; ours is its classical
Gaussian shadow, and the "classical multi-information Van Raamsdonk" is unwritten only because it is regarded as the
trivial shadow. Pillar 3 (receipts) genuinely converges with Quantum Darwinism in *principle* while using a *different*
quantity (Stein rate S/2 ≠ redundancy R_δ), and the Darwinism→gravity bridge is open for everyone, us included. Pillar 4
(carrier-vs-pattern) is the *soundest* pillar precisely because it is **convergent with proven physics** (QNEC + binding
energy), and it correctly kills the "pattern gravitates" reading that Vopson embodies.

**The single element with no clean precedent** is the **blindness taxonomy used as an instrument**: characterizing the
correlation ledger's *provable null space* (mean / amplitude / order-≥3) and identifying it with the dark sector via a
two-ledger difference. That inversion — study what the ledger cannot see, not what it can — is ours. But it is a
*framing*, and its dark-sector payoff is, by the program's own audit, still circular-or-CDM. **Verdict: a classical
shadow of it-from-qubit, re-branded around the null space, distinguished by mechanization and audit discipline rather
than by any new physical claim that survives.**

---

## Sources

- Bianconi, *Gravity from entropy*, PRD 111, 066001 (2025): [arXiv:2408.14391](https://arxiv.org/abs/2408.14391)
- Verlinde, *Emergent Gravity and the Dark Universe* (2016): [arXiv:1611.02269](https://arxiv.org/abs/1611.02269); dwarf test [arXiv:1706.00785](https://arxiv.org/pdf/1706.00785); Solar-System [arXiv:2005.05322](https://arxiv.org/pdf/2005.05322)
- Jacobson, *Thermodynamics of Spacetime*, PRL 75, 1260 (1995): [gr-qc/9504004](https://arxiv.org/abs/gr-qc/9504004)
- Jacobson, *Entanglement Equilibrium and the Einstein Equation* (2015): [arXiv:1505.04753](https://arxiv.org/abs/1505.04753)
- Padmanabhan, holographic equipartition / emergent cosmic space: [arXiv:1905.03529](https://arxiv.org/pdf/1905.03529)
- Li, *A Model of Holographic Dark Energy* (2004): [hep-th/0403127](https://arxiv.org/pdf/hep-th/0403127); DESI+ACT tension [MNRAS stag365](https://academic.oup.com/mnras/article/547/3/stag365/8494946)
- Van Raamsdonk, *Building up spacetime with quantum entanglement*, GRG 42, 2323 (2010): [arXiv:1005.3035](https://arxiv.org/abs/1005.3035)
- Cao, Carroll & Michalakis, *Space from Hilbert Space*, PRD 95, 024031 (2017): [arXiv:1606.08444](https://arxiv.org/abs/1606.08444)
- Maldacena & Susskind, *Cool horizons for entangled black holes* (ER=EPR, 2013): [arXiv:1306.0533](https://arxiv.org/abs/1306.0533)
- Swingle, *Constructing holographic spacetimes using entanglement renormalization* (2012): [arXiv:1209.3304](https://arxiv.org/abs/1209.3304)
- Emergent distance & metricity of mutual information in 1D chains (2025): [arXiv:2507.09749](https://arxiv.org/pdf/2507.09749)
- Zurek, *Quantum Darwinism*, Nature Physics 5, 181 (2009): [nature.com/articles/nphys1202](https://www.nature.com/articles/nphys1202)
- Ollivier, Poulin & Zurek, *Objective Properties from Subjective Quantum States: Environment as a Witness*, PRL 93, 220401 (2004): [journals.aps.org](https://link.aps.org/doi/10.1103/PhysRevLett.93.220401)
- Vopson, *The mass-energy-information equivalence principle*, AIP Advances 9, 095206 (2019): [pubs.aip.org](https://pubs.aip.org/aip/adv/article/9/9/095206/1076232); *Information Catastrophe* [arXiv:2009.01937](https://arxiv.org/pdf/2009.01937); critique [MDPI Information 13, 540](https://www.mdpi.com/2078-2489/13/11/540)
- QNEC — Bousso, Casini, Fisher, Maldacena, *Proof of a Quantum Null Energy Condition*: [arXiv:1509.02542](https://arxiv.org/abs/1509.02542)
- It from Qubit (Simons Collaboration) overview: [simonsfoundation.org/it-from-qubit](https://www.simonsfoundation.org/mathematics-physical-sciences/it-from-qubit/)
- Log-det entropy / total correlation background: [arXiv:1309.0482](https://arxiv.org/pdf/1309.0482); total-correlation sampling [PMC7514253](https://pmc.ncbi.nlm.nih.gov/articles/PMC7514253/)
</content>
</invoke>

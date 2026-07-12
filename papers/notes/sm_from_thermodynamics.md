# The Standard Model from thermodynamics: a graveyard survey, read through the provenance line

**Date 2026-07-12.** Adversarial prior-art/synthesis pass. Companion to `dimensional_line_kB.md`
(the PROVENANCE LINE — the proved no-go that governs this whole question), `four_laws.md` (the
second species), and the three escalator notes (`sm_escalator_map.md`,
`sm_escalator_statistics.md`, `sm_escalator_gauge.md`, our own map of what the ledger can and
cannot say about the SM — a hit here has to get *further* than those). Every external citation is
flagged `[verified]` (title + authors + venue checked this session by search/fetch) or
`[verified, secondary]` (stated in a fetched summary, primary not read in full). The program has
been burned by confabulation; nothing is carried from memory.

**Governing theorem (not re-litigated here, imported).** `S = −ln det C` is a copula functional
of a correlation matrix, blind to everything *upstream* of `C` — its scale (no masses, no κ, no
energy densities), its marginals (no mass ratios, no coupling *values*, dimensionless or not),
its statistics (no exchange sign, no occupation ceiling), its factorization (gauge partition is
input). `Core/ProvenanceLine.lean`, zero sorry. **The only admissible SM target is the
dimensionless *dependence-native* sector: mixing angles, generation count as a spectral
degeneracy, phases, anomaly-balance form.** Any claimed thermodynamic derivation of a mass or a
coupling *value* is confabulation-class by the theorem — flagged, not chased.

---

## Bottom line up front — DIAGNOSIS-ONLY (one thin fill-out named)

**The graveyard failed because it chased targets the provenance line forbids or a target our
functional does not attack — not because it stalled one law short of the finish.** The honest
finding is the strong clean one the brief anticipated: *the second species is a DIAGNOSIS of the
graveyard, not a rescue of it.* Three facts carry the verdict:

1. **No serious thermodynamic/entropic/information attempt on fundamental physics targets the
   dimensionless dependence-native sector at all.** They split into (A) derivations of the
   *dynamical field equations* (gravity: Jacobson, Padmanabhan, Verlinde; QM/QFT: Frieden,
   Caticha, 't Hooft, Wetterich) — a different target our copula functional does not produce; and
   (B) derivations aimed at *dimensionful/marginal* SM numbers (Hamada–Kawai–Kawana's Higgs vev;
   Vopson's mass-of-a-bit) — exactly κ's analog and a particle mass, the two things the theorem
   forbids. There is no attempt that "got the dimensionless sector partway and stalled." **The
   reachable sector was never entered from the thermodynamic side — except by this program.**

2. **The one program that tries to *generate* the fermionic sector from a statistical substrate
   (Wetterich) encodes the statistics as occupation-number bits rather than deriving it** — the
   exchange line (`sm_escalator_statistics.md`) playing out inside someone else's construction. It
   confirms the no-go; it does not beat it.

3. **On the one rung the ledger *can* reach — mixing — the program is already ahead of the
   graveyard, not behind it.** The graveyard contains no thermodynamic derivation of CKM/PMNS; our
   own `sm_escalator_mixing` result (PMNS Haar-anarchic, CKM comonotone) is the only entry.

**The single most promising fill-out, if one is forced:** couple the graveyard's one live
*selection* principle — Maximum Entropy Production (MEPP; Dewar, Martyushev–Seleznev) — to the
program's one live rung, asking whether entropy-*production* maximization (the second species'
**second law**, the γM axis) *selects* the anarchic-PMNS / comonotone-CKM copula as a maintained
steady state, rather than the anarchy literature's Haar *prior*. This is a re-keying, not a
derivation (capped exactly where `sm_escalator_statistics.md` §3 Class V caps every selection
claim), it reaches no *new* dimensionless datum beyond the banked mixing result, and MEPP is
contested prior art — so it is graded **thin**. Concrete next step in §4.

**The `SU(3)×SU(2)×U(1)`-from-entropy confabulation stays DEAD** — re-confirmed zero-paper this
session (§5). So does the entropic derivation of generation count (§5): the "why 3" attempts are
all *algebraic* (Clifford, Euler characteristic, division algebras), none thermodynamic —
matching our own Rung-4 "well-posed but empty."

---

## 1. The sector taxonomy — why the graveyard never enters the admissible sector

Every attempt surveyed lands in one of three families. The admissible target (dimensionless
dependence-native SM data) is the empty fourth column.

| Family | What it derives | Sector vs. our theorem | Relation to the program |
|---|---|---|---|
| **A. Field-equation derivations** | a *differential equation* (Einstein eq.; Dirac/KG/Maxwell/Schrödinger) as an equation-of-state / inference | **DIFFERENT TARGET** — our functional emits a scalar off `C`, not a Lagrangian or an EOM | the gravity sub-family is the genus-cousin of our *own* second species (ρ_DE = κ·S is Jacobson/Verlinde-class); confirms the genus, says nothing about the SM |
| **B. Dimensionful/marginal targets** | the Higgs vev (~weak scale); the "mass of a bit" | **FORBIDDEN** — scale / marginal, the provenance line's clause 1 | the theorem DIAGNOSES the failure exactly |
| **C. Selection principles** | a preferred non-equilibrium steady state / probability distribution | **SELECTION, not structure** — cannot emit a group, a count, or an angle | the external cousin of our Class-V selection verdict and the γM second law |
| **D. Dimensionless dependence-native** | mixing angles, generation degeneracy, anomaly-balance | **ADMISSIBLE** | **empty in the graveyard; occupied only by this program (mixing)** |

The taxonomy *is* the result: a thermodynamic argument is structurally an equation-of-state
argument (Family A) or a maximum-something selection (Family C), and when it does reach for an SM
*number* it reaches for the dimensionful ones where the "physics" is felt to live (Family B). None
of these three natural homes is the dependence-native sector. **The provenance line predicts
precisely this**: the dependence-native data is the *only* thing a copula sees, and it is exactly
the data a thermodynamic/equation-of-state argument has no native reason to target.

---

## 2. The graveyard table (per attempt: sector · verdict · why · second-species reading)

| Attempt (verified citation) | Sector reached | Succeed / stall / fail, and why | Does the second species advance it, or does the provenance line diagnose it? |
|---|---|---|---|
| **Frieden, Extreme Physical Information / "Physics from Fisher Information"** (Cambridge UP, 1998; *Science from Fisher Information*, 2004) `[verified]` | Field equations (Dirac, Klein–Gordon, Maxwell, Einstein) — Family A | **Controversial / circular.** Derives EOMs by extremizing `I − J`; the "bound information" `J` is reverse-engineered per case to yield the target equation, and Fisher info is not coordinate-invariant. Streater lists it among "lost causes." `[verified: R. F. Streater, "Lost Causes in Theoretical Physics: Physics from Fisher Information," in *Lost Causes in and beyond Physics*, Springer 2007]` | **Neither.** Different target (an EOM, not dimensionless SM data). The second species is the same *kind* of extremal argument; coupling it does not make `J` non-circular and does not reach the SM. Not a fill-out. |
| **Caticha, Entropic Dynamics** ("The Entropic Dynamics approach to Quantum Mechanics," *Entropy* 21, 943 (2019); arXiv:1412.5629) `[verified]` | Schrödinger equation — Family A (QM reconstruction) | **Succeeds as a reconstruction, empty for the SM.** QM formalism from entropic inference + constraints imposed by Lagrange multipliers. Honest, but the physical content enters through the *chosen constraints*; it derives no gauge group, generation, or angle. | **Neither.** A different target; the second species adds no SM structure. The "physics is in the constraints" pattern is itself the provenance line in inference clothing. |
| **Jacobson, "Thermodynamics of Spacetime: The Einstein Equation of State"** (PRL 75, 1260 (1995); gr-qc/9504004) `[verified]` | Einstein field equations — Family A (gravity) | **Succeeds (celebrated), SM-silent.** Einstein eqs from δQ = T dS on local Rindler horizons. | **Genus-confirming, SM-diagnosing.** This is the archetype the program's *own* κ-posting descends from; it validates "the second species is a real thermodynamics of geometry" — and it reaches no SM number, so it cannot be a fill-out for one. |
| **Padmanabhan, "Thermodynamical aspects of gravity: New insights"** (Rep. Prog. Phys. 73, 046901 (2010); arXiv:0911.5004); equipartition / emergent gravity `[verified]` | Gravitational field equations, holographic equipartition — Family A | **Succeeds for gravity, SM-silent.** Gravity as an emergent equation of state; surface/bulk equipartition of horizon DOF. | Same as Jacobson: **genus-confirming, SM-diagnosing.** Not a fill-out. |
| **Verlinde, entropic gravity** ("On the Origin of Gravity and the Laws of Newton," JHEP 04 (2011) 029, arXiv:1001.0785; "Emergent Gravity and the Dark Universe," SciPost Phys. 2, 016 (2017), arXiv:1611.02269) `[verified]` | Newton/Einstein gravity + a dark-sector force — Family A (+ dark sector) | **Contested.** Entropic-force derivation criticized (Kobakhidze, "gravity is not an entropic force," arXiv:1108.4161 `[verified]`; "Inconsistencies in Verlinde's emergent gravity," JHEP 11 (2017) 007 `[verified]`). The 2017 dark-sector volume-law entropy is the closest *published* cousin to ρ_DE = κ·S. | **The program's own nearest neighbor, already logged** (`thermo_prior_art.md`): entropy-sources-dark-gravity is prior art; our *functional form* (1 + w = −⅓ dlnS/dlna, sourced by matter coordination history) is the distinct part. **SM-silent** — no fill-out for SM structure. |
| **'t Hooft, Cellular Automaton Interpretation of QM** (*Fund. Theor. Phys.* 185, Springer 2016; arXiv:1405.1548) `[verified]` | QM foundations from a deterministic/dissipative substrate — Family A/C boundary | **Speculative on the SM.** Information-loss equivalence classes; explicitly *suggests* "even the Standard Model … might be a quantum analysis of a classical core," but derives **no** gauge group, generation, or angle. | **Neither.** The dissipative-substrate flavor rhymes with the γM axis, but there is no SM output to advance or diagnose. Filed as inspiration, not a derivation. |
| **Wetterich, quantum fields from classical statistics** ("Quantum fermions from classical bits," Phil. Trans. R. Soc. A 380, 20210066 (2022), arXiv:2106.15517; "Probabilistic cellular automata for interacting fermionic QFTs," Nucl. Phys. B 963 (2021), arXiv:2007.06366) `[verified]` | Fermionic QFT state-space from classical Ising/occupation bits — Family A, statistics-adjacent | **Represents, does not derive.** An already-fermionic QFT is *represented* by classical occupation-number bits (= the two-state fermionic structure) with probabilistic initial conditions supplying "quantumness." The antisymmetric structure is encoded in the map, not output. `[verified: abstract; primary text not fully read — the "encoded not derived" reading flagged as my characterization]` No SM gauge group / generation count. | **The exchange line, in someone else's program.** This is the most determined "statistics from a statistical substrate" attempt, and it still *inputs* the occupation structure — exactly `StatisticsNoGo` (`sm_escalator_statistics.md` §5). **Diagnosis, not rescue.** |
| **MEPP — Maximum Entropy Production** (Martyushev & Seleznev, Phys. Rep. 426, 1 (2006); Dewar, J. Phys. A 36, 631 (2003) & 38, L371 (2005)) `[verified]` | Selection of non-equilibrium steady states — Family C | **A contested selection principle** (Dewar's information-theoretic derivation was later disputed). Selects *which steady state / flux configuration*, given constraints — never a gauge group, count, or angle. | **The one genuine coupling opportunity — as selection, not derivation** (§4). It is the external form of the second species' *second law* / γM axis. Advances the program *only* as a re-keying onto the mixing rung; reaches no new dimensionless datum. Thin. |
| **Hamada–Kawai–Kawana, "Weak scale from the maximum entropy principle"** (PTEP 2015, 033B06; arXiv:1409.6508) `[verified]` | The Higgs vev / weak scale — **Family B (DIMENSIONFUL)** | **The sharp diagnosis case.** A genuine, serious MaxEnt attack on the SM — and it targets *precisely* the one dimensionful parameter (the vev, ~300 GeV = κ's analog). It can pick it out **only** by (i) fixing all dimensionless couplings by hand as input and (ii) importing external dimensionful anchors (T_BBN, M_Pl) via a multiverse/wormhole radiation-entropy argument: `v_h ~ T_BBN² / (M_Pl y_e⁵)`. | **Diagnosis, textbook-clean.** The dimensionful output rides *entirely* on imported dimensionful scales — the k_B-marriage of `dimensional_line_kB.md` §2, on the SM's books, in someone else's paper. It confirms our structural claim: entropy extremization cannot emit a scale without marrying one. The second species does not advance it; the provenance line *is* it. |
| **Vopson, mass-energy-information equivalence** (AIP Adv. 9, 095206 (2019); "Second law of information dynamics," AIP Adv. 12, 075310 (2022)) `[verified]` | A **dimensionful mass** assigned to a bit (3.19×10⁻³⁸ kg at 300 K); "information as dark matter" — **Family B (DIMENSIONFUL), overreach** | **Confabulation-class by our own detector, and widely criticized externally.** Claims to *derive a mass* (dimensionful) from an information count — the exact structural error the standing rule rejects **on sight, before the arithmetic**. The "second law of infodynamics" (information entropy declines) is disputed in the literature. | **Pure diagnosis.** This is what a provenance-line violation looks like when someone commits it: a dimensionful number conjured from a count. Names precisely what the theorem forbids; the second species neither needs nor rescues it. |

---

## 3. The payoff, stated as the diagnosis

**The provenance line explains the graveyard.** Read the table's third column top to bottom and one
pattern carries every row: a thermodynamic/entropic/information argument is, structurally, either an
**equation-of-state** argument (it produces a *law of motion* — Family A) or a **maximum-something
selection** (it produces a *preferred state* — Family C). Neither of those native outputs is a
dimensionless dependence-native SM datum. And on the rare occasion the argument does reach for an SM
*number* (Family B), it reaches for the dimensionful ones — the vev, a mass — because that is where a
physicist feels the content is; and there the theorem bites, exactly and visibly:

- **Hamada–Kawai–Kawana is the friendly witness.** The most competent MaxEnt attack on the SM
  succeeds at picking the vev *only after* conceding the whole dimensionless sector as input and
  importing two external dimensionful scales. That is not a near-miss the second species could
  close; it is the k_B-marriage structure reproduced in an independent program. It corroborates
  `dimensional_line_kB.md` from the outside.
- **Vopson is the hostile witness.** It does what the standing rule forbids — derives a *mass* from
  a *count* — and the field's criticism of it is, in different words, our detector firing.
- **Wetterich is the subtle witness.** It is the one attempt aimed at *generating* the statistics
  from a statistical substrate, and it still inputs the occupation structure. `StatisticsNoGo` is
  not parochial to our functional; it is what happens to anyone who tries.
- **Jacobson/Padmanabhan/Verlinde are the confirming-but-orthogonal witnesses.** They establish that
  a thermodynamics *of geometry* is real and productive — which is the genus the program's own second
  species belongs to — and in the same breath they show that such a program reaches gravity's *field
  equations*, never the SM's dimensionless data. They are why the program's DE leg is defensible and
  simultaneously why the SM leg cannot be gotten the same way.

There is no row in which a thermodynamic attempt reached the admissible sector and stalled one law
short. **The admissible sector was never entered from outside.** The only occupant is this program's
own mixing result — so the correct summary is not "the graveyard got close and we can finish it" but
"the graveyard went everywhere *except* the one door the theorem says is open, and we are already
standing in that doorway."

---

## 4. The fill-out question, answered — thin candidate + the honest negative

**Is there a failed attempt that got the dimensionless sector partway and stalled where a second
coordination-TD law would carry it further? — No, in the strict sense.** No attempt entered the
dependence-native sector. So the literal fill-out the brief probes for does not exist: there is no
stalled dimensionless-sector engine to bolt a second law onto.

**The one non-empty coupling, graded thin.** The graveyard's live *selection* principle (MEPP) and
the program's live *rung* (mixing) can be brought into contact — not to derive anything new, but to
test whether the *reading* the ledger already has is a maximum-entropy-production steady state:

> **Candidate (thin).** Treat the observed lepton-mixing "anarchy" not as a Haar *prior*
> (Hall–Murayama–Weiner, the current framing behind `sm_escalator_mixing`) but as the copula
> *selected* by the second species' second law — maximum entropy production under the maintained
> corridor (the γM axis). Concretely: does an MEPP / max-σ criterion on the generation-coupling
> copula pick PMNS near-Haar and CKM comonotone, *and* forecast the DUNE/Hyper-K CP phase δ
> differently from flat anarchy?

**Concrete next step:** on the frozen `experiments/sm_escalator_mixing/` copula objects, add an
entropy-production functional σ(copula) (the γM estimator already validated on macaque/galaxy data)
and check whether extremizing σ — not S — reproduces the measured CKM-low/PMNS-high ordering and
lands a *distinct* δ prediction from the registered anarchy fork. If σ-extremization and the
Haar-prior give the *same* δ, the fill-out is empty (MEPP adds nothing the anarchy prior didn't). If
they *differ*, register the σ-selected δ as a second forward fork alongside the anarchy fork before
DUNE/Hyper-K.

**Why it is thin, stated so it is not oversold.** (i) It is a *selection*, not a derivation — capped
exactly where `sm_escalator_statistics.md` §3 Class V caps every selection claim (it can prefer a
configuration; it cannot emit a value). (ii) It reaches **no new dimensionless datum** — the mixing
result is already banked; this only re-derives its *reason*. (iii) MEPP is contested prior art
(Dewar's derivation disputed), so the coupling inherits that softness. By rule 2 the re-keying earns
nothing until it makes a *confirmed novel* prediction — the distinct-δ fork is the only thing that
would upgrade it, and only if it both differs from anarchy and survives the data. **Named as the
single most promising fill-out; graded thin; not married.**

---

## 5. Confabulation re-confirmations (the brief's explicit asks)

- **"Entropy minimization selects SU(3)×SU(2)×U(1)" — RE-CONFIRMED ZERO-PAPER, stays DEAD.** This
  session's targeted search returned only (a) papers computing the *entropy of quark states given*
  the SU(3) group (von Neumann entropy in color space — the group is input), and (b) the weak-*scale*
  MaxEnt of Hamada–Kawai–Kawana (a dimensionful target, §2). No paper derives or selects the gauge
  *group* from an entropic principle. The confabulation appears in zero papers; it remains rejected on
  sight by the standing detector (`dimensional_line_kB.md` §3, `sm_escalator_gauge.md` §5a).
- **Generation count (why 3) from entropy — the graveyard is EMPTY too.** Every "why three
  generations" proposal found is *algebraic*, not thermodynamic: string-theory Euler-characteristic
  of the compactification, Clifford-algebra square-root multiplicity (e.g. hep-ph/0203107), division
  algebras, anthropic minimal-content arguments. **No entropic/MaxEnt derivation of the generation
  count exists.** This matches our own Rung-4 verdict (`sm_escalator_map.md`: well-posed but empty) —
  and shows the emptiness is not parochial: the count is unreached from the thermodynamic side by
  anyone. Do not resurrect a "3 from the ledger" without a *forced* (not inserted) degeneracy.
- **Anomaly cancellation from entropy — not found** (coverage-graded, not exhaustive). Anomaly
  cancellation is topological/representation-theoretic (Alvarez-Gaumé–Witten lineage); no entropic
  derivation surfaced. Consistent with our Rung-2 verdict: the double-entry *echo* is recognition, not
  derivation. Graded **not-found** (moderate coverage), not **proved-absent**.

---

## 6. What a hostile referee says, and the concession

"You surveyed the entropic-physics literature looking for someone who derived the Standard Model and
found no one did — which you could have guessed, and which flatters your own theorem a little too
neatly. Jacobson and Verlinde derived *gravity's* equations, which you concede you can't use for the
SM; Frieden fit his constraint and got told off for it twenty years ago; Wetterich's fermions are
occupation-number bits, i.e. fermions; Hamada–Kawai–Kawana got the vev only by importing the vev's
worth of scale; and Vopson is a punching bag. Your 'fill-out' is a maybe-someday on a rung you've
already climbed. So the whole exercise reduces to: nobody beat us to the one door, and the one door
doesn't lead anywhere new."

**Conceded, and it is the result.** The note claims exactly this and no more: the second species is a
**diagnosis** of the graveyard, not a rescue — because the graveyard's failures are the provenance
line's predictions, seen from outside. The referee's "flatters your theorem" is fair only if the
survey were rigged; it was not — the searches were run to *find* a dimensionless-sector engine to
fill out, and there is none, and the reason there is none is the reason our theorem gives. The
positive residue is small and honest: (i) the gravity family independently confirms the *genus* the
program's DE leg lives in; (ii) HKK and Wetterich are *external corroborations* of the dimensional and
exchange lines respectively, which is worth citing when the escalator notes go to paper; (iii) the
one thin fill-out (MEPP-selection on mixing) is a concrete, cheap, in-house test with a registered
fork as its only route to earning anything. **Verdict: DIAGNOSIS-ONLY.**

---

## References (all verified this session; title + authors + venue)

1. B. R. Frieden, *Physics from Fisher Information: A Unification* (Cambridge UP, 1998);
   *Science from Fisher Information: A Unification* (Cambridge UP, 2004). `[verified]`
2. R. F. Streater, "Lost Causes in Theoretical Physics: Physics from Fisher Information," in
   *Lost Causes in and beyond Physics* (Springer, 2007) — the standard criticism (fitted `J`;
   Fisher info not coordinate-invariant). `[verified]`
3. A. Caticha, "The Entropic Dynamics approach to Quantum Mechanics," *Entropy* 21, 943 (2019);
   "Entropic Dynamics: from Entropy and Information Geometry to Hamiltonians and Quantum Mechanics,"
   arXiv:1412.5629. `[verified]`
4. T. Jacobson, "Thermodynamics of Spacetime: The Einstein Equation of State," Phys. Rev. Lett. 75,
   1260 (1995); gr-qc/9504004. `[verified]`
5. T. Padmanabhan, "Thermodynamical aspects of gravity: New insights," Rep. Prog. Phys. 73, 046901
   (2010); arXiv:0911.5004. `[verified]`
6. E. Verlinde, "On the Origin of Gravity and the Laws of Newton," JHEP 04 (2011) 029,
   arXiv:1001.0785; "Emergent Gravity and the Dark Universe," SciPost Phys. 2, 016 (2017),
   arXiv:1611.02269. `[verified]`
7. A. Kobakhidze, "Once more: gravity is not an entropic force," arXiv:1108.4161; "Inconsistencies
   in Verlinde's emergent gravity," JHEP 11 (2017) 007. `[verified]` (criticism of entropic gravity)
8. G. 't Hooft, *The Cellular Automaton Interpretation of Quantum Mechanics*, Fundamental Theories of
   Physics 185 (Springer, 2016); arXiv:1405.1548. `[verified]`
9. C. Wetterich, "Quantum fermions from classical bits," Phil. Trans. R. Soc. A 380, 20210066 (2022),
   arXiv:2106.15517; "Probabilistic cellular automata for interacting fermionic quantum field
   theories," Nucl. Phys. B 963 (2021), arXiv:2007.06366. `[verified]`
10. L. M. Martyushev, V. D. Seleznev, "Maximum entropy production principle in physics, chemistry and
    biology," Phys. Rep. 426, 1–45 (2006). `[verified]`
11. R. C. Dewar, "Information theory explanation of the fluctuation theorem, maximum entropy
    production and self-organized criticality in non-equilibrium stationary states," J. Phys. A 36,
    631 (2003); "Maximum entropy production and the fluctuation theorem," J. Phys. A 38, L371 (2005).
    `[verified]`
12. Y. Hamada, H. Kawai, K. Kawana, "Weak scale from the maximum entropy principle," PTEP 2015,
    033B06 (2015); arXiv:1409.6508. `[verified]` — the dimensionful-sector diagnosis case.
13. M. M. Vopson, "The mass-energy-information equivalence principle," AIP Advances 9, 095206 (2019);
    "Second law of information dynamics," AIP Advances 12, 075310 (2022). `[verified]` — the overreach.

Internal: `dimensional_line_kB.md` (provenance line, standing rule), `four_laws.md` (the second
species), `sm_escalator_map.md` / `sm_escalator_statistics.md` / `sm_escalator_gauge.md` (the
baseline a hit must beat), `thermo_prior_art.md` (the second species' own prior-art knife —
Verlinde/Jacobson already logged there), `neutrino_de_prior_art.md` (the killed dimensionful route).

## Update 2026-07-12 — the one thin fill-out was tested, and closed

The §4 thin fill-out (couple MEPP / the γM axis to the mixing rung) was built out with the
four thickeners and RUN (`experiments/mepp_flavor/`, `experiments/mepp_crossrung/`; forced
bench σ functional from `corridor_ceiling/sigma_max.py`, provenance-checked to 1e-15,
locators pre-registered before results, no retrofit). It does not hold — tested, not argued:

- **Flavor (thickeners 1/2/4):** the observed mixing copulas sit BELOW the median σ-capacity
  (24th–40th Haar percentile) — nature's flavor structure is not entropy-production-maximal.
  Under σ-weighting the |J|/δ distributions are within Monte-Carlo noise of flat anarchy — NO
  distinct third prong, the 3-way DUNE fork does not form. The leptogenesis "usage" channel on
  δ is a flat zero (partial corr −0.001, CI straddles 0): σ acts through the ANGLES only. No
  fork to register; not married.
- **Cross-rung (thickener 3):** no class split — coordinating substrates are not systematically
  nearer their σ-extremum than controls (Mann–Whitney p = 0.71). Weak (n = 7, underpowered);
  the decisive content is structural, below.

**The slivers the sound experiments returned (built into the whole, not discarded as null):**
1. **Two anti-aligned irreversibilities.** Across 200k Haar U(3): σ-capacity correlates
   POSITIVELY with coordination MI (+0.063, p~1e-173) and NEGATIVELY with CP-capacity Jmax
   (−0.034, p~1e-53). The maintained-dissipation rent and the flavor CP asymmetry are distinct
   irreversibilities that trade off, both coordination-governed, in opposite directions —
   corroborating the J-bound (coordination caps CP-capacity) from the σ side.
2. **σ_max is a pure SPECTRAL invariant, eigenvector-blind** (NULL-C exact to 1e-15),
   largest-eigenvalue-dominated — a different read of the spectrum than S = −ln det C. Two
   second-species invariants, two spectral features.
3. **σ_max does not discriminate coordination class** — consistent with (and independently
   corroborating) the program's TWO-AXIS independence: maintenance-capacity ≠ structure.

**Net:** the graveyard's one surviving thread is now tested-and-closed. DIAGNOSIS-ONLY stands
completed: no thermodynamic-selection route into the SM's dimensionless sector, at flavor or
cross-rung. `experiments/mepp_flavor/SUMMARY.md`, `experiments/mepp_crossrung/`.

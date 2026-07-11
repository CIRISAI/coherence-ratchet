# The Standard Model escalator: what a copula functional may legitimately attack

**Date 2026-07-10.** Discovery-mode map (no pre-registration), kills staked per rung.
Companion to `dimensional_line_kB.md` (the coarse filter) and `entropic_matter_sector.md`
(the closed fermion routes). The ledger is `S = −ln det C` on a normalized correlation
matrix: a copula functional, amplitude-blind by theorem (clause 3). It emits only
dimensionless numbers. This note decomposes the SM into what such a functional could in
principle read and orders the readable objects into an escalator, most to least reachable.

The headline is a sharpening of the attack surface, not a new prediction: **dimensionless is
the coarse filter, but it is not sufficient.** The copula strips *marginals* and sees only
*dependence*. So among the SM's dimensionless objects there is a second, finer cut — and it
disqualifies roughly half of the dimensionless sector that `dimensional_line_kB.md` §4 listed
as admissible.

---

## 1. The SM decomposition: 1 dimensionful bridge, ~25 dimensionless, and the second cut

Parameter count (massless-neutrino SM = 19; the count and the "vev is the only dimensionful
parameter" statement verified against the standard reference [1]):

**Dimensionful — the single bridge (`= κ`'s analog on the SM side):**
- The Higgs mass parameter `μ²` (equivalently the vev `v = 246 GeV`). **One number.** Every
  fermion mass is `Yukawa × v`; `Λ_QCD` is generated from the *dimensionless* `g_s` by
  transmutation, and only acquires GeV units by reference to `v` (or any one measured mass).
  This is the k_B marriage of `dimensional_line_kB.md` §2, on the SM's own books.

**Dimensionless (18 in the massless-ν SM; +7 Dirac-ν → 25; +2 Majorana → 27):**
- 3 gauge couplings `g', g, g_s`
- 9 charged-fermion Yukawas (→ mass ratios), + 3 neutrino Yukawas with massive ν
- 1 Higgs quartic `λ`
- 4 CKM (3 angles + 1 phase); + 4 PMNS (3 angles + 1 phase) with massive ν
- 1 `θ_QCD` (strong-CP phase)

The ratio dimensionless : dimensionful is **18 : 1** (or 25 : 1, 27 : 1). This is the shape
`dimensional_line_kB.md` predicted: a counting theory with one bridge constant is the shape
the SM *already has*. So far, folklore-confirming.

**The second cut (this note's contribution).** The copula normalizes each margin to unit
scale — it is invariant under monotone reparametrization of every coordinate (clause 3). That
is *marginal*-blindness, not merely dimensionful-blindness. A dimensionless number that is
fundamentally a **single interaction/coupling strength** — a scale in its own one-dimensional
subspace — is a marginal, and the copula strips it just as it strips `v`. Only **dependence
structure** (how coordinates couple *to each other*, relations *between* bases, degeneracies,
counts) survives into `det C`.

Partition the dimensionless sector by this cut:

| | SM objects | Copula sees it? |
|---|---|---|
| **Marginal-native** (a strength / a scale in one direction) | 3 gauge couplings, 12 Yukawas (→ all mass ratios), `λ` | **NO** — stripped with the marginals |
| **Dependence-native** (a coupling between bases / a count / a phase) | 4 CKM + 4 PMNS mixing, generation count, gauge-group rank/reps, `θ_QCD` (borderline: a phase) | **Possibly** — this is the whole attack surface |

**Consequence, stated plainly and against our own prior note:** `dimensional_line_kB.md` §4
listed "mass ratios" and "dimensionless couplings" as admissible ledger targets. They are
dimensionless, so they pass the coarse filter — but they are **marginal**-native, so they
fail the second cut. A copula functional is blind to them *for the same theorem-reason it is
blind to κ*. The admissible attack surface is smaller than the dimensionless sector: it is the
**dependence-native** sublist. Everything below is ordered inside that sublist.

---

## 2. The escalator (most → least reachable)

### Rung 1 — Mixing angles (CKM / PMNS) — **RUN 2026-07-10: REGISTERED CLAIM HIT** (`experiments/sm_escalator_mixing/`). PMNS Haar-typical in all six functionals (MI pct 37, |J| pct 58); CKM extreme-aligned in all (MI pct 99.98, within 0.10 of a permutation). Label correction: on the functional, Haar = independence = LOW coordination, alignment = HIGH — the quark book is the coordinated one (~87% of the ln3 ceiling), the lepton book near-independent (17%). Forward fork registered: DUNE/Hyper-K δ discriminates anarchy (J stays Haar-typical) vs entanglement-minimization (J suppressed; Thaler–Trifinopoulos arXiv:2410.23343).

**Why it is the top rung.** A mixing matrix is *definitionally* a copula-shaped object: it
is the coupling between two generation bases (up- vs down-type mass eigenstates; charged-lepton
vs neutrino). `|V_ij|²` is a doubly-stochastic matrix — a coupling of two probability vectors,
which is exactly what a copula is. The angles are dimensionless and purely relational (they
survive any rescaling of the individual masses). This is the one place in the SM where the
ledger's native object type and the SM's object type coincide.

**Ledger-side object.** The generation-coupling structure read as a coordination matrix: CKM
as a near-identity coupling (low coordination — the up and down bases are nearly aligned),
PMNS as a near-anarchic coupling (high coordination — the charged-lepton and neutrino bases
are strongly mixed). Under the anarchy hypothesis the PMNS angles are distributed by the
**Haar measure** on the diagonalizing Lie group [2,3] — i.e. maximal, structureless mixing:
the *anti-corridor* limit. CKM sits at the opposite end. So the ledger has a genuine ordering
statement to make: **CKM = low-`S`, near-diagonal; PMNS = high-`S`, near-Haar** — and a
sharper statement if a *corridor location* (`ρ ∈ (0.1, 0.43)`, `k_eff ≤ 10`) can be attached
to either matrix's coordination.

**What a hit looks like.** The coordination `S` of the measured CKM and PMNS couplings orders
CKM-low / PMNS-high *without* tuning, and (the strong form) one of them lands in the corridor
at a location the ledger predicts parameter-free — e.g. PMNS coordination pinned near the Haar
(maximal) value, CKM near the chaos pole.

**The fork that decides well-posedness — and the kill.** There are two readings of where
mixing *comes from*, and only one is inside the functional's reach:
- **Dependence reading (anarchy / Haar [2,3]):** mixing is structureless relational data,
  independent of the mass hierarchy. Copula-native. Ledger CAN see it. Rung is well-posed.
- **Mass-ratio reading (Gatto–Sartori–Tonin: `θ_C ≈ √(m_d/m_s)` [4]):** mixing is a *function
  of mass ratios*. Mass ratios are marginal-native (§1) — the copula is **blind** to them. If
  observed mixing is fundamentally GST-type, the ledger cannot produce the angles, and this
  rung **collapses into the Rung-7 mass-ratio no-go.**

**Kill condition (Rung 1).** The coordination reading of mixing is falsified if either (a) the
measured CKM/PMNS coordination does *not* order CKM-low / PMNS-high, or (b) reproducing the
actual angles demands a tuned mass-ratio input — in which case GST wins, mixing is marginal,
and the rung is dead. Empirically the PMNS/anarchy side is the live half (the CKM hierarchy is
the GST-friendly half), so the honest target is: **can the ledger predict the PMNS coordination
(near-Haar) parameter-free, while conceding CKM to the marginal sector?** That asymmetry —
lepton mixing readable, quark mixing not — is itself a falsifiable, non-obvious claim.

### Rung 2 — Anomaly cancellation as double-entry balance — **LIVE as recognition, NOT as a prediction.**

**The structural echo is real and it is the program's own metaphor.** Anomaly cancellation is
the requirement that certain representation-weighted charge sums vanish (`Tr Y = 0`,
`Tr Y³ = 0`, the mixed gauge-gravitational condition). It is a **balance law on representation
content** — debits equal credits — which is exactly the double-entry language the coordination
ledger uses. And it carries real numerical force: the SM hypercharges are fixed *up to a global
normalization* by anomaly cancellation (with the one-generation two-fold ambiguity resolved by
the mixed gravitational anomaly / a right-handed neutrino / Yukawa-consistency) [5,6,7]. So the
single piece of *numerical* representation data (the rational hypercharges) is an **output of
anomaly cancellation**, not of a coordination readout.

**The honest boundary — do not over-claim.** The ledger does **not** derive anomaly
cancellation. Anomaly cancellation is a consistency requirement of chiral gauge QFT; it lives
in representation theory and the topology of the gauge bundle, not in a correlation spectrum.
What is legitimate is **recognition**: the SM's consistency condition has the same *form* as
the ledger's balance discipline. This is a bridge worth stating *as recognition* — and a trap
if stated as derivation. It posts no number the ledger did not already have to be told.

**Kill / guard.** Any document that says "the ledger derives anomaly cancellation" or "entropy
minimization selects the anomaly-free content" is confabulation-class (cf. the SU(3)×SU(2)×U(1)
confabulation, `entropic_matter_sector.md` §4a) and is rejected on sight. The recognition
survives only as an analogy of *form*.

### Rung 3 — Fermion/boson statistics: DISCRIMINATION banked, SELECTION ill-posed.

**Selection is ill-posed.** Which statistics a field obeys is fixed by the spin-statistics
theorem in relativistic QFT (Lorentz representation + microcausality). It is an *input* to the
correlation functional — you build either a bosonic covariance or a fermionic Majorana
covariance — not an output of it. Asking a copula functional to *derive* Fermi vs Bose is a
category error.

**Discrimination is closed and banked.** The functional has *distinct closed-form signatures*
for the two statistics, already computed (`experiments/fermionic_ledger/search_log.md`):
bosonic `S` diverges at the rigidity pole; fermionic `I_F` is **capped at `ln 2` per collective
mode** by Pauli exclusion; bosonic dimensional collapse removes `k − 1/ρ → ∞` dimensions,
fermionic removes `≤ 1` per mode (both sympy-verified). So the ledger *reads which statistics
it was fed* with a parameter-free, dimensionless signature. That is a genuine result and it is
in the record — but it is discrimination, not selection. Nothing to hit here that is not
already banked.

### Rung 4 — Generation counting (why 3) — **WELL-POSED but EMPTY. Three routes closed.**

**Well-posed in principle:** a generation count is an *integer degeneracy*, and a degeneracy
(repeated eigenvalues) is exactly the kind of thing a spectrum can carry. Unlike a gauge group,
"3" is not the wrong *type* of object for a correlation functional. This is why it is the most
tempting rung and why it has been attacked most.

**Empty in fact — the honest verdict.** Every concrete mechanism that could force the threefold
degeneracy from coordination structure has been closed:
- **Kähler–Dirac multiplicity → generations** — DEAD. GfE's matter field is *bosonic* (no
  species index); the "1 KD field = 4 Dirac" theorem is about a *fermionic* object the theory
  does not contain, and 4 ≠ 3 anyway (LEP). (`entropic_matter_sector.md` Q2, Candidate A.)
- **Internal form-sector death 4→3** — DEAD, three independent ways: form grading is transverse
  to species grading (top-form truncation smears across all four species → modified spectrum,
  not a count); the entropic functional is flavor-symmetric (cannot select an asymmetric 4→3
  without an *imported* breaking term); the field is bosonic. (`entropic_matter_sector.md` Q6,
  Candidate A′.)
- **Anomaly / 't Hooft multiplicity** — WRONG DIRECTION. The mod-2 anomaly counts multiplicity
  *up* in even steps (→ 8, 16), never down to 3. (`entropic_matter_sector.md` Q2 table.)

**Data check, negative and on record:** the "3-2-1 degeneracy pattern" was checked against our
own data and **does not exist** there. Do not resurrect it.

**Revival condition (what would have to be true, none of it currently in hand):** a
*forced* — not inserted, not imported — threefold degeneracy in the coordination spectrum,
produced by the dynamics rather than seeded into a hand-chosen block structure. Absent that,
Rung 4 is well-posed-but-empty. **Kill:** any "3 from the ledger" that inspection shows put a
threefold block into the correlation matrix by hand is assuming the conclusion — rejected.

### Rung 5 — Representation content (why these reps) — **ILL-POSED as readout; numeric residue is Rung 2's.**

A correlation functional outputs a scalar (or an eigenvalue spectrum); it does not output
representation-theoretic assignments (which SU(3)×SU(2)×U(1) rep each fermion sits in). Reading
"`Q ~ (3,2,+1/6)`" out of `det C` would require hand-inserting exactly that block/charge
structure — the assuming-the-conclusion trap. **Ill-posed.** The only *numerical* content of
the rep assignments is the hypercharges, and those are fixed by **anomaly cancellation**
(Rung 2 [5,6,7]), not by coordination. Nothing here is a ledger target.

### Rung 6 — Gauge group structure (why SU(3)×SU(2)×U(1)) — **ILL-POSED; two sub-routes closed.**

A gauge group is a continuous Lie group; recovering its rank, simple factors and dimensions
from a PSD matrix's spectrum requires putting the block structure in by hand. **Ill-posed for
a bare correlation functional.** Two attempted routes are already closed:
- "Entropy minimization selects SU(3)×SU(2)×U(1)" — **verified confabulation**, appears in zero
  papers (`entropic_matter_sector.md` §4a). Do not resurrect.
- The "3-2-1 degeneracy pattern" in our data — **verified absent** (Rung 4). Do not resurrect.

The only non-ill-posed escape is *outside* this functional: a gauge group as the automorphism
/ symmetry group of a coordination structure that was *itself* forced. That is a
"symmetry-of-the-substrate" question about a different object, not a `det C` readout, and this
program has no such forced substrate. Recorded as a no-go for the functional; flagged as not
even the right tool.

### Rung 7 — Mass ratios — **CLOSED by the second cut (marginal-blind), despite being dimensionless.**

Mass ratios (`m_μ/m_e`, `m_t/m_u`, …) are dimensionless, so `dimensional_line_kB.md` §4 listed
them admissible. **They are not.** They are ratios of Yukawa singular values — *marginal*-sector
objects (each mass is a strength in one flavor direction). The copula strips exactly the marginal
scales (§1). So the functional is blind to mass ratios *by the same clause-3 theorem* that makes
it blind to κ. A claimed mass-ratio derivation from the ledger alone is a structural error under
the standing rule, **and this note extends the rule**: the forbidden set is not only dimensionful
quantities but *dimensionless marginal-ratios* too.

**One admissible indirect route:** a mass-ratio *relation* could appear as a *consequence* of a
Rung-1 mixing prediction (GST ties `θ_C` to `√(m_d/m_s)` [4]) — i.e. if the ledger predicts a
mixing structure, a mass-ratio relation falls out as dependence-structure, not as a marginal
readout. Direct sourcing of a mass ratio from `S`: rejected on sight.

### Rung 8 (bottom) — Dimensionless coupling values — **ILL-POSED / blind (marginal + running).**

Each gauge coupling and the quartic `λ` is a single interaction *strength* — marginal-native,
stripped by the copula (§1). Worse, couplings **run**: "the value" is not one number without a
reference scale, which smuggles a dimensionful anchor back in. The one structural residue is the
GUT hypercharge normalization ratio (the `5/3` of SU(5)/SO(10)) and the `α1:α2:α3` unification
pattern — but that is *representation-theory* output (embedding + running), not a coordination
readout. `θ_QCD` is a phase (dependence-ish) but its value/smallness is the strong-CP problem,
addressed by axions, not coordination — not a natural ledger target. Bottom of the escalator.

---

## 3. Ledger of verdicts

| Rung | Object | Well-posed for a copula functional? | Status |
|---|---|---|---|
| 1 | Mixing angles (CKM/PMNS) | **Yes** (dependence-native) | **LIVE — top target** (fork: anarchy=readable, GST=blind) |
| 2 | Anomaly cancellation | As *recognition* only | **LIVE as recognition**, not prediction (double-entry echo) |
| 3 | Statistics selection / discrimination | Selection **no**; discrimination yes | Selection ill-posed; discrimination **closed & banked** |
| 4 | Generation count (3) | Yes (a count is spectral) | **Well-posed but empty** — 3 routes closed, data-negative |
| 5 | Representation content | **No** (needs hand-inserted blocks) | Ill-posed; numeric residue = hypercharges via Rung 2 |
| 6 | Gauge group | **No** | Ill-posed; 2 sub-routes closed (confabulation + absent pattern) |
| 7 | Mass ratios | **No** (marginal-native, blind) | **Closed by the second cut** — indirect via Rung 1 only |
| 8 | Coupling values | **No** (marginal + running) | Ill-posed / blind |

---

## 4. The single most promising rung and its kill

**Mixing angles (Rung 1), lepton sector.** It is the only SM object whose native type
(a coupling between two bases, `|V|²` doubly-stochastic) *is* the functional's native type (a
copula), it is manifestly dimensionless and marginal-free, and the physics literature already
frames neutrino mixing as **Haar-random / maximal coordination** [2,3] — the ledger's own
anti-corridor limit, computable without a mass input.

**Concrete kill:** compute the coordination `S` (or corridor position `ρ`, `k_eff`) of the
measured PMNS and CKM couplings. The reading is *falsified* if (a) they do not order CKM-low /
PMNS-high, or (b) reproducing the observed angles requires a tuned mass-ratio input (GST [4]
wins → mixing is marginal → Rung 1 collapses into the Rung-7 no-go). The reading *survives —
and becomes a real, non-obvious prediction* — only if the PMNS coordination is pinned near its
Haar/maximal value parameter-free while quark mixing is conceded to the marginal sector. That
asymmetry (leptons readable, quarks not) is the falsifiable claim to register before computing.

## 5. Standing additions this note makes

1. **The second cut.** Dimensionless is necessary, not sufficient. The copula strips marginals;
   the admissible attack surface is the *dependence-native* sublist, not the whole dimensionless
   sector. Mass ratios and coupling values are dimensionless but marginal-native, hence blind —
   the standing rule of `dimensional_line_kB.md` §3 extends to them.
2. **Recognition ≠ derivation (anomaly cancellation).** The double-entry echo is a legitimate
   *recognition* and a confabulation-trap if promoted to *derivation*. Kept at recognition weight.
3. **The over-attacked rung is generation count.** It is well-posed but empty; three routes are
   closed and the data check is negative. Do not re-open without a *forced* (not inserted)
   threefold degeneracy.

---

## References (all verified this session; title + venue checked)

[1] *Mathematical formulation of the Standard Model*, Wikipedia — 19-parameter count (massless
ν; +7 → 26 with Dirac neutrinos); the Higgs vev is the sole dimensionful parameter.
`[verified]`
[2] L. Hall, H. Murayama, N. Weiner, *Neutrino Mass Anarchy*, Phys. Rev. Lett. 84 (2000) 2572,
hep-ph/9911341. `[verified]`
[3] N. Haba, H. Murayama, *Anarchy and Hierarchy*, Phys. Rev. D 63 (2001) 053010 — PMNS angles
distributed by the Haar measure of the diagonalizing group. `[verified]`
[4] R. Gatto, G. Sartori, M. Tonin, *Weak Selfmasses, Cabibbo Angle, and Broken SU(2)×SU(2)*,
Phys. Lett. 28B (1968) 128 — the GST relation `θ_C ≈ √(m_d/m_s)`. `[verified]`
[5] *Comment on anomaly cancellation in the standard model*, Phys. Rev. D 41 (1990) 715 —
anomaly conditions constrain SM hypercharges. `[verified]`
[6] C. Q. Geng / secondary (hep-ph/9710396, *On Charge Quantization and Abelian Gauge*) and
hep-ph/9304312 (*A Note on Charge Quantization Through Anomaly Cancellation*) — hypercharges
fixed up to global normalization; one-generation two-fold ambiguity resolved by the mixed
gravitational anomaly / RH neutrino / Yukawa consistency. `[verified: arXiv listings]`
[7] N. Lohitsiri, *Anomalies and the Standard Model of Particle Physics* (Cambridge thesis) —
review of anomaly cancellation fixing hypercharge assignments. `[verified: repository listing]`

Internal: `dimensional_line_kB.md` (coarse filter, standing rule), `entropic_matter_sector.md`
(Rungs 4/5/6 closures, confabulation debunk), `experiments/fermionic_ledger/search_log.md`
(Rung 3 discrimination, closed-form bosonic/fermionic split).

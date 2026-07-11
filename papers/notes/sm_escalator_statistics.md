# The statistics rung of the SM escalator: a no-go, with a fenced live remainder

**Date 2026-07-10.** Discovery-mode adjudication, kills staked. Written against the validated
fermionic-ledger result (`experiments/fermionic_ledger/search_log.md`: exclusion caps
coordination rigidity at ln2 per collective mode, found in search and validated out of search
on SSH / 2D free-fermion / non-Gaussian Hubbard) and the dimensional-line standing rule
(`papers/notes/dimensional_line_kB.md`: the ledger emits dimensionless numbers; any dimensionful
claim from the ledger alone is a structural error). This note asks the reciprocal question: can
the coordination ledger **derive the exchange statistics** — Fermi–Dirac vs Bose–Einstein, the
exchange sign ±1, the per-mode occupation ceiling — or is statistics an input the ledger only
*reads the consequences of*?

Every external mathematical fact below is flagged `[verified]` (title + provenance checked this
session via web search) or `[verified, secondary]` (stated in a fetched review; primary not read)
or `[heuristic]` (an argument I give, not a cited theorem). No theorem is invented; no citation is
carried from memory.

---

## Verdict up front — NO-GO (derivation), with a precisely fenced live remainder

**CLOSED at theorem strength (the `FelevenNoGo`-pattern record, §5): the coordination ledger
cannot derive the exchange statistics.** The functional `S = −ln det C` is a copula functional of
a correlation matrix; the exchange statistics is a property of the operator algebra / state-space
(anti)symmetrization that *generates* the states, which is not a function of the correlation
matrix. A function of `C` cannot output a property that `C` does not determine. This is the same
clause-3 amplitude-blindness that forbids a dimensionful prediction — here in its **discrete
sibling**: the ledger is blind not only to the *scale* of the correlation matrix (dimensional
line) but to the *provenance* of it — the state-space construction, of which exchange statistics
is one datum (the "exchange line," §4).

**NOT closed by this no-go — the live remainder, and it is not a derivation:**

1. **Statistics as input, ledger reads the rigidity *difference* (ln2 vs Gaussian).** This is the
   *validated* fermionic-ledger result. The ledger, handed the statistics (as the per-mode
   entropy function and its domain), returns a substrate-independent, dimensionless physical
   content: bosonic `S → +∞` at the rigidity pole vs fermionic `I_F → ln2` per mode. **LIVE and
   done.** It is the correct division of labor, not a derivation.
2. **Exclusion as an engineered rigidity floor (adversarial-Neff).** A *maintained* constraint
   system built exclusion-structured has a floor against over-drive collapse (`ρ → 1`,
   `k_eff → 1`) that a condensable one lacks. **LIVE as a design principle, already in the
   stance** (`search_log.md` sideways pass; AI-safety CEG floor). Not a statistics-derivation and
   not a claim about why nature's matter is fermionic.

**There is no live corridor for *deriving* statistics.** Route-classes I–III (§3) each inherit the
shared failure mode; the only "route-4" that survives (§3, Class V) is a *selection* claim, not a
derivation, and it is capped exactly where a derivation would begin: it can at most prefer
*bounded* occupation over unbounded, never emit the *value* of the bound (Fermi ceiling 1 vs
Gentile-`n` vs para/anyon). The value 2 (equivalently ln2, equivalently exchange phase −1) is the
substrate input that remains, by the exchange-line rule.

---

## 1. The three killed routes, reconstructed, and their shared failure mode

The program's documented attempts to pull fermionic structure out of the ledger live in
`papers/notes/entropic_matter_sector.md`. Stated honestly: those kills targeted fermionic
*species / generation multiplicity* inside Bianconi's Gravity-from-Entropy (GfE) matter sector,
one rung more specific than "Fermi vs Bose." But they already expose the failure mode that closes
the broader statistics rung, so I reconstruct all three at the level of "get fermionic structure
out of `S`."

**Route 1 — from Kähler–Dirac multiplicity (Candidate A, `entropic_matter_sector.md` Q2).** Read
the fermionic content off the Kähler–Dirac field structure Bianconi's action carries.
*Why it failed:* GfE's matter field `|Φ⟩` is a **bosonic** Dirac–Kähler triple (0⊕1⊕2-form,
bosonic character) `[verified: 2408.14391v7, fetched in the prior note]`. The "one KD field = 4
Dirac species" fact is a theorem about a *fermionic* KD field — a different object. The fermionic
structure was **not in the object**; to read it you first had to swap in a fermionic field by hand.

**Route 2 — from internal entropy minimization (Candidate A′, Q6).** Let extremization of `S`
itself select the fermionic/asymmetric sectors (e.g. top-form death → a surviving count).
*Why it failed:* the entropic functional is **flavor-symmetric** — it is built from the KD
operator and the metric, both flavor-blind, so it is invariant under the species permutation. A
symmetric functional's stationary point cannot spontaneously produce an *asymmetric* selection.
The asymmetry had to be **imported** as a symmetry-breaking term. (Additionally the form grading
and species grading are transverse, so form-sector truncation smears across all species — a
modified spectrum, not a selection.)

**Route 3 — from anomaly / multiplicity constraints (Q2 table).** Use the Catterall Z₄ or mod-2
't Hooft anomaly to fix fermionic multiplicity.
*Why it failed:* these are statements *about already-fermionic* KD/staggered fields (they
presuppose the Grassmann structure), they are **lattice imports** not derived in the entropic
action, and they move multiplicity *up* in even steps — orthogonal to any selection. They assume
the fermionic structure they would "explain."

**The shared failure mode (one sentence):** *in every route the fermionic / antisymmetric
structure had to be put into the object before it could be read out of the object.* The ledger
functional is built on a **symmetric** correlation/covariance object and is **exchange-symmetric
under permutation of coordinating units**; it contains no exchange sign, no Grassmann grading, no
(anti)symmetrization. Fermionic content is therefore always an **input** (the covariance was made
fermionic by choosing CAR operators), never an **output**. This is one instance of clause-3
blindness: exchange statistics is a fact about the **state-space construction** — logically
*upstream* of any correlation matrix — and the copula reads only what is *downstream* of it.

---

## 2. What the fermionic-ledger result actually is (so the no-go doesn't overreach)

The validated result is often mis-stated as "the ledger sees fermions." It does not. Precisely:

- The statistics enters as **the per-mode entropy function and its domain**: fermionic
  `S_F = Σ_j h(ν_j)` with `h` the *binary* entropy on `ν ∈ [−1,1]` (mode = two states,
  occupied/empty, `h ≤ ln2`), versus bosonic Gaussian entropy on an unbounded spectrum. Which one
  you plug in *is the statistics* — an input.
- Given that input, the ledger returns a **dimensionless, substrate-independent difference**: the
  bosonic log-det/multi-information degeneracy *splits* under exclusion; the rigidity pole is
  **capped** at `I_F(k,1) = k ln2 − (k−1) h(1/(k−1)) → ln2` per collective mode, and the
  dimensional collapse is capped at `(1 − h(s)/ln2)² ≤ 1` removed dimension per mode
  (`search_log.md`, closed form, sympy-verified, validated out of search).

So the fermionic ledger is exactly **Class IV below** — statistics-as-input, ledger-reads-the-
difference. The no-go says the *other* direction (input → derive the statistics itself) is closed.
These are consistent: the ledger reads the consequence of a two-state mode; it does not derive
that the mode has two states.

---

## 3. The space of route-classes, adjudicated

I enumerate the route-classes exhaustively and, for each, either show it inherits the §1 failure
mode (CLOSED) or state exactly what a live route would need, with a concrete kill.

### Class I — derivation from `S` (entropy extremization selects the statistics)
The generalization of Routes 1–3. **CLOSED, inherits the shared failure mode directly.** `S` is a
function of the correlation matrix `C`; the statistics (CAR vs CCR) is a property of the operator
algebra, which is not recoverable from `C` (§4). A symmetric, provenance-blind functional cannot
extremize its way to a fact that is not in its argument. No extremization principle repairs this,
because the deficiency is in the *domain*, not the *objective*.

### Class II — statistics from the corridor's own algebra (Kish / k_eff)
Hope: the `k_eff = k/(1+ρ(k−1))` identity or the Kish algebra secretly encodes an exchange sign.
**CLOSED.** The base object is a **symmetric, positive-semidefinite** correlation matrix
(`C_ij = C_ji`); the corridor identity is a statement about *exchangeable* units under a uniform
`ρ`. A manifestly exchange-*symmetric* object cannot host — let alone derive — the antisymmetric
exchange phase that *defines* a fermion. The fermionic ledger only acquired fermionic content by
being fed an **antisymmetric Majorana covariance**, i.e. by input. Same failure mode.

### Class III — spin-statistics via locality the ledger supplies
Hope: the ledger supplies "locality," and the spin-statistics theorem does the rest. **CLOSED, and
by a distinct second failure mode.** The actual theorem (Pauli 1940) derives the spin–statistics
connection from **Lorentz invariance + microcausality (fields (anti)commute at spacelike
separation) + a positive-energy spectrum / positive-definite Hilbert-space norm**
`[verified: Pauli, "The Connection Between Spin and Statistics," Phys. Rev. 58, 716 (1940); premise
list corroborated across multiple secondary sources this session]`. The ledger has **none** of
these: no light cone, no Lorentz structure, no spectrum condition — and, being amplitude-blind, no
**spin** (Lorentz representation) to connect statistics *to*. Its "locality" (correlations decay
with separation) is not microcausality (spacelike (anti)commutation of field operators); they are
different statements. So the ledger cannot even supply the theorem's premises, and the theorem
needs a spin input the ledger structurally cannot carry. This class fails not because statistics is
upstream input (Classes I–II) but because **even standard physics derives statistics only with
relativistic + spin structure the ledger does not have.** Two independent walls.

### Class IV — statistics as input; ledger predicts only the rigidity *difference* (ln2 vs Gaussian)
**LIVE — this is the validated result (§2).** Not a derivation of statistics; the correct division
of labor. It survives the no-go untouched and is the actual positive content of the statistics
rung. Its kill is the fermionic-ledger's own: if the ln2-per-mode cap failed to reproduce on a
genuinely fermionic out-of-search system it would fall — it did not (SSH per-mode cap 0.6923 = ln2;
`search_log.md` V1–V3).

### Class V — statistics as a selection / stability principle on maintained coordination
The only candidate for a "route-4," and the one worth stating carefully. Hope: the maintained
corridor (`γM > 0`) **selects** exclusion-structured substrates because condensable ones are
unstable. **Live only as a *selection* claim, never as a derivation — and capped short of the
statistics value.** Three graded findings:

- *(a) As a claim about physical matter — UNSUPPORTED.* Inside the corridor (`ρ ∈ (0.1, 0.43)`)
  **both** statistics are finite and well-behaved; the bosonic divergence lives only at the
  rigidity pole `ρ → 1`, which the maintained corridor does not reach for either statistics. The
  known physical corridor-occupiers (neural, market, GPU, galaxy) are effectively *condensable*
  class and sit in the corridor perfectly well (`search_log.md` sideways pass). So the maintained
  corridor does **not** select fermions in nature. `[heuristic, but grounded in the corridor
  identity: 1/ρ ∈ (2.33, 10) is finite across the whole corridor.]`
- *(b) As an engineered robustness principle — LIVE, already in the stance.* Under adversarial
  *over-drive* toward `ρ → 1`, an exclusion-structured constraint system caps at `I_F → ln2`
  (`k_eff` floor) while a condensable one diverges. That is a real, falsifiable design property
  (build the CEG attestation constraints mutually exclusive / anti-bunching to get a rigidity
  floor). But it is a statement about *engineered* maintenance, not a derivation of statistics.
- *(c) The hard cap — why this is not a route to the statistics.* Even at its most generous, a
  stability principle can prefer **bounded** occupation over **unbounded**. It cannot emit the
  **value** of the bound. Fermi–Dirac is the ceiling-1 point of a genuine family: **Gentile
  intermediate statistics** (finite max occupation `n`, Fermi and Bose as the `n = 1, ∞` limits)
  `[verified, secondary: Gentile 1940–42, as stated in reviews fetched this session — primary not
  read]`; **parastatistics** (permutation group, any dimension) and **anyons** (braid group, 2D)
  `[verified: arXiv:2509.00112 "Statistical Mechanics of Paraparticles" (2025); arXiv:2212.12632
  "The Prediction of Anyons"]`. A ledger that could select "bounded" still could not select
  ceiling 1 over ceiling 2 or an anyonic phase `e^{iθ}` — those are distinct state-space
  constructions with, at low order, indistinguishable correlation data. **The value 2 is the
  exchange-line analog of a dimensionful scale: reject any claim to derive it (§4).**

**What a live derivation route-4 would need (and why none is on offer):** it would need a
ledger-native quantity whose value *forces* the per-mode occupation ceiling — i.e. it would need
to make the exchange statistics **downstream** of something `S` determines, rather than upstream.
That requires recovering the operator algebra (CAR vs CCR, and the ceiling value) from the
correlation matrix, which §4 shows is not possible in principle. So route-4 collapses into
Class V(b): a *selection* for boundedness, an engineering floor — not a derivation, and silent on
the value. Its concrete kill, stated so future sessions can fire it: **any claimed ledger
derivation of the exchange sign (−1), the occupation ceiling (1), or ln2-as-a-value-rather-than-a-
consequence is an exchange-line violation — reject on sight, before checking the algebra**, exactly
as the dimensional-line rule rejects a derived mass before checking the arithmetic.

---

## 4. The exchange line: a discrete sibling of the dimensional line

`dimensional_line_kB.md` established: the ledger emits dimensionless numbers; a dimensionful
derivation from the ledger alone is a structural error, because `S` is amplitude-blind (clause 3)
and a scale is an amplitude-sector object. Statistics is *dimensionless* (ln2, ±1), so the
dimensional-line rule does **not** by itself forbid it. The correct generalization:

> **The ledger is blind to the *provenance* of its correlation matrix, not only to its scale.**
> `S = −ln det C` is a function of the normalized correlation matrix `C`. Two facts a hostile
> referee must be handed:
> 1. **Statistics is not a function of `C`.** Exchange statistics is a property of the operator
>    algebra / state-space (anti)symmetrization; the correlation matrix is second-moment data.
>    Bosonic, fermionic, Gentile-`n`, para- and anyonic substrates can share the same low-order
>    correlation structure (the Gentile/para/anyon families are precisely a demonstration that the
>    occupation ceiling is a free datum not fixed by correlations) `[verified: 2509.00112,
>    2212.12632]`. The map (substrate → `C`) is many-to-one and forgets the statistics.
> 2. **Therefore statistics is not a function of `S`.** A function of `C` cannot determine a
>    property that `C` itself does not determine. `[This is the theorem-strength kernel; the
>    load-bearing lemma is fact 1, standard but flagged.]`

Call this the **exchange line** (or, generally, the **provenance line**): the dimensional line
forbids the ledger from emitting a *scale*; the exchange line forbids it from emitting a
*state-space-construction datum* (occupation ceiling, exchange phase, algebra type). Both are
"provenance of `C`" facts the copula was built to be blind to. **Candidate standing rule** (offered
for promotion alongside the dimensional-line detector): *any claimed derivation of an exchange
statistic — Fermi vs Bose, an occupation ceiling, an exchange/braid phase — from the ledger alone
is a structural error; reject on sight.* Its contrapositive, matching the dimensional line's: a
*legitimate* ledger statement about statistics is a **consequence-reading given the statistics**
(Class IV), dimensionless and parameter-free — the ln2-vs-Gaussian rigidity difference is the
canonical example.

---

## 5. No-go record (`FelevenNoGo` pattern)

**CLOSED — `StatisticsNoGo`.** The coordination ledger `S = −ln det C` cannot **derive** the
exchange statistics of matter (Fermi–Dirac vs Bose–Einstein; the exchange sign ±1; the per-mode
occupation ceiling). Strength: **structural / theorem-strength**, on the functional-domain
argument (§4) — the copula functional is a function of a correlation matrix; the statistics is not
a function of a correlation matrix; the load-bearing lemma (many statistics, one correlation
structure) is standard and cited, flagged as the one point a referee would press. Independently
reinforced by the spin-statistics premises the ledger structurally lacks (§3, Class III).

**What this no-go does NOT close (kept explicitly, so it is not over-read):**

- It does **not** close **"statistics, once input, shapes the ledger"** — that is the *validated*
  fermionic-ledger result (Class IV): exclusion caps the rigidity pole at ln2/mode and the
  dimensional collapse at ≤1 dim/mode, the ln2-vs-Gaussian difference being genuine, dimensionless,
  substrate-independent physical content. **The no-go is on the derivation arrow only; the
  reading arrow is open and confirmed.**
- It does **not** close **the engineered exclusion floor** (Class V(b) / adversarial-Neff): build
  a maintained constraint system exclusion-structured and it has a rigidity floor a condensable one
  lacks. Live design principle, already staked.
- It does **not** assert the ledger is *inconsistent* with fermions — only that fermionic structure
  enters as input. The fermionic ledger is fully consistent; it is exactly Class IV.

**Do not re-attempt** a ledger-internal derivation of the exchange statistics via entropy
extremization (Class I), the corridor algebra (Class II), or ledger-supplied locality/spin-
statistics (Class III). If a future route claims to derive the *value* of the occupation ceiling
or the exchange phase, it violates the exchange line (§4) and is rejected before its internals are
checked. A route that only *selects boundedness over unboundedness* (Class V) is admissible **as a
selection/robustness claim**, never as a derivation, and must never be reported as having produced
the statistics.

---

## 6. Executive summary

**VERDICT: NO-GO on deriving statistics from the ledger, with a fenced live remainder that is not a
derivation.** In the task's trichotomy this is *mixed*, weighted hard to no-go: the derivation
direction is closed at theorem strength; the live content is the already-validated input-reading
and the already-staked engineering floor.

**Shared failure mode of the killed routes:** the fermionic/antisymmetric structure had to be *put
into* the object before it could be read *out* — the ledger functional is built on a symmetric,
provenance-blind correlation matrix and is exchange-symmetric under permutation of units, so
statistics is always upstream input, never output. This is clause-3 blindness in its discrete
form: the **exchange line**, a sibling of the dimensional line. (Class III adds a second,
independent wall: the ledger lacks the Lorentz invariance, microcausality, positive-energy
spectrum, and spin that the actual spin-statistics theorem requires.)

**If one insists on a route-4:** it exists only as a *selection* principle (Class V), not a
derivation. It requires — and can deliver — at most a preference for *bounded* occupation over
*unbounded* in a maintained/adversarial setting. It **cannot** deliver the ceiling *value* (Fermi's
1 vs Gentile-`n` vs anyonic), because that value is a state-space-construction datum the copula is
blind to by the exchange line. Its concrete kill: any output of the exchange sign, the occupation
ceiling, or ln2-as-a-value is an exchange-line violation, rejected on sight.

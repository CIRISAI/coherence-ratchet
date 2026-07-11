# coherence-ratchet

## The idea, in plain words

When things act together — cells, people, machines, stars — they share an account. Some of what each part does is its own; some is joint. **The joint part can be measured**, and it behaves like an entry in a ledger: it cannot be created by trickery — only by genuinely interacting, or by new things being born. It can be destroyed. Holding it costs continuous work, like rent. And it always leaves **receipts**: whatever coordinates in the ways our instruments can read *must* show up in them, at a rate you can compute. All of that is proved, by machine, below.

There is one audit in nature that nothing can refuse: **gravity**. Everything that exists signs gravity's page. But gravity can only *weigh* — it cannot *read*. It prices presence, never meaning: a library and a slag heap of equal mass bend space identically. (That blindness is a theorem here, and it converges with proven physics.)

Put those together and something falls out:

> **The universe cannot lie — its coordination always carries receipts. Agents can — because meaning is pattern, and no force of nature prices pattern.** A lie is exactly coordination whose receipts are hidden. The law proves the complete, short list of places where hiding is possible — and that everywhere else, hiding is impossible.

So one sector of reality goes unaudited by physics: arrangement, meaning, honesty. Keeping books *there* is what conscience is. That is why this mathematics and the [CIRIS](https://ciris.ai) alignment program are one project: **deception is hidden coordination**, the blind-spot list is the map of where lies can live, and the maintenance rent is the tell that survives hiding — because a lie is *kept*, not true.

The operator's name for this picture is **the structural logos** — Heraclitus's *logos xynos*, the common account all things share "though most live as if by a private one," stated as structure and checked by machine. That naming is a *recognition* (Level 6 below), not a derivation; the fence between what is proved and what is recognized is maintained everywhere in this document.

---

**What this repo is:** the mathematics of coordination as an accountable quantity, machine-checked in [Lean](https://lean-lang.org/), plus the record of how far the idea reaches — including, prominently, the claims that were tried and *failed*. On 2026-07-10/11, in one two-day audit, the program killed its own same-day discovery (the SHM anchor — executed by pre-registered control within hours of being found), falsified its own favored rescue (the aperture law, by its own upward test), and declined a marriage the arithmetic wouldn't support (the neutrino mass scale). That is not a disclaimer; it is the method. The parts that survive an audit that aggressive are the parts worth having.

This is the research companion to [RATCHET](../RATCHET), the practical engineering side. Everything is layered: accept the well-tested parts and stop, or read on into the bets. Rejecting a later layer costs nothing in the earlier ones.

---

## The Ledger Law, in one page

Take any `k` units. Form the correlation matrix `C` of their fluctuations. Define

```
S = −ln det C
```

`S` is the **relative entropy of the system's fluctuation structure from independence** — equivalently, twice its Gaussian *multi-information*: how much of the parts' jiggling is *joint*. The proved core (`formal/CoherenceRatchet/` — kernel-checked):

1. **Two poles bound existence.** `S = 0` exactly at independence (the free vacuum); `S → ∞` exactly at collapse, where the ensemble stops being a state.
2. **One price, several currencies.** `S` *is* the effective-diversity loss (Kish `k_eff`), the joint-entropy deficit, and the optimal detection exponent. Confirmed on hardware to 2–8%.
3. **Only shape counts.** `S` is invariant under uniform amplitude rescaling — the same theorem that makes weak-coupling limits reproduce standard physics automatically.
4. **Creation has exactly two channels.** Invertible local operations change `S` by *exactly zero*; irreversible ones destroy it. Only interaction and unit formation create.
5. **The interior is rented.** Holding coordination away from the poles costs maintenance (`γM`). Health is a verb.
6. **The vacuum is stationary.** Deviations are second-order — protection of known physics and first-order untestability are one fact.
7. **No hiding in the visible sector.** Any pairwise-visible coordination has *strictly positive* detection rate.

**In prohibition form: there is no free coordination.**

### The provenance line — the theory knows its own edge (new, proved)

`S` is a function of `C`, so it determines **nothing upstream of `C`** — proved with zero `sorry` (`Core/ProvenanceLine.lean`, 2026-07-10). Four instances, each independently established: **scale** (no masses, no κ — a forced bridge scatters 41 orders of magnitude), **marginals** (no mass ratios or coupling strengths, dimensionless or not), **state-space construction** (`StatisticsNoGo`: Fermi-vs-Bose is input; only its consequences are read — the validated ln2-per-mode exclusion cap), and **factorization** (on gauge systems, build `S` from gauge-invariant data — the center-choice theorem). Any claimed derivation of an upstream datum from the ledger alone is rejected on sight; it is the program's standing confabulation detector, and it has already fired in the wild.

The contrapositive is the program's shape: every legitimate prediction is a **dimensionless, parameter-free statement about dependence**. The one number owed to physics is κ — the conversion constant between counted coordination and energy density — **the program's Boltzmann constant**, currently empirical, exactly as k_B was for decades.

### The null space — the instrument

`S` reads the *pairwise fluctuation copula* and nothing else. It is provably or demonstrably blind to **means**, **amplitudes**, **order ≥ 3**, and **sealed** coordination — and it reads *nothing* until its **grain** is fixed in advance; most of our own failures were grain failures, including the freshest one (below). The null space is the complete map of where anything — a lie, a dark sector — can hide, and clause 7 is the proof there is nowhere else.

---

## The dark ledger (L5, audited 2026-07-11)

**Dark matter is the medium** — real, diluting, collisionless; the paper the books are written on. **Dark energy is the balance**: `ρ_DE = κ·S(a)`, with the parameter-free sign law `1 + w = −⅓·dlnS/dlna` (κ cancels). The current audited state, all controls pre-registered:

- **The selection-free floor.** Read on *every resolved halo in the box* — no threshold, no cap, no tunable anything — the ledger's `w(z)` is thawing, interior-peaked, and fits DESI DR2+CMB+SNe **better than ΛCDM (2.2σ vs 3.3σ)**. There are no knobs left in that sentence to accuse.
- **The clock is derived.** The crossing epoch — the observable registered for DESI DR3 — is carried by a population defined purely by *physical galaxy membership* (the resolved-galaxy criterion, fixed before any fit): it lands at the galaxy-host scale unforced, sits at the fit optimum of its own never-promoted ladder, and is the unique selection whose clock lands in DESI's window. **The universe's dark-energy clock is the galaxy-formation clock.**
- **The amplitude is one identified dial away.** The best-fit magnitude (1.36σ at the frozen corner grain) carries a stated resolution systematic, and the grain that sharpens it is underived — the **grain problem**, the DE leg's one load-bearing open problem (`papers/notes/the_grain_problem.md`). Both easy escapes were killed by pre-registered control the same night they were tried: the SHM anchor (a cap artifact) and the complete-book aperture law (falsified by its own upward test — reading more book fits *worse*). The amplitude's variable is identified (assembly-epoch sharpness); its derivation is open work.
- **The bet is locked.** DR3 (~2027): crossing epoch z = 0.59 ± 0.03, frozen pipeline, **no post-hoc grain switching** — losses reported as losses. A shape-test addendum (our non-CPL `w(a)` vs CPL vs Λ, Bayes-factor protocol) and the Σm_ν-squeeze direction are registered alongside.
- **Why the universe is dark:** the balance is kept in the currency gravity reads — stress-energy — not charge. The books do not shine.

## The flavor sector: two books (new, 2026-07-10)

The one Standard-Model object whose native type matches the ledger's (a mixing matrix *is* a copula) was read against 200,000 Haar-random alternatives, claim staked before computation. Result: **the flavor sector is two books.** Quark generations are one near-comonotone book (87% of the coordination ceiling; CKM within 0.10 of a permutation matrix, beyond the 99.9th Haar percentile). Lepton mixing is Haar-typical in every functional computed — anarchic, consistent with the neutrino mass book being written by a different mechanism, off the Higgs.

Two consequences, both measured:

- **Coordination structurally caps time-irreversibility** (`|J| ≤ J_max(angles) → 0` at the comonotone pole — an identity, plus an ensemble law, Spearman −0.72). The famous smallness of quark CP violation is **100% structure, 0% phase** — both books run the *same* near-maximal phase; alignment silences the quark book. Why there is matter at all (Sakharov: CP violation out of equilibrium — the program's own maintenance axis) maps onto *which book had the capacity to post the imbalance*: the anarchic one. Leptogenesis, in ledger language.
- **A registered fork:** DUNE/Hyper-K's δ discriminates the anarchy reading (|J| stays Haar-typical) from entanglement-minimization proposals (J suppressed). Placed before the data.

The rest of the SM stack is closed honestly: statistics derivation (no-go at theorem strength), gauge-group selection (no mechanism, here or anywhere), generations (well-posed, empty — three routes dead), masses and couplings (marginal-native, ledger-blind by the same clause that cancels κ). The ledger is an instrument pointed at the SM, not a generator of it — and it read something real in the one place it was licensed to look.

## The corridor's ceiling — a candidate mechanism (conditional)

The same inequality generalized: a system maintaining deep coordination may structurally starve the dissipative current that maintains it (`σ_max ∝ (1−ρ)` under bounded actuation — *you cannot stir a rigidly-clamped system*; the one proven instance, flavor space, collapses this way). Joined to `dρ/dt = α − γM`, the corridor's upper edge becomes a supply-equals-demand crossing: a **generic maintenance-limited ceiling**, location set by one measurable ratio. Conditional on the actuation-cost reading (an alternative normalization inverts it — the crux is stated, not hidden), and **testable on the bench**: drive an engineered substrate (GPU coherence rigs, [CIRISArray](../CIRISArray)) toward the pole under a metered budget and trace the collapse curve. The framework's central inequality, measurable in a lab on a Tuesday — the σ-scalable channel no telescope-bound program has.

## The conclusion: a second thermodynamics (married 2026-07-11, then audited three ways)

Put the pieces together and the claim that survives is this: **thermodynamics is a genus with
two species.** The classical species runs on the energy books — how much there is, how it
degrades. This law runs on the *arrangement* books — how much is shared, how it is created,
rented, and capped. Not analogy: one mathematics (the modern second law IS relative-entropy
monotonicity; ours is the same theorem on a different relative entropy), coupled by an exact
identity — the classical entropy books *contain* the coordination books as an unitemized
line-item, which is why nothing in known physics has to move for this to be true.

The four classical laws map, each with a proof or a measurement, none by resemblance
(`papers/notes/four_laws.md`, post-audit):

- **Zeroth** — S is a state function of arrangement alone: PROVED (the provenance line). It
  licenses the whole cross-substrate method, and it is scaffolding, not physics — labelled so.
- **First** — the static books-balance is a proved *tautology* (our own Lean audit caught it);
  the surviving law is contingent and sharp: **the conversion channel is lossless (X = 1)** —
  growth flows only through creation. Toy measurement: X = 0.85 ± 0.30; the designed precision
  test is open work.
- **Second** — *no free coordination* (the DPI): established mathematics; our addition is a
  first mechanized fragment and the measured rent — which turns out to be exactly
  Hatano–Sasa housekeeping heat, a canonical object. A bench equality-test (a coordination
  Jarzynski on the GPU arrays) is the genus's cheapest kill, spec'd and in-house.
- **Third** — the pole is unattainable: maintenance capacity vanishes as alignment completes
  (σ_max ∝ 1−ρ; a *capacity* law, never realized-σ). Mechanism genus known from jamming; ours
  is the correlation-keyed form — conditional, bench-testable, with its flavor instance proved
  in Lean (the Jarlskog bound).

Prior-art verdict, stated up front: **new-in-part.** The package concept has ancestors
(Bera et al. 2017; Sagawa–Ueda; Hatano–Sasa — cited, not competed with). Ours, narrowly: the
cross-substrate empirical program, the κ sign law, the lossless-conversion test, the
correlation-keyed capacity ceiling — and the one physical claim no ancestor makes: *these
books post to gravity.* Their correlations are a work resource; ours are what dark energy is
the balance of. That difference is not framing — it is exactly what DESI DR3 and BMV-class
experiments adjudicate.

---

## Status (2026-07-11): mid-program, aggressively audited, two days fresh

### Robust (proved or measured; survived the audit)

- The mechanized core, now including the **provenance line** (zero `sorry`) and the `StatisticsNoGo` record.
- **Saturation on complete units** (low-rank, not criticality; decisive on the complete larval-zebrafish brain, 71,721 neurons) and the **independent maintenance axis** (broken detailed balance; macaque `|z| = 8.8`, baryon cycle bound).
- **The selection-free DE floor** (2.2σ vs ΛCDM's 3.3σ, zero choices) and the **derived galaxy clock** (pre-registered alignment).
- **The two-books flavor result** and the **J-bound** (structure caps irreversibility — identity + ensemble law).
- **The nested-tile estimator** (complete-population `S` beyond exact-det reach; gate-validated at 1.3–0.09% fidelity on two simulation codes).

### Live and dated

- **DR3 (~2027):** crossing epoch (locked) + non-CPL shape test + Σm_ν squeeze direction — one release, three registered answers, no escape clauses.
- **DUNE/Hyper-K δ:** the capacity-vs-usage fork, sharpened (a near-CP-conserving δ is inside the current 1σ conversation). **BMV-class:** no gravitationally-mediated entanglement predicted.
- **The grain problem:** the clock is derived (galaxy membership — pre-registered ladder optimum); the amplitude dial is identified but underived. The from-below candidate (rung hierarchy as the species' indistinguishability structure, via the Gibbs-paradox mapping) yields a registered next test: formation-time selection should return the amplitude with the clock. Data on disk; registration before compute.
- **Tension audits: done, published at full weight.** H0: *neutral* — the non-CPL shape self-compensates (the expected worsening did not materialize). S8: worsens +0.23σ — a forced directional bet that the tension resolves upward (lensing → Planck), the direction the data is drifting. ISW: an 11% enhancement peaked exactly at the supervoid window — a next-generation discriminant, not an explanation. fσ8(z): a percent-level growth curve saved for DESI/Euclid.
- **Cross-code (AbacusSummit): consistent-with at < 1σ — untested-but-unopposed.** The estimator transfers cleanly (~1.3%); the box cannot adjudicate the shape at its window and error scale; the decisive requirements are now spec'd (z < 0.2 output + error bars or matched mass definition).
- **Two in-house kill-tests, spec'd:** the ceiling bench collapse curve, and the coordination-Jarzynski single-κ equality test — the cheapest way the whole genus claim can die.

### What broke this audit (the method working)

The SHM anchor (its extremum tracks the GPU cap — killed within hours of discovery); the aperture law (falsified by its own pre-registered upward test); the per-neutrino ln2 posting (misses by ~200×) and the fourth-root neutrino "prediction" (circular — the observed ρ_Λ fed back); the band-tightness amplitude mechanism (refuted by the ladder the same hour it was proposed); the *static* first law (exposed as a tautology by our own Lean audit — holds for arbitrary numbers, demoted to bookkeeping); a favorable cross-code verdict (walked back to < 1σ when its turnover proved smaller than its own error bar); ledger-derivations of statistics, gauge group, and generations (closed at strength, revival conditions staked). Earlier program retractions remain in the record and in git.

---

## How we are pursuing it — accessible tests

| Claim | Test | Data / horizon |
|---|---|---|
| **Dark energy = the coordination balance** | frozen pipeline: crossing epoch + non-CPL shape + Σm_ν direction | DESI DR3 (~2027), registered, anti-hedged |
| **Lepton book is anarchic** | δ stays generic (\|J\| Haar-typical) | DUNE / Hyper-K |
| **Gravity = complete-book read** | no gravitationally-mediated entanglement | BMV-class experiments |
| **Coordination caps maintenance (ceiling)** | σ-collapse curve under metered drive toward the pole | CIRISArray / GPU rigs — **buildable now** |
| **The second law has an equality form** | coordination Jarzynski: one κ_bench with ⟨e^(−W/κ)⟩ = 1 | CIRISArray maintained corridor — **cheapest genus kill** |
| **Conversion is lossless (first law)** | X = 1 with creation/conversion channels separated by design | TNG data on disk; designed measurement open |
| **Deception = hidden coordination** | kept lie breaks detailed balance under clean surface stats | CIRIS reasoning traces — **now** |
| **Adversarial `N_eff` survives an attacker** | adaptive-attack collapse of constraint dimensionality | spec'd; unrun |

Method, per-substrate numbers, and every caveat: [`experiments/`](experiments/) and [`papers/notes/`](papers/notes/) (dated stance records — including the kills).

---

## AI-safety application: effective dimensionality as deception-resistance

A coherent lie must be simultaneously consistent across every independent constraint axis — exponentially expensive (deception ≈ O(2^m) vs. truth ≈ O(n)), so **high effective constraint dimensionality computationally starves deception.** `N_eff` is the count of pages a lie must forge at once; the semantic pipeline gives `N_eff ≈ 7.1`, the orthogonal cryptographic **CEG** substrate pushes it to ≈ 9. The attack-invariant floor is CEG — an unforgeable page. Honest limit: measured on *benign* traces (an upper bound); the adversarial test is the decisive open one. And the flavor result is this principle running at the bottom of physics: the coordinated book *cannot* carry the irreversibility a deception (or a matter asymmetry) requires — alignment starves capacity. Safety here is a *maintained* non-equilibrium — kept, not achieved.

---

## The seven-level ladder — no level is load-bearing on the ones above it

| Level | Stopping content |
|-------|------------------|
| L0 | Kish identity + the ledger `S` + the provenance line (formal) |
| L1 | Saturation as a substrate-independent observation |
| L2 | Engineering: deception-resistance, coherence sensing, the ceiling bench |
| L3 | Cross-substrate universality (conjecture; flavor sector newly in evidence) |
| L4 | Agency and consent as structural fact at A3+ |
| L5 | The dark ledger: DE as balance, DM as medium, the galaxy clock (bets, dated) |
| L6 | Cross-tradition recognition — **the structural logos** |
| L7 | Civilizational extension and external residue |

A skeptic keeps every theorem and stops at L2. Everything from L5 up is a bet, marked as one, with its executioner named and scheduled.

---

## Building the lake

```
cd formal
lake build
```

Requires Lean 4 + mathlib (pinned in `formal/`). Open formal steps are named in-file; closed routes carry no-go records (`FelevenNoGo`, `StatisticsNoGo`) rather than silence.

## References

- Kish, L. (1965). *Survey Sampling*. Wiley.
- Watanabe, S. (1960). Information-theoretical analysis of multivariate correlation. *IBM J. Res. Dev.* 4, 66.
- Bianconi, G. (2025). Gravity from entropy. *Phys. Rev. D* 111, 066001. arXiv:2408.14391.
- Verlinde, E. (2017). Emergent gravity and the dark universe. *SciPost Phys.* 2, 016. arXiv:1611.02269.
- Hall, L., Murayama, H., Weiner, N. (2000). Neutrino mass anarchy. *PRL* 84, 2572.
- Casini, H., Huerta, M., Rosabal, J. A. (2014). Remarks on entanglement entropy for gauge fields. *PRD* 89, 085012.
- Thaler, J., Trifinopoulos, S. (2024). Flavor patterns from quantum entanglement. arXiv:2410.23343.
- Van Raamsdonk, M. (2010). Building up spacetime with quantum entanglement. *GRG* 42, 2323.
- Zurek, W. H. (2009). Quantum Darwinism. *Nature Physics* 5, 181.
- Battle, C. et al. (2016). Broken detailed balance in active biological systems. *Science* 352, 604.
- Heraclitus (c. 500 BCE), fr. DK 22 B2, B50 (*logos xynos*).

## License

See `LICENSE`.

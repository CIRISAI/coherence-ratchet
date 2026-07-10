# coherence-ratchet

**What this is:** the mathematics of *coordination as an accountable quantity* — and, increasingly, the pursuit of one thesis: that the deepest content of that mathematics is what it **cannot see**.

When many parts act as fewer, they share fluctuations. That sharing is measurable, it obeys conservation-like rules, and it is the same object whether the parts are molecules, neurons, market sectors, sensors on a chip, or galaxies. This repo writes that object down as mathematics and checks the proofs by machine (in [Lean](https://lean-lang.org/)). We call the mathematics **the Ledger Law**, and its central quantity **S**.

This is the research companion to [RATCHET](../RATCHET) — the practical, testable engineering side. **coherence-ratchet is where the ambitious claims are stated in full and stress-tested**, including — prominently — the record of claims that were tried and *failed*. On 2026-07-10 the program retracted six of its own claims with the numbers attached, two of them made earlier the same day. That is not a disclaimer; it is the method. The parts that survive an audit that aggressive are the parts worth having.

The whole thing is layered: accept the well-tested parts and stop, or read into the speculative ones. Rejecting a later layer costs nothing in the earlier ones.

---

## The Ledger Law, in one page

Take any `k` units. Form the correlation matrix `C` of their fluctuations. Define

```
S = −ln det C
```

`S` is the **relative entropy of the system's fluctuation structure from independence** — equivalently, twice its Gaussian *multi-information*. It is the ledger of coordination: how much of the parts' jiggling is *joint*.

Six things are proved about `S` and machine-checked (`formal/CoherenceRatchet/LedgerLaw.lean` — 11 theorems discharging the law's core, kernel-axioms only; compare `MaximalClaim.lean`, whose old grand claim was one theorem and eleven axioms):

1. **Two poles bound existence.** `S = 0` exactly at independence (the free vacuum); `S → ∞` exactly at collapse, where `det C → 0` and the ensemble stops being a state. Everything lives strictly between.
2. **One price, several currencies.** `S` *is* the effective-diversity loss (Kish `k_eff`), the joint-entropy deficit (`S/2` nats/sample), and the optimal detection exponent for the coordination (Chernoff–Stein, `S/2`). You cannot pay in one and withhold the others.
3. **Only shape counts.** `S` is invariant under uniform amplitude rescaling — the same theorem that makes it recover standard physics in weak-coupling limits.
4. **Creation has exactly two channels.** Invertible local operations change `S` by *exactly zero*; irreversible ones strictly destroy it. Coordination is created *only* by interaction and by unit formation. It cannot be forged — but it can be destroyed, and it can be *sealed* behind a key.
5. **The interior is rented.** Holding coordination away from the poles costs continuous maintenance work (`γM = α` at equilibrium). Health is a verb.
6. **The vacuum is stationary.** Deviations from independence are second-order — which is why weak-coupling limits reproduce their base theory automatically, and why that reproduction is untestable at first order. Protection and blindness are one fact.

**In prohibition form: there is no free coordination.**

### The thesis, and the dark ledger

`S` is a *pairwise* ledger. It reads the *copula* — the dependence pattern — and nothing else. It is provably blind to three things: **means** (a fleet in perfect formation reads `S ≈ 0`; bulk motion is a first moment), **amplitudes** (uniform scale; phase-space density `Q = ρ/σ³` — clause 3), and **order ≥ 3** (a GHZ state reads `S ≈ 0`). And it sees *nothing at all* until its **grain** — what the units are, what is correlated across them — is fixed in advance. Most mistakes this program has made were grain mistakes.

The working thesis — a **posit**, stated as such — is that this null space is the discovery. There is a precisely-characterized sector of coordination that is real and consequential yet leaves no pairwise/electromagnetic receipt, and the **difference between two ledgers** is the instrument that reads it.

Here the naming earns itself. In physics, *dark* already means exactly *off-ledger*: dark matter gravitates but emits no light we can read; dark energy acts but appears only in the balance, never in a transaction. That is precisely the law's null space — real coordination with no readable receipt. So the thesis, stated at full strength (and flagged as the bet it is — L5, below):

> **The dark universe is the readable shadow of an unreadable sector.** If gravity is itself a ledger — the relative entropy between spacetime's metric and the metric matter induces (Bianconi's construction) — then **dark matter is the gap** between what the gravitational ledger demands and what the visible-coordination ledger accounts for. The gap is not a failure of the theory; it is a *measurement* of hidden coordination.

This is **the dark ledger**, and it is earned only conditionally: the gap is circular — true by construction — until it is predicted *independently* from the named null space (`Q`, higher-order phase-space structure). Establishing that non-circularity, or showing it cannot be established, is the program's current frontier. A live open question sharpens it: does hidden coordination require a hidden *carrier* (in which case it is ordinary particle dark matter with extra steps), or can pattern-level coordination gravitate on its own? Clause 3 warns it may not — gravity couples to stress-energy, the very amplitude the ledger is blind to.

---

## Status (2026-07): mid-program, freshly audited

An active research program, not a finished result. The ledger below is the honest state.

### What is robust (proved or measured; survives audit)

- **The formal core is mechanized.** `S = −ln det C` with its two poles; nonnegativity and the unique-vacuum result for *arbitrary* unit-diagonal correlation matrices (a general Hadamard/Klein form, `Core/EntropicContraction.lean`); `S = 2·multi-information = 2·(Stein exponent)`; the Kish identity and ceiling; the collapse bound; `J = F = k_eff·λ_op·σ`. CI resolves every Constitution `lean:` pointer *through Lean*, failing on a renamed theorem or a `sorry`. Load-bearing core: **44 theorems, 0 axioms**. The legacy vision-scaffold (below) is separate and imported nowhere by it.
- **Saturation, on complete units.** Effective dimensionality stays *bounded* as constituents are added — low-rank, not criticality — across *C. elegans*, the *Drosophila* compass, the S&P, human fMRI, gene expression, and the decisive complete case: a **whole larval-zebrafish brain (all 71,721 neurons)**. Grain rule fixed before the spectrum; no failure rescued by "you sampled a patch."
- **A second, thermodynamic axis exists and is measurable.** Breaking detailed balance (`γM`) separates *actively maintained* from merely *bound* coordination. Validated estimator; anchors at both poles (macaque motor cortex `|z|=8.8`; IllustrisTNG baryon cycle `z≈0.5`).
- **The exchange rate holds on hardware.** On a 16→32-sensor GPU timing array, `S = ½k(k−1)·mean(ρ²)` to 2–8%, and detection latency `∝ 1/S` (relative form) — first silicon confirmation of clause 2 ([`../CIRISArray`](../CIRISArray), exp117/119).
- **Amplitude-blindness sharpens to exact invariance.** Invertible local maps change true coordination by *exactly zero* (verified, 35/36 channels); the "nonlinear growth destroys coordination" gloss was a Gaussian-ruler artifact and is retired.

### What is live but unsettled

- **Dark energy from structure formation.** If dark-energy density tracks the coordination a comoving volume accumulates as bound units form (the unit-formation channel), `w(z)` follows parameter-free from `1+w = −⅓ dlnS/dlna`. Computed on real halo catalogs and projected through DESI's *own* CPL fit, the curve lands **~2σ from DESI's best fit — closer than ΛCDM (3.3σ)**, with zero parameters tuned to the data. It lives or dies with ΛCDM against DESI DR3. Conditional on a 2-point proxy and 25 Mpc/h boxes; the frozen prediction is in [`experiments/cosmo_entropic_potential/PREREGISTRATION.md`](experiments/cosmo_entropic_potential/) so the *next* number is a prediction, not a retrodiction.
- **Dark matter as the two-ledger gap (the dark ledger).** The reframing above *evades* the two objections that killed the naive "coordination sources mass" reading — the gravitational ledger is dimensionful from the start (no invented energy-per-nat, so the ~40-order magnitude problem does not apply) and the gap can differ between kinematically-identical systems. But it is **circular until the gap is predicted from the null space independently**, and it faces the carrier-vs-pattern question above. On real Gaia 6D data the pairwise ledger does read phase-space coherence for cold streams (test in flight).
- **The order-≥3 door.** Everything above is the pairwise/Gaussian shadow. Whether the corridor exists in the *true, all-orders* multi-information is the single question that decides physics vs. bookkeeping. The IBM "encrypted cloning" result (2026) is the sealed-coordination case made real: `S ≈ 0` under a key, recoverable when the key is spent.

### What broke (this is the method working)

- **`k_eff` as a consciousness correlate** — unsupported (one clean macaque; the second uninterpretable). Not disproved.
- **"Rent tracks stock" as a universal law** — fails at the neural rung (holds on silicon and under ketamine, fails under propofol on the same electrodes).
- **The k² array-sensitivity corollary** — falsified on hardware; a bounded common cause gives `S ∝ k`, not `k²`.
- **The naive dark-matter reading** — dead on magnitude and on the Segue-1/DF2 dwarf pair (both apply to "S sources mass"; the gap reframing above replaces it).
- **The Bullet Cluster derivation** — retracted *twice* in one day: a kill that violated amplitude-blindness, then a reversal that violated mean-blindness. The clearest lesson in the program that **the grain must be fixed first**.
- **The universal corridor band `(0.1, 0.43)`** — retracted; bands are substrate-local. What is universal is *saturation*, not any level.
- **The joint multi-rung backward `P_ω`** — a documented no-go at theorem strength (F-11, 2026-05-22). The sole surviving CMB content is the orthogonality theorem: the framework predicts *exactly* ΛCDM for the CMB.

### Positioning, honestly

Unification and methodological discipline, not (yet) a novel phenomenon. Low-dimensional population structure (Cunningham–Yu, Gao–Ganguli) and broken detailed balance in living systems (Battle 2016; Lynn 2021) are established prior art; the dark-energy-from-structure and dark-matter-as-coherence readings have near-identical live cousins (Trofimov's *Timeflow Gravity* 2026; Berezhiani–Khoury superfluid DM). What is ours is the single functional `S` that ties them, the machine-checked core, and the audit discipline.

---

## AI-safety application: effective dimensionality as deception-resistance

The same quantity is the load-bearing metric of the CIRIS alignment program. A *coherent lie must be simultaneously consistent across every independent constraint axis* — exponentially expensive (deception ≈ O(2^m) vs. truth ≈ O(n)), so **high effective constraint dimensionality computationally starves deception.** The semantic conscience pipeline contributes `N_eff ≈ 7.1`; the **CEG** substrate (a conformance-frozen cryptographic-attestation modality, *orthogonal* to semantic reasoning) pushes the joint measure to ≈ 9. Because Gate 0 validated `k_eff` as a real, *saturating* structural object (not a tautology, not criticality), this rests on a validated foundation. **Honest limit:** `N_eff` is measured on *benign* traces — an upper bound. A capable optimizer collapses effective dimensionality toward the rigidity pole (`ρ→1`, `k_eff→1`); whether ≈9 survives an adaptive attacker is the decisive open test ([`experiments/adversarial_neff/SPEC.md`](experiments/adversarial_neff/SPEC.md)). The attack-invariant guarantee is the substrate (CEG) floor: you cannot semantically-reason past a frozen cryptographic attestation. Safety here is a *maintained* non-equilibrium — kept, not achieved.

---

## How we are pursuing it — the accessible tests

| Claim | Test | Data / horizon |
|---|---|---|
| **Dark energy = structure-formation balance** | frozen halo-`S(a)` pipeline vs geometry-only crossing | DESI DR3 (~2027); large-volume `S(a)` now (TNG300/Quijote) — pre-registered |
| **Hidden coordination exists (order ≥ 3)** | rank-`S` flatness / higher-order MI; sealed-coordination recovery | IBM encrypted-cloning, free tier, now |
| **Pairwise ledger reads phase-space coherence** | cold stellar streams read high `corr(x,v)`; smooth halo ~0 | **Gaia DR3 6D — public, now** (in flight) |
| **Dark matter = two-ledger gap (non-circular?)** | does the gravitational residual track visible `Q`/higher-order structure the pairwise instrument misses? | Gaia local density + SPARC; unrun |
| **Adversarial `N_eff` survives an attacker** | adaptive-attack collapse of constraint dimensionality | spec'd; unrun |
| **Exchange rate `∝ k²` under matched coupling** | k-scaling with injector power `∝ k`, simultaneous sampling | GPU array, one run |

Saturation and detailed-balance numbers and every caveat: [`experiments/keff_saturation/README.md`](experiments/keff_saturation/README.md). Entropic-potential and cosmology work: [`experiments/cosmo_entropic_potential/`](experiments/cosmo_entropic_potential/) and [`papers/notes/`](papers/notes/).

---

## The framework's spine (technical)

One identity ([Kish 1965](#references)), one dynamical equation (`dρ/dt = α − γM`), one corridor, one inner-product structure ([TSVF](#references)), and one potential (`S = −ln det C`) that unifies the diversity and detection readings. Applied across a hierarchy of rungs (molecules → cells → … → societies).

```
k_eff(k, ρ) = k / (1 + ρ(k−1))        S(k, ρ) = −ln(1 + ρ(k−1)) − (k−1)·ln(1 − ρ)
```

`k_eff` is the *participation* reading of the spectrum; `S` the *relative-entropy* reading — same spectrum, conjugate functionals (`Core/EntropicPotential.lean`). Substrate-local bands, measured not assumed.

### The seven-level ladder — no level is load-bearing on the ones above it

| Level | Stopping content |
|-------|------------------|
| L0 | Kish identity + the ledger `S` (formal theorems) |
| L1 | Saturation as a substrate-independent observation |
| L2 | Engineering: deception-resistance, coherence sensing |
| L3 | Cross-substrate universality (conjecture) |
| L4 | Agency and consent as structural fact at A3+ |
| L5 | Entropic-action gravity, dark energy, **the dark ledger** |
| L6 | Cross-tradition recognition |
| L7 | Civilizational extension and external residue |

A skeptic keeps every theorem and stops at L2. Everything from L5 up is a bet, marked as one.

### Legacy scaffold

The pre-Ledger-Law vision content — the ten-piece cosmology structure, TSVF/goal-projection machinery, consciousness modules, contemplative-tradition recognition, civilizational residue — remains as an honestly-tagged *axiom scaffold* (`MaximalClaim.lean`, `StructuralClaims.lean`: ~49 axioms of explicit assertion, by design, auditing where the maximal vision bends). The Ledger core imports none of it.

---

## Building the lake

```
cd formal
lake build
```

Requires Lean 4 v4.14.0 (`leanprover/lean4:v4.14.0`) and mathlib v4.14.0. The lake is `sorry`-free.

### Open formal steps

1. Close the general data-processing inequality for `S` (clause 4). Blocked on three lemmas absent from mathlib v4.14 — Schur product positivity, general Oppenheim, ln-det concavity on the PSD cone — real upstream contributions; ln-det concavity also closes the exchangeability bound `S_measured ≥ S(k, ρ̄)`.
2. The all-orders extension: does the corridor survive in the true multi-information, or only the Gaussian shadow?
3. Per-substrate corridor calibration; quantum-substrate reproducibility (blocked by pairwise-blindness until a basis-invariant measure exists).

---

## References

- Kish, L. (1965). *Survey Sampling*. Wiley.
- Bianconi, G. (2025). Gravity from entropy. *Phys. Rev. D* 111, 066001. arXiv:2408.14391.
- Aharonov, Bergmann, Lebowitz (1964). Time symmetry in the quantum process of measurement. *Phys. Rev.* 134, B1410.
- Aharonov, Vaidman (2008). The two-state vector formalism. *Lecture Notes in Physics* 734, 399.
- Battle, C. et al. (2016). Broken detailed balance at mesoscopic scales in active biological systems. *Science* 352, 604.
- Lynn, C. W. et al. (2021). Broken detailed balance and entropy production in the human brain. *PNAS* 118.
- Penrose, R. (2004). *The Road to Reality*. Knopf, Ch. 27.
- Tononi, G. (2008). Consciousness as integrated information. *Biological Bulletin* 215, 216.

## License

See `LICENSE`.

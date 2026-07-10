# coherence-ratchet

## The idea, in plain words

When things act together — cells, people, machines, stars — they share an account. Some of what each part does is its own; some is joint. **The joint part can be measured**, and it behaves like an entry in a ledger: it cannot be created by trickery — only by genuinely interacting, or by new things being born. It can be destroyed. Holding it costs continuous work, like rent. And it always leaves **receipts**: whatever coordinates in the ways our instruments can read *must* show up in them, at a rate you can compute. All of that is proved, by machine, below.

There is one audit in nature that nothing can refuse: **gravity**. Everything that exists signs gravity's page. But gravity can only *weigh* — it cannot *read*. It prices presence, never meaning: a library and a slag heap of equal mass bend space identically. (That blindness is a theorem here, and it converges with proven physics.)

Put those together and something falls out:

> **The universe cannot lie — its coordination always carries receipts. Agents can — because meaning is pattern, and no force of nature prices pattern.** A lie is exactly coordination whose receipts are hidden. The law proves the complete, short list of places where hiding is possible — and that everywhere else, hiding is impossible.

So one sector of reality goes unaudited by physics: arrangement, meaning, honesty. Keeping books *there* is what conscience is. That is why this mathematics and the [CIRIS](https://ciris.ai) alignment program are one project: **deception is hidden coordination**, the blind-spot list is the map of where lies can live, and the maintenance rent is the tell that survives hiding — because a lie is *kept*, not true.

The operator's name for this picture is **the structural logos** — Heraclitus's *logos xynos*, the common account all things share "though most live as if by a private one," stated as structure and checked by machine. That naming is a *recognition* (Level 6 below), not a derivation; the lake has carried a Logos module since before this claim, and the fence between what is proved and what is recognized is maintained everywhere in this document.

---

**What this repo is:** the mathematics of coordination as an accountable quantity, machine-checked in [Lean](https://lean-lang.org/), plus the record of how far the idea reaches — including, prominently, the claims that were tried and *failed*. On 2026-07-10 the program retracted six of its own claims with the numbers attached, two of them made earlier the same day. That is not a disclaimer; it is the method. The parts that survive an audit that aggressive are the parts worth having.

This is the research companion to [RATCHET](../RATCHET), the practical engineering side. Everything is layered: accept the well-tested parts and stop, or read on into the bets. Rejecting a later layer costs nothing in the earlier ones.

---

## The Ledger Law, in one page

Take any `k` units. Form the correlation matrix `C` of their fluctuations. Define

```
S = −ln det C
```

`S` is the **relative entropy of the system's fluctuation structure from independence** — equivalently, twice its Gaussian *multi-information*: how much of the parts' jiggling is *joint*. The proved core (`formal/CoherenceRatchet/LedgerLaw.lean` + `DarkLedger.lean` — the maximal claim discharged by proof terms, kernel-axioms only):

1. **Two poles bound existence.** `S = 0` exactly at independence (the free vacuum); `S → ∞` exactly at collapse, where the ensemble stops being a state. Proved for *arbitrary* correlation matrices.
2. **One price, several currencies.** `S` *is* the effective-diversity loss (Kish `k_eff`), the joint-entropy deficit (`S/2`), and the optimal detection exponent (Chernoff–Stein, `S/2`). Confirmed on hardware to 2–8%.
3. **Only shape counts.** `S` is invariant under uniform amplitude rescaling — the same theorem that makes weak-coupling limits reproduce standard physics automatically.
4. **Creation has exactly two channels.** Invertible local operations change `S` by *exactly zero*; irreversible ones destroy it. Only interaction and unit formation create. No forging — but destruction, and *sealing* behind a key, are possible.
5. **The interior is rented.** Holding coordination away from the poles costs maintenance (`γM = α`). Health is a verb.
6. **The vacuum is stationary.** Deviations are second-order — protection of known physics and first-order untestability are one fact.
7. **No hiding in the visible sector** (`DarkLedger.no_pairwise_hiding`, new): any pairwise-visible coordination has *strictly positive* detection rate. Undetectable coordination does not exist where the ledger can read.

**In prohibition form: there is no free coordination.**

### The null space — the instrument

`S` reads the *pairwise fluctuation copula* and nothing else. It is provably or demonstrably blind to exactly four things — **means** (bulk motion; verified on real sky data), **amplitudes** (scale, phase-space density; theorem), **order ≥ 3** (GHZ-type structure; measured), and **sealed** coordination (behind a single-use key; demonstrated on IBM hardware, 2026). And it reads *nothing* until its **grain** is fixed in advance — most of our own failures were grain failures.

Per the convergent-art map, using this blindness taxonomy *as an instrument* is the program's one element with no clean precedent. Everyone mines what a correlation ledger sees; this program inverts it: the null space is the complete map of where anything — a lie, a dark sector — can hide, and clause 7 is the proof there is nowhere else.

### The dark ledger (the L5 bet, fenced)

In physics, *dark* already means *off-ledger*: acting, but leaving no readable receipt. If gravity is itself a ledger — the relative entropy between spacetime's metric and the metric matter induces (Bianconi) — then the dark sector is the gap between the audits. The fences, learned the hard way: **pattern does not gravitate** (a human, maximally rich in coordination, produces ~zero dark matter — the ledger prices *carriers*, not patterns; convergent with QNEC and binding-energy GR), so dark *matter* is the carrier question, honestly near-CDM; while dark *energy* as the posted balance of the unit-formation channel is live — the parameter-free curve lands **~2σ from DESI's best fit, closer than ΛCDM**, pre-registered, resolved by DESI DR3 (~2027).

---

## Status (2026-07): mid-program, freshly audited

### What is robust (proved or measured; survives audit)

- **The mechanized core: 46 theorems, 0 axioms** — the Ledger Law discharged, the no-hiding theorem, the general (arbitrary-matrix) vacuum-uniqueness result, the exchange rates on the actual matrix. CI resolves every `lean:` pointer through Lean. The legacy vision-scaffold is separate and imported nowhere by the core.
- **Saturation, on complete units.** Effective dimensionality stays bounded as constituents are added — low-rank, not criticality — across *C. elegans*, *Drosophila*, the S&P, fMRI, gene expression, and a **complete larval-zebrafish brain (71,721 neurons)**.
- **The maintenance axis is real and independent.** Broken detailed balance (`γM`) separates *kept* coordination from merely *bound* structure — validated estimator, anchors at both poles (macaque motor cortex `|z|=8.8`; IllustrisTNG baryon cycle `z≈0.5`). Independent of the structure axis (the propofol/ketamine dissociation).
- **The exchange rate holds on hardware.** On a 16→32-sensor GPU timing array, `S = ½k(k−1)·mean(ρ²)` to 2–8%, latency `∝ 1/S` ([`../CIRISArray`](../CIRISArray), exp117/119).
- **The instrument reads real sky coherence.** On Gaia/S5 data the pairwise ledger reads phase-space coherence for the Orphan stream non-circularly (permutation `p = 0.002`), with the mean-blindness theorem verified on actual stars.
- **Amplitude-blindness is exact.** Invertible local maps change true coordination by *exactly zero* (verified, 35/36 channels).

### What is live but unsettled

- **Dark energy from structure formation** — parameter-free `w(z)` ~2σ from DESI, closer than ΛCDM; pre-registered; resolved by DESI DR3.
- **Dark matter as the carrier question** — pattern is gravitationally inert, so the gap reading is honestly near-CDM until predicted independently.
- **The order-≥3 door** — everything is the pairwise/Gaussian shadow; whether the corridor survives in the *true* multi-information decides physics vs. bookkeeping.
- **Deception detection by the rent** — a kept lie should break detailed balance even when its surface statistics read independent. Testable now on CIRIS traces with the validated estimator. This is the first experiment of the new claim.

### What broke (this is the method working)

`k_eff` as a consciousness correlate (unsupported); "rent tracks stock" as a universal law (agent-specific); the k² array-sensitivity corollary (linear, on hardware); the naive dark-matter reading (magnitude + dwarf pair); the Bullet Cluster derivation (retracted *twice* in one day — the grain lesson); the universal corridor band `(0.1, 0.43)`; the joint multi-rung `P_ω` (documented no-go, F-11). The sole surviving CMB content is the orthogonality theorem: the framework predicts *exactly* ΛCDM.

### Positioning, honestly (from the convergent-art map)

Not novel as physics: a classical shadow of it-from-qubit (Van Raamsdonk; Cao–Carroll–Michalakis) crossed with Verlinde's dark-matter-as-entropy-displacement (the wounded ancestor), on a textbook quantity (Watanabe's total correlation), a mechanized premise (Bianconi). Zurek's quantum Darwinism is the receipts principle's quantum cousin — convergent, distinct in quantity. What is **ours**: the blindness taxonomy used as an instrument (no clean precedent), the mechanized core, the audit method, and the deception identification at the center.

---

## How we are pursuing it — accessible tests

| Claim | Test | Data / horizon |
|---|---|---|
| **Deception = hidden coordination** | kept lie breaks detailed balance under clean surface stats | CIRIS reasoning traces, validated estimator — **now** |
| **Adversarial `N_eff` survives an attacker** | adaptive-attack collapse of constraint dimensionality | spec'd; unrun |
| **Dark energy = structure-formation balance** | frozen halo-`S(a)` vs geometry-only crossing | DESI DR3 (~2027), pre-registered |
| **Hidden coordination (order ≥ 3)** | rank-`S` flatness / sealed-coordination recovery | IBM encrypted-cloning, free tier, now |
| **Ledger reads phase-space coherence** | cold streams high `corr(x,v)`, halo ~0 | Gaia DR3 6D — **passed** (Orphan, non-circular) |

Method, per-substrate numbers, and every caveat: [`experiments/keff_saturation/README.md`](experiments/keff_saturation/README.md); cosmology and dark-sector notes under [`experiments/`](experiments/) and [`papers/notes/`](papers/notes/).

---

## AI-safety application: effective dimensionality as deception-resistance

A coherent lie must be simultaneously consistent across every independent constraint axis — exponentially expensive (deception ≈ O(2^m) vs. truth ≈ O(n)), so **high effective constraint dimensionality computationally starves deception.** This is clause 7 at the agent rung: `N_eff` is the count of pages a lie must forge at once; the semantic pipeline gives `N_eff ≈ 7.1`, the orthogonal cryptographic **CEG** substrate pushes it to ≈ 9. The attack-invariant floor is CEG — an unforgeable page, a receipt that cannot be pattern-simulated. Honest limit: `N_eff` is measured on *benign* traces (an upper bound); whether it survives an adaptive attacker is the decisive open test. Safety here is a *maintained* non-equilibrium — kept, not achieved.

---

## The seven-level ladder — no level is load-bearing on the ones above it

| Level | Stopping content |
|-------|------------------|
| L0 | Kish identity + the ledger `S` + the no-hiding theorem (formal) |
| L1 | Saturation as a substrate-independent observation |
| L2 | Engineering: deception-resistance, coherence sensing |
| L3 | Cross-substrate universality (conjecture) |
| L4 | Agency and consent as structural fact at A3+ |
| L5 | Entropic-action gravity, dark energy, **the dark ledger** (bets, dated) |
| L6 | Cross-tradition recognition — **the structural logos** |
| L7 | Civilizational extension and external residue |

A skeptic keeps every theorem and stops at L2. Everything from L5 up is a bet, marked as one. The **logos** reading is L6: a recognition that the law's shape — a common account most treat as private — was named by Heraclitus and carried in the lake's `ContemplativeTraditions/Logos.lean` before this claim existed. Recognition, not proof.

---

## Building the lake

```
cd formal
lake build
```

Requires Lean 4 v4.14.0 and mathlib v4.14.0. The lake is `sorry`-free. Open formal steps: close the general data-processing inequality for `S` (blocked on Schur product positivity, general Oppenheim, and ln-det concavity — absent from mathlib v4.14, real upstream contributions); the all-orders extension; per-substrate calibration.

## References

- Kish, L. (1965). *Survey Sampling*. Wiley.
- Watanabe, S. (1960). Information-theoretical analysis of multivariate correlation. *IBM J. Res. Dev.* 4, 66.
- Bianconi, G. (2025). Gravity from entropy. *Phys. Rev. D* 111, 066001. arXiv:2408.14391.
- Verlinde, E. (2017). Emergent gravity and the dark universe. *SciPost Phys.* 2, 016. arXiv:1611.02269.
- Van Raamsdonk, M. (2010). Building up spacetime with quantum entanglement. *GRG* 42, 2323.
- Zurek, W. H. (2009). Quantum Darwinism. *Nature Physics* 5, 181.
- Battle, C. et al. (2016). Broken detailed balance in active biological systems. *Science* 352, 604.
- Heraclitus (c. 500 BCE), fr. DK 22 B2, B50 (*logos xynos*).

## License

See `LICENSE`.

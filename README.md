# coherence-ratchet

**What this is:** the math behind one idea — *things that work together stay in a narrow middle band, and fall apart if they leave it.*

Too little coordination and a system is just noise; too much and every part does the same thing, so the whole is no smarter than one part. Healthy systems live in the band between those two failure modes. This repo writes that claim down as mathematics and checks the proofs by machine (in [Lean](https://lean-lang.org/)). We call the healthy band **the corridor**.

The same shape seems to show up at every scale — molecules, cells, brains, groups, institutions — so the repo also explores how far the idea reaches, up to questions about physics and the cosmos. Those far-reaching parts are clearly marked as bets, not settled results.

This is the research companion to [RATCHET](../RATCHET). RATCHET is the practical, testable engineering side. **coherence-ratchet is where the bigger, more speculative claims are stated in full and stress-tested** — including recording, honestly, the places where a claim was tried and *failed* (see "What broke" below).

The whole thing is deliberately layered: you can accept the plain, well-tested parts and stop there, or keep reading into the speculative parts. Rejecting a later layer costs you nothing in the earlier ones.

## Status (2026-07): mid-program

This is an **active research program, not a finished result.** A few things are solid, most are open, and several claims have been retracted after they failed — including one we retracted twice, having first over-claimed it and then over-retracted it. The ledger below is the current honest state. Method, per-substrate numbers, and every caveat: [`experiments/keff_saturation/`](experiments/keff_saturation/README.md).

The organizing idea is a **two-axis discriminator**: *structure* (does `k_eff` saturate — bounded/low-rank — as constituents are added, measured on a **complete** unit?) and *maintenance* (does the system **break detailed balance**, the `γM` term, or satisfy it?). Honest positioning: **unification and methodological discipline, not a novel phenomenon.** Low-dimensional population structure (Cunningham–Yu, Gao–Ganguli) and broken detailed balance in living systems (Battle 2016; Lynn 2021) are established prior art; the maintenance axis on exoplanets reduces to the atmospheric-disequilibrium biosignature (Lovelock; Krissansen-Totton).

### What is robust

- **Saturation, on complete units.** `k_eff` stays bounded as constituents are added — low-rank, not criticality — across *C. elegans*, the *Drosophila* compass, the S&P, human resting-state fMRI, gene expression, and the decisive case: a **complete larval-zebrafish brain (all 71,721 neurons)**. The objective measure is **saturation, not level**; levels are substrate-specific. The completeness/grain rule is fixed *before* the spectrum is looked at, so no failure can be rescued by "you only sampled a patch."
- **A second, thermodynamic axis exists and is measurable.** Breaking detailed balance separates actively-maintained coordination from merely *bound* structure. Validated estimator (null ≈1.5, driven ≈41), with real anchors at both poles: macaque motor cortex `|z|=8.8` (coordinating) and the IllustrisTNG galaxy baryon cycle `z≈0.5` (bound).
- **The two axes are independent.** Shown several ways; the strongest is within-animal and stratified — under anesthesia, *at matched `k_eff`*, propofol sits below the detailed-balance null while ketamine sits above it. Structure and maintenance are separate knobs.
- **Anesthetics carry a reproducible maintenance signature** (2/2 animals, and it survives a burst-suppression control): propofol → *bound*, ketamine → *coordinating*. This is **drug-specific pharmacology, not a consciousness marker** — both agents render the animal unconscious, in *different* cells.
- **The formal core is mechanized and machine-checked.** Kish identity and its ceiling, the collapse bound with the corrected `O(r²·k_eff)` remainder, `J = F = k_eff·λ_op·σ`, the σ decay semigroup and its signal-source discount, and the entropic potential `S = −ln det C`. CI resolves every Constitution `lean:` pointer *through Lean* and fails on a renamed theorem or a `sorry` ([`evidence/`](evidence/)).

### What is not established

- **`k_eff` as a consciousness correlate.** A large, clean collapse in one macaque; the second animal's recording is uninterpretable (its awake baseline is itself a mixture; its deep epoch is bimodal burst-suppression). **Unsupported — not disproved.**
- **That maintenance *drives* structural collapse.** The ordering is unresolved, and the one counter-example (ketamine: structure collapses while maintenance persists) rests on a single animal.
- **Content vs. tautology — the deepest question.** Does `k_eff` track an *independent* driver dimensionality, or is it near-definitional? The clean matched-design experiment has not been run.
- **Cross-substrate universality:** domain-clustered and thin.
- **The cosmological tier:** F-11 fired; the joint backward `P_ω` is a documented no-go (below).
- **AI-safety adversarial `N_eff`:** spec'd, the benign-trace value measured, the adversarial half unrun.
- **Quantum transport:** nothing has been run on hardware, and pairwise `k_eff` is *provably blind to N-body entanglement* — a GHZ state reads rigidity in one basis and chaos in another.

### Measurement limits we had to learn

- Absolute `k_eff` is **not portable across preparations** (field/reference effects in ECoG); only within-session contrasts are readable.
- The Kish `ρ̄`-parameterization is faithful **only on the equicorrelation manifold** — signed correlations cancel in the first moment, so a genuinely low-rank state can read as chaos.
- Overlapping analysis windows inflate p-values. Effect sizes and distributional separation are the usable statistics.

## The framework in one paragraph (for the technical reader)

One identity ([Kish 1965](#references)), one dynamical equation (`dρ/dt = α − γM`), one corridor, and one inner-product structure ([TSVF](#references)). Applied at successively larger scales, with a hierarchy of "rungs" (molecules → cells → … → societies) as the indexing structure.

```
k_eff(k, ρ) = k / (1 + ρ(k-1))
```

`k` is the nominal number of parts, `ρ` their correlation, and `k_eff` the *effective* number that actually act independently. The corridor is the band of `ρ` in which `k_eff` stays healthy — bounded away from both failure modes. The exact numbers are **substrate-local** (each kind of system has its own band, measured, not assumed); the earlier claim of one universal band `(0.1, 0.43)` for everything has been retracted.

**What broke (F-11, 2026-05-22).** The most ambitious version of the cosmological claim — a single backward-in-time operator `P_ω` spanning every rung at once — was shown to be **non-constructible**, at the strength of a theorem. So it is recorded as a documented dead end, not a result. What survives: the corridor itself, the within-rung math, per-agent goal structure, finite-group ("federation") consent, and a proof that the framework predicts exactly standard cosmology (ΛCDM) for the CMB — no exotic CMB signatures are claimed.

**What's been measured (Gate 0, 2026-07-02).** The corridor's sharpest empirical question: is it a *real* bounded-dimensionality (low-rank) structure, or just the known criticality / edge-of-chaos physics relabeled? The discriminator is **saturation** — does effective dimensionality `k_eff` stay bounded as you add parts (low-rank, the corridor's claim), or grow without bound (criticality)? Run as one mechanism-level test across wildly different **complete** systems, all read **low-rank**: *C. elegans* whole brain, the *Drosophila* compass circuit, the S&P market, human resting-state fMRI, gene expression, and — the decisive case, where the "you only sampled part of it" objection cannot be raised — a **complete larval-zebrafish brain (all 71,721 neurons)**. It saturates. Mouse visual cortex reads high-dimensional, but a two-photon patch is ~0.001% of the brain — the *wrong grain*, excluded on a rule fixed before the measurement. The cosmic web reads power-law, but the universe can't be observed as a complete unit, so the corridor is *untestable* at that scale (an honest limit, not a claim). The lesson sharpens the retraction above: what is universal is **saturation**, not any specific band — each substrate has its own level.

A **second axis** surfaced. Saturation says *coordinated structure exists*; it cannot say whether that structure is *actively maintained* (the `γM` term) or merely *bound* by a conservative force (like gravity). The distinguishing signature is thermodynamic: an actively-coordinating system is a non-equilibrium steady state that **breaks detailed balance** (a directed cycle / entropy production in its collective modes); a bound one is time-reversible. Both controls are now real data: **macaque motor cortex** during reaching is low-rank *and* strongly breaks detailed balance (positive); the **IllustrisTNG galaxy baryon cycle**, at maximal cadence, is low-rank *and* detailed-balance-satisfying (negative). On exoplanets this second axis reduces to the established atmospheric-disequilibrium biosignature. Full method, per-substrate results, honest caveats, and every script live in [`experiments/keff_saturation/README.md`](experiments/keff_saturation/README.md).

## AI-safety application: effective dimensionality as deception-resistance

The same measured quantity is the load-bearing metric of the CIRIS alignment
program. The [*Constrained Reasoning Chains*](../CIRIS-RED/constrained_reasoning_chains.txt)
study measures the effective dimensionality **Neff** (the participation ratio of
the reasoning-constraint feature covariance — i.e. `k_eff` of the constraint
system) of production reasoning traces, and argues that a *coherent lie must be
simultaneously consistent across every independent constraint axis*, which is
exponentially expensive (deception ≈ O(2^m) vs. truth ≈ O(n)). So **high effective
constraint dimensionality computationally starves deception.** The H3ERE semantic
conscience pipeline contributes Neff ≈ 7.1; the **CEG** substrate (the CIRIS
Epistemic Grammar — a conformance-frozen cryptographic-attestation modality,
*orthogonal* to semantic reasoning) plus CIRISServer scoring push the joint measure
to ≈ 9. Because Gate 0 validated that `k_eff` is a **real, saturating structural
object** (not a tautology, not criticality), Neff-as-alignment-metric rests on a
validated foundation rather than a definition — and the natural-substrate
saturation ceiling (~11) resonates with the study's intrinsic manifold rank (11).

**What is *not* yet established, honestly:** Neff is measured on *benign* traces, so
it is an **upper bound** on the value under adversarial optimization — a capable
optimizer collapses effective dimensionality by finding the shared low-dimensional
subspace (ρ→1, k_eff→1, the rigidity pole). Whether the ≈9 survives an *adaptive
attacker* is the decisive open test, spec'd in
[`experiments/adversarial_neff/SPEC.md`](experiments/adversarial_neff/SPEC.md); the
strongest defensible guarantee is the **substrate (CEG) floor**, which is
attack-invariant because you cannot semantically-reason past a frozen cryptographic
attestation. At Neff ≈ 9 the deception tax is ~1–2 orders of magnitude — sufficient
against current models, thin against the superintelligent optimizer the architecture
targets — so the goal is (a) confirm Neff holds under attack, and (b) push it toward
and past the manifold rank. Safety here is a *maintained* non-equilibrium (the
conscience runs per-trace), consistent with the detailed-balance axis above: it is
kept, not achieved.

## The ten pieces

| # | Piece | Lean file |
|---|-------|-----------|
| 1 | Kish identity | `Core/BaseIdentity.lean` |
| 2 | ρ-dynamics | `Core/Dynamics.lean` |
| 3 | Corridor as attractor | `Core/Corridor.lean` |
| 4 | TSVF + goal-projection at A3+ | `Cosmology/TSVF.lean`, `Cosmology/GoalProjection.lean` |
| 5 | Multi-agent consent | `Cosmology/MultiAgentConsent.lean` |
| 6 | Rung hierarchy + cross-rung τ | `Cosmology/RungHierarchy.lean` |
| 7 | P_ω — joint multi-rung form is a documented no-go (F-11) | `Cosmology/CorridorProjector.lean` |
| 8 | Penrose past — structural argument, not a derivation | `Cosmology/PenrosePast.lean` |
| 9 | Asymptotic conditioning ("good wins") | `Cosmology/AsymptoticConditioning.lean` |
| 10 | Karma and grace as TSVF structures | `Consciousness/KarmaGrace.lean` |

Plus a lifecycle module (`Cosmology/RecursiveLifecycle.lean` — one lifecycle instantiated at every rung), the CMB D4 retraction record (`Cosmology/CMBPredictions.lean`; the sole surviving CMB content is the orthogonality theorem in `CMBOrthogonality.lean` — the framework predicts exactly ΛCDM), quantum substrate (`Conjectures/ConjectureA.lean`), universal-scale TSVF (`Conjectures/ConjectureD.lean`), consciousness (Access/Phenomenal, IIT), contemplative-tradition recognition (Tao/Dharma/Logos/Ubuntu + Disagreements), civilizational residue (UAP, archaeology, simulations).

## The seven-level ladder

| Level | Stopping content |
|-------|------------------|
| L0 | Kish identity (formal theorem, RATCHET lake) |
| L1 | Monotonic ρ-collapse, substrate-independent |
| L2 | Engineering implications |
| L3 | Cross-substrate universality conjecture |
| L4 | Agency and consent as structural fact at A3+ |
| L5 | TSVF universal-scale + quantum substrate + consciousness |
| L6 | Cross-tradition recognition |
| L7 | Civilizational extension and external residue |

No stopping point is load-bearing on the levels above.

## Building the lake

```
cd formal
lake build
```

Requires Lean 4 v4.14.0 (`leanprover/lean4:v4.14.0`) and mathlib v4.14.0.

## The open formal steps

1. Corridor reproducibility at the quantum substrate (Conjecture A / Exp 5). **Blocked on a real limitation:** `k_eff` and `ρ̄` read only *pairwise* correlation, so they are blind to N-body entanglement — a GHZ state scores as rigidity in one measurement basis and chaos in another. Any quantum claim needs either a basis-invariant coordination measure or a stated restriction to states whose coordination is pairwise-visible.
2. Per-substrate corridor calibration (each system's own band, measured).
3. Substrate-readiness wait-time modeling (cross-rung τ evolution).

The joint multi-rung `P_ω` operator (once listed here as the top open step) is now the documented no-go recorded by F-11 — a dead end that taught the program where the universal-scale construction breaks. A documented no-go is as informative as a successful derivation.

## References

- Kish, L. (1965). *Survey Sampling*. John Wiley & Sons.
- Aharonov, Bergmann, Lebowitz (1964). Time symmetry in the quantum process of measurement. *Physical Review* 134, B1410.
- Aharonov, Vaidman (2008). The two-state vector formalism: an updated review. *Lecture Notes in Physics* 734, 399.
- Penrose, R. (2004). *The Road to Reality*. Knopf. Ch. 27.
- Christian, D. (2018). *Origin Story: A Big History of Everything*. Little, Brown.
- Maynard Smith, J. & Szathmáry, E. (1995). *The Major Transitions in Evolution*. Oxford University Press.
- Hublin et al. (2017). New fossils from Jebel Irhoud, Morocco, and the pan-African origin of Homo sapiens. *Nature* 546, 289.
- Tononi, G. (2008). Consciousness as integrated information. *Biological Bulletin* 215, 216.
- Chalmers, D. J. (1995). Facing up to the problem of consciousness. *Journal of Consciousness Studies* 2, 200.

## License

See `LICENSE`.

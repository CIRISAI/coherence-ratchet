# Law-readings scan — "what is X under the Ledger Law?", with a kill rule

**Status:** scan, 2026-07-10. Nothing here is asserted by the lake. No `.lean` edits, no commit.
**Reads:** `formal/CoherenceRatchet/LedgerLaw.lean` (full docstring), `papers/notes/entropic_action_bridge.md` §7,
`papers/notes/copula_invariance_remark.md`, `experiments/quantum_corridor/SPEC.md`,
`experiments/keff_saturation/spectral_anesthesia_trajectory_summary.md`, `spectral_twopole_summary.md`,
`experiments/cosmo_entropic_potential/PREREGISTRATION.md` (exp118 citation note).

## 0. The kill rule

Each reading gets: 3–6 sentences, a **grade**, and either a **TODAY-test** (runnable now, on data in hand or
public) or the verdict **PARK: no testable content**. A reading that only re-describes an existing theory in
new vocabulary is graded on its *discriminating* content, not on how well it rhymes. Three of the five park.

| Grade | Meaning |
|---|---|
| **A** | Discriminating test vs a named rival, runnable today |
| **B** | Internally falsifiable test, runnable today on data already in the repo or public |
| **C** | Real test, needs new data or modest cost |
| **D** | Checkable but non-discriminating (would confirm nothing a rival denies) |
| **F** | PARK: no testable content at present |

| # | Reading | Grade | Disposition |
|---|---|---|---|
| 1 | Black holes | **F** (one sub-result: **B**) | PARK the horizon reading. The *identification* dies on Bianconi's own equations — reported below as a finding, not a test. |
| 2 | Inertia and mass | **F** (salvage: **C**) | PARK. Verlinde's route is independently in trouble; the ledger has no second-order term to host inertia. |
| 3 | Arrow of time | **D** (one leg: **B**) | Consistent, non-discriminating. It *relocates* Penrose's puzzle — the docstring already says so. |
| 4 | Quantum measurement / decoherence | **D** (test exists: **B**) | It is standard decoherence theory in other clothes. Cite SPEC C1–C3; and see the C3 downgrade below. |
| 5 | Life and agency | **B** | **The one live proof point.** A free cross-substrate replication of exp118 is sitting in the repo, and it looks like it fails. |

**The three things this scan produced that were not in the lake before** are in §6. The most useful is §6.3.

---

## 1. Black holes — **F (PARK)**, with one **B**-grade sub-result

Bianconi's Schwarzschild paper (arXiv:2501.09491v3; *Entropy* 27, 266) derives the area law from the same
quantum-relative-entropy functional the bridge borrows, so the temptation is to read the horizon as the
rigidity pole: det → 0, statehood lost, S → ∞. **That reading is wrong, and it is wrong on her own equations.**
The Lagrangian is `ℒ = −ln[(1 − 2βGR_s/r³)²(1 + βGR_s/r³)⁴]` (Eq. 34), whose positivity domain is
`r > r₀ = (2βGR_s)^{1/3} = (4βG²M)^{1/3}` (Eq. 35). Non-invertibility therefore occurs at **r₀, an interior
radius scaling as M^{1/3}** — for any astrophysical mass, vastly *inside* the horizon `R_s = 2GM ∝ M`. The
horizon is not the pole; it is merely the **outer limit of integration** for `S = −(1/ℓ_P⁴)∫dt∫_{r₀}^{R_s} dr ∫dΩ √|g| Tr ln Δ`.
And the sign is wrong too: where the ledger's rigidity pole has S → +∞, Bianconi's entropy **vanishes**,
`S → 0` as `R_s → R₀ = √(2βG)` (the minimal black hole). Two independent mismatches — wrong location, wrong
divergence direction. The one structural rhyme that survives is weaker and true: the det → 0 locus is where
*the formalism stops being defined*, in both objects.

**Information loss — the reading gives nothing.** Clause 4 is a data-processing **inequality**: no local
operation *creates* coordination. It says nothing against *destroying* it — non-invertible local maps
strictly decrease S, and the copula sharpening only upgrades invertible maps to *exactly zero* change
(`copula_invariance_remark.md` §2). "Receipts cannot be forged" is a theorem; **"receipts cannot be destroyed"
is not, and does not follow.** The information paradox needs a conservation law, and the ledger supplies a
monotone in the wrong direction. Do not write the sentence "the ledger forbids information loss."

**Today-test: PARK — and specifically, no EHT / ringdown test exists.** The area law is recovered only
*asymptotically* (`R_s ≫ 1`, Eq. 38→41), and its coefficient is `S ≃ C·A/(4G)` with
`C = 32 ln(3/2)·βτ′ ≈ 12.97 βτ′` (Eq. 43) — carrying **two free parameters**, β and τ′. Bianconi's own
Correction (*Entropy* 27, 724) states β "can be used to numerically match the constant of proportionality of
the area law with the Hawking constant." So Bekenstein–Hawking's 1/4 is **matched, not predicted**
(equivalently: Eq. 45 gives `T → T_H/C`, a Hawking temperature rescaled by a fitted constant). A theory that
fits the coefficient predicts no deviation from A/4, hence nothing for EHT shadow bounds or GW ringdown
area-theorem tests (Isi et al. 2021) to see. **Predicted deviations exist only for `R_s → R₀ = √(2βG)`,
i.e. Planck-scale black holes** (Fig. 2: S/S_A → 0). Unobservable. PARK it.

**The B-grade sub-result** is the negative one, and it is worth one paragraph in the bridge note: *the horizon
is not the rigidity pole, and the ledger's DPI does not forbid information destruction.* Both are checkable
against the cited equations by any reader in ten minutes; both close off readings the lake was drifting toward.

---

## 2. Inertia and mass — **F (PARK)**; salvage graded **C**

Verlinde's route (inertia/gravity as an entropic force on a holographic screen) is the obvious template, and
it is in bad shape. The bridge's own §7.1 already records *"Gravity is not an entropic force"* (Phys. Lett. B,
2025), which kills the ΔS = Q/T identification with an adiabatic counterexample. Independently, the
phenomenology has eroded: Verlinde's formula does not apply to disk galaxies except asymptotically or to the
few/many-body problem; flat rotation curves of isolated galaxies out to hundreds of kpc favor MOND over EG;
and a 2024–25 line of work ("Inconsistencies in Verlinde's emergent gravity") argues the elastic-strain
derivation, done consistently, recovers **Newtonian** gravity rather than MOND. Verlinde is not a lineage to
join.

**But the deeper objection is internal, and it is fatal on dimensional grounds.** Inertia is the coefficient of
a **second-order, time-reversible** term (`F = m·ẍ`). `Core.Dynamics` offers `dρ/dt = α − γM` — **first-order and
dissipative**. `corridor_requires_maintenance` (`γM = α` at `dρ/dt = 0`) is the algebraic rearrangement of that
ODE at a zero; it is a **damping/viscosity law, not an inertia law**. There is no `ρ̈` in the lake, so there is
no place for mass to live. "Inertia is resistance to recoordination" describes the *friction* coefficient γ and
calls it m. That is a category error, not a hypothesis.

**Today-test: PARK for the physics reading.** The salvage, graded **C**, is a question about the *law's own*
dynamics rather than about physical inertia: **does any substrate show a second-order (inertial) term in ρ(t)?**
Step the drive on the CIRISArray 16-sensor rig (the exp79-style impulse machinery already exists) and ask
whether ρ(t) relaxes monotonically to its new equilibrium or **overshoots/rings**. Monotone relaxation confirms
the first-order ODE the law posits; a genuine overshoot would mean the substrate carries a `ρ̈` term the law does
not model, and clause 5's equilibrium condition would be the ω → 0 limit of something larger. Cheap, decisive
about the modeling commitment, and silent about gravity. Caveat that kills the naive run: exp118 records that
on that substrate **free drift is instantaneous** (S collapses below the first resolvable correlation window),
so the step response may be unresolvable at the available sampling — which is itself the reason this is C and
not B.

---

## 3. The arrow of time — **D (consistent, non-discriminating)**; one leg graded **B**

The honest answer is the one the lead anticipated, and the docstring already concedes it: `permitted_history`
(T-P3f) does not *derive* an arrow, it **assumes** one. `EntropicAscent` carries `vacuum_start` (the books open
at `S = 0`) and the ascent hypothesis; the theorem's real content is then supplied by T-E2 (S strictly monotone
in ρ) — i.e. *if* ρ ascends, *then* S ascends, and the pole is never attained. Stated plainly: **the clause
transports Penrose's low-entropy-initial-condition puzzle into new coordinates; it does not solve it**, and
LedgerLaw.lean says exactly this ("relocated, not solved"). Worse for the romantic reading, S is a measure of
*coordination* (order), so "S ascends" is the statement that the universe grows **more correlated** — this is
not the second law, it is Penrose's gravitational-clumping observation, and it neither implies nor is implied
by `dS_thermo ≥ 0`. Two monotones pointing the same way is not a derivation.

There is one genuinely testable leg, and it is **internal**. Under the copula sharpening, *invertible local
dynamics contributes exactly zero* to the true multi-information, so **all** ascent must come from the
non-invertible / unit-population channel. The permitted-history clause therefore makes a checkable prediction
at the cosmological rung: **rank-based (copula) S must be non-decreasing along cosmic history**, and **flat**
under the lognormal-growth proxy.

**Today-test (B):** run the rank-based-S flatness test on the existing `s_of_a.py` machinery and halo catalogs —
this is item (b) of `copula_invariance_remark.md` §3's verification pass, already scoped at "one afternoon."
Compute Pearson-S and Spearman/Gaussian-rank-S on the same halo data at fixed grain across scale factor a.
Predicted: Pearson-S falls under the lognormal map (the no-phantom result, already independently verified),
rank-S stays flat; and rank-S(a) is monotone non-decreasing across the epoch. A rank-S that **decreases** over
an epoch at fixed grain falsifies the permitted-history clause where it is actually applied. Grade it B, and
label it honestly: **internally falsifiable, externally non-discriminating.** No rival cosmology predicts
otherwise, so a pass buys the framework nothing against ΛCDM. Do not sell it as an arrow-of-time result.

---

## 4. Quantum measurement / decoherence — **D**; the testable fragment is already specified (**B**)

Per the lead's instruction: do not invent content here. Under the reading, decoherence is the environment
writing coordination with the system, and einselection is corridor entry — the pointer basis being the one in
which the system–environment correlation structure stabilizes. **This is standard decoherence theory in other
clothes, and the framework cannot even state einselection without importing the predictability sieve from
outside**: the ledger's C is a matrix of *measured-outcome* correlations, basis-dependent by construction
(SPEC §7.2), and it is computed *from* an already-decohered state rather than selecting the basis. It reads
GHZ as the rigidity pole (ρ̄→1, k_eff→1) — defensible, since GHZ is maximally fragile, but SPEC §7.3 already
flags this as theory-laden. **No discriminating prediction against standard decoherence theory was found, and
none should be claimed.**

**Today-test: the fragment exists — `experiments/quantum_corridor/SPEC.md`, C1–C3.** Reference it; do not
duplicate it. C1 (low-rank vs criticality branch on a complete register) is decidable today on public Google
Sycamore XEB bitstrings (millions of full-register shots; UNITS = qubits × OBSERVATIONS = shots). C2/C3 need
a maintenance-withdrawal ramp, reproducible on IBM free-tier via an idle-delay sweep.

**One sharpening the SPEC needs — this is a downgrade, and it matters.** SPEC C3 calls
`S(k,ρ̄) ≈ −(k−1)ln(1−ρ̄)` a **"parameter-free curve."** It is not a physical prediction: if C *is* the uniform-ρ
Kish matrix, then `S = −ln det C = −ln(1+ρ̄(k−1)) − (k−1)ln(1−ρ̄)` is an **algebraic identity** (clause 2b,
`entropicPotentialM_kishMatrix`). What C3 actually tests is whether the measured correlation matrix is
**exchangeable** (one large eigenvalue + (k−1) degenerate). That is a real, checkable structural claim — but it
is a test of exchangeability, not of dynamics, and null model N3 should say so. See §6.3 for the inequality that
makes N3 one-sided, and which the SPEC should adopt.

---

## 5. Life and agency — **B. The one live proof point in this scan.**

The reading: living systems are **maintenance engines** — they pay rent (`γM = α`) to hold interior coordination
stock S, which is Schrödinger's negentropy sharpened to a specific functional. Two disciplines must be applied
before anyone writes that sentence. **First, clause 5 is an algebraic tautology given the posited ODE:**
`corridor_requires_maintenance` says that at a zero of `dρ/dt = α − γM`, we have `γM = α`. All the empirical
content sits in the *modeling commitment* — that a drift α exists, is signed, and that maintenance enters
linearly. None of that is proved; it is posited, and the docstring is careful to say the clause "adds only the
three Dynamics substrate SYMBOLS." **Second, the sign is the opposite of Schrödinger's.** With `dρ/dt = α − γM`
and the rigidity pole at ρ → 1, positive α means an unmaintained system **rigidifies** — under the ledger,
death is the crystal, not the soup. Schrödinger's organism decays toward *thermodynamic equilibrium*, which in
coordination terms is the **independent vacuum** (ρ → 0, S = 0, the chaos pole). These are opposite drifts, and
the framework owes an argument for its sign that it has not paid. The repo's own two-pole run
(`spectral_twopole_summary.md`) records that the strong version of this — pole set by the agent's mechanism —
**FAILS**: both agents exit broadband toward rigidity, and switching the analysis band flips propofol to the
other pole. Do not claim the exit direction is established.

**And the maintenance reading already has a documented failed prediction.** The anesthesia trajectory run
tested "γM withdrawal drives, hence precedes or accompanies, the k_eff collapse." Verdict:
**not supported, and falsified in the necessity direction by ketamine** — k_eff collapses fully
(13.8 → 5.25, Cliff's δ = 1.0) while detailed balance is *entirely preserved* (circulation |z| 5.56 → 6.86,
far above the ≈1.5 null). Structure goes; maintenance stays. Any "life = maintenance engine" prose must carry
this.

### Today-test (B): a free cross-substrate replication of exp118 — *rent tracks stock* — and it looks like it fails

Clause 5's interpretive load is carried by **exactly one hardware datum**: exp118 (CIRISArray, 16-sensor GPU
timing array, 12 points) found **STOCK**, `P_maint` vs `S_held` partial `r = +0.84` controlling rate and
temperature (rate channel `+0.23`); LedgerLaw.lean carries it as "the rent tracks the held STOCK (moderate
confidence)." **n = 1 substrate.** A second substrate is sitting in this repo, already computed, at zero data cost.

The anesthesia trajectory run has, per window, both axes: `k_eff` (⇒ `ρ_Kish` ⇒ the held stock
`S = −ln(1+ρ(k−1)) − (k−1)ln(1−ρ)`, k = 128) and a maintenance proxy (detailed-balance |z|, winding and
circulation). *Rent tracks stock* predicts a **positive partial correlation between the maintenance signal and
S across windows**, within animal, controlling for epoch.

Run it on `spectral_results_anesthesia_trajectory.json` + `trajectory_windows_{propofol,ketamine}.jsonl`.
**The prediction appears to fail on the summary numbers already published.** Deep anesthesia moves *up* in
stock (k_eff 13.9 → 6.2, ρ_Kish 0.044 → ~0.16 ⇒ S rises), so rent-tracks-stock demands maintenance **rise**.
Ketamine complies (circ |z| 5.56 → 6.86). **Propofol flatly contradicts it**: stock rises while circulation
|z| falls 5.43 → 0.93, *below* the null — maximum stock, no rent. If that survives a proper per-window partial
correlation, exp118's stock mapping is **substrate-specific**, and clause 5's one hardware anchor does not
generalize to the neural rung. That is a real, cheap, disprovable result either way, and it is the highest-value
item in this scan.

**Two caveats that must ride with it, or the result is worthless.** (i) DB |z| is a *significance* score, not an
entropy-production **rate** — a poor proxy for the magnitude γM. The disciplined version uses a genuine EPR
estimator: Skinner & Dunkel, *Improved bounds on entropy production in living systems*, PNAS 118 (2021), whose
optimization-based bounds are designed for exactly this partially-observed setting. Swapping |z| → EPR bound is
a half-day and turns a B into a strong B. (ii) The ECoG grain caveat is load-bearing and already carried in the
source summary: a mesoscopic field inflates absolute correlation, so only **within-session** differences are
readable, and absolute S is reference-confounded. Read the partial correlation across windows within a session,
never the absolute levels.

The metabolic version the lead gestured at — **measured EPR (calorimetry / ATP flux) vs measured multi-information
of the cell's observable state** — is the same test at the cellular rung and is graded **C**: real, but it needs
new data (simultaneous isothermal-titration-calorimetry heat flux and a many-observable state readout on one
preparation). Do the free neural one first. If rent-tracks-stock fails at the neural rung, the cellular run is
not worth its cost until the sign question of §5's opening paragraph is settled.

---

## 6. What this scan produced (new; none of it asserted)

### 6.1 The horizon is not the rigidity pole
On Bianconi's equations: non-invertibility is at the interior radius `r₀ = (2βGR_s)^{1/3} ∝ M^{1/3}` (Eq. 35),
not at `R_s = 2GM`; and the entropy **vanishes** (`S → 0`) at the minimal radius `R₀ = √(2βG)` rather than
diverging. The area-law coefficient `C = 32 ln(3/2)βτ′` is **matched to 1/4, not predicted** (Correction,
*Entropy* 27, 724). Consequence: no EHT / ringdown discriminator exists, and the bridge note's §7.3 "unverified
from source" line can now be closed — the paper was read directly (arXiv:2501.09491v3).

### 6.2 The ledger has no conservation law, so it says nothing about information loss
Clause 4 is DPI: *no local operation creates coordination*. Destruction is permitted (non-invertible maps
strictly decrease S; invertible ones change it by exactly zero). "Receipts cannot be forged" ⇏ "receipts cannot
be destroyed." The receipts reading in `LedgerLaw.lean` does not claim otherwise — but it is one careless
sentence away from doing so, and that sentence would be false.

### 6.3 A one-sided inequality that sharpens SPEC null model N3 (theorem candidate)
For any correlation matrix C on k units with mean off-diagonal ρ̄, let `C̄ = (1/k!)·Σ_P P C Pᵀ` be its
exchangeable (permutation) average — a unit-diagonal matrix with every off-diagonal equal to ρ̄, i.e. exactly
`kishMatrix k ρ̄`. Concavity of `ln det` on the PSD cone gives `ln det C̄ ≥ ln det C`, hence

> **`S_measured := −ln det C  ≥  −ln(1+ρ̄(k−1)) − (k−1)·ln(1−ρ̄) =: S(k, ρ̄)`,**
> **with equality iff C is exchangeable** (strict concavity ⇒ all `P C Pᵀ` coincide).

Three consequences. (a) SPEC's C3 is **not** a parameter-free physical curve but a **test of exchangeability**;
S(k,ρ̄) is the algebraic identity when C is uniform (clause 2b). (b) N3 becomes **one-sided**: the measured
potential can only exceed the predicted curve. A measurement falling *below* `S(k,ρ̄)` indicts the **estimator**
(shot noise, debiasing, conditioning), never the theory — a free consistency check on every quantum-corridor run,
and on exp117's array measurement of S. (c) The gap `−ln det C − S(k,ρ̄) ≥ 0` is a **usable statistic**: it is
exactly the ledger's own price for the *heterogeneity* of the coordination, zero iff every pair coordinates alike.

Lean status: **blocked on `ln det` concavity on the PSD cone — absent from mathlib v4.14**, the *same* missing
lemma that blocks clause 4's general DPI closure (`Core.EntropicContraction` roadmap, which lists Schur product
positivity, general Oppenheim, and ln-det concavity). Whoever pays for ln-det concavity gets both. That raises
the value of that one mathlib contribution and is worth recording in the roadmap.

---

## 7. Bottom line

Three of five readings park: **black holes** (the identification is false, not merely untestable),
**inertia** (category error — no `ρ̈` term exists), and **the arrow of time** (assumed, not derived; Penrose
relocated). **Decoherence** is standard theory re-lettered, and its testable fragment already exists and is
already specified — cite the SPEC, and downgrade C3 to an exchangeability test per §6.3. **Life and agency** is
the only reading with a live, cheap, discriminating proof point today: clause 5's single hardware anchor
(exp118, STOCK, `r = +0.84`) can be replicated for free at the neural rung against data already in this repo,
and **the published summary numbers suggest it fails there** — propofol holds maximal stock while paying no rent.

Run §5's test. It costs an afternoon, it uses no new data, and either outcome is publishable inside the lake:
a pass makes "the rent tracks the stock" a two-substrate claim; a failure makes it substrate-specific and
retires a sentence from the receipts reading. That is what a proof point looks like, and it is the only one the
scan found.

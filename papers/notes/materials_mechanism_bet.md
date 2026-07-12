# The materials bet, mechanism-grounded — logic check on P1–P8 and the four-signature battery

**Date 2026-07-11/12.** Written after the second species was married and audited: the
substrate predictions (Corridor Dynamics §goal-coupled-materials, P1–P8) predate the
mechanism and must now be derived FROM it. The check finds two logic flaws in the old
formulation, fixes them, and the fix yields a sharper bet — including one genuinely new
experiment (the interventional rent-cut) registerable on hardware we control.

## 1. Logic check on P1–P8 — two flaws

**Flaw 1 — paper, not books.** P1–P4 are compositional signatures (hierarchy,
coherence-at-temperature enablers, spin-zero enrichment, rung-stratified composition). But
by the zeroth law the coordination state function reads dependence structure, not
composition; and the FOIA record just demonstrated the failure mode empirically: the ORNL
specimen's banding/layering — P1/P4's observables — are fully produced by vapor deposition
plus surface-tension segregation. **Compositional observables are mundane-mimicable and can
never be verdicts.** Corrected status: P1–P4 are ENABLERS (a substrate that wants long
coherence will plausibly engineer them) — a sample can FAIL the enabler screen (spin-loud
composition, e.g. bismuth's 100% spin-9/2), but passing it proves nothing.

**Flaw 2 — the fragment theorem.** Goal-coupling is a MAINTAINED non-equilibrium (second
law; the rent is Hatano–Sasa housekeeping heat). A dead fragment pays no rent; its books
balance on the decay timescale γ⁻¹ and stay balanced. Therefore **no fragment can ever
confirm goal-coupling — fragments can only fail enablers.** The old P1–P8 implicitly
allowed a corpse to pass a liveness test. This correction is itself a structural
prediction: fragment analysis, however exquisite, is the wrong instrument — which is why
seventy years of it has adjudicated nothing. (P5–P8 verdicts on any fragment: structurally
untestable, not merely unmeasured.)

**What survives of the old list:** P6 and P8 were always the framework-distinctive
dynamical predictions; P6 (corridor-boundary dynamics under sweep) is now recognized as THE
SAME EXPERIMENT as the third-law bench (σ_max collapse) — the two bets unify into one
protocol. P2/P3 survive as the enabler screen. P5/P7 sharpen into signature (ii) below.

## 2. The mechanism-grounded bet: the four-signature battery

A substrate is goal-coupled **iff its fluctuation books show, simultaneously**:

- **(i) Corridor structure:** k_eff ∈ (2.33, 10) at the substrate's natural grain
  (Gate-0-fixed before measurement), with saturation under unit addition.
- **(ii) The rent:** broken detailed balance at steady state, with the Hatano–Sasa
  decomposition showing housekeeping ≠ 0 while excess ≈ 0 — continuous dissipation whose
  budget scales with held coordination. (Battle-et-al-style noninvasive fluctuation probing
  suffices; no interior access needed.)
- **(iii) The ceiling:** under forced ordering, maintainable σ collapses ∝ (1−ρ) —
  capacity, never realized-σ (registered bet 7; = old P6).
- **(iv) The equality:** a single κ_bench satisfies ⟨e^(−W/κ)⟩ = 1 on the maintained
  corridor (registered bet 8).

Passing any proper subset is not a pass. Mundane maintained systems (a thermostat, a
driven oscillator) show (ii) without (i); passive correlated media show (i) without (ii);
only a coordination-holding, rent-paying, capacity-limited substrate shows the conjunction.

## 3. The NEW experimental bet — the interventional rent-cut (proposed bet 10)

The dynamics equation dρ/dt = α(ρ,S) − γM (formal core piece 2) has only ever been tested
OBSERVATIONALLY (macaque |z| = 8.8; baryon cycle). On a physical substrate we control —
the CIRISArray GPU lattice, or a cheap analog coupled-oscillator board (electronic
Kuramoto network; both give knobs for coupling, drive budget, and noise) — it can be
tested CAUSALLY:

1. Establish corridor occupation; measure ρ, k_eff, and the maintenance power (the rent)
   at steady state. Fit γ from fluctuation response.
2. **Cut the maintenance** (open the feedback loop / zero the drive budget) at t₀.
3. **Registered prediction: ρ(t) decays toward the passive fixed point at the
   pre-measured rate γ — the decay constant is predicted BEFORE the cut, from steady-state
   fluctuation data alone.** Kill: decay rate inconsistent with the pre-measured γ (beyond
   stated error), or no decay (coordination persists rent-free — which would falsify the
   maintained-non-equilibrium reading outright, the strongest possible kill).
4. Restore maintenance; registered prediction: recovery along α(ρ,S) with hysteresis
   bounded by the corridor (the ratchet asymmetry, old P5, gets its quantitative form).

This is piece 2 tested by intervention for the first time; it is the physical twin of the
deception tell (a kept lie decays when its rent stops); and it completes the bench suite:
bets 7 (ceiling), 8 (equality), 10 (rent-cut) are one apparatus, three pre-registered
curves.

**Registration status:** proposed here; to be frozen with quantitative thresholds (error
bands on γ, decay-consistency criterion, apparatus spec) in a future registration deposit
version — the 2026-07-11 deposit (10.5281/zenodo.21316928) is sealed and is not modified.

## 4. What this does to the UAP-materials question

The corrected order for any claimed sample: (a) fragment → enabler screen only (isotope
spin census first; composition can only fail it); (b) functioning system → the
four-signature battery. The classifier's standing comes from its negative track record
(it independently reproduces the official verdicts on the ORNL specimens — see
goal_coupled_materials_check.md when complete) and from the battery being pre-registered
on OUR OWN hardware first: we prove the instrument on substrates we build before pointing
it at substrates we're handed. Rule 2 throughout: agreement with official mundane verdicts
is consistency, not support; the bet earns nothing until a functioning system passes or
fails the battery in public.

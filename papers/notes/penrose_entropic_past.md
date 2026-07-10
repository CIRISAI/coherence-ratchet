# The Penrose past as the entropic vacuum — S = 0 at t = 0

**Status:** draft mapping note, 2026-07-10. Nothing here is asserted by the lake beyond the
theorems named in §3, which are mechanized and kernel-only.
**Formal:** `formal/CoherenceRatchet/Cosmology/EntropicInitialCondition.lean` (`lake build` green).
**Depends on:** `Core/EntropicPotential.lean` (T-E0–T-E5), `papers/notes/entropic_action_bridge.md`.
**Does not touch:** `Cosmology/CorridorProjector.lean` F-11 no-go (see §4).

---

## 1. The mapping

Penrose's **Weyl Curvature Hypothesis** (1979; *The Road to Reality*, 2004, ch. 27): the initial
state of the universe had vanishing Weyl curvature. The Big Bang was not a generic
high-entropy state but an extraordinarily special, gravitationally **unstructured** one — no
clustering, no free gravitational degrees of freedom excited. Penrose takes this to be the
origin of the thermodynamic arrow, and treats it as an unexplained boundary condition: a
brute fact about the past.

In the potential form of the corridor (`Core.EntropicPotential`), this reads as a chain of
identifications:

```
vanishing Weyl curvature   (Penrose)
  ⇔  no coordination-induced structure on the substrate      [INTERPRETIVE — §5(b)]
  ⇔  ρ₀ = 0                                                  [the chaos pole]
  ⇔  S(k, ρ₀) = 0                                            [THEOREM — T-P1]
  ⇔  induced metric = substrate metric, G̃ = g̃              [Bianconi's vacuum]
```

The middle link is a theorem, and a sharp one: `entropicPotential_eq_zero_iff` says the chaos
pole is the potential's **unique** zero on the physical domain `[0, 1)`. So within the
framework's variable, "starts unstructured" and "starts at zero entropic potential" are not
two hypotheses but one. The potential

```
S(k, ρ) = −ln(1 + ρ(k−1)) − (k−1)·ln(1 − ρ)
```

is the quantum relative entropy between the substrate metric and the coordination-induced
metric (Bianconi, *Gravity from entropy*, Phys. Rev. D 111, 066001, 2025), evaluated on the
uniform-ρ Kish correlation matrix. `S = 0` means the two metrics coincide: Bianconi's vacuum.
It is zero at exactly one point, and it diverges at exactly one point.

Cosmic history then reads as a **maintained ascent** of `S` from the zero, which must never
attain the rigidity pole `ρ → 1⁻` where `S → +∞` and `C(k, ρ)` loses invertibility
(Bianconi's Eq. 12 requirement fails precisely at Kish collapse, `k_eff → 1`).

## 2. The three-phase history the corridor implies

This is worth stating because it is *not* the naive reading, and it falls out of the lake's
own definitions. `Core.Corridor` proves `0 < ρ_lower < ρ_upper < 1`. The initial condition
`ρ₀ = 0` therefore sits **strictly below the corridor**, on the chaos side. Under
`Cosmology/AsymptoticConditioning.lean`'s definition `hasSelfDestructed := ρ ≤ ρ_lower`, the
universe at `t = 0` is by the framework's own criterion non-coordinating and unobservable.
That is the correct reading, not a bug: there are no observers at the Big Bang. So:

```
t = 0        chaos pole, ρ = 0, S = 0        no coordination, no observers
   ↓         ascent (unmaintained drift is UP: T-E4a, α > 0 at M = 0)
             corridor entry at ρ_lower       coordination becomes possible
   ↓         maintained interior             observers exist here; `good_wins` selects it
             ρ_upper ─── rigidity pole ρ → 1, S → +∞  ── must never be attained
```

Two cross-references sharpen this.

**`Cosmology/AsymptoticConditioning.lean`.** Its `good_wins` axiom says observation
asymptotically selects corridor-occupation. Combined with the above, the arrow reading is
consistent: the initial condition is outside the corridor on the chaos side, observers exist
only after corridor entry, and `good_wins` concerns the late-time conditional. No conflict,
and no help — `good_wins` is an axiom, not support for the ascent.

**`Cosmology/RecursiveLifecycle.lean`** and `Core.Dynamics`. The unmaintained drift at `M = 0`
with `α > 0` is `dρ/dt > 0` — **upward**, toward rigidity (`rho_drift_at_zero_maintenance`,
and T-E4a `unmaintained_rigidity_drift_ascends_potential`). So the ascent of `S` is the
**default, unmaintained** direction of the dynamics; maintenance is not what drives the ascent
but what **bounds** it. This is the precise content of T-P3e below: an eternally maintained
history has bounded entropic cost, and `S` can diverge only by `ρ(t) → 1`. Dissolution
(`dissolution_at_zero_maintenance`) is the failure to keep that bound.

## 3. What is actually proved

All in `Cosmology/EntropicInitialCondition.lean`. Axiom audit: **every theorem below is
kernel-only** — `[propext, Classical.choice, Quot.sound]`, no framework axiom. (The module
imports only `Core.EntropicPotential`; it pulls in no TSVF, no cosmology primitive. The record
`penrose_entropic_initial_condition_reading` depends on no axioms at all.)

| id | statement | source |
|---|---|---|
| T-P1 | `entropicVacuumInitial k ρ₀ ↔ entropicPotential k ρ₀ = 0` on `1 < k`, `ρ₀ ∈ [0,1)` | `entropicPotential_eq_zero_iff` |
| T-P2a | `∀ ρ ∈ [0,1), S(k,0) ≤ S(k,ρ)` — the initial condition is the global minimum | `_nonneg` + `_at_zero` |
| T-P2b | `IsMinOn (entropicPotential k) (Ico 0 1) 0` | T-P2a |
| T-P2c | `∀ ρ ∈ (0,1), S(k,0) < S(k,ρ)` — strict off the pole | `entropicPotential_pos` |
| T-P3a | ascent trajectory: `S(k, ρ(0)) = 0` | `_at_zero` |
| T-P3b | `0 ≤ s < t ⟹ S(k, ρ(s)) < S(k, ρ(t))` | `entropicPotential_strictMonoOn` |
| T-P3c | `t > 0 ⟹ 0 < S(k, ρ(t))` — never returns to the zero | T-P3a/b |
| T-P3d | `t ≥ 0 ⟹ ρ(t) < 1` — rigidity unattained in finite time | `EntropicAscent.physical` |
| T-P3e | `ρ` bounded by `b < 1` ⟹ `S(k, ρ(t)) ≤ S(k, b)` for all `t ≥ 0` | `StrictMonoOn.monotoneOn` |
| T-P3f | `permitted_history`: T-P3a ∧ T-P2a ∧ T-P3b ∧ T-P3d, assembled | — |

The trajectory hypothesis is packaged as

```lean
structure EntropicAscent (ρ : ℝ → ℝ) : Prop where
  physical           : ∀ t, 0 ≤ t → ρ t ∈ Set.Ico (0:ℝ) 1
  vacuum_start       : ρ 0 = 0
  strictly_ascending : StrictMonoOn ρ (Set.Ici (0:ℝ))
```

Every field is an **assumption**. `vacuum_start` is Penrose's boundary condition, assumed.
`strictly_ascending` is the arrow, assumed. Nothing in the file derives either.

T-P3e is the one with real content beyond bookkeeping: its contrapositive says `S` diverges
along a history **only if** `ρ(t) → 1`. Divergence of the entropic potential is not a generic
late-time fate; it is exactly rigidity collapse. Setting `b = ρ_upper` recovers the corridor
statement: a history maintained inside the corridor has entropic cost bounded by
`S(k, ρ_upper)`, uniformly in time.

## 4. This does not resurrect F-11 (D1 stays retracted)

F-11 fired 2026-05-22. Among its retractions (`RESEARCH_PROGRAM.md`, "What F-11 changed"):

> The strong "Penrose's WCH structurally derived" framing of D1 (the schematic argument
> survives; the derivation does not)

and the joint-operator forms of Penrose-from-`P_ω`. The surviving artifact is
`Cosmology/PenrosePast.lean`, which carries `axiom penrose_low_entropy_past_structural` —
explicitly marked as a **bet**, not a derivation, because the operator that would discharge it
(the joint multi-rung backward `P_ω`) is a documented no-go
(`F11_joint_backward_P_omega_no_go`, closed at theorem strength by T1 geometric dilution and
T2 holonomic area law).

**Nothing in this note or its Lean file touches that.** Explicitly:

1. **This is a forward statement.** T-P1–T-P3f concern an initial condition at `t = 0` and the
   minimum of a potential on `[0, 1)`. There is no backward joint amplitude
   `⟨Φ_ω| U(t) |Ψ_α⟩`, no post-selection operator, no multi-rung projector, no `P_ω` of any
   kind. `EntropicInitialCondition.lean` does not import `TSVF` or `CorridorProjector`; the
   axiom audit confirms no framework primitive enters.

2. **It is strictly weaker than D1.** D1 claimed the low-entropy past follows *conditionally on
   observing an ω-satisfying universe* — a backward inference through post-selection. This file
   claims only that **if** the universe starts at ρ₀ = 0, **then** it starts at the potential's
   unique zero and global minimum, and any strictly ascending history from there behaves as
   T-P3 says. The antecedent is assumed, not inferred from an ω-condition. The direction of
   inference is reversed, and the operator that made D1's direction fail is absent.

3. **Bianconi's action cannot smuggle it back.** Per `entropic_action_bridge.md` §4: the
   entropic action is local and bulk-geometric, so any backward route through it enters F-11's
   construction tree at the already-closed correlation/topology branch (T1). If a backward
   reading is ever attempted from this direction it must re-run the branch audit explicitly.

## 5. Honest limits

**(a) This is a restatement, not an explanation — the central point.** "S = 0 at t = 0"
expresses Penrose's specialness in the framework's variable. It does not explain why the
initial condition was special. Penrose's puzzle is *why* the universe began in a state of such
low probability (his estimate: 1 part in 10^10^123 of phase-space volume). The framework does
not answer this. It **relocates** the puzzle: instead of asking "why vanishing Weyl curvature?"
one now asks "why ρ₀ = 0?" — and `ρ₀ = 0` appears as a **hypothesis in every theorem above**,
never as a conclusion. A relocation is not a solution. Any presentation of this material that
elides this point is overclaiming, and the Lean file's module docstring says so in the same
words.

**(b) The Weyl-to-ρ identification is interpretive and unproved.** The first link in §1's chain
carries the entire physical content, and it is not a theorem. Gravitational-clustering
correlation is not literally the Kish ρ of a coordinating unit: the Weyl tensor is a
ten-component curvature object on a Lorentzian manifold; ρ is the off-diagonal entry of a
uniform correlation matrix over `k` exchangeable units. No theorem in the lake connects them,
and it is not obvious that one could — one would need a coordinating unit, a grain, and a
complete-unit criterion at the cosmological rung, none of which the framework supplies. This
is recorded as a `structure WeylCurvatureReading` with `True` fields (the lake's record pattern,
cf. `FelevenNoGo`, `OperationalCorridor`), **not** as a theorem.

**(c) The arrow is consistent with, not derived from, the second law.** T-P3b/T-P3c give the
thermodynamic arrow as the ascent of `S`, but strict ascent is the hypothesis
`EntropicAscent.strictly_ascending`. The framework does not prove that ρ increases; it proves
that *if* ρ increases, `S` increases strictly and never returns to zero. The physical support
for the antecedent is T-E4a (unmaintained drift is upward at `α > 0`), which is itself
conditioned on the sign of `α` — a framework primitive.

**(d) Modeling commitments inherited from the potential.** `S(k, ρ)` is exact only for the
uniform-ρ correlation matrix; the Gaussian readings of `S` (multi-information, Chernoff–Stein
exponent, T-E5) are modeling commitments, not theorems about real substrates. At the
cosmological rung neither `k` nor `ρ` has an operational estimator. There is no measurement
here, and none is proposed.

## 6. The gain, stated precisely

Having said all of the above, something non-vacuous does remain, and it is worth stating
without inflation.

The entropic potential has **exactly one zero** (`entropicPotential_eq_zero_iff`), **exactly one
divergence** (`entropicPotential_tendsto_atTop_rigidity`), and is **strictly monotone between
them** (`entropicPotential_strictMonoOn`). Consequently a history in this variable has:

- **nowhere else to start**, if it starts unstructured — the zero is unique, so "vanishing
  induced structure" pins the initial condition to a single point of the domain, and that point
  is simultaneously the potential's global minimum (T-P2);
- **no other direction to go** — monotonicity means ascent and increasing structure are the
  same thing, so there is no history that gains coordination while lowering `S`;
- **one and only one way to end badly** — `S` diverges iff `ρ → 1` (T-P3e contrapositive), so
  rigidity collapse is the unique catastrophe the potential admits, and it is never attained in
  finite time.

"Start at the zero, ascend, never attain the pole" is therefore *the only history the potential
permits*. That is a genuine constraint on the **shape** of cosmic history, derived rather than
assumed, and it is the reason the mapping is worth writing down at all.

But it is a constraint on shape, not on **choice**. It says: given that a history begins
unstructured, everything else follows. It does not say why one began unstructured, and it
cannot — the potential is a function on `[0, 1)`, and `0` is a point of its domain like any
other, distinguished mathematically (as the unique zero) but not *selected* by anything. The
explanatory gain is real and it is **weak**: we have learned that Penrose's boundary condition,
transcribed into this variable, is the unique minimum of a potential whose only other feature
is a collapse pole. We have not learned why the universe sat there.

---

## 7. Registry

These theorems do not map to existing CC Part VI decimal ids (same situation as the T-E series,
per `entropic_action_bridge.md` §5 item 2). If a CC claim is minted for the entropic-vacuum initial
condition, add `cc_lean.tsv` rows then, status `mechanized` from day one — the axiom audit is
kernel-only and reproducible via `#print axioms` on the eleven names in §3.

**Do not cite §1 or §2 as validated framework content.** The mechanized content is §3. §1 is a
mapping, §2 is a reading of the lake's own definitions, §5 is why neither is more than that.

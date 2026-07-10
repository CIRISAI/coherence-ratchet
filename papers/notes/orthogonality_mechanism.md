# Orthogonality as a linearization limit — fence or mechanism?

**Status:** draft, 2026-07-10. Mechanized content is in
`formal/CoherenceRatchet/Cosmology/EntropicLinearization.lean` (`lake build` green, axiom audit
below). The reading around it is interpretation and is labelled as such.

**F-11 compliance, stated up front.** Everything here is **forward** content: the forward soft
`P_ω` (the ρ_ss steady state) and the entropic potential `S(k, ρ)`. Nothing below uses, needs, or
resurrects the joint multi-rung backward `P_ω`, D4, or F-19. Bianconi's action is a *local,
bulk-geometric, forward variational principle*; per `entropic_action_bridge.md` §4 it enters the
F-11 construction tree at the already-closed correlation/topology branch (T1, geometric dilution).
The no-go (`CorridorProjector.F11_joint_backward_P_omega_no_go`) stands untouched.

**Depends on:** `papers/notes/entropic_action_bridge.md` (§1 Bianconi's Eqs. 45–47, §4 the F-11
fence, §7.2 the Hamiltonian/Λ^G reading); `formal/CoherenceRatchet/Core/EntropicPotential.lean`
(T-E0–T-E5); `formal/CoherenceRatchet/CMBOrthogonality.lean`.
**Sibling note, reached independently and agreeing:** `papers/notes/lambda_maintenance_wz.md` §7(e).

---

## 1. The honest formal question, asked first

The thesis handed to this note was: *Bianconi's entropic action reduces exactly to
Einstein–Hilbert with zero Λ at low coupling; the lake's orthogonality theorem says the framework's
CMB power spectrum equals ΛCDM's exactly; these are the same statement, so the orthogonality fence
is really a mechanism.*

Before developing it, read what `CMBOrthogonality.lean` actually proves. The theorem is:

```lean
theorem framework_cmb_power_eq_lcdm {Ω : Type*}
    (E : (Ω → ℝ) → ℝ) (w S : Ω → ℝ)
    (indep : E (fun x => w x * S x) = E w * E S) (hw : E w ≠ 0) :
    E (fun x => w x * S x) / E w = E S
```

Three observations, all of which constrain what may be claimed:

1. **`E` is an arbitrary functional `(Ω → ℝ) → ℝ`.** It is not assumed linear, positive,
   normalized, or an expectation of any kind. `w` and `S` are arbitrary functions. The proof is
   one line of field algebra: `rw [indep, mul_comm, mul_div_assoc, div_self hw, mul_one]`. The
   *entire* physical content of Part B lives in the hypothesis `indep`, which is asserted, not
   derived — the file cites Fisher's χ²-⊥-direction independence for Gaussian vectors.

2. **The conclusion is exact at every coupling β.** No limit is taken. β does not appear.
   A linearization statement is *asymptotic* — "the deviation → 0 as the coupling → 0". These are
   different logical shapes. **The orthogonality theorem is not literally a linearization limit,
   and this note does not claim it is.**

3. **Parts A and B of that file are never joined.** `participation_scale_invariant` (a real
   theorem: the participation ratio is invariant under `a ↦ c·a`) and `pomega_preserves_power`
   (the algebra above) sit side by side, and *nothing in Lean says the weight `w` is a function of
   `participation`*. The bridge between them exists only in the docstring.

So a "linearization limit restatement" needs to supply two things the lake did not have:
a formal factorisation of the weight through the scale-invariant shape observable (to close the
A–B gap), and an actual asymptotic statement in the coupling (to earn the word *limit*).
Both are now proved.

---

## 2. What is proved

The mechanized content splits into two sectors. It is the *conjunction* that is the framework's
analogue of Bianconi's Eqs. 45–47 — not an identification of two theorems.

### 2.1 Shape sector — the deviation is second order in the coupling (the new content)

`Core/EntropicPotential.lean` already proved that the chaos pole is the **zero** of the entropic
potential (T-E1a, `entropicPotential_at_zero`: `S(k, 0) = 0`). The new theorem is that it is also
the **critical point**:

| id | statement | Lean name |
|---|---|---|
| **T-L1** | `HasDerivAt (entropicPotential k) 0 0` — *no hypothesis on `k`* | `entropicPotential_hasDerivAt_zero` |
| T-L1a | `S'(k, 0) = 0` in closed form | `entropicPotentialDeriv_at_zero` |
| T-L1b | `S''(k, 0) = k(k−1)` in closed form | `entropicPotentialDeriv2_at_zero` |
| T-L1c | `S(k, ·) =o[𝓝 0] id` — no first-order term | `entropicPotential_isLittleO_id` |
| **T-L2** | `S(k, ρ)/ρ² → k(k−1)/2` as `ρ → 0⁺`, for `k ≥ 1` | `entropicPotential_div_sq_tendsto` |
| **T-L3** | `1 − exp(−βS(k,ρ))` is second order with coefficient `β·k(k−1)/2` | `entropicWeight_deviation_secondOrderDeviation` |

with supporting infrastructure: `hasDerivAt_entropicPotential`,
`hasDerivAt_entropicPotentialDeriv` (the two derivative formulas
`S' = (k−1)/(1−ρ) − (k−1)/(1+ρ(k−1))`, `S'' = (k−1)/(1−ρ)² + (k−1)²/(1+ρ(k−1))²`), and
`entropicPotentialDeriv_div_tendsto` (the intermediate L'Hôpital pass, `S'/(2ρ) → k(k−1)/2`).
T-L2 is two applications of `HasDerivAt.lhopital_zero_right_on_Ioo` on `(0, 1)`, where both
spectral branches of `C(k, ρ)` stay positive for `k ≥ 1`.

Two packaging predicates capture the weak-coupling structure:

```lean
structure LowCouplingLimit (D : ℝ → ℝ) : Prop where
  vanishes_at_substrate : D 0 = 0
  tendsto_zero : Tendsto D (𝓝[>] 0) (𝓝 0)

structure SecondOrderDeviation (D : ℝ → ℝ) (c : ℝ) : Prop where
  vanishes_at_substrate : D 0 = 0
  stationary_at_substrate : HasDerivAt D 0 0     -- the load-bearing clause
  curvature_limit : Tendsto (fun ρ => D ρ / ρ ^ 2) (𝓝[>] 0) (𝓝 c)
```

with `entropicPotential_secondOrderDeviation k hk : SecondOrderDeviation (entropicPotential k) (k*(k-1)/2)`
and `SecondOrderDeviation.toLowCouplingLimit`.

T-L2 also promotes the small-ρ sensing law that `entropic_action_bridge.md` §T-E5 recorded as
"documented, not mechanized" (`S ≈ ½k(k−1)ρ²`) to a theorem with an exact limit.

### 2.2 Power sector — closing the A–B gap in `CMBOrthogonality`

`H_sum` is built from `ρ_ℓ`, the per-multipole Kish correlation, which is read off the
participation ratio by inverting `k_eff = k/(1 + ρ(k−1))`. That inversion is now a definition with
a correctness theorem, and the weight is now *exhibited* as a shape function:

| statement | Lean name |
|---|---|
| `kishRhoOfParticipation k (k_eff k ρ) = ρ` for `k > 1`, `0 ≤ ρ < 1` | `kishRhoOfParticipation_k_eff` |
| any `f ∘ participation` is scale-invariant | `shape_weight_scale_invariant` |
| the entropic weight `exp(−βS(k, ρ(participation a)))` is scale-invariant | `entropicWeightOfAmplitudes_scale_invariant` |
| any shape weight preserves the power expectation, given `indep` | `shape_weight_preserves_power` |
| the entropic instance of the above | `entropic_pomega_preserves_power` |

These do **not** prove `indep`. They isolate it. After this file, the orthogonality theorem's only
unproved input is the Gaussian shape ⊥ scale independence (Fisher), and that fact is now visible in
the statement rather than buried in a docstring.

### 2.3 Build and axiom audit

```
$ cd formal && lake build CoherenceRatchet.Cosmology.EntropicLinearization
✔ [5701/5701] Built CoherenceRatchet.Cosmology.EntropicLinearization
Build completed successfully.
```
No warnings. Not imported from `CoherenceRatchet.lean` (the orchestrator wires that).

`#print axioms` on all 18 declarations: **kernel-only**, `[propext, Classical.choice, Quot.sound]`,
for every theorem — `SecondOrderDeviation.toLowCouplingLimit`, `hasDerivAt_entropicPotential`,
`hasDerivAt_entropicPotentialDeriv`, `entropicPotentialDeriv_at_zero`,
`entropicPotentialDeriv2_at_zero`, `entropicPotential_hasDerivAt_zero`,
`entropicPotential_isLittleO_id`, `entropicPotentialDeriv_div_tendsto`,
`entropicPotential_div_sq_tendsto`, `entropicPotential_secondOrderDeviation`,
`entropicPotential_lowCouplingLimit`, `entropicWeight_at_zero`,
`entropicWeight_deviation_secondOrderDeviation`, `kishRhoOfParticipation_k_eff`,
`entropicWeightOfAmplitudes_scale_invariant`, `shape_weight_scale_invariant`,
`shape_weight_preserves_power`, `entropic_pomega_preserves_power`.
`orthogonality_is_linearization` (the structural record) *does not depend on any axioms*.

No framework primitives, no `sorry`. Unlike T-E4a/b in `EntropicPotential.lean`, nothing here
composes with `Core.Dynamics`, so nothing here carries `α`, `γ`, `M`.

---

## 3. The argument: why this is a mechanism and not a coincidence

Bianconi's Eqs. 45–47 say: at low coupling (`α', β' ≪ 1`) the entropic action reduces **exactly**
to Einstein–Hilbert **with zero cosmological constant**. Structurally, that is one statement:

> *The vacuum `G̃ = g̃` is a stationary point of the relative-entropy action, so no term survives
> at first order in the coupling.*

A nonzero first-order term would *be* a cosmological constant: a coupling-linear piece of the
Lagrangian surviving as the coupling is switched off.

**T-L1 is exactly that statement for `S(k, ρ)`.** The two spectral branches of the uniform-ρ
correlation matrix — the one stretched eigenvalue `1 + ρ(k−1)` and the `(k−1)` compressed ones
`1 − ρ` — contribute `−(k−1)` and `+(k−1)` to `dS/dρ` at `ρ = 0` and cancel exactly. `S` is flat at
the substrate. Nothing is tuned; the cancellation is forced by the trace structure
(`Tr C(k, ρ) = k` for all ρ, so the spectrum's *first* moment is coupling-independent, and the
relative entropy can only see it at *second* moment).

This gives the fence a mechanism, in the following precise sense.

- Before: *"We happen not to deviate from ΛCDM in the power sector."* An unexplained coincidence
  of the weight's functional form.
- After: *"The deviation from the substrate theory is a second-order entropic quantity, and the
  first-order term vanishes because the substrate extremizes the action. In the power sector, that
  second-order deviation is furthermore exactly zero, at every coupling, because the weight is a
  scale-invariant shape function."*

And a quantitative rhyme worth recording (interpretation, §4): Bianconi's follow-up
(arXiv:2510.22545, bridge §7.2) identifies the emergent cosmological constant with the G-field
**Hamiltonian**, `Λ^G = ℋ = Σ_k z_k[𝒢_k − 1 − ln 𝒢_k] > 0` — not with the action. Λ^G is therefore
*not* the linearized object; it is what survives *beyond* strict linearization. On the framework
side that is precisely the curvature term T-L1 forces to be leading:

```
Λ = 0     at strict linearization          ⟸  S'(k, 0) = 0        (T-L1)
Λ > 0     at second order in the coupling  ⟸  S''(k, 0) = k(k−1) > 0 for k > 1   (T-L1b)
Λ = 0     for k = 1                        ⟸  S(1, ρ) ≡ 0: one unit, no coordination
```

The emergent Λ is the *second-order term T-L1 says must be the leading one*, and its positivity is
the positivity of `S''(k, 0)` — the same convexity that makes `S` a Lyapunov-type potential
(T-E2). Read with the maintenance mapping (bridge §2, G-field ↔ `γ·M`): **Λ is the standing
maintenance cost of coordination, and it is second order in the coupling because the substrate is
a critical point.** The sibling note `lambda_maintenance_wz.md` develops the dynamical consequence
(`1 + w(a) = −(1/3) d ln S / d ln a`); this note supplies the reason the leading term is quadratic.

### 3.1 A caveat that must not be skipped: second order in ρ is not "small"

`S ≈ ½·k(k−1)·ρ²` is second order in **ρ**, and *quadratic in the mode count k*. For a CMB
multipole, `k = 2ℓ+1`. At the framework's own measured baseline `ρ ≈ 0.26–0.33`
(GPU array, Exp 82; RATCHET `CLAUDE.md`), the shape-sector weight exponent is
`S ≈ ½(2ℓ+1)(2ℓ)ρ²` — order `1` at `ℓ = 2`, order `10²` at `ℓ = 30`. This is the `~k²`
sensitivity of T-E5, and it is *good* for detection.

The consequence for this note is a negative one, and it is the honest reading:

> **T-L3's second-order smallness is not what protects the CMB power spectrum.** What protects it
> is the *exact* scale-invariance of `participation` (T-L2's power-sector counterpart), which holds
> at every β and every ℓ regardless of how large `S` gets.

Anyone tempted to argue "the framework agrees with ΛCDM because the deviation is `O(ρ²)` and ρ is
small" is arguing something false at high ℓ. The power-sector agreement is exact and structural;
the shape-sector deviation is second-order in ρ but unbounded in k.

---

## 4. Theorem vs interpretation — the ledger

Recorded in-lake as `OrthogonalityIsLinearization` (a `structure` + `def ... := ⟨trivial,…⟩`
record, following `CorridorProjector.FelevenNoGo` and `OperationalCorridor`), because these are
statements *about* theorems, not theorems.

**THEOREM (kernel-only):**
- The substrate is a stationary point of `S`; the deviation has no first-order term (T-L1).
- The exact quadratic coefficient is `k(k−1)/2` (T-L2), and the induced weight's is `β·k(k−1)/2` (T-L3).
- Any weight factoring through `participation` is scale-invariant, and the entropic weight does so
  factor (via the Kish inversion, `kishRhoOfParticipation_k_eff`).
- Given `indep`, any such weight preserves the power expectation exactly, at every β.

**INTERPRETATION (not theorems; do not cite as framework content):**
- **The orthogonality theorem is not literally a linearization limit.** It is exact at all β and
  takes no limit. What is proved is the *conjunction* of the two sector facts, which is the
  framework's analogue of Eqs. 45–47.
- **That `H_sum = Σ_ℓ (ρ_ℓ − ρ_mid)²` *is* the entropic weight `exp(−β Σ_ℓ S(k_ℓ, ρ_ℓ))` is a
  modelling commitment.** Both are shape functions — both factor through `participation`, so both
  are power-orthogonal, and the power-sector theorem holds for either. But they are different
  functionals, and the coefficient `k(k−1)/2` is specific to `S`. The lake's numerical demo
  (`experiments/open_system_pomega/cmb_weak_value_spectrum.py`) used the `(ρ_ℓ − ρ_mid)²` form.
- **`indep` (Gaussian shape ⊥ scale, Fisher) is cited, not proved.** It remains the single
  unproved input of the orthogonality theorem.
- **The Λ^G ↔ `½k(k−1)ρ²` identification of §3 is an analogy** at the level of "both are the
  second-order curvature term of the same relative-entropy shape". Bianconi's Λ^G is a Legendre
  transform of a field-theoretic action; `S` is a finite-dimensional functional of a correlation
  spectrum. The rhyme is structural.
- Bianconi's theory itself is ~18 months old, actively developed by its originator, and not
  independently stress-tested (bridge §7.4). Per bridge §7.5, all mechanized content here survives
  intact even if entropic gravity is false — it is finite-dimensional real analysis on the spectrum
  of a correlation matrix. What would be lost is the physical-rung analogy, not the mathematics.

---

## 5. The critical internal-consistency check: does an evolving Λ contradict `framework_cmb_power_eq_lcdm`?

Posed sharply: if Λ is the G-field Hamiltonian — a *maintenance cost* — then it can vary with
cosmic time as the maintenance bill varies. Late-time evolving Λ changes the distance to last
scattering (hence the acoustic scale `θ*`), changes the late integrated Sachs–Wolfe contribution at
low ℓ, and changes CMB lensing. All three move CMB observables. Does that break the theorem that
says the framework's CMB power spectrum *equals ΛCDM's*?

### 5.1 Resolution: the theorem's letter is safe; the theorem's *slogan* is not

**The orthogonality theorem is about the post-selection operator's action on modes at a fixed
underlying ensemble. It is not about background cosmology.**

Re-read the statement (§1). `E` is the forward ensemble — arbitrary, unconstrained, supplied from
outside. `w` is the post-selection weight. The theorem says:

> for **any** `E`: reweighting by `w` does not change `E S`.

The framework's predicted power spectrum is `E(wS)/E(w)`; the forward theory's is `E S`; they are
equal. **Which background `E` encodes is not the theorem's business.** Evolving Λ modifies `E` — it
changes the transfer function and the geometric projection, hence changes the number `E S`. It does
**not** modify `w`, which factors through `participation`, a per-multipole, within-ℓ, scale-invariant
*directional* observable of the `2ℓ+1` amplitudes. Λ is a background zero-mode quantity; it does not
live in the shape sector at all.

The two sectors are disjoint. **No contradiction with the theorem.** Indeed this is a *third*
orthogonality, and it is the resolution: `P_ω` deforms the conditioning sector; Λ deforms the
background sector; the theorem is a commutation statement across them.

What *is* false, if Λ evolves, is the **corollary as written in the docstring** of
`CMBOrthogonality.lean` and repeated in `RESEARCH_PROGRAM.md`:

> "C_ℓ^framework = C_ℓ^ΛCDM, exactly … the framework is a strict extension of ΛCDM at the
> cosmological tier."

That corollary silently substitutes `E = the ΛCDM ensemble`. The theorem licenses only
`C_ℓ^framework = C_ℓ^forward`. If the entropic action's G-field delivers a time-varying Λ^G, the
framework's forward background is `w₀wₐCDM`-like, not ΛCDM, and the framework's CMB prediction is
not ΛCDM's. **The theorem survives; the marketing line does not.**

### 5.2 The tension is real and must be flagged loudly

This is the *price of the upgrade this note performs*. So long as orthogonality was a bare fence —
"we happen not to deviate" — one could recite "framework = ΛCDM exactly, nothing to test". The
moment you say orthogonality is the power-sector face of an entropic action's stationarity, you
have imported that action's own content, and Bianconi's action produces an emergent Λ^G beyond
strict linearization (§3). Fence and mechanism cannot both be free.

Stated as a trilemma, the framework may hold at most two of:

1. `framework_cmb_power_eq_lcdm` *as read in its docstring* — the framework cannot disagree with
   ΛCDM on the bulk power spectrum;
2. the entropic action as the **mechanism** of orthogonality (this note);
3. an **evolving** Λ^G.

The theorem itself is in none of these slots — it is compatible with all three, because it
quantifies over `E`. It is (1)'s *reading* that must go if (2) and (3) are kept. The recommended
resolution is to keep (2) and (3) and restate (1) with its scope:

> **Strict extension of ΛCDM in the conditioning / within-multipole sector (theorem, exact at all
> β). Possibly a deformation in the background sector, governed by the entropic action.**

This is the same verdict `lambda_maintenance_wz.md` §7(e) reaches from the `w(z)` side, arrived at
independently. That note adds the mitigating fact this one cannot supply: by its §2 linear-theory
fence, `S` is constant through recombination and the whole linear era (the correlation *shape* is
blind to the growth factor `D(a)`, by the same scale-invariance that `participation_scale_invariant`
expresses for the amplitude vector), so `w = −1` exactly there. The sound horizon `r_s`, the
acoustic peaks, and the primary anisotropies are untouched. What moves is the low-`z` `H(z)` integral
into `θ*` — largely degenerate with `H₀` — and the late ISW at low ℓ.

### 5.3 F-19 is not resurrected

Worth stating because it is the obvious misread. F-19 (CMB temporal drift) was declared **moot**
post-F-11 because the drift mechanism was a time-dependent `β(t)` in the *post-selection weight*,
which required the joint operator. Evolving Λ^G does not make `β` time-dependent and induces no
shape-sector drift. It is a background-sector effect, arising from a forward variational principle.
**F-19 stays moot. D4 stays retracted. A new, distinct, background-sector falsifier appears** — and
per bridge §6 that falsifier sits on *Bianconi's* ledger ("her theory dies on these independently of
the framework"), not the framework's, unless and until the framework commits to `ρ_DE = κ·S(a)` as
`lambda_maintenance_wz.md` proposes. That note is explicitly conjecture-grade and supplies no `S(a)`.

---

## 6. What to change downstream

1. **`CMBOrthogonality.lean` docstring.** The corollary "C_ℓ^framework = C_ℓ^ΛCDM, exactly" should
   read "= C_ℓ^forward, exactly, for whatever forward background `E` encodes". Suggested; not done
   here (single-file scope).
2. **`RESEARCH_PROGRAM.md`,** "Untouched by F-11" bullet: *"the orthogonality theorem (the framework
   is a strict extension of ΛCDM at the cosmological tier)"* → add the scope qualifier
   *"…in the conditioning/within-multipole sector, at fixed background."*
3. **`entropic_action_bridge.md` §5 item 2** (registry): T-L1/T-L2 are candidate `cc_lean.tsv` rows
   at status `mechanized` from day one, if a CC claim is minted for the stationarity of the
   substrate. T-L2 also closes the "documented, not mechanized" gap in the §T-E5 small-ρ sensing law.
4. **Anyone quoting the orthogonality theorem alongside either this note or
   `lambda_maintenance_wz.md` must quote both halves of the restated fence.**

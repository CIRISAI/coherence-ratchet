# Λ as maintenance cost — a sign law for w(z)

**STATUS: CONJECTURE-GRADE. Not lake content. Not asserted by the framework.**
A research direction with one concrete falsification path (compute `S(a)`). Nothing here is
mechanized; nothing here is cited by any paper. Draft 2026-07-10.

**Depends on:** `papers/notes/entropic_action_bridge.md` (§2 mapping, §3 the Kish object, §4
F-11 fence, §7.2 Bianconi's Hamiltonian); `formal/CoherenceRatchet/Core/EntropicPotential.lean`
(T-E0–T-E5); `formal/CoherenceRatchet/Core/Dynamics.lean` (`dρ/dt = α − γM`).

**F-11 compliance (stated up front).** Everything below is **forward** content: a steady-state
output of the maintenance field, read off a forward continuity equation. It does not use, need,
or resurrect the joint multi-rung backward `P_ω`, D4 (CMB anomalies as TSVF post-selection),
or F-19 (β(t) drift). Those stay retracted. The bridge note's §4 argument applies verbatim:
an entropic-action route is a forward variational principle, and its steady states are exactly
the half of `P_ω` that survived F-11.

---

## 1. The reading, and the sign law

Bianconi's follow-up (arXiv:2510.22545) Legendre-transforms the gravity-from-entropy action into

```
ℋ = Σ_k z_k [ 𝒢_k − 1 − ln 𝒢_k ],      𝒢_k = 1/(1 − τ_k)
```

and states that ℋ is positive and **equals the emergent cosmological constant Λ^G**. In the
bridge's mapping, her G-field (the Lagrange-multiplier field that holds the metric on its
constraint surface) is the framework's maintenance term `γ·M`. Read together: **Λ is the
standing maintenance cost of cosmic coordination structure.**

Give that reading teeth. Posit that the dark-energy density tracks the coordination relative
entropy,

```
ρ_DE(a) = κ · S(a),      κ > 0 constant                                    (1)
```

with `S` the entropic potential of `EntropicPotential.lean`. The DE continuity equation is

```
ρ̇_DE + 3H(1 + w)ρ_DE = 0.
```

Using `d/dt = H d/d ln a`, divide by `H ρ_DE`:

```
d ln ρ_DE / d ln a = −3(1 + w).
```

Substituting (1), the constant κ cancels in the logarithmic derivative, leaving

```
┌────────────────────────────────────────┐
│   1 + w(a) = −(1/3) · d ln S / d ln a  │                                 (2)
└────────────────────────────────────────┘
```

**The proportionality constant drops out.** Given `S(a)`, `w(z)` is predicted with **no free
parameters** — not even the amplitude of Λ, which (2) never sees. This is the whole content of
the note. Its three immediate corollaries:

| `S(a)` | `w` | reading |
|---|---|---|
| constant | `= −1` exactly | a true cosmological constant |
| rising | `< −1` (phantom) | coordination structure being **built** |
| falling | `> −1` | coordination structure being **lost** |

Λ is constant exactly when the maintenance bill is constant. That is not a tuning; it is what
"cosmological constant" *means* under (1).

### 1.1 The hidden normalization (flagged here, returned to in §7)

(1) equates an energy **density** with `S`, which is extensive in the number of coordinating
units `k` (T-E3: `S ≈ k · s(ρ)` with `s = −ln(1−ρ)`). So (1) is only well-posed once we say
*per what volume*. Per **physical** volume, a frozen comoving structure gives `ρ_DE ∝ a⁻³` and
`w = 0` — dust, not Λ. Per **comoving** volume it gives `w = −1`. Only the second choice makes
(2)'s ΛCDM limit come out. We adopt it, and we adopt it because it gives the right answer.
See §7(a).

---

## 2. The linear-theory fence

**Claim.** In linear growth `δ(x, a) = D(a) δ(x)`, `S` is independent of `D`, hence `w = −1`.

**Proof.** Let `C_ij = ⟨δ_i δ_j⟩ / √(⟨δ_i²⟩⟨δ_j²⟩)` be the normalized correlation matrix over a
fixed set of `k` tracers. Then `⟨δ_i δ_j⟩(a) = D(a)² ⟨δ_i δ_j⟩₀`, and the denominator carries
`D(a)²` as well, so `C_ij(a) = C_ij(0)` for every pair. Since `S = −ln det C` (T-E5b), `S` is a
functional of `C` alone: `S(a) = S(0)`. By (2), `w = −1`. ∎

The structural reason is worth naming, because it is the same reason twice. `S = 2·I` with `I`
the Gaussian multi-information (T-E5c), and multi-information is **invariant under invertible
per-component transformations** — it is a property of the copula, not the marginals. Linear
growth is exactly a common invertible rescaling of every marginal. So `S` cannot see it.

This is the *same theorem* as `participation_scale_invariant` in `CMBOrthogonality.lean`, which
says the participation ratio depends only on the direction of the amplitude vector, not its
scale. One spectrum, two functionals (T-E3 conjugacy: participation form `k_eff`,
relative-entropy form `S`); both blind to uniform amplitude. The `w(z)` fence and the CMB
orthogonality fence are one fact, applied to two matrices. That is a real structural rhyme, and
it is the strongest thing in this note.

**So all deviation from `w = −1` comes from what changes the *shape* of the correlation
structure, never its amplitude.** σ₈ growth contributes exactly nothing. Sources of shape change:

1. **Nonlinear mode coupling** — collapse correlates modes that linear theory keeps independent.
2. **Causal / horizon effects** — `γ·M` is *maintenance*, and maintenance requires ongoing causal
   contact. Under accelerated expansion, pairs of regions exit each other's Hubble radius and
   their coordination stops being maintainable.
3. **Baryonic feedback** — small-scale shape, astrophysical, not cosmological.

### 2.1 Correction: the fence is narrower than it looks

The brief for this note asserted `w = −1` *exactly* in linear theory. **That is not right, and
the error matters**, because it is the same effect as source (2) above.

The proof of §2 fixes the tracer set. But source (2) says the coordinating support — *which*
pairs are maintainable — is set by the comoving Hubble radius `(aH)⁻¹`, which **varies even in
pure linear theory**, and varies in matter domination, long before any nonlinearity. Horizon
*entry* in the past is the same physics as horizon *exit* in the future; you cannot invoke one
in §3 and forbid the other in §2.

The correct fence, then:

> **Linear growth of the amplitude contributes nothing to `w`. `w = −1` holds in linear theory
> only for a *fixed coordinating support*. The support is not fixed.**

Decompose accordingly. Write `S(a) = k_maint(a) · s̄(a)` — an extensive count of maintainable
coordination links times a mean per-link relative entropy — so that

```
d ln S / d ln a  =  d ln k_maint / d ln a  +  σ(a),      σ := d ln s̄ / d ln a.       (3)
                    └── kinematic, causal ──┘   └── shape: nonlinear + baryonic ──┘
```

Term one is the maintenance/horizon term. Term two is the shape term. The fence kills the
growth factor; it does not kill either of these.

---

## 3. The sign competition — not resolved

The two surviving terms in (3) pull opposite ways:

| source | effect on `S` | sign of `1 + w` | vs DESI today |
|---|---|---|---|
| nonlinear collapse | `S ↑` | `w < −1` (phantom) | **wrong sign** |
| horizon exit under acceleration | `S ↓` | `w > −1` | **right sign** |

So the framework as it stands yields a **sign law** (eq. 2), not a **sign**. It cannot say which
way `w` deviates from `−1` today until someone computes `S(a)`. This must be said plainly and
not papered over.

**The argument that horizon exit should win** (an argument, explicitly *not* a calculation):
by (3) the horizon term acts on the **extensive** factor `k_maint` — it removes whole causal
volumes, and with them every mode they contained, at all scales. The nonlinear term acts on the
**intensive** factor `s̄`, and only for the small-scale subset of links that have gone nonlinear.
Extensive beats intensive if the removed volume fraction is comparable to the nonlinear link
fraction. Note that the naive Fourier version of this argument — "there are more large-scale
modes" — is **backwards** (mode counts go as `k³`, dominated by small scales), and I decline to
use it. The extensive/intensive version is the defensible one, and it is still only an argument.

§5 shows the competition is close: today the two terms differ by a factor of ~1.5, with opposite
signs. Nothing in the framework fixes that ratio.

> **CORRECTION (2026-07-10, from the computation this section called for —
> `experiments/cosmo_entropic_potential/SUMMARY.md`).** Both rows of the table above are
> wrong, in different ways, and the competition does not survive contact with the numbers:
>
> | source | this note guessed | computed |
> |---|---|---|
> | nonlinear collapse | `S ↑` (phantom) | **`S ↓`** — theorem: for ANY pointwise transform `g`, `S(C_g) ≤ S(C_linear)` (Mehler/Hadamard/Oppenheim; 0 violations in 1700 independent-verification trials) |
> | horizon exit | `S ↓` (right sign) | **null** — 61% of pairs lie beyond `r_EH` today but carry ~3×10⁻¹⁶ of `S`; distant pairs are uncorrelated, so removing them costs nothing |
>
> The nonlinear intuition tracked the *unnormalized* `ξ_NL(r)`, which does grow; but `S`
> depends on the **normalized** `C`, and `Var(δ) = e^{σ_g²}−1` outruns `ξ_NL` — every
> off-diagonal entry *falls*. The extensive-beats-intensive argument above is likewise
> refuted by measurement: `s̄(removed)/s̄(kept) ≈ 2×10⁻¹⁶`. Net: within local growth models
> there is **no competition** — `S` is monotone decreasing, `w ≥ −1` always (thawing), and
> the framework's CPL shadow is `w_a ≈ −(1+w₀)` (ratio −0.954) against DESI's −3.83. The
> sign question moved from "uncomputed" to "computed, and in structural tension with the
> CPL best-fit point"; whether that tension is a likelihood-level exclusion is open — see
> SUMMARY.md §8 and the follow-up probes (rate-form mapping, halo grain, DESI-likelihood).

---

## 4. The DESI target

Epochs, for `Ω_m = 0.315`, `Ω_Λ = 0.685` (recomputed here):

- matter–Λ equality (`Ω_m(1+z)³ = Ω_Λ`): **z = 0.2956**
- acceleration onset (`q = 0`): **z = 0.6323**, and `q₀ = −0.5275`

DESI DR2 BAO, combined with CMB and supernovae, prefers `w₀ > −1` and `w_a < 0` at **2.8–4.2σ**,
the significance depending on which SNe compilation is used (Pantheon+ / Union3 / DES-SN5YR).
Dataset-dependent significance is **suggestive, not decisive**, and the range is quoted here as a
range for that reason. (Refs. as supplied in the task brief and **not independently verified
here**, per the bridge note's §7.1 habit: arXiv:2602.05368, *Dark Energy After DESI DR2*;
arXiv:2411.16046, *On the evidence of dynamical dark energy*.)

Invert (2) on a CPL `w(a) = w₀ + w_a(1−a)`. Then `d ln S/d ln a = −3(1 + w(a))`, `S` peaks where
`w = −1`, i.e. at `a = 1 + (1+w₀)/w_a`. Computed:

| `(w₀, w_a)` | `d ln S/d ln a` today | early (`a→0`) | `S` peaks at |
|---|---|---|---|
| `(−0.83, −0.75)` | **−0.51** | **+1.74** | **z = 0.293** |
| `(−0.85, −0.80)` | −0.45 | +1.95 | z = 0.231 |
| `(−0.90, −0.60)` | −0.30 | +1.50 | z = 0.200 |

**DESI ⇒ `S` rose steeply through matter domination, peaked at z ≈ 0.2–0.3, and is now declining
gently.** That is a coherent story on the maintenance reading: coordination structure was being
built while gravity assembled it, and is now being destroyed faster than it is built, as
acceleration carries regions out of causal contact.

Note, for §6: these three numbers depend **only** on `(w₀, w_a)`. `Ω_m` does not appear in
`a_peak` or in either log-derivative. (The task brief's parenthetical that they were "computed
with `Ω_m = 0.315`" is harmless but misleading — `Ω_m` enters only the equality and onset
redshifts.)

---

## 5. A toy `S(a)`, and what it kills

Take the maintenance term alone: coordination links are maintainable when separated by less than
the comoving Hubble radius, so `k_maint ∝ (aH)^{−p}` with `p = 3` for a volume count. Since
`d ln(aH)/d ln a = 1 + Ḣ/H² = −q`, (3) with `σ ≡ 0` gives

```
d ln S / d ln a = p · q(a)      ⇒      1 + w = −(p/3) · q(a).                       (4)
```

Solved **self-consistently** (`ρ_DE ∝ (aH)^{−p}` fed back into `E² = Ω_m a⁻³ + Ω_Λ a^{−p}E^{−p}`,
so `w(a)` and `H(a)` are consistent; zero free parameters given `Ω_m` and `p`):

| `p` | `w₀` | `w_a` | `d ln S/d ln a` today | `S` peaks at |
|---|---|---|---|---|
| 3 (volume) | −0.740 | −0.262 | −0.781 | z = 0.780 |
| 2 | −0.791 | −0.241 | −0.626 | z = 0.742 |
| 1 (radius) | −0.869 | −0.182 | −0.393 | z = 0.694 |

Four things follow, and they are the useful part of this note.

**(a) The qualitative structure is right, free.** Every `p` lands in DESI's quadrant: `w₀ > −1`,
`w_a < 0`, `w < −1` in the past, one phantom-divide crossing. The framework did not have to do
this. A model with `S ↑` monotone would give `w < −1` today and be dead on arrival.

**(b) The crossing epoch is wrong, for every `p`.** By (4), `d ln S/d ln a = 0 ⟺ q = 0`: in the
pure-maintenance family the phantom-divide crossing coincides with **acceleration onset**,
independent of `p`. The toys put it at z ≈ 0.69–0.78. DESI puts it at z ≈ 0.20–0.29. So the
pure-maintenance model is **already disfavoured**, and `σ(a) ≠ 0` — a nonlinear shape term — is
*required*, not optional. This is a genuine, non-vacuous constraint that fell out of the algebra.

**(c) `p` is unforced, and `(1 + w₀) ∝ p`.** The counting dimension of the maintainable-link set
is a modeling choice, not a derivation, and it controls the magnitude linearly. So **the toy is
not parameter-free**, whatever §1 says about κ. Only a computed `S(a)` — a real correlation
matrix on a real density field — removes `p`. This is the sharpest available argument for doing
the computation.

**(d) The event horizon is excluded outright.** If the maintainable set is bounded by the
comoving *event* horizon `r_E(a) = a∫_t^∞ dt/a` (arguably the more natural "will ever be in
causal contact" boundary) rather than the Hubble radius, then `r_E` decreases monotonically, `S`
declines at all times, there is **no phantom past and no crossing**, and on a ΛCDM background
`d ln S/d ln a = −2.61` today, i.e. `w₀ = −0.13`. Ruled out by everything. The choice of causal
boundary is therefore load-bearing and unforced — a second free choice hiding in the "obvious"
mechanism.

### 5.1 The required shape term

Invert (3) with `p = 3`: `σ(a) = −3(1 + w_CPL(a)) − 3q(a)`, for `(w₀,w_a) = (−0.83,−0.75)`.
Computed in two backgrounds, because the answer is sensitive to which one:

| z | `σ` (ΛCDM background) | `σ` (self-consistent w₀wₐCDM) |
|---|---|---|
| 3.0 | −0.18 | −0.22 |
| 1.0 | +0.08 | +0.20 |
| 0.632 | +0.36 | +0.56 |
| 0.296 | +0.75 | +0.83 |
| 0.0 | **+1.07** | **+0.55** |

Read this honestly. In the ΛCDM background `σ` is monotone rising and O(1) today — exactly the
shape a nonlinear-collapse term should have, and a clean target. In the self-consistent
w₀wₐCDM background (which is the *correct* one, since `q` in (4) must be the real deceleration)
`σ` is **non-monotone**: it peaks near z ≈ 0.3 and falls to +0.55 today. A shape term that
*decreases* while structure formation accelerates is awkward. The `σ < 0` entries at z ≳ 1.3 are
probably CPL extrapolation artefacts — DESI's constraints come from z ≲ 2.3 and CPL is a fit, not
a model — but the non-monotonicity inside the constrained range is not obviously dismissible.

**Net:** the required shape term is O(1), positive over the DESI-constrained range, and of the
same magnitude as the maintenance term it opposes. Today, term-by-term in (3): in the ΛCDM
background, `σ = +1.07` against `3q = −1.58`; in the self-consistent w₀wₐCDM background,
`σ = +0.55` against `3q = −1.06`. Either way the maintenance term wins by a factor of only
~1.5–1.9. The competition of §3 is decided at the ~50% level. Nothing here decides it.

---

## 6. The coincidence, weighed down

`S`'s required peak (z ≈ 0.2–0.3) sits at matter–Λ equality (z = 0.2956), which the framework
independently reads as the epoch where coordination destruction overtakes creation. It is not a
fitted parameter: it is set by `Ω_Λ/Ω_m` alone. And — from §4 — the peak redshift is set by
`(w₀, w_a)` alone, with no `Ω_m` in it. So the two numbers being compared come from **logically
independent inputs**: one from the background density budget, one from the SNe+BAO fit. The
agreement is not tautological.

Now weigh it down. Four discounts, in increasing order of severity:

1. **Precision.** 0.2956 versus a target that ranges 0.200–0.293 across three plausible SNe
   compilations. Agreement at the 10–30% level with a quantity known to ±20%.
2. **`Ω_m` sensitivity.** `z_eq` runs 0.229–0.370 over `Ω_m ∈ [0.28, 0.35]` while `z_peak` sits
   fixed at 0.293. The coincidence is fragile at the ~25% level in a parameter that is *not* that
   well determined once `w` is allowed to float.
3. **Everything happens then.** Equality (0.296), acceleration onset (0.632), and the DESI
   crossing (0.2–0.3) are all within a factor ~2 in `(1+z)`. In an era with one scale, hitting
   "the" scale is cheap.
4. **The framework's own mechanism points at the *other* epoch.** This is the one the task brief
   got backwards, and it cuts against the framework, not for it. The brief supposed that any
   acceleration-sourced DE model is kinematically forced to equality, making the match weak
   evidence. §5(b) shows the opposite: the pure-maintenance family is forced to `q = 0`
   — **acceleration onset, z = 0.632** — for every counting exponent. Equality is a *different*
   epoch. So the coincidence is less forced than supposed (good), *and the framework's simplest
   mechanism does not produce it* (bad, and worse). Getting the peak to 0.296 requires the
   nonlinear `σ(a)` to be present at precisely the right size.

**The epoch match is therefore weak evidence at best, and it is not even evidence for the
mechanism the framework would want to claim.** The discriminating content is the **magnitude**:
`d ln S/d ln a` today must land near **−0.3 to −0.5**, from a decomposition whose two terms are
each O(1) and opposite. A computed `S(a)` either reproduces that or does not.

---

## 7. Failure modes

**(a) The normalization is chosen to give the answer. ← the single weakest link.**
Per §1.1, (1) is not well-posed until "per unit volume" is fixed, and only the comoving choice
yields `w = −1` for frozen structure. That choice was made because it reproduces Λ. Everything
downstream — the fence of §2, the sign law's ΛCDM limit, the whole note — rests on a step that
inserted the desired conclusion. This is logically prior to (b) and I regard it as more damaging,
because (b) is a gap in an *analogy* while (a) is a gap in the *definition*.

**(b) `Λ ∝ S` is an analogy — but a tighter one than the brief supposed.** The brief called the
functional gap between Bianconi's `ℋ = Σ z_k[𝒢_k − 1 − ln 𝒢_k]` and our `S = −Σ ln λ'` the weakest
link. It is not, because on a **correlation** matrix the gap closes exactly: `Tr C = k` (unit
diagonal), so `Σ(λ_i − 1) = 0`, and therefore

```
S = −Σ ln λ_i = Σ [ λ_i − 1 − ln λ_i ].                                             (5)
```

Our `S` **is** a Bregman divergence of `−ln` about the vacuum, term for term, with `z_k = 1` and
`𝒢_k = λ_k`. (This is not new mathematics: it is exactly the Klein-inequality proof already in
`entropicPotential_nonneg`, read forwards. Verified numerically.) The residual gap is not the
functional form but the **identification of the arguments and the weights**: Bianconi's `𝒢_k` are
eigenvalues of the metric ratio `G̃g̃⁻¹` with volume weights `z_k` and no trace constraint; ours
are eigenvalues of a density-field correlation matrix with unit weights and `Tr C = k`. Asserting
that the spectrum whose Bregman divergence is `Λ^G` *is* the correlation spectrum of the cosmic
density field is the leap. It remains a leap. It is just a smaller one than advertised.

**(c) The perturbation sector is unaddressed.** Phantom crossing `w < −1` in the past is a
standard no-go for a single canonical scalar field (gradient/ghost instability at the crossing).
Λ here is an emergent Lagrange multiplier, not a scalar, so the no-go does not formally bite —
but a *varying* `Λ^G` has a fluctuation sector with its own clustering and sound speed `c_s²`.
If `c_s² ≈ 1` the DE stays smooth on sub-horizon scales and the ISW/growth impact is mild; if
`c_s² ≈ 0` it clusters and CMB/ISW constraints are severe. **The multiplier field's fluctuation
sector has not been examined for ghosts, and the ISW constraint has not been evaluated.** Flagged
as an unaddressed constraint, not as a resolved one.

**(d) Unfalsifiable until `S(a)` is computed. ← the most important line in this note.**
If DESI's evolution evaporates and `w = −1` is restored, the framework says: *of course — the
correlation shape is frozen, §2*. If DESI's evolution stands, the framework says: *of course —
the maintainable support is shrinking, §3*. **It accommodates both outcomes.** A theory that
survives either result is not being tested by either result. The sign law (2) is exact and
parameter-free, and it is *empty* until someone supplies `S(a)`. The toys of §5 do not supply it:
they carry two unforced choices (`p`, and the causal boundary) that between them span
`w₀ ∈ [−0.87, −0.13]`.

This is the whole argument for doing the computation, and it should not be softened.

**(e) Internal consistency with the orthogonality theorem — resolved, at a cost.**
Does an evolving Λ contradict `framework_cmb_power_eq_lcdm`?

*Formally, no.* `pomega_preserves_power` says: if the post-selection weight is statistically
independent of the mode amplitudes, `E[w·S] = E[w]·E[S]`, so the soft `P_ω` moves no bulk power.
That is a statement about the **conditioning operator's action on modes at a fixed underlying
ensemble**. It says nothing about the background expansion history. Evolving Λ is a
**background-sector** modification. The theorem's sector and the deviation's sector are disjoint.

*Substantively, the fence must be restated.* "The framework is a strict extension of ΛCDM at the
cosmological tier" would become false: it would be a strict extension of `w₀wₐCDM`. Two concrete
CMB observables move — the distance to last scattering (hence `θ*`), and the late ISW.

*And the linear fence rescues the primary CMB.* By §2, the deviation switches on only where the
correlation **shape** changes: nonlinearity and horizon exit, both at `z ≲ 1`. Through
recombination and the entire linear era `S` is (shape-)constant and `w = −1` exactly, so the
sound horizon `r_s`, the acoustic peaks, and the primary anisotropies are untouched. What moves
is the low-`z` `H(z)` integral into `θ*` — largely degenerate with `H₀` — and the late ISW, which
is exactly the multipole range where `pomega_preserves_power` was never the load-bearing claim.

**Verdict: consistent, but the marketing line must change.** The honest statement is: *strict
extension of ΛCDM in the conditioning/perturbation sector (theorem); a one-parameter-family
deformation in the background sector, with the deformation vanishing identically in linear
theory (the fence of §2).* Anyone quoting the orthogonality theorem alongside this note must
quote both halves.

---

## 8. What would settle it

`S(a)` is a computable object, not a philosophical one. The recipe:

1. Take an N-body (then hydro) simulation across `z ∈ [0, 3]`.
2. Tile it into comoving cells; build the normalized correlation matrix `C_ij(a)` of the density
   contrast over the cells.
3. Restrict to the **maintainable support**: pairs within the comoving Hubble radius `(aH)⁻¹`.
   (Test the event-horizon restriction too; §5(d) predicts it fails.)
4. `S(a) = −ln det C(a)` (T-E5b). Differentiate: `d ln S/d ln a`.
5. Read `w(a)` off (2). Compare to DESI.

Three pre-registered discriminants, in order of strength:

| # | Prediction | Kills the reading if |
|---|---|---|
| 1 | `d ln S/d ln a` today ∈ [−0.5, −0.3] | it is positive (⇒ `w < −1` today) or `≪` −1 |
| 2 | `S` peaks at z ≈ 0.2–0.3 | it peaks at acceleration onset (z ≈ 0.63) — the pure-maintenance answer, §5(b) |
| 3 | shape term `σ(a)` monotone rising, O(1) | it is non-monotone, or `≪ 1`, over `z ∈ [0,1]` |

Discriminant 1 is the one the framework cannot dodge, because (2) has no free parameters once
`S(a)` exists. Discriminant 2 tests whether the maintenance mechanism or the nonlinear mechanism
sets the epoch. Discriminant 3 is the cheapest and can be run first, on existing correlation
matrices, without any cosmology at all.

Until then: **the framework has a sign law, and no sign.**

---

## 9. Returns to the task brief

- **The sign law:** `1 + w(a) = −(1/3) · d ln S/d ln a`. Exact; κ cancels; parameter-free given `S(a)`.
- **Does the framework predict a sign?** **No — only the law.** The two shape-change sources pull
  opposite ways and the competition is decided at the ~50% level (§3, §5.1). Worse than the brief
  supposed: the pure-maintenance mechanism, which is the one with the right sign, puts the
  phantom crossing at acceleration onset (z ≈ 0.63–0.78) for *every* counting exponent, not at
  DESI's z ≈ 0.2–0.3 (§5b). The nonlinear term — the one with the *wrong* sign today — is
  therefore *required*, at a size that must be tuned. The framework does not currently predict
  DESI's result; it predicts DESI's *quadrant*.
- **Orthogonality consistency:** consistent. The theorem fences the conditioning sector at fixed
  background; evolving Λ deforms the background sector. Disjoint. But "strict extension of ΛCDM"
  must become "strict extension in the conditioning sector; `w₀wₐCDM`-class deformation in the
  background, vanishing identically in linear theory" (§7e).
- **The single weakest link:** **not** the Bianconi analogy — that gap is exactly closed by (5),
  `Tr C = k ⇒ S = Σ[λ−1−lnλ]`, and the brief overstated it. The weakest link is **§1.1 / §7(a):
  the comoving-vs-physical normalization of `ρ_DE ∝ S`**, which is undetermined by anything in the
  framework and was fixed by choosing the option that reproduces `w = −1`. The conclusion was
  inserted at the definition.

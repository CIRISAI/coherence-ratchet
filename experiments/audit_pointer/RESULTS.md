# The endogenous audit pointer — RESULT

**Verdict: FAIL.** The endogenous audit-pointer weak measurement is not a
working measurement apparatus for the cross-rung timescale g/J.

Pre-registered in `PREREGISTRATION.md`, committed in a preceding commit; git
history is the proof. Simulation: `weak_measure_gj.py` (CUDA / cupy, RTX 4090).
Two-sided design — FAIL is a valid, reportable outcome and is the outcome.

| Hypothesis | Verdict | Why |
|------------|---------|-----|
| H-conjugate | **FAIL** | Q_M, P_M are not a clean conjugate pair; measured δ⟨P_M⟩ = −0.59× the AAV prediction (wrong sign and magnitude). |
| H-readout (decisive) | **FAIL** | Im⟨A⟩_w is non-monotone in g/J → δ⟨P_M⟩ does not invert to a unique g/J. Median recovery error 57%; 3/10 cells within 15% tolerance. |
| H-noncollapse | **PASS** | At genuinely weak λ the coupling back-action on ρ_n is tiny (max 0.0006). |

All three must pass for PASS. Two fail; the decisive one (H-readout) fails.

## The construction tested

Faithful to the pre-registration. Adjacent-rung two-level system, basis
|n⟩, |n+1⟩, Hamiltonian carrying both timescales:

```
H_sys = (J/2)(|n⟩⟨n| − |n+1⟩⟨n+1|)  +  g(|n+1⟩⟨n| + |n⟩⟨n+1|)
```

J = intra-rung scale (detuning, fixed at 1.0), g = cross-rung coupling (swept,
so g/J = g). Cross-rung transfer operator `A = |n+1⟩⟨n|`. The maintenance-layer
pointer: `P_M` is γM, the audit-pressure work rate, built as a genuine momentum
operator on a γM lattice (spectral / FFT derivative); `Q_M` is its position
partner, the un-collapsed corridor variance. Weak interaction
`H_meas = λ·A⊗P_M`. Because `A² = 0`, `exp(−iλA⊗P_M) = I − iλA⊗P_M` is exact.
ABL pre/post-selection on two distinct within-corridor states (ρ_n = 0.26 pre,
0.30 post). AAV shifts read exactly as written:
`δ⟨Q_M⟩ = (∫λ dt)·Re⟨A⟩_w`, `δ⟨P_M⟩ = 2(∫λ dt)·Var(P_M)·Im⟨A⟩_w`.

g/J grid: {0.10, 0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00}.
Genuine weak regime: λ·√Var(P_M) ≪ 1. With Var(P_M) ≈ 232 this forces
λ ≲ 0.004; the main run uses λ = 0.002 (λ·√Var(P_M) ≈ 0.03). λ = 0.04 — a
plausible "small" value a priori — is **not** weak for this pointer (back-action
≈ 0.13); this is itself a finding (below).

## H-conjugate — FAIL

`Q_M` and `P_M` do **not** function as canonical conjugates, and the AAV split
does not hold.

- `⟨[Q_M, P_M]⟩ = 0.000 + 1.000i` on the pointer state — but the **bulk
  operator deviation** `|[Q_M,P_M] − iI| = 1.08` is order-1. The commutator is
  i in expectation only; as an operator it is not iI. A spectral (FFT) momentum
  on a finite lattice is not canonically conjugate to lattice position — the
  edge terms are large. This is exactly the failure mode the pre-registration
  flagged: **∂ρ_ss/∂γM < 0 is monotonicity, not conjugacy.** The framework's γM
  layer gives a monotone Q_M↔P_M relation; it does **not** supply a canonical
  conjugate pair, and assuming one was never licensed.
- Decisive sub-test: measured δ⟨P_M⟩ vs the AAV prediction
  `2λ·Var(P_M)·Im⟨A⟩_w`. Across the g/J grid the **median ratio is −0.59** —
  wrong sign, ~40% magnitude. The AAV momentum-shift formula fails for this
  pointer. (δ⟨Q_M⟩ vs its AAV prediction: median ratio +1.06 — the *coordinate*
  shift does track Re⟨A⟩_w; only the momentum channel is broken.)
- Correlations across the grid: corr(δ⟨Q_M⟩, Re⟨A⟩_w) = +0.72,
  corr(δ⟨P_M⟩, Im⟨A⟩_w) = −0.63. Neither channel is clean; the momentum
  channel even has the wrong sign of correlation with Im⟨A⟩_w.

The AAV derivation of δ⟨P_M⟩ = 2λ·Var(P_M)·Im⟨A⟩_w assumes a standard Gaussian
pointer with [Q,P] = iI and the initial Gaussian in Q. The endogenous γM
pointer satisfies neither cleanly: the momentum channel built from the
maintenance layer does not reproduce the imaginary-weak-value shift.

## H-readout — FAIL (decisive)

δ⟨P_M⟩ does not recover the set g/J.

The root cause is geometric and unfixable by tuning: **Im⟨A⟩_w is a
non-monotone function of g/J.** Over g/J ∈ [0.02, 5.0] it rises from ≈ −0.17,
crosses zero near g/J ≈ 0.37, peaks (≈ +0.26) near g/J ≈ 1.1, falls back
through zero near g/J ≈ 2.0, troughs (≈ −0.21) near g/J ≈ 2.8, then rises
again. This is the Rabi phase winding of the two-level ABL geometry — a real
property, not a simulation artifact (confirmed on a 2000-point fine grid). A
non-monotone Im⟨A⟩_w means the same δ⟨P_M⟩ corresponds to up to **three**
different g/J values. The audit-pointer readout is fundamentally many-to-one.

Recovered-vs-set g/J (invert δ⟨P_M⟩ through the analytic Im⟨A⟩_w(g/J) curve;
the inversion uses no fit to the set values):

| set g/J | Im⟨A⟩_w | δ⟨P_M⟩ | recovered g/J | rel. error |
|--------:|--------:|-------:|--------------:|-----------:|
| 0.10 | −0.170 | +0.152 | 1.64 | 1537% |
| 0.20 | −0.105 | +0.091 | 0.55 | 174% |
| 0.35 | −0.011 | +0.015 | 0.40 | 13% |
| 0.50 | +0.074 | −0.045 | 0.29 | 42% |
| 0.75 | +0.184 | −0.091 | 3.35 | 347% |
| 1.00 | +0.246 | −0.045 | 0.29 | 71% |
| 1.50 | +0.207 | +0.134 | 1.69 | 13% |
| 2.00 | +0.017 | +0.096 | 1.80 | 10% |
| 3.00 | −0.202 | +0.052 | 3.65 | 22% |
| 4.00 | +0.274 | −0.296 | 0.02 | 100% |

Median relative error **57%**; **3/10** cells within the pre-registered 15%
tolerance. Tolerance requires ≥ 9/10. FAIL. The 3 cells that land near the
truth are coincidences of the non-monotone fold, not a working calibration —
neighbouring cells (g/J = 0.20 ↔ 0.35, 0.75 ↔ 1.00) recover wildly different
values from nearby δ⟨P_M⟩.

Two compounding faults: (1) the H-conjugate failure means δ⟨P_M⟩ already
mis-measures Im⟨A⟩_w; (2) even a perfect δ⟨P_M⟩ could not invert, because
Im⟨A⟩_w(g/J) is not injective. Fault (2) alone is fatal.

## H-noncollapse — PASS

At genuinely weak λ the measurement's own back-action is negligible. Isolating
back-action correctly (coupled ρ_n minus *bare* ρ_n at the same instant, not
ρ_n vs the corridor band — see the structural note below):

| λ | back-action on ρ_n |
|------:|------:|
| 0.0005 | 0.00003 |
| 0.001 | 0.00011 |
| 0.002 | 0.00044 |
| 0.004 | 0.00176 |
| 0.008 | 0.00695 |

Across the g/J grid at λ = 0.002, max back-action 0.0006. Well under the 0.02
tolerance. The weak coupling is genuinely weak; it does not disturb the system.
H-noncollapse passes — but it is the non-decisive hypothesis, and a measurement
that does not perturb the system is worthless if it also does not read it.

## Two structural findings the run forced out

**1. The unitary construction has no corridor.** The bare adjacent-rung
Hamiltonian H_sys is unitary; it has no α−γM steady state, only Rabi
oscillation. The pre-selected corridor state (ρ_n = 0.26) evolves under H_sys
alone — *no measurement at all* — and ρ_n sweeps the full [0, 0.5] range: at
the measurement instant ρ_n reaches 0.46–0.50 for every g/J ≥ 1. The "corridor"
is a property of the **dissipative** α−γM dynamics (Piece 2); a unitary von
Neumann weak measurement cannot host it. The pre-registration's H-noncollapse —
"the back-action keeps ρ_n in the corridor" — is therefore ill-posed for a
unitary construction: there is nothing keeping ρ_n in the corridor to begin
with. The honest version of H-noncollapse is "does the *coupling* perturb ρ_n",
and that passes; but the corridor itself is simply absent from the apparatus.

**2. The readout gain and the back-action are the same Var(P_M).** The AAV
formula δ⟨P_M⟩ = 2λ·Var(P_M)·Im⟨A⟩_w has Var(P_M) as the gain. But Var(P_M)
also sets the back-action scale (the disturbance is ∝ λ·√Var(P_M)). You cannot
make δ⟨P_M⟩ large enough to read while keeping back-action small — they are
governed by the same quantity. A weak measurement that uses P_M as both the
coupling generator and the readout channel is squeezed between unreadable
(small Var(P_M)) and collapsing (large Var(P_M)). λ = 0.04 looked "small" but
gave back-action 0.13; only λ ≤ 0.004 is genuinely weak, and there δ⟨P_M⟩ is
already mis-scaled by the conjugacy failure.

## Comparison to w3 (the blocked direct g/J observable)

w3 (`path23_pairB`) found the canonical timescale g/J **observable-blocked** at
the LLM substrate: 1/48 family-cells cleared the window-domination gate; the
cross-rung coupling g sat below its noise floor. w3's failure was *statistical*
— the direct relaxation-timescale observable was too noisy to resolve.

The audit pointer fails for a **different and deeper** reason. It is not a noise
failure — the simulation is exact (no sampling noise; A² = 0 makes the von
Neumann evolution closed-form). It is a **structural** failure: (a) the
endogenous γM pointer is not a canonical conjugate pair, so the AAV momentum
shift does not hold; and (b) Im⟨A⟩_w(g/J) is non-monotone, so even a perfect
δ⟨P_M⟩ cannot invert to g/J. w3 was blocked by noise; the audit pointer is
blocked by the geometry of the construction. **The audit-pointer observable
does not succeed where the direct one failed — it fails harder, because its
failure is in the apparatus, not in the data.**

## Honest assessment

The endogenous audit pointer is **not** a working measurement apparatus for the
cross-rung timescale g/J. The candidate "what replaces F-11" does not, on this
test, replace it.

The pre-registration named the exact way this could fail — "∂ρ_ss/∂γM < 0 is
monotonicity, not canonical conjugacy" — and that is the way it failed. The
framework's γM maintenance layer gives a *monotone* relation between audit
pressure and un-collapsed variance; it does not supply the canonical conjugate
pair the von Neumann / AAV machinery needs. Calling P_M "the pointer momentum"
and Q_M "the pointer coordinate" is a relabelling that the underlying dynamics
does not earn. Building P_M as a genuine momentum operator (the disciplined
choice — not relabelling a Gaussian) exposes this directly: the commutator is i
only in expectation, the AAV momentum shift comes out at −0.59× prediction.

Two further faults are independent of the conjugacy question and would sink the
construction on their own: the cross-rung two-level geometry makes Im⟨A⟩_w
non-monotone in g/J (no unique inversion), and a unitary weak measurement has
no corridor to preserve because the corridor is a dissipative-dynamics object.

A constructive route, if the framework wants to keep this direction: the
measurement would have to be built on the **dissipative** α−γM generator (a
Lindblad / open-system weak measurement with a genuine ρ_ss corridor), not on a
unitary two-level H_sys, and the pointer would need an honestly conjugate pair
rather than the γM monotonicity dressed as conjugacy. That is a different
construction, not a tuning of this one. As pre-registered, this construction
returns FAIL, and the FAIL is reported flat.

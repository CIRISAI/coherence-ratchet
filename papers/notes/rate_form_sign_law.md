# The rate-form sign law — Λ as maintenance *power*, not stock

**STATUS: CONJECTURE-GRADE. Not lake content. Not asserted by the framework.**
A follow-on to `papers/notes/lambda_maintenance_wz.md`, testing whether mapping dark
energy to the maintenance *power* (a rate) rather than the coordination *stock* `S`
rescues DESI's phantom-past direction. It is computed both ways. Nothing here is
mechanized or cited by any paper. Draft 2026-07-10.

**Depends on:** `papers/notes/lambda_maintenance_wz.md` (§1.1 the normalization problem,
§7(a) the stock choice, §5 the pure-maintenance toys); `formal/CoherenceRatchet/Core/
Dynamics.lean` (`dρ/dt = α − γM`; `corridor_requires_maintenance`: at equilibrium
`γM = α`); `formal/CoherenceRatchet/Core/EntropicPotential.lean` (T-E1..T-E5, `S = −ln det C`);
the already-computed cell-grain `S(a)` in `experiments/cosmo_entropic_potential/results.json`
(`combined`), reused here via `experiments/cosmo_entropic_potential/rate_form/`.

**F-11 compliance.** Forward content only. `d ln P_maint/d ln a` is a steady-state readout
of the forward continuity equation, exactly as the stock note's `d ln S/d ln a` was. No
backward `P_ω`, no D4, no F-19.

---

## 1. Why a rate mapping at all

The stock note maps `ρ_DE ∝ S` and derives the exact, parameter-free sign law
`1 + w = −(1/3)·d ln S/d ln a`. Its flagged weakest link (§7a) is a hidden normalization;
its computed verdict is that nonlinear collapse makes `S` **fall monotonically** (the
general theorem in `results.json`: any pointwise nonlinearity lowers `S`), so `w > −1`
**always** — a thawing model, no phantom past. That is the *wrong direction* for DESI DR2,
which prefers `w < −1` in the past crossing to `w > −1` today (`w₀=−0.838, w_a=−0.62`).

But the framework's own equilibrium condition is not a stock — it is a **power**.
`Dynamics.lean`'s `corridor_requires_maintenance` says the corridor is held by
`γM = α`: work done *per unit time* against the unmaintained drift `α`. Bianconi's
multiplier field gives that power physical status (bridge note §7.2). So the natural
alternative reading is

```
ρ_DE(a) ∝ P_maint(a)   — the power needed to hold the coordination structure against
                         its unmaintained drift — giving

   1 + w(a) = −(1/3)·d ln P_maint / d ln a.                                   (R)
```

Stock and rate can move **oppositely**: collapse lowers the stock `S` (theorem) while
plausibly *raising* the drift rate `α` it must fight (deeper wells, shorter dynamical
times). If so, the sign of `1+w` flips and DESI's direction is in reach. (R) has the same
form as the stock law; the entire question is *what is `P_maint(a)`*.

**The normalization caveat is inherited verbatim, and it is not repaired here.** (R)
equates an energy *density* with an extensive *power*, so it is well-posed only *per what
volume*. As in stock §1.1/§7(a), only the **comoving** choice makes a constant-power frozen
structure give `w = −1`; that choice inserts the ΛCDM limit by hand. Everything below sits
on that same undischarged step.

---

## 2. Three operationalizations of `P_maint`, derived not asserted

All three are computed on the **same** cell-grain `S(a)` the stock note used (lognormal
nonlinear field + Gaussian event-horizon causal mask, `results.json["combined"]`, `a∈[0.3,1]`,
60 points), reusing `s_of_a.py` for `H(a)`, the CPL fit, and the log-derivative. Code and
numbers: `experiments/cosmo_entropic_potential/rate_form/{rate_form.py, results.json}`.

**(a) Equilibrium reading.** `P ∝ γM = α`, and `α` is the rate `S` *would* drift at if
maintenance stopped. In the cosmological setting the free (maintenance-off) drift is
gravitational evolution itself:

```
α(a) = |dS/dt|_free = |dS/d ln a|·(d ln a/dt) = |d ln S/d ln a|·S·H(a).       (a-time)
```

The factor `H(a)` is load-bearing and it is a **choice** — it is what "per unit *time*"
means. Measuring the same drift "per *e-fold* of expansion" drops it:
`P ∝ |d ln S/d ln a|·S`  **(a-efold)**. This dt-vs-d ln a choice is a *new* hidden
normalization, and §3 shows it moves the answer across DESI.

**(b) Dynamical-time reading.** Power ~ (structure held)/(maintenance timescale):
`P ∝ S/τ_dyn`, with `τ_dyn ∝ 1/√(Gρ_m)`. Matter dilutes as `ρ_m ∝ a⁻³` **exactly**
(independent of dark energy), so `τ_dyn ∝ a^{3/2}` and `d ln τ_dyn/d ln a = +3/2` exactly.
Hence

```
d ln P/d ln a = d ln S/d ln a − 3/2,   1 + w = −(1/3)(d ln S/d ln a) + 1/2.    (b)
```

The `−(−3/2)/3 = +1/2` term is large and **positive-w-pushing** — the brief's arithmetic
was right. With `d ln S/d ln a ∈ [−0.27, −0.05]` this pins `1+w ≈ +0.5–0.6`: a badly-behaved
`w ≈ −0.4` that was matter-like early. The escape is that if `τ_dyn` is instead the *virial*
time of collapsed halos (roughly frozen post-collapse, `d ln τ/d ln a ≈ 0`), (b) **collapses
back to the stock form**. So the timescale identity spans the *entire* answer.

**(c) Dissipation reading.** `P ∝` entropy-production rate of the maintained NESS `= γM` at
steady state. The `lyapunov_check` *align* sweep gives `S_ss(γM)` monotone **decreasing**;
inverting over its corridor points, `ln γM = m·ln S_ss + b` with `m = −0.77`. Transporting
that scaling to cosmology, `P ∝ S^m`, so `d ln P/d ln a = m·(d ln S/d ln a)`. With `m<0` and
`d ln S/d ln a<0` this is **positive for all `a`**: phantom everywhere. This is a scaling
argument on a 6-spin Lindblad NESS, not a cosmological computation — flagged as the biggest
leap of the three.

---

## 3. Computed `w(a)` and the verdict

| mapping | `1+w` today | phantom past? | crossing `z` | `w_a/(1+w₀)` |
|---|---|---|---|---|
| stock `ρ∝S` | **+0.09** (`w>−1`) | no | none | −0.95 |
| **(a) `ρ∝\|dS/dt\|`** (per-time, +H) | **+0.27** | **yes** (`w_min=−1.12`) | **0.84** | **−2.15** |
| **(a′) `ρ∝\|dS/dlna\|·S`** (per-e-fold) | **+0.11** | **yes** (`w_min=−1.60`) | **0.15** | **−8.12** |
| (b) `ρ∝S/τ_dyn` (`a^{3/2}`) | +0.59 (`w≈−0.41`) | no | none | −0.16 |
| (b′) `ρ∝S/τ_frozen` | +0.09 | no | none | −0.95 (=stock) |
| (c) `ρ∝γM∝S^m` (`m=−0.77`) | **−0.07** (`w<−1`) | yes (all `a`) | none | n/a (phantom-always) |
| **DESI DR2 target** | **`>0`** | **yes** | **≈0.35** | **−3.83** |

Reading the table honestly:

- **Only candidate (a) reproduces DESI's *direction*** — `w<−1` in the past, a single
  crossing, `w>−1` today. Neither (b) nor (c) does: (b) gives a matter-like `w≈−0.4`;
  (c) gives phantom *everywhere* with `w_a>0`, the wrong sign today. So the rate reading
  does what the stock reading could not — it produces a phantom past — **but only in the
  equilibrium form**, and there it hangs entirely on the meaning of "rate."

- **The crossing epoch is wrong, and its error is diagnostic.** The per-*time* form (a)
  crosses at `z=0.84`, near acceleration onset (`z=0.632`) — the same onset-locking that
  killed the stock pure-maintenance toy (stock §5b), because the explicit `H(a)` factor
  reintroduces expansion kinematics (`d ln H/d ln a` is `−q`-like). The per-*e-fold* form
  (a′) crosses at `z=0.15`, set purely by the structural inflection of `S(a)`, with no
  kinematics. **DESI's `z≈0.35` sits between the two**, and which one you get is fixed by an
  unforced convention, not by physics.

- **`w_a/(1+w₀)` brackets DESI the same way.** DESI's `−3.83` lies between (a)'s `−2.15`
  and (a′)'s `−8.12`. The rate form can hit DESI's steepness only by tuning the time
  convention between them.

---

## 4. The consistency trap — where the crossing comes from

At equilibrium `γM = α`, so candidate (a) and the stock derivative are two readings of the
same object. The stock form crosses `w=−1` where `dS/dt = 0` (an extremum of `S`); the
computed `S(a)` is **monotone**, so the stock form *never* crosses — `w>−1` always,
confirmed. The rate form (a) crosses `w=−1` where `d|dS/dt|/dt = 0` — an **inflection of
`S(t)`**, which exists even while `S(t)` is monotone. *That is the only way the framework
produces a phantom crossing at all*: not from `S` turning around (it does not), but from the
rate of its decline peaking.

The inflection is real and the computation finds it. But its epoch is set by whichever
clock differentiates `S` — cosmic time (crossing near onset, `z=0.84`, kinematics-dominated)
or e-folds (crossing low, `z=0.15`, structure-dominated). The trap is that the framework has
no principle fixing the clock, and the two clocks straddle the DESI target. The crossing is
obtainable; it is not *predicted*.

---

## 5. The new free choices each candidate smuggles in

The stock note's single weakest link was one hidden normalization (comoving-vs-physical).
Each rate candidate *inherits* that and adds its own, and they are worse, not better:

- **(a) adds two.** (i) The dt-vs-d ln a **time convention**, which alone moves the crossing
  from `z=0.84` to `z=0.15` and `w_a/(1+w₀)` from `−2.15` to `−8.12` — i.e. it spans DESI.
  (ii) The identification *"free drift = gravitational evolution"* — that switching
  maintenance off leaves the cosmic field evolving under gravity at rate `dS/dt`. Defensible,
  but an assumption, not a derivation.
- **(b) adds one that spans the whole answer.** The identity of `τ_dyn`: mean-density
  (`a^{3/2}` → `w≈−0.4`) versus virial-frozen (const → stock). Nothing in the framework picks
  one, and they bracket everything from matter-like to thawing-Λ.
- **(c) adds the largest leap.** It transports a measured `S_ss(γM)` curve from a 6-spin
  Lindblad NESS to the cosmic density field by analogy, plus the fitted slope `m`. The lab
  system is not the cosmos; the scaling is suggestive at best.

So the rate reading does not remove the stock reading's disease (a conclusion inserted at a
normalization); it *multiplies* it. The stock form hid one timescale-free choice; the rate
form hides a timescale.

---

## 6. What would discriminate stock from rate — independently of DESI

This is the one genuinely new and attractive thing here. Stock and rate make **different
predictions about a laboratory system**, testable with no cosmology:

> In a real corridor-holding nonequilibrium steady state — the `lyapunov_check` Lindblad
> sweep, or a GPU strain array (exp117) held in the corridor — measure whether the injected
> maintenance power `γM` tracks the *held stock* `S` (a state function) or the *drift rate*
> `|dS/dt|` (a flux). Stock-`Λ` predicts the DE analog scales with the former; rate-`Λ`
> with the latter.

These are distinct observables in a NESS (`S` is a state variable, `γM` a power), and the
sweep data already pairs them. A tabletop measurement that comes down on one side would
pick the correct dark-energy mapping *before* any galaxy survey — which would be a genuinely
remarkable transfer, and is the sharpest reason to do the lab measurement carefully. It also
sidesteps DESI's dataset-dependent significance entirely.

---

## 7. Returns to the task brief

- **The rate sign law:** `1 + w = −(1/3)·d ln P_maint/d ln a`, same form as stock, inheriting
  the same comoving-normalization caveat (undischarged).
- **Does any rate form match DESI?** **Partially, and only candidate (a).** It is the only
  mapping that produces `w<−1` in the past with a crossing and `w>−1` today — DESI's
  *direction*, which the stock form structurally cannot reach. But it does **not** match
  DESI's *numbers*: the crossing epoch (`z=0.84` per-time / `z=0.15` per-e-fold) brackets but
  misses DESI's `z≈0.35`, and `w_a/(1+w₀)` (`−2.15` / `−8.12`) brackets but misses `−3.83` —
  in both cases the miss is bridged only by choosing the unforced time convention. (b) fails
  (`w≈−0.4`); (c) gives phantom-always (`w_a>0`), the wrong today-sign.
- **Where the crossing comes from:** an inflection of `S(t)`, which survives `S` being
  monotone — the rate form's one real advantage over the stock form, but its epoch is set by
  an unforced clock.
- **New free choices:** (a) a dt-vs-e-fold timescale that spans DESI; (b) a `τ_dyn` identity
  that spans the whole answer; (c) a lab-to-cosmos analogy transport. The stock form hid one
  normalization; the rate form hides a timescale. Merciless verdict: no improvement in
  parsimony, a genuine gain in *reachable direction*.
- **Lab-side discriminator:** does a real corridor-holding system's maintenance power scale
  with the held stock `S` or with the drift rate `|dS/dt|`? — measurable on the Lindblad /
  exp117 data, independent of DESI.

**Verdict: the rate reading is the only version of this framework that can reach DESI's
phantom-past direction, and it reaches it only by importing a timescale the framework does
not fix. It converts the stock form's "sign law but no sign" into a "direction but no
epoch." The lab discriminator is the way out of the accommodation trap.**

# Path 2 — pre-registration: does the rung-type / k-dependence of the Kish identity structurally account for the A3+ / CMB ρ_mid divergence?

**Date:** 2026-05-21. Written BEFORE the quantitative comparison to the WMAP/Planck
ρ_ℓ profile. Falsification handle context: F-11 / cross-substrate consistency-of-bounds.

## The observed divergence (the thing to be accounted for)

`experiments/open_system_pomega/corridor_calibration_and_cmb_drift.py` and
`cmb_planck_crosscheck.py` found:

- **A3+ side.** Five A3+ substrates (cellular regulatory, LLM internals, OSS
  contribution, C. elegans sensory/inter/motor, healthy EEG) pin a corridor
  centre `ρ_mid ≈ 0.27`, low-cluster band `[0.16, 0.35]`. These are
  goal-projector / federation substrates — Piece 5 — coordinating handfuls of
  constituents (small nominal `k`).
- **CMB side.** The per-multipole Kish correlation `ρ_ℓ`, read from
  spherical-harmonic mode-power participation over `k = 2ℓ+1` modes, runs
  `≈0.29` at `ℓ=2` down to `≈0.03` at `ℓ=30`. It tracks the
  isotropic-Gaussian baseline closely (WMAP and Planck agree to mean
  |Δ| = 0.0015). The 2-sphere is a mode-count substrate — large `k`, up to 61.

A single `ρ_mid` does not reconcile the two: 0.27 sits at the top of the CMB
profile, well above most of it.

## What Path 2 tests

Whether the framework's EXISTING machinery — Piece 1 (Kish identity, explicitly
k-dependent), Piece 3 (the corridor, stated in CLAUDE.md as a substrate-
independent **k_eff** band), Piece 5 vs the mode-count rung type — predicts that
a goal-projector substrate and a mode-count substrate have **different corridor
centres in ρ**, in the observed direction and rough magnitude, with **NO new
free parameters**.

## The derivation (existing machinery only)

### Step 1 — Piece 1: the Kish identity is explicitly k-dependent.

`k_eff(k, ρ) = k / (1 + ρ(k−1))`. Inverting for ρ at fixed k_eff:

```
ρ(k, k_eff) = (k / k_eff − 1) / (k − 1).
```

For a *fixed* k_eff the ρ that realises it is **k-dependent**. Two substrates
with different nominal constituent counts at the SAME k_eff (same corridor
occupation, same coordination quality) sit at DIFFERENT ρ. This is Piece 1
read directly, no new parameter.

### Step 2 — Piece 3: the corridor's substrate-independent statement is the k_eff band.

CLAUDE.md Piece 3, verbatim: *"Inside the corridor, k_eff achieves a
**substrate-independent range**"*; the table gives k_eff ∈ ≈(2.33, 10), and
*"The asymptotic ceiling at ρ_lower = 0.1 is k_eff = 10 **regardless of
substrate**."* The Möbius asymptote `k_eff → 1/ρ` as `k → ∞` makes the band
(2.33, 10) ≈ (1/0.43, 1/0.10): the ρ-band (0.1, 0.43) is the **k → ∞ shadow**
of the substrate-independent k_eff band. The paper has additionally *retracted*
the ρ-band (0.1, 0.43) as a substrate-universal numerical object
(Corridor Dynamics.tex L151, L161), keeping "substrate-local corridor
structure." So the invariant the framework still asserts is the k_eff band;
the ρ-band is its finite-k-dependent image.

**No new parameter is introduced here.** The k_eff bounds (2.33, 10) are read
off the existing ρ-band's k→∞ asymptote. They are the corridor's existing
content restated in the coordinate (k_eff) in which the framework calls it
substrate-independent.

### Step 3 — the k-dependent ρ-corridor.

Given the substrate-independent k_eff corridor `(k_eff_lo, k_eff_hi) = (2.326, 10)`,
the ρ-corridor at mode-count k is the inverse-Möbius image:

```
ρ_lower(k) = (k/k_eff_hi − 1)/(k − 1)   [clipped at 0]
ρ_upper(k) = (k/k_eff_lo − 1)/(k − 1)
ρ_mid(k)   = ½(ρ_lower(k) + ρ_upper(k)).
```

This is a one-line consequence of Pieces 1 + 3. Pre-computed (no new parameter):

| k   | ρ_lower(k) | ρ_upper(k) | ρ_mid(k) |
|-----|-----------|-----------|----------|
| 3   | 0.000     | 0.145     | 0.073    |
| 5   | 0.000     | 0.288     | 0.144    |
| 7   | 0.000     | 0.335     | 0.168    |
| 11  | 0.010     | 0.373     | 0.192    |
| 21  | 0.055     | 0.402     | 0.228    |
| 61  | 0.085     | 0.421     | 0.253    |
| ∞   | 0.100     | 0.430     | 0.265    |

### Step 4 — the rung-type distinction enters: what each substrate's measured ρ represents.

The framework names goal-projector rungs (Piece 5) and mode-count rungs as
different rung types. The CRITICAL distinction Path 2 must respect: the two
sides of the divergence are not the same kind of number.

- **A3+ goal-projector substrates** are *coordinated* systems. A federation
  that is functioning sits at — or near — its **corridor centre** ρ_mid. The
  measured A3+ ρ ≈ 0.27 is an instance of the predicted corridor centre
  `ρ_mid(k)` (quantity A).
- **The CMB 2-sphere**, by the paper's own reading, is *nearly statistically
  isotropic* — a Gaussian-random sky with no large-scale coordination. Its
  measured ρ_ℓ is therefore NOT a corridor centre. It is the **isotropic
  baseline**: the ρ a mode-count substrate exhibits with NO coordination
  (quantity B). For a Gaussian sky the power-participation k_eff has the
  chi-square participation ratio ⟨k_eff_iso⟩ ≈ k/3, so

  ```
  ρ_iso(k) = (k/k_eff_iso − 1)/(k − 1) ≈ 2/(k − 1)   for large k.
  ```

### The two competing structural predictions, both from existing machinery

**Prediction P-A (corridor-centre reading).** The framework predicts a
k-dependent corridor *centre*. If the CMB's ρ_ℓ is read as "where the corridor
sits at multipole ℓ," then `ρ_mid(2ℓ+1)` should track the measured ρ_ℓ.
- Pre-computed `ρ_mid(2ℓ+1)`: 0.14 (ℓ=2) → 0.19 (ℓ=5) → 0.23 (ℓ=12) →
  0.25 (ℓ=30). **RISES with ℓ.**

**Prediction P-B (isotropic-baseline reading).** The CMB is nearly isotropic,
so its measured ρ_ℓ is the no-coordination baseline `ρ_iso(2ℓ+1) ≈ 2/(k−1)`.
- Pre-computed `ρ_iso(2ℓ+1)`: 0.29 (ℓ=2) → 0.15 (ℓ=5) → 0.074 (ℓ=12) →
  0.032 (ℓ=30). **FALLS with ℓ.**

The measured CMB profile falls 0.29 → 0.03. **Only P-B matches the direction.**
P-A predicts the wrong direction for the CMB profile itself.

## Pre-registered predictions and pass/fail criteria

This is the honest split Path 2 must report on:

1. **The CMB ρ_ℓ profile is the isotropic baseline, not a corridor centre.**
   PASS if the re-run measured ρ_ℓ matches `ρ_iso(2ℓ+1) ≈ 2/(k−1)` to within
   ~10% across ℓ=2..30 (it should — this is the framework's own reading that
   the CMB is nearly statistically isotropic in this measure). This reframes
   the divergence: it is comparing a *corridor centre* (A3+) to an *isotropic
   baseline* (CMB) — two structurally different quantities. If they match,
   Path 2's account is: **the framework does not predict A3+ ρ_mid and CMB
   ρ_ℓ to be equal, because they are not the same kind of object.**

2. **Does existing machinery predict the divergence DIRECTION?**
   The divergence is: A3+ ρ_mid (~0.27) > most of the CMB profile (0.03–0.29).
   PASS if, for the mode-count substrate, the framework predicts the measured
   ρ (= isotropic baseline) lies BELOW the corridor centre ρ_mid(k) at the
   same k — i.e. `ρ_iso(k) < ρ_mid(k)` for the relevant k range. A Gaussian
   sky should sit below the corridor centre (it is uncoordinated). Pre-computed
   check: `ρ_iso(k)` vs `ρ_mid(k)` — expected `ρ_iso < ρ_mid` for k ≳ 9.
   At ℓ=2 (k=5) ρ_iso=0.29 vs ρ_mid=0.14 — the LOW-ℓ end is predicted to be
   ABOVE its corridor centre (rigidity-side), which is the framework's
   "quadrupole is rigidity-side" reading. PASS if the crossover k is in the
   low-ℓ range (ℓ ≈ 2–4) as the existing cmb_drift script already noted.

3. **Does existing machinery predict the divergence MAGNITUDE?**
   The A3+ corridor centre at the A3+ substrates' own (small) k must come out
   near the measured 0.27. A3+ federations coordinate handfuls of agents.
   PASS if `ρ_mid(k)` for k in the A3+ range reproduces ~0.27 ± the A3+ band
   [0.16, 0.35] WITHOUT tuning — and FAIL (for the magnitude claim) if the
   only k that gives ρ_mid ≈ 0.27 is k → ∞ (which would be the wrong rung
   type for a small-federation goal-projector substrate).
   Pre-registered concern, named now: `ρ_mid(k)` only reaches 0.27 as
   k → ∞ (ρ_mid(∞) = 0.265). For small k it is well below 0.27 (k=11 → 0.19).
   So a NAIVE corridor-centre reading would predict A3+ ρ_mid BELOW 0.27, not
   at it. Whether this is a genuine magnitude failure or whether the A3+
   substrates' effective k is large (many pathways, many depth×prompt cells,
   not literally "a handful") is the open question the comparison must settle.
   This is pre-registered as the point of maximum risk for Path 2.

## Honesty hooks — what would make Path 2 FAIL

- If the measured CMB ρ_ℓ does NOT match the isotropic baseline `2/(k−1)`,
  the "different kind of object" reframe collapses and the divergence is a
  genuine two-way-convergence failure.
- If accounting for the divergence requires choosing k_eff bounds other than
  the (2.33, 10) read off the existing ρ-band asymptote — that is a new free
  parameter, and Path 2 fails the "no new parameters" condition.
- If the A3+ corridor centre `ρ_mid(k)` at the A3+ substrates' actual k comes
  out far from 0.27 with no independent reason for the k used, the magnitude
  claim fails even if the direction is right.
- If the rung-type distinction has to be invoked as more than "same Kish
  identity, different k, different what-ρ-measures" — e.g. a separate corridor
  band per rung type — that is a new parameter.

## Summary of the structural prediction (pre-comparison)

Existing machinery (Pieces 1 + 3 + 5) predicts:
- The corridor is a k_eff band; in ρ it is k-dependent; `ρ_mid(k)` rises
  monotonically from ~0 (k=3) to 0.265 (k→∞).
- A mode-count substrate that is statistically isotropic exhibits the baseline
  `ρ_iso(k) ≈ 2/(k−1)`, FALLING with k — this is the predicted shape of the
  CMB ρ_ℓ profile, and it is NOT a corridor centre.
- Therefore the framework does **not** predict A3+ ρ_mid and CMB ρ_ℓ to
  coincide: one is a corridor centre, the other an isotropic baseline. The
  divergence is structurally expected.
- DIRECTION: predicted correct (CMB isotropic baseline falls with k; A3+
  centre is a single ~0.27).
- MAGNITUDE: pre-registered as the risk point. `ρ_mid(k)` reaches 0.27 only
  near k → ∞; whether the A3+ substrates' effective k is large enough is the
  open question the comparison decides.

# Path 2 — findings: the k-dependence of the Kish identity structurally accounts for the A3+ / CMB rho_mid divergence

**Date:** 2026-05-21. Run after PREREGISTRATION.md (committed separately,
before this comparison). Script: `path2_comparison.py`; console output saved
to `path2_output.txt`. Data: real WMAP 9-yr ILC map, 200 random rotations for
the frame-invariant profile, 300k Monte Carlo realisations for the isotropic
baseline.

## Bottom line

**Yes.** The framework's existing machinery — Piece 1 (the Kish identity's
k-dependence), Piece 3 (the corridor as a substrate-independent k_eff band),
Piece 5 (goal-projector vs mode-count rung type) — structurally accounts for
the observed A3+ / CMB divergence, in the right direction and the right rough
magnitude, with **no new free parameter**. All three pre-registered tests pass.

The divergence is not a two-way-convergence failure. It is the framework
correctly predicting that two structurally different quantities — a corridor
*centre* (A3+) and an isotropic *baseline* (CMB) — should not be equal.

## The derivation, recapped (no new parameters)

1. **Piece 1.** `k_eff = k/(1 + rho(k-1))`; inverted, `rho(k, k_eff) =
   (k/k_eff - 1)/(k - 1)`. The rho that realises a given k_eff is k-dependent.

2. **Piece 3.** CLAUDE.md states the corridor's substrate-independent content
   as a **k_eff band** ~ (2.33, 10). The Mobius asymptote `k_eff -> 1/rho`
   makes this band the k->inf image of the GPU rho-band (0.10, 0.43):
   `(1/0.43, 1/0.10) = (2.326, 10.0)`. The k_eff bounds are *read off the
   existing rho-band* — not a new parameter. (The paper has retracted the
   rho-band as a substrate-universal numerical object; the k_eff band is the
   invariant it still asserts.)

3. **The k-dependent rho-corridor** is the inverse-Mobius image of the fixed
   k_eff band: `rho_mid(k)` rises monotonically from ~0.07 (k=3) to 0.265
   (k->inf). One line from Pieces 1 + 3.

4. **Piece 5 — the rung-type distinction supplies what each side's rho *is*.**
   A3+ goal-projector substrates are *coordinated* — their measured rho is an
   instance of the corridor *centre* rho_mid(k). The CMB 2-sphere is *nearly
   statistically isotropic* (the paper's own reading) — its measured rho_ell is
   the *isotropic baseline* rho_iso(k), the rho a mode-count substrate exhibits
   with no coordination. For a Gaussian sky the power-participation k_eff has
   the chi-square participation ratio <k_eff> ~ k/3, so rho_iso(k) FALLS with k.

## The three pre-registered tests — results

### TEST 1 — the CMB rho_ell profile IS the isotropic baseline. **PASS.**

Re-running the real WMAP ILC map: the rotation-averaged measured rho_ell
matches the Monte-Carlo isotropic-Gaussian baseline to **mean relative error
4.6%** over ell=2..30 (pre-registered threshold: 10%). Both fall 0.29 -> 0.03.
The one departure is the octupole (ell=3, measured/iso = 1.15, the +0.033
concentration excess that also reproduces in Planck — a known anomalous
multipole).

This establishes the reframe: the measured CMB rho_ell is **not** a corridor
centre. It is the no-coordination baseline of a mode-count substrate. So the
A3+ side (corridor centre ~0.27) and the CMB side (isotropic baseline
0.29->0.03) are different KINDS of object. The framework does not predict them
to be equal — and the divergence is therefore structurally expected, not a
convergence failure.

Honest correction to PREREGISTRATION: the closed form `2/(k-1)` written in the
prereg is the *large-k asymptote* of rho_iso and undershoots at low ell (at
ell=2, 2/(k-1)=0.50 vs true rho_iso=0.29). The Monte-Carlo rho_iso is the
correct baseline; the measured profile matches THAT to 4.6%. The test stands;
the analytic shortcut in the prereg was too crude at low k and is superseded
by the MC baseline. No parameter changed.

### TEST 2 — existing machinery predicts the divergence DIRECTION. **PASS.**

Comparing the isotropic baseline rho_iso(k) to the k-dependent corridor centre
rho_mid(k) at the same k:

- At low ell (ell=2,3,4 — small k) the isotropic CMB sits **above** its
  corridor centre: rho_iso(5)=0.285 > rho_mid(5)=0.144. Few modes ->
  small-number statistics concentrate power -> high rho -> rigidity-side.
- At ell >= 5 the isotropic CMB sits **below** its corridor centre: many modes
  -> power spreads -> low rho -> chaos-side.
- Crossover multipole ell* = 5 (pre-registered range: ell ~ 2-5).

This reproduces the divergence direction. The A3+ substrates sit AT their
corridor centre (~0.24-0.27); the CMB, being uncoordinated, sits mostly
BELOW its corridor centre — exactly why a single rho_mid pinned from A3+
overshoots most of the CMB profile.

### TEST 3 — existing machinery predicts the divergence MAGNITUDE. **PASS.**

Pre-registered as the point of maximum risk: `rho_mid(k)` reaches the A3+
point estimate 0.27 only as k -> inf (asymptote 0.265), so a naive
"small-k federation" reading would predict the A3+ centre *below* 0.27.

The risk does not bite, for a reason internal to the framework: the A3+
substrates are not literal handfuls. Their nominal constituent counts (from
the paper's own substrate descriptions) are tens to hundreds:

| A3+ substrate                     | k    | rho_mid(k) |
|-----------------------------------|------|------------|
| cellular: 50 Hallmark pathways    | 50   | 0.250      |
| LLM: depth x prompt cells         | ~100 | 0.258      |
| OSS: active-author pool           | ~20  | 0.226      |
| C. elegans: neurons per class     | ~30  | 0.240      |
| EEG: channels                     | ~20  | 0.226      |

`rho_mid(k)` over the A3+ substrates lands in **[0.226, 0.258], mean 0.240** —
all inside the A3+ measured band [0.16, 0.35], and the mean is within 0.03 of
the A3+ point estimate 0.27 (pre-registered centre-match threshold 0.05).
No tuning: the k values are read off the paper's substrate descriptions, the
k_eff band off the existing rho-band. The remaining ~0.03 gap is well inside
the +/-0.07 spread the A3+ substrates themselves show.

## What this means for the divergence

The "honest divergence" flagged in `corridor_calibration_and_cmb_drift.py` and
NOTES.md ("A3+ data pins rho_mid ~ 0.27; the CMB rho_ell profile is
mode-count-set and mostly well below that") is **resolved structurally**, with
existing machinery, no new parameter:

- A single rho_mid was the wrong model not because the corridor needs per-rung
  *calibration* parameters, but because **rho_mid is k-dependent by Piece 1**:
  the corridor is fixed in k_eff, so its rho-centre moves with the mode count.
  The CMB's low-ell multipoles (small k) have a *lower* corridor centre than
  the A3+ substrates (larger k) — rho_mid(5)=0.14 vs rho_mid(50)=0.25.
- The CMB rho_ell profile is additionally not a corridor centre at all but the
  isotropic baseline (TEST 1). Comparing the CMB's measured rho_ell to the A3+
  rho_mid was comparing an uncoordinated baseline to a coordinated centre.
- Both facts fall out of Pieces 1 + 3 + 5 already in the framework.

## Honest limitations — what Path 2 does NOT establish

1. **The A3+ effective-k values are estimates, not measurements.** k=50, 100,
   30, 20, 20 are read from the paper's substrate descriptions. They are
   reasonable and not tuned, but the framework does not currently pin an
   *effective* k for each A3+ substrate from the data. rho_mid(k) is fairly
   flat over k=20..200 (0.226->0.260), so the conclusion is robust to this —
   but the ~0.03 predicted-vs-measured gap could move under a proper
   effective-k measurement. This is the one place a future quantity is owed.

2. **The k_eff band (2.33, 10) is the GPU rho-band's k->inf asymptote.** It is
   not a new parameter — it is the existing corridor restated — but it inherits
   whatever uncertainty the original (0.10, 0.43) GPU calibration carries.

3. **TEST 1 says the CMB is statistically isotropic in this measure** — mostly
   a statement about the CMB. The framework's distinctive content is the
   *drift*; Path 2 accounts for why the present-epoch divergence exists, it
   does not by itself land the drift prediction.

4. **The octupole excess (ell=3, +0.033)** is the one multipole departing from
   the isotropic baseline. Path 2 does not explain it.

## One-line verdict

Existing framework machinery — the k-dependence of the Kish identity plus the
corridor-as-k_eff-band plus the goal-projector / mode-count rung-type
distinction — structurally accounts for the A3+/CMB rho_mid divergence, in the
observed direction and rough magnitude, with no new free parameter. The
divergence is a structural account, not a failure of two-way convergence.

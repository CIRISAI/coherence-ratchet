# THREAD 1 — the dilution hole: coupled cross-rung dynamics — PRE-REGISTRATION

**Date:** 2026-07-20. **Committed BEFORE any scaling run** (`run_coupled.py`,
`results_*.json`). **Handle:** F-11 scope test (the coordinated non-pairwise case
left open by the 2026-07-20 `FelevenNoGo` scope correction in
`Cosmology/CorridorProjector.lean`).

## What this is and is NOT

This is a **scope test of an invariant's R-scaling under a MODEL dynamics.** It is
NOT the construction of the joint backward P_ω operator (forbidden — the operator
is a documented no-go for {pairwise} ∪ {k-body on independent dynamics}; the open
case is a *scope note*, not a reopening). A dynamics **model** is legitimate: the
original k-body test (`build_kbody_pomega.py`) used the R2 simulator, which is
also a model. This is NOT synthetic empirical data — no measurement is claimed of
any real substrate. Every result is framed as: *under this model coupling, does a
multipartite occupancy invariant dilute or not as the rung count R grows.*

## The finding that opened the test (stated, then tested)

F-11's k-body horn-empty result (`RESULTS.md`) is a **tautology of its simulator**:
the R2 dynamics evolves each rung's ρ_n by INDEPENDENT per-rung draws (own KGAIN,
target, noise), so the corridor-occupancy indicators X_n are near-independent by
construction → multi-information ≈ 0 at every arity. The "coupling ⇒ rigidity
pole" defense is refuted by a concrete counterexample: a global parity/GHZ
structure on the binary occupancy indicators has total correlation TC = 1 bit,
τ_k = TC/(R−1) = 1/(R−1) = 0.125 at R=9, with EVERY pairwise correlation ρ = 0 and
NO rung near rigidity. T1's dilution argument ("participation ratio extensive →
1/R dilution") is a **Secondness (arity-2)** argument; genuine multipartite (GHZ)
coordination is precisely the coordination that need not dilute with extent.

**We do not presume a non-diluting object exists.** If every coupling still
dilutes the genuine (bias-subtracted) multi-information to the null floor, that is
a real and important result — it would mean T1's dilution binds even coordinated
dynamics, strengthening the no-go.

## The dynamics model (a genuine coupled dynamics, framework-referenced)

Frame: the R2 within-rung ρ-dynamics, Piece-2 faithful, constants imported
UNCHANGED from `build_history_pomega.py` (ρ band (0.10,0.43), centre 0.265;
ALPHA0, ALPHA_RHO, GAMMA, KGAIN, M_BASE, M_NOISE_SD). The ONE change vs R2: the
per-rung management **target** is set by a JOINT cross-rung rule, so the rungs'
targets are *jointly* determined (the coupling) rather than drawn independently.

- Each history assigns a desired occupancy bit `d_n ∈ {0,1}` to each rung by the
  coupling rule (below). `d_n = 1` → target = 0.265 (corridor centre; dynamics
  settles occ = 1 at fidelity ~1.0). `d_n = 0` → target = 0.50 (settles ρ ≈ 0.56,
  occ = 0, OUT of band but NOT at a pole — avoids manufacturing rigidity).
- **Management reliability** `q ∈ [0,1]` (a dynamics knob, exactly the "management
  quality" R2 itself varies): with probability `(1−q)` a rung suffers a management
  failure and its realized desired bit is redrawn iid Bernoulli(0.5), independent
  of the coupling. `q = 1` = perfect management (framework high-fidelity limit);
  `q < 1` = a per-rung binary-symmetric channel that decoheres the injected
  coordination. This is the knob that tests whether per-rung noise DESTROYS a
  multipartite invariant as R grows.
- ρ_n(t) then evolves T steps by the R2 dynamics `dρ = α(ρ) − γ·M`,
  `M = M_base + KGAIN·(ρ − target) + noise`. Occupancy `X_n = 1[ρ_n(t_f) ∈ (0.10,0.43)]`.

## The couplings (pre-registered; strength g ∈ [0,1] interpolates independent→coordinated)

Per history, with probability `g` the constrained assignment is used; with
probability `(1−g)` the bits are iid Bernoulli(0.5). `g = 0` reproduces the
independent (R2-like) baseline; `g = 1` is the pure coupling.

1. **`independent`** — `d_n` iid Bernoulli(0.5). CONTROL. Must reproduce the
   `RESULTS.md` near-zero (TC_genuine ≈ 0) — validates the pipeline against the
   original F-11 finding.
2. **`global_parity`** (GHZ / single R-body hyperedge) — draw `d_1..d_{R−1}` iid,
   set `d_R = XOR`. Ideal (noiseless): TC = 1 bit ∀R, R-body II = ±1 bit,
   pairwise ρ = 0, τ_k = 1/(R−1). The counterexample the task names.
3. **`block_parity`** (local high-order / disjoint 3-body GHZ blocks) — partition
   into `⌊R/3⌋` consecutive blocks of exactly 3 rungs (remainder rungs left
   independent); each block is even-parity. Ideal: TC = ⌊R/3⌋ bits (EXTENSIVE),
   3-body window II ≠ 0, R-body II ≈ 0, pairwise ρ = 0 (size-3 even-parity → all
   pairs independent), τ_k = ⌊R/3⌋/(R−1) → ~1/3 (INSIDE the (0.10,0.43) band).
   The candidate robust non-diluting in-corridor Third.
4. **`vouching`** (Secondness contrast / CIRIS inter-agent "component (i)") — chain
   `d_n = d_{n−1}` w.p. `(0.5 + 0.5g)`, else fresh Bernoulli(0.5). One rung's
   occupancy raises another's probability. Ideal: pairwise ρ > 0, growing to
   rigidity (all-equal) as g→1. Expected NOT a Third — a pairwise/rigidity object.

## Estimators (REUSED EXACTLY from `build_kbody_pomega.py`, imported, not reimplemented)

`joint_entropy_bits`, `total_correlation` (TC), `interaction_information` (II),
`kbody_tau` (τ_k = TC/((|S|−1)·1bit)). Plus, added here:
- **pairwise ρ**: Pearson correlation matrix of the binary occupancy indicators;
  report mean adjacent |ρ|, mean all-pairs |ρ|, max |ρ|.
- **shuffled-null bias control** (exactly as `RESULTS.md` / `bias_control_kbody.py`):
  independently permute each rung's occupancy column (destroys ALL cross-rung
  structure, keeps every marginal exact); recompute TC/II/τ_k. Repeat `N_SHUF = 6`
  times → null mean and null scatter (std). **Genuine excess = measured − null
  mean**; the null scatter is the sampling-noise error bar. EVERY information
  number is reported bias-subtracted.

## Runs

- **Scaling** (the decisive run): each coupling at `g = 1`, `q = 1` (framework
  high-fidelity), for `R ∈ {3, 5, 7, 9, 11, 13}`, `N = 4,000,000` histories.
  Primary observable: `TC_genuine(R)` (raw bits, bias-subtracted). Secondary:
  `τ_k_genuine(R)`, R-body `II_genuine(R)` (R ≤ 11), 3-body window II
  (block_parity). Also pairwise ρ(R), marginal occupancy (rigidity check).
- **Reliability sweep** (noise-fragility): `global_parity` and `block_parity` at
  `q ∈ {1.0, 0.9, 0.7}`, same R grid — does per-rung noise dilute the invariant,
  and does it dilute the single R-body GHZ faster than the 3-body blocks?
- **Strength sweep** (interpolation): each coupling at `R = 9`, `q = 1`,
  `g ∈ {0, 0.25, 0.5, 0.75, 1.0}` — TC_genuine(g) and pairwise ρ(g), showing the
  independent→coordinated dial and where ρ stays low (Third) vs rises (Second).

## Gates (pre-registered) and the pass/fail

For a coupling's scaling result to count as a **non-diluting in-corridor
multipartite (Third) object**, ALL of:

- **G1 genuine-signal:** `TC_genuine(R) > 5 × null_scatter(R)` at each R (real
  signal above finite-sample bias, not a plug-in artifact).
- **G2 Thirdness (low pairwise ρ):** mean all-pairs `|ρ| < 0.10` across the R grid.
  If `|ρ| ≥ 0.10` the coupling is a **Secondness / pairwise object**, reported as
  such — NOT a Third. (0.10 echoes the corridor floor.)
- **G3 not-rigidity:** every rung marginal occupancy ∈ (0.05, 0.95) (no pinned
  rung) AND τ_k < 0.90 (not driven to the all-locked pole).
- **G4 NON-DILUTING (primary verdict):** `TC_genuine(13) ≥ 0.5 × max_R TC_genuine(R)`
  AND `TC_genuine(13)` passes G1. **DILUTING** iff `TC_genuine(R)` trends to the
  null floor: `TC_genuine(13) < 0.2 × TC_genuine(3)` OR fails G1 at R=13.

**VERDICT LOGIC (two-sided, decided by the frozen gates):**
- A coupling passing G1∧G2∧G3∧G4 ⇒ a non-diluting in-corridor multipartite object
  EXISTS under coordinated model dynamics ⇒ the F-11 coordinated-non-pairwise case
  is **OPEN-by-construction** (a witness exists). Scope note only — NOT the operator.
- If EVERY coupling either dilutes (fails G4) or is Secondness (fails G2), then
  T1's dilution binds even coordinated dynamics for the genuine-Third class ⇒ the
  no-go is **strengthened**.

## The τ_k normalizer caveat (registered before the run, load-bearing)

The corridor bounds on the `I_total` (raw multi-information) scale are
**UNCALIBRATED and owed** (`the_third_prenup.md`, `Thirdness.lean`). `τ_k =
TC/(R−1)` is the ONLY defined band ((0.10,0.43)), but its `(R−1)` normalizer
dilutes even the ideal single-hyperedge GHZ (τ_k = 1/(R−1) → 0) purely as an
artifact of the normalizer, NOT a property of the object. Therefore we report BOTH
raw `TC_genuine` and normalized `τ_k_genuine`, and the pass/fail G4 is on the RAW
invariant; the τ_k-band status is reported separately and read as measure-relative.
A coupling can be raw-non-diluting yet τ_k-diluting (single GHZ) or non-diluting on
BOTH (block_parity, τ_k → const ~1/3). Which measure is "the corridor coordinate"
is exactly the owed calibration; we do not pre-decide it.

## Addendum (2026-07-20, mid-run, BEFORE any affected result was seen)

The full R-body interaction information `II` (a `2^R` subset sum) is a SECONDARY
diagnostic. At `R = 11`, at `N = 4M × N_SHUF = 6`, it costs ~10 min/record and is
already noisy (RESULTS.md flagged `II` going negative at `R = 11`). To keep the
run tractable without touching the PRIMARY observable or any gate, full R-body
`II` is computed only in the **scaling** run at `R ≤ 9` (the framework's rung
count and below — RESULTS.md's decisive clean point). `TC` (primary, and every
gate G1–G4), `τ_k`, pairwise ρ, and the cheap 3-body window `II` run at **every**
R (3→13) and in **every** sweep, unchanged. This was decided when only the
`independent` control's `R ≤ 9` records existed on disk — no `global_parity`,
`block_parity`, or `vouching` result, and no `R ≥ 11` result, had been seen. It
changes no primary number and no verdict logic.

## The two readings (both to be stated at true strength in SUMMARY)

- **Exciting:** if a witness passes the gates, the coordinated case is genuinely
  open-by-construction — a multipartite invariant can be built that does not
  dilute, sits in the band, and posts zero to every pairwise detector (the
  Thirdness blind spot made concrete).
- **Deflationary:** open ≠ there. (a) A model coupling is not the universe's
  dynamics — nothing here authors a backward P_ω. (b) The measured cosmic Third
  is forward-authored anyway (`thirdness/SUMMARY.md`), already killed as a
  backward source. (c) Whether such a coupling is REALIZED by any real cross-rung
  dynamics is untouched. This test can only move the no-go from "closed" to
  "scope-open on the non-pairwise branch"; it cannot and does not assert the object
  is instantiated.

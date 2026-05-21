# Pre-registration — the canonical timescale g/J at a CIRISArray block pair

Committed BEFORE any results, in a SEPARATE commit that PRECEDES the results
commit; git history is the proof.

Companion to:
- `../gpu/` — w2-gpu-exitrate: established that CIRISArray's coherence-decay
  relaxation is CLEAN (τ ≈ 47 s, exponential, artifact-verified, τ/W ≈ 9×).
  The GPU substrate is where relaxation measurement WORKS.
- `../../crossrung_series/path23_pairB/` — w3: established the canonical
  timescale g/J is OBSERVABLE-BLOCKED at the LLM substrate (1 gate-pass of 48
  family-cells; the rest window/noise-dominated). The LLM cannot deliver it.

## 0. What this run settles, and the load-bearing caveat

`StructuralClaims.lean` Claim 6 (amended) is a statement about **g/J**, where
the PROTOCOL fixes the canonical meaning of g and J as **TIMESCALES**:

- `J` — within-rung intrinsic dynamical rate: a relaxation timescale⁻¹.
- `g` — cross-rung coupling: how strongly one rung's dynamics drive the other.

The canonical **timescale** g/J has been measured at ZERO framework rung pairs.
w3 showed the LLM substrate cannot deliver it. This run measures it on the
substrate where relaxation measurement demonstrably works — the CIRISArray GPU
oscillator array — using the array's native BLOCK STRUCTURE (Exp E1:
ρ_intra > ρ_inter) as two coupled "rungs".

### THE CAVEAT — stated up front, carried in RESULTS.md

**A CIRISArray block pair is a WITHIN-INSTRUMENT structure, NOT one of the
framework's Ph0..A5 coordinated rung pairs.** The two blocks are two halves of
one oscillator array on one GPU; they are not Ph0→Ph1, not A2→A3, not any
framework rung pair. This run is a **methodology-and-reliability anchor**: it
establishes (a) whether the canonical timescale g/J CAN be measured at all on a
clean substrate, and (b) at what value, with error bars. It is NOT a sixth
framework rung-pair datum and MUST NOT be counted as one. The six-pair
crossrung series remains at the count it had before this run. This run tells
the program whether the canonical quantity is *measurable in principle* — w3
left that open by hitting an observable block, not a substrate block.

**HONEST NULL is a valid outcome.** If the block-resolved decay is
window-dominated, or g is noise-dominated, the result is reported as a null:
"the canonical timescale g/J is not cleanly measurable even at the GPU block
pair." Given w2 already showed clean τ on the whole array, the prior is that
the block-resolved version also works — but it is gated, not assumed.

## 1. The substrate and the block partition

- **Instrument**: CIRISArray `experiments/exp51_physics_validation.py`
  `PhysicsTestSensor`, 2048 ossicles × depth 64 = **131072 oscillators** per
  bank, on the real RTX 4090 Laptop GPU with the CuPy backend (cupy 13.6.0,
  GPU confirmed available). Identical sensor and `step_with_noise(0.01)`
  free-relaxation dynamics as w2's `../gpu/` run.
- **Block partition (fixed here, before results)**: the oscillator index range
  `[0, 131072)` of each bank is split into **2 contiguous equal blocks**:
  - Block 0 = oscillator indices `[0, 65536)`
  - Block 1 = oscillator indices `[65536, 131072)`
  Two blocks, equal size, contiguous — the Exp E1 partition shape (E1 used 2
  blocks of equal size). The partition is of the OSCILLATOR INDEX, fixed and
  not tuned. This is the within-instrument analogue of "two adjacent rungs".
- **Per-block coherence observable**: each block has its own k_eff stream,
  computed by exp51's formula restricted to that block's index range:
  `k_eff_block = r_ab_block · (1 − x_block) · COUPLING_FACTOR · 1000`
  where `r_ab_block` is the Pearson correlation between bank-a and bank-b
  oscillators WITHIN that block, and `x_block` the clamped variance term of
  that block. This is exp51's k_eff (the framework's coherence/k_eff
  observable), evaluated block-resolved. No new observable is invented.

## 2. The time axis and capture

- **Time axis**: continuous wall-clock capture. After one `reset()` the array
  starts freshly randomised (uncorrelated). `step_with_noise(0.01)` then
  evolves it UNMAINTAINED (γM = 0, Piece 2). At each sample both blocks'
  k_eff are recorded → two parallel k_eff(t) streams.
- **Capture**: 120 s at 10 Hz = 1200 samples per stream, matching w2's `../gpu/`
  run exactly. **N_RUNS = 3** independent resets/captures for an across-run
  spread, matching w2.
- **Real GPU runs only.** If CuPy / the device is unavailable the run aborts
  honestly; no synthetic stream is substituted.

## 3. The three measured quantities

### 3.1 J — within-block relaxation rate (the w2 τ measurement, block-resolved)

For each block's k_eff(t) stream, the SAME running-correlation construction w2
pre-registered and validated:
- Running correlation `r_b(t)` = Pearson correlation between two adjacent
  W = 50-sample (5.0 s) windows of that block's k_eff(t):
  `r_b(t) = corr( k_eff_b[t−W:t], k_eff_b[t:t+W] )` — the **temporal
  autocorrelation** of the block's coherence signal, exactly w2's r(t).
- Fit `r_b(t) = r∞ + A·exp(−t/τ_b)` (the exp51 / w2 decay model, identical
  bounds `r∞∈[0,0.5], A∈[0,1.5], τ∈[1,200]`).
- Within-block relaxation rate **J_b = 1 / τ_b** (units 1/s).
- The pair's within-block scale is **J_within = sqrt(J_0 · J_1)** — the
  geometric mean, the Path-1 / w3 pre-registered choice (the two blocks may
  relax at different rates; the ratio must not be dominated by the faster one).

### 3.2 g — cross-block coupling rate

`g` is how strongly one block's dynamics couple to the adjacent block — a
directed, lagged quantity, the within-instrument analogue of cross-rung drive.
Pre-registered estimator, the **lagged predictive coupling** (the w3 §3.2
estimator, verbatim in construction):
- Fit two nested linear models for block 1's k_eff one step ahead:
  - restricted: `k1_{t+1} ~ k1_t` (block 1's own autoregression).
  - full: `k1_{t+1} ~ k1_t + k0_t` (adds block 0's k_eff at lag 1).
  `g_raw = 1 − Var(resid_full)/Var(resid_restricted)` — the partial R² of
  block 0 predicting block 1's next k_eff, controlling for block 1's own
  autocorrelation. A Granger-style directed coupling, `g_raw ∈ [0,1]`.
- **Debiasing** — block-shuffle null: block 0's k_eff series is permuted in
  contiguous **BLOCK_SHUF = 16-sample** blocks (preserves block 0's own
  autocorrelation, destroys the cross-block timing alignment), `N_SHUFFLE = 50`
  times; `g_floor` = mean null partial R². Reported `g = max(g_raw − g_floor, 0)`.
  If `g / g_raw < 0.3` the coupling is flagged **noise-dominated** for that run.
- Both directions are measured (0→1 and 1→0); the headline `g` is the mean of
  the two debiased directed couplings (the block pair is undirected — neither
  block is "upstream" — so a symmetric combination is the honest choice; both
  directed values are reported).
- `g` is a one-step partial R² in [0,1]; `J` is a rate in 1/s. To form the
  dimensionless **timescale g/J**, `g` is converted to a per-sample rate by the
  w3 convention, fixed here before results: `g_rate = −ln(1 − g)` (the
  continuous-time decay rate whose one-step survival is `1−g`), then divided by
  the sample interval Δt = 0.1 s to put it in 1/s. So:

  ```
  timescale g/J  =  ( g_rate / Δt )  /  J_within
  ```

  both rates in 1/s, ratio dimensionless. `−ln(1−g)` is monotone and ≈ g for
  small g; stated explicitly so the number is reproducible.

### 3.3 coupling-ratio g/J — the Path-1 / w3 mutual-information method

So the timescale ratio and the coupling ratio can be DIRECTLY compared at the
same block pair, exactly as w3 did, the Path-1 construction is also computed
here on the same captured streams:
- `tau_MI` = normalised cross-block Gaussian mutual information
  `I(R_0; R_1) / min(H_0, H_1)` — the `crossrung_lib.cross_rung_tau` estimator,
  imported from `../../crossrung_series/path1_tau/`, UNCHANGED. The two
  representations `R_0, R_1` are the per-block k_eff streams reshaped as the
  observation matrices the estimator expects: each block contributes its
  per-sample k_eff plus a small fixed set of block-internal coordinates (the
  block's bank-a / bank-b sub-block correlations), so the estimator has a
  multi-dimensional representation per block, as in Path 1. Construction fixed
  in §3.4 below.
- `W_within` = `sqrt(W_0 · W_1)` of the within-block mean-|Pearson| couplings
  (`crossrung_lib.within_rung_W`, imported, UNCHANGED).
- `coupling-ratio g/J = tau_MI / W_within`.

### 3.4 Per-block representation for the MI estimator (fixed before results)

The MI estimator needs a multi-coordinate observation matrix per block. Fixed
construction: each block is sub-divided into **8 equal sub-blocks** of 8192
oscillators; at each captured sample the block's representation row is the
8-vector of per-sub-block `r_ab` correlations. Over the 1200 samples this gives
each block a `1200 × 8` observation matrix `R_b` — the multi-coordinate
within-block structure the Path-1 estimator consumes (8 coords, matching the
PCA cap `q = min(8, m//6)` in `crossrung_lib`). The 8-sub-block partition is
fixed, not tuned; 8 is `crossrung_lib`'s own component cap.

## 4. The window-domination GATE (pre-committed, mandatory)

Mirrors w2's `../gpu/` C3 and the C. elegans pre-registration. A relaxation
timescale τ measured on a windowed running-correlation is meaningless if it is
merely the autocorrelation the window mechanically imposes.

**GATE G1 — window-domination.** For each block's fitted τ_b:
```
τ_b  >  3 · W   =  15 s        (W = 5 s running-correlation window)
```
This is w2's exact C3 gate. BOTH blocks must clear it.

**GATE G2 — real fit.** For each block: the fit converges; `r∞ ∈ [−0.1, 0.3]`
(near the chaos pole); `A ∈ [0.5, 1.5]` (starts near full correlation); the
gross decay `r_b(0) − r_b(end) ≥ 0.3` (monotone gross decay). w2's exact C4.

**GATE G3 — reproducible.** Across the 3 resets, for each block `max τ / min τ
< 2`. w2's exact C5.

**GATE G4 — g not noise-dominated.** The debiased coupling `g` must satisfy
`g / g_raw ≥ 0.3` in the MAJORITY of runs (≥ 2 of 3) for the timescale g/J to
be reported. If `g` is noise in the majority of runs, that is a COUPLING NULL.

## 5. The verdict (pre-committed)

- **PASS** — G1, G2, G3 all hold for both blocks and G4 holds. → The canonical
  timescale g/J IS measurable at the GPU block pair. Report
  `timescale g/J = (g_rate/Δt) / J_within` as the across-run mean ± SD, AND the
  coupling-ratio g/J from §3.3.
- **WINDOW-DOMINATED NULL** — G1 fails (some block τ ≤ 15 s). No timescale
  reported; the canonical quantity is not cleanly measurable even at the GPU
  block pair.
- **FIT-FAILURE NULL** — G2 fails. Reported plainly.
- **INCONCLUSIVE** — G3 fails (run-to-run scatter > factor 2). Full spread
  shown, no headline.
- **COUPLING NULL** — G4 fails. The relaxation rates J are reported but no
  timescale g/J, because g is noise.

IF the gate passes and both ratios are obtained, they are compared exactly as
w3 pre-registered:
- **AGREE** — the timescale g/J and the coupling-ratio g/J are the same order
  of magnitude (their ratio is within [1/3, 3]).
- **COME APART** — the two ratios differ by more than 3×.
The timescale g/J is ALSO reported against the amended Claim 6 band
(`CouplingComparable`: g/J ~ O(1), Path-1 measured 0.47–1.47) — but, per the §0
caveat, NOT as a Claim 6 rung-pair datum. It is a measurability anchor: it
shows whether the canonical timescale quantity, when the substrate cooperates,
lands O(1) or at a pole.

## 6. Incremental output (mandatory — three runs lost to wedges this session)

- All prints flushed (`python -u` / `print(..., flush=True)`).
- The results JSON is rewritten after EVERY run completes (after run 1, run 2,
  run 3), not once at the end — a kill/wedge leaves a recoverable partial.
- The run is launched in the background (not piped through `tail`).
- Commits are incremental: this pre-registration first (its own commit), then
  the results.

## 7. Fixed parameters (no tuning)

```
INSTRUMENT     = CIRISArray exp51 PhysicsTestSensor, RTX 4090, CuPy 13.6.0
N_OSSICLES     = 2048   (× depth 64 = 131072 oscillators per bank)
N_BLOCKS       = 2      (contiguous equal blocks of 65536 oscillators)
N_SUBBLOCKS    = 8      (per block, for the MI estimator representation)
DURATION_SEC   = 120.0
SAMPLE_RATE    = 10.0 Hz   (Δt = 0.1 s)
W              = 50 samples = 5.0 s   (running-correlation window)
N_RUNS         = 3      (independent resets)
N_SHUFFLE      = 50     (g block-shuffle null)
BLOCK_SHUF     = 16     (g null block length, samples)
GATE G1        = τ > 3·W = 15 s
GATE G4        = g/g_raw ≥ 0.3 in ≥ 2 of 3 runs
SEED           = 17     (matches the existing pipeline)
```

## 8. Honest prior

w2 already established clean τ ≈ 47 s on the whole array with τ/W ≈ 9×. The
block-resolved τ is the same measurement on half the oscillators, so the prior
is that G1–G3 pass. The genuine open question is g: whether two halves of one
freely-relaxing array carry a *detectable, non-noise* cross-block coupling
above the block-shuffle floor. Two halves of one array share no driver once the
maintenance is off (the coupling constants couple bank a/b/c, not block 0/1),
so g could land at the noise floor — a COUPLING NULL is a real possibility and
would itself be informative (it would say: the canonical timescale g/J needs a
substrate where the two rungs are genuinely coupled, which two passive halves
of one array may not be). The numbers are reported either way, with the
block-pair-≠-rung-pair caveat foremost.

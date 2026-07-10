# Self-consistency loop: closing S(a) ↔ H(a) — the fixed point is ~where the open loop was

**Date 2026-07-10.** Companion to `../epoch_check/` and `../halo_grain/`; motivated by the
one-ledger pressure test (`papers/notes/one_ledger_pressure_test.md` §"what survives"): the
published pipeline measured S(a) in boxes evolved under a **fixed ΛCDM background**, then mapped
`ρ_DE ∝ S(a)` — but that mapping's own background is *not* ΛCDM, so the pipeline was open-loop.
This experiment closes the loop and asks the pre-stated question: **does the fixed point move
toward or away from DESI?**

## Method

Fixed-point iteration on the pooled 6-box B-total curve (the published headline object):

1. `E²_i(a) = Ω_m a⁻³ + (1−Ω_m)·S_i(a)/S_i(1)` (the stock mapping, unchanged).
2. Linear growth `D_i(a)` under `E_i`: ODE in ln a, smooth DE, `D → a` early
   (**fixed primordial amplitude** — the CMB-anchored normalization; σ8 today is an output).
3. Halo-count response via the Sheth–Tormen cumulative mass function:
   `R_i(a) = N_ST(>10¹¹; σ·g_i(a)) / N_ST(>10¹¹; σ)`, `g_i = D_i/D_ΛCDM` (both early-normalized).
4. `S_{i+1}(a) = S⁰(a)·R_i(a)^η` — only the extensive k-channel responds (η = dlnS/dlnk; T-E3
   `S ≈ k·s̄` ⇒ η = 1 headline; 0.5/1.5 sensitivity). The per-unit geometry s̄ is held fixed:
   bias and growth cancel exactly in the normalized C (halo_grain's governing theoretical point),
   so its background response is second order.
5. Project the fixed point through the **identical** CPL machinery (`cpl_projection.py` functions
   lifted verbatim; mock DESI DR2 BAO + CMB θ\* distance fit, Ω_m = 0.3155 convention).

**Response-model validation (the load-bearing check).** ST count shape vs the box's measured
k(a) at the 10¹¹ threshold, both normalized to a=1:

```
a           :  0.25  0.30  0.37  0.42  0.49  0.56  0.65  0.75  0.87  1.00
N_ST/N_ST(1):  0.65  0.86  0.99  1.05  1.08  1.09  1.07  1.05  1.03  1.00
k_meas/k(1) :  0.60  0.82  0.95  1.02  1.09  1.09  1.05  1.04  1.02  1.00
```

Global log-slopes 0.23 (ST) vs 0.28 (measured); **the non-monotonic peak at a ≈ 0.55 and the
late ~9% decline are reproduced** — the feature I expected the model to miss, it captures,
because at this threshold growth moves mass *through* 10¹¹ into larger halos. The same physics
gives the response its locally counterintuitive sign today: `dlnN/dlng ≈ −0.34` at a=1
(suppressed growth ⇒ slightly *more* 10¹¹-scale halos).

## Result

**Convergence: 2 iterations** (max|Δln f_shape| < 6×10⁻⁶ at it. 2). The feedback is weak and
damping: the framework background suppresses growth by only **g(1) = 0.987** (−1.3% by today;
the DE deviation lives at z ≲ 1 and integrated growth barely notices), giving |R−1| ≤ 0.4%
across the whole range.

| projection | open loop (published) | fixed point (η=1) | Δσ |
|---|---|---|---|
| dist BAO+CMB | (−0.784, −0.442) **2.42σ** | (−0.788, −0.436) **2.37σ** | −0.05 |
| ρ_DE-weighted | (−0.777, −0.531) **2.03σ** | (−0.781, −0.522) **1.98σ** | −0.05 |
| w-space (DE-wtd) | (−0.786, −0.519) **1.89σ** | (−0.789, −0.512) **1.85σ** | −0.04 |
| ΛCDM (anchor) | 3.28σ | 3.28σ | — |

(Open-loop row reproduces `cpl_projection_results.json` exactly — pipeline-identity check
passed.) Physical crossing unmoved: z = 0.917 → 0.918.

- **η-sensitivity:** 2.39σ (η=0.5) / 2.37σ (η=1) / 2.34σ (η=1.5) — monotone, small.
- **Per-box fixed points (η=1, dist):** w₀ = −0.783 ± 0.091, wₐ = −0.462 ± 0.294; Mahalanobis
  0.35σ (CV_3) to 5.63σ (CV_5). The 25 Mpc/h cosmic variance dominates the self-consistency
  correction by ~30×, as expected.

## Verdict

1. **The loop closes, converges immediately, and the fixed point sits ~where the open loop
   was.** The self-consistency correction is a ≤0.4% perturbation to the S(a) shape → ~0.004 in
   w₀, ~0.009 in wₐ. **The published ~2σ, closer-than-ΛCDM result was not an artifact of the
   open loop.**
2. **Direction: toward DESI**, in every projection and every η — by ~0.05σ. Real but far below
   cosmic variance; quoted as a direction, not a detection. The self-consistent system does not
   run away, oscillate, or degrade the fit: the coupled gravity ↔ ledger dynamics is
   **near its fixed point already**.
3. This is "derive the ledger dynamics" in the only sense that survived the one-ledger pressure
   test — the closed causal loop gravity → clustering → S → H → gravity — and its first output
   is a stability statement: the mapping is self-consistent to sub-percent at 25 Mpc/h.

## Caveats (honest)

- **Response model is formation-channel only** (ST ratio on the extensive k), validated on shape
  against measured k(a) but still a model; s̄ held fixed (second order by the bias-cancellation
  argument, not by measurement); η is an assumption with a sensitivity band, not a measurement.
- **Smooth DE in the growth ODE** (no DE perturbations; c_s² unexamined — same open flank as
  `lambda_maintenance_wz.md` §7c). Radiation omitted (identical in both backgrounds; cancels in
  g to first order).
- **Everything rides on the 25 Mpc/h boxes and the 2-point proxy C** — the correction being
  small does not launder those; the pre-registered large-volume test remains the decider.
- The normalization choice (fixed primordial vs fixed σ8-today) flips the *sign* of g's shape;
  fixed-primordial is the physically correct anchor for a self-consistency statement (initial
  conditions fixed, late growth is the output), and the magnitude is sub-percent either way.

## Files

`selfconsistency.py` · `results.json` (incremental writes: S⁰ pooled, ST validation, per-iteration
history, projections, η-sensitivity, per-box fixed points). Runtime ~7 s (halo cache warm).

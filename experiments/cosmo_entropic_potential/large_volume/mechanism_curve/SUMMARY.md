# The mechanism curve — S-peak tracks the halo-count peak across the threshold dial

**Date 2026-07-10.** Densifies the mechanism check of `../SUMMARY.md` (3 points) into a
measured curve on TNG300-1 (205 Mpc/h, data on disk from the large-volume test): 12 log-spaced
thresholds, 7.4×10¹¹ → 2×10¹³ M⊙/h, frozen B-total estimator (GPU, gate-validated pipeline).
Figure: `mechanism_curve.png`. Data: `results.json`, `raw_Sa.json`.

## Verdict

**Mechanism CONFIRMED as a curve.** Over the 9 thresholds with an interior S peak, the S-peak
epoch tracks the above-threshold halo-count peak epoch at **correlation 0.948, RMS Δz = 0.088**
— the crossing epoch is the halo-formation turnover, across the whole resolved threshold range,
not just at the frozen rule's selection.

| threshold (M⊙/h) | z_Speak | z_kpeak | w_today |
|---|---|---|---|
| 7.4×10¹¹ (frozen rule's selection) | 0.590 | 0.546 | −0.833 |
| 1.0×10¹² | 0.472 | 0.329 | −0.849 |
| 1.4×10¹² | 0.436 | 0.329 | −0.865 |
| 1.8×10¹² | 0.462 | 0.329 | −0.770 |
| 2.5×10¹² | 0.135 | 0.153 | −0.737 |
| 3.3×10¹² | 0.188 | 0.153 | −0.770 |
| 4.5×10¹² | 0.131 | 0.153 | −0.697 |
| 6.0×10¹² | 0.099 | 0.0 | −0.910 |
| 8.1×10¹² | 0.063 | 0.0 | −0.747 |
| 1.1×10¹³ | **none** | 0.0 | −1.088 |
| 1.5×10¹³ | **none** | 0.0 | −1.072 |
| 2.0×10¹³ | **none** | 0.0 | −1.245 |

- **The K3 boundary in threshold space:** the interior S peak disappears between
  **8.1×10¹² and 1.1×10¹³ M⊙/h**. The frozen resolved-corner rule selects 7.4×10¹¹ —
  more than an order of magnitude on the safe side. Above the boundary the pipeline
  yields a phantom w_today (−1.1 to −1.2) with no crossing, exactly the K3 configuration
  anticipated in `../DECISIONS.md` — realized only at thresholds the rule does not select.
- **The threshold dial, quantified:** w_today spans **[−1.25, −0.70]** across the ladder.
  The dial is real and large; the frozen rule is what disciplines it.

## The ST overlay — pure mass-function theory predicts NO count peak (and that matters)

The first-pass theory column (argmax dn/dt, "peak assembly epoch," z ≈ 2.8–3.2) was the wrong
object for a *count turnover* and is retained only as a labeled trend line. The correct
pure-theory comparator, the ST cumulative count n_ST(>M, a) under ΛCDM growth, is **monotone
rising to within ~1%** (turnover depth ≥ 0.99 — no real interior peak), while the simulation's
k(a) turnover is several times deeper. **Pure Sheth–Tormen predicts no interior count peak;
the observed peak is merger/absorption-driven** — i.e., the S-peak the w(z) result rides on is
genuinely nonlinear content, invisible to the mass-function-only description, and the empirical
k(a) is the only valid tracking comparator. (This also explains why the selfconsistency loop's
ST response model — which captures formation, not mergers — was validated on the *ratio*, not
the turnover.)

## Caveats

- **z-grid quantization:** 10 snapshots make z_peak coarse; the z_kpeak plateaus at 0.329,
  0.153, and 0.0 are grid artifacts, and part of the RMS Δz = 0.088 is quantization, not
  physics. The fine-grid run (`../fine_grid/`) is the fix at the primary threshold.
- Single box, single cosmology; frozen estimator conventions inherited (2-point proxy C,
  R_smooth = 1.0); thresholds below the corner not computable at exact-det scale (the
  ladder runs upward only).
- `w_today` per threshold is a spline endpoint slope on 10 points — indicative, not
  jackknifed (only the primary threshold carries error bars, in `../results.json`).

*(Summary written by the orchestrating session from the agent's completed results.json —
including its corrected ST treatment — after the agent idled; all numbers are the agent's
executed output.)*

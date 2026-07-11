# Measured-C proxy upgrade — estimator decisions, fixed BEFORE any S or w

**Date 2026-07-10. Status: decisions record, written before any measured-C S(a) or w value
existed.** This file exists because the estimator design is the load-bearing choice and must be
frozen before results are seen, exactly as `../large_volume/DECISIONS.md` froze the model-C run.

## What this upgrade changes, and what it deliberately does NOT

The frozen pipeline (`../halo_grain/halo_grain.py::op_B`, `../PREREGISTRATION.md`,
`../large_volume/run_test.py`) builds the coordination matrix from a **MODEL** two-point function:

```
C_ij = xi_R(r_ij) / sigma2_R ,   C_ii = 1
```

where `xi_R` is the eh98-P(k), tophat-smoothed (`R_smooth = 1.0` Mpc/h) matter correlation
function (`s_of_a.xi_spline`), evaluated at the REAL TNG300-1 halo positions. That model-xi is the
"2-point proxy" caveat carried by every headline. **The only change here: replace the model
`xi_R(r)` with the MEASURED correlation function `xi_hat(r)` of the same above-threshold halos,
measured per snapshot from the same catalog.** Everything downstream is held byte-identical:

- **Same snapshot grid**: `[25,30,36,42,49,56,65,76,87,99]` (z = 3.008 … 0.000), the frozen grid.
- **Same corner threshold**: `thr_corner = 7.4253e11 Msun/h` (read from
  `../large_volume/results.json::stage0`, selected there by the frozen count rule — NOT reselected
  here). Same point set, same k(a) = [8606 … 38000 … 35818].
- **Same estimator for S**: `S = -Σ ln λ(C)`, computed by the SAME GPU fp64 in-place blocked
  Cholesky log-det (`S_gpu` / `_cholesky_inplace`, copied verbatim from `run_test.py` — NOT
  imported). The measured xi enters `S_gpu` only through its interpolation table `(xr, xv)`.
- **Same sign law + analysis**: `1+w = -(1/3) dlnS/dlna` (`s_of_a.dln_dlna`), the same CPL
  projection machinery (`epoch_check/cpl_projection.py`), and the same real DESI DR2 BAO
  likelihood (`desi_likelihood_v2/likelihood_fit.py`), with only S(a) swapped.

So the reported shift in (w0, wa, crossing, chi2) IS the proxy → measured systematic, isolated.

## (1) Measuring xi_hat(r) — per snapshot, at the corner threshold

Halos with `m200 > thr_corner` in the periodic box (L = 205 Mpc/h). Pair counts DD(r) in log-r
bins via minimum-image periodic distances, computed in CPU tiles (rows × all cols; the diagonal
self-distances are 0 and fall below r_min, so they are excluded naturally). **Ordered** pair
counting (both (i,j) and (j,i)); the analytic RR is ordered to match.

**Periodic-box analytic RR** (no random catalog needed): for N points uniform in volume V=L^3, the
expected number of ordered random pairs with separation in shell [r_lo, r_hi] is
```
RR(bin) = N*(N-1) * V_shell / V_box ,   V_shell = (4/3)π (r_hi^3 - r_lo^3) ,  V_box = L^3 .
```
**Natural estimator**: `xi_hat(bin) = DD(bin)/RR(bin) - 1`. `xi_hat > -1` always (DD ≥ 0).

**Bins (fixed now):** 32 log-spaced bins over r ∈ [0.1, 102.5] Mpc/h. `r_max = L/2 = 102.5` is the
largest separation for which the inscribed-sphere shell volume is exact under the periodic RR
formula (for r > L/2 the analytic shell volume overcounts the available volume). `r_min = 0.1` sits
below the halo-exclusion floor (M200c ≳ 7e11 ⇒ R200 ≳ 0.25 Mpc/h ⇒ min separation ≳ 0.4 Mpc/h), so
no real pair is ever below the table.

## (2) Smoothing / spline rule (fixed now)

Interpolate `ln(1 + xi_hat)` (guaranteed real since xi_hat > -1) against `ln r` at the bin centers
with a **cubic spline** through the bin centers (interpolating, not smoothing — the ~7e8 pairs make
the per-bin Poisson error negligible, so no extra kernel smoothing is imposed; the spline IS the
smoothing rule). Recover `xi_smooth(r) = exp(spline(ln r)) - 1`. Empty or DD=0 bins (none expected
at these pair counts) would be dropped before splining.

**Beyond the measured range** (r > r_max, which occurs because the max min-image distance is
√3·L/2 ≈ 177.5 Mpc/h): xi is set to **0** (uncorrelated at large separation). Since `xi_hat(r_max)`
is already ≈ 0, this introduces no material discontinuity; it mirrors the model table's own
xi → 0 large-r behavior and keeps those C entries PSD-neutral. `S_gpu` clamps input distances into
the table range, so the table is defined on [r_min, 180] with xi ≡ 0 on [r_max, 180].

## (3) Diagonal normalization convention (fixed now)

The model pipeline normalizes by `sigma2_R = sigma^2(R_smooth)`, the variance of the matter field
smoothed on `R_smooth = 1.0`, and sets `C_ii = 1`. The measured analog, stated before fitting:
```
C_ij = xi_smooth(r_ij) / sigma2_hat ,   sigma2_hat = xi_smooth(R_smooth = 1.0) ,   C_ii = 1 .
```
i.e. the measured correlation function evaluated at the same R_smooth limit the model takes for its
diagonal. **Sensitivity check (pre-registered):** re-normalize with `sigma2_hat =
xi_smooth(0.5·R_smooth)` and `xi_smooth(2.0·R_smooth)` and report the resulting (S-shape, w0, wa,
crossing) spread as the normalization systematic.

## (4) PSD handling (fixed now)

A measured-xi C is not guaranteed PSD (its implied P(k) may dip negative). We use the SAME clip the
frozen op_B uses:
- **log-det path**: `S_gpu`'s Cholesky; on a PD failure add `jitter = 1e-8` to the diagonal
  (identical to op_B's `1e-12` eigenvalue clip in spirit — the smallest bound that restores PD).
- **REPORT the negative-eigenvalue mass**: at a representative early (z≈3) and late (z≈0) snapshot,
  compute the full eigenspectrum of C on a fixed random subsample (k_sub = 6000, `eigvalsh`
  feasible on CPU) and report `neg_mass = Σ|λ_i|(λ_i<0) / Σ|λ_i|`. Because C is a fixed
  correlation-shape sampled at random positions, neg_mass is a property of the xi_hat spline and
  transfers across k. **If neg_mass > 1% of the spectrum weight at either epoch, the measured
  estimator is FLAGGED as failing and the log-det number is reported as unreliable, not headlined.**

## (5) The b^2 / growth cancellation — now tested empirically, not assumed

`halo_grain`'s governing point: in the NORMALIZED model C, linear halo bias b(M,z) and linear growth
D(a) cancel exactly (both numerator and diagonal carry b^2 D^2), so model-C is a-independent. The
measured xi_hat carries the REAL b^2(a) D^2(a) AND real nonlinear / scale-dependent-bias shape
evolution. Normalizing measured-C by `sigma2_hat = xi_smooth(R_smooth)` cancels the amplitude
(b^2 D^2) the same way — so **measured-C departs from a-independence ONLY through the SHAPE
evolution of xi_hat(r).** The measured run therefore tests the cancellation empirically: if the
normalized measured-C is a-independent, S(a) tracks a fixed-shape curve and the model result is
recovered; if the shape evolves, S(a) and w(a) shift, and that shift is the physical content the
model proxy discarded.

## Order of operations (enforced)

1. Measure xi_hat(r) per snapshot at the corner threshold (CPU pair counts) — no S computed.
2. Build ln(1+xi_hat) splines, sigma2_hat (three R_smooth), measured tables — no S computed.
3. PSD diagnostic (neg-eigenvalue mass, k_sub=6000, z≈3 and z≈0) — gate before headlining.
4. GPU Cholesky log-det S(a) with the per-snapshot measured tables (under the flock).
5. Analysis: w(a), interior peak, crossing, CPL projection, real DESI DR2 chi2 — S(a) swapped only.
6. SUMMARY.md: measured-vs-model table (headline), normalization spread, PSD mass, Abacus verdict.

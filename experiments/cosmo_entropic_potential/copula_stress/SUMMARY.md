# Copula-Gaussianity stress test — the 2-point asterisk is removed FOR THE OBSERVABLE; the higher-order gap is small, inverting, and redshift-flat

**Date 2026-07-10.** Stress-tests the assumption that lets `S = −ln det C = 2·multi-information`
carry the cosmology result: that the cosmic field's **copula** is Gaussian enough that the
2-point log-det captures the true (all-orders) multi-information. Discovery mode. Data:
`results.json`; tiers in `tier1_verify.py`, `tier2_lognormal.py`, `tier3_nbody.py`+`tier3_lowz.py`.

## The three tiers

**Tier 1 (verify): PASS.** The KSG multi-information estimator recovers the analytic
`−½ ln det C` on synthetic Gaussians to sampling error; the factor `S = 2·I` (from the unit
diagonal) confirmed.

**Tier 2 (lognormal — the decisive demonstration): the theorem's protection is real.** A
Gaussian-copula field with maximally non-Gaussian lognormal marginals (σ = 0.5–1.0) has a
**copula gap of ~0.1%** — `−ln det C` on the rank correlation is *exact* for a Gaussian copula
regardless of the marginals, and copula-invariance held to machine precision
(`rank_invariance_dev = 0.0`). **The lognormal part of cosmic non-Gaussianity — most of it —
contributes zero gap, for free.** Separately flagged: using the **field Pearson** correlation
instead of the rank/log correlation is a **~20% error** on the multi-information — an *estimator*
issue (which 2-point), distinct from and larger than the higher-order gap below.

**Tier 3 (the real test — N-body copula gap, TNG300, bias-cancelled via matched Gaussian-copula
surrogate):** the higher-order gap `I_true − I_Gaussian-copula` is:

| z | mean rank corr | gap (finest 4.3 Mpc, m=6) | gap (block m=8) |
|---|---|---|---|
| 0.00 | 0.292 | **−8.4%** (inverts) | −10.0% |
| 3.01 | 0.285 | **−10.5%** (inverts) | −16.2% |

Three findings, all against the posit's hope:
1. **The gap INVERTS** — the 2-point log-det *over*-reads the true coordination by
   single-to-low-double-digit % (the Hubbard-warned direction), it does *not* hide extra
   coordination the pipeline is missing.
2. **The gap does NOT grow toward low z** — it is redshift-flat, if anything *shrinking*
   (−10.5% → −8.4%). The copula non-Gaussianity is roughly scale/z-stable, not blowing up in
   the nonlinear regime.
3. **It shrinks with scale** (−8% at 4.3 Mpc → sign-noise by 25 Mpc), consistent with the
   copula becoming Gaussian on large scales — where the `w ≠ −1` signal is born (§2 fence).

## What this does to the headline (the posit's number-claim)

`w(z)` depends on `dlnS/dlna`, so a **redshift-stable fractional gap cancels in the
log-derivative.** Propagating the measured z=3→0 gap change through the sign law:

| scale/template | Δw from the gap |
|---|---|
| line, 4.3 Mpc | **−0.005** |
| line, 6.4 Mpc | −0.012 |
| block m=8, 4.3 Mpc | −0.017 |

**Δw ≈ −0.005 to −0.017 — an order of magnitude inside the ±0.05–0.20 error bars.** The
headline does not move.

## Verdict on the posit ("removes the asterisk AND moves the headlines")

- **Asterisk (higher-order, 2-point-vs-all-orders): removed for the observable.** The gap is
  small, inverting, and redshift-flat, so it cancels in the log-derivative `w(z)` reads. The
  2-point isn't faking or hiding the signal — it reads the copula faithfully where it counts.
  Converted from "unbounded unknown" to "measured, bounded (≲10% on S, ≲0.02 on w), inverting."
- **Headlines: not moved.** Δw ≲ 0.02.
- **And the hoped direction is wrong.** The posit hoped the higher-order content would *add*
  coordination at low z — supplying §5.1's required positive shape term σ(a). It does the
  opposite (inverts) and is flat. **σ(a) is NOT the missing non-Gaussian copula content**; it
  must come from the maintenance/horizon term or elsewhere.
- **The real lever is the OTHER asterisk:** tier-2's field-Pearson-vs-rank ~20%. That is
  scale/z-dependent and actionable (use the log-field/rank correlation) — the bigger and more
  honest correction, and an estimator fix rather than a higher-order mystery.

## Caveats

Gap measured on small cell-tuples (m = 6, 8), not the full k = 38,000 halo-grain S — the trend
(inverting, z-flat, scale-shrinking) is the robust result, not the exact % on the pipeline's own
matrix; the halo-grain R_smooth = 1 Mpc is smaller-scale than the finest tuple here, so the gap
there could be larger in magnitude while (by finding 2) still largely z-flat and cancelling.
KSG bias cancelled by the matched surrogate (validated tier 1). Number-weighted CIC field, not
the matter field. **Intermediate redshifts completed after first write and confirm the
flatness — measured, not extrapolated** (finest 4.3 Mpc, line m=6): z=3.01 → −10.5%,
z=2.00 → −7.9%, z=1.36 → −6.8%, z=0.70 → −6.2%, z=0.50 → −7.1%, z=0.00 → −8.4%. A shallow
U with minimum near z ≈ 0.7 (close to the S-peak epoch), total variation < 4.5 points over
the full range — no low-z blowup, and the Δw ≲ 0.02 propagation stands on the full curve.

## Sideways pass

The redshift-flatness is itself the interesting object: it says the cosmic **copula** reaches
its (mildly non-Gaussian, coordination-*reducing*) shape early and holds it — the growth of
structure moves *amplitude* (marginals), which `S` is blind to by clause 3, far more than it
moves *dependence shape* (copula), which is what `S` reads. That is the copula-invariance fence
(§2) seen from the data side: the reason `S(a)`'s evolution is gentle and its `w` near −1 is
that late-time structure formation is mostly a marginal (amplitude) phenomenon, and the
coordination ledger is constitutionally blind to it — reading only the slowly-evolving copula.

*(Tiers 1–2 by the copula-stress agent; tier 3 executed by the orchestrating session after the
agent idled mid-tier; summary by the orchestrator from executed output.)*

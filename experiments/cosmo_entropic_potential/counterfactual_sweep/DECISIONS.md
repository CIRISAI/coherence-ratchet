# Counterfactual cosmology sweep — DECISIONS (pre-registered before results)

**Date 2026-07-10.** The test of law-ness vs coincidence for the dark-energy law
`rho_DE ∝ S`, sign law `1 + w(a) = -(1/3) d ln S / d ln a`.

A **law** must hold **counterfactually**: in universes with different formation histories
the entropic potential `S(a)` must co-vary with **that universe's own** clustering history
in the way the mechanism requires. A **fitted coincidence** works only near our cosmology.

## What is varied

CAMELS IllustrisTNG **1P** parameter-variation boxes (public Flatiron mirror, keyless),
same 25 Mpc/h box, same snapshots, same group-catalog format, same hydro physics as the
CV fiducial the frozen pipeline was built on. One parameter varied at a time:

- **Omega_m axis (p1):** `1P_p1_{n2,n1,0,1,2}` → **Om = 0.1, 0.2, 0.3, 0.4, 0.5** (sigma8=0.8).
  Om read directly from each catalog's `Header/Omega0`; OmegaLambda = 1−Om (flat).
- **sigma8 axis (p2):** `1P_p2_{n2,n1,0,1,2}` → **sigma8 = 0.6, 0.7, 0.8, 0.9, 1.0** (Om=0.3).
  Header does not store sigma8; values are the frozen CAMELS 1P design (linear, step 0.1).
- **Fiducial** (Om=0.3, sigma8=0.8) = `1P_p1_0` = `1P_p2_0`, run once, used on both axes.
- Fixed at fiducial in all runs: h=0.6711, ns=0.9624, Ob=0.049; hydro feedback params fixed.

9 unique cosmologies × 10 snapshots (z = 3 → 0, the frozen SNAPS grid).

## Frozen estimator (REUSED, not re-tuned)

The `../halo_grain/halo_grain.py` **op_B B-total** pipeline: `S(a) = -ln det C(a)`,
`C_ij = xi_R(r_ij)/sigma_R^2`, `C_ii=1`, over actual halo positions, R_smooth=1.0,
cap=1000, n_draw=8. **Linear bias b and growth D(a) cancel in the normalized C** — the
cosmology enters through (i) the **halo point set** (formation history: k(a) and geometry)
and (ii) the P(k) **shape** in xi_R/sig_R (rebuilt per cosmology). The point set is the
mechanism; that is what this sweep probes.

**Threshold rule (frozen RULE, not the number):** lowest decade-ladder threshold with
≥200 halos at z=3, resolution-floored. On identical 25 Mpc/h resolution this is **1e11**
for the fiducial (217 halos at z=3). Per cosmology we compute k(>1e11, z=3) and **report
whether the rule still endorses 1e11** (≥200). Structure-poor boxes (low Om / low sigma8)
may fall below 200 at z=3 — then 1e11 is the resolution-floored selection and we flag it.
The threshold is held **fixed at 1e11 across the sweep** so a threshold change cannot
confound the cosmology signal; the ≥200 flag is reported as an honest compliance/caveat.

## PRE-STATED PREDICTIONS

### (1) What the law says MUST CO-VARY (with each universe's own formation history)
- Higher sigma8 / higher Om ⇒ **earlier** structure formation ⇒ the above-threshold
  halo-count `k(a)` **formation-peak (turnover) at higher z** ⇒ `S(a)` **peak at higher z**
  ⇒ the phantom-divide **crossing epoch earlier** (higher z), and `w_today` **less phantom
  / more thawing** (further above −1, because today is deeper into the post-peak falling
  regime).
- Lower sigma8 / lower Om ⇒ **later** formation ⇒ k-turnover pushed toward z=0 or beyond
  ⇒ S-peak later or **no interior peak within z<3** (formation still rising at z=0) ⇒ no
  crossing, `w_today` at or below −1 (still phantom today — the K3-like configuration).

### (2) What must remain INVARIANT (the mechanism lock)
- **The S-peak epoch tracks that universe's OWN k-peak epoch** — the 0.948 correlation of
  `../large_volume/mechanism_curve/` generalized across cosmologies. Plotting S-peak z vs
  k-peak z for ALL 9 universes must fall on **one line near identity**. This is the load
  bearing invariant: the mechanism is S = coordination bookkeeping of the evolving unit set,
  the SAME relation in every universe, not a per-cosmology refit.

### (3) What outcome KILLS law-ness
- `S(a)` **shape insensitive to cosmology** (S-peak epoch flat vs Om and vs sigma8): the
  potential is not reading formation history — coincidence.
- **S-peak DECOUPLES from k-peak** across the sweep (correlation collapses, scatter ≫ the
  fiducial CV noise): the mechanism lock is fiducial-only — coincidence.
- The covariation runs **opposite** to prediction (1) (e.g. higher sigma8 ⇒ later crossing).

## HONEST ASYMMETRY (state loudly)

These non-fiducial universes are **NOT expected to fit our DESI data** (w0=−0.838,
wa=−0.62). A universe with Om=0.1 or sigma8=0.6 is not our universe; its w(z) should NOT
land on DESI. **The test is the internal S ↔ formation-history relation**, not the DESI fit.
The DESI fit appearing ONLY at the fiducial point is CONSISTENT with a law (the law +
our cosmology → our w(z)); it would falsify law-ness only if the *internal relations*
(mechanism lock, covariation direction) also failed off-fiducial.

## CAVEATS carried
- **One box per cosmology** (no CV suite off-fiducial): 25 Mpc/h cosmic variance. Noise
  scale = the fiducial CV suite spread (halo_grain CV_0..CV_5). A per-cosmology shift must
  exceed that spread to count. The fiducial point here (one box) is checked against the
  known CV-suite mean.
- 1P varies **one parameter at a time**; hydro feedback fixed. Om and sigma8 are partially
  degenerate for structure growth (both raise it) — expected to push the SAME direction,
  a consistency check not an independent-axis claim.
- 2-point proxy C, R_smooth=1.0, decade threshold ladder — all inherited frozen.
- z-grid is 10 snapshots ⇒ peak epochs are coarse (quantization ~ the snapshot spacing).

## VERDICT RULE (decided in advance)
- **LAW-LIKE** if: mechanism lock holds across all 9 (S-peak↔k-peak correlation stays high,
  scatter ~ fiducial noise) AND crossing epoch / w_today co-vary with Om and sigma8 in the
  predicted direction.
- **COINCIDENCE-LIKE** if: S-shape flat vs cosmology, or lock decouples off-fiducial, or
  covariation is reversed.
- **MIXED** stated plainly if one relation holds and the other fails.

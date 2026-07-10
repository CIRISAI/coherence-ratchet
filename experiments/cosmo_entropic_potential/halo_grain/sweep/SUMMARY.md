# Sensitivity + volume sweep of the B-total halo-grain DESI structure

Two mandated follow-ups to the ADDENDUM (`../ADDENDUM_btotal_peak.md`), which found
that the extensive B-total channel `S_total(a) = -ln det C` over the evolving halo
population reproduces DESI's structure at ONE point in a choice space (threshold
1e11 M⊙/h, R_smooth = 1.0 Mpc/h, cap = 1000): interior `S` peak 6/6 CAMELS boxes,
w_today = -0.841 ± 0.050 (DESI w₀ = -0.838), crossing epoch median z ≈ 0.77 with
large 25-Mpc/h scatter (0.33-1.36). The questions: **(1)** how much do w_today and
the peak epoch move with the free choices, and **(2)** does volume tighten the
crossing epoch, toward or away from DESI's ~0.35. Nothing here is tuned; the spread
is reported as found. Same `halo_grain.op_B` code path throughout.

---

## 1. Sensitivity sweep (CAMELS CV, all 6 boxes)

Grid: mass threshold {5e10, 1e11, 3e11, 1e12} M⊙/h × R_smooth {0.5, 1.0, 2.0} Mpc/h
× cap {500, 1000}. 24 cells × 6 boxes. Per cell: mean w_today, boxes with an
interior `S` peak, peak-z distribution.

| thr (M⊙/h) | R | cap | w_today (mean ± box σ) | interior peak | peak z (med [min,max]) |
|---|---|---|---|---|---|
| 5e10 | 0.5 | 500 | −0.991 ± 0.063 | 6/6 | 3.00 [2.30, 3.00] |
| 5e10 | 0.5 | 1000 | −0.862 ± 0.103 | 6/6 | 1.05 [0.77, 1.36] |
| 5e10 | 1.0 | 500 | −0.998 ± 0.045 | 6/6 | 2.65 [2.30, 3.00] |
| 5e10 | 1.0 | 1000 | −0.865 ± 0.088 | 6/6 | 1.05 [0.77, 1.36] |
| 5e10 | 2.0 | 500 | −1.001 ± 0.035 | 6/6 | 2.30 [2.30, 3.00] |
| 5e10 | 2.0 | 1000 | −0.836 ± 0.085 | 6/6 | 1.05 [0.77, 1.36] |
| **1e11** | 0.5 | 500/1000 | **−0.837 ± 0.051** | **6/6** | 0.91 [0.33, 1.36] |
| **1e11** | 1.0 | 500/1000 | **−0.841 ± 0.050** | **6/6** | 0.77 [0.33, 1.36] |
| **1e11** | 2.0 | 500/1000 | **−0.841 ± 0.050** | **6/6** | 0.91 [0.33, 1.36] |
| 3e11 | 0.5 | 500/1000 | −0.911 ± 0.212 | 5/6 | 0.54 [0.00, 0.77] |
| 3e11 | 1.0 | 500/1000 | −0.863 ± 0.212 | 5/6 | 0.54 [0.00, 0.77] |
| 3e11 | 2.0 | 500/1000 | −0.852 ± 0.198 | 5/6 | 0.54 [0.00, 0.77] |
| 1e12 | 0.5 | 500/1000 | −1.221 ± 0.382 | 5/6 | 0.54 [0.00, 1.05] |
| 1e12 | 1.0 | 500/1000 | −1.136 ± 0.432 | 5/6 | 0.54 [0.00, 1.05] |
| 1e12 | 2.0 | 500/1000 | −1.006 ± 0.421 | 6/6 | 0.43 [0.15, 1.05] |

(For 1e11 and above the halo count never reaches the cap, so cap = 500 and 1000 are
identical — collapsed above. Cap only bites at 5e10, where k reaches ~640-744; see
"biggest mover".)

**Biggest mover — the mass threshold, by a wide margin.**

| free choice | w_today by value | span |
|---|---|---|
| **threshold** | 5e10: −0.926 · **1e11: −0.840** · 3e11: −0.875 · 1e12: −1.121 | **0.281** |
| R_smooth | 0.5: −0.974 · 1.0: −0.943 · 2.0: −0.905 | 0.069 |
| cap | 500: −0.958 · 1000: −0.923 | 0.036 |

R_smooth and cap are nearly inert at the reference threshold: at 1e11 the whole
result is invariant to R_smooth (0.5-2.0) and cap (500-1000) to within ±0.004. All
the motion in w_today is the **mass threshold** — i.e. how deep into the
merger-dominated regime you push. The 25-Mpc/h box only *resolves* the 1e11 corner
(217→364 halos); at 1e12 it holds 11-53 halos and the estimate is noise-dominated
(±0.3-0.4). The cap is a genuine knob only at 5e10, where it truncates the extensive
`k`-growth: capping at 500 freezes `S` once the population exceeds 500, pulling the
peak to high z (2.3-3.0) and w_today to −1.0 — a bookkeeping artifact of the cap, not
physics.

### The defensible claims

- **w_today, robust statement:** at the one threshold the box resolves (1e11),
  **w_today = −0.84 ± 0.05, invariant to R_smooth and cap.** The 0.003 coincidence
  with DESI's central w₀ = −0.838 is surely partly fortuitous, but the **−0.85 ± 0.05
  scale is robust**. Across the *full* grid, w_today ∈ **[−1.22, −0.84]** (grid mean
  −0.94); every excursion past −1 lives in the halo-starved high-threshold cells
  (1e12, σ ≈ 0.4), never in a resolved one. 17/24 cells are non-phantom (w > −1) today.
- **Peak-structure survival — the qualitative DESI shape does NOT die under the
  sweep.** The interior `S` peak (⇒ w < −1 in the past, a single crossing, w > −1
  today) survives in a **majority of boxes in 24/24 cells**, and at the strict 6/6
  level in **14/24 cells** (mean interior-peak fraction across the grid = **0.93**).
  The strict 6/6 only weakens in the noisy high-threshold corners; the shape itself
  is everywhere.

---

## 2. Volume test

**No independent larger-volume catalog was reachable, so no independent large-box
test was run** (per the brief: not faked). Reachability, checked 2026-07-10 and
logged in `results.json → volume_test.reachability`:

| large-volume option | status |
|---|---|
| Quijote (1 Gpc/h FoF) | gated — Globus HTTPS host does not resolve (DNS); Binder is OAuth-walled + signup form. No anonymous HTTP. |
| CAMELS-SAM (100 Mpc/h) | not on the public ~camels mirror (404 at every path). |
| CAMELS-TNG L50n512 (50 Mpc/h, same mass res) | listed but permission-blocked (dir 403, file 404). |

**What was done instead (labelled for what it is).** `S_total` is extensive and the
correlation between halos in two disjoint comoving sub-volumes is ~0, so `C` over the
union of N independent-phase boxes is block-diagonal and `S_pooled(a) = Σ S_box(a)`.
Pooling the 6 CV boxes is therefore a real volume increase **in the sampling /
cosmic-variance sense** — it reduces the scatter on the crossing epoch as ~1/√N.

| N boxes | equiv. box (Mpc/h) | crossing z (mean ± scatter) | w_today |
|---|---|---|---|
| 1 | 25.0 | 0.84 ± 0.31 [0.33, 1.36] | −0.841 |
| 2 | 31.5 | 0.80 ± 0.30 | −0.841 |
| 3 | 36.1 | 0.84 ± 0.23 | −0.842 |
| 6 | 45.4 | **1.05** (single pooled estimate) | −0.842 |

**Verdict: volume SHARPENS the epoch but AWAY from DESI.** The scatter falls with
volume (0.31 → 0.23 by N=3, roughly the 1/√N expectation), so more volume genuinely
tightens the crossing epoch — but the variance-reduced central value converges to
**z ≈ 1.05**, at the *high* end of the single-box range, **not toward DESI's ~0.35**.
w_today is untouched by pooling (−0.842). The epoch does not firm up on DESI; it firms
up near z ≈ 1.

Two honest hedges, both pointing the other way: (i) pooled independent 25-Mpc/h boxes
add sampling volume but **not Fourier modes larger than 25 Mpc/h** — a true 50-100
Mpc/h box carries large-scale power this construction lacks, and could shift the epoch;
(ii) the epoch is resolved only to the **10-snapshot grid spacing**, and the sweep's
higher-threshold cells (3e11, 1e12) do hint at a *lower* epoch (peak z 0.43-0.54,
closer to DESI) that the small box cannot sample. So the direction "volume → z ≈ 1"
is what *this* (mode-limited) volume increase shows; whether a true large box with
large-scale modes and resolved massive halos lands there is exactly the untested part.

---

## 3. Measured-covariance variant (direction-of-effect, one config)

Replaces the model-ξ `C` with a covariance **measured** from the halo field: coarse-grid
the halo counts into a fixed n³ comoving grid per snapshot, treat the 6 boxes as 6
realizations, estimate the cell-cell covariance across them, regularize with
Ledoit-Wolf linear shrinkage toward the diagonal (6 realizations ≪ Ncell, so shrinkage
is heavy — δ ≈ 0.68-0.75, reported per snapshot), take `S = -ln det` of the shrunk
correlation matrix.

| grid | global slope | w_global | S rises? | interior peak | shrinkage δ |
|---|---|---|---|---|---|
| 3³ = 27 cells | +0.033 | −1.011 | yes | yes (z = 1.05) | 0.68-0.75 |
| 4³ = 64 cells | +0.011 | −1.004 | yes | yes (z = 0.77) | 0.67-0.69 |

**Direction: swapping model-ξ for a measured covariance does NOT flip the sign.** `S`
still rises with an interior peak. This is a *fixed-dimension* measure (Ncell constant
across snapshots), so it probes the op_A-like fixed-unit channel, **not** the extensive
B-total `k`-growth — which is why w_global sits at ≈ −1.0 (~ΛCDM) rather than −0.84,
and why the magnitude is not interpretable (heavy shrinkage, 6-member ensemble). Its
one job is narrow and it delivers: the rise-then-peak shape is **not** an artifact of
the model-ξ assumption. Limits: 6 realizations, δ ≈ 0.7 dominant, magnitude meaningless.

---

## Bottom line for the tier

**The DESI-structure claim NARROWS but does not die under the sweep.**

- **Survives:** the qualitative DESI shape — interior `S` peak ⇒ w < −1 past, single
  crossing, w > −1 today — is robust across **24/24** grid cells (majority-of-boxes;
  strict 6/6 in 14/24). The **magnitude w_today ≈ −0.85 ± 0.05 is robust at the one
  threshold the 25-Mpc/h box resolves (1e11)** and is invariant to R_smooth and cap
  there. The measured-covariance check confirms the rise is not a model-ξ artifact.
- **Narrows / does not firm up:** w_today swings to −1.0…−1.1 at higher mass thresholds,
  but only in **halo-starved, noise-dominated (±0.3-0.4)** cells the box cannot resolve;
  the mass threshold is the sole meaningful mover (span 0.28 vs 0.07 / 0.04). The tight
  0.003 match to DESI's central w₀ should be read as the −0.85 scale plus luck, not a
  precision result.
- **Crossing epoch does NOT sharpen toward DESI with volume.** Pooling reduces the
  cosmic-variance scatter (~1/√N, as it should) but the epoch converges to **z ≈ 1.05**,
  above DESI's ~0.35 — with the caveats that this pooled volume lacks >25-Mpc/h modes
  and that higher (unresolved) mass thresholds hint at a lower epoch. A true
  large-volume, well-resolved rerun (TNG300 / Quijote-class) remains the required test
  before any epoch claim; it is unreachable from here.

## Files
`sweep.py` (sensitivity grid) · `quijote.py` (volume: reachability probe + pooled-volume
convergence) · `measured_cov.py` (measured-covariance direction check) · `results.json` ·
`figures/{fig_w_today_grid, fig_peak_survival, fig_reference_trajectories,
fig_volume_convergence, fig_measured_cov}.png`

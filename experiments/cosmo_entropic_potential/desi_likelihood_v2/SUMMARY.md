# DESI DR2 likelihood-grade comparison — v2

**Date:** 2026-07-10 · **Dir:** `desi_likelihood_v2/`
**Upgrade:** representative fractional errors → the **real DESI DR2 BAO data vector + full 13×13 covariance** (official Cobaya likelihood file, reproducing DESI DR2 Results II, arXiv:2503.14738).

---

## VERDICT

**The "closer than ΛCDM" result survives the real likelihood, and on the clean apples-to-apples test the frozen framework curve is *preferred* over ΛCDM: on the official DR2 Cobaya likelihood (13 pts, full covariance) + a θ\* anchor, framework χ²=8.86 vs ΛCDM 10.32 at matched k_params=2 — Δχ²=−1.46 favoring the framework with ZERO shape parameters — and the framework wins AIC/BIC against both ΛCDM and the 2-parameter CPL fit.**

The framework's dark-energy shape is **frozen**: `E²(a) = Ωₘa⁻³ + Ω_r a⁻⁴ + (1−Ωₘ−Ω_r)·S(a)/S(1)` from the TNG300-1 halo-grain `S(a)`, with **no free (w0,wa)**. It fits only (Ωₘ, β=c/H₀r_d).

### With the θ\* CMB anchor (n = 14)

| model | shape params | χ² | Ωₘ | AIC | BIC |
|---|---|---|---|---|---|
| **framework** | **0** | **8.86** | 0.317 | **12.86** | **14.14** |
| ΛCDM | 0 | 10.32 | 0.296 | 14.32 | 15.60 |
| CPL (w0,wa) | 2 | 6.90 | 0.346 | 14.90 | 17.46 |

- **Framework beats ΛCDM by Δχ² = −1.46 at identical parameter count.**
- **Framework wins AIC and BIC against both ΛCDM and CPL:** ΔAIC(fw−CPL) = −2.04, ΔBIC(fw−CPL) = −3.32; ΔAIC(fw−ΛCDM) = −1.46, ΔBIC = −1.46.
- **CPL's lower χ² is chasing BAO noise without SNe.** Its BAO+θ\*-only best fit is **(w0,wa) = (−0.50, −1.44)** — far from DESI's SNe-informed **(−0.838, −0.62)**. Supernovae pin the low-z end; absent them, CPL's two extra parameters buy a marginal χ² gain that AIC/BIC reject.
- Framework's preferred **Ωₘ = 0.317 ≈ Planck 0.3153, unforced**; ΛCDM is pulled to 0.296. The edge sits in the low-z `D_H/r_d` points (z=0.51: framework pull −0.9σ vs ΛCDM −1.4σ; z=0.71: −1.2σ vs −1.7σ) — exactly where DESI DR2's evolving-DE signal lives, not a covariance artifact.

### BAO only (no CMB anchor, n = 13)

| model | shape params | χ² | Ωₘ | AIC | BIC |
|---|---|---|---|---|---|
| **framework** | **0** | **7.14** | 0.327 | **11.14** | **12.27** |
| ΛCDM | 0 | 10.28 | 0.297 | 14.28 | 15.41 |
| CPL | 2 | 5.62 | 0.386 | 13.62 | 15.88 |

- Framework beats ΛCDM by **Δχ² = −3.14** BAO-only. CPL best fit runs to **(w0,wa) = (−0.18, −2.71)**, Ωₘ = 0.386 — an extreme SNe-free BAO fit. Framework still wins AIC/BIC (ΔAIC fw−CPL = −2.48, fw−ΛCDM = −3.14). The anchor's leverage is visible: it moves fw−ΛCDM from −3.14 (BAO-only) to −1.46 (with θ\*).

---

## Reconciling with the earlier "1.36 σ" framing

The old headline reported a **Mahalanobis distance** in projected (w0,wa) space: the framework's CPL-projected point was 1.36 σ from DESI's published posterior, vs ΛCDM at 3.28 σ. That is a 2-D Gaussian distance against DESI's SNe-informed ellipse.

Two framings, same conclusion (framework sits between ΛCDM and DESI's CPL, near DESI):

- **Projection / Mahalanobis (needs a projection):** redone through the real DESI covariance, the faithful distance-space projection is **(−0.783, −0.730), Mahalanobis = 1.01 σ** from DESI (old value 1.36 σ; ΛCDM 3.28 σ). Slightly tighter than before.
- **Δχ² (projection-free, load-bearing):** framework−ΛCDM = −1.46 (with CMB) is a direct goodness-of-fit difference at matched params in the full 14-point distance space; as a ~1-dof preference this is √1.46 ≈ **1.2 σ** in favor of the framework. It needs no CPL projection, which is why it is the primary statement.

The Δχ² and Mahalanobis numbers are related but not identical (different spaces: full 14-pt distance space without SNe vs 2-D projected (w0,wa) against a SNe-informed posterior). Both put the framework far closer to DESI than ΛCDM.

---

## Projection-method spread = a systematic on (w0,wa) (task 4, `projection_spread.json`)

The framework has no intrinsic (w0,wa); "which CPL point" depends on the projection metric:

| method | (w0, wa) | cross z | Mahalanobis from DESI |
|---|---|---|---|
| distance-space, real cov (BAO+CMB) — faithful | (−0.783, −0.730) | 0.42 | 1.01 σ |
| distance-space, real cov (BAO only) | (−0.758, −0.593) | 0.69 | 2.17 σ |
| ρ-weighted | (−0.738, −0.977) | 0.37 | 1.95 σ |
| w-space, DE-weighted | (−0.762, −0.917) | 0.35 | 1.56 σ |
| w-space, uniform | (−0.646, −1.423) | 0.33 | 4.13 σ |
| ΛCDM (anchor) | (−1.0, 0.0) | — | 3.28 σ |

**Method systematic:** `wa` spans −0.59 to −1.42 (**std 0.28**, comparable to DESI's own σ_wa = 0.20); `w0` spans −0.65 to −0.78 (std 0.05). Projected significance should be quoted as "~1–2 σ, method-dependent," not a single number — which is why the projection-free Δχ²/AIC is the headline.

---

## Honest caveats (prominent)

1. **No supernovae likelihood included.** DESI's published (−0.838, −0.62) uses DESY5 SNe. BAO+θ\*-only, CPL runs to extreme `wa` (−1.44 with CMB, −2.71 BAO-only) because SNe pin the low-z end. **Adding Pantheon+ would plausibly** tighten the CPL posterior back toward (−0.84, −0.62) and shrink its χ² advantage over the framework further (CPL is currently over-fitting low-z BAO scatter that SNe would constrain); it would not change the sign of framework−ΛCDM, which is driven by the same low-z `D_H` shape. **This is the next step** (Pantheon+ is a 1701×1701 covariance + absolute-magnitude marginalization — a real but tractable lift).
2. **The θ\* anchor is a CMB-prior approximation.** One point, `D_M(z*)/r_d = 94.28 ± 0.03%` at z\*=1089.8, target from Planck-2018 base-ΛCDM. Uses only the acoustic-scale distance to last scattering, folds the fixed early-physics ratio rs\*/rd into the target, includes radiation in E(z), Gaussian. It does **not** carry the full CMB covariance or the sound-horizon (rs) uncertainty. BAO-only rows are shown so its leverage is explicit.
3. **Ωₘ is profiled, not marginalized with a full CMB.** We profile Ωₘ on a grid (β analytic); a full treatment would marginalize Ωₘ against the complete CMB likelihood, which would slightly broaden all three models' effective errors.
4. **Modest significance.** Δχ² = 1.5–3.1 at matched params ≈ 1.2–1.8 σ, not a detection. Honest claim: *a frozen, zero-shape-parameter curve fits real DESI DR2 at least as well as ΛCDM and, by AIC/BIC, better than both ΛCDM and a 2-parameter CPL fit.*
5. `Ω_r` fixed at 9.2e-5; `S(a)` frozen (constant) below the sim's a_min ≈ 0.25 (only the high-z anchor integral, matter/radiation-dominated, is affected).

---

## Provenance & files

- **DESI data:** `desi_dr2_data/desi_gaussian_bao_ALL_GCcomb_{mean,cov}.txt` — official Cobaya file from `CobayaSampler/bao_data/desi_bao_dr2/`, reproducing DESI DR2 Results II (arXiv:2503.14738); 13 measurements / 7 tracers (BGS `DV`; LRG1/2, LRG3+ELG1, ELG2, QSO `DM`&`DH`; Lyα `DM`&`DH`).
- **Framework curve:** TNG300-1 205 Mpc/h B-total corner 7.43e11, frozen `S(a)` (10 pts) from `../large_volume/results.json → stage2_primary.records`.
- **Code:** `likelihood_fit.py` (tasks 2–3), `projection_spread.py` (task 4).
- **Results:** `results.json`, `projection_spread.json`. Nothing committed.

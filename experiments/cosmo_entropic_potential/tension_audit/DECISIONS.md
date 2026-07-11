# Tension audit — DECISIONS (pre-stated, written before any number was computed)

**Date 2026-07-11.** What the framework's registered dark-energy background (`ρ_DE(a) ∝ S(a)`,
the frozen large-volume corner-rule `S(a)` from `../large_volume/results.json`) does to the two
classic ΛCDM tensions: **H0** (CMB-inferred vs local distance ladder) and **S8/growth** (CMB-
inferred vs weak-lensing/clustering). This is an **honest-exposure audit, not a victory run.**

## The honesty rule (rule 1, restated for this audit)

All directions and magnitudes are reported **as found**. A worsening is published as exposure:
if the framework's background makes either tension *worse*, that number goes in the SUMMARY and
the final report at full weight. Inconvenient numbers are still numbers. There is no
pre-registered "target" here — the ΛCDM tensions are what they are; we report the shift and its
sign, whichever way it lands.

## Pre-stated expected directions (to be checked against the computation)

The frozen `S(a)` rises from z=3, peaks at z=0.59 (S=9936), and declines to S(a=1)=8867. So
`g(a) ≡ S(a)/S(1) > 1` for a ∈ ~[0.49, 0.90] (z ∈ ~[0.11, 1.0]) — **more** dark-energy density
than ΛCDM's constant Λ in that band — and `g < 1` at higher z (less, and dynamically negligible
by z≳3). The equation of state is thawing: `w(a) = −1 − ⅓ dlnS/dlna`, `w_today ≈ −0.83 > −1`,
crossing w=−1 at the S-peak (z=0.59), phantom (w<−1) just above it.

- **TASK A — H0 (the risk check).** Hold physical densities ω_b, ω_c (hence r_s, early-time,
  **unchanged by a late-time DE deformation** — stated) and the acoustic scale θ\* fixed at
  Planck. Replace Λ with ρ_DE(a) ∝ S(a), close the universe today, solve for the H0 that
  preserves the comoving distance to z\*=1090.
  **EXPECTED: WORSENS (lowers inferred H0).** Reasoning: more DE at z∈[0.1,1] ⇒ larger H(z)
  there ⇒ smaller comoving distance at fixed H0 ⇒ to restore D_M(z\*) the inferred H0 must drop.
  Thawing w>−1 lowering CMB-inferred H0 is the textbook direction. **If the sign comes out
  otherwise, double-check before reporting.** Magnitude expected small (w_today only ~0.17
  above −1).

- **TASK B — S8/growth.** Solve δ'' + (2 + dlnH/dlna)δ' = (3/2)Ω_m(a)δ in ln a, our background
  vs ΛCDM, normalized identically at a=0.01 (early equality — the deformation vanishes there by
  construction). Report D(z=0) ratio → σ8/S8 fractional shift, and fσ8(z) difference at z=0.3–0.8.
  **EXPECTED: RELIEVES (lowers σ8/S8, toward the lensing side).** Reasoning: more DE at z∈[0.1,1]
  ⇒ faster expansion ⇒ growth more suppressed ⇒ lower σ8 today ⇒ toward KiDS/DES (S8≈0.76) and
  away from Planck (S8≈0.83).

**Note the asymmetry we may be about to publish:** the same hump that would *relieve* S8 is what
*worsens* H0. If both expected directions hold, the framework trades one tension for the other —
that is the honest headline, stated in advance so it cannot be spun after the fact.

## Method decisions (fixed before computing)

1. **S(a) source.** Primary = frozen large-volume **corner-rule** B-total (`stage2_primary.records`,
   `../large_volume/results.json`). Robustness = **complete-book** B-total (full population >10¹¹,
   `../full_population/results.json` `full_1e11` best tile T=2). Both reported.
2. **r_s fixed.** The deformation is purely late-time (z<3 where S is measured; DE is <1% of the
   matter density by z=3 and falls). r_s is set by pre-recombination physics (ω_b, ω_c, radiation)
   and is held **identical** to ΛCDM. Stated, not assumed silently.
3. **H0 constraint.** Preserve the comoving angular-diameter distance to z\*=1089.80 at fixed
   ω_m = ω_b+ω_c and fixed r_s (equivalently fixed θ\*). Ω_m = ω_m/h² floats with h; flat closure
   Ω_DE = 1 − Ω_m − Ω_r. Root-find h. Radiation Ω_r = 4.15×10⁻⁵/h² included (matters to z\*).
4. **High-z extrapolation of g(a) below a=0.25.** Constant-w (frozen local log-slope) continuation;
   verified to contribute <0.01% of D_M(z\*) either way (DE negligible at z>3). Reported.
5. **Growth comparison.** Hold Ω_m fixed at the Planck ΛCDM value; swap only the DE sector Λ→S(a);
   smooth DE (no DE perturbations — same open flank as the self-consistency run). σ8 shift = D-ratio
   at a=1 (identical early normalization). S8 = σ8√(Ω_m/0.3); Ω_m common ⇒ S8 ratio = σ8 ratio.
6. **Cross-check.** Both tasks must be consistent with the self-consistency run's own H(a)
   (`../selfconsistency/`, which already iterated gravity→clustering→S→H to a fixed point; it found
   growth suppression g(1)=0.987). Reconcile before reporting.

## Verified literature anchors (WebSearch, 2026-07-11)

- Planck 2018 (TT,TE,EE+lowE+lensing): H0 = 67.36 ± 0.54; Ω_b h² = 0.02237; Ω_c h² = 0.1200;
  Ω_m = 0.3153; 100θ\* = 1.04109 (100θ_MC=1.04092); z\* = 1089.80; r\* = 144.39 Mpc;
  σ8 = 0.8111; S8 = 0.834 ± 0.016. (arXiv:1807.06209.)
- SH0ES (Riess et al. 2022): H0 = 73.04 ± 1.04. Gap to Planck = 5.68 km/s/Mpc, ~5σ.
  (arXiv:2112.04510, ApJL 934 L7.)
- Weak lensing S8: KiDS-1000 = 0.759₋₀.₀₂₁⁺⁰·⁰²⁴; KiDS+DES combined ≈ 0.762 ± 0.025;
  ~2.5–3σ below Planck. (Asgari et al. 2021; Heymans et al. 2021.)

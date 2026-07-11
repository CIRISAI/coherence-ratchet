# DECISIONS — ISW supervoid flag (pre-stated BEFORE computing)

**Date 2026-07-11.** Question: our background (frozen large-volume S(a) → thawing w(z),
w > −1 after z ≈ 0.6) decays late-time gravitational potentials faster than ΛCDM → an
ENHANCED integrated Sachs-Wolfe (ISW) signal at supervoid redshifts (z ~ 0.4–0.7). Compute
OUR enhancement and state plainly whether it (a) reaches the reported stacked-void excess,
(b) is a measurable discriminant, or (c) is negligible. Do NOT claim the anomaly is explained
unless the number reaches it.

## Background inputs (frozen, not re-fit here)

- **PRIMARY:** the frozen large-volume B-total **corner** S(a) (threshold 7.43e11 M⊙/h),
  `../large_volume/results.json` → `stage2_primary.records` (10 snaps, z = 3.008 → 0). This is
  the 1.36σ headline background (w_today = −0.833, S-peak z = 0.59).
- **ROBUSTNESS (complete-book variant):** the complete halo population ≥1e11 M⊙/h, the tiled
  full-box S(a), `stage4_tiles` (w_today = −0.939, S-peak z = 0.89). This is the "complete
  book" grain (lowest mass cut, whole population) as the maximal-inclusion robustness check.
- Mapping (frozen, stock): ρ_DE(a) ∝ S(a) ⇒ **E²(a) = Ω_m a⁻³ + (1−Ω_m) S(a)/S(1)**, exactly.
  Ω_m = 0.300 (the TNG300/CAMELS box cosmology the S(a) was measured in). No S differentiation
  is needed for the background E(a); the ISW derivative acts on the growth factor D, not S.
- ΛCDM reference: same Ω_m = 0.300, f_DE(a) ≡ 1.

## Kernel choice (pre-stated) — the physically-correct ISW source

Linear ISW temperature source along the line of sight: ΔT/T = 2 ∫ (∂Φ/∂η) dη (conformal time
η, c = 1, Φ = Ψ). Poisson in comoving k: −k²Φ = 4πG ρ_m0 a⁻¹ δ_m, with δ_m(a) ∝ D(a)
(early-normalized). Hence the potential

    Φ(a) ∝ D(a)/a      (the growth-suppression factor; constant in EdS ⇒ no ISW),

and the local ISW **source** is

    Φ'(a) ≡ dΦ/dη ∝ d(D/a)/dη = a²·H(a)·d(D/a)/da ,   dη = da/(a²H).

The team-lead brief wrote the kernel as "d/dη[(1+z)⁻¹ D]"; since (1+z)⁻¹ = a that literal form
is d(aD)/dη (a GROWING quantity, not a decaying potential). The brief's own parenthetical —
"potential decay ∝ d[D/a]/dη" — is the correct linear-ISW source, and is what I compute. Stated
here so the choice is on the record: **Φ ∝ D/a, source ∝ d(D/a)/dη.**

**Normalization (load-bearing):** both D early-normalized (D → a as a → 0), i.e. identical
primordial amplitude — the CMB-anchored, matter-era-identical choice, same as the
selfconsistency machinery. Potentials agree at high z; the difference accumulates late. The
Poisson prefactor 4πG ρ_m0 is identical in both models (same Ω_m, H0) and cancels in every
ratio. Each model uses its OWN E(a) in both the growth ODE and the dη conversion.

**Reported quantity — ISW source ratio:**

    R_ISW(z) = Φ'_ours(z) / Φ'_ΛCDM(z)
             = [ E_ours·a²·d(D_ours/a)/da ] / [ E_Λ·a²·d(D_Λ/a)/da ]   (H0 cancels).

Both numerator and denominator are negative (potentials decay); R_ISW > 1 means our late-time
potential decays FASTER ⇒ enhanced ISW. Reported for z ∈ (0, 2).

**Stacked-void window integral (pre-stated void kernels — same voids in both cosmologies, so
only the source ratio differs):**

    A_ratio = ∫ dz W(z) Φ'_ours(z) / ∫ dz W(z) Φ'_ΛCDM(z).

- **PRIMARY window** W(z) = top-hat over **[0.4, 0.7]** — the Granett-Neyrinck-Szapudi (2008)
  supervoid stack redshift range (SDSS LRG, mean z ≈ 0.5).
- **ROBUSTNESS window** W(z) = Gaussian(μ = 0.52, σ = 0.15) — a DES/BOSS-era broader void
  selection (Kovács et al.). Reported, never promoted over the primary.
- The void kernel is cosmology-independent (identical void catalog in both models); it is a
  pure redshift weight on the source ratio, NOT a per-void ISW amplitude model. Stated so no
  one reads A_ratio as an absolute ISW prediction — it is strictly ours/ΛCDM.

## Verdict bands (pre-stated BEFORE seeing any number)

Let E★ = A_ratio over the PRIMARY window (the enhancement factor at the supervoid window).

- **(a) RELEVANT:** E★ ≥ 1.5×  → genuinely relevant to the anomaly; register as a flag. (Even
  1.5× does NOT by itself "explain" a 3–5× excess — I will say explicitly how much of the
  reported excess our number covers, and will not claim more.)
- **(b) DISCRIMINANT:** 1.05× ≤ E★ < 1.5× (i.e. a ~5–50% effect) → NOT an explanation of the
  excess but a REGISTERED DISCRIMINANT; quantify the stacked-void ISW measurement precision
  needed to separate our background from Λ at the supervoid window.
- **(c) NEGLIGIBLE:** E★ < 1.05× (< 5%) → negligible; closed honestly.

**Confabulation guard (house rule):** a 20% effect does not explain a 3× excess. The verdict
word is set by the band E★ falls in, and the SUMMARY will state the covered fraction of the
literature excess explicitly. No upgrade of the verdict word beyond the band.

## Pipeline discipline

CPU only. Incremental flush to results.json after each stage. Growth ODE, E(a), and the
S(a) → f_de mapping are lifted verbatim from `../selfconsistency/selfconsistency.py` and
`../epoch_check/cpl_projection.py` (same ODE, same normalization). No simulation reload — S(a)
is read from the frozen large_volume results.json.

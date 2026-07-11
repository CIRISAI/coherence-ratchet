# Functional-falsification — pre-committed DECISIONS

**Date 2026-07-10.** Written BEFORE any fit is computed. Dir: `functional_falsification/`.
CPU-only; no GPU lock; nothing committed.

## The question (one sentence)

Does the *specific* frozen functional — the extensive halo-grain log-det Gaussian
multi-information `S(a) = −ln det C` — fit DESI DR2 where *reasonable alternative
functionals of the same structure-formation data* fail (→ the object is SPECIFIC), or
does any structure functional mapped through the same stock rule land in the DESI
quadrant (→ the DESI fit is FAMILY-GENERIC and "the object" deflates to "a generic
family of monotone structure clocks")?

## What is held FIXED across every row (apples-to-apples)

1. **Same data.** The same 10 TNG300-1 halo catalogs (`large_volume/data/tng300_groups_{025,030,036,042,049,056,065,076,087,099}.npz`), box 205 Mpc/h, TNG cosmology Ωm=0.3089, all halos M200c > 1e11. Snapshots span z≈3.0 → 0, the same a-grid as the frozen `S(a)`.
2. **Same stock mapping.** `ρ_DE(a) ∝ F(a)` (comoving), giving the frozen background
   `E²(a) = Ωm a⁻³ + Ω_r a⁻⁴ + (1−Ωm−Ω_r)·F(a)/F(1)`. No free (w0,wa). This is the
   identical map the framework row uses (`likelihood_fit.py::make_f_fw`, `E_of`).
3. **Same sign law for w_today.** `1 + w(a) = −(1/3) d ln F/d ln a` (the κ-cancelling
   stock law), evaluated at a=1 by the same finite-difference operator (`s_of_a.dln_dlna`).
4. **Same likelihood.** Real DESI DR2 BAO (official Cobaya `desi_gaussian_bao_ALL_GCcomb`,
   13 pts, full 13×13 covariance) + the θ\* CMB anchor, profiled over exactly two free
   parameters (Ωm, β=c/H₀r_d) — identical to the framework row. AIC/BIC at matched
   k_params=2 for every zero-shape-parameter functional. (`likelihood_fit.py` reused
   verbatim as an imported module — it reproduces framework χ²=8.86, LCDM χ²=10.32.)

The ONLY thing that varies row to row is **the functional F(a)**. That is the whole point.

## The frozen operationalizations (fixed before any number is seen)

Halos are deposited on a periodic cubic grid by **Cloud-In-Cell (CIC)**. Primary cell
size **≈4 Mpc/h → N=51³** (205/51 = 4.02 Mpc/h). Grid-scale sensitivity is reported at
**2 Mpc/h (N=102³)** and **8 Mpc/h (N=26³)** for F1–F3 (the grid-dependent functionals).
Two deposit weights where noted: **count** (each halo weight 1) and **M200c-mass**.
Density normalized to mean 1: `ρ_i → ρ_i/⟨ρ⟩`; contrast `δ_i = ρ_i/⟨ρ⟩ − 1`.

- **F1 — Das–Pandey Shannon configuration entropy.** `p_i = ρ_i/Σρ_j` (probability mass
  per cell); `S_c(a) = −Σ_i p_i ln p_i` (discrete Shannon entropy of the mass partition;
  the ln V_cell additive constant is dropped — grid is identical across snapshots, but
  note this additive choice DOES shift d ln S_c/d ln a, so it is recorded as a stated
  convention). Max = ln(N_cells) for a uniform field; decreases as mass concentrates.
  Count-weighted and mass-weighted variants. This is the **halo-field** operationalization
  of Das–Pandey's full-matter-field `S_c = −∫ρ ln ρ dV` — same catalogs our functional used.
- **F2 — Sarkar-class one-point marginal negentropy.** `J(a) = ½ ln[σ²(1+σ²)/ln(1+σ²)]`
  with σ² = Var(δ) of the gridded contrast (same grids as F1). One-point marginal
  non-Gaussianity — the copula-orthogonal complement of the log-det.
- **F3 — variance / amplitude control.** `F(a) = σ²(a) = Var(δ)`. Pure amplitude. Our
  functional is amplitude-BLIND by the linear-growth-invariance theorem; F3 tests whether
  an amplitude-carrying functional does better or worse.
- **F4 — k(a) bookkeeping control.** `F(a) =` halo count above the frozen corner threshold
  (`k_at_corner` from `large_volume/results.json`: unit count, NO correlation content).
  This is the load-bearing control: S(a) and k(a) share the same interior-peaked shape
  because both are built from the same halos, so if k(a) alone fits as well, the
  *correlation/copula* content of the log-det is NOT what earns the DESI fit — the claim
  would narrow from "the log-det copula" to "any interior-peaked abundance clock."
- **F5 — PEDE external benchmark** (NOT structure-derived, zero-parameter):
  `Ω_DE(z) = Ω_DE0·[1 − tanh(log₁₀(1+z))]` → `f_DE(a) = 1 − tanh(log₁₀(1/a))`. Fit with the
  same machinery, k_params=2. Answers "are there *other* zero-parameter models that beat
  ΛCDM on DR2?" with a number.

**Imported family rows (already computed elsewhere, cited):**
- **Framework** = frozen B-total halo-grain log-det `S(a)` (the object under test).
- **ΛCDM**, **CPL(w0,wa)** — the anchors, from the same `likelihood_fit.py`.
- **cell-grain** — the intensive/cell-scale log-det variant `(w0,wa)=(−0.897,−0.099)`; fit
  as a *fixed* CPL through the machinery. CAVEAT: its cell scale is a FREE CHOICE
  (`results.json::desi_matching_cell_scale.note` — "calibration, not prediction"), i.e. it
  carries a hidden tuned parameter the extensive functional does not; recorded, not hidden.
- **intensive / fixed-k** — S falling, w≈−0.99: effectively ΛCDM-like; stated, fit as ΛCDM-adjacent.

## Handling pathological F(a) — committed BEFORE seeing them

A functional is recorded as **FAILED** (not massaged) if:
- any `F(a) ≤ 0` on the grid → `ρ_DE ∝ F < 0` is unphysical (the stock map breaks);
- `F(a)` monotone in the wrong direction so strongly that `w_today` leaves the physical
  DESI-relevant band `[−1.22, −0.84]` used as the pre-registered P3/K7 gate, OR gives a
  wildly off `w0/wa`; that IS the result — a structure functional that does not thaw
  toward DESI is a *specificity confirmation*, and must be reported plainly, not fixed.
- A functional whose χ² merely **fails to beat ΛCDM (χ²≥10.32)** is NOT a code failure —
  it is a legitimate "does not land in the DESI quadrant" outcome.

## Verdict rule — the DESI quadrant, defined BEFORE computing

The framework anchor: `w_today ≈ −0.83`, thaws (crossing from w<−1 in the past to w>−1
today, interior-peaked F), χ²=8.86 **beating** ΛCDM's 10.32 (Δχ²=−1.46 at matched
params), Mahalanobis ≈1.0–1.4σ from DESI's (w0,wa) posterior. A functional **lands in the
DESI quadrant** iff BOTH:
(a) it **thaws** — `w_today ∈ (−1, −0.84]` with an interior-peaked / late-declining F(a)
    (quintessence side, crossing up through w=−1), AND
(b) it **beats ΛCDM**: χ² < 10.32 (equivalently AIC/BIC below ΛCDM at k=2).

## The two outcomes and what each MEANS (stated before the numbers)

- **OUTCOME A — SPECIFICITY CONFIRMED.** F1–F4 mostly FAIL condition (a) and/or (b): they
  do not thaw, give wrong-sign / phantom / ΛCDM-indistinguishable w, or χ²≥ΛCDM. Then the
  extensive log-det is a *specific* object — the DESI fit is not a generic property of
  "some structure clock," and the specificity sentence in the paper is earned. The
  strongest form: F4=k(a) FAILS while framework passes → the *correlation copula*, not mere
  abundance, is load-bearing.
- **OUTCOME B — FAMILY-GENERIC DEFLATION.** Several of F1–F4 (especially F4=k(a)) also
  satisfy (a)+(b) with χ² comparable to the framework. Then "landing in the DESI quadrant"
  is a *generic* property of monotone-then-declining structure clocks under the stock map,
  and "the object" deflates to "a generic family." The honest paper statement becomes:
  the DESI proximity is shared by a family; the log-det's *distinctive* claims (amplitude-
  blindness, copula-only, parameter-free sign theorem) are then the ONLY residue of
  novelty, and the DR2 closeness is downgraded from evidence-for-the-functional to
  evidence-for-the-family. A partial/mixed result (F4 passes but F1–F3 fail) is reported as
  exactly that: the *shape* (interior-peaked abundance) is generic, the *functional form*
  is not uniquely selected by DR2.

Either outcome is informative and will be stated plainly in SUMMARY.md, verdict-first,
with THE TABLE (functional × {w_today, crossing/peak epoch, χ², AIC, BIC, verdict}).

## Caveats to carry into SUMMARY (known now)

- These are **halo-field** operationalizations of full-matter-field functionals (F1, F2);
  Das–Pandey/Sarkar used the continuous matter field. Same catalogs our functional used, so
  the *comparison* is apples-to-apples, but the absolute values are not their published ones.
- **Grid-scale sensitivity** (F1–F3 depend on cell size); reported at 2/4/8 Mpc/h.
- **Single box** (TNG300-1), no cosmic-variance ensemble; matches the framework's own caveat.
- BAO+θ\* only, **no supernovae** — same limitation as the framework likelihood; CPL
  over-fits low-z BAO scatter absent SNe (documented in `desi_likelihood_v2/SUMMARY.md`).

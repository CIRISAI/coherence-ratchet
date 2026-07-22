# copula_stress under a SHOT-MATCHED null — PRE-REGISTRATION

**Date 2026-07-21. Method frozen BEFORE any shot-null number is seen.**
The frozen `copula_stress/` files are read-only; this directory holds the re-run.

## The debt

`copula_stress` (2026-07-10, tier 3) is the study the program leans on for *"the Third does
not move `w(z)`"*: it measured the higher-order copula gap

```
gap_matched(z) = I_KSG(real) − I_KSG(surrogate)
```

on a **CIC number-count field** of TNG300-1 halos, against a **continuous matched-Gaussian-copula
surrogate** (`gaussian_surrogate`: an MVN draw with the field's rank correlation `C_rank`).
It found the gap inverting (−6% to −11%), redshift-flat, and propagating to `Δw ≈ −0.005 to
−0.017` — an order of magnitude inside the DESI error bars. That is the DE bet's own defense
against the Third.

**K4 (2026-07-20, `thirdness/discriminator/`) proved that null TYPE is insufficient for
discrete/count data.** A coordination-free Poisson process matched to `n̄` and `P(k)`
*over*-reproduced an apparently-robust 13–22σ copula signal, and an `argsort∘argsort`
tie-break on empty cells manufactured 37–63% of it. A continuous Gaussian null has no
discreteness and no exact ties, so it cannot expose either. `copula_stress`'s tier-3 gap is
also a 13–38σ number against exactly that (continuous) null, on a count field with exact ties
at `δ = −1`. **The Third-defense therefore currently rests on the wrong null type.**

## What the frozen null does and does NOT control (same audit as the discriminator)

The frozen `gaussian_surrogate` matches `C_rank` and nothing else. It does **not** control:

1. **Discreteness / shot noise.** Real is a CIC deposit of a finite point catalog; the
   surrogate is a smooth MVN. Poisson sampling injects connected ≥3-point structure from
   discreteness alone (the `1/n̄` terms), invisible to a continuous null.
2. **Marginal shape / the empty-cell atom.** The frozen `I_KSG(real)` runs on the **raw CIC
   values** (a hard atom at `δ = −1`, broken by a `1e-10` random jitter inside
   `ksg_multiinformation`), while `I_KSG(surrogate)` runs on **exactly Gaussian marginals**.
   KSG's finite-sample bias is marginal-shape dependent, so the "bias-cancelling" surrogate
   does not in fact cancel the bias. Spreading an atom into `m` independently jittered columns
   *destroys* dependence inside the atom → a **negative** gap for free. This is a candidate
   mechanism for the entire "inversion."
3. **Rank-transform tie handling.** The frozen baseline `gaussian_copula_MI` uses
   `rankdata(method="average")` (ties collapsed to one value), which is *not* `argsort∘argsort`;
   but the estimator family K4 indicted is one step away, and the asymmetry between the two
   tie treatments (collapsed in the baseline, randomly spread in the KSG) is itself uncontrolled.
4. **Assignment/aliasing.** CIC only; NGP untested (NGP has many more exact ties).

## Data and estimator (both inherited, not re-implemented)

- **Data:** TNG300-1 FoF group catalogs already on disk, `../../large_volume/data/tng300_groups_*.npz`,
  **number weighting** (`weights=1`), exactly as frozen tier 3. Six snapshots matching the frozen
  curve: 025 (z=3.01), 033 (2.00), 042 (1.36), 059 (0.70), 067 (0.50), 099 (0.00). No new data pulled.
- **Estimator:** imported *unmodified* from the frozen `copula_stress/copula_lib.py` —
  `cic_grid`, `template_samples`, `ksg_multiinformation` (KSG1, k = 4), `gaussian_copula_MI`,
  `gaussian_surrogate`, `normal_scores`. Nothing in `copula_stress/` is edited.

## Configurations (exactly the three rows of the frozen Δw table)

| id | grid | template | cell | frozen Δw row |
|----|------|----------|------|----------------|
| **A (PRIMARY)** | ng = 48 | line, m = 6, sep = 1 | 4.27 Mpc/h | line 4.3 Mpc → −0.005 |
| B | ng = 32 | line, m = 6, sep = 1 | 6.41 Mpc/h | line 6.4 Mpc → −0.012 |
| C | ng = 48 | block2, m = 8 | 4.27 Mpc/h | block m=8 → −0.017 |

## Nulls (pre-committed NULL controls — same status as the frozen phase-randomized null and
the CMB null ensembles; not synthetic data standing in for measurement)

- **S0 — the frozen null, reproduced.** MVN draw with the field's `C_rank`
  (`gaussian_surrogate`). n = 4 draws. Validation: `gap_S0` must reproduce the frozen
  `results.json` `gap_matched` to within the null spread.
- **S0f — continuous field null.** Phase-randomize the real field's `|δ_k|` at the same `ng`
  (DC zeroed), template-sample identically. Continuous marginals, matched `P(k)` exactly, no
  discreteness. Isolates "MVN draw vs field-level phase randomization." n = 3.
- **S1 — SHOT-MATCHED POISSON NULL (the decisive one).** Built as a *point process*, so that
  the null passes through the identical CIC gridding the real catalog does:
  1. `amp = |rfftn(δ_real)|`, deconvolved by the CIC window `W(k) = Π_i sinc²(π n_i/ng)`
     (floored at 0.05) so that re-gridding the null restores the real `P(k)`;
  2. phase-randomize → Gaussian `δ_G`, DC zeroed;
  3. intensity `∝ max(1 + δ_G, 0)`; **multinomial draw of exactly N points** (⇒ `n̄` matched
     exactly, same halo count as the snapshot);
  4. positions = cell + uniform sub-cell offset;
  5. `cic_grid` at the same `ng`, `template_samples` identically.
  Matched `n̄`, matched `P(k)`, Poisson discreteness, the same empty-cell atom, the same
  assignment window — **zero genuine connected higher-order structure** beyond the mild
  clipping non-negativity (which pushes the null *toward* the real negative gap ⇒ conservative
  for claiming the real gap survives). n = 4.
- **S1b — shot-subtracted bracket.** As S1 but `amp² → max(amp² − P_shot, 0)` first, with
  `P_shot` measured empirically as the mean mode power of 5 uniform-random N-point CIC
  realizations, so that after Poisson sampling the *total* `P(k)` matches real. S1 and S1b
  bracket the true matched-discreteness null (S1 carries one extra `1/n̄` of shot). n = 3.

## AMENDMENT 1 (2026-07-21, before any verdict statistic) — S1 construction repaired

The S1/S1b recipe registered above **fails numerically** and the failure was found in a smoke
test. Full disclosure of what was seen, so the amendment is auditable:

- **What broke.** Dividing the real amplitude by the CIC window `W(k)` amplifies the modes near
  Nyquist by up to ~15×. Those modes are **shot-dominated**, and a periodogram's mode-to-mode
  scatter is O(100%), so the deconvolution amplifies noise, not signal: the resulting Gaussian
  intensity had `var(δ_G) ≈ 200–410` (target O(1)), which drove the non-negativity clip to
  **47% of cells**. That is not a Poisson null of the real field; it is a rare-spike catalogue.
- **Numbers seen at the moment of the amendment** (2-point diagnostics + one smoke gap):
  at z = 0, ng = 32, the deconvolved null had `I_gauss = 2.09` against real's `1.07`
  (mean rank correlation off by +33%) — far outside the ≥10% mismatch guard already registered
  above, which flags such a null unreliable. The smoke also printed `gapc_S1 = −0.111` for that
  broken null at ng = 32, z = 0 (one config, one redshift, broken construction, no z-trend and
  therefore no Δw). No verdict statistic has been read.
- **The repair (registered now, before re-running).** The operative meaning of "matched P(k)"
  for this estimator is *2-point-matched*, because the frozen null it replaces (`gaussian_surrogate`)
  matched `C_rank` **exactly**. A null that is not 2-point-matched cannot be compared like for
  like. S1/S1b are therefore rebuilt as:
  1. angle-binned real power `P_real(k)`; empirical shot `P_shot(k)` from 4 uniform-random
     N-point catalogues gridded identically (window + aliasing included automatically);
  2. intensity template `P_t(k) = max(P_real − P_shot, 0)/W²(k)`, **restricted to modes with
     `W² ≥ 0.25`** — the high-k modes are shot-dominated and unrecoverable, and Poisson sampling
     regenerates exactly that power by itself;
  3. amplitude scaled by `√A`, with the single scalar `A` **calibrated by secant search so the
     gridded null's own `I_gauss_copula` matches the real field's to ≤ 1%** (≤ 6 evaluations,
     `A ∈ [0.05, 50]`);
  4. steps 3–5 of the original recipe unchanged (`max(1+δ_G,0)` intensity, multinomial draw of
     exactly N points, uniform sub-cell placement, identical CIC gridding and template sampling).
  **S1b** is identical but omits the shot subtraction in step 2 (`P_t = P_real/W²`), keeping the
  registered "double-shot bracket" role as a *spectral-shape* bracket.
- **What this does and does not change.** The null still has matched `n̄` (exactly), matched
  2-point structure (now by construction rather than by hope), Poisson discreteness, the same
  empty-cell atom, the same assignment window, and **no connected higher-order coordination**
  beyond the clipping non-negativity — whose severity is now small and is **reported per run**
  (`clip_frac`, `var_dG`). The verdict statistic, the thresholds, and the pass/fail ladder below
  are **unchanged**.

## Statistics (frozen here, not tuned after seeing numbers)

For any field `Y`: `resid(Y) = I_KSG(Y) − I_gauss_copula(Y)` (the field's own excess over its
own 2-point log-det).

- **Raw gap** (the frozen definition): `gap_X = I_KSG(real) − mean_draws I_KSG(X)`.
- **PRIMARY, 2-point-corrected gap:** `gapc_X = resid(real) − mean_draws resid(X)`.
  This removes any residual 2-point mismatch between real and the null (the nulls match `P(k)`
  only approximately after clipping/Poisson), so what remains is excess *higher-order* content.
- **Null band:** σ = std across draws of the null's `I_KSG` (resp. `resid`); `z = gapc/σ`.
- **Match diagnostic (reported, non-scoring):** `mean_offdiag_rankcorr` and `I_gauss_copula`
  of each null vs real. If a null's mean rank correlation differs from real's by > 10%
  relative, the raw gap for that null is flagged unreliable and only `gapc` is read.

**Δw propagation** — the frozen `w_implication.py` recipe, unchanged:
`S_X(a) = 2·(I_gauss_copula,real(a) + gap(a))`, `1 + w = −⅓ dlnS/dlna`, slope by the frozen
last-two-point (a-ascending) difference; `Δw = w_true − w_2pt`. Reported for the frozen gap
and for each null side by side. **Robustness variant, also reported:** slope from an OLS fit
of `lnS` on `lna` over the full six-snapshot range.

## Tie-break decomposition (task item (a))

Reported per snapshot at config A. First the fact: the exactly-tied fraction (empty cells) of
the CIC and NGP number fields. Then `I_KSG(real)` under four transforms:

1. **frozen**: raw CIC values + the built-in `1e-10` random jitter;
2. **ns-avg**: normal scores with `rankdata(method="average")` (atom collapsed, then jittered);
3. **ns-pos**: normal scores with `argsort∘argsort` (K4's indicted positional tie ordering);
4. **ns-rand**: normal scores with a random tie-break.

**Tie-artifact fraction** ≡ `(gap_ns-pos − gap_ns-rand)/gap_ns-pos`, against the same S0 null.
K4's analogue was 37–63%.

## Assignment / aliasing (task item (b))

Config A repeated with **NGP** assignment for real and for S1 (NGP has far more exact ties and
no anti-aliasing). Reported as a sensitivity; the CIC result remains primary, matching frozen.

## Pass / fail — pre-committed

The frozen defense's operative claim is *"Δw ≈ −0.005 to −0.017, an order of magnitude inside
the ±0.05–0.20 error bars; the headline does not move."* The threshold is therefore the
**tightest error bar the frozen summary itself invokes: |Δw| = 0.05.**

- **SURVIVES AS STATED** — `|Δw|` from the shot-matched `gapc_S1` ≤ 0.05 on config A **and** on
  at least 2 of the 3 configs, **and** no low-z blowup (the `|gapc_S1|` at z = 0 is not larger
  than its z = 3 value by more than 2× in the direction that would push `Δw` past 0.05).
  ⇒ The Third-defense survives the correct null; the frozen conclusion stands on its own terms.
- **SURVIVES BUT REDESCRIBED** — `|Δw| ≤ 0.05` **and** `|gapc_S1| < 2σ_null` at config A, i.e.
  the shot-matched null reproduces the frozen gap. ⇒ The *conclusion* (`w` does not move)
  stands, but the frozen *characterization* ("measured, bounded (≲10% on S), inverting") is
  **void**: what tier 3 measured was shot noise + estimator asymmetry, and the physical
  higher-order gap is **UNOBSERVED** — an upper bound, not a measurement. Report as a partial
  kill on the frozen wording with the conclusion intact.
- **DEFENSE FIRES (the defense was an artifact of the wrong null)** — `|Δw|` from `gapc_S1`
  **> 0.05** on config A, **or** the shot-corrected gap develops z-structure that reverses the
  frozen conclusion (a gap growing toward low z with `|Δw| > 0.05`). ⇒ The Third-defense was an
  artifact of the continuous null; the DE bet loses its Third-defense and the debt reopens as a
  live threat to `w(z)`.
- **Non-scoring flag:** if the `argsort∘argsort` variant contributes > 30% of the gap in the
  normal-score estimator family, K4's tie artifact is confirmed present in this family too and
  is reported as such — noting that the frozen tier-3 baseline uses `average`, not
  `argsort∘argsort`, so this is an indictment of the estimator family, not automatically of the
  frozen code.

**Stated prior (so it can be scored against): the conclusion is expected to SURVIVE** — K4's own
Poisson null pointed the same way (the Third doesn't move `w`). The run is nonetheless executed
blind, and a fired kill will be reported plainly and without softening.

## Discipline

No synthetic data (S0/S0f/S1/S1b are pre-committed nulls). Grain fixed before spectrum: configs,
nulls, statistics, thresholds and the tie/assignment variants are all committed above, before any
shot-null number exists. Dual null (the frozen continuous null is retained alongside the
shot-matched one and both are reported side by side). Incremental flush per (snapshot, config)
to per-snapshot JSON. Fixed seeds (`20260721 + snap`). The frozen `copula_stress/` files are
imported read-only and never modified. No git commit; no registration edited.

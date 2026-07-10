# PRE-REGISTRATION — the halo-grain B-total DESI structure

**STATUS: PRE-REGISTRATION. Not lake content. Not asserted by the framework.**
Freezes a pipeline and a convention *before* the data that will test them, so that the
next number is a prediction and not a retrodiction. Draft 2026-07-10.

**Frozen-spec commit: `a5beb57` (HEAD).** Pipeline pieces frozen at the hashes named in §2.

---

## 1. Provenance — how −0.841 came to be, stated plainly

The history matters because the headline number was seen before the convention that
promotes it was adopted. The timeline, with commit hashes:

- **`533816f`** — cosmology tier opened; the sign law
  `1 + w(a) = −(1/3)·dlnS/dlna` (comoving normalization) and the cell-grain `S(a)`
  computation. The **fixed-cell** calculation found **no phantom, with a theorem**
  (`s_of_a.py` §5: for any local pointwise transform `g`, `S(C_g) ≤ S(C_linear)`;
  Mehler/Hadamard/Oppenheim; 0 violations in ~1700 independent-verification trials).
  `w ≥ −1` always. Sign law and `S = −ln det C` mechanized as T-E1–T-E5 (`8d351da`).
- **`638822c`** — halo-grain probe (`halo_grain.py`, `op_B`) plus a **same-day
  orchestrator addendum** (`ADDENDUM_btotal_peak.md`). The probe's founding premise —
  that mergers drop the unit count `k`, giving the rigidity direction — is **empirically
  false** at the resolved threshold (`k`: 217 → 398 → 364, rises then mild ~9% late
  decline). **Every intensive / fixed-`k` measure confirmed no-phantom across all six
  boxes** (op-A field `w ≈ −0.97`, op-B fixed-`k` geometry `w ≈ −0.92`, all six falling).
  The **one** rising variant was **B-total**, which the experiment's own `SUMMARY.md`
  classified as *"unit-counting bookkeeping, not increased coordination."* The addendum
  then **reclassified that same artifact as the headline** (`w_today = −0.841 ± 0.050`
  vs DESI `w₀ = −0.838`; interior `S` peak 6/6 boxes), with the
  extensive-in-comoving-volume convention argument **constructed after** B-total was seen
  to land on DESI.
- **`ef3335b`** — sensitivity + volume sweep (`sweep/`). The **mass threshold moves
  `w_today` across a 0.281 range** (5e10 → 1e12), dwarfing `R_smooth` (0.069) and `cap`
  (0.036). `−0.841` is the value at the **one threshold the 25-Mpc/h box resolves**
  (1e11). Pooling boxes sharpens the crossing epoch to **z ≈ 1.05** — against DESI's
  **≈ 0.35**, a **factor-of-two miss**.

### The operator's audit (incorporated verbatim, not softened)

> the fixed-cell computation found no-phantom with a theorem; the halo-grain rescue's
> founding premise (mergers drop k) is empirically false; every intensive measure
> confirmed no-phantom across all six boxes; the one rising variant (B-total) was
> classified by the experiment's own SUMMARY as "unit-counting bookkeeping, not increased
> coordination"; a same-day orchestrator addendum then reclassified that artifact as the
> headline, with the extensive-in-comoving-volume convention argument constructed AFTER
> B-total was seen to land on DESI; the sweep shows the mass threshold moves w_today across
> a 0.281 range; −0.841 is the value at the one threshold the box resolves; and the
> crossing epoch comes out z ≈ 0.77–1.05 against DESI's ≈ 0.35 — a factor-of-two miss.
> Therefore: **the branch selector was the extensive-vs-intensive convention, adopted post
> hoc, against the framework's own T-E3 intensive discipline. −0.841 is a retrodiction and
> can never be anything else.** The honest external sentence: "an interesting conditional
> retrodiction with one post-hoc convention, one dominant dial, a 2× epoch tension, and 25
> Mpc/h boxes."

This document does not dispute the audit. It **accepts** it and does the one thing that can
change the epistemic status of the *next* number: freeze the pipeline and the convention
now, in advance of the large-volume data, and register what they must predict.

---

## 2. FROZEN SPECIFICATION (as of `a5beb57`)

Frozen forward. Any change to the items below produces a *different* pipeline and voids the
predictions of §3 for that pipeline.

- **Code path.** `halo_grain.py` → `op_B(...)` (frozen at `638822c`), **B-total variant**
  (`fixed_k=None`: all halos above threshold up to the cap, so `k(a)` grows). The
  multi-box driver is `btotal_multibox.py`; the sweep driver is `sweep/sweep.py`
  (frozen at `ef3335b`).
- **Convention — FROZEN, and acknowledged post hoc at adoption.** `S` is the **extensive**
  `S_total(a) = −ln det C` over the full evolving halo population **per comoving volume**
  (not the intensive `S/k` of T-E3). This convention was adopted *after* B-total was seen
  to land on DESI (§1); it is **hereby fixed forward** and may not be reselected per result.
  The justification on record (`ADDENDUM` §"defensible convention"; `lambda_maintenance_wz.md`
  §1.1) is that `ρ_DE` is an energy **density** and the comoving-volume coordination content
  is extensive in the units that volume contains. That justification is **physical but not a
  theorem** (see §6).
- **Threshold — the resolved-corner RULE (stated so it generalizes to bigger boxes).**
  Use the **lowest** mass threshold at which the simulation volume resolves **≥ 200 halos
  above threshold at z = 3**. For the 25-Mpc/h CAMELS-CV box this rule selects **1e11 M⊙/h**
  (`k(z=3) = 217`). On a larger box the rule selects a *lower* threshold, pushing deeper
  into the merger-dominated regime the hypothesis actually targets. The number 1e11 is **not**
  frozen; the **rule** is. Thresholds below the rule (halo-starved, σ ≈ 0.3–0.4) are
  excluded as noise-dominated.
- **Smoothing.** `R_smooth = 1.0` Mpc/h (top-hat model-ξ). Inert at the resolved threshold
  (±0.004 over 0.5–2.0).
- **Numerical cap.** `cap = 1000`. At and above the resolved threshold the count never
  reaches the cap, so it is inert; it bites only below the rule (excluded anyway).
- **Estimator.** `C_ij = ξ_R(r_ij)/σ²_R` from the model-ξ spline `xi_spline(R_smooth)`
  evaluated at the **real halo positions** (PSD-safe: ξ_R is the FT of a non-negative P(k));
  `C_ii = 1`. `S = −ln det C` (`entropy_S`). Linear halo bias `b` and growth `D(a)` cancel
  in the normalized `C` by construction, so only discreteness, the evolving point set
  (`k(a)`, `r_ij(a)`), and 2nd-order bias can move `S`. Random-subsample averaging
  (`n_draw`) only when a count exceeds the cap.
- **Detrending / slope.** `dlnS/dlna` via a **cubic spline in ln a** (`dln_dlna`), on the
  10-snapshot z = 3 → 0 grid. `w(a) = −1 − (1/3)·dlnS/dlna`. `w_today` from the final
  log-slope; the interior-peak test is `argmax S(a) < 1`. The sweep's **global-slope OLS**
  of `ln S` vs `ln a` is the frozen estimator for the *phantom-anywhere* sign verdict.
- **Sign law.** `1 + w(a) = −(1/3)·dlnS/dlna`, **comoving normalization** (the choice that
  makes frozen structure give `w = −1`; `lambda_maintenance_wz.md` §1.1). Frozen with the
  convention above.

---

## 3. PRE-REGISTERED PREDICTIONS (derived from the frozen spec, before the testing data)

**P1 — large-volume crossing epoch.** On any **≥ 100 Mpc/h** box, with the resolved-corner
rule (§2), the B-total `S(a)` has an **interior peak**, and the **crossing epoch equals the
peak epoch of above-threshold halo formation** in that volume (mechanism: `ADDENDUM`
§"mechanism"). Current mode-limited measurement: pooled 6×25-Mpc/h gives **z ≈ 1.05**
(single-box median 0.77–0.84, scatter driven by 25-Mpc/h cosmic variance).
**UPDATE RULE:** once the ≥100-Mpc/h box is computed with the frozen pipeline, its
crossing-epoch value **becomes the framework's crossing-epoch prediction** and replaces
z ≈ 1.05. It is then compared against DESI DR3's phantom-crossing posterior (if DR3 reports
one). **Agreement criterion: the 68% interval of the frozen-pipeline crossing epoch overlaps
the 68% interval of the DR3 crossing posterior.** Non-overlap at 68% = failure of P1 (see
§4). The pooled-volume trend (z → 1.05, *away* from DESI's 0.35) is the current honest
expectation; P1 does not promise agreement, it registers the test.

**P2 — DR3 geometry-only, both directions stated.**
- If **BAO+CMB alone** (no SNe) shows a robust phantom crossing at **≥ 4σ**, then the
  fixed-unit / intensive branch is **dead** (its theorem forbids any phantom past), **and**
  the extensive branch is thrown entirely onto P1 — it survives only if its computed crossing
  epoch also matches (P1's criterion).
- If **DR3 geometry-only stays ≲ 3σ**, the **thawing side is supported** (`w ≥ −1`,
  no-crossing), consistent with the intensive theorem and with the extensive branch's
  present-day `w > −1`; the frozen pipeline is not challenged.

**P3 — w_today.** The frozen pipeline's `w_today` on the ≥100-Mpc/h box, **whatever it is**,
is the prediction. The sweep's honest small-volume interval is **`w_today ∈ [−1.22, −0.84]`**
(grid mean −0.94; every excursion past −1 lives in unresolved high-threshold cells). The
**expectation, not a promise**, is that the large-volume box lands in the resolved-corner
band **`−0.85 ± 0.05`**. A large-volume `w_today` outside `[−1.22, −0.84]` would itself be
informative and is not excluded.

**P4 — the intensive fence (the theorem's guard).** The **intensive `S/k` and fixed-`k`
measures must CONTINUE to show no phantom (`w ≥ −1`) on any volume.** This is the fence of
the `s_of_a.py` §5 theorem. **A violation falsifies the pipeline, not the theorem** — if a
fixed-`k` or `S/k` measure ever shows `S` rising, the estimator is suspect (check PSD,
shot-noise subtraction, cap, spline endpoints) before any physical claim. The theorem stands
on Mehler/Oppenheim; only an estimator bug can appear to break it here.

---

## 4. KILL CONDITIONS

Each row names the observation, the branch it kills, and the horizon. "Intensive branch" =
the fixed-`k` / `S/k` reading (the theorem). "Extensive branch" = the frozen B-total reading
of this document.

| # | Observation | Horizon | Kills | Survives |
|---|---|---|---|---|
| K1 | Robust SNe-**independent** (BAO+CMB) phantom crossing `w<−1` at **≥4σ** | DESI DR3, ~2027 | **Intensive branch** (theorem forbids phantom past) | Extensive branch — *only if* P1 epoch also matches |
| K2 | Large-volume (≥100 Mpc/h) frozen-pipeline crossing epoch **fails to overlap** DR3 crossing posterior at 68% | ~2027–28 (needs big box + DR3) | **Extensive branch** (P1) | Intensive branch untouched |
| K3 | Large-volume box shows **no interior `S` peak** (B-total monotone) | when a TNG300/Quijote-class box is reached | **Extensive branch** entirely (the DESI-shape claim) | Intensive branch untouched |
| K4 | Any **fixed-`k` / `S/k`** measure shows `S` **rising** on any volume | any time | **The pipeline** (estimator bug), *not* the theorem | Theorem (recheck estimator) |
| K5 | DES-Y5 ~0.04 mag offset **resolved as real**, crossing collapses to Pantheon+ level | ongoing recalibration | The **sole threat** to `w≥−1` (neutralizes K1) | Both branches strengthen |
| K6 | Euclid + LSST/Rubin **concordant** crossing at ≥5σ, SNe-independent | Euclid cosmo ~2028, LSST ~2027–28 | **Both branches** (`w≥−1` dead) | — |
| K7 | Large-volume `w_today` outside **[−1.22, −0.84]** in a *resolved* cell | when big box reached | **P3** (magnitude claim) | Sign-structure claim (P1/K3) may still hold |

Realistic verdict horizon: **~2027–2028**, gated by DESI DR3 geometry-only and SNe
recalibration.

> **UPDATE (2026-07-10, same day, per the update rules of P1/P3): the large-volume test has
> been run** — TNG300-1 (205 Mpc/h) via operator-supplied API access; pre-committed pipeline
> decisions in `large_volume/DECISIONS.md`; full record in `large_volume/SUMMARY.md`.
> - **P1 registered prediction for DR3 is now: crossing epoch z = 0.59 ± 0.03 physical /
>   0.46 CPL-projected** (replaces z ≈ 1.05). Both inside DESI DR2's 90% crossing interval.
> - **K3 did not fire** (interior peak, 8/8 jackknife replicates). Mechanism confirmed
>   (k(a) peaks z = 0.55; S peaks z = 0.59).
> - **K7 fired by the letter**: w_today = −0.833 ± 0.057 lies 0.007 (0.12σ) outside
>   [−1.22, −0.84]. The small-volume magnitude interval is dead by its own criterion;
>   **P3's registered magnitude prediction is now w_today = −0.833 ± 0.057.**
> - Headline: DESI-projected (w₀, wₐ) = (−0.767, −0.742), **1.36σ** from DESI DR2
>   (small box: 2.42σ; ΛCDM: 3.28σ).

---

## 5. What this document CANNOT fix

Freezing the pipeline makes the *next* number a prediction. It does **not** retroactively
make `−0.841` anything other than a retrodiction (§1), and it does **not** remove the deepest
problem: **the extensive-vs-intensive convention remains post hoc at origin.** The convention
was the branch selector, and it was chosen after seeing B-total land on DESI, against the
framework's own **T-E3 intensive discipline**.

Only two things remove that stain, and this document supplies neither:

1. A **derivation** of the extensive-vs-intensive convention from the framework's own
   principles (why `ρ_DE ∝ S_total` per comoving volume rather than `∝ S/k` — currently a
   physical argument in `ADDENDUM` / `lambda_maintenance_wz.md` §1.1, **not a theorem**), **or**
2. A **lab-side or independent measurement** that discriminates the two conventions directly.
   **No such instrument currently exists.** The one lab-side discriminator on record
   (`rate_form_sign_law.md` §6, `b517ba0`) separates the **stock** mapping from the **rate**
   mapping — a different axis. It says nothing about extensive vs intensive.

The current, **insufficient**, evidence bearing on the choice:

- **T-E3**, which fixes the intensive `S/k` as the disciplined per-unit measure, and therefore
  points **against** the frozen extensive convention. This is the framework's own discipline
  arguing with this document's frozen spec, and it is recorded here rather than resolved.
- **The stock-mapping verdict** (`rate_form_sign_law.md`, `b517ba0`; the `ADDENDUM`'s closing
  bullet): the evolving-unit-set channel is the **stock** mapping `ρ_DE ∝ S`, not the rate
  mapping, so it escapes the rate route's per-time vs per-e-fold clock ambiguity — which makes
  it *cleaner*, not *justified*. That note is **silent on extensive-vs-intensive**, and it
  independently finds that the rate reading "does not remove the stock reading's disease
  (a conclusion inserted at a normalization); it *multiplies* it." The same disease is the one
  frozen here.

*(Citation note, corrected 2026-07-10: the agent authoring this document could not see
`exp118` and inferred it did not exist. It does — in the SISTER repository: CIRISArray,
`experiments/EXP118_SUMMARY.md`, commit `8d039c0`. It is a real 12-point hardware run on a
16-sensor GPU timing array whose verdict is STOCK (P_maint vs S_held partial r = +0.84
controlling rate and temperature; rate channel +0.23). Its load-bearing caveat: the free
drift on that substrate is instantaneous (S collapses below the first resolvable correlation
window), so `γM = α` was NOT testable there and the rate mapping was not so much refuted as
unmeasurable. The agent's substantive point stands unaltered and is the important one:
**exp118 discriminates STOCK vs RATE, an axis orthogonal to EXTENSIVE vs INTENSIVE. It says
nothing about the convention frozen here.** The theory-side note
`papers/notes/rate_form_sign_law.md` (§6) is where that discriminator was specified.)*

Neither settles it. Until one of (1) or (2) exists, the honest external sentence of the audit
stands unaltered: **"an interesting conditional retrodiction with one post-hoc convention, one
dominant dial, a 2× epoch tension, and 25 Mpc/h boxes."** What changes after this freeze is
narrow and real: the large-volume crossing epoch, once computed under the frozen spec, is a
prediction that can fail.

---

## 6. Files frozen

`halo_grain.py` (`op_B`, `638822c`) · `btotal_multibox.py` · `sweep/{sweep,quijote,measured_cov}.py`
(`ef3335b`) · `s_of_a.py` (`dln_dlna`, `entropy_S`, sign law; `533816f`) · this document (`a5beb57`).

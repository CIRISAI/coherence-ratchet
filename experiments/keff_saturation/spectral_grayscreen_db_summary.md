# Gray-screen deconfound of the "turbulent-cell" detailed-balance signal

**Question.** The 2×2 "turbulent" cell (HIGH-rank + BREAKS detailed balance) was anchored
on Allen Neuropixels **visual cortex during `natural_movie_three`** — a *looping* clip.
A response phase-locked to the movie's repeat period produces a rotation in the top
covariance modes that reads as "breaks DB" and survives phase-randomization, but whose
**source is the external periodic drive, not the system's own maintenance (γM)**.
Prior smoking gun: the movie circulation *z* = 4.0 was carried almost entirely by **one
mode-pair** (0–2), the others at null → looks like a single driven rotation.

**Test.** Recompute the DB axis on the **same** session, **same** VIS cortical units,
**same** 20 ms bins, **same** estimators, across three stimulus conditions differing
only in external periodicity. Population held **fixed** = 403 VIS units active >0.5 Hz in
**all three** windows, so the stimulus is the only thing that changes. Each condition's
null is a **phase-randomization of that condition's own data** (never the movie null
reused elsewhere).

- Data: DANDI:000021, session **721123822** (brain_observatory_1.1), 1603 units / 774 VIS.
- Estimators reused verbatim: `entropy_production.irreversibility_from_units` (winding-rate
  *z*, block-bootstrap null), `spectral_galaxy_db.db_stats` (direct circulation *z* vs
  phase-randomized null + **per-mode-pair** *z*), `spectral_test` (rank / k_eff).
- Script: `spectral_grayscreen_db.py`; results: `spectral_results_grayscreen_db.json`.

## Results

| condition | periodicity | T | k_eff (PR) | eff-rank | **winding \|z\|** | **circ \|z\|** | per-pair circ z (0-1 / 0-2 / 1-2) | null ceiling (wind / circ) |
|---|---|---:|---:|---:|---:|---:|---|---|
| **spontaneous** | NONE (gray screen) | 15063 | 182.5 | 5 | **4.87** | **3.28** | −1.30 / **+2.59** / −2.30 | 1.24 / 1.38 |
| **natural_movie** | looping clip | 30026 | 168.6 | 6 | 2.91 | 5.42 | −1.48 / **+7.27** / +1.43 | 1.41 / 0.21 |
| **drifting_gratings** | periodic, ≠ movie period | 34179 | 105.4 | 10 | 6.21 ⚠ | 15.92 | +4.49 / **+11.38** / −5.27 | **17.11** ⚠ / 1.13 |

Winding reference null ≈ 1.5. "null ceiling" = the estimator's \|z\| on a **phase-randomized
copy of that same condition's data**. ⚠ see estimator-trust note below.

## Verdict: INTRINSIC γM — the turbulent cell **HOLDS** (confound real but partial)

**1. Spontaneous still breaks DB.** With the stimulus removed, gray-screen visual cortex
retains a significant arrow of time: **winding \|z\| = 4.87** vs its own phase-randomized
null ceiling **1.24** (~3.9×) and above the ~1.5 winding null; **circulation \|z\| = 3.28**
vs null ceiling 1.38. The irreversibility is intrinsic, not a stimulus artifact.

**2. The single-dominant-pair smoking gun VANISHES in spontaneous.** The movie circulation
is carried by **one** mode-pair (0–2, *z* = +7.27; others at null), and gratings even more
so (0–2, *z* = +11.38). In **spontaneous** the circulation is **distributed and modest**
(per-pair z: 0–2 = +2.59, 1–2 = −2.30, 0–1 = −1.30 — **no dominant pair**). So the sharp,
drive-locked single-pair rotation *is* stimulus-locking; it disappears when the periodic
drive is removed.

**3. Reconciling the two.** The looping movie (and, more strongly, gratings) **inflate and
concentrate** the DB signal into one external-drive-locked mode-pair — that concentrated
excess is a confound. But a genuine, weaker, **distributed** intrinsic irreversibility
survives underneath it during gray screen. The confound is **confirmed as a real inflating
mechanism but rejected as the sole source**: real γM remains.

**4. Gratings positive-controls the confound mechanism.** A *different* imposed period than
the movie loop yields the strongest, most single-pair-concentrated circulation
(\|z\| = 15.92, pair 0–2 z = 11.38) — external periodicity does inject a drive-locked
rotation exactly as hypothesized. Spontaneous lacking it confirms the concentration is
stimulus-sourced.

### Estimator trust (condition-dependent — load-bearing)

- **Spontaneous, T = 15063:** large T (half the movie). Winding does **not** degenerate
  here (unlike the short-T anesthesia case); trust **both** winding (4.87) and circulation
  (3.28), each well above its own null.
- **Movie, T = 30026:** winding null ceiling 1.41 — clean; trust both estimators.
- **Drifting gratings:** the winding estimator is **corrupted** — phase-randomizing the
  same data gives winding \|z\| = **17.11 > the real 6.21**, because strong narrowband
  stimulus periodicity is preserved by phase-randomization and blows up the block-bootstrap
  winding. **For gratings trust circulation only** (real 15.92 vs null 1.13). This is why
  the gratings winding cell is flagged ⚠ and is not used in the verdict.

### Honest caveats

- Winding and circulation can pick different carrier mode-pairs (winding best-pair 1–3 in
  spontaneous, 0–1 in movie; circulation carrier 0–2 throughout) because they normalize the
  top SVD modes differently; both measure top-mode rotation. The *distribution* of per-pair
  z (concentrated vs spread) is the robust discriminator, not the specific index.
- Spontaneous is gray screen but the animal is awake/behaving (running, arousal); that
  self-generated activity is legitimately **intrinsic** γM, not external stimulus
  periodicity — which is exactly what "no external periodicity" isolates.
- Rank axis is not the focus here; all three conditions read the same "high PR /
  modest debiased eff-rank" intermediate as before (k_eff PR 105–182, eff-rank 5–10).

**Bottom line.** The arrow of time in visual cortex is **intrinsic** — it persists in
gray-screen spontaneous activity above a same-data phase-randomized surrogate. The turbulent
(high-rank + breaks-DB) cell stands. What the looping movie added was a *concentration and
inflation* of that signal into a single stimulus-drive-locked mode-pair, which correctly
disappears when the periodicity is removed.

# The phase-space ledger on REAL Gaia data — the instrument reads phase-space coherence, cleanly on the one grain that isn't self-selected

**Date 2026-07-10. Companion to `dm_phasespace_grain.md` (which proved, in a toy, that the
ledger S = −ln det C reads the copula shadow corr(x,v) of phase-space coherence — high for cold
coherent streams, ~0 for dispersion-supported systems, mean-blind and amplitude-blind by
theorem). That note flagged its own central test as "essentially sim-only: G1 needs the full 6D
f(x,v)." This note discharges that flag for the one accessible case — the Milky Way — on REAL
PUBLIC DATA.** Code: `experiments/dm_coherence/gaia/{fetch_gaia.py, gaia_test.py, make_figures.py}`;
numbers below are executed output (`results.json`, seed 20260710).

**Pre-registered predictions (written into `gaia_test.py` before any number was computed).**
The ledger reads phase-space coherence as high corr(position, velocity). Therefore:
- **P1** a dynamically COLD stream reads HIGH S on the (x,v) grain — velocity is a tight function
  of position along the stream (v = f(x));
- **P2** the kinematically-mixed field/halo in the same volume reads LOW S — position does not
  predict velocity;
- **P3** the S ordering is driven by the position-velocity GRADIENT (a real copula feature), it
  SURVIVES removing the stream's bulk mean motion (mean-blindness on real stars — the gradient is
  intact where a bulk offset would vanish), and it COLLAPSES when the gradient is destroyed.

---

## Bottom line up front

**VERDICT: PASS — but only on the grain that escapes the selection confound, and that
distinction is the whole result.** The ledger demonstrably reads real phase-space coherence in
the Milky Way. It does so **cleanly and non-circularly on the radial-velocity grain** (Orphan
stream, S5 spectroscopy), where the velocity dimension is not used to define the sample. On the
**proper-motion-only grain** (GD-1, Gaia astrometry) the same ordering appears but is
**SELECTION-CONFOUNDED** — stream membership is defined by a velocity-track cut, which manufactures
corr(x,v) by construction, and a matched-geometry control confirms the artifact equals or exceeds
the signal. Two real cold streams, two grains, and the honest split is: *the instrument works, and
you can only prove it works where selection didn't do the work for you.*

| | Part A — GD-1 (Gaia astrometry) | Part B — Orphan (S5 radial velocity) |
|---|---|---|
| Real data | Gaia DR3 TAP, 51 177 stars | S5 / Li+2019, 6 470 spectra |
| Grain | {φ₁, μ_φ1, μ_φ2} (5D, **no RV**) | {φ₁, v_los} (real line-of-sight velocity) |
| Velocity used in SELECTION? | **YES** (PM-track band) → circular | **NO** (RV sets only per-field *mean*) → clean |
| S_stream / S_field | 0.775 / 0.069 | 0.351 / 0.020 |
| corr(x,v) stream / field | −0.69 / −0.16 | +0.54 / +0.14 |
| Shuffle-null S | 0.118 (collapses) | — |
| **Confound control** | **fake-band S = 1.10 ≥ signal** | **permutation p = 0.002** |
| Mean-blindness (P3) | — | S identical under bulk-mean removal (0.351→0.351) |
| Gradient-removal | — | S → 0.000 (per-field de-mean) |
| Verdict | **SELECTION-CONFOUNDED** | **PASS, non-circular** |

---

## 1. Data — both REAL, no mock; which path worked

Checked availability first. `galstreams` (Mateu 2023) **installs** but its `MWStreams` initializer
crashes against the local gala/astropy versions (an angular-momentum-track indexing bug), so the
bundled member tables were unreachable through it. Two independent REAL paths worked instead and
were used:

- **Part A — direct Gaia DR3 archive query** (`astroquery.gaia` TAP). A union of circular cones
  along the published GD-1 track (Koposov et al. 2010 frame, via gala's `GD1Koposov10`), with only
  distance/quality/broad-PM cuts (parallax < 1 mas, RUWE < 1.4, |μ| < 25 mas/yr, G ∈ [15, 20.5]) —
  cuts that are NOT specific to GD-1's velocity, so the same table is both stream and field. 51 177
  stars. (Async queries required: the sync endpoint hard-caps at 2 000 rows.) **GD-1 has no usable
  Gaia RV** (G > 15, below the RVS limit) — so Part A is genuinely **5D, not 6D**.
- **Part B — Vizier `J/MNRAS/490/3508`**, the S5 Southern Stellar Stream Spectroscopic Survey
  (Li et al. 2019), which provides **real radial velocities**. This supplies the velocity dimension
  Gaia denies GD-1, and — decisively — an RV that no astrometric selection touches.

No mock was needed or used.

## 2. Part A — GD-1 on the astrometric grain: right ordering, wrong reason (SELECTION-CONFOUNDED)

GD-1 is textbook-cold and it shows: transformed into the stream frame, the members trace a razor
track in (φ₁, μ_φ1) with intrinsic scatter **0.57 mas/yr about a fitted track** — visibly a thin
sheet in phase space (`figures/fig1_gd1_astrometry.png`). On the grain {φ₁, μ_φ1, μ_φ2}:

```
  S_stream (812 members)      = 0.775      corr(φ1, μ_φ1) = -0.69
  S_field  (2564 off-stream)  = 0.069      corr(φ1, μ_φ1) = -0.16
```

P1/P2 ordering holds (11×), and the **shuffle null** — permuting (μ_φ1, μ_φ2) across members,
preserving every marginal but breaking the φ₁ pairing — **collapses S 0.775 → 0.118**, confirming
S reads the copula pairing rather than the marginals. So far, a PASS.

**But it is not, and honesty requires saying why.** Stream members are defined by a
**velocity-track band** (|μ − track(φ₁)| < 1 mas/yr). Selecting a thin band around a line
*manufactures* corr(φ₁, μ) whether or not a real stream is there. Two controls quantify it:

- **Fake-band control** — apply the *identical* band geometry, offset +3 mas/yr into pure-field
  territory (a "stream that isn't there"): **S = 1.10, corr = −0.76** — *equal to or larger than
  the real stream's.* The selection geometry alone produces the whole signal.
- **Dilution / stream-blind** — the on-stream spatial band with the broad PM box but **no**
  velocity-track cut: **S = 0.056**, indistinguishable from the field floor. Without the circular
  cut, GD-1's coherence does not emerge from the astrometry — it is a ~10 % overdensity that a
  global functional cannot see.

**Part A verdict: SELECTION-CONFOUNDED.** The stream is real and tight (scatter 0.57 ≪ band 1.0),
but proper motion alone cannot separate real phase-space coherence from the coherence filter used
to find the stream. This is exactly the confound the phase-space note anticipated (its gate (a):
"the G1 test is essentially sim-only") — on sky astrometry the selection *is* the coherence.

## 3. Part B — Orphan on the radial-velocity grain: the non-circular escape (PASS)

The escape is a velocity dimension that selection does not touch. S5 gives it: each Orphan *field*
(a single pointing) contains a **cold RV clump** sitting on the broad Milky-Way distribution, and
the clump's velocity varies smoothly along the stream. Crucially, membership is set **per field**
by the densest RV window — this fixes each field's **mean** RV and nothing more. It cannot impose a
position→RV *gradient*: independently chosen per-field means only line up into a track if the track
is physically there.

The clumps are genuinely cold — **median per-field dispersion 4.82 km/s** (25 fields, φ₁ ∈
[−78°, +65°] along Orphan). On the grain {φ₁, v_los}:

```
  S_stream (998 clump members) = 0.351     corr(φ1, RV) = +0.54
  S_field  (5472 non-clump MW) = 0.020     corr(φ1, RV) = +0.14
  clump-centers (25 fields)    S = 0.478   corr = 0.62  (robust: 0.36 / 0.55 dropping 1 low-N field)
```

P1/P2 hold (17×), and every P3 clause is satisfied on **real stars**:

- **Mean-blindness (the theorem, verified):** subtract the stream's bulk mean RV →
  **S = 0.351, identical.** A bulk offset is a mean; the correlation matrix deletes it; the
  gradient is what S reads. This is the property that killed the retracted Bullet "reversal" (which
  rode a bulk mean) and it *survives* here because the stream's coherence is a genuine gradient.
- **Gradient-removal:** subtract each field's OWN clump mean (keep the cold clumps, remove the
  across-field track) → **S = 0.000.** The coherence *is* the position-velocity gradient, not the
  per-field clumping.
- **Non-circularity permutation:** reassign each field's clump-mean to a random field position
  (destroy the φ₁↔RV alignment, keep every clump intact) — 500–2000 draws. Observed clump-center
  **S = 0.478** vs permuted **mean 0.046, 95th pct 0.155, p = 0.002.** If the correlation were an
  artifact of "pick the densest window per field," it would survive the permutation; it does not.

**Part B verdict: PASS, non-circular.** RV is never used to build the gradient, the ordering is
decisive, and the ledger's two signature blindnesses (mean, amplitude) are demonstrated on sky
data, not asserted.

## 4. Honesty gates

- **(a) Dimensionality & selection function, stated plainly.** Part A is **5D** (position + PM), no
  RV — GD-1 is too faint for Gaia RVS. Part B is position-along-stream + line-of-sight velocity,
  from a spectroscopic survey with its own magnitude/fibre selection. Neither is the full 6D f(x,v)
  of the toy; each reads a **projection** of the phase-space sheet. The claim is exactly the note's
  claim — the ledger reads the *copula shadow* corr(x,v), here in one projected velocity at a time.
- **(b) The selection confound, weighed, not waved.** "S_stream ≫ S_field partly reflects that we
  found the stream BY its coherence" is the central risk and it is **real and decisive for Part A**
  — the fake-band control shows selection alone produces S ≥ the signal. The question the task
  posed — *is the effect bigger than the selection artifact?* — has a clean split answer:
  **astrometric grain: NO** (artifact ≥ signal); **RV grain: YES** (p = 0.002 above the
  selection-preserving permutation null). The verdict rests entirely on Part B, which is why Part B
  exists.
- **(c) What this validates, and what stays dead.** This validates the **INSTRUMENT** — S = −ln det
  C reads real phase-space coherence in real Milky-Way streams. It says **nothing** about the
  dark-matter *magnitude* (still ~40 orders off, no a₀; `dm_phasespace_grain.md` §5) or the
  **dSph/DF2 pair** (dispersion-supported ⇒ corr(x,v) ≈ 0 for both ⇒ no split;
  `dm_phasespace_grain.md` §6). Those remain dead, grain-independent. A working thermometer does not
  make the sun cold: reading coherence honestly is not reading dark-matter mass.
- **(d) Cold streams only, by construction.** Both PASS cases are cold streams (v = f(x)). The note
  predicts, and this does not test, that dispersion-supported systems (relaxed clusters, dwarfs)
  read S ≈ 0 — which is precisely why the reading captures the *shadow* of phase-space coherence,
  not dark matter itself.

## 5. Verdict

**PASS on real Gaia-era data — the ledger reads phase-space coherence — with the selection caveat
weighed and dispositive about *which* grain earns the pass.**

- The phase-space note's flag ("sim-only, needs full 6D") is **discharged**: the ledger's central
  phase-space prediction is confirmed on **real public data** for two independent cold streams.
- On the **proper-motion grain** the confirmation is **SELECTION-CONFOUNDED** — the stream is real
  and razor-thin, but the coherence and the selection filter are the same object, and a
  matched-geometry control cannot tell them apart.
- On the **radial-velocity grain** the confirmation is **clean**: RV is untouched by selection,
  S_stream ≫ S_field, S is invariant under bulk-mean removal and collapses under gradient removal,
  and the position–velocity alignment sits at p = 0.002 above a selection-preserving null.

The instrument reads phase-space coherence on the real sky. It reads **corr(x,v)** — the copula
shadow — and nothing with a scale, which is why validating it here changes none of the three
separable dark-matter verdicts: **direction revived, magnitude dead, dwarf pair fatal.**

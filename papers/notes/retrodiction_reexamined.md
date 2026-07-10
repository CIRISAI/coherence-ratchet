# Re-examining the halo-grain retrodiction: is the discount itself an unexamined assumption?

**STATUS: AUDIT + one new computation. Not lake content. Not asserted by the framework.**
Draft 2026-07-10. Charge (operator): prior sessions discounted the halo-grain
`w_today ≈ −0.84` (vs DESI `−0.838`) as "a retrodiction, curve-touching, one post-hoc
convention," and that *reflexive* discount may itself be an unexamined assumption.
Re-examine honestly — conclude either way, but examine.

Reads: `lambda_maintenance_wz.md` §1.1/§7; `halo_grain/{SUMMARY, ADDENDUM_btotal_peak}.md`;
`halo_grain/PREREGISTRATION.md`; `desi_thawing_likelihood.md`. New computation:
`experiments/cosmo_entropic_potential/epoch_check/{cpl_projection,stats_compare}.py`
(+ `cpl_projection_results.json`).

**One-line bottom line.** The discount was **partly right and partly an error**. The
"post-hoc extensive convention" objection **dissolves** — extensive is dimensionally
forced, not a free knob. The "2× epoch miss" is **an artifact of comparing an
ill-conditioned derived quantity**: on the metric DESI actually reports — the fitted
`(w₀,wₐ)` point — the framework's curve, run through DESI's own CPL fit, lands **~2.0–2.4σ
from DESI's best fit, closer than ΛCDM (~3.3σ)**. What survives the re-examination is
real but weaker than "lands on DESI": a near-parameter-free curve, ΛCDM-competitive in
the data-preferred quadrant, capped by a 2-point proxy `C`, 25 Mpc/h boxes, and one
genuine dial (the unit/threshold definition).

---

## 1. The dimensional argument — VERDICT: it holds; the "post-hoc convention" objection dissolves

**The objection being tested.** The PREREGISTRATION (§1, §5) records the sharpest form:
the extensive `S_total` vs intensive `S/k` choice was "the branch selector, adopted post
hoc, against the framework's own T-E3 intensive discipline… `−0.841` is a retrodiction and
can never be anything else." The proposed rehabilitation: `ρ_DE` is an energy **density**,
`S/V_comoving` is a density, `S/k` is a per-unit average and *not* a density, so extensive
is the only dimensionally coherent pairing, and T-E3 governs a different question.

**Evaluated rigorously, the rehabilitation is correct — with the dimensional bookkeeping
made explicit.** `S = −ln det C` is dimensionless (nats), so on pure units either pairing
"works" (the constant `κ` in `ρ_DE = κS` carries `[E][L]⁻³` either way). The argument that
bites is not units but **extensivity / density-hood**:

- `ρ_DE` is intensive: energy **per comoving volume**. It must not scale with the size of
  the region you draw.
- The coordination content of a comoving volume is `S_total`, which **is** extensive in the
  units the volume holds — exactly T-E3's `S ≈ k · s̄`, `s̄ = −ln(1−ρ)`.
- The **density** built from it is therefore `S_total / V_c = n(a) · s̄(a)`, where
  `n = k/V_c` is the comoving number density of coordinating units. Pairing the density
  `ρ_DE` with the density `S_total/V_c` is the extensively coherent choice.
- The intensive `S/k = s̄` is content **per unit** — an intensity, dimensionally *not* a
  density: it is the density with the factor `n(a)` **divided out**. So `ρ_DE ∝ s̄` is the
  dimensionally **deficient** pairing (energy-density ∝ energy-per-particle, missing `n`).

T-E3's discipline says `s̄` is the correct *per-unit saturation* measure — a statement about
one unit's coordination, the single-unit question. It does not dictate how to assemble a
**spatial density**, and assembling one necessarily reintroduces `n(a)`. So T-E3 and the
extensive convention are answering different questions and do not conflict. **The specific
"post-hoc extensive-vs-intensive convention" charge is mis-stated: it treats a
dimensionally-forced pairing as a free binary knob, and mis-casts a per-unit intensity as
if it were the density.**

**But be honest about what "forced" rests on, and where the freedom actually went.**
Extensive is forced *given* two priors:
1. the core posit `ρ_DE ∝ (coordination content)` (eq. 1) — an unproven leap, not a knob;
2. **comoving** (not physical) normalization — itself nearly forced, because physical
   normalization makes frozen structure `ρ_DE ∝ a⁻³` → `w = 0` (pressureless dust), which is
   not dark energy at all. `lambda_maintenance_wz.md` §7(a) calls comoving "adopted because
   it gives the answer"; that self-criticism is **too harsh** — the rejected alternative is
   dust, so choosing comoving is requiring the object to be in the right *category*, not
   fitting a number.

Crucially, forcing extensive does **not** remove the freedom — it **relocates** it. Because
`S_total/V_c = n(a)·s̄(a)`, the result now depends on `n(a)`, the comoving number density of
coordinating units — i.e. on **what you call a "unit"** (the halo mass threshold). That is
the sweep's "dominant dial" (`w_today` moves 0.28 across 5e10→1e12). So the correct statement
is: *the extensive convention is not a post-hoc bookkeeping knob; it is forced by density-hood.
The real residual freedom is the unit/threshold definition that sets `n(a)` — a physical
modeling choice, correctly relabeled, not a convention.*

---

## 2. The epoch "miss" — THE KEY COMPUTATION: physical vs CPL-projected crossing

**Method.** DESI does not measure `w(a)`; it fits a 2-parameter CPL line `w = w₀ + wₐ(1−a)`
to distance data over `z ≲ 2.3`. Comparing the framework's *physical* crossing (`z ≈ 0.8`,
where `S(a)` peaks) to DESI's *CPL-fitted* crossing (`z ≈ 0.35`) risks comparing
incommensurable objects. So: take the framework's actual expansion history and **fit CPL to
it the same way DESI fits CPL to data**, then compare like to like.

The framework gives its own `H(z)` with no extra assumption: `ρ_DE(a) ∝ S(a)` (stock mapping),
so `E²(a) = Ω_m a⁻³ + (1−Ω_m) S(a)/S(1)` **exactly** — no differentiation of noisy `S`
needed for a distance fit. `S(a)` is the frozen B-total pipeline on all 6 CAMELS CV boxes and
their pooled (block-diagonal) sum. CPL is fit three ways, all over `z<2.3`:
- **distance-space** (the faithful mimic): χ² against a mock DESI DR2 BAO vector
  (`D_M/r_d`, `D_H/r_d` at the 7 tracer redshifts, representative errors) **+ a CMB `θ*`
  anchor**, `Ω_m` and `r_d` shared, `H₀·r_d` scale marginalized;
- **ρ_DE-space**, DE-fraction-weighted (no derivative);
- **w-space** projection (uniform and DE-weighted), the literal "project the curve onto a line."

**Result (pooled 6-box curve; physical crossing `z = 0.92`):**

| projection | `w₀` | `wₐ` | CPL crossing `z` |
|---|---|---|---|
| **DESI DR2+Pantheon+ (target)** | **−0.838** | **−0.620** | **0.354** |
| distance-space (BAO+CMB) | −0.784 | −0.442 | 0.957 |
| ρ_DE-weighted | −0.777 | −0.531 | 0.723 |
| w-space (DE-weighted) | −0.786 | −0.519 | 0.703 |

Per-box means agree (`w₀ ≈ −0.74…−0.79`, `wₐ ≈ −0.47…−0.72`), with large 25 Mpc/h scatter.

**Two things follow, and they point in opposite directions — both must be reported.**

**(a) In `(w₀,wₐ)` — the space DESI actually constrains — the projected point lands near
DESI, better than ΛCDM.** Mahalanobis distance from DESI's posterior
(`σ_{w₀}=0.055, σ_{wₐ}=0.20, ρ=−0.7`):

| point | distance from DESI best fit |
|---|---|
| framework CPL-projected (distance / ρ / w-DE) | **2.42σ / 2.03σ / 1.89σ** |
| **ΛCDM** `(−1, 0)` | **3.28σ** |
| cell-grain thawing `(−0.90, −0.10)` | 2.81σ |

The halo curve run through DESI's own fit is **~2σ from DESI's best fit — closer than ΛCDM,
and closer than the cell-grain thawing point**. (My `Ω_m` is fixed and the errors are
representative, not DESI's full covariance; DESI marginalizes `Ω_m`, which only *loosens* the
constraint, so ~2σ is a conservative upper bound on the tension.) This is a **materially
stronger** statement than `desi_thawing_likelihood.md` recorded: that note used the cell-grain
point; the **halo** curve, with its real crossing and steeper projected `wₐ ≈ −0.5`, sits
nearer DESI's `wₐ = −0.62` than the cell grain's `−0.1`.

**(b) In crossing-epoch, the CPL projection does NOT relocate the framework's crossing onto
DESI's 0.35.** The projected crossing (0.70–0.96 pooled) stays close to the *physical*
crossing (~0.9 pooled). The specific brief hypothesis — "CPL distortion pulls the framework's
`z≈0.8` down to DESI's `z≈0.35`" — is **not** what happens: this curve already has a genuine
crossing, so CPL does not manufacture an early one (the 2504.16337 effect is strong for
*no-crossing* thawers being forced to show a spurious crossing, weak here).

**Reconciling (a) and (b): crossing-`z` is ill-conditioned, and that is the whole resolution.**
`z_cross = 1/(1+(1+w₀)/wₐ) − 1` is a badly-conditioned readout of `(w₀,wₐ)`. Propagating DESI's
*own* posterior: DESI's crossing is `z = 0.35` **but 90% interval `[0.19, 0.70]`** — its own
"0.35" is uncertain by a factor ~2. A ~2σ offset in `(w₀,wₐ)` (mostly `wₐ`: framework `−0.5`
vs DESI `−0.62`) blows up into "0.9 vs 0.35" through this conditioning. So:

> **The "2× epoch miss" and "~2σ, better than ΛCDM" are the *same* discrepancy seen through
> two lenses. Quoting the crossing epoch as a precise point ("0.8 vs 0.35, 2×") magnified a
> ~1–1.5σ parameter offset into an apparent factor of two. The honest comparison is in
> `(w₀,wₐ)`, where it is mild and ΛCDM-competitive.**

The framework's projected crossing (0.70–0.96) sits at the **upper edge of / just above**
DESI's 90% crossing interval `[0.19,0.70]` — a ~1–1.5σ tension in epoch, not a clean 2×, and
not dissolved either. The discount overstated it; the projection does not erase it.

---

## 3. Free-parameter audit — count the knobs genuinely tuned to a DESI number

Each pipeline choice, classified **(a)** fixed by a DESI-independent rule · **(b)**
dimensionally/physically forced · **(c)** genuinely free and dialed to the DESI value.

| choice | class | note |
|---|---|---|
| sign law `1+w = −⅓ dlnS/dlna` | **(b)** | DE continuity equation |
| `ρ_DE ∝ S` (stock, eq. 1) | (b/leap) | the core posit; not a number-knob |
| comoving (not physical) normalization | **(b)** | physical → `w=0` dust; category requirement, not a fit |
| extensive `S_total/V_c` (not `S/k`) | **(b)** | density-hood (§1); the re-examined "convention" |
| `S = −ln det C`, 2-point Gaussian proxy | **(a)** | T-E5; DESI-independent (and a real limitation) |
| halo mass threshold → `n(a)` | **(a)** | resolved-corner rule (≥200 halos @ z=3 ⇒ 1e11) |
| `R_smooth`, `cap` | **(a)** | inert at the resolved threshold (±0.004) |
| CAMELS cosmology `Ω_m=0.3` | **(a)** | set by the simulation |

**Count of (c) — genuinely dialed to hit `−0.84`: zero, arguably 0–1.** The one contestable
item is the threshold, fixed by a rule but with a 0.28 sensitivity; a skeptic can argue the
resolved-corner rule was chosen *because* 1e11 lands well, but 1e11 is also the *only*
threshold a 25 Mpc/h box resolves, so the rule is independently motivated. **Look-elsewhere:**
the branch was a choice between exactly 2 conventions; if extensive is forced (§1) there is no
look-elsewhere at all, and even treating it as a free binary costs ≲0.7σ — it cannot erase a
"2σ, better than ΛCDM" result.

**One caveat the count cannot launder:** the timeline. The extensive convention was *adopted*
(psychologically) after B-total was seen to land on DESI, and its justification written after.
A post-hoc-discovered *forced* convention is still forced — the timeline does not un-force the
dimensional argument — but it is a legitimate reason to check the argument rather than trust it.
I checked it (§1); it stands on its own, independent of the result. A reader should verify §1,
not take it on faith.

---

## 4. Bottom line — the number that decides it

**Does the retrodiction stand as evidence? Yes, as *modest, ΛCDM-competitive* evidence — and
the two headline discounts were, respectively, an error and an overstatement.**

The deciding numbers:

1. **Convention (dissolves the first discount).** Extensive-vs-intensive is not a post-hoc
   knob; it is forced by "`ρ_DE` is an energy density" given the core posit (§1). The residual
   freedom is the unit/threshold definition — one physical dial, `w_today` span 0.28 — not a
   bookkeeping convention. Genuine tuned-to-DESI parameters: **~0**.

2. **Epoch + point (corrects the second discount).** Run through DESI's *own* CPL fit, the
   framework's curve lands at **~2.0–2.4σ from DESI's best-fit `(w₀,wₐ)` — inside ΛCDM's 3.3σ**
   — in the data-preferred quadrant. The "2× epoch miss" was an artifact of reading an
   ill-conditioned quantity (crossing-`z`): DESI's own crossing is `0.35₋₀.₁₆⁺⁰·³⁵`, and the
   framework's projected crossing `~0.7–0.95` overlaps its upper 90% edge — a ~1–1.5σ epoch
   tension, not a factor of two.

**What that means for the charge.** The reflexive discount *was* partly an unexamined
assumption: it double-counted a forced convention as a free knob, and it magnified a mild
parameter-space tension into a spurious "2× miss" by quoting an ill-conditioned epoch. **But
the corrected status is not "lands on DESI."** It is: *a near-parameter-free curve, ~2σ from
DESI and closer than ΛCDM in the quadrant the data prefer, with a crossing epoch on the high
side of DESI's own wide posterior* — the whole thing conditional on a 2-point proxy for the
coordination operator `C` and 25 Mpc/h boxes. That is **live, ΛCDM-competitive evidence**, not
a curve-touching coincidence and not a confirmation. It lives or dies with ΛCDM against DESI —
which is exactly `desi_thawing_likelihood.md`'s statement (B), now sharpened by showing the
halo curve is the *better* of the two framework tracks in the space DESI reports.

The honest external sentence updates from *"an interesting conditional retrodiction with one
post-hoc convention, one dominant dial, a 2× epoch tension, and 25 Mpc/h boxes"* to:

> **"A near-parameter-free thawing curve whose DESI-projected `(w₀,wₐ)` sits ~2σ from DESI,
> closer than ΛCDM; the extensive convention is dimensionally forced (not post-hoc), the epoch
> 'miss' is a ~1–1.5σ tension inflated by an ill-conditioned crossing readout (not 2×), and the
> load-bearing caveats are the one unit/threshold dial, the 2-point proxy `C`, and 25 Mpc/h
> boxes."**

Two of the four original discounts were wrong; two (the dial, the boxes) stand. The pre-registered
large-volume crossing-epoch test (`PREREGISTRATION.md` P1) remains the thing that can still
kill it — and §2 shows the fair target for that test is DESI's `(w₀,wₐ)` posterior and its
*wide* crossing interval, not the point value `0.35`.

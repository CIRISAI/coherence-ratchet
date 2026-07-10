# The dark-matter reading on the phase-space grain — direction revived, magnitude and the dwarf pair still dead

**Date 2026-07-10. Companion to `reversal_adversarial_audit.md`, `bullet_cluster_correction.md`
(retracted), `dm_coherence_priorart.md`, and `gravity_dark_matter_reading.md` §8.** Toy:
`experiments/dm_coherence/phasespace/phasespace_grain.py` (seed 20260710; every number below is
executed output, `results.json`).

**The charge.** Both the Bullet "kill" and its "reversal" computed S = −ln det C on a
**velocity-component** correlation matrix — units = galaxies, variables = (vx,vy,vz). That grain
is mean-removed (blind to bulk velocity, a MEAN) **and it discards position entirely.** On it
S(cold) = S(thermal) = 0: *silent.* The reversal-audit itself recorded "on the velocity-component
grain the ledger is silent." The charge: silent is not dead — the grain was wrong, and the
framework's own object for a self-gravitating collisionless system is **phase space** (position
AND velocity together), where DM/collisionless stars fold onto a thin low-entropy sheet (Liouville;
Abel, Hahn & Kaehler 2012, arXiv:1111.3944) while shocked gas thermalizes and fills phase space.
This note fixes the grain first (Gate-0) and reports what the ledger actually says.

**Bottom line up front.** Fixing the grain **revives the DIRECTION** and does so through a
genuinely different object than the retracted reversal — proven, not asserted, by bulk-velocity
invariance. It leaves the **MAGNITUDE dead** (grain-independent, if anything worse) and the
**dSph/DF2 pair fatal** (the grain cannot split them). Three separable verdicts, and only one
moves.

---

## 1. Enumerate the grains honestly

For a self-gravitating collisionless system the coordinating structure could be read on any of:

| Grain | units × variables | what S = −ln det C measures | mean-blind? | amplitude-blind? |
|---|---|---|---|---|
| **G0 velocity-component** (the kill's grain) | galaxies × (vx,vy,vz) | correlation *among velocity components* | **yes** (bulk = mean, removed) | yes (clause 3) |
| **G1 x-v copula** (particles as samples) | particles × (x,y,z,vx,vy,vz) | correlation *between position and velocity* — corr(x,v) | **yes, and correctly so** | yes |
| **G2 phase-space density Q** = ρ/σ³ | — | the Liouville-protected coherent/incoherent *magnitude* | n/a | **Q is an amplitude → clause 3 blinds S to it** |
| **G3 occupation copula** | phase-space cells × occupation | whether occupied cells co-vary across the sheet | yes | yes |

**The crux, stated once.** The DM-is-coherent literature is about **G2** (phase-space density; a
cold stream is a thin high-Q sheet, a thermal blob is low-Q). But **Q is a density magnitude, and
S is amplitude-blind by a proved theorem (clause 3, `copula_blindness`/T-L2).** The ledger cannot
read Q. What the ledger *can* read of the phase-space sheet is **G1: corr(x,v)** — the copula
between position and velocity. And corr(x,v) is a legitimately different object from the bulk mean
that G0 deletes:

- a **bulk velocity** is `v = V₀` (same everywhere) ⇒ corr(x,v) = 0 — a mean, correctly invisible;
- a **cold sheet/stream** is `v = f(x)` (velocity varies with position) ⇒ corr(x,v) ≠ 0 — a real
  correlation that survives mean removal *and* amplitude rescaling;
- a **thermal blob** is `v ⊥ x` (Maxwellian, position-independent) ⇒ corr(x,v) = 0.

So G1 reads the sheet's x-v *gradient*, not the bulk *offset*. This is the whole question of
whether the grain is a fix or the mean error relabeled — settled numerically in §3.

---

## 2. Cold-sheet vs thermal-blob S ordering (G1) — the predicted inversion holds

Matched total mass (same N=20000) and matched spatial extent (same σ_x). Cold sheet: `v = H·x +`
thin noise (σ_sheet = 0.05). Thermal blob: `v ~ N(0,σ)` independent of x.

```
                 x-v copula grain (G1)      velocity-component grain (G0, the kill)
  cold sheet     S = 5.98 (1D), 18.0 (3D)   S = 0.0003   <- SILENT (position discarded)
  thermal blob   S = 0.00 (1D),  0.00 (3D)  S = 0.0000   <- SILENT
```

The DM-is-coherent ordering — **cold sheet HIGH S, thermal blob LOW S** — holds on the
phase-space grain and is **the opposite of the velocity grain, where both are silent.** The kill
was silent on the sheet *because G0 threw away position*; the sheet's entire signal lives in
corr(x,v), which G0 does not contain. **On this the charge is correct: the reading was killed on a
grain that structurally cannot see the claimed structure.**

Robustness (Part 3): S rises smoothly and monotonically as the sheet thins (σ_sheet 2.0→0.01 gives
S 0.22→9.2); at σ_sheet ≈ σ_thermal the "sheet" is no longer cold and S → thermal value; N-stable
(5.94→6.01 over N = 1k→100k). Not a knife-edge artifact.

---

## 3. Is this the mean-blind reversal relabeled? — NO, and it is executed, not asserted

The reversal's engine was "coherent bulk motion (4500 km/s) = perfect correlation = high S." That
signal is a **mean**; G0 and every correlation matrix delete it. The decisive test: add a bulk
velocity to the G1 systems. If the sheet's high S is the bulk mean, it dies; if it is the x-v
gradient, it survives.

```
  V_bulk =        0.0 :  S_sheet = 5.996    S_thermal = 0.000
  V_bulk =     4500.0 :  S_sheet = 5.998    S_thermal = 0.000
  V_bulk =  1,000,000 :  S_sheet = 5.997    S_thermal = 0.000
```

**S_sheet is invariant under the bulk shift** (same for the two-clump Bullet model in §5:
0.7788 → 0.7788 under a global 10⁶ boost). The sheet's S is the x-v *gradient*, a genuine copula
feature that survives both blindnesses that killed G0. **The phase-space grain is a genuinely
different object, not the mean error relabeled.** This *corrects a framing in
`reversal_adversarial_audit.md`*: that audit's "every grain that makes galaxies look correlated
hands the gas an equal-or-larger S" is true for the *spatial-velocity-field* grain it considered,
but the x-v copula is a grain it did not test, and on it the coherent component is distinguished by
a real, mean-blind-surviving correlation. The reversal was killed on the wrong grain. That does
**not** mean the reversal's *conclusion* is rescued — see the three verdicts.

**One honesty caveat on G1 itself.** A *folded* phase-space sheet (multi-stream regions) has v as
a multi-valued function of x; the linear/Gaussian corr(x,v) that S = −ln det C reads is the
pairwise shadow (LedgerLaw, "known hole") and misses folds — those are the **order-≥3 blind spot**.
So even on G1 the ledger reads only the single-valued (unfolded) part of the sheet's coherence.

---

## 4. Separable verdict A — DIRECTION: revived, defensibly, but circular and geometry-bound

On G1 the Bullet's asymmetry is real and copula-visible (§5, Part 6): model the merger as two
infalling clumps. The **galaxies** (collisionless) keep the two-clump infall x-v structure
(S = 0.779); the **gas pre-shock** shares it exactly (S = 0.778); **post-shock the gas
thermalizes** — its ordered infall velocity converts to disordered thermal motion and corr(x,v)
collapses (**S = 0.004**). The ledger points at the collisionless galaxies (= the lensing mass),
and it does so through a **genuine ordered→disordered copula change that survives a global bulk
shift** — not the retracted mean error.

**But this is not a win, for three reasons that all survive the grain fix:**

1. **Merger-geometry-specific.** The galaxy signal is the two-clump *infall* x-v gradient. A
   **relaxed** cluster has no infall gradient — its dispersion-supported galaxies give corr(x,v) ≈ 0
   (Part 4), so G1 is silent there — and in relaxed clusters the missing mass **tracks the hot gas**
   at ≈10:1 (Famaey, Pizzuti & Saltas 2025, arXiv:2410.02612), the *opposite* of the reading. The
   Bullet is the one transient geometry where "tracks galaxies" and "tracks gas" separate and the
   reading wins; it does not generalize.
2. **Circular with CDM.** "Dark mass sits with the collisionless component" is the definition of
   CDM. G1 fixes the *direction* for a defensible reason (phase-space coherence, not a mean error)
   — a real improvement over the silent G0 — but it adds no ledger-specific content CDM lacks.
3. **Coarse-grained and modest, not the Liouville sheet.** The high-S "thin sheet" of §2 is a
   *fine-grained* object; the Bullet's real galaxies are dispersion-supported (σ ~ 1000 km/s) and
   the coarse signal is the modest infall structure (S ~ 0.8), not S ~ 18.

**DIRECTION verdict: revived from SILENT to a defensible point-at-the-galaxies — genuinely
different from the mean-blind reversal — but merger-geometry-bound and circular with CDM.**

## 5. Separable verdict B — MAGNITUDE: dead, grain-independent, if anything worse

The magnitude problem (`dm_coherence_priorart.md` §2: ε ≈ 10⁴⁶–10⁵⁶ J/nat, 37–47 orders above
Planck; no a₀ from a shape-only S) is **independent of grain.** S is a dimensionless copula
functional carrying no length, mass, or acceleration scale (clause 3, a theorem); no choice of
grain manufactures a₀. Worse: the phase-space sheet is **low-dimensional** (thin ⇒ few effective
modes), so its coordination-nat count is *small*, pushing ε = ΔE/S **up**, not down. The grain fix
does nothing here and mildly aggravates it. **MAGNITUDE verdict: DEAD, unchanged.**

## 6. Separable verdict C — the dSph/DF2 pair: still kills it, on either grain

Segue 1 (M/L ~ 3400, most DM known) and NGC1052-DF2/DF4 (M/L ~ 1, no DM) are the **same kinematic
class** — dispersion-supported stellar systems, v isotropic and ~independent of x. On G1 both give
corr(x,v) ≈ 0:

```
  S_Segue1-like = 0.0009   (M_dark/M_bary ~ 3000)
  S_DF2-like    = 0.0009   (M_dark/M_bary ~ 0)
```

**Identical S; observation splits them by 3–4 orders.** A one-variable ΔM_eff ∝ S cannot produce
that split. Nor does the fine grain help: both are collisionless stellar systems, so both preserve
fine-grained phase-space density (Q) **equally** by Liouville — a fine-grained measure has no
discriminating power between them (exactly the `dm_coherence_priorart.md` §3a argument, which the
grain fix does not touch). Whichever grain you pick, you must use it for both, and neither splits
the pair. **dSph/DF2 verdict: KILLS it, grain-independent.**

---

## 7. Honesty gates

- **(a) Measurability.** G1 needs the full 6D f(x,v). Real systems give **projected** position (2D)
  and **line-of-sight** velocity (1D); full phase space exists only in simulations (and, partially,
  the solar neighborhood via Gaia). **The G1 test is essentially sim-only.** The §2 inversion and
  the §5 Bullet direction are demonstrated in a toy, not measured on sky data.
- **(b) Q vs the copula.** The literature's coherent/incoherent variable is Q (phase-space
  density), which *does* separate sheet from thermal (toy: Q ratio 3.9×). But **Q is an amplitude
  the ledger is blind to (clause 3).** The ledger reads only corr(x,v), which fires for *cold
  streams* (v = f(x)) and is silent for *dispersion-supported* systems (dwarfs, relaxed-cluster
  galaxies). The reading therefore captures the *shadow* of phase-space coherence, not the thing
  itself.
- **(c) "The framework's prescribed grain" is not unique.** LedgerLaw defines S on a normalized
  correlation matrix of *a* field across *units* without uniquely fixing which, for a gravitating
  system. G1 is the most defensible phase-space grain and the cleanest separation from the mean
  error — but "fix the grain" has no single forced answer; this note picks the strongest candidate
  and reports it.

---

## 8. Bottom line — which of {revive, revive-direction-only, dead}

**Revive the direction only.** Precisely:

- **The grain was wrong, and fixing it matters.** The velocity-component grain was silent on the
  phase-space sheet because it discarded position. On the x-v copula grain the DM-is-coherent
  ordering (cold sheet high S, thermal low S) holds, and it is a **genuinely different object from
  the retracted mean-blind reversal** — proven by bulk-velocity invariance, not asserted. The
  reversal-audit's "same mean error on every grain" is too strong: it did not test the x-v copula.
- **Direction: revived** from SILENT to a defensible point-at-the-lensing-mass for the Bullet
  (via a real ordered→disordered copula change) — but merger-geometry-specific, silent in relaxed
  clusters (where the data point the other way), and circular with CDM. A cleaner epitaph than
  "mean-blind," not a victory.
- **Magnitude: dead**, grain-independent, mildly worse (thin sheet ⇒ small S ⇒ larger ε; still no a₀).
- **dSph/DF2 pair: dead**, grain-independent (both dispersion-supported ⇒ identical S; fine-grained
  Q preserves both equally ⇒ no split on either grain).

The reading is **still dead** — but the cause of death is now stated correctly. It is not "the
ledger is silent / mean-blind." It is: **the ledger reads only the copula shadow (corr(x,v)) of
phase-space coherence — which fires for cold streams, misses dispersion-supported dark matter
entirely, and carries no scale.** That reads the Bullet's direction honestly and dies, unchanged,
on magnitude (~40 orders) and on the two dwarfs that are identical to it and 10³–10⁴ apart in the
sky.

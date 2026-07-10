# Verlinde's emergent gravity on SPARC: reproduce the death, test the maintenance repair

**STATUS: [computed]. Verdict NULL — the repair is REFUTED, not merely underpowered.**
A falsifiability-today exercise. Draft 2026-07-10.

**Grading key:** **[theorem]** = discharged in Lean; **[computed]** = numerically established,
not mechanized; **[conjecture]** = a stated bet with a falsification path.

**Depends on:** `experiments/dm_coherence/verlinde/{verlinde_repair.py, results.json, figures}`
(the run); `experiments/dm_coherence/sparc/` (the validated RAR pipeline this REUSES —
same table1/table2, same cuts, reproduces g† = 1.16×10⁻¹⁰, scatter 0.133 dex);
`papers/notes/gravity_dark_matter_reading.md` §8.3 (the systematic-floor numbers, RESPECTED);
`formal/CoherenceRatchet/LedgerLaw.lean` clause 5 (maintenance = active coordination / broken
detailed balance; note the "rent tracks held STOCK" amplitude gloss was RETIRED 2026-07-10 as
agent-specific — the maintenance axis is a *coordination* coordinate, not an amplitude one).

**One-line answer.** Verlinde's EG dies on SPARC exactly as Lelli+2017 reported — the residual
correlates with radius (ρ = +0.26, CI excludes 0) and it needs the stellar M/L cut by ~1.4×. Our
distinctive second axis — maintenance / coldness — does **not** repair it. A weak maintenance
signal exists with the pre-registered opposite-pole structure, but it **loses to radius on both
decisive tests** and sits an order of magnitude below the systematic floor. **Radius, not
maintenance, owns the EG residual.** The door closes cleanly.

---

## 1. The exact EG equations implemented

From Lelli, McGaugh & Schombert (2017, arXiv:1702.04355; MNRASL 468 L68), which tests Verlinde
(2016, arXiv:1611.02269). Acceleration scale `a₀ = c H₀/6 ≈ 1.2×10⁻¹⁰ m/s²` (they adopt the MOND
convention `a₀ = 1.2×10⁻¹⁰`).

```
Eq 3 (Verlinde 2016 Eq. 7.40, apparent dark mass M_D for spherically symmetric M_b):
        ∫₀ʳ  G M_D²(r̂) / r̂²  dr̂  =  M_b(r) · a₀ · r
Eq 4 (differentiate Eq 3, ×G/r²):
        g_D = G M_D/r² = √(a₀) · √( g_b + (G/r) ∂M_b/∂r )
Eq 5 (total centripetal acceleration — THE relation fit here):
        g_t = g_b + g_D = g_b ( 1 + √(a₀/g_b) · √( 1 + (G/(g_b r)) ∂M_b/∂r ) )
Eq 6 (point-mass deep-MOND limit; ∂M_b/∂r = 0, g_b ≪ a₀):
        g_t = V²/r = √(a₀ g_b)
```

Evaluated in the spherical approximation Lelli+2017 use as their statistical starting point
(spherical-vs-disc geometry differences ~20%, §2.1). With the spherical-equivalent enclosed mass
`M_b(r) = g_b(r) r²/G`, the inner square-root term reduces **algebraically** to a clean
per-galaxy log-derivative:

```
        1 + (G/(g_b r)) ∂M_b/∂r  =  3 + d ln g_b / d ln r
```

(verified: a point mass `g_b ∝ r⁻²` gives term = 1 → Eq 6; a flat rotation curve gives term = 2).
**The entire radius-dependence of EG lives in this term:** at large r where M_b saturates it → 1
(MOND); at small/intermediate r it exceeds 1 (the EG "hook" above the RAR, Lelli+2017 Fig. 1–2).
Therefore `Δ_EG = log₁₀ g_obs − log₁₀ g_EG` **must** carry a radius structure if EG is wrong about
that hook — which is exactly the failure mode we go looking for. `term ∈ [−0.74, 6.80]`, median
1.80 across the sample.

---

## 2. Instrument check + his reproduced death

**Instrument — PASSED.** Same pipeline as `../sparc`: 2,688 points / 141 galaxies (Q ≤ 2,
inc ≥ 30°, per-point fractional V error ≤ 0.10). MOND RAR reproduced: `g† = 1.166×10⁻¹⁰ m/s²`
(literature 1.20), scatter **0.132 dex** (reference band 0.11–0.13). The pipeline sees what the
field sees.

**His death — REPRODUCED, both failure modes.** [computed]

| Lelli+2017 finding | Our reproduction | Verdict |
|---|---|---|
| (i) EG needs stellar M/L substantially **below** fiducial | mean `Δ_EG = −0.153 dex`: at Υ=0.5/0.7 EG **overpredicts** g by 0.15 dex, i.e. demands M/L cut by **1.42×** | ✓ reproduced |
| (ii) EG residual should **correlate with radius**; not observed for the true law | `Δ_EG` vs `log r`: partial ρ = **+0.261**, CI [0.152, 0.371], p ≈ 0 (controls: inc, Qual) | ✓ EG's own residual carries the predicted radius correlation |

A clean, and slightly sharper-than-expected, kill: the EG residual tracks **physical radius**
(ρ = +0.26) but is **flat in g_bar** (ρ = −0.006, CI includes 0). The EG failure is specifically a
*radius* residual, not an acceleration one — which matters for the confound analysis below.
Figure `fig1_eg_death.png`.

---

## 3. The repair test — three sub-results

**The claim (pre-registered, `verlinde_repair.py` header, before fitting):** the residual Verlinde
mis-attributes to radius is better explained by a maintenance/coldness proxy. Directional:
**H1** `Δ_EG` correlates *more* with maintenance than with radius (joint model); **H2** controlling
maintenance *flattens* the `Δ_EG`–radius correlation; **H3** the maintenance signal *survives* an
explicit g_bar control. Proxies: `f_gas` = V_gas|V_gas|/V_bar² (cold, rotationally coherent H I →
HIGH maintenance); `f_bul` = Υ_b V_bul²/V_bar² (dispersion-supported bulge → LOW maintenance, the
opposite pole).

**(a) Maintenance partials (controls: inc, Qual; then + g_bar).**

| proxy | partial ρ \| inc,Qual | 95% CI | + g_bar control | reading |
|---|---|---|---|---|
| `f_gas` (cold H I, high maint.) | **−0.064** | [−0.169, +0.083] | −0.136, CI [−0.24,−0.03] | NULL band unless g_bar removed |
| `f_bul` (bulge, low maint.) | **+0.209** | [+0.048, +0.343] | +0.270, CI [+0.13,+0.40] | WEAK, CI excludes 0, **opposite sign to f_gas** |

The pre-registered **opposite-poles structure holds** (f_gas < 0, f_bul > 0): "maintenance" is not
a pure empty relabelling of a single mass/SB proxy. But both effects are weak, and note the
signal *strengthens* under g_bar control rather than collapsing (see gate ii).

**(b) THE KEY FLATTEN TEST (H2) — FAILS, and reverses.**

```
radius corr before maintenance control:  ρ = +0.261   CI [0.152, 0.371]
radius corr after  controlling f_gas:     ρ = +0.300   CI [0.164, 0.416]   ← STRONGER, not flatter
```

Controlling for maintenance does **not** absorb the radius residual; it slightly *strengthens* it.
The repair signature — maintenance eating the radius correlation — is **absent and pointing the
wrong way**. (Mechanically: radius and f_gas are positively correlated (+0.34) while f_gas relates
weakly *negatively* to Δ_EG, so removing f_gas lifts a mild suppression.)

**(c) HORSE RACE (H1) — radius wins decisively.**

| joint model `Δ_EG ~ …` (controls inc, Qual) | std. coeff | partial R² (unique variance) |
|---|---|---|
| radius (`log r`) | +0.319 | **0.089** |
| maintenance (`f_gas`) | −0.169 | **0.025** |
| — radius wins | | **3.5×** |
| + g_bar added: radius | +0.315 | 0.087 |
| + g_bar added: maintenance | −0.354 | 0.031 |
| + g_bar added: g_bar itself | −0.217 | 0.012 |

Radius carries ~3.5× the unique variance of maintenance in the base model, and still dominates in
every specification. g_bar itself contributes almost nothing unique (R² = 0.012), consistent with
the flat `Δ_EG`–g_bar correlation.

Figures `fig2_repair_maintenance.png`, `fig3_horserace_flatten.png`.

---

## 4. The four honesty gates

**(i) The systematic floor (the decisive gate).** The RAR observed scatter is 0.13 dex, of which
~0.10 dex is nuisance (Υ*, distance, inclination) and only 0.034 dex is intrinsic (Desmond 2023).
The maintenance effect in dex-space is `|ρ|·σ_resid`:

```
f_gas:           0.008 dex   (g_bar-controlled 0.018 dex)
f_bul:           ~0.028 dex
systematic floor: 0.10  dex   >>  every maintenance effect above
```

Every maintenance signal, including the resolved f_bul one, sits **an order of magnitude below the
systematic floor** — uninterpretable as physics. Resolvable |ρ| at 2σ over 141 galaxies ≈ 0.17.
**Crucially, this is not a symmetric power failure:** we *did* cleanly resolve the radius
correlation (ρ = +0.26, well above 0.17) and the horse-race outcome (radius R² 3.5× maintenance).
So the repair is **refuted**, not merely unresolved — radius is measured to win.

**(ii) The g_bar confound.** `f_gas` is **86% rank-collinear with g_bar** (Spearman −0.863) — gas-rich
systems are the low-acceleration dwarfs. This is the gate the brief flags: a Δ_EG–f_gas correlation
could be Verlinde's own g_bar-dependence in disguise. The honest resolution is subtler than either
"survives" or "collapses": `Δ_EG` **does not track g_bar at all** (ρ = −0.006), so the EG residual
is genuinely a *radius* residual, not an acceleration one, and the f_gas signal is therefore not
literally g_bar relabelled (indeed it *strengthens* to −0.136 when g_bar is partialled out, because
g_bar removal strips f_gas's dominant shared variance and leaves a small radius-flavoured residual).
The maintenance proxy is entangled with **both** g_bar (86%) and radius (34%); radius wins the
disentangling. So: not CONFOUNDED-by-g_bar in the naive sense, but not separable enough to be a
clean independent axis either.

**(iii) This is a modification of Verlinde's INPUT, not a rescue.** The test swaps his radius
coordinate for a maintenance coordinate inside an otherwise-unchanged EG apparent-DM formula. It
does not restore his theory (which stays dead on the M/L suppression and the relativistic/cluster
failures the reading note catalogues); it asks only whether *our* coordinate would have absorbed
the residual that killed his. It does not.

**(iv) Competing explanations for the same residual, named.** The radius residual has at least two
standard homes that need no new axis: **MOND's external-field-effect** (the ambient galactic field
modulates the low-acceleration behaviour radius-dependently) and **ordinary baryonic-feedback
scatter** (feedback moves inner DM density by factors of a few — the core–cusp systematic, reading
§8.3). Either accounts for a radius-correlated residual at the ~0.1 dex level without invoking a
coordination coordinate. We do not claim to distinguish these; we claim only that maintenance is
not needed and does not help.

---

## 5. Verdict — NULL (repair REFUTED)

```
┌───────────────────────────────────────────────────────────────────────────┐
│  H1  maintenance beats radius (unique variance) ...... FALSE (radius 3.5×)  │
│  H2  maintenance flattens the radius residual ........ FALSE (+0.26→+0.30)  │
│  H3  maintenance survives g_bar control .............. TRUE  (but moot)     │
│  above the 0.10 dex systematic floor ................. FALSE (0.008 dex)    │
│  opposite-poles (f_gas<0, f_bul>0) as predicted ...... TRUE                 │
└───────────────────────────────────────────────────────────────────────────┘
```

**VERDICT: NULL — the maintenance repair is REFUTED.** A weak maintenance signal exists with the
pre-registered opposite-pole structure, so this is not a bare "no signal" null; but it **loses to
radius on both decisive tests** (horse-race 3.5×; flatten reverses), and the residual effect sits
an order of magnitude below the systematic floor. Because radius is cleanly *resolved* as the
winner, the outcome is a refutation rather than UNDERPOWERED, and because Δ_EG is flat in g_bar it
is not CONFOUNDED-by-acceleration in the naive sense either. **Radius, not maintenance, owns the EG
residual.**

This closes the maintenance channel honestly and on the record, consistent with the reading note's
bottom line: the framework's contribution to the dark-sector discussion is the *residual
discipline* (§8.3), not a modified-gravity repair. Verlinde's radius residual is real; our second
axis does not claim it.

---

## Sources

- Lelli, McGaugh, Schombert & Pawlowski 2017, "Testing Verlinde's Emergent Gravity with the Radial
  Acceleration Relation," [arXiv:1702.04355](https://arxiv.org/abs/1702.04355); MNRASL 468, L68.
- Verlinde 2016, "Emergent Gravity and the Dark Universe," [arXiv:1611.02269](https://arxiv.org/abs/1611.02269) (Eq. 7.40).
- Lelli, McGaugh & Schombert 2016, SPARC database, AJ 152, 157.
- McGaugh, Lelli & Schombert 2016; Li & McGaugh 2018 (0.057 dex); Desmond 2023 (0.034 dex intrinsic)
  — the systematic-floor chain, via `gravity_dark_matter_reading.md` §8.3.

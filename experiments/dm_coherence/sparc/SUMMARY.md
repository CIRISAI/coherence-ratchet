# SPARC coherence-residual test — ORPHANED prediction, verdict UNDERPOWERED (strong form excluded)

**Status: the pre-registered prediction was ORPHANED between registration and result** — its
motivating mechanism (`bullet_cluster_correction.md`) was retracted the same day
(`reversal_adversarial_audit.md`: S acts on a mean-removed correlation matrix; coherent
bulk/rotational motion is a mean and invisible to S). Run to completion anyway as a
null-hypothesis check, per instruction. Summary written by the orchestrator from
`results.json` (executed numbers; the assigned agent was blocked from writing .md files).

## Instrument check — PASSED

Real SPARC data: 149 galaxies, 2,700 rotation-curve points after quality cuts (Q ≤ 2).
Reproduced the radial acceleration relation: fitted g† = 1.16 × 10⁻¹⁰ m s⁻²
(literature 1.20 × 10⁻¹⁰), observed scatter **0.133 dex** (reference band 0.11–0.13 dex).
The pipeline sees what the field sees.

## Results against the orphaned prediction

Prediction (registered before fitting, mechanism now dead): RAR residual correlates
**negatively** with the dispersion-supported baryon fraction (f_bul), and cold coherent gas
(f_gas) behaves oppositely to f_bul.

| proxy | partial ρ (controlling systematics) | 95% CI | dex effect | reading |
|---|---|---|---|---|
| f_bul (dispersion-supported) | **+0.119** | [−0.060, +0.275] | 0.016 | WEAK; **sign opposite to prediction** |
| f_gas (cold rotating H I) | **−0.177** | [−0.289, −0.037] | 0.023 | excludes zero; **also opposite to prediction** |
| bulge-only subsample (n=31) | −0.031 | [−0.323, +0.247] | — | null |

- **The strong form of the orphaned prediction is EXCLUDED** (`strong_negative_excluded_fbul:
  true`): no large negative coherence–residual correlation exists.
- The weak signals that do exist have the **wrong signs** relative to the prediction, and are
  not mutually same-signed (so the coherence proxy is not merely a surface-brightness alias —
  the EMPTY-VARIABLE outcome did not obtain either).
- **Both effect sizes (0.016, 0.023 dex) sit far below the ~0.10 dex systematic floor**
  (stellar M/L, distance, inclination; intrinsic RAR scatter 0.034 dex). At n = 149 (31 with
  bulges), the 1σ-resolvable partial is 0.18 for f_bul. Anything at this level is
  uninterpretable as physics.

## Verdict

**UNDERPOWERED** for the subtle version; **the strong form is excluded**; the resolvable signs
run *against* the (already-dead) prediction. Combined with the same-day mechanism retraction,
the magnitude squeeze (ε 37–47 orders above Planck), and the dSph/DF2 pair (same
kinematic class, 3–4 orders apart in dark mass), this closes the last open channel:

> The DM-coherence reading is dead on mechanism, dead on magnitude, dead on the dwarf pair,
> and its one pre-registered observational signature is excluded where resolvable.

The f_gas partial (−0.18, CI excluding zero, 0.023 dex) is a real feature of the SPARC
residuals and is consistent with known RAR phenomenology (gas-rich systems sit slightly
differently); it is recorded here as a data point, not as evidence for any reading.

Artifacts: `sparc_coherence.py`, `results.json`, `data/`, `figures/`. Seed fixed;
pre-registered bands in the script header.

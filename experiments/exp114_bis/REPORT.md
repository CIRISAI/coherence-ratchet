# Exp 114-bis Report

**Date:** 2026-05-18.
**Rig:** RTX 4090 Laptop GPU, NVIDIA driver 580.142, CUDA 13.0, CIRISArray Sentinel (cupy 13.6.0).
**Question:** Does the β = 1.09 critical-exponent claim from Exp 114 (January 2026) survive a properly-counted replication on the same substrate type, and is the power-law parameterization preferred over alternative functional forms?

## Method

Three runs:

1. **CPU OU coupled-array** (`run.py`). N=16 mean-field-coupled OU units; control parameter = coupling strength c. 50 c values × 30 trials × 4000 measurement steps.
2. **CPU coupled-Lorenz array** (`run_lorenz.py`). N=16 coupled Lorenz oscillators (σ=10, ρ=28, β=8/3, mean-field x-coupling); control parameter = integration timestep dt. 50 dt values × 30 trials × 2000 measurement steps.
3. **GPU rig** (`run_rig.py`). CIRISArray `Sentinel` (`use_lorenz=True`, default config) on RTX 4090; control parameter = `lorenz_dt`. 50 dt values × 30 trials × 100 samples (5 ms sample interval). Identical measurement chain to original Exp 114 except for the expanded sweep.

For each run: power-law fit `ρ = A|x − x_c|^β + C` with bootstrap CI on β; AIC comparison vs linear / exp / sigmoid; susceptibility exponent γ from log Var(ρ) vs log|x − x_c|.

## Result table

| Source | β | β 95% CI | x_c | R² | n_x × n_trials |
|---|---:|---|---:|---:|---|
| Exp 114 (2026-01) | 1.0921 | **not published** | 0.03279 | 0.978 | 9 × 5 |
| **Exp 114-bis rig** | **1.1529** | **[1.1462, 1.1595]** | **0.03315** | **0.9707** | **50 × 30** |
| CPU OU sim | 1.7211 | [0.58, 4.00] | n/a | 0.17 | 50 × 30 |
| CPU Lorenz sim | 4.0 (boundary) | [0.51, 4.00] | 0.0329 | −0.00 | 50 × 30 |

**Δβ rig-vs-original: +0.061** — the original 1.0921 sits **below** the 95% CI of the replication. The number has shifted as statistics improved and/or as the rig drifted (driver 580.142, CUDA 13.0 today; original was a different software stack).

## AIC across functional forms (rig data)

| Model | params | R² | AIC | ΔAIC vs best |
|---|---:|---:|---:|---:|
| Sigmoid | 4 | 0.9710 | **−382.00** | 0 (best) |
| Power law | 4 | 0.9707 | −381.36 | +0.64 |
| Exp | 3 | 0.9682 | −379.30 | +2.70 |
| Linear | 2 | 0.9635 | −374.40 | +7.60 |

**Sigmoid is marginally preferred over power-law (ΔAIC = 0.64) — statistically indistinguishable.** The framework's "critical exponent" interpretation is not preferred over a simple sigmoidal transition fit. Power-law is *one* functional form that fits the data; sigmoid fits the same data equally well with the same parameter count.

## Susceptibility γ (rig data)

`log Var(ρ) ~ −γ · log|dt − dt_c|` over 49 valid points:
- γ point: 0.2767
- R² of log fit: **0.306** ← terrible

A real second-order critical point would show clean γ-scaling with R² near 0.9+. The rig's variance scaling does NOT follow a power law in distance from criticality. The diverging-susceptibility signature, marked "? Noisy data" in original Exp 114, is confirmed absent here. **β-as-critical-exponent does not satisfy the textbook scaling-relation test.**

## Cross-substrate non-reproduction

Neither CPU simulation (OU array; coupled Lorenz array) reproduces β ≈ 1.15. The OU model gives flat ρ across the sweep; the Lorenz simulation produces sigmoidal data with power-law fit failing. **β = 1.15 is therefore a property of the CIRISArray-Sentinel-on-RTX-4090 measurement chain specifically, not a generic property of coupled chaotic-coordinator dynamics.**

## Verdict

1. **β reproduces on the rig**, with tight CI [1.146, 1.160]. The within-rig measurement is robust.
2. **β reproduces with a shifted value** (1.15 vs original 1.09); the original 1.09 is outside the replication CI.
3. **Power-law is not preferred over sigmoid** by AIC (ΔAIC = 0.64). The "critical exponent" framing is one parameterization among equivalent ones.
4. **No diverging susceptibility** — companion γ exponent has R² = 0.31, fails the second-order-transition test.
5. **CPU simulations do not reproduce β ≈ 1.15** — the number is substrate-specific.

## Recommendation for the paper

In `papers/main.md` §1 (engineering tier as cited existence proof), §10 (F-handles), and the abstract:

**Replace:** "β = 1.09 at R² = 0.978 in the framework's predicted critical regime; universality-class status pending Exp 5."

**With:** "The CIRISArray Sentinel on RTX 4090 with `lorenz_dt` swept across [0.018, 0.034] produces a sigmoidal transition in the lag-1 autocorrelation of k_eff(t); a 4-parameter power-law fit yields β = 1.153 ± 0.007 (95% CI bootstrap on 50 dt × 30 trials, Exp 114-bis 2026-05-18). The same data is fit equally well (ΔAIC = 0.64) by a 4-parameter sigmoid; the power-law parameterization is not statistically preferred. The companion susceptibility exponent γ fails the second-order-transition test (R² of log fit = 0.31). CPU simulations of natural candidate dynamics (OU coupled array; coupled Lorenz array) do not reproduce β ≈ 1.15. The framework therefore treats β as **a substrate-specific measurement of the corridor transition, not a universality class**; the universality-class language is retracted until either (a) a non-GPU substrate reproduces β with overlapping CI, OR (b) Conjecture A / Exp 5 quantum-substrate measurement lands a matching value."

This is the honest replacement. The framework's bet does not weaken — the corridor transition is real, the rig sees it consistently, the value's substrate-specificity is named. What retracts is the *universality* rhetoric.

## Files

- `run.py` — CPU OU coupled-array simulation, results in `results.json`
- `run_lorenz.py` — CPU coupled-Lorenz array simulation, results in `results_lorenz.json`
- `run_rig.py` — GPU rig replication, results in `results_rig.json`
- This report.

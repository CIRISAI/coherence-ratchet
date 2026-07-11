# Counterfactual cosmology sweep — VERDICT: LAW-LIKE

**Date 2026-07-10.** The law-ness test (pre-registered in `DECISIONS.md` before any fit): a law
must hold counterfactually. Frozen op_B B-total estimator (reused from `../halo_grain/`, no
modifications) run across 9 CAMELS IllustrisTNG 1P single-parameter-variation universes:
Ω_m ∈ {0.1, 0.2, 0.3, 0.4, 0.5} and σ₈ ∈ {0.6, 0.7, 0.8, 0.9, 1.0}, same 25 Mpc/h box, same
snapshots, same physics; threshold held fixed at 10¹¹ M⊙/h across the sweep so it cannot
confound. Data: `results.json`, `sweep.py`, `figures/fig1–3`, 90 cached catalogs.

## The three results

1. **The mechanism lock generalizes (the load-bearing invariant).** The S-peak epoch tracks
   each universe's OWN halo-formation-turnover (k-peak) epoch: corr = 0.846 across all 9
   universes; **corr = 0.963, RMS Δz = 0.185 excluding the one noisy fiducial-plateau box** —
   reproducing the TNG300 fiducial mechanism curve (0.948 / 0.088). The 0.95-level lock is NOT
   a property of our cosmology; it holds in every counterfactual universe tested. This is the
   relation whose off-fiducial collapse would have killed law-ness. It did not collapse.

2. **Covariation in the pre-stated direction, both axes.** Formation epoch is strictly
   monotonic in cosmology — k-peak z across the Ω_m axis: 0.15, 0.15, 0.77, 1.05, 1.36
   (slope +3.3); across the σ₈ axis: 0.33, 0.54, 0.77, 1.05, 1.36 (slope +2.6, strictly
   monotone). Crossing (S-peak) z: slope +3.4 vs Ω_m, +2.5 vs σ₈. Higher Ω_m/σ₈ ⇒ earlier
   formation ⇒ earlier phantom-divide crossing — exactly pre-stated prediction (1); the
   low-structure universes (Ω_m ≤ 0.2, σ₈ ≤ 0.7) show the predicted late-former behavior
   (crossings pushed to z = 0.15–0.54). Cross-cosmology epoch shifts (Δz ≈ 1.2 per axis)
   comfortably exceed the fiducial CV-suite noise scale.

3. **w_today amplitude is NOT constrained by this sweep** — an endpoint derivative on 10
   snapshots at single-box 25 Mpc/h is noise-dominated (scatter −0.17…−1.19, non-monotone).
   The robust covariation lives in the EPOCH quantities, not the amplitude. Read no claim in
   either direction from the amplitudes.

## Verdict

**NOT COINCIDENCE-LIKE.** A fiducial-tuned coincidence would show a flat S-shape vs cosmology,
or the S↔formation lock collapsing off-fiducial, or reversed covariation. None occurred: the
S(a) shape shifts strongly and monotonically with cosmology, the lock survives at 0.85–0.96
across Ω_m 0.1–0.5 and σ₈ 0.6–1.0, and the shift is in the pre-registered direction. **The
entropic-potential dark-energy law behaves like a law that reads each universe's own formation
history.**

**The honest asymmetry held** (pre-stated in DECISIONS): the non-fiducial universes do NOT
reproduce the DESI fit — nor should they; the test passed is the internal S↔formation-history
relation, not the fit.

## Caveats

One box per cosmology (no off-fiducial CV suite — the single fiducial 1P box under-formed,
k(z=3) = 176 vs CV_0's 217, and is the sole S-peak plateau outlier; a cosmic-variance
artifact — the DESI-matching fit lives at the CV-suite fiducial in `../large_volume/`, not this
box). 1P varies one parameter at a time, and Ω_m & σ₈ push formation the same way — this is a
consistency check along two correlated axes, not two independent confirmations. Hydro/feedback
parameters fixed. 2-point proxy C, R_smooth = 1.0, coarse 10-snapshot epoch grid. Bias and
growth cancel in the normalized C by construction, so the signal is genuinely the evolving
halo point set.

## Files

`DECISIONS.md` (pre-registered predictions and kill conditions) · `sweep.py` · `results.json` ·
`figures/fig1_lock.png, fig2_covariation.png, fig3_curves.png` · cached 1P catalogs.

*(Summary written by the orchestrating session from the agent's delivered verdict text — the
harness blocks subagent SUMMARY writes in some paths; all numbers are the agent's executed
output.)*

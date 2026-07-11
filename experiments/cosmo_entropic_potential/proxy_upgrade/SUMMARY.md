# Proxy upgrade — measured-C fails its own PSD gate (caveat stands); Abacus reachability proven, galaxy-host-scale cross-code test still open

**Date 2026-07-10.** Two-part upgrade attempt per `DECISIONS.md` (estimator conventions
pre-committed): (1) replace the model-ξ 2-point proxy with the measured correlation function;
(2) probe AbacusSummit as the non-TNG cross-code. Data: `results.json`,
`cpu_fallback_results.json`, `abacus_cpu_results.json`, `measured_tables.npz`.

## 1. Measured-C: the pre-staged estimator-failure gauge FIRED

The measured ξ̂(r) (periodic-analytic RR, 32 log bins, cubic spline on ln(1+ξ)) evaluated at
halo positions produces a **non-PSD C**: up to 1,600 non-positive eigenvalues per snapshot
(negative spectral mass to 2.6%), and after the op_B-style clip the resulting S is
**regularization-dominated** (clip-affected fraction 0.75–0.96) — the agent's own verdict,
matching DECISIONS' pre-stated failure criterion (>1% negative mass ⇒ estimator failure).

**Consequence, stated plainly: the 2-point-proxy caveat is NOT resolved.** The model-ξ
(PSD by construction — FT of a non-negative P(k)) remains the only valid estimator at this k.
The measured-route numbers (e.g. Δw₀ ≈ −0.25, Δwₐ ≈ +0.90 vs model) are floors contaminated by
regularization, not a measured proxy systematic — with one weak comfort worth recording: even
the contaminated variant moves the real-likelihood χ² by only **+0.27**, so the distance-level
result is insensitive to the estimator at the resolution this test achieved.

**The v2 route (named, not run):** fit a non-negative P(k) to the measured pair counts and FT
it — PSD by construction, measured content, no clip. That is the correct upgrade and it is
open work.

## 2. AbacusSummit: reachable, pipeline runs cross-code; the decisive scale is not yet testable

- **Reachability PROVEN** (the sweep's 2026-07-10 morning verdict is obsolete):
  `AbacusSummit_small_c000_ph3000` (500 Mpc/h, CompaSO halos) fetched anonymously within the
  disk budget; the frozen pipeline ran end-to-end on a second simulation code.
- **But the CPU-feasible configuration forced a cluster-scale threshold (2.1×10¹³ M⊙/h,
  cap 20,000, a = 0.37–0.83 only)** — deep in the zone where TNG300's own ladder shows no
  interior peak and phantom w (the K3 zone, boundary ~10¹³). The Abacus result there
  (peak z = 0.13, poor DESI fit) is **consistent with the known threshold-zone behavior on a
  different code**, and is NOT evidence about the galaxy-host-scale claim either way.
- **The real cross-code test needs the retention scale (~7×10¹¹), where the 500³ box holds
  ~550k halos — beyond exact-det reach.** Named route: the block-extensive tiling device
  (512× (25.6)³ tiles as in `large_volume/` CAMELS-continuity) or subvolume sampling. Open
  work, now unblocked on the data side.

## Verdict

Both halves land honestly short: the measured-C design fails its own gate (proxy caveat
stands, v2 route named), and the cross-code test is data-unblocked but scale-blocked (route
named). Nothing here changes the headline numbers; the 2-point-proxy asterisk stays on all of
them, as before.

*(DECISIONS, fetch, and runs by the proxy-upgrade agent; summary by the orchestrator from the
agent's executed output after it idled.)*

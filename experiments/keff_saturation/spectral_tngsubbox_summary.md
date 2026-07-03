# Fine-cadence baryon-cycle detailed-balance test on IllustrisTNG (TNG50-1-Subbox1)

**Substrate.** IllustrisTNG TNG50-1-Subbox0/1 fine-cadence subbox; TNG50-1-Subbox1, most massive galaxy by gas-mass peak -- GAS (PartType0)
Most massive galaxy by gas-density peak in the TNG50-1-Subbox1 fine-cadence subbox
(4 cMpc/h fixed comoving region, full TNG physics: cooling, star formation, winds, BHs).

**Cadence achieved.** T = 14 snapshots, mean dt = 33.9 Myr
(range 33.7-34.2), z = 0.032 -> 0.000,
cosmic-time span 0.44 Gyr. This is the point of the exercise: the earlier
CAMELS galaxy tests had only T=16 (time-underpowered); subbox fine cadence gives T>>16 at ~34 Myr.

**State construction (Eulerian, gas PartType0).** Eulerian disk-aligned 3D grid (+/-60 kpc/h, 8^3 cells) + 12 radial shells in the gas-density-tracked galaxy frame; cells x snapshots; scalars logrho / logT / v_r; region-overlapping chunks streamed per subbox snapshot (no whole-subbox download).
Cells x snapshots per scalar (NOT the trivial cells x few-properties table): a genuine
collective-mode decomposition. Grid = 8^3 disk-aligned cells within +/-50 kpc/h; plus 12 radial shells.

## Saturation (does the gas dynamics go low-rank / bounded k_eff?)
- logrho: PR/k_eff = 3.15, eff_rank(surrogate floor) = 1, MP eff_rank = 2 (N=438 cells, T=14)
- logT:   PR/k_eff = 1.81, eff_rank = 1
- v_r:    PR/k_eff = 1.90, eff_rank = 1

**SATURATION verdict: LOW-RANK.**

## Detailed balance (sustained cycle -> coordinating, vs reversible/transient -> bound)
Primary = direct (log rho, log T) CONFIGURATION-plane circulation vs phase-randomized null
(the baryon-cycle signature: inflow-cool -> feedback-heat -> outflow -> recycle is a directed loop):
- per-cell (logrho,logT):        mean_omega = -0.0046, z = -2.28 (438 cells)
- global mean-state (logrho,logT): omega = +0.0181, z = +0.07
- radial-shell mean-state:         omega = -0.1523, z = -0.64
- (logrho, v_r) [CONFOUNDED - position-velocity plane, reported not used]: z = -0.20

Primary config-plane |z| = 2.28. Auxiliary ep-winding |z| = 10.82.

**DETAILED-BALANCE verdict: MARGINAL configuration-plane circulation (2<|z|<3): weak/ambiguous sustained cycle at this T.**

## Honest caveats
- TNG gas has cooling+feedback BY CONSTRUCTION -> some irreversibility guaranteed; the question is a SUSTAINED homeostatic cycle (net circulation/loop) vs one-way depletion.
- star-forming gas sits on the TNG effective EOS -> the cold-dense branch of (rho,T) is model-imposed.
- one galaxy, one subbox region.
- sim-physics dissipation is NOT automatically the framework's gamma*M maintenance term.
- ep.entropy_production winding is AUXILIARY here: at T<=50 its block-bootstrap ruler does not cleanly separate cycle/driven/null, so the verdict rests on the (logrho,logT) circulation vs phase-randomized null (the direct baryon-cycle signature).
- TNG50-1-Subbox1 subboxes are re-decomposed every snapshot and have no group catalog, so the galaxy was located fresh each snapshot from the full subbox gas (no per-object cutout exists).

## Bottom line
With fine time resolution (T=14, dt~34 Myr, 0.4 Gyr span) the gas baryon cycle of this
one TNG50 galaxy is **LOW-RANK** in effective dimensionality, and the (log rho, log T)
configuration-plane circulation test says it is MARGINAL.
Sim gas has cooling+feedback by construction, so some irreversibility is guaranteed; the discriminating
question asked here is sustained homeostatic CYCLE (net circulation) vs one-way depletion, and simulation
dissipation is not automatically the framework's gamma*M maintenance term.

Artifacts: spectral_results_tngsubbox.json (full numbers), spectral_tngsubbox_summary.md (this file).

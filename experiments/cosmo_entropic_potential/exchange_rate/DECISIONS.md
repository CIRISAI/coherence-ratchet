# DECISIONS — first exchange-rate measurement

Choices made before/while computing, so the number is reproducible and the caveats are legible.
This is a **FIRST TOY MEASUREMENT**, not a law. Seed 20260710. Key read from `$TNG_KEY`
(sourced from `~/.tng_api_key`), never written to disk.

## What is being measured
The double-entry exchange rate
`X = <within-halo x-v coherence DESTROYED per formation event (DEBIT)> / <inter-halo coordination CREATED per halo formed (CREDIT)>`,
in nats/nats. Halo formation debits the constituent (phase-space) rung and credits the
unit (halo-grain) rung; X is the conversion factor between the two ledger entries.

## CREDIT side (data on disk, TNG300-1)
1. Source: `../large_volume/results.json`, `stage2_primary.records` — S(a), k(a) at the
   halo-mass threshold 7.4253e11 Msun/h. S_total = n(a)·s̄(a) is the extensive halo-grain
   entropy; k = number of halos above threshold.
2. Credit per halo = **dS_total/dk** across adjacent snapshots. Computed as finite differences
   ΔS/Δk on the **growing branch only** (z_hi < 1.75), which is the formation-epoch window
   relevant to the double-entry transaction.
3. **Excluded**: the cap-saturated snapshot (k = 38000 = the pipeline cap at a=0.647) and the
   late declining branch (k falls at low z as halos merge / drop below threshold — that is
   net *un*-formation, not a formation event).
4. Error bar: spread of dS/dk across the pairs, plus a jackknife SD from the stored
   `stage2_primary.jackknife` S(a) realisations.

## DEBIT side (particle data, TNG100-1 — better resolution than TNG300)
1. **Snapshots**: BEFORE = snap 50 (z=0.997, assembling/infall), AFTER = snap 67 (z=0.503,
   virialized). This brackets the formation-peak epoch z~0.5–1 the credit side is weighted to.
2. **Sample**: 18 halos. Selected as primary (central) subhalos at snap 67, `mass` 33–70
   (1e10 Msun/h), ordered by mass, keeping those with M200c(z=0.5) in 5e11–1.15e12 Msun and a
   valid main-progenitor at snap 50. Selection + progenitor tracking via the SubLink
   main-progenitor-branch tree (`subhalos/<id>/sublink/mpb.hdf5`), which carries Group_M_Crit200
   and the host GroupID (SubhaloGrNr) at every snapshot.
   - **Known selection skew** (documented, not hidden): `order_by=-mass` pulled the most massive
     centrals, so the sample sits at M200c(z=0.5) ≈ 1.0–1.1e12 Msun, ABOVE the 7.4e11 credit
     threshold; only 1 of 18 literally crosses 7e11 inside the z=1→0.5 window. Debit and credit
     are therefore NOT measured on identically mass-matched populations. See SUMMARY caveat 2.
3. **Grain**: reused verbatim from `experiments/dm_coherence/phasespace/phasespace_grain.py` —
   S = −ln det C, C = 6×6 correlation matrix of (x,y,z,vx,vy,vz), particles as samples.
4. **Same-material tracking** (the load-bearing choice). Comparing whole FOF groups at two
   epochs is confounded: the z=0.5 group is far larger and its infalling *envelope* dominates
   corr(x,v), which INVERTS the sign (measured: whole-group S rises 0.48→1.91). Instead I track
   a **fixed particle set**: the progenitor's DM ParticleIDs at z=1, intersected with the
   descendant's IDs at z=0.5 (~85% survive). S_before = copula on those particles at z=1;
   S_after = copula on the SAME particles at z=0.5. Debit = S_before − S_after. This isolates
   the virialization of a conserved material set from envelope growth.
5. **Centering**: each epoch's particles recentered on their own group median with periodic
   unwrapping (box L=75000 ckpc/h) before building C — without this, boundary wrap corrupts corr.
6. **Fixed N**: subsample to N=5000 per halo per epoch (S is grain/N-dependent). Same N across
   all halos and both epochs. N-sensitivity reported at N=2000.

## Honest gates (folded into SUMMARY)
- The two sides live on **different grains/matrices** (halo-grain S_total vs particle x-v copula);
  that a genuine conserved "exchange rate" relating them EXISTS is unestablished (flagged in
  `papers/notes/one_ledger_pressure_test.md` §5). X=0.85 is a ratio of two separately-measured
  nat-quantities, not a demonstrated conversion law.
- Progenitor at z=1 is already partly bound ⇒ S_before understates true cold-infall coherence ⇒
  the debit is a **lower bound**.
- Copula S is the pairwise/linear shadow; multi-stream folds are invisible (order-≥3 blind spot).
- Two different simulations (TNG300 credit, TNG100 debit); box/resolution mismatch.

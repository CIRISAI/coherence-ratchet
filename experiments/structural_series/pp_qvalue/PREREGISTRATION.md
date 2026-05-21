# Pre-registration — particle decay concentration at fixed Q-value

Date: 2026-05-21. Committed BEFORE results are computed.

## 1. Is this a coordinated rung in the framework's sense?

Stated plainly, before any test: **No.** A particle's set of decay channels is
not a "coordinated rung" in the framework's sense. The corridor claim (Pieces
2-3, Claim 1/Claim 4) attaches to substrates with *actively maintained or
sustained* dynamics — a non-trivial `gamma*M(t)` keeping `drho/dt` near zero
inside a band. Particle decay is the opposite: it is a one-shot quantum
transition governed by a fixed Hamiltonian (a coupling constant times a
phase-space factor times a matrix element). There is no maintenance work, no
attractor dynamics, no `drho/dt`. The branching-fraction distribution is a
static spectrum, not a coordinated population.

The corridor *preconditions* therefore **do not apply**. This test is honestly
framed as: "does the shape observable (Kish rho of the branching fractions)
show corridor structure ANYWAY — a tight interior band — once the two known
confounds are controlled?" A positive result would be a surprising coincidence
worth noting; the honest prior is null. E4 already returned a null on this rung
(rho spread [0.015, 0.78], median 0.33, std 0.21).

## 2. The two confounds and how they are controlled

E4 controlled **confound A — decay-table completeness**: a particle with many
tabulated channels has an inflated raw k_eff. Control: compute rho on a FIXED
count of top channels per particle. Retained here (N_FIX top channels).

This test additionally controls **confound B — kinematic phase-space
suppression**: a channel with small Q-value (energy release = parent mass minus
sum of daughter masses) is suppressed by phase space regardless of any
"dynamics," inflating rho toward rigidity. Two controls, both pre-registered:

- **B1 — Q-band restriction.** For each particle, keep only decay channels
  whose Q-value falls in a comparable band, defined per particle as a fraction
  of the parent mass: Q/M_parent in [0.05, 0.60]. Channels outside this band
  (near-threshold or near-full-mass) are dropped. Then compute rho on the
  top N_FIX of the survivors.
- **B2 — phase-space normalisation.** Divide each branching fraction by an
  approximate two/three-body phase-space volume factor evaluated at that
  channel's Q-value, renormalise, then compute rho. This removes the
  monotone phase-space envelope so rho reflects only the residual
  (matrix-element) concentration. Phase-space factor: for an n-body channel,
  use Q^((3n-5)/2) (the non-relativistic n-body phase-space scaling;
  2-body -> Q^0.5, 3-body -> Q^2). Approximate, stated as such.

Both B1 and B2 are reported. Confound A control (fixed N) is applied on top of
each.

## 3. Parameters, fixed now

- N_FIX = 5 top channels (E4 used 6; 5 chosen so the Q-band restriction, which
  removes channels, still leaves enough particles in the sample. If fewer than
  ~12 particles survive, N_FIX is relaxed to 4 and that is reported, not hidden.)
- Q-band for B1: Q/M_parent in [0.05, 0.60].
- Particle set: the E4 list, hadrons only (W, Z, H0 excluded — their decay
  products are heavy and the Q-value notion is dominated by daughter rest mass
  in a way that defeats the band; their exclusion is pre-registered, not
  post-hoc). Particles surviving with >= N_FIX in-band clean channels enter.
- Clean channel = exclusive, subdecay_level 0, not an upper limit, not an
  inclusive/"anything"/"X" mode, value > 0, all decay products mass-resolvable
  (neutrinos and photons treated as massless).

## 4. What counts as a corridor — the pre-registered bar

A corridor finding requires ALL of:

1. **Tight band.** std(rho) across the particle sample < 0.10. (The A3+
   corridor rho ~ 0.17-0.35 has full width ~0.18; a genuine attractor band
   sample should have std well inside that — < 0.10 is the bar. E4's std 0.21
   was explicitly NOT a corridor.)
2. **Off both poles.** median(rho) in [0.15, 0.45], and no more than 20% of
   particles with rho > 0.55 (rigidity) or rho < 0.10 (chaos).
3. **Confound-robust.** The tight band must hold under BOTH B1 and B2, not
   just one. If it holds under only one control, that is reported as a
   confound-dependent (i.e. not robust) result, NOT a corridor.

If any of (1)-(3) fails: **NULL** — no corridor at the particle-decay rung at
fixed Q-value. A null is the expected outcome and will be reported as a null.

A "narrower than E4 but still not < 0.10" outcome is a null with a note that
the kinematic confound explained part of E4's spread — reported honestly,
not upgraded to a corridor.

## 5. Pre-committed verdict logic

```
if std(rho_B1) < 0.10 and std(rho_B2) < 0.10
   and median in [0.15,0.45] for both
   and pole_fraction <= 0.20 for both:
       CORRIDOR
else:
       NULL  (with the numbers and which criterion failed)
```

Real PDG 2025 data only (`pdg` package, v0.2.2). No fabricated values. Any
particle that cannot be cleanly processed is dropped and counted, not faked.

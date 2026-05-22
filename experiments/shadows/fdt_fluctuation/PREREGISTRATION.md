# Shadow 1 — the fluctuation-dissipation shadow of γM — pre-registration

**Date:** 2026-05-22. Indirect readout of active maintenance γM, after the
direct unitary pointer (H_meas) failed (it cannot read a dissipative system
without collapsing it).

## The idea

The direct pointer failed because it coupled a conjugate momentum to a
dissipative α−γM system. The *indirect* route: a dissipative steady state held
open by active work γM has a noise signature. Fluctuation-dissipation links
spontaneous fluctuations to the dissipation doing the holding — so the system's
own "breathing" inside the corridor is a non-invasive readout of γM.

## The test

Substrate: the GPU (CIRISArray strain gauge) is primary — its corridor-exit
*dissipation* rate is already measured (1/τ ≈ 0.0214 s⁻¹). LLM internals
(attention-head / within-layer ρ over a generation runway) secondary.

Measure ρ as a time series in-corridor; compute its fluctuation power spectrum.
**Decisive test:** does an FDT-type relation link the fluctuation spectrum to
the *independently measured* corridor-exit relaxation rate? And does the
spectrum discriminate in-corridor from rigidity (mode-collapse) and chaos?

## Two-sided verdict

- **PASS:** the fluctuation spectrum carries γM — either the FDT relation to the
  measured relaxation rate holds quantitatively, or the spectrum sharply
  discriminates corridor from the two poles. A non-invasive γM readout exists.
- **NULL:** the spectrum does not discriminate / no FDT link holds.

## Discipline

CUDA where it applies (cupy). "The system shows 1/f noise" is **not** a result —
1/f is ubiquitous and non-diagnostic; the test is the *quantitative* FDT link to
the measured relaxation rate, or sharp pole-discrimination. FDT is an
equilibrium theorem; α−γM is a non-equilibrium open system — state honestly
whether the relation genuinely holds or is an analogy. Two-sided; NULL is valid.
Incremental output.

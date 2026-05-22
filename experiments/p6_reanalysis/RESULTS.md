# P6 re-analysis — three-regime corridor in public qubit decoherence-sweep data — results

**Date:** 2026-05-22. Weak-proxy test of P6 (Conjecture A / Exp 5), two-sided,
pre-registered at `PREREGISTRATION.md`. This is **not** Exp 5 (the decisive
new-qubit-array experiment); it is a re-analysis of already-published quantum-
hardware data, honestly labelled as a proxy.

## Verdict: **BLOCKED**

No suitable published empirical dataset was found. Per the pre-registration,
BLOCKED is the honest outcome when no control-parameter sweep + machine-readable
tomography/purity dataset exists. It is reported flat, as a valid result.

## What "suitable" requires

The pre-registration fixes the observable as k_eff = 1/Tr(ρ²) and the method as:
find a **published, empirical** quantum-hardware experiment in which a
decoherence or control parameter is swept and the **density matrix (or enough to
reconstruct purity) is measured**, then compute k_eff at each parameter value and
test for a bounded three-regime corridor. A qualifying dataset therefore needs
**numerical, machine-readable** reconstructed density matrices (or purity / Bloch
coordinates) at a series of swept-parameter values — not a figure, not a video,
not a process-matrix-only characterization.

## What was searched

Search was conducted via web search over arXiv, Nature/Science/PRX/PRA/PRR,
PMC, figshare, Zenodo, and GitHub, May 2026. Search axes: superconducting,
trapped-ion, and photonic substrates; state tomography and process tomography;
decoherence-rate / measurement-strength / noise-strength / time / circuit-depth
sweeps; published supplementary data, figshare/Zenodo datasets, and code repos.

### Candidate datasets examined and why each was rejected

1. **Almeida et al., "Environment-Induced Sudden Death of Entanglement,"
   Science 317, 579 (2007) — arXiv:quant-ph/0701184.**
   Genuine all-optical experiment. Decoherence parameter p = 1 − exp(−Γt) swept
   0 → 1; two-qubit state tomography performed; the paper reports **purity vs p**
   (its Fig. 3) and concurrence vs p. *Closest fit found.* Rejected: the paper
   presents purity only as a plotted figure — **no numerical table of density
   matrices or purity values** is published, and no data file accompanies it.
   Re-using it would require digitizing a figure, which injects pixel-estimation
   error and is not an honest re-analysis. Separately, the physics is adverse:
   under amplitude damping the joint state runs pure (entangled) → mixed → pure
   (product |HH⟩ at p=1), and under dephasing purity decays monotonically —
   neither trace is a rigidity → corridor → **chaos** structure (the chaos pole
   k_eff → 2ⁿ is never approached).

2. **Ficheux et al., "Dynamics of a qubit while simultaneously monitoring its
   relaxation and dephasing," Nat. Commun. 9, 1926 (2018) —
   arXiv:1711.01208, dataset 10.6084/m9.figshare.6127958.v1.**
   Genuine superconducting-qubit experiment with full single-qubit tomography
   (x,y,z Bloch components), sweeping Rabi frequency and dephasing rate.
   Rejected: the figshare "dataset" contains **only MP4 animation files** — no
   numerical Bloch-coordinate or density-matrix data. The experiment also
   measures *conditional* quantum trajectories, not an ensemble decoherence
   sweep with one reconstructed ρ per parameter value.

3. **Xu et al., "Experimental quantum process tomography of single-photon
   quantum channels with controllable decoherence" — arXiv:1108.1543.**
   Genuine photonic experiment; explicitly sweeps a decoherence parameter
   (crystal angle θ, waveplate angle φ, 0°→90°). Rejected: it reports **process
   (χ) matrices**, not state density matrices, and publishes only χ-eigenvalue
   plots — no numerical state ρ from which k_eff = 1/Tr(ρ²) can be computed, and
   no data table.

4. **"Qubit-State Purity Oscillations from Anisotropic Transverse Noise" —
   arXiv:2409.12303 (2024).**
   Genuine fluxonium experiment that directly measures qubit purity vs an
   injected-noise control parameter (noise duration, phase, anisotropy, bandwidth),
   with non-monotone purity (revivals). Rejected: purity is shown only as plots
   and 2D heatmaps — **no numerical purity table**, and the supplemental-data URL
   was an unfilled placeholder in the posted version. The non-monotonicity is
   coherent oscillation / quasi-static-noise revival, not a three-regime corridor
   in a monotone control parameter.

5. **Mirror randomized benchmarking on IBM Eagle/Heron processors —
   arXiv:2311.05933, arXiv:2112.09853.**
   Genuine hardware, circuit-depth sweep. Rejected: reports effective
   polarization / success probability decay, **not reconstructed density matrices
   or purity** — k_eff = 1/Tr(ρ²) is not recoverable.

6. **Ben Av et al., "Direct reconstruction of the quantum-master-equation
   dynamics of a trapped-ion qubit," PRA 101, 062305 (2020) — arXiv:2003.04678.**
   Genuine ⁸⁸Sr⁺ trapped-ion experiment. Rejected: reconstructs the Lindbladian
   *generator*, not a parameter sweep of measured density matrices with a public
   numerical table.

## Why nothing qualified — the honest assessment

Two distinct obstacles, both load-bearing for the BLOCKED verdict:

**(a) Data-availability.** Decoherence-sweep tomography experiments do exist and
are genuine empirical hardware work, but the community norm is to publish
reconstructed density matrices and purities **as figures**, not as machine-
readable tables or data files. Of every candidate examined, none provided
numerical ρ(parameter) or purity(parameter) data. A re-analysis cannot be built
on digitized figure pixels without violating the pre-registration's "real
published empirical data" and fixed-observable discipline; doing so would
manufacture false precision.

**(b) Structural.** Even granting a digitized dataset, standard single- and
two-qubit decoherence physics does not produce the P6 three-regime structure.
A control parameter swept from no-decoherence to full-decoherence takes a pure
state monotonically toward a mixed state: k_eff = 1/Tr(ρ²) rises monotonically
from the rigidity floor (≈1) toward the chaos ceiling (≈2ⁿ) — which the
pre-registration explicitly names as **NULL**. The non-monotone cases that do
appear (amplitude-damping sudden-death: pure → mixed → pure product; injected-
noise purity revivals: coherent oscillation) are rigidity → corridor → rigidity
or oscillatory, not rigidity → corridor → chaos. There is no standard
quantum-decoherence experiment in which a monotone control parameter yields a
bounded k_eff plateau pinned off both poles.

## Bottom line for P6

P6 finds **no weak-proxy support in public data — but it also is not refuted by
public data.** This re-analysis is genuinely at the edge of what already-
published quantum-hardware data can say: the qualifying observable
(machine-readable k_eff vs a swept control parameter) has not been published,
and the experiments that come closest have decoherence physics that, on
inspection, would read NULL rather than corridor. The pre-registered weak proxy
returns BLOCKED.

This leaves P6's evidential status exactly where the paper places it: the
decisive test is **Exp 5** — a new programmable-qubit-array experiment sweeping
decoherence rate γ with state tomography at each γ, designed so k_eff is
measured across the full sweep and a corridor (if any) would be visible.
Re-analysis of public data cannot stand in for that experiment. F-8 / F-13
remain open and untouched by this result.

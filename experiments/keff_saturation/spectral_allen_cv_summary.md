# Allen visual cortex -- cross-validated eigenspectrum verdict

> **NOTE (team-lead, SUPERSEDING the "LOW-RANK / rescue HOLDS" verdict below).**
> That verdict is a LEVEL-TRAP misread. It reads `noise_free_keff` ~4.8 (a k_eff
> LEVEL at fixed N) as corridor-occupation — but this same run's own power-law
> exponent **α median 0.97 (95% CI [0.88, 1.22], matching Stringer 2019 ~1.04)**
> is a scale-free spectrum whose participation ratio GROWS with N (β=0.83), i.e.
> NON-saturating. The corridor claim is about SATURATION, not level; participation
> ratio is a poor discriminator for a power law (variance concentrates in the top
> few modes, keeping PR modest, while the tail runs long and unbounded). CORRECT
> reading: a few dominant modes (low PR) over a NON-saturating scale-free tail
> (α≈1) = HIGH-dimensional, NOT low-rank. It is distinguishable from pure noise
> (α≈1 vs the noise null's α≈0), so it is genuine scale-free structure, not noise —
> and it remains a subsample at the WRONG GRAIN regardless (a subsample's k_eff is
> not the system's). The agent's one fair point survives: cortex k_eff (~5) sits
> BELOW the pure-noise null (~11), so there ARE dominant low-d modes — but "below
> noise at fixed N" is not "bounded/saturating." Authoritative record:
> `formal/CoherenceRatchet/Cosmology/CriticalityDiscriminator.lean`.

Decisive noise-removed test for the contradictory raw beta (0.84, noise-leaning) vs bounded spike count (median 5). Block-interleaved cross-validation (5-s blocks, so train/test do not share the GCaMP autocorrelation that breaks signed even/odd cvPCA on non-repeated data) with phase-randomized surrogate nulls.

Real Allen data, 21 sessions, N in [21, 240] (median 152).

- **(a) CV-positive intrinsic dims** (noise removed): median **50** (range 1-143). Cortex is NOT low-rank.
- **noise_free_keff** (PR of the CV-positive spectrum): median **4.8** (range 1.0-37.1, 95% CI [4.2, 11.6]). Framework ceiling ~10.
- **(b) dims above the strict surrogate ceiling** (cross-neuron coordination): median **0** (range 0-2). Lower bound (surrogates preserve each neuron's power spectrum).
- **power-law alpha** (lambda_i ~ i^-alpha): median **0.969**, 95% CI [0.876, 1.215]. Stringer mouse V1 ~ 1.04; match=True.
- **pure-noise null @ N=152** (calibration, synthetic): n_cv_pos=12, noise_free_keff=11.1, n_above_surr=0, alpha=0.022. Cortex readouts must clear this to count as structure beyond independent autocorrelation.

## VERDICT: LOW-RANK

noise-removed effective dimension at/under the ~10 ceiling (and not above the pure-noise null): the covariance-observable rescue HOLDS.

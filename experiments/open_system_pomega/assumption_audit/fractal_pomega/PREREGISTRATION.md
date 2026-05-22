# P_ω — the fractal / RG-nested construction — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.

## The error this corrects

The assumption audit declared F-11 fired after R1, R2, R3, and the R1∧R2
conjunction all horned. **That declaration was premature.** Every one of those
constructions used a **1D nearest-neighbour chain** for the cross-rung coupling.
The framework's rungs are not a chain — they are **RG coarse-grainings** (Piece 6
is RG nesting; the P_ω history built MERA isometry towers): rung n+1 is built
*from* rung n, so every higher rung contains the lower ones, and the coupling is
cross-scale — a fractal / hierarchical / all-to-all-across-scales structure.

The no-go's load-bearing law — ρ_joint ~ c/(count−1), the joint Kish
participation ratio diluting to the chaos pole — is **chain-specific**: it rests
on each constituent having O(1) correlated partners (the nearest-neighbour
property). A fractal coupling gives partners at every scale → a power-law
correlation spectrum → **sub-extensive** k_eff → ρ_joint need not dilute as
1/count. The audit never ran R4 (assumption 5, topology); the terminal F-11
condition was never validly met. F-11 is **not** fired.

## The construction

The R1∧R2 machinery — R1's non-additive joint Kish participation-ratio
functional, on R2's open sequential history-space frame — with the **one fix**:
the cross-rung coupling is the genuine **RG-nested / fractal** structure, not a
nearest-neighbour chain.

- The rung hierarchy is an RG/MERA tree: each rung a coarse-graining of the one
  below; the joint rung-correlation structure is **hierarchical / ultrametric**
  — rung n and rung n+k coupled through the nesting, coupling set by scale-
  distance k (a self-similar decay), not zero for k>1.
- This must be the framework's genuine RG nesting (Piece 6; the existing
  `construct_p_omega_mera.py` MERA tower is the reference), **not** a free-
  parameter power-law tuned to a verdict.

## Hypotheses

- **H2′ — no dilution under fractal coupling (the decisive one).** With the
  RG-nested coupling, the joint correlation spectrum is power-law and k_eff is
  sub-extensive, so ρ_joint stays bounded — off the chaos pole — to the
  framework's 9 rungs and beyond. This is the direct test of whether the
  ρ_joint ~ 1/count law was a chain artifact.
- **H1 — non-decomposability.** The non-additive functional on the fractal
  structure does not factorize (segment-shuffle gap real, growing with R).
- **H3 — joint work.** Non-empty, selective, genuinely coupling, well-defined
  to 9 rungs.

## Three-way verdict

- **OPENS:** H2′ ∧ H1 ∧ H3 — the fractal coupling holds ρ_joint bounded, the
  functional does not factorize, the joint object is non-empty and selective to
  9 rungs. P_ω is constructed on the framework's genuine rung topology.
- **EMPTY:** ρ_joint dilutes even under the genuine RG-nested coupling.
- **TRIVIAL:** the functional still factorizes.

## Terminal commitment (binding — and genuinely terminal)

This construction uses the framework's **actual** rung topology — RG-nested /
fractal. There is no more-faithful topology to test: fractal/RG-nesting is what
the framework's rung hierarchy *is*. So:

- **OPENS → P_ω is constructed**, F-11 does not fire, v2 records the construction.
- **EMPTY or TRIVIAL → F-11 fires for real** — the no-go now holds for the
  framework's genuine structure, not a chain artifact — v2's §sec:open-research
  records it. No further constructions: the framework's own topology has been
  tested.

## Discipline

CUDA mandatory (cupy). The build script must print per-depth progress, flush
interim results per depth, and resume from on-disk partials — verified before
the long run. Two-sided: EMPTY or TRIVIAL is a valid result. The RG-nested
coupling must be the framework's genuine structure (Piece 6 / the MERA tower),
not tuned. If the construction finds itself choosing the coupling to manufacture
a verdict, it stops and reports that.

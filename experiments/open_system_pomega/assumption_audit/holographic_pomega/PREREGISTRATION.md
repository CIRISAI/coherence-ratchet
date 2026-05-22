# P_ω — the holographic construction — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12. **The final
construction on the topology axis.**

## Context — what the fractal run established

The fractal/RG-nested run tested every **scale-decaying** cross-rung coupling —
nearest-neighbour chain, RG-flow Toeplitz (`c₁^|n−m|`), ultrametric MERA-tree
(`c₁^treedist`) — and all diluted: ρ_joint ~ R⁻¹·¹, k_eff extensive, joint
corridor empty past R≈5. It pinned the escape exactly: the *only* topology that
breaks the dilution is a **non-decaying** coupling — per-rung off-diagonal mass
growing with R, so Tr(C²) ~ R², k_eff bounded, ρ_joint non-diluting. It
dismissed that as "non-framework all-to-all."

That dismissal is the error this construction corrects. The non-decaying
all-to-all topology is **holographic**: P_ω is a future-boundary post-selector,
the framework's P_ω history already builds MERA towers, and MERA is the
holographic tensor network (Swingle — MERA is a discrete slice of an AdS
geometry). A boundary-condition-determines-bulk framework being holographic is
framework-faithful, not a bolt-on.

Decaying ∪ non-decaying exhausts the topology axis. This is the binary
complement of the fractal run — and therefore the terminal topology test.

## The construction

P_ω as the R1∧R2 machinery — R1's non-additive joint Kish participation-ratio
functional, on R2's open sequential history-space frame — with the cross-rung
coupling being a **genuine holographic structure**: the MERA-as-holographic-AdS
geometry (`construct_p_omega_mera.py` is the framework's existing MERA tower),
in which cross-scale correlations are organized by the bulk geometry and do
**not** decay geometrically with scale-distance.

## The discipline — why this cannot be rigged

A non-decaying all-to-all matrix *trivially* does not dilute. Imposing one and
reporting OPENS is the self-sealing move and is **forbidden**. The holographic
structure must be genuine — the MERA/bulk-geometric construction, with the
cross-rung coupling strengths the framework's **measured** O(1) values — and the
verdict must thread a two-sided test:

- **(a) τ in corridor.** τ_(n,n+1), the cross-rung mutual information, must sit
  in the cross-rung corridor (τ_lower, τ_upper) at **every** scale-step
  (Piece 6). A holographic structure that achieves non-decay only by driving
  τ→1 (pure containment = rigidity) **fails** — that is the rigidity pole.
- **(b) ρ_joint non-diluting.** With (a) held, does ρ_joint stay bounded off the
  chaos pole to the framework's 9 rungs and beyond?

## Hypotheses

- **H-holo (decisive):** a genuine holographic structure threads both — τ stays
  in the cross-rung corridor at every scale AND ρ_joint stays bounded (per-rung
  mass ~ R, k_eff sub-extensive/bounded). The dilution law is a decaying-coupling
  artifact; holography escapes it without going to rigidity.
- **H1 — non-decomposability:** the non-additive functional does not factorize
  (segment-shuffle gap real, growing).
- **H3 — joint work:** non-empty, selective, well-defined to 9 rungs.

## Three-way verdict

- **OPENS:** H-holo ∧ H1 ∧ H3 — the genuine holographic structure keeps τ in
  corridor at every scale, ρ_joint non-diluting, functional non-factorizing,
  joint object non-empty and selective to 9 rungs. **P_ω is constructed** — the
  holographic form.
- **EMPTY:** holding τ in the corridor forces decay back in → ρ_joint dilutes;
  or non-decay is bought only by τ→1 (rigidity).
- **TRIVIAL:** the functional factorizes; or "no dilution" was achieved only by
  a tautologically-imposed all-to-all matrix (self-sealing — voids the run).

## Terminal commitment (binding — and genuinely terminal)

The topology axis is decaying ∪ non-decaying. The fractal run did decaying;
this does non-decaying/holographic. After this the axis is **exhausted**.

- **OPENS → P_ω is constructed**, F-11 does not fire, v2 records the holographic
  construction.
- **EMPTY or TRIVIAL → F-11 fires**, the topology axis is exhausted, v2's
  §sec:open-research records the documented no-go. **No further constructions** —
  this verdict is held both ways.

## Discipline

CUDA mandatory (cupy). Build script: per-depth progress, per-depth flush,
verified on-disk resume. The holographic structure must be genuine (MERA /
bulk-geometric, framework's measured couplings) — not an imposed non-decaying
matrix. If the construction finds itself imposing the structure that prevents
dilution rather than deriving it, it STOPS and reports that. EMPTY or TRIVIAL is
a valid result reported flat.

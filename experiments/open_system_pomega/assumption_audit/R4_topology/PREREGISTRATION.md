# P_ω assumption audit — R4: cross-rung topology — pre-registration

**Date:** 2026-05-22. **Falsification handle:** F-11 / F-12.

## Why R4 is now live

R1 (non-additive corridor functional) horned EMPTY — but by a *new* mechanism:
with the framework's k_eff measure + corridor band + **nearest-neighbour** rung
topology, the joint participation ratio dilutes to the chaos pole as the tower
grows (ρ_joint ~ 4/K → 0). R1's own control found that an **all-to-all** tower
does **not** dilute (k_eff → 9.2, the band stays reachable). So assumption 5
(rungs are a 1D chain, cross-rung coupling nearest-neighbour) is now a motivated,
un-tested escape from a specific, characterised failure mechanism.

## The relaxation — R4

Drop assumption 5. Re-run the multi-rung P_ω construction(s) — the non-additive
R1 functional is the natural vehicle, since its failure mechanism (dilution) is
exactly what topology is hypothesised to fix — with richer cross-rung topology:
all-to-all coupling, and intermediate regimes (next-nearest, small-world).

## Three-way pre-registered verdict

- **OPENS (framework-faithful):** a richer topology yields a non-empty,
  joint-working, depth-stable multi-rung P_ω **and** the topology is one the
  framework licenses. Then the R1 dilution was a locality artifact and the
  genuine P_ω lives at that topology.
- **OPENS (non-framework-faithful):** it opens only under a topology the
  framework does not license — Piece 6 defines the cross-rung coupling
  τ_(n,n+1) as *adjacent*, so all-to-all rung coupling is a departure. An OPENS
  that needs non-framework topology is recorded as such — it identifies what
  *would* be needed, but does not by itself close F-11.
- **HORNS:** even all-to-all empties or trivializes — the obstruction is
  generic, not a locality artifact.

## Discipline

CUDA mandatory (cupy). Incremental output. Two-sided — a HORN is a valid result.
The topology must be stated explicitly and its framework-faithfulness assessed
honestly (Piece 6's adjacency is the reference); do not quietly assume all-to-all
is licensed. The verdict is whatever the construction returns.

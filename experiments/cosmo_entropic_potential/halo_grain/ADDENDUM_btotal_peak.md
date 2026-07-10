# Addendum (2026-07-10, orchestrator check): the B-total channel peaks — and lands on DESI

The parent SUMMARY.md classified the extensive B-total variant as "phantom, artifact"
based on its **global** slope (z=3→0 mean, +0.31, all six boxes rising). The pointwise
trajectory tells a different story, and it is the headline of this experiment, not a
footnote.

## The check (`btotal_multibox.py`, same `op_B` code path, all six boxes)

S_total(a) = −ln det C over the full evolving halo population (>10¹¹ M⊙/h, cap 1000):

| box | peak a (z) | S_end/S_peak | w_today |
|---|---|---|---|
| CV_0 | 0.564 (z=0.77) | 0.742 | −0.903 |
| CV_1 | 0.564 (z=0.77) | 0.786 | −0.865 |
| CV_2 | 0.564 (z=0.77) | 0.860 | −0.865 |
| CV_3 | 0.423 (z=1.36) | 0.864 | −0.792 |
| CV_4 | 0.751 (z=0.33) | 0.878 | −0.863 |
| CV_5 | 0.488 (z=1.05) | 0.625 | −0.757 |

**Interior peak: 6/6 boxes. w_today > −1: 6/6 boxes. Mean w_today = −0.841 ± 0.050.**
DESI DR2's w₀ = −0.838.

Under the sign law 1 + w = −(1/3)·d ln S/d ln a, the extensive halo-grain trajectory
gives, with no tuning: **w < −1 in the past (structure-building era), a single
crossing at the peak of above-threshold halo formation (median z ≈ 0.77, box scatter
0.33–1.36), and w > −1 today** — DESI's full qualitative structure, with today's
value landing on DESI's central w₀ to within the box-to-box scatter.

## Why this is not in conflict with the no-phantom theorem

The theorem (parent SUMMARY §5) governs a FIXED unit set under LOCAL transforms.
Halo formation is neither: new coordinating units condense out of the field through
gravitational interaction — exactly the "created only by interaction" channel the
theorem leaves open. The wrong assumption in the earlier no-phantom verdict is now
identified precisely: **fixed coordinating units**. The grain hypothesis was right,
but through unit-population evolution (formation-then-merger balance sets the peak),
not through the mergers-reduce-k premise as originally stated (which is false at
these thresholds — see parent SUMMARY).

## Why extensive-in-comoving-volume is the defensible convention here

ρ_DE is an energy **density**. The λ-maintenance note (§1.1) already adopts the
comoving-volume normalization; the coordination content *of a fixed comoving volume*
is then extensive in the units that volume contains. The intensive S/k convention was
inherited from the fixed-k cell grain, where unit count could not change and the
question never arose. When units form and die, the volume's total is the physical
object. (The parent SUMMARY's "bookkeeping" objection — that −ln det is monotone in
dimension — cuts against comparing *arbitrary* dimensions; here the dimension IS the
physical unit count of the same comoving volume at different times.)

## The mechanism, in one paragraph

Coordination content rises while structure forms (halo population grows, each new
unit correlated with the web), peaks when above-threshold formation is balanced by
merging (z ≈ 0.3–1.4 across boxes, median ≈ 0.8), and declines thereafter as mergers
absorb units. Under Λ-as-maintenance-cost this reads: dark energy behaves phantom
while the universe builds coordination, crosses −1 at peak structure formation, and
thaws as consolidation sets in — a mechanism-sketch for the coincidence problem
(dark energy "turns on" as structure formation winds down).

## Honest caveats (all inherited, plus new ones)

- **Small boxes.** 25 Mpc/h CAMELS CV suite; the crossing-epoch scatter (z 0.33–1.36)
  is cosmic variance. DESI's CPL crossing (~z 0.35) is inside the observed range but
  the median (0.77) is high. Needs a large-volume rerun (TNG300-class) before any
  epoch claim.
- **Magnitude is choice-dependent.** w_today = −0.841 moves with threshold (10¹¹),
  smoothing (R = 1 Mpc/h), and cap (1000). The 0.003 agreement with DESI's central
  w₀ is surely partly fortuitous; the robust claims are the SIGN structure and the
  ~−0.85 ± 0.05 scale. A threshold/R sensitivity sweep is the required next step.
- **Modeled C.** Correlations are model-ξ evaluated at real halo positions (PSD-safe),
  not measured halo-halo covariance. Inherits the parent's proxy disclaimer.
- **Convention is doing work.** A reader who insists on the intensive S/k reading
  recovers the parent's no-phantom verdict. The convention argument above is physical
  but not a theorem; it is now the single most consequential open modeling choice in
  the cosmology tier.
- The per-time vs per-e-fold clock ambiguity of the rate-form note does not arise
  here (this is the stock mapping on an evolving unit set), which makes this channel
  *cleaner* than the rate route to the same structure.

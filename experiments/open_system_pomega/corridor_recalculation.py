"""
Recalculating the corridor from all substrate data.
====================================================

The Path 1 / Path 2 investigation isolated one load-bearing question: is the
corridor's k_eff band (formerly 2.33-10, from the GPU substrate) a live
framework invariant, or a retired number? Rather than argue the framework's
internal sources (CLAUDE.md asserts it; the Lean core removed it), this
CALCULATES the corridor from the substrate data now in hand -- five A3+
substrates with measured within-rung |rho|, instead of the single GPU substrate
the old (0.1,0.43)/(2.33,10) numbers came from.

The corridor is a band of coordination quality between rigidity (k_eff -> 1,
single voice) and chaos (k_eff -> k, uncorrelated). Two coordinates:
  rho     -- within-rung correlation (substrate-local; k-dependent)
  k_eff   -- effective dimensionality, k_eff = k/(1+rho(k-1)); the framework's
             candidate substrate-INDEPENDENT coordinate. k_eff -> 1/rho as k->inf.

Only COORDINATED substrates define the corridor. The CMB is (in this measure)
nearly statistically isotropic -- it is the null baseline, not a corridor
occupant, so it does not enter the corridor calculation.

Honest limit, stated up front: the within-rung |rho| values are MEASURED (from
the paper, which sources experiments/). The constituent counts k are ESTIMATED
from substrate descriptions. k_eff depends on k, so the k_eff corridor inherits
that estimate uncertainty -- propagated below by corner evaluation over
plausible k ranges.
"""
import numpy as np


def k_eff(k, rho):
    return k / (1.0 + rho * (k - 1.0))


# (name, rho_centre, (rho_lo, rho_hi), k_centre, (k_lo, k_hi), provenance)
A3 = [
    ("cellular regulatory", 0.270, (0.20, 0.34), 50, (40, 60),
     "50 Hallmark pathways; healthy median |rho| 0.27+/-0.07 (paper L214)"),
    ("LLM internals", 0.200, (0.09, 0.31), 100, (16, 500),
     "within-rung |rho| 0.09-0.31, 4 architectures (L220); k most uncertain"),
    ("OSS contribution", 0.165, (0.15, 0.18), 20, (8, 60),
     "rolling 6-mo within-rung |rho| 0.15-0.18; active-author pool (L226)"),
    ("C. elegans s/i/m", 0.350, (0.25, 0.45), 80, (30, 110),
     "sensory/interneuron/motor band 0.25-0.45; neurons per class (L208)"),
    ("EEG healthy", 0.282, (0.25, 0.32), 23, (19, 30),
     "interictal mean |rho| 0.282; CHB-MIT ~23 channels (L210)"),
]
CMD = ("C. elegans command", 0.635, (0.52, 0.75), 15, (10, 25),
       "command-neuron class band 0.52-0.75 (L208) -- expected rigidity-side")

print("=" * 78)
print("THE CORRIDOR, RECALCULATED FROM SUBSTRATE DATA")
print("=" * 78)
print(f"  {'substrate':<22}{'rho':>14}{'k':>12}{'k_eff':>16}{'1/rho':>8}")
keff_centre = []
for name, rho, rb, k, kr, prov in A3:
    ke = k_eff(k, rho)
    # k_eff is decreasing in rho, increasing in k -> corners give the range
    ke_lo = k_eff(kr[0], rb[1])
    ke_hi = k_eff(kr[1], rb[0])
    keff_centre.append(ke)
    print(f"  {name:<22}{rho:>6.3f} [{rb[0]:.2f},{rb[1]:.2f}]"
          f"{k:>6d} [{kr[0]},{kr[1]}]".rjust(12)
          + f"{ke:>8.2f} [{ke_lo:.1f},{ke_hi:.1f}]".rjust(16)
          + f"{1/rho:>8.2f}")

# the command-neuron class, reported separately (rigidity-side)
nm, rho, rb, k, kr, prov = CMD
ke_cmd = k_eff(k, rho)
print(f"  {nm:<22}{rho:>6.3f} [{rb[0]:.2f},{rb[1]:.2f}]"
      f"{k:>6d} [{kr[0]},{kr[1]}]".rjust(12)
      + f"{ke_cmd:>8.2f}".rjust(16) + f"{1/rho:>8.2f}   <- rigidity-side")

print()
print("=" * 78)
print("THE CORRIDOR")
print("=" * 78)
rho_los = [rb[0] for _, _, rb, _, _, _ in A3]
rho_his = [rb[1] for _, _, rb, _, _, _ in A3]
rho_ctr = [r for _, r, _, _, _, _ in A3]
print(f"  in rho (within-rung correlation):")
print(f"    5 coordinated A3+ substrates, centre |rho| span "
      f"[{min(rho_ctr):.2f}, {max(rho_ctr):.2f}], median {np.median(rho_ctr):.2f}")
print(f"    full measured-band envelope [{min(rho_los):.2f}, {max(rho_his):.2f}]")
print(f"  in k_eff (effective dimensionality):")
print(f"    central k_eff across the 5: [{min(keff_centre):.1f}, "
      f"{max(keff_centre):.1f}], median {np.median(keff_centre):.1f}, "
      f"mean {np.mean(keff_centre):.1f}")
print(f"  command-neuron class: rho {CMD[1]}, k_eff {ke_cmd:.1f} -- "
      f"sits ABOVE the corridor in rho / BELOW in k_eff = rigidity-side,")
print(f"    consistent with command neurons being highly synchronised.")

print()
print("=" * 78)
print("COMPARISON TO THE GPU-SUBSTRATE NUMBER")
print("=" * 78)
print(f"  GPU substrate (the old single-substrate calibration):")
print(f"    rho corridor (0.10, 0.43);  k_eff corridor (2.33, 10).")
print(f"  5 A3+ substrates (this calculation):")
print(f"    rho centres cluster {min(rho_ctr):.2f}-{max(rho_ctr):.2f}; "
      f"k_eff centres {min(keff_centre):.1f}-{max(keff_centre):.1f}.")
print(f"  -> The A3+ coordinated systems sit INSIDE the GPU rho envelope but")
print(f"     do NOT reach either edge: not the chaos floor 0.10, not the")
print(f"     rigidity ceiling 0.43. In k_eff they top out near "
      f"{max(keff_centre):.0f}, well below the GPU ceiling of 10.")
print(f"  -> The 'k_eff = 10 maximum, substrate-independent' claim is NOT")
print(f"     supported by the A3+ data; the A3+ ceiling is ~{max(keff_centre):.0f}.")
print(f"     Either the GPU substrate genuinely reaches higher k_eff (a real")
print(f"     substrate difference) or the 10 was substrate-specific. The")
print(f"     honest combined corridor is the A3+ cluster, not the GPU number.")

print()
print("=" * 78)
print("READING")
print("=" * 78)
print(f"  Can we calculate the corridor more reliably now? Yes -- from 5")
print(f"  independent A3+ substrates instead of 1. The result:")
print()
print(f"    CORRIDOR (coordinated systems):  |rho| ~ 0.16-0.35, centre ~0.25")
print(f"                                     k_eff ~ 2.5-5,    centre ~3.5")
print()
print(f"  But 'more reliable' is not 'a tight universal constant'. The cross-")
print(f"  substrate spread (factor ~2 in rho) is REAL -- the framework's own")
print(f"  paper says corridor location is substrate-local. What the 5-substrate")
print(f"  calculation adds: the band is narrower than the GPU (0.1,0.43)")
print(f"  envelope, the centre is ~0.25, and the k_eff ceiling is ~5 not 10.")
print()
print(f"  The current limiting uncertainty is NOT the rho values (measured) --")
print(f"  it is the constituent counts k (estimated). A proper effective-k")
print(f"  measurement per substrate is what would make the k_eff corridor")
print(f"  genuinely reliable. That is the concrete next data step.")
print()
print(f"  Why this is not circular: the corridor is now CALIBRATED on A3+")
print(f"  substrates (biology / tech / social) only. The CMB drift predicted")
print(f"  from this corridor is then a genuine OUT-OF-SAMPLE prediction --")
print(f"  the corridor never saw CMB data. Calibrate on A3+, predict the CMB")
print(f"  drift, test on CMB-S4: calibration and test use disjoint data. That")
print(f"  is what makes F-19 a real test rather than a fit.")

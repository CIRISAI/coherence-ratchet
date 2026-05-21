"""
Corridor-centre calibration + real-CMB drift prediction.
========================================================

Path step 1 (pin rho_mid from A3+ data) and a real-data instance of step 3-4
(present-epoch rho_ell profile -> per-multipole drift direction), as far as is
doable in-environment. NOT a claim of a substrate-universal constant -- the
paper holds rho as substrate-LOCAL. This is the A3+ side of a two-way
convergence test: A3+ data gives a candidate rho_mid; cosmological consistency
is the other side; tight clustering would license a transfer, divergence is
the F-handle signal at the universal-scale tier.

PART 1 -- corridor centre from the five A3+ substrates (real measured values,
sourced from papers/Corridor Dynamics.tex, which sources experiments/).

PART 2 -- present-epoch rho_ell profile from a real CMB map. WMAP 9-yr ILC
map (nside 512; lambda.gsfc.nasa.gov). WMAP not Planck: at ell = 2..30 the CMB
is cosmic-variance-limited and WMAP/Planck agree to within noise -- the low-ell
anomalies were first characterised in WMAP. rho_ell is read off the Kish
identity from the power participation ratio over the 2ell+1 real harmonic
modes, exactly as the toy (cmb_drift_soft_pomega.py) defined it.

PART 3 -- the drift. For the actual single-realization universe the per-ell
drift under the sharpening soft-P_omega weight is the gradient
  d(rho_ell)/dbeta  =  -dH_sum/d(rho_ell)  =  2 (rho_mid - rho_ell),
so the SIGN at each multipole is sign(rho_mid - rho_ell(present)): a concrete,
real-data, per-multipole prediction once rho_mid is pinned.
"""
import os
import urllib.request
import numpy as np
import healpy as hp

# ===========================================================================
# PART 1 -- corridor centre rho_mid from the five A3+ substrates
# ===========================================================================
# (substrate, rung class, rho band low, high, provenance line in the paper)
SUBSTRATES = [
    ("cellular regulatory", "Hallmark pathways", 0.20, 0.34,
     "healthy median |rho| = 0.27 +/- 0.07 (Corridor Dynamics.tex L214)"),
    ("LLM internals", "depth x prompt cells", 0.09, 0.31,
     "within-rung |rho| band, 4 architectures (L220)"),
    ("OSS contribution", "stable-population rungs", 0.15, 0.18,
     "rolling 6-month within-rung |rho| (L226)"),
    ("neural / C. elegans", "sensory-interneuron-motor", 0.25, 0.45,
     "cross-lab band, 10/11 studies (L208)"),
    ("neural / EEG", "healthy interictal", 0.282, 0.282,
     "mean |rho| = 0.282, CHB-MIT 1322 windows (L210)"),
    ("neural / C. elegans", "command", 0.52, 0.75,
     "cross-lab band, 10/11 studies (L208) -- high-rho functional class"),
    # social groups: corridor membership by AM-checklist, no within-rung rho
]

print("=" * 78)
print("PART 1 -- corridor centre rho_mid from A3+ substrates (real measured)")
print("=" * 78)
print(f"  {'substrate':<22}{'rung class':<26}{'rho band':>12}{'centre':>9}")
centres = []
for name, cls, lo, hi, prov in SUBSTRATES:
    c = 0.5 * (lo + hi)
    centres.append((name, cls, c, lo, hi))
    print(f"  {name:<22}{cls:<26}{f'{lo:.2f}-{hi:.2f}':>12}{c:>9.3f}")
print("  social groups: corridor membership scored by AM-checklist (AM=0/5),")
print("    no within-rung rho reported -- excluded from the numeric aggregate.")

low_cluster = [c for (_, cls, c, _, _) in centres if cls != "command"]
allc = [c for (_, _, c, _, _) in centres]
cmd = [c for (_, cls, c, _, _) in centres if cls == "command"]
rho_mid = float(np.median(low_cluster))
print()
print(f"  low cluster (5 rung classes): centres = "
      f"{sorted(round(c,3) for c in low_cluster)}")
print(f"    median = {np.median(low_cluster):.3f}, mean = {np.mean(low_cluster):.3f}, "
      f"range = [{min(low_cluster):.3f}, {max(low_cluster):.3f}]")
print(f"  high outlier: C. elegans command-neuron class, centre {cmd[0]:.3f}")
print(f"    -- the paper holds rho substrate-LOCAL; the command class diverges,")
print(f"    a documented divergence, not folded into the estimate.")
print()
print(f"  ==> rho_mid estimate (A3+ side) = {rho_mid:.2f}, band ~ "
      f"[{min(low_cluster):.2f}, {max(low_cluster):.2f}]")
RHO_MID = rho_mid
RHO_MID_BAND = (min(low_cluster), max(low_cluster))

# ===========================================================================
# PART 2 -- present-epoch rho_ell from the real WMAP ILC CMB map
# ===========================================================================
print()
print("=" * 78)
print("PART 2 -- present-epoch rho_ell profile from the WMAP 9-yr ILC map")
print("=" * 78)
LMAX = 32
ELLS = list(range(2, 31))
MAP_PATH = "cmb_data/wmap_ilc_9yr_v5.fits"
MAP_URL = "https://lambda.gsfc.nasa.gov/data/map/dr5/dfp/ilc/wmap_ilc_9yr_v5.fits"
if not os.path.exists(MAP_PATH):
    os.makedirs("cmb_data", exist_ok=True)
    print(f"  downloading WMAP 9-yr ILC map from lambda.gsfc.nasa.gov ...")
    urllib.request.urlretrieve(MAP_URL, MAP_PATH)
cmb = hp.read_map(MAP_PATH)
cmb = hp.remove_dipole(cmb)                          # drop monopole + dipole
alm = hp.map2alm(cmb, lmax=LMAX)
print(f"  map nside {hp.get_nside(cmb)}; alm computed to lmax {LMAX}; "
      f"ell = 2..30")


def rho_ell(alm, lmax, ell):
    """Kish rho_ell from the 2ell+1 real-harmonic-mode power participation."""
    p = [abs(alm[hp.Alm.getidx(lmax, ell, 0)].real) ** 2]      # m = 0
    for mm in range(1, ell + 1):
        a = alm[hp.Alm.getidx(lmax, ell, mm)]
        p += [2.0 * a.real ** 2, 2.0 * a.imag ** 2]            # +/- m real modes
    p = np.array(p)
    k = 2 * ell + 1
    k_eff = p.sum() ** 2 / (p ** 2).sum()
    return (k / k_eff - 1.0) / (k - 1.0)


rho_gal = {ell: rho_ell(alm, LMAX, ell) for ell in ELLS}

# rotation-averaged rho_ell -- the frame-invariant version (galactic-frame
# rho_ell is frame-dependent; rotating the sky redistributes power among m)
rng = np.random.default_rng(20260521)
N_ROT = 200
rho_rot = {ell: [] for ell in ELLS}
for _ in range(N_ROT):
    a2 = alm.copy()
    hp.rotate_alm(a2, rng.uniform(0, 2 * np.pi), rng.uniform(0, np.pi),
                  rng.uniform(0, 2 * np.pi))
    for ell in ELLS:
        rho_rot[ell].append(rho_ell(a2, LMAX, ell))
rho_rot_mean = {ell: float(np.mean(rho_rot[ell])) for ell in ELLS}
rho_rot_std = {ell: float(np.std(rho_rot[ell])) for ell in ELLS}

# isotropic-Gaussian baseline (standard cosmology): <rho_ell>_iso by Monte Carlo
N_MC = 200_000
rho_iso = {}
for ell in ELLS:
    a = rng.standard_normal((N_MC, 2 * ell + 1))
    p = a * a
    k_eff = p.sum(1) ** 2 / (p * p).sum(1)
    rho_iso[ell] = float(np.mean((( 2 * ell + 1) / k_eff - 1) / (2 * ell)))

print(f"  {'ell':>4}{'rho(galactic)':>15}{'rho(rot-avg)':>14}{'rho_iso':>10}"
      f"{'rot-avg vs iso':>16}")
for ell in ELLS:
    excess = rho_rot_mean[ell] - rho_iso[ell]
    tag = "anomalous+" if excess > 2 * rho_rot_std[ell] / np.sqrt(N_ROT) else ""
    print(f"  {ell:>4}{rho_gal[ell]:>15.4f}{rho_rot_mean[ell]:>14.4f}"
          f"{rho_iso[ell]:>10.4f}{excess:>+16.4f} {tag}")

# ===========================================================================
# PART 3 -- the per-multipole drift prediction
# ===========================================================================
print()
print("=" * 78)
print("PART 3 -- drift  d(rho_ell)/dbeta = 2 (rho_mid - rho_ell):  crossover")
print("=" * 78)
print("  rho_ell(present) falls monotonically with ell (0.29 at ell=2 to ~0.03")
print("  at ell=30 -- set by the mode count k = 2ell+1). So the drift profile")
print("  has a single CROSSOVER multipole ell*: below ell* multipoles sit above")
print("  the corridor centre and drift toward isotropy; above ell* they sit")
print("  below it and drift toward concentration. ell* is set by rho_mid.")
print()
print(f"  {'rho_mid':>9}{'crossover ell*':>16}   drift structure")
for rm in [0.16, 0.20, 0.27, 0.35]:
    above = [ell for ell in ELLS if rho_rot_mean[ell] >= rm]
    ellstar = (max(above) + 1) if above else 2
    tag = "  <- A3+ low-cluster median" if abs(rm - 0.27) < 1e-9 else ""
    print(f"  {rm:>9.2f}{ellstar:>16d}   ell<{ellstar}: de-concentrate; "
          f"ell>={ellstar}: concentrate{tag}")
print()
print("  low-ell detail (rotation-averaged, frame-invariant rho_ell):")
print(f"  {'ell':>4}{'rho_ell':>10}{'rho_iso':>10}{'excess':>10}   note")
for ell in range(2, 11):
    ex = rho_rot_mean[ell] - rho_iso[ell]
    note = ("octupole -- real concentration excess" if ell == 3 and ex > 0.02
            else "consistent with isotropic" if abs(ex) < 0.015 else "")
    print(f"  {ell:>4}{rho_rot_mean[ell]:>10.4f}{rho_iso[ell]:>10.4f}"
          f"{ex:>+10.4f}   {note}")

print()
print("=" * 78)
print("READING -- result, and an honest divergence")
print("=" * 78)
print(f"  THE RESULT. The soft-P_omega CMB drift is computed from real data:")
print(f"  WMAP low-ell rho_ell + the A3+ corridor calibration. Its framework-")
print(f"  distinctive content is a SIGNED drift profile with a single crossover")
print(f"  multipole ell* -- low multipoles de-concentrate, high multipoles")
print(f"  concentrate. Standard cosmology and anthropic conditioning both")
print(f"  predict a flat zero; neither has a crossover. The structure is real")
print(f"  and computable; this is the universal-scale tier made empirically")
print(f"  testable in the same shape as the A3+ tier.")
print()
print(f"  THE DIVERGENCE (honest). A SINGLE A3+ rho_mid does not transfer")
print(f"  cleanly to the CMB. The A3+ low-cluster centre ~0.27 sits at the very")
print(f"  TOP of the CMB rho_ell profile (which runs 0.29 -> 0.03, set by the")
print(f"  per-multipole mode count) -- so at rho_mid=0.27 the crossover is")
print(f"  ell*~2-3 and almost the whole spectrum drifts one way. This is the")
print(f"  two-way-convergence test returning a DIVERGENCE at the cosmological")
print(f"  substrate: the A3+ side and the cosmological side do not pin the same")
print(f"  number. It is real empirical traction, consistent with the paper's")
print(f"  open cross-substrate consistency-of-bounds question -- not a free pass")
print(f"  and not a refutation. It does NOT touch F-11: P_omega is constructed.")
print()
print(f"  WHY A SINGLE rho_mid IS THE WRONG MODEL. The framework's own P_omega")
print(f"  definition carries PER-RUNG bounds (rho_lower,n .. rho_upper,n). The")
print(f"  CMB rung index is ell, and the natural rho scale is ell-dependent")
print(f"  (mode count). The correct object is a per-ell corridor calibration --")
print(f"  the cosmological-consistency side of the two-way test, and open work.")
print()
print(f"  WHAT THE REAL DATA ADDED. The WMAP low-ell profile is close to the")
print(f"  isotropic-Gaussian baseline (the CMB is nearly statistically isotropic")
print(f"  in this measure); the cleanest real departure is the OCTUPOLE (ell=3),")
print(f"  rotation-averaged concentration +0.033 above isotropic -- the octupole")
print(f"  is independently a famously anomalous multipole, and the Kish-rho")
print(f"  measure picks it up. To a falsifiable forecast still owed: per-ell")
print(f"  corridor calibration, Planck cross-check, a mask, and dbeta/dt.")

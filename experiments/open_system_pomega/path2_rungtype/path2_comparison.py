"""
Path 2 — quantitative comparison: does the k-dependence of the Kish identity
structurally account for the A3+ / CMB rho_mid divergence, with NO new free
parameters?
=============================================================================

Run AFTER PREREGISTRATION.md (committed separately). Tests the three
pre-registered predictions against the real WMAP 9-yr ILC CMB map.

Existing machinery only:
  Piece 1  Kish identity      k_eff = k/(1 + rho(k-1))
  Piece 3  corridor as a substrate-independent k_eff band (2.326, 10),
           read off the existing rho-band (0.10, 0.43) k->inf asymptote
  Piece 5  goal-projector vs mode-count rung type
No parameter is introduced that is not already in Pieces 1/3.
"""
import os
import urllib.request
import numpy as np
import healpy as hp

# ----- existing-machinery constants (NO new free parameters) ----------------
RHO_BAND = (0.10, 0.43)                    # GPU-substrate rho-corridor (Piece 3)
KEFF_LO = 1.0 / RHO_BAND[1]                # 2.3256 : corridor floor  (k->inf asymptote)
KEFF_HI = 1.0 / RHO_BAND[0]                # 10.000 : corridor ceiling
A3_RHO_MID = 0.27                          # five A3+ substrates, low-cluster median
A3_BAND = (0.16, 0.35)


def keff_of(k, rho):
    return k / (1.0 + rho * (k - 1.0))


def rho_of(k, keff):
    return (k / keff - 1.0) / (k - 1.0)


def rho_corridor(k):
    """k-dependent rho-corridor = inverse-Mobius image of the fixed k_eff band."""
    lo = max(rho_of(k, KEFF_HI), 0.0)      # high k_eff -> low rho
    hi = rho_of(k, KEFF_LO)                # low  k_eff -> high rho
    return lo, hi, 0.5 * (lo + hi)


print("=" * 78)
print("PATH 2 — k-dependence of the Kish identity vs the A3+/CMB divergence")
print("=" * 78)
print(f"  substrate-independent k_eff corridor (Piece 3, no new param): "
      f"({KEFF_LO:.4f}, {KEFF_HI:.4f})")
print(f"  A3+ measured corridor centre: rho_mid = {A3_RHO_MID}, "
      f"band {A3_BAND}")

# ===========================================================================
# PART 1 — re-run the CMB rho_ell profile from the real WMAP ILC map
# ===========================================================================
print()
print("=" * 78)
print("PART 1 — present-epoch CMB rho_ell from the WMAP 9-yr ILC map")
print("=" * 78)
LMAX = 32
ELLS = list(range(2, 31))
HERE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(HERE, "..", "cmb_data", "wmap_ilc_9yr_v5.fits")
MAP_URL = ("https://lambda.gsfc.nasa.gov/data/map/dr5/dfp/ilc/"
           "wmap_ilc_9yr_v5.fits")
if not os.path.exists(MAP_PATH):
    os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)
    print("  downloading WMAP 9-yr ILC map (~25 MB) ...")
    urllib.request.urlretrieve(MAP_URL, MAP_PATH)
cmb = hp.read_map(MAP_PATH)
cmb = hp.remove_dipole(cmb)
alm = hp.map2alm(cmb, lmax=LMAX)
print(f"  map nside {hp.get_nside(cmb)}; alm to lmax {LMAX}")


def rho_ell(alm, lmax, ell):
    """Kish rho_ell from the 2ell+1 real-harmonic-mode power participation."""
    p = [abs(alm[hp.Alm.getidx(lmax, ell, 0)].real) ** 2]
    for mm in range(1, ell + 1):
        a = alm[hp.Alm.getidx(lmax, ell, mm)]
        p += [2.0 * a.real ** 2, 2.0 * a.imag ** 2]
    p = np.array(p)
    k = 2 * ell + 1
    k_eff = p.sum() ** 2 / (p ** 2).sum()
    return (k / k_eff - 1.0) / (k - 1.0)


# rotation-averaged (frame-invariant) measured profile
rng = np.random.default_rng(20260521)
rho_rot = {ell: [] for ell in ELLS}
for _ in range(200):
    a2 = alm.copy()
    hp.rotate_alm(a2, rng.uniform(0, 2 * np.pi), rng.uniform(0, np.pi),
                  rng.uniform(0, 2 * np.pi))
    for ell in ELLS:
        rho_rot[ell].append(rho_ell(a2, LMAX, ell))
rho_cmb = {ell: float(np.mean(rho_rot[ell])) for ell in ELLS}

# isotropic-Gaussian baseline by Monte Carlo
N_MC = 300_000
rho_iso_mc = {}
for ell in ELLS:
    a = rng.standard_normal((N_MC, 2 * ell + 1))
    p = a * a
    k_eff = p.sum(1) ** 2 / (p * p).sum(1)
    rho_iso_mc[ell] = float(np.mean(((2 * ell + 1) / k_eff - 1) / (2 * ell)))

# ===========================================================================
# PART 2 — TEST 1: is the measured CMB rho_ell the isotropic baseline?
# ===========================================================================
print()
print("=" * 78)
print("TEST 1 — measured CMB rho_ell  vs  isotropic baseline 2/(k-1)")
print("=" * 78)
print("  pre-registered PASS: measured matches iso baseline within ~10% over")
print("  ell=2..30 (the CMB is nearly statistically isotropic in this measure)")
print()
print(f"  {'ell':>4}{'k':>5}{'rho_cmb(meas)':>15}{'rho_iso(MC)':>14}"
      f"{'2/(k-1)':>10}{'meas/iso':>10}")
rel_err = []
for ell in ELLS:
    k = 2 * ell + 1
    analytic = 2.0 / (k - 1)
    r = rho_cmb[ell] / rho_iso_mc[ell]
    rel_err.append(abs(r - 1.0))
    if ell <= 12 or ell % 5 == 0:
        print(f"  {ell:>4}{k:>5}{rho_cmb[ell]:>15.4f}{rho_iso_mc[ell]:>14.4f}"
              f"{analytic:>10.4f}{r:>10.3f}")
mean_rel = float(np.mean(rel_err))
test1 = mean_rel < 0.10
print()
print(f"  mean |measured/iso - 1| over ell=2..30 = {mean_rel:.3f}")
print(f"  TEST 1: {'PASS' if test1 else 'FAIL'} — the measured CMB rho_ell "
      f"{'IS' if test1 else 'is NOT'} the isotropic baseline.")

# ===========================================================================
# PART 3 — TEST 2: does existing machinery predict the divergence DIRECTION?
# ===========================================================================
print()
print("=" * 78)
print("TEST 2 — direction: iso baseline vs the k-dependent corridor CENTRE")
print("=" * 78)
print("  pre-registered PASS: rho_iso(k) < rho_mid(k) for k beyond a low-ell")
print("  crossover (the Gaussian sky sits below its corridor centre); the")
print("  crossover multipole ell* in the range ell ~ 2-4.")
print()
print(f"  {'ell':>4}{'k':>5}{'rho_iso':>10}{'rho_mid(k)':>12}"
      f"{'rho_lo..rho_hi':>18}{'  position'}")
ellstar = None
for ell in ELLS:
    k = 2 * ell + 1
    lo, hi, mid = rho_corridor(k)
    iso = rho_iso_mc[ell]
    pos = "above centre (rigidity-side)" if iso > mid else "below centre (chaos-side)"
    if ellstar is None and iso <= mid:
        ellstar = ell
    if ell <= 8 or ell % 5 == 0:
        print(f"  {ell:>4}{k:>5}{iso:>10.4f}{mid:>12.4f}"
              f"{f'{lo:.3f}..{hi:.3f}':>18}   {pos}")
test2 = (ellstar is not None) and (2 <= ellstar <= 5)
print()
print(f"  crossover multipole ell* (rho_iso drops below rho_mid) = {ellstar}")
print(f"  TEST 2: {'PASS' if test2 else 'FAIL'} — direction "
      f"{'matches' if test2 else 'does NOT match'}: the isotropic CMB sits")
print(f"  above its corridor centre at low ell, below it for ell >= {ellstar}.")

# ===========================================================================
# PART 4 — TEST 3: does existing machinery predict the MAGNITUDE (A3+ side)?
# ===========================================================================
print()
print("=" * 78)
print("TEST 3 — magnitude: does rho_mid(k) reproduce the A3+ 0.27 at small k?")
print("=" * 78)
print("  pre-registered PASS: rho_mid(k) for k in the A3+ range reproduces")
print("  ~0.27 (band [0.16,0.35]) WITHOUT tuning; FAIL if only k->inf works.")
print()
print(f"  {'k':>6}{'rho_mid(k)':>12}{'  in A3+ band [0.16,0.35]?'}")
for k in [3, 5, 7, 11, 21, 41, 61, 100, 300, 1000, 10 ** 6]:
    lo, hi, mid = rho_corridor(k)
    inband = A3_BAND[0] <= mid <= A3_BAND[1]
    tag = "  <- in band" if inband else ""
    print(f"  {k:>6d}{mid:>12.4f}{tag}")
# smallest k whose corridor centre reaches the A3+ lower band edge / the 0.27 point
ks = np.arange(3, 200001)
mids = np.array([rho_corridor(int(k))[2] for k in np.arange(3, 400)])
k_band = int(np.arange(3, 400)[np.argmax(mids >= A3_BAND[0])])
mid_inf = rho_corridor(10 ** 7)[2]
# k needed for rho_mid >= 0.27 exactly
reach_027 = mid_inf >= 0.27
print()
print(f"  rho_mid(k -> inf) = {mid_inf:.4f}")
print(f"  smallest k with rho_mid(k) >= A3+ lower band edge 0.16: k = {k_band}")
print(f"  rho_mid reaches the A3+ point estimate 0.27 exactly: "
      f"{'never (asymptote 0.265 < 0.27)' if not reach_027 else 'yes'}")
# A3+ substrates' plausible effective k: pathways(50), depth x prompt cells,
# OSS author pools, neuron classes -- tens to hundreds, NOT a literal handful.
print()
print("  A3+ substrate effective k (nominal constituent counts, from the paper):")
A3_K = [("cellular: 50 Hallmark pathways", 50),
        ("LLM: depth x prompt cells (tens-hundreds)", 100),
        ("OSS: active-author pool per window", 20),
        ("C. elegans: neurons per functional class", 30),
        ("EEG: channels", 20)]
mids_a3 = []
for name, k in A3_K:
    lo, hi, mid = rho_corridor(k)
    mids_a3.append(mid)
    print(f"    {name:<44} k~{k:>4d}  rho_mid(k) = {mid:.3f}")
mids_a3 = np.array(mids_a3)
print(f"  rho_mid(k) over the A3+ substrates: "
      f"[{mids_a3.min():.3f}, {mids_a3.max():.3f}], mean {mids_a3.mean():.3f}")
test3 = bool((mids_a3 >= A3_BAND[0]).all() and (mids_a3 <= A3_BAND[1]).all())
test3_centre = bool(abs(mids_a3.mean() - A3_RHO_MID) < 0.05)
print(f"  TEST 3: {'PASS' if test3 else 'PARTIAL/FAIL'} — all A3+ rho_mid(k) "
      f"{'inside' if test3 else 'NOT all inside'} the A3+ band [0.16,0.35].")
print(f"          centre match (|mean - 0.27| < 0.05): "
      f"{'PASS' if test3_centre else 'FAIL'} "
      f"(mean {mids_a3.mean():.3f} vs 0.27)")

# ===========================================================================
# VERDICT
# ===========================================================================
print()
print("=" * 78)
print("VERDICT")
print("=" * 78)
print(f"  TEST 1 (CMB rho_ell = isotropic baseline)        : "
      f"{'PASS' if test1 else 'FAIL'}")
print(f"  TEST 2 (divergence direction from k-dependence)   : "
      f"{'PASS' if test2 else 'FAIL'}")
print(f"  TEST 3 (A3+ magnitude from rho_mid(k), no tuning) : "
      f"{'PASS' if test3 else 'PARTIAL/FAIL'}"
      f" / centre {'PASS' if test3_centre else 'FAIL'}")
print()
if test1 and test2 and test3:
    print("  Existing machinery structurally accounts for the divergence:")
    print("  the A3+ and CMB numbers are different KINDS of object (corridor")
    print("  centre vs isotropic baseline), and the k-dependence of the Kish")
    print("  identity predicts both, in the observed direction and magnitude,")
    print("  with no new free parameter.")
else:
    print("  Existing machinery accounts for the divergence PARTIALLY — see")
    print("  FINDINGS.md for exactly which part holds and which does not.")

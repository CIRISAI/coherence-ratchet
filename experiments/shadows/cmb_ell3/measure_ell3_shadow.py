"""
Shadow 3 -- the ell=3 inflection shadow in the CMB.
====================================================

Pre-registration: experiments/shadows/cmb_ell3/PREREGISTRATION.md.

THE TEST. Is there a genuine present-epoch structural inflection near ell=3 in
the CMB rho_ell shape profile, statistically distinguishable from a LambdaCDM
Gaussian cosmic-variance ensemble, at the framework's out-of-sample-calibrated
location?

The rho_ell measure (Kish identity on per-ell power participation) was computed
this session on WMAP 9-yr ILC and Planck 2018 SMICA; the two profiles agree to
mean |Delta| = 0.0015, and the octupole (ell=3) carries a rotation-averaged
concentration excess of +0.033 (WMAP) / +0.037 (Planck) over a Gaussian
baseline. This script asks whether that excess is SIGNIFICANT against a genuine
LambdaCDM cosmic-variance Monte-Carlo ensemble -- not just above the ensemble
MEAN, but outside the ensemble's cosmic-variance SPREAD.

ENSEMBLE. Under LambdaCDM + statistical isotropy, the 2*ell+1 spherical-harmonic
coefficients a_{ell,m} at a fixed ell are i.i.d. Gaussian. The within-ell rho_ell
measure is scale-free in the power (it depends only on the SHAPE of the power
distribution over m, not its amplitude C_ell), so the per-ell rho_ell sampling
distribution is exactly the distribution over Gaussian a_{ell,m} draws -- the
LambdaCDM cosmic-variance distribution of rho_ell. We build it per ell with
cupy on the GPU, N = 4,000,000 realizations per multipole.

The observed statistic is the rotation-averaged rho_ell (frame-invariant). The
matched ensemble statistic is the per-realization rho_ell, which is frame-
invariant in distribution. Significance = two-sided percentile of the observed
value in the ensemble, per ell, and for the signed-crossover / inflection
structure as a whole.

ell=3 LOCATION. The framework's out-of-sample crossover (cmb_corridor_
prediction.py, A3+-calibrated, no CMB-fitted parameter) lands at ell ~ 5, not
ell = 3. The octupole anomaly at ell = 3 is a known CMB feature; whether the
framework PREDICTS ell = 3 specifically, or only ell ~ 3-5 as a free-rho_mid
fit, is reported explicitly.

Incremental output: each block flushes and the JSON is rewritten as it grows.
"""
import json
import os
import sys
import time

import numpy as np
import healpy as hp

try:
    import cupy as cp
    HAVE_GPU = True
except Exception:
    HAVE_GPU = False

HERE = os.path.dirname(os.path.abspath(__file__))
CMB_DATA = os.path.join(HERE, "..", "..", "open_system_pomega", "cmb_data")
RESULTS = os.path.join(HERE, "results_ell3_shadow.json")

LMAX = 32
ELLS = list(range(2, 13))          # ell = 2..12: the low-ell shape sector
N_MC = 4_000_000                   # LambdaCDM cosmic-variance realizations per ell
N_ROT = 400                        # random rotations for the frame-invariant obs
SEED = 20260522

state = {"meta": {"date": "2026-05-22", "test": "Shadow 3 -- ell=3 CMB inflection",
                   "n_mc_per_ell": N_MC, "ells": ELLS, "gpu": HAVE_GPU}}


def flush():
    with open(RESULTS, "w") as f:
        json.dump(state, f, indent=2)
    sys.stdout.flush()


def banner(s):
    print("=" * 78)
    print(s)
    print("=" * 78)
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# rho_ell -- Kish identity on per-ell real-harmonic-mode power participation
# ---------------------------------------------------------------------------
def rho_ell_from_alm(alm, lmax, ell):
    p = [abs(alm[hp.Alm.getidx(lmax, ell, 0)].real) ** 2]
    for mm in range(1, ell + 1):
        a = alm[hp.Alm.getidx(lmax, ell, mm)]
        p += [2.0 * a.real ** 2, 2.0 * a.imag ** 2]
    p = np.array(p)
    k = 2 * ell + 1
    k_eff = p.sum() ** 2 / (p ** 2).sum()
    return (k / k_eff - 1.0) / (k - 1.0)


# ===========================================================================
# 1 -- observed present-epoch rho_ell profile (WMAP ILC + Planck SMICA)
# ===========================================================================
banner("1 -- observed present-epoch rho_ell profile (WMAP ILC + Planck SMICA)")

MAPS = {
    "WMAP_ILC_9yr": os.path.join(CMB_DATA, "wmap_ilc_9yr_v5.fits"),
    "Planck_SMICA_R3": os.path.join(CMB_DATA, "planck_smica_R3.fits"),
}

obs = {}
for label, path in MAPS.items():
    if not os.path.exists(path):
        print(f"  MISSING: {path}")
        continue
    m = hp.remove_dipole(hp.read_map(path))
    alm = hp.map2alm(m, lmax=LMAX)
    gal = {ell: rho_ell_from_alm(alm, LMAX, ell) for ell in ELLS}
    # rotation-averaged (frame-invariant)
    rng = np.random.default_rng(SEED)
    rot = {ell: [] for ell in ELLS}
    for _ in range(N_ROT):
        a2 = alm.copy()
        hp.rotate_alm(a2, rng.uniform(0, 2 * np.pi), rng.uniform(0, np.pi),
                      rng.uniform(0, 2 * np.pi))
        for ell in ELLS:
            rot[ell].append(rho_ell_from_alm(a2, LMAX, ell))
    rot_mean = {ell: float(np.mean(rot[ell])) for ell in ELLS}
    rot_std = {ell: float(np.std(rot[ell])) for ell in ELLS}
    obs[label] = {"galactic": {str(e): float(gal[e]) for e in ELLS},
                  "rot_mean": {str(e): rot_mean[e] for e in ELLS},
                  "rot_std": {str(e): rot_std[e] for e in ELLS}}
    print(f"  {label}: rho_3 (rot-avg) = {rot_mean[3]:.4f}")

state["observed"] = obs
flush()

# the canonical observed profile for the test: mean of WMAP + Planck rot-avg
rho_obs = {}
for ell in ELLS:
    vals = [obs[lab]["rot_mean"][str(ell)] for lab in obs]
    rho_obs[ell] = float(np.mean(vals))
print()
print("  joint (WMAP+Planck mean) rotation-averaged rho_ell:")
for ell in ELLS:
    print(f"    ell={ell:2d}: rho = {rho_obs[ell]:.4f}")
state["rho_obs_joint"] = {str(e): rho_obs[e] for e in ELLS}
flush()


# ===========================================================================
# 2 -- LambdaCDM Gaussian cosmic-variance Monte-Carlo ensemble of rho_ell
# ===========================================================================
banner("2 -- LambdaCDM cosmic-variance ensemble of rho_ell (cupy, %s)"
       % ("GPU" if HAVE_GPU else "CPU fallback"))
print("  Under LambdaCDM + statistical isotropy the 2*ell+1 a_{ell,m} at fixed")
print("  ell are i.i.d. Gaussian. rho_ell is scale-free in the power, so the")
print("  per-ell cosmic-variance distribution of rho_ell is exactly the")
print("  distribution over Gaussian a_{ell,m} draws -- no C_ell input needed.")
print(f"  N = {N_MC:,} realizations per multipole.")
print()

xp = cp if HAVE_GPU else np


def rho_ensemble(ell, n, seed):
    """n LambdaCDM cosmic-variance realizations of rho_ell at this ell.

    Real harmonic representation: k = 2*ell+1 real modes (m=0, plus real and
    imag parts of m=1..ell). Under statistical isotropy each is i.i.d. N(0,1)
    up to the (irrelevant, cancelling) C_ell amplitude. Power p = a^2."""
    k = 2 * ell + 1
    rs = xp.random.RandomState(seed)
    out = xp.empty(n, dtype=xp.float64)
    chunk = 2_000_000
    done = 0
    while done < n:
        c = min(chunk, n - done)
        a = rs.standard_normal((c, k), dtype=xp.float64)
        p = a * a
        s1 = p.sum(axis=1)
        s2 = (p * p).sum(axis=1)
        k_eff = s1 * s1 / xp.maximum(s2, 1e-300)
        out[done:done + c] = (k / k_eff - 1.0) / (k - 1.0)
        done += c
    return out


ensemble = {}
ens_summary = {}
t0 = time.time()
for ell in ELLS:
    r = rho_ensemble(ell, N_MC, SEED + ell)
    rh = cp.asnumpy(r) if HAVE_GPU else r
    o = rho_obs[ell]
    # two-sided percentile of the observed value in the cosmic-variance dist
    pct = float(np.mean(rh < o))                 # fraction of ensemble below obs
    p_two = 2.0 * min(pct, 1.0 - pct)            # two-sided p-value
    mean, std = float(np.mean(rh)), float(np.std(rh))
    z = (o - mean) / std
    ens_summary[ell] = {
        "obs": o, "ens_mean": mean, "ens_std": std,
        "ens_p05": float(np.percentile(rh, 5)),
        "ens_p95": float(np.percentile(rh, 95)),
        "ens_p2_5": float(np.percentile(rh, 2.5)),
        "ens_p97_5": float(np.percentile(rh, 97.5)),
        "pct_below": pct, "p_two_sided": p_two, "z": z}
    ensemble[ell] = rh
    print(f"  ell={ell:2d}: obs={o:.4f}  ens_mean={mean:.4f}  ens_std={std:.4f}"
          f"  z={z:+.2f}  p(2-sided)={p_two:.4f}")
    sys.stdout.flush()
print(f"  [ensemble built in {time.time()-t0:.1f} s]")
state["ensemble_per_ell"] = {str(e): ens_summary[e] for e in ELLS}
flush()


# ===========================================================================
# 3 -- the signed-crossover / inflection structure at ell=3
# ===========================================================================
banner("3 -- signed-crossover / ell=3 inflection structure vs the ensemble")

# The pre-registered structural claim: quadrupole (ell=2) toward isotropy
# (low rho excess), higher multipoles toward concentration (positive rho
# excess), with an INFLECTION near ell=3. We test three concrete statistics
# against the LambdaCDM ensemble:
#
#   (A) octupole excess        D3  = rho_3 - ens_mean_3
#   (B) quadrupole deficit     D2  = rho_2 - ens_mean_2
#   (C) inflection / curvature C3  = rho_3 - 0.5*(rho_2 + rho_4)
#       -- the discrete second difference centred on ell=3; a genuine
#          ell=3 "inflection" shows up as C3 large and positive.
#
# Each is recomputed on every LambdaCDM realization triple (the ensembles at
# ell=2,3,4 are independent under statistical isotropy, exactly as the real
# multipoles are independent) to get a cosmic-variance null distribution.

e2, e3, e4 = ensemble[2], ensemble[3], ensemble[4]
m = min(len(e2), len(e3), len(e4))
e2, e3, e4 = e2[:m], e3[:m], e4[:m]

# (A) octupole excess
D3_obs = rho_obs[3] - ens_summary[3]["ens_mean"]
D3_null = e3 - ens_summary[3]["ens_mean"]
pA = float(np.mean(D3_null >= D3_obs))           # one-sided: excess UP

# (B) quadrupole: signed toward isotropy means rho_2 BELOW its corridor-rigid
# expectation. We report it descriptively vs the ensemble (no strong claim).
D2_obs = rho_obs[2] - ens_summary[2]["ens_mean"]
D2_null = e2 - ens_summary[2]["ens_mean"]
pB_low = float(np.mean(D2_null <= D2_obs))

# (C) inflection / discrete curvature centred on ell=3
C3_obs = rho_obs[3] - 0.5 * (rho_obs[2] + rho_obs[4])
C3_null = e3 - 0.5 * (e2 + e4)
pC = float(np.mean(C3_null >= C3_obs))           # one-sided: inflection UP
pC_two = 2.0 * min(pC, 1.0 - pC)

print(f"  (A) octupole excess   D3 = rho_3 - ens_mean = {D3_obs:+.4f}")
print(f"      LambdaCDM cosmic-variance: P(D3_null >= D3_obs) = {pA:.4f}")
print(f"      ens std of D3 = {np.std(D3_null):.4f}  -> z = "
      f"{D3_obs/np.std(D3_null):+.2f}")
print()
print(f"  (B) quadrupole offset D2 = rho_2 - ens_mean = {D2_obs:+.4f}")
print(f"      P(D2_null <= D2_obs) = {pB_low:.4f}  (toward-isotropy = D2 < 0)")
print()
print(f"  (C) ell=3 inflection  C3 = rho_3 - (rho_2+rho_4)/2 = {C3_obs:+.4f}")
print(f"      LambdaCDM cosmic-variance: P(C3_null >= C3_obs) = {pC:.4f}")
print(f"      two-sided p = {pC_two:.4f}   ens std of C3 = {np.std(C3_null):.4f}")
print(f"      -> inflection z = {C3_obs/np.std(C3_null):+.2f}")

state["structure_tests"] = {
    "octupole_excess": {"D3_obs": D3_obs, "p_one_sided_up": pA,
                        "z": float(D3_obs / np.std(D3_null))},
    "quadrupole_offset": {"D2_obs": D2_obs, "p_one_sided_low": pB_low},
    "ell3_inflection": {"C3_obs": C3_obs, "p_one_sided_up": pC,
                        "p_two_sided": pC_two,
                        "z": float(C3_obs / np.std(C3_null))},
}
flush()


# ===========================================================================
# 4 -- is ell=3 the framework-predicted location, or a free fit?
# ===========================================================================
banner("4 -- ell=3: framework-predicted location or free fit?")

# The framework's out-of-sample crossover: cmb_corridor_prediction.py mapped
# the A3+-calibrated corridor (k_eff in [2.8,4.8], 5 substrates, NO CMB data)
# through the Kish identity to a per-ell corridor centre, and found the
# observed profile crosses that centre at ell ~ 5 -- NOT ell = 3.
KEFF_LO, KEFF_HI = 2.8, 4.8
KEFF_MID = 0.5 * (KEFF_LO + KEFF_HI)


def rho_at(k, keff):
    return (k / keff - 1.0) / (k - 1.0)


centre = {ell: rho_at(2 * ell + 1, KEFF_MID) for ell in ELLS}
crossover = None
for ell in ELLS:
    if rho_obs[ell] < centre[ell]:
        crossover = ell
        break
print(f"  framework A3+-calibrated per-ell corridor centre (k_eff={KEFF_MID}):")
for ell in [2, 3, 4, 5, 6, 8, 12]:
    print(f"    ell={ell:2d}: centre={centre[ell]:.4f}  obs={rho_obs[ell]:.4f}"
          f"  {'obs ABOVE' if rho_obs[ell]>=centre[ell] else 'obs below'}")
print(f"  out-of-sample crossover (obs crosses centre): ell = {crossover}")
state["framework_location"] = {
    "keff_mid": KEFF_MID,
    "per_ell_centre": {str(e): centre[e] for e in ELLS},
    "out_of_sample_crossover_ell": crossover,
    "predicted_ell_is_3": crossover == 3,
}
flush()


# ===========================================================================
# 5 -- verdict
# ===========================================================================
banner("5 -- VERDICT")
ALPHA = 0.05
sig_octupole = pA < ALPHA
sig_inflection = pC_two < ALPHA
at_predicted = (crossover == 3)

print(f"  octupole (ell=3) excess significant vs LambdaCDM ensemble: "
      f"{sig_octupole}  (p={pA:.4f})")
print(f"  ell=3 inflection significant vs LambdaCDM ensemble:        "
      f"{sig_inflection}  (p_two={pC_two:.4f})")
print(f"  ell=3 is the framework's out-of-sample-calibrated location: "
      f"{at_predicted}  (crossover at ell={crossover})")
print()

if (sig_octupole or sig_inflection) and at_predicted:
    verdict = "PASS"
    reason = ("the ell=3 feature is significant beyond LambdaCDM cosmic "
              "variance AND sits at the framework's out-of-sample-calibrated "
              "location.")
else:
    verdict = "NULL"
    bits = []
    if not (sig_octupole or sig_inflection):
        bits.append("the ell=3 feature is within LambdaCDM cosmic variance")
    if not at_predicted:
        bits.append(f"the framework's out-of-sample crossover is at ell="
                     f"{crossover}, not ell=3")
    reason = "; ".join(bits) + "."

print(f"  VERDICT: {verdict}")
print(f"  {reason}")
state["verdict"] = {"verdict": verdict, "reason": reason,
                    "alpha": ALPHA,
                    "octupole_significant": bool(sig_octupole),
                    "inflection_significant": bool(sig_inflection),
                    "at_predicted_location": bool(at_predicted)}
flush()
print()
print(f"  results JSON: {RESULTS}")

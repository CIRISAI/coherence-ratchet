"""
fMRI corridor test — Claims 1 & 4 at the human-neural substrate.
================================================================

StructuralClaims.lean Claim 1 (the corridor is a bounded attractor at every
coordinated substrate — off rigidity ρ→1, off chaos ρ→0) and Claim 4 (the
corridor recurs at every coordinated rung). The human brain at rest is a
coordinated, maintained, non-thermal rung — the corridor IS expected here if
the claims hold; a null is a genuine partial falsifier.

Substrate: resting-state functional MRI. Constituents = brain regions
(CC200 functional parcellation, k = 200). Within-rung correlation ρ = mean
absolute pairwise functional connectivity (region-region BOLD correlation).

Data: ABIDE Preprocessed (ABIDE-PCP), fetched via nilearn — fully open, no
credentials (HCP would need a data-use agreement). cpac / filt_noglobal
pipeline. Typically-developing CONTROLS only.

See PREREGISTRATION.md for the pre-registered ρ construction, corridor
criterion, confound controls, and falsifier — all fixed before this ran.
"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from nilearn import datasets

# Pre-registration capped at n_subjects=100 (50 controls). The ABIDE fetcher's
# n_subjects counts ALL subjects, not controls; raising it to 250 yields 139
# controls across 7 sites — strictly more data and better site coverage, same
# fixed pipeline/parcellation/criterion. Both runs are reported in RESULTS.md;
# the 100-subject run produced the identical CORRIDOR-CONFIRMED verdict.
N_SUBJECTS = 250
N_SURROGATE = 5           # phase-randomized noise-floor draws
K_NOMINAL = 200           # CC200 regions
A3_BAND = (0.17, 0.35)    # recalculated A3+ corridor (corridor_recalculation.py)
LOW_MOTION_FD = 0.20      # mm, pre-registered low-motion cutoff
SEED = 0


def mean_abs_offdiag(C):
    d = C.shape[0]
    return float(np.mean(np.abs(C[~np.eye(d, dtype=bool)])))


def phase_randomize(x, rng):
    """Phase-randomize a real timeseries: destroys cross-series correlation,
    preserves each series' power spectrum / autocorrelation."""
    n = x.shape[0]
    F = np.fft.rfft(x, axis=0)
    amp = np.abs(F)
    ph = np.angle(F)
    # randomize phases of the non-DC, non-Nyquist bins, independently per column
    rand = rng.uniform(-np.pi, np.pi, size=F.shape)
    rand[0] = 0.0
    if n % 2 == 0:
        rand[-1] = 0.0
    Fs = amp * np.exp(1j * (ph * 0.0 + rand))
    return np.fft.irfft(Fs, n=n, axis=0)


def subject_rho(ts, rng):
    """ts: (T timepoints x R regions). Returns (rho_raw, floor, rho_debiased,
    k_eff_emp, k_eff_kish) or None if the timeseries is unusable."""
    ts = np.asarray(ts, dtype=float)
    if ts.ndim != 2 or ts.shape[0] < 30:
        return None
    sd = ts.std(axis=0)
    keep = sd > 1e-8
    ts = ts[:, keep]
    if ts.shape[1] < 10:
        return None
    Z = (ts - ts.mean(axis=0)) / ts.std(axis=0)
    T = Z.shape[0]
    C = (Z.T @ Z) / T
    rho_raw = mean_abs_offdiag(C)

    floors = []
    for _ in range(N_SURROGATE):
        Zs = phase_randomize(Z, rng)
        Zs = (Zs - Zs.mean(axis=0)) / (Zs.std(axis=0) + 1e-12)
        Cs = (Zs.T @ Zs) / T
        floors.append(mean_abs_offdiag(Cs))
    floor = float(np.mean(floors))
    rho_deb = float(np.sqrt(max(rho_raw ** 2 - floor ** 2, 0.0)))

    # effective dimensionality: participation ratio of the C eigenvalues
    ev = np.linalg.eigvalsh(C)
    ev = ev[ev > 1e-9]
    k_eff_emp = float((ev.sum() ** 2) / (ev ** 2).sum())
    k = ts.shape[1]
    k_eff_kish = float(k / (1.0 + rho_deb * (k - 1.0)))
    return rho_raw, floor, rho_deb, k_eff_emp, k_eff_kish


def pct(a, q):
    return float(np.percentile(a, q))


print("=" * 78)
print("fMRI corridor test — Claims 1 & 4, human-neural substrate (ABIDE-PCP)")
print("=" * 78)
print("Fetching ABIDE-PCP rois_cc200 (cpac / filt_noglobal, no GSR) ...")
abide = datasets.fetch_abide_pcp(
    derivatives=["rois_cc200"], pipeline="cpac",
    band_pass_filtering=True, global_signal_regression=False,
    n_subjects=N_SUBJECTS, quality_checked=True, verbose=0)
ts_all = abide["rois_cc200"]
ph = abide["phenotypic"]
print(f"  fetched {len(ts_all)} subjects (quality_checked).")

# CONTROLS only (DX_GROUP == 2, pre-registered)
dx = np.asarray(ph["DX_GROUP"])
fd = np.asarray(ph["func_mean_fd"], dtype=float)
site = np.asarray(ph["SITE_ID"])
ctrl = dx == 2
print(f"  controls (DX_GROUP==2): {ctrl.sum()} of {len(ts_all)}.")

rng = np.random.default_rng(SEED)
rows = []   # (rho_raw, floor, rho_deb, k_eff_emp, k_eff_kish, fd, site)
for i in range(len(ts_all)):
    if not ctrl[i]:
        continue
    res = subject_rho(ts_all[i], rng)
    if res is None:
        continue
    rows.append((*res, fd[i], str(site[i])))

rho_raw = np.array([r[0] for r in rows])
floor = np.array([r[1] for r in rows])
rho_deb = np.array([r[2] for r in rows])
keff_emp = np.array([r[3] for r in rows])
keff_kish = np.array([r[4] for r in rows])
fd_s = np.array([r[5] for r in rows])
site_s = np.array([r[6] for r in rows])
n = len(rows)

print()
print("=" * 78)
print(f"RESULTS — n = {n} control subjects")
print("=" * 78)
print(f"  rho_raw      (mean|FC|)        : median {np.median(rho_raw):.3f}  "
      f"[{rho_raw.min():.3f}, {rho_raw.max():.3f}]")
print(f"  noise floor  (phase-random.)   : median {np.median(floor):.3f}  "
      f"[{floor.min():.3f}, {floor.max():.3f}]")
print(f"  rho_DEBIASED (genuine FC)      : median {np.median(rho_deb):.3f}  "
      f"[{rho_deb.min():.3f}, {rho_deb.max():.3f}]")
print(f"    5th pctile {pct(rho_deb,5):.3f}   25th {pct(rho_deb,25):.3f}   "
      f"75th {pct(rho_deb,75):.3f}   95th {pct(rho_deb,95):.3f}")
iqr = pct(rho_deb, 75) - pct(rho_deb, 25)
print(f"    IQR {iqr:.3f}")
print(f"  k_eff empirical (particip.rat.): median {np.median(keff_emp):.1f}  "
      f"[{keff_emp.min():.1f}, {keff_emp.max():.1f}]   (k_nominal = {K_NOMINAL})")
print(f"  k_eff Kish  (200/(1+rho(k-1))) : median {np.median(keff_kish):.2f}  "
      f"[{keff_kish.min():.2f}, {keff_kish.max():.2f}]")

print()
print("CORRIDOR CRITERION (pre-registered)")
c1 = (pct(rho_deb, 95) < 0.60) and (rho_deb.max() <= 0.80)
c2 = (pct(rho_deb, 5) > 0.05)
median_in_band = A3_BAND[0] <= np.median(rho_deb) <= A3_BAND[1]
c3 = (iqr <= 0.15) and median_in_band
print(f"  C1 off rigidity  (95p<0.60 & max<=0.80) : {'PASS' if c1 else 'FAIL'}"
      f"   (95p={pct(rho_deb,95):.3f}, max={rho_deb.max():.3f})")
print(f"  C2 off chaos     (5p>0.05)              : {'PASS' if c2 else 'FAIL'}"
      f"   (5p={pct(rho_deb,5):.3f})")
print(f"  C3 bounded band  (IQR<=0.15 & median in {A3_BAND}) : "
      f"{'PASS' if c3 else 'FAIL'}   (IQR={iqr:.3f}, median={np.median(rho_deb):.3f})")

print()
print("CONFOUND CONTROLS (pre-registered)")
# 1. motion
from scipy.stats import spearmanr
rho_fd, p_fd = spearmanr(rho_deb, fd_s)
print(f"  motion: Spearman(rho_deb, mean_FD) = {rho_fd:+.3f}  (p={p_fd:.3g})")
lowm = fd_s < LOW_MOTION_FD
if lowm.sum() >= 10:
    rd_lm = rho_deb[lowm]
    c1_lm = (pct(rd_lm, 95) < 0.60) and (rd_lm.max() <= 0.80)
    c2_lm = pct(rd_lm, 5) > 0.05
    iqr_lm = pct(rd_lm, 75) - pct(rd_lm, 25)
    c3_lm = (iqr_lm <= 0.15) and (A3_BAND[0] <= np.median(rd_lm) <= A3_BAND[1])
    print(f"    low-motion subset (FD<{LOW_MOTION_FD}): n={lowm.sum()}, "
          f"median rho_deb={np.median(rd_lm):.3f}, IQR={iqr_lm:.3f}")
    print(f"    low-motion corridor verdict: "
          f"C1={'P' if c1_lm else 'F'} C2={'P' if c2_lm else 'F'} "
          f"C3={'P' if c3_lm else 'F'}  "
          f"-> {'STABLE' if (c1_lm,c2_lm,c3_lm)==(c1,c2,c3) else 'FLIPPED (motion-confounded)'}")
else:
    print(f"    low-motion subset too small (n={lowm.sum()}) — skipped")

# 4. site heterogeneity
print(f"  site heterogeneity ({len(np.unique(site_s))} sites):")
for s in sorted(np.unique(site_s)):
    m = site_s == s
    if m.sum() >= 3:
        print(f"    {s:<14} n={m.sum():>3}  median rho_deb={np.median(rho_deb[m]):.3f}")

print()
print("=" * 78)
print("READING")
print("=" * 78)
poles_clear = c1 and c2
if c1 and c2 and c3:
    verdict = ("CORRIDOR CONFIRMED. The human-neural rung sits in a bounded "
               "band, off both poles, median inside the A3+ corridor. Claims "
               "1 & 4 SUPPORTED at the human-neural substrate.")
elif poles_clear and not c3:
    verdict = ("PARTIAL. Off both poles (C1 & C2 pass) but the band/median "
               "criterion (C3) fails — corridor exists as 'off the poles' but "
               "does not coincide with the calibrated A3+ band. Claims 1 & 4 "
               "WEAKLY supported, mirroring E1's LLM verdict.")
else:
    failed = []
    if not c1: failed.append("rigidity pole (C1)")
    if not c2: failed.append("chaos pole (C2)")
    verdict = ("PARTIAL FALSIFIER. " + " and ".join(failed) + " — a "
               "coordinated, persistent substrate sitting at a pole. Claims "
               "1 & 4 PARTIALLY FALSIFIED at the human-neural substrate.")
print("  " + verdict)

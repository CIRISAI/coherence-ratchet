#!/usr/bin/env python3
"""
ADVERSARIAL cosmological probe of the criticality-vs-low-rank SATURATION
discriminator, on EMERGENT COSMIC STRUCTURE (the galaxy density field / cosmic
web), NOT the CMB.

WHY ADVERSARIAL. The primordial matter power spectrum is nearly scale-invariant
(n_s ~ 0.96 -- almost a pure power law). In this discriminator's language a
power-law, NON-saturating spectrum is the CRITICALITY signature. So cosmology is
a substrate whose natural prior is exactly the "trivial / power-law" read. If the
corridor (bounded k_eff) is a universal claim it has to survive here.

WHAT IS AND ISN'T THE TARGET. The framework is EXACTLY LambdaCDM for the CMB
(orthogonality theorem); the CMB is NOT the target and is not touched here. The
corridor / low-rank content is about EMERGENT coordinating structure -- halos,
the cosmic web, galaxy clustering -- i.e. the LATE-TIME, gravitationally-evolved
density field. That is what we spectrum.

THE OBJECT WE BUILD (physically transparent). Real SDSS DR17 spectroscopic
galaxies (NGC, z in [0.02,0.15]) -> comoving Cartesian coords -> a fine cubic
mesh of micro-cells (L=10 Mpc/h). We tile the survey interior with disjoint
sub-cubes of M^3 = 5^3 = 125 micro-cells (50 Mpc/h). Each sub-cube that lies
fully inside the survey footprint is one "observation". The matrix is

    X[i, t] = overdensity delta of relative micro-cell position i in sub-cube t

so UNITS = relative micro-cell positions (N = 125), OBSERVATIONS = sub-cubes
(T ~ 159). The unit x unit correlation over sub-cubes is then, by construction,
the normalized two-point density covariance C_ij ~ xi(|r_i - r_j|); ITS
EIGENVALUES ARE THE DISCRETE POWER-SPECTRUM MODES. Subsampling micro-cells tests
whether effective dimensionality saturates; the eigenvalue power-law slope alpha
is the discriminator's "criticality" axis and is directly a P(k) diagnostic.

THE GRAIN CAVEAT (load-bearing; stated up front in the summary). The universe is
the one truly complete unit, but ANY dataset is a subsample of it -- a finite
volume of our past light cone. By the objective measure used this session
(saturation on a COMPLETE unit), a subsample can read high-dimensional for grain
reasons alone -- exactly as mouse-V1 cortex did. So a NON-saturating read here is
most likely GRAIN-INCONCLUSIVE, not a falsification. Reported accordingly.

Analysis core (corr_eig, participation_ratio, mp_edge, phase_randomize,
subsample_pr, synth_*) is reused verbatim from spectral_test.py; synthetics ONLY
calibrate the estimator at this (N,T). No fabricated data enters the verdict.
"""
import numpy as np, pandas as pd, json, os
from astropy.cosmology import FlatLambdaCDM

RNG = np.random.default_rng(0)
HERE = os.path.dirname(os.path.abspath(__file__))
GAL = os.path.join(HERE, "cosmo_sdss_galaxies.parquet")

# ---- analysis core (identical to spectral_test.py) --------------------------
def corr_eig(X):
    N, T = X.shape
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    C = (Z @ Z.T) / T
    ev = np.linalg.eigvalsh(C)[::-1]
    return np.clip(ev, 0, None), N, T
def participation_ratio(ev):
    return (ev.sum() ** 2) / (ev ** 2).sum()
def mp_edge(N, T, sigma2=1.0):
    q = N / T
    return sigma2 * (1 + np.sqrt(q)) ** 2
def phase_randomize(X):
    F = np.fft.rfft(X, axis=1)
    ph = np.exp(1j * RNG.uniform(0, 2*np.pi, F.shape)); ph[:, 0] = 1
    return np.fft.irfft(F * ph, n=X.shape[1], axis=1)
def subsample_pr(X, sizes, ndraw=40):
    N = X.shape[0]; out = []
    for n in sizes:
        if n > N: continue
        prs = []
        for _ in range(ndraw):
            idx = RNG.choice(N, n, replace=False)
            ev, *_ = corr_eig(X[idx]); prs.append(participation_ratio(ev))
        out.append((n, float(np.mean(prs)), float(np.std(prs))))
    return out
def synth_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T)); W = RNG.standard_normal((N, r))
    return W @ F + snr**-1 * RNG.standard_normal((N, T)) * np.sqrt(r)
def synth_powerlaw(N, T, alpha=1.0):
    lam = (np.arange(1, N+1) ** (-alpha)); lam = lam / lam.sum() * N
    L = np.sqrt(lam)[:, None] * RNG.standard_normal((N, T))
    Q, _ = np.linalg.qr(RNG.standard_normal((N, N))); return Q @ L
def synth_noise(N, T):
    return RNG.standard_normal((N, T))

def powerlaw_alpha(ev, i_lo=2, i_hi_frac=0.5):
    """slope of eigenvalue_i ~ i^-alpha over an informative rank range."""
    ev = np.clip(ev, 1e-12, None)
    n = len(ev); i_hi = max(i_lo+3, int(i_hi_frac*n))
    idx = np.arange(i_lo, i_hi)
    a = -np.polyfit(np.log10(idx+1), np.log10(ev[idx]), 1)[0]
    return float(a)

def calibrate(N, T):
    print(f"=== CALIBRATION at N={N}, T={T} (cosmology ruler) ===")
    sizes = [s for s in [10,15,20,30,40,60,80,100,125] if s <= N]
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("power-law a=0.3", synth_powerlaw(N, T, 0.3)),
                    ("pure noise", synth_noise(N, T))]:
        ev, n, t = corr_eig(X); pr = participation_ratio(ev)
        Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
        eff = int((ev > evs.max()).sum())
        curve = subsample_pr(X, sizes, ndraw=20)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        up = cn >= max(30, cn.max()//4)
        beta = np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]
        alpha = powerlaw_alpha(ev)
        print(f"  {name:16s}: PR={pr:7.2f}  eff_rank={eff:3d}  beta_sub={beta:6.3f}  alpha={alpha:6.3f}")
    print("  (expect: low-rank beta~0 small-rank; power-law beta 0.2-0.7 alpha~input; noise beta~1)\n")

# ---- build the density-field covariance matrix from real galaxies ----------
def build_matrix(L=10.0, M=5, min_frac=1.5):
    df = pd.read_parquet(GAL)
    cos = FlatLambdaCDM(H0=100, Om0=0.31)     # H0=100 -> Mpc/h
    z = df.z.to_numpy(); ra = np.deg2rad(df.ra.to_numpy()); dec = np.deg2rad(df.dec.to_numpy())
    Dc = cos.comoving_distance(z).value
    x = Dc*np.cos(dec)*np.cos(ra); y = Dc*np.cos(dec)*np.sin(ra); zc = Dc*np.sin(dec)
    grid_d = np.linspace(0.001, 0.2, 400); grid_D = cos.comoving_distance(grid_d).value
    def interior(xx, yy, zz):
        d = np.sqrt(xx**2+yy**2+zz**2); ra_ = np.rad2deg(np.arctan2(yy, xx)) % 360
        dec_ = np.rad2deg(np.arcsin(np.clip(zz/d, -1, 1))); zz_ = np.interp(d, grid_D, grid_d)
        return (ra_>132)&(ra_<238)&(dec_>2)&(dec_<58)&(zz_>0.023)&(zz_<0.147)
    lo = np.array([x.min(), y.min(), zc.min()])
    ix = np.floor((x-lo[0])/L).astype(int); iy = np.floor((y-lo[1])/L).astype(int); iz = np.floor((zc-lo[2])/L).astype(int)
    nx, ny, nz = ix.max()+1, iy.max()+1, iz.max()+1
    counts = np.zeros((nx, ny, nz)); np.add.at(counts, (ix, iy, iz), 1)
    cols = []
    for bx in range(nx//M):
      for by in range(ny//M):
        for bz in range(nz//M):
          block = counts[bx*M:(bx+1)*M, by*M:(by+1)*M, bz*M:(bz+1)*M]
          cx = lo[0]+(bx*M+np.arange(M)+0.5)*L; cy = lo[1]+(by*M+np.arange(M)+0.5)*L; cz = lo[2]+(bz*M+np.arange(M)+0.5)*L
          gx, gy, gz = np.meshgrid(cx, cy, cz, indexing='ij')
          if interior(gx, gy, gz).all() and block.sum() >= min_frac*M**3:
              mean = block.mean()
              delta = (block.ravel()/mean) - 1.0     # overdensity per micro-cell, sub-cube-relative
              cols.append(delta)
    X = np.array(cols).T                             # N micro-cells x T sub-cubes
    return X, dict(L=L, M=M, subcube_Mpc_h=L*M, N=X.shape[0], T=X.shape[1])

def main():
    X, meta = build_matrix()
    N, T = X.shape
    # drop degenerate units (constant across sub-cubes)
    good = X.std(1) > 1e-9
    X = X[good]; N = X.shape[0]
    print(f"density-field covariance matrix: N={N} micro-cells (10 Mpc/h) x T={T} "
          f"sub-cubes ({meta['subcube_Mpc_h']:.0f} Mpc/h)\n")
    calibrate(N, T)

    ev, N, T = corr_eig(X)
    pr = participation_ratio(ev)
    edge = mp_edge(N, T)
    eff_rank_mp = int((ev > edge).sum())
    Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
    surr_top = float(evs.max()); surr_rank_mp = int((evs > edge).sum())
    eff_rank_surr = int((ev > surr_top).sum())
    alpha = powerlaw_alpha(ev)

    sizes = [s for s in [8,12,16,24,32,48,64,80,100,125] if s <= N]
    curve = subsample_pr(X, sizes)
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    up = cn >= max(30, cn.max()//4)
    beta = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]) if up.sum()>=3 else float("nan")
    beta_top = float(np.polyfit(np.log10(cn[cn>=cn.max()//2]), np.log10(cp[cn>=cn.max()//2]), 1)[0])

    print(f"{'N':>4s} {'T':>5s} {'PR/k_eff':>9s} {'eff_rank_mp':>11s} {'eff_rank_surr':>13s} "
          f"{'MPedge':>7s} {'beta':>6s} {'alpha':>6s}")
    print(f"{N:4d} {T:5d} {pr:9.2f} {eff_rank_mp:11d} {eff_rank_surr:13d} {edge:7.2f} {beta:6.3f} {alpha:6.3f}")
    print("\nsaturation curve (PR vs N'):")
    for n, m, s in curve:
        print(f"  N'={n:4d}  PR={m:7.3f} +/- {s:5.3f}")
    print(f"\ntop 10 eigs: {[round(float(x),3) for x in ev[:10]]}")
    print(f"phase-randomized surrogate: {surr_rank_mp} eigs above MP edge, top {surr_top:.3f}")

    # verdict with grain caveat
    saturates = (beta_top < 0.15) and (eff_rank_surr <= 12)
    powerlaw  = (beta > 0.2) or (alpha > 0.2 and eff_rank_surr > 12)
    if saturates:
        verdict = ("SATURATES (bounded k_eff): consistent with the corridor AT THIS GRAIN. "
                   "Not decisive -- a complete-unit test is impossible for the universe.")
    elif powerlaw:
        verdict = ("NON-SATURATING / POWER-LAW (alpha>0): the adversarial cosmological "
                   "scale-invariance signature -- BUT GRAIN-CONFOUNDED (survey = finite "
                   "past-light-cone subsample), so GRAIN-INCONCLUSIVE, not a falsification.")
    else:
        verdict = "MIXED / GRAIN-INCONCLUSIVE"
    print(f"\nVERDICT: {verdict}")

    out = dict(
        substrate="SDSS DR17 galaxy density-field covariance (emergent cosmic web; NOT the CMB)",
        construction=("micro-cell overdensity matrix; units=relative micro-cell positions, "
                      "observations=survey-interior sub-cubes; unit x unit correlation = "
                      "normalized two-point density covariance, eigenvalues = discrete P(k) modes"),
        n_galaxies=int(pd.read_parquet(GAL).shape[0]),
        micro_cell_Mpc_h=meta['L'], subcube_Mpc_h=meta['subcube_Mpc_h'],
        N_units=N, T_observations=T, PR_keff=pr, mp_edge=edge,
        eff_rank_mp=eff_rank_mp, eff_rank_surr=eff_rank_surr, surr_rank_mp=surr_rank_mp,
        beta_sub=beta, beta_top=beta_top, alpha_powerlaw=alpha,
        top_eigs=[float(x) for x in ev[:16]], subsample=curve,
        primordial_ns_ref=0.96,
        grain_caveat=("any dataset is a subsample of the one complete unit (the universe); "
                      "a non-saturating read can be grain-driven, as mouse-V1 cortex was."),
        verdict=verdict)
    json.dump(out, open(os.path.join(HERE, "spectral_results_cosmo.json"), "w"), indent=1)
    print("\nwrote spectral_results_cosmo.json")

if __name__ == "__main__":
    main()

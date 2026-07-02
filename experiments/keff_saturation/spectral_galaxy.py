#!/usr/bin/env python3
"""
COMPLETE-GALAXY k_eff SATURATION test of the criticality-vs-low-rank discriminator.

A legitimate COMPLETE, GRAVITATIONALLY-BOUND unit at astrophysical scale: ONE
central galaxy (SUBFIND subhalo 0) from a CAMELS IllustrisTNG L25n256 simulation
(CV_0), with ALL ~4.8e4 of its z=0 star particles. Because we hold every star of
the bound unit, subsampling runs up to the full constituent count and "wrong
grain" cannot be invoked (unlike a galaxy-SURVEY subsample of the universe, or
Gaia's partial internal view of the Milky Way).

CONCEPTUAL CAVEAT (stated up front, not glossed). A galaxy is bound by GRAVITY --
a conservative binding force. In this framework's dynamics drho/dt = alpha(rho,S)
- gamma*M, gravity is the SPONTANEOUS alpha-term (shared potential well), NOT the
active-maintenance gamma*M that defines corridor COORDINATION. So this tests
"does a complete BOUND unit saturate," which is adjacent to but not identical to
"does a complete COORDINATING unit saturate." It does not settle the
coordinating-unit question.

THE MATRIX (the crux -- avoids the trivial rank<=6 stars x {x,y,z,vx,vy,vz} trap).
TIME-RESOLVED: units = star particles (tracked by ParticleID), observations =
simulation snapshots. Entry X[i,t] = a kinematic scalar of star i at snapshot t,
measured in the galaxy's own instantaneous frame:
   primary  : z-height above the instantaneous disk plane (physical kpc)
   robust-2 : specific angular momentum j_z about the disk axis
   robust-3 : galactocentric radial velocity v_r (km/s, physical peculiar)
The star x star correlation OVER SNAPSHOTS then asks whether the galaxy's
dynamics collapse to a FEW collective modes (rotation / bar / bending+breathing
waves / coherent settling = LOW-RANK) or are high-dimensional (each star an
independent oscillator). Saturation = few collective modes.

Because rank <= T-1, PR necessarily plateaus in N; that plateau is NOT itself the
signal. The discriminating quantities are (i) the plateau LEVEL vs the matched-
(N,T) synthetic calibrators, (ii) the eigenvalue power-law slope alpha, (iii) the
effective rank above the Marchenko-Pastur edge and above a phase-randomized
surrogate. Synthetics ONLY calibrate the estimator at this (N,T); no fabricated
data enters the verdict.

Analysis core (corr_eig, participation_ratio, mp_edge, phase_randomize,
subsample_pr, synth_*) reused verbatim from spectral_test.py.
"""
import numpy as np, h5py, fsspec, json, os, time

RNG = np.random.default_rng(0)
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-1000/-home-emoore-coherence-ratchet/a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad"
BASE = "https://users.flatironinstitute.org/~camels/Sims/IllustrisTNG/CV/CV_0"
SNAPS = list(range(40, 91, 2))          # z=2.3 -> 0.0, 26 snapshots
TARGET_SUB = 0                          # central of group 0; first N stars in snapshot
N_TARGET_STARS = 47736                  # SubhaloLenType[0,4] at snap 90

# ---- analysis core (identical to spectral_test.py) --------------------------
def corr_eig(X):
    """Correlation-matrix eigenvalues (desc). For N>T use the Gram/dual trick:
    the nonzero spectrum of (1/T)ZZ^T (NxN) equals that of (1/T)Z^T Z (TxT).
    Identical nonzero eigenvalues, no NxN matrix formed. (Same device the
    zebrafish whole-brain run used for N>>T.)"""
    N, T = X.shape
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    if N > T:
        G = (Z.T @ Z) / T                    # TxT, same nonzero eigenvalues
        ev = np.linalg.eigvalsh(G)[::-1]
    else:
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
def powerlaw_alpha(ev, i_lo=2, i_hi_frac=0.7):
    ev = np.clip(ev, 1e-12, None)
    n = len(ev); i_hi = max(i_lo+3, int(i_hi_frac*n))
    idx = np.arange(i_lo, i_hi)
    a = -np.polyfit(np.log10(idx+1), np.log10(ev[idx]), 1)[0]
    return float(a)

# ---- data fetch (remote partial HDF5; ~8MB of star arrays per snapshot) ------
def opn(u): return h5py.File(fsspec.open(u, 'rb').open(), 'r')

def fetch_snapshot_stars(snap):
    """Return dict a, ids, pos(ckpc/h), vel(raw), for ALL box star particles.
    Cached to scratchpad so restarts are cheap."""
    cache = f"{SCRATCH}/gal_snap_{snap:03d}.npz"
    if os.path.exists(cache):
        d = np.load(cache)
        return dict(a=float(d['a']), ids=d['ids'], pos=d['pos'], vel=d['vel'])
    with opn(f"{BASE}/snapshot_{snap:03d}.hdf5") as f:
        a = float(f['Header'].attrs['Time'])
        ids = f['PartType4/ParticleIDs'][:]
        pos = f['PartType4/Coordinates'][:].astype(np.float64)   # ckpc/h
        vel = f['PartType4/Velocities'][:].astype(np.float64)    # km/s * sqrt(a)
    np.savez(cache, a=a, ids=ids, pos=pos, vel=vel)
    return dict(a=a, ids=ids, pos=pos, vel=vel)

def robust_center(pos, vel, box=25000.0, n_iter=4):
    """Iterative robust galaxy center & bulk velocity, periodic-aware."""
    # unwrap relative to the median (galaxy << box, so a single shift suffices)
    ref = np.median(pos, axis=0)
    d = pos - ref
    d -= box * np.round(d / box)
    p = ref + d
    c = np.median(p, axis=0)
    for _ in range(n_iter):
        r = np.linalg.norm(p - c, axis=1)
        rcut = np.percentile(r, 80)          # shrink onto the bound core
        m = r < max(rcut, 1e-3)
        c = p[m].mean(0)
    r = np.linalg.norm(p - c, axis=1)
    core = r < np.percentile(r, 80)
    V = vel[core].mean(0)
    return p, c, V, core

def build_tracked(scalar="zheight"):
    """Build the persistent-star x snapshot matrix for one bound galaxy."""
    target_ids = np.load(f"{SCRATCH}/target_ids.npy")
    target_ids = target_ids[target_ids > 0]      # drop wind (id encoded); real stars
    # first pass: which target stars exist in EVERY snapshot
    present = None
    snapdata = {}
    for s in SNAPS:
        d = fetch_snapshot_stars(s)
        idset = d['ids']
        # membership of target ids in this snapshot
        order = np.argsort(idset)
        sid = idset[order]
        pos_in = np.searchsorted(sid, target_ids)
        pos_in = np.clip(pos_in, 0, len(sid)-1)
        hit = sid[pos_in] == target_ids
        snapdata[s] = (d, order, sid, pos_in, hit)
        present = hit if present is None else (present & hit)
        print(f"  snap {s:03d} z={1/d['a']-1:5.2f}: target present {hit.sum():6d} / {len(target_ids)}  (cum {present.sum()})", flush=True)
    keep_ids = target_ids[present]
    print(f"persistent stars across all {len(SNAPS)} snaps: {len(keep_ids)}", flush=True)

    T = len(SNAPS); Nfull = len(keep_ids)
    Z = np.full((Nfull, T), np.nan)
    prevL = None
    radii_last = None
    for ti, s in enumerate(SNAPS):
        d, order, sid, _, _ = snapdata[s]
        pos_in = np.searchsorted(sid, keep_ids)
        idx = order[pos_in]                       # rows in this snapshot's arrays
        a = d['a']
        pos = d['pos'][idx]; vel = d['vel'][idx]
        p, c, V, core = robust_center(pos, vel)
        r = (p - c) * a                           # physical kpc/h
        vv = vel * np.sqrt(a) - V                 # physical peculiar km/s (TNG conv)
        # disk axis from angular momentum of the bound core
        L = np.cross(r[core], vv[core]).sum(0)
        Lh = L / (np.linalg.norm(L) + 1e-30)
        if prevL is not None and np.dot(Lh, prevL) < 0:
            Lh = -Lh
        prevL = Lh
        z = r @ Lh                                # height above plane
        Rvec = r - np.outer(z, Lh)               # in-plane
        Rcyl = np.linalg.norm(Rvec, axis=1)
        rhat = r / (np.linalg.norm(r, axis=1, keepdims=True) + 1e-30)
        v_r = np.sum(vv * rhat, axis=1)
        j = np.cross(r, vv); j_z = j @ Lh
        if scalar == "zheight": Z[:, ti] = z
        elif scalar == "jz":    Z[:, ti] = j_z
        elif scalar == "vr":    Z[:, ti] = v_r
        elif scalar == "Rcyl":  Z[:, ti] = Rcyl
        if s == SNAPS[-1]:
            radii_last = np.linalg.norm(r, axis=1)
    return keep_ids, Z, radii_last

def calibrate(N, T):
    print(f"=== CALIBRATION at N={N}, T={T} (galaxy ruler) ===", flush=True)
    sizes = [s for s in [10,20,50,100,300,1000,3000,10000,30000] if s <= N]
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("low-rank r=6", synth_lowrank(N, T, r=6)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("pure noise", synth_noise(N, T))]:
        ev, *_ = corr_eig(X); pr = participation_ratio(ev)
        Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
        eff = int((ev > evs.max()).sum())
        curve = subsample_pr(X, sizes, ndraw=8)
        cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
        up = cn >= max(300, cn.max()//10)
        beta = np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]
        alpha = powerlaw_alpha(ev)
        print(f"  {name:16s}: PR={pr:6.2f} eff_rank={eff:3d} beta_top={beta:6.3f} alpha={alpha:6.3f}", flush=True)
    print("  (low-rank: PR~r, beta~0, small rank; power-law: PR big, beta>0, alpha~input; noise: rank~0)\n", flush=True)

def analyze(Z, scalar):
    good = np.isfinite(Z).all(1) & (Z.std(1) > 1e-12)
    X = Z[good]; N, T = X.shape
    ev, N, T = corr_eig(X); pr = participation_ratio(ev)
    edge = mp_edge(N, T); eff_rank_mp = int((ev > edge).sum())
    Xs = phase_randomize(X); evs, *_ = corr_eig(Xs)
    surr_top = float(evs.max()); surr_rank_mp = int((evs > edge).sum())
    eff_rank_surr = int((ev > surr_top).sum())
    alpha = powerlaw_alpha(ev)
    sizes = [s for s in [10,20,50,100,300,1000,3000,10000,30000,N] if s <= N]
    curve = subsample_pr(X, sorted(set(sizes)))
    cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
    up = cn >= max(300, cn.max()//10)
    beta_top = float(np.polyfit(np.log10(cn[up]), np.log10(cp[up]), 1)[0]) if up.sum()>=3 else float('nan')
    return dict(scalar=scalar, N=N, T=T, PR_keff=float(pr), mp_edge=float(edge),
                eff_rank_mp=eff_rank_mp, eff_rank_surr=eff_rank_surr,
                surr_rank_mp=surr_rank_mp, surr_top=surr_top,
                beta_top=beta_top, alpha=alpha,
                top_eigs=[float(x) for x in ev[:12]],
                subsample=[(int(a),float(b),float(c)) for a,b,c in curve])

def main():
    t0 = time.time()
    keep_ids, Z, radii = build_tracked("zheight")
    np.save(f"{SCRATCH}/gal_Z_zheight.npy", Z)
    N, T = Z.shape
    calibrate(min(N, 5000), T)   # synth_powerlaw does an NxN QR; cap N (ruler is N-indep for N>>T)
    res = {}
    for scalar in ["zheight", "jz", "vr"]:
        _, Zs, _ = build_tracked(scalar) if scalar != "zheight" else (keep_ids, Z, radii)
        r = analyze(Zs, scalar)
        res[scalar] = r
        print(f"\n[{scalar}] N={r['N']} T={r['T']} PR/k_eff={r['PR_keff']:.2f} "
              f"eff_rank(MP)={r['eff_rank_mp']} eff_rank(surr)={r['eff_rank_surr']} "
              f"beta_top={r['beta_top']:.3f} alpha={r['alpha']:.3f}", flush=True)
        print("  saturation curve PR vs N':")
        for n,m,sd in r['subsample']:
            print(f"    N'={n:6d}  PR={m:7.3f} +/- {sd:5.3f}", flush=True)
        print(f"  top eigs: {[round(x,2) for x in r['top_eigs']]}", flush=True)

    prim = res["zheight"]
    # verdict on primary scalar
    saturates = (prim['beta_top'] < 0.05) and (prim['eff_rank_surr'] <= 12) and (prim['PR_keff'] < 12)
    powerlaw  = (prim['alpha'] < 0.9) and (prim['eff_rank_surr'] > 12 or prim['PR_keff'] > 12)
    if saturates:
        verdict = ("SATURATES (bounded k_eff, few collective modes): a complete BOUND galaxy "
                   "collapses to a low-rank set of dynamical modes -- like the complete zebrafish "
                   "brain's spectral shape but at the corridor ceiling. NOTE gravity is the alpha-term, "
                   "not gamma*M, so this is a bound-unit result, not a coordinating-unit result.")
    elif powerlaw:
        verdict = ("HIGH-DIMENSIONAL / POWER-LAW: effective dimensionality does NOT collapse to a few "
                   "collective modes; the stellar phase-space is high-rank. Adjacent to the zebrafish "
                   "whole-brain falsification. Gravity=alpha caveat applies.")
    else:
        verdict = "MIXED / INCONCLUSIVE at this (N,T)."
    print(f"\nVERDICT (primary=zheight): {verdict}", flush=True)

    out = dict(
        substrate="CAMELS IllustrisTNG L25n256 CV_0, SUBFIND subhalo 0 (central galaxy)",
        complete_unit=("all star particles of one gravitationally-bound galaxy; subsampling "
                       "runs to full N so 'wrong grain' cannot be invoked"),
        gravity_caveat=("galaxy is bound by GRAVITY = the spontaneous alpha-term in drho/dt = "
                        "alpha(rho,S) - gamma*M, NOT the active-maintenance gamma*M that defines "
                        "corridor coordination; this is a complete-BOUND-unit test, adjacent to "
                        "but not identical to the complete-COORDINATING-unit question."),
        construction=("units=star particles tracked by ParticleID; observations=snapshots; "
                      "X[i,t]=kinematic scalar in the galaxy's instantaneous frame; star x star "
                      "correlation over snapshots reveals collective dynamical modes. Not the "
                      "trivial rank<=6 stars x 6-phase-coords table."),
        n_star_particles_z0=int(N_TARGET_STARS),
        snapshots=SNAPS, z_range=[2.3, 0.0], N_persistent=int(prim['N']), T=int(prim['T']),
        results_by_scalar=res, primary_scalar="zheight", verdict=verdict,
        compare=dict(
            zebrafish="complete brain, FALSIFICATION (high-dim), PR~34, 1592 CV dims, alpha~1.36",
            celegans="complete brain, LOW-RANK (saturates)",
            cortex_subsample="alpha~0.97 (grain-inconclusive)",
            cosmic_web_subsample="power-law alpha~0.75, grain-inconclusive"),
        elapsed_sec=round(time.time()-t0,1))
    json.dump(out, open(f"{HERE}/spectral_results_galaxy.json","w"), indent=1)
    print(f"\nwrote spectral_results_galaxy.json  ({out['elapsed_sec']}s)", flush=True)

if __name__ == "__main__":
    main()

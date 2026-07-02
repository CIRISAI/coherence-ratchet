#!/usr/bin/env python3
"""
ADVERSARIAL breadth test on the criticality camp's FLAGSHIP living system:
collective animal motion. Wild midge swarms (Attanasi, Cavagna et al., PNAS 2014,
"Collective behaviour without collective order in wild swarms of midges") and
starling flocks (Cavagna et al., PNAS 2010, "Scale-free correlations in starling
flocks") are THE canonical "scale-free correlations in a living system" results:
the velocity-fluctuation correlation length grows with group size -> the signature
of self-organized criticality.

DATA: Sinhuber, van der Vaart, Ni, Puckett, Kelley, Ouellette (2019),
"Three-dimensional time-resolved trajectories from laboratory insect swarms",
figshare doi:10.6084/m9.figshare.11546013. Laboratory swarms of the non-biting
midge Chironomus riparius, tracked in 3D at 100 Hz. Columns: id,t,x,y,z,vx,vy,vz.
We use UNPERTURBED takes (the pure spontaneous-coordination signal). A complete
swarm at an instant is a COMPLETE UNIT -- no grain escape -- so this is a clean
adversarial test on the criticality camp's home turf.

TWO OBSERVABLES (distinct, both reported):

(A) COVARIANCE SATURATION (the RATCHET discriminator). Build individuals x time of
    the VELOCITY FLUCTUATION delta_v_i = v_i - <v>_swarm (subtract bulk swarm
    translation; the coordination signal is the fluctuation, not the drift). Form
    the N x N correlation matrix of the (3-vector) fluctuation time series across
    co-present individuals; ask whether its effective rank / participation ratio
    SATURATES (bounded, low-rank) or grows with N (scale-free). NOTE: lab swarms
    hold only ~10-15 midges co-present at once, so subsampling leverage is small;
    the ABSOLUTE k_eff vs N is the readout here.

(B) CORRELATION LENGTH vs GROUP SIZE (Cavagna's ACTUAL observable -- a SPATIAL
    quantity, RELATED TO BUT NOT identical to the covariance eigenspectrum PR).
    Per frame: dimensionless fluctuation phi_i = delta_v_i / sqrt(<|delta_v|^2>);
    connected correlation C(r) = <phi_i . phi_j>_{r_ij=r}; correlation length
    xi = first zero crossing of C(r) (Cavagna's definition). Scale-free/critical
    prediction: xi grows ~linearly with system size L. Bounded prediction: xi
    saturates to a fixed value independent of L.

(C) DETAILED BALANCE. A swarm is actively self-propelled = far from equilibrium
    -> expect broken detailed balance (the coordinating signature). Winding-based
    irreversibility on the swarm's collective velocity modes.

Real data only. No fabricated trajectories.
"""
import numpy as np, pandas as pd, json, os, glob
from entropy_production import irreversibility_from_units

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(0)
TAKES = sorted(glob.glob(os.path.join(HERE, "flock_data", "take_*_unperturbed.csv")))

# ----------------------------------------------------------------------------
# shared spectral helpers (mirror spectral_test.py; adapted to 3-vector units)
# ----------------------------------------------------------------------------
def participation_ratio(ev):
    ev = np.clip(ev, 0, None)
    return (ev.sum() ** 2) / (ev ** 2).sum()

def fluct_corr_matrix(V):
    """V: N x T x 3 velocity-fluctuation array (mean over individuals already
    removed per frame). Return N x N correlation matrix of the flattened (T*3)
    per-individual fluctuation vectors, each individual L2-normalized (so diag=1,
    off-diag in [-1,1]) -- the multi-component analogue of a Pearson correlation
    across units. Eigenvalues of this matrix give the effective number of
    collective velocity modes."""
    N = V.shape[0]
    D = V.reshape(N, -1)                       # N x (T*3)
    D = D - D.mean(1, keepdims=True)
    nrm = np.linalg.norm(D, axis=1, keepdims=True)
    D = D / (nrm + 1e-12)
    C = D @ D.T
    return C

def corr_eig(V):
    C = fluct_corr_matrix(V)
    ev = np.linalg.eigvalsh(C)[::-1]
    return np.clip(ev, 0, None)

def phase_randomize_V(V):
    """Phase-randomize each individual's each velocity component independently
    -> destroys cross-individual coordination, preserves each unit's own power
    spectrum. Surrogate null for 'no collective structure'."""
    N, T, d = V.shape
    out = np.empty_like(V)
    F = np.fft.rfft(V, axis=1)
    ph = np.exp(1j * RNG.uniform(0, 2*np.pi, F.shape))
    ph[:, 0, :] = 1
    out = np.fft.irfft(F * ph, n=T, axis=1)
    return out

def subsample_pr(V, sizes, ndraw=60):
    N = V.shape[0]
    out = []
    for n in sizes:
        if n > N: continue
        prs = []
        for _ in range(ndraw):
            idx = RNG.choice(N, n, replace=False)
            prs.append(participation_ratio(corr_eig(V[idx])))
        out.append((n, float(np.mean(prs)), float(np.std(prs))))
    return out

# ----------------------------------------------------------------------------
# window builder: largest set of midges co-present over a window
# ----------------------------------------------------------------------------
def load_take(path):
    df = pd.read_csv(path)
    ts = np.sort(df.t.unique())
    tindex = {t: i for i, t in enumerate(ts)}
    df["fi"] = df.t.map(tindex)
    return df, ts

def best_copresent(df, ts, W, step=None):
    from collections import defaultdict
    idset = defaultdict(set)
    for idd, fi in zip(df.id.values, df.fi.values):
        idset[idd].add(int(fi))
    nfr = len(ts); step = step or max(1, W // 5)
    best = (0, None)
    for s in range(0, nfr - W, step):
        want = set(range(s, s + W))
        ids = [idd for idd, fr in idset.items() if fr.issuperset(want)]
        if len(ids) > best[0]:
            best = (len(ids), (s, ids))
    return best[1]  # (start_frame, id_list)

def window_matrix(df, s, W, ids):
    """Return V: N x W x 3 velocity FLUCTUATION (per-frame swarm mean removed)."""
    sub = df[(df.fi >= s) & (df.fi < s + W) & (df.id.isin(ids))]
    ids = sorted(ids)
    idx = {i: k for k, i in enumerate(ids)}
    V = np.full((len(ids), W, 3), np.nan)
    for r in sub.itertuples():
        V[idx[r.id], int(r.fi) - s] = (r.vx, r.vy, r.vz)
    # per-frame swarm-mean velocity removed (subtract bulk translation)
    mean = np.nanmean(V, axis=0, keepdims=True)
    return V - mean

# ----------------------------------------------------------------------------
# (B) Cavagna correlation length xi per frame + xi-vs-size scaling
# ----------------------------------------------------------------------------
def frame_corr_length(pos, vel, nbins=12):
    """pos: n x 3, vel: n x 3 for one frame. Returns (xi, L, n) using Cavagna's
    connected correlation C(r) = <phi_i.phi_j> at separation r, phi the
    dimensionless velocity fluctuation; xi = first zero crossing of C(r)."""
    n = len(pos)
    if n < 6: return None
    dv = vel - vel.mean(0)
    m = np.sqrt((dv ** 2).sum(1).mean())        # sqrt<|dv|^2>
    if m < 1e-9: return None
    phi = dv / m
    # pairwise
    iu = np.triu_indices(n, 1)
    rij = np.linalg.norm(pos[iu[0]] - pos[iu[1]], axis=1)
    cij = (phi[iu[0]] * phi[iu[1]]).sum(1)
    L = rij.max()
    # bin C(r)
    edges = np.linspace(0, L, nbins + 1)
    ctr = 0.5 * (edges[:-1] + edges[1:])
    Cr = np.full(nbins, np.nan)
    for b in range(nbins):
        m2 = (rij >= edges[b]) & (rij < edges[b + 1])
        if m2.sum() >= 3:
            Cr[b] = cij[m2].mean()
    # first zero crossing of C(r) (from small r, where C>0, to first sign change)
    valid = ~np.isnan(Cr)
    rr = ctr[valid]; cc = Cr[valid]
    xi = np.nan
    for k in range(1, len(cc)):
        if cc[k - 1] > 0 and cc[k] <= 0:
            # linear interp of zero crossing
            xi = rr[k - 1] + (rr[k] - rr[k - 1]) * cc[k - 1] / (cc[k - 1] - cc[k])
            break
    if np.isnan(xi) and len(cc) and cc[0] <= 0:
        xi = rr[0]
    return (xi, L, n)

def correlation_length_scaling(df, ts, max_frames=4000):
    """Compute (xi, L, n) over many frames; regress xi vs L (and xi vs n)."""
    rows = []
    fis = np.linspace(0, len(ts) - 1, min(max_frames, len(ts))).astype(int)
    g = df.groupby("fi")
    for fi in fis:
        try:
            sub = g.get_group(fi)
        except KeyError:
            continue
        pos = sub[["x", "y", "z"]].values
        vel = sub[["vx", "vy", "vz"]].values
        out = frame_corr_length(pos, vel)
        if out and np.isfinite(out[0]):
            rows.append(out)
    return np.array(rows)  # cols: xi, L, n

# ----------------------------------------------------------------------------
# synthetic calibration of observable (A): does the pipeline separate a
# genuinely low-dimensional collective field from a scale-free one?
# ----------------------------------------------------------------------------
def calib_lowrank(N, T, r=3, snr=3.0):
    F = RNG.standard_normal((r, T, 3))
    W = RNG.standard_normal((N, r))
    V = np.einsum("nr,rtd->ntd", W, F) + snr ** -1 * RNG.standard_normal((N, T, 3))
    return V - V.mean(0, keepdims=True)

def calib_independent(N, T):
    V = RNG.standard_normal((N, T, 3))
    return V - V.mean(0, keepdims=True)

def calibrate():
    print("=== CALIBRATION of observable (A) on synthetic collective fields ===")
    N, T = 15, 200
    for name, V in [("low-rank r=3 (bounded)", calib_lowrank(N, T)),
                    ("independent (extensive)", calib_independent(N, T))]:
        ev = corr_eig(V); pr = participation_ratio(ev)
        Vs = phase_randomize_V(V); evs = corr_eig(Vs)
        eff = int((ev > evs.max()).sum())
        print(f"  {name:26s}: N={N} PR={pr:5.2f} eff_rank={eff:2d} top3={ev[:3].round(2)}")
    print("  (expect: low-rank PR~3 eff_rank~3 ; independent PR~N eff_rank~0)\n")

# ----------------------------------------------------------------------------
def main():
    calibrate()
    results = {"dataset": "Chironomus riparius lab midge swarms (Sinhuber/Ouellette 2019, "
               "figshare 11546013), unperturbed takes", "takes": []}
    print(f"{'take':6s} {'N':>3s} {'W':>4s} {'PR':>5s} {'effR':>4s} {'surrPR':>6s} "
          f"{'beta':>6s} {'xi/L':>6s} {'xiL_r':>6s} {'DBz':>6s} {'nfr_xi':>6s}")
    for path in TAKES:
        take = os.path.basename(path).split("_")[1]
        df, ts = load_take(path)

        # ---- (A) covariance saturation on best co-present window ----
        W = 200
        win = best_copresent(df, ts, W)
        if win is None:
            continue
        s, ids = win
        V = window_matrix(df, s, W, ids)
        # drop any individual with residual NaN (shouldn't happen for full-presence)
        good = ~np.isnan(V).any(axis=(1, 2))
        V = V[good]
        N = V.shape[0]
        ev = corr_eig(V); pr = participation_ratio(ev)
        Vs = phase_randomize_V(V); evs = corr_eig(Vs)
        eff_rank = int((ev > evs.max()).sum())
        surr_pr = participation_ratio(evs)
        sizes = [n for n in [4, 5, 6, 8, 10, 12, 14, 16, 18, 20] if n <= N]
        curve = subsample_pr(V, sizes) if N >= 8 else []
        if len(curve) >= 3:
            cn = np.array([c[0] for c in curve]); cp = np.array([c[1] for c in curve])
            beta = float(np.polyfit(np.log10(cn), np.log10(cp), 1)[0])
        else:
            beta = np.nan

        # ---- (B) correlation length scaling ----
        cl = correlation_length_scaling(df, ts)
        xiL_ratio = xiL_r = np.nan
        n_xi = len(cl)
        if n_xi >= 30:
            xi, L, ncnt = cl[:, 0], cl[:, 1], cl[:, 2]
            xiL_ratio = float(np.median(xi / L))
            # regress xi on L across frames (Cavagna's scale-free test: slope>0, xi~L)
            if np.ptp(L) > 1e-6:
                xiL_r = float(np.corrcoef(L, xi)[0, 1])

        # ---- (C) detailed balance on collective velocity modes ----
        # top swarm velocity-fluctuation modes over the whole take (co-present window
        # units x time), reuse window V flattened to units x (T*3) -> mode traj.
        Xunits = V.reshape(N, -1)
        try:
            db = irreversibility_from_units(Xunits, k=4)
            dbz = float(db["z"])
        except Exception:
            dbz = np.nan

        rec = dict(take=take, N=int(N), W=W, PR=float(pr), eff_rank=eff_rank,
                   surr_PR=float(surr_pr), beta_sub=beta,
                   xi_over_L_median=xiL_ratio, xi_vs_L_corr=xiL_r,
                   n_frames_xi=int(n_xi),
                   xi_median=float(np.median(cl[:, 0])) if n_xi else None,
                   L_range=[float(cl[:, 1].min()), float(cl[:, 1].max())] if n_xi else None,
                   n_range=[int(cl[:, 2].min()), int(cl[:, 2].max())] if n_xi else None,
                   db_z=dbz, top_eigs=[float(x) for x in ev[:6]], subsample=curve)
        results["takes"].append(rec)
        print(f"{take:>6s} {N:3d} {W:4d} {pr:5.2f} {eff_rank:4d} {surr_pr:6.2f} "
              f"{beta:6.3f} {xiL_ratio:6.3f} {xiL_r:6.3f} {dbz:6.2f} {n_xi:6d}")

    # ---- pooled correlation-length scaling across ALL frames of ALL takes ----
    print("\n=== POOLED xi-vs-size scaling (Cavagna's flagship observable) ===")
    allcl = []
    for path in TAKES:
        df, ts = load_take(path)
        cl = correlation_length_scaling(df, ts)
        if len(cl): allcl.append(cl)
    allcl = np.vstack(allcl)
    xi, L, n = allcl[:, 0], allcl[:, 1], allcl[:, 2]
    # log-log slope xi ~ L^a ; a~1 scale-free/critical, a~0 bounded/saturating
    a_L = float(np.polyfit(np.log10(L), np.log10(np.clip(xi, 1e-6, None)), 1)[0])
    a_n = float(np.polyfit(np.log10(n), np.log10(np.clip(xi, 1e-6, None)), 1)[0])
    r_L = float(np.corrcoef(np.log10(L), np.log10(np.clip(xi, 1e-6, None)))[0, 1])
    print(f"  frames pooled: {len(allcl)}   L range [{L.min():.1f},{L.max():.1f}] mm   "
          f"n range [{int(n.min())},{int(n.max())}]")
    print(f"  xi/L median = {np.median(xi/L):.3f}")
    print(f"  log-log slope  d log xi / d log L = {a_L:.3f}  (r={r_L:.3f})   "
          f"[~1 => scale-free/critical ; ~0 => bounded]")
    print(f"  log-log slope  d log xi / d log n = {a_n:.3f}")
    results["pooled_xi_scaling"] = dict(
        n_frames=int(len(allcl)),
        L_range=[float(L.min()), float(L.max())],
        n_range=[int(n.min()), int(n.max())],
        xi_over_L_median=float(np.median(xi / L)),
        slope_logxi_logL=a_L, corr_logxi_logL=r_L, slope_logxi_logn=a_n,
        xi_median=float(np.median(xi)))

    # ---- overall verdict inputs (observable A) ----
    prs = np.array([t["PR"] for t in results["takes"]])
    effs = np.array([t["eff_rank"] for t in results["takes"]])
    Ns = np.array([t["N"] for t in results["takes"]])
    betas = np.array([t["beta_sub"] for t in results["takes"] if np.isfinite(t["beta_sub"])])
    dbz = np.array([t["db_z"] for t in results["takes"] if np.isfinite(t["db_z"])])
    print("\n=== VERDICT INPUTS (observable A: velocity-fluctuation covariance) ===")
    print(f"  n takes = {len(results['takes'])}, co-present N range {Ns.min()}-{Ns.max()}")
    print(f"  PR (k_eff): median {np.median(prs):.2f}  vs mean N {Ns.mean():.1f}  "
          f"-> k_eff/N = {np.median(prs)/Ns.mean():.2f}")
    print(f"  effective rank above surrogate: median {np.median(effs):.1f}, range {effs.min()}-{effs.max()}")
    if len(betas):
        print(f"  subsampling beta: mean {betas.mean():.3f} +/- {betas.std():.3f} (n={len(betas)}) "
              f"[limited leverage, N<=~15]")
    print(f"  detailed balance |z|: median {np.median(np.abs(dbz)):.2f}  "
          f"[|z|>>2 => broken DB = actively coordinating]")
    results["verdict_inputs"] = dict(
        n_takes=len(results["takes"]),
        N_range=[int(Ns.min()), int(Ns.max())],
        PR_median=float(np.median(prs)), N_mean=float(Ns.mean()),
        keff_over_N=float(np.median(prs) / Ns.mean()),
        eff_rank_median=float(np.median(effs)),
        eff_rank_range=[int(effs.min()), int(effs.max())],
        beta_mean=float(betas.mean()) if len(betas) else None,
        beta_std=float(betas.std()) if len(betas) else None,
        db_absz_median=float(np.median(np.abs(dbz))) if len(dbz) else None)

    out = os.path.join(HERE, "spectral_results_flocks.json")
    json.dump(results, open(out, "w"), indent=1)
    print(f"\nwrote {out}")

if __name__ == "__main__":
    main()

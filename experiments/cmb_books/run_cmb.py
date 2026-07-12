"""Bet 11 -- low-ell CMB anomalies vs the ledger battery (frozen REGISTRATION.md, incl. the
pre-data S_logdet amendment). One functional battery on the Planck sky vs an isotropic Gaussian
null ensemble; joint depth statistics; look-elsewhere computed ON THE ENSEMBLE.

Data: Planck 2018 SMICA full-sky CMB temperature (I_STOKES, K_CMB, Galactic, Nside=2048).
Null : isotropic Gaussian skies from the Planck best-fit LCDM TT spectrum. 100k, seeded.

CPU only. Incremental flush. The null ensemble is the METHOD (labelled synthetic), not data.
Registration is the sole scorer; this script computes, it does not re-adjudicate.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")               # 1 BLAS thread/worker; parallelism is over realizations
import json, time
import numpy as np
import healpy as hp
from multiprocessing import Pool

NPROC = int(os.environ.get("CMB_NPROC", "14"))

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "results.json")
NPZ = os.path.join(HERE, "null_battery.npz")

LMAX = 60                      # generate to 60; batteries assembled at ell_max in {10,30,60}
ELLMAXES = [10, 30, 60]
PRIMARY = 30
N_NULL = 100_000
SEED = 20260711
NSIDE_HEMI = 64                # A_hemi map resolution (registration)
NSIDE_AXES = 8                 # 768 hemisphere axes AND S_logdet direction grid (registration)
CHUNK_FLUSH = 5000

# tail direction per marginal for the look-elsewhere union (registration section 4)
TAIL = dict(align_23="U", A_hemi="U", S_half="L", Q_amp="L",
            axis_conc="U", S_logdet="U", pr_lowell="L")
VEC = ["align_23", "A_hemi", "S_half", "Q_amp", "axis_conc", "S_logdet", "pr_lowell"]

# ----------------------------------------------------------------------------- theory spectrum
def load_theory_cl(lmax):
    """Planck best-fit LCDM: file columns L, TT(=D_ell=l(l+1)C_l/2pi, uK^2), ..."""
    arr = np.loadtxt(os.path.join(DATA, "planck_bestfit_theory.txt"))
    L = arr[:, 0].astype(int); DTT = arr[:, 1]
    cl = np.zeros(lmax + 1)
    for l, d in zip(L, DTT):
        if 2 <= l <= lmax:
            cl[l] = d * 2 * np.pi / (l * (l + 1))
    return cl                                     # uK^2, cl[0]=cl[1]=0


# --------------------------------------------------------------- angular-momentum operators / ell
def L_operators(l):
    """L_x,L_y,L_z in the |l,m> basis, m ordered -l..+l (dim 2l+1). Complex."""
    ms = np.arange(-l, l + 1)
    d = 2 * l + 1
    Lz = np.diag(ms.astype(complex))
    Lp = np.zeros((d, d), complex); Lm = np.zeros((d, d), complex)
    for i, m in enumerate(ms):
        if m + 1 <= l:
            Lp[i + 1, i] = np.sqrt(l * (l + 1) - m * (m + 1))     # L+ |m> -> |m+1>
        if m - 1 >= -l:
            Lm[i - 1, i] = np.sqrt(l * (l + 1) - m * (m - 1))     # L- |m> -> |m-1>
    Lx = 0.5 * (Lp + Lm)
    Ly = (Lp - Lm) / (2j)
    return Lx, Ly, Lz


def preferred_axis(a_full, Lops):
    """de Oliveira-Costa AMD axis: n maximizing <a|(n.L)^2|a> = top eigvec of the symmetric
    3x3 M_ij = Re<a| (Li Lj + Lj Li)/2 |a>.  a_full: complex, m=-l..+l."""
    Lx, Ly, Lz = Lops
    Ls = [Lx, Ly, Lz]
    M = np.empty((3, 3))
    La = [Lk @ a_full for Lk in Ls]
    for i in range(3):
        for j in range(i, 3):
            M[i, j] = M[j, i] = np.real(np.vdot(La[i], La[j]))   # <a|Li Lj|a>, symmetrized by (i,j)+(j,i)/2 = Re for Hermitian
    w, V = np.linalg.eigh(M)
    return V[:, -1]                                # unit preferred axis


def synalm_local(cl, lmax, rng):
    """Reproducible isotropic-Gaussian alm from C_l (healpy convention), local Generator.
    E|a_l0|^2 = C_l (real); E|a_lm|^2 = C_l for m>0 (Re,Im each var C_l/2)."""
    nalm = hp.Alm.getsize(lmax)
    alm = np.zeros(nalm, complex)
    for l in range(2, lmax + 1):
        s = np.sqrt(cl[l])
        if s == 0:
            continue
        alm[hp.Alm.getidx(lmax, l, 0)] = s * rng.standard_normal()
        for m in range(1, l + 1):
            alm[hp.Alm.getidx(lmax, l, m)] = s / np.sqrt(2) * (rng.standard_normal() + 1j * rng.standard_normal())
    return alm


# ------------------------------------------------------------------- per-realization alm objects
class Battery:
    def __init__(self):
        self.Lops = {l: L_operators(l) for l in range(2, LMAX + 1)}
        self.idx0 = {l: hp.Alm.getidx(LMAX, l, 0) for l in range(2, LMAX + 1)}
        self.idxm = {l: [hp.Alm.getidx(LMAX, l, m) for m in range(0, l + 1)]
                     for l in range(2, LMAX + 1)}
        # S_logdet design: real & imag response of each (l,m>=0) coeff on the NSIDE_AXES grid
        self.npix_ax = hp.nside2npix(NSIDE_AXES)
        nalm = hp.Alm.getsize(LMAX)
        Cr = np.zeros((self.npix_ax, nalm)); Ci = np.zeros((self.npix_ax, nalm))
        for l in range(2, LMAX + 1):
            for m in range(0, l + 1):
                k = hp.Alm.getidx(LMAX, l, m)
                e = np.zeros(nalm, complex); e[k] = 1.0
                Cr[:, k] = hp.alm2map(e, NSIDE_AXES, lmax=LMAX)
                e[k] = 1.0j
                Ci[:, k] = hp.alm2map(e, NSIDE_AXES, lmax=LMAX)
        self.Cr, self.Ci = Cr, Ci
        # ell-grouping matrix G (nalm x (LMAX-1)): G[k, l-2]=1 if idx k belongs to ell=l
        G = np.zeros((nalm, LMAX - 1), np.float32)
        for l in range(2, LMAX + 1):
            for k in self.idxm[l]:
                G[k, l - 2] = 1.0
        self.G = G
        # hemisphere geometry at NSIDE_HEMI, axes at NSIDE_AXES
        vpix = np.array(hp.pix2vec(NSIDE_HEMI, np.arange(hp.nside2npix(NSIDE_HEMI)))).T  # (Npix,3)
        vax = np.array(hp.pix2vec(NSIDE_AXES, np.arange(self.npix_ax))).T                # (Naxes,3)
        self.hemif = ((vpix @ vax.T) > 0).astype(np.float32)   # (Npix, Naxes): pixel in +axis hemisphere
        self.nhemi = self.hemif.sum(0).astype(float)           # (Naxes,) count per +hemisphere

    def full_alm(self, alm, l):
        """complex a_{l,m} for m=-l..+l from healpy alm (real field)."""
        pos = alm[self.idxm[l]]                    # m=0..l
        neg = ((-1.0) ** np.arange(1, l + 1)) * np.conj(pos[1:])[::-1]  # m=-l..-1
        return np.concatenate([neg, pos])

    def compute(self, alm):
        """Return dict[ell_max] -> battery vector. alm generated to LMAX."""
        # per-l primitives at LMAX
        cl = hp.alm2cl(alm, lmax=LMAX)             # Chat_l = (1/(2l+1)) sum_m |a_lm|^2
        axes = {}; PRl = {}
        # per-l maps on the axis grid, for S_logdet power maps
        re = np.real(alm); im = np.imag(alm)
        for l in range(2, LMAX + 1):
            af = self.full_alm(alm, l)
            axes[l] = preferred_axis(af, self.Lops[l])
            # real-component power participation ratio (Galactic frame)
            a0 = np.real(alm[self.idx0[l]])
            amp = alm[self.idxm[l][1:]]            # m=1..l
            x = np.concatenate([[a0], np.sqrt(2) * np.real(amp), np.sqrt(2) * np.imag(amp)])
            s2 = np.sum(x ** 2); s4 = np.sum(x ** 4)
            PRl[l] = (s2 * s2 / s4) / (2 * l + 1)  # in [~0,1]; 1 = spread evenly over 2l+1 modes
        # per-l field maps on axis grid via design + grouping matrix (vectorized): (Naxes, LMAX-1)
        mmap_all = (self.Cr * re[None, :]) @ self.G + (self.Ci * im[None, :]) @ self.G
        pow_all = mmap_all ** 2                     # per-l POWER maps p_l = m_l^2, columns l=2..LMAX
        out = {}
        for LM in ELLMAXES:
            ls = list(range(2, LM + 1))
            # align_23
            a23 = abs(float(axes[2] @ axes[3]))
            # A_hemi: map from l=2..LM at NSIDE_HEMI
            alm_lm = hp.almxfl(alm.copy(), np.array([1.0 if l <= LM else 0.0 for l in range(LMAX + 1)]))
            hmap = hp.alm2map(alm_lm, NSIDE_HEMI, lmax=LMAX).astype(np.float32)
            n = self.nhemi                                 # (Naxes,)
            hmap2 = hmap ** 2
            s1 = hmap @ self.hemif; s2 = hmap2 @ self.hemif
            nc = len(hmap) - n; s1c = hmap.sum() - s1; s2c = hmap2.sum() - s2
            varp = s2 / n - (s1 / n) ** 2
            varm = s2c / nc - (s1c / nc) ** 2
            asym = (varp - varm) / (varp + varm)
            A_hemi = float(np.max(np.abs(asym)))
            # S_half: C(theta)= sum (2l+1)/4pi Chat_l P_l(cos th), integral of C^2 over cos th in [-1,1/2]
            S_half = self._s_half(cl, LM)
            # Q_amp: quadrupole power
            Q_amp = float(2 * 3 * cl[2] / (2 * np.pi))
            # axis_conc: lambda_max of weighted axis dyadic
            w = np.array([(2 * l + 1) * cl[l] for l in ls]); w = w / w.sum()
            T = np.zeros((3, 3))
            for wl, l in zip(w, ls):
                T += wl * np.outer(axes[l], axes[l])
            axis_conc = float(np.linalg.eigvalsh(T)[-1])
            # S_logdet: -ln det of correlation of per-l POWER maps p_l = m_l^2 across axis grid
            P = pow_all[:, :LM - 1]                           # columns l=2..LM
            Pc = P - P.mean(0)
            sd = Pc.std(0); sd[sd < 1e-30] = 1e-30
            Ccorr = (Pc / sd).T @ (Pc / sd) / P.shape[0]
            sign, logdet = np.linalg.slogdet(Ccorr)
            S_logdet = float(-logdet) if sign > 0 else float("nan")
            # pr_lowell
            pr_lowell = float(np.mean([PRl[l] for l in ls]))
            out[LM] = dict(align_23=a23, A_hemi=A_hemi, S_half=float(S_half), Q_amp=Q_amp,
                           axis_conc=axis_conc, S_logdet=S_logdet, pr_lowell=pr_lowell)
        return out

    _pl_cache = {}
    def _s_half(self, cl, LM):
        # Gauss-Legendre in cos(theta) over [-1, 1/2]; C(theta)=sum (2l+1)/4pi Chat_l P_l(x)
        key = LM
        if key not in self._pl_cache:
            x, wq = np.polynomial.legendre.leggauss(256)      # on [-1,1]
            # rescale nodes to [-1, 1/2]
            a, b = -1.0, 0.5
            xs = 0.5 * (b - a) * x + 0.5 * (b + a); ws = 0.5 * (b - a) * wq
            Pl = np.array([np.polynomial.legendre.Legendre.basis(l)(xs) for l in range(LM + 1)])
            self._pl_cache[key] = (xs, ws, Pl)
        xs, ws, Pl = self._pl_cache[key]
        coef = np.array([(2 * l + 1) / (4 * np.pi) * cl[l] for l in range(LM + 1)])
        Ct = coef @ Pl                                        # C(theta) at nodes
        return float(np.sum(ws * Ct ** 2))


# --------------------------------------------------------------------------------- depth helpers
def _ppf(p):
    p = np.asarray(p, float)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    x = np.empty_like(p); lo = p < plow; hi = p > phigh; mid = ~(lo | hi)
    q = np.sqrt(-2 * np.log(p[lo]))
    x[lo] = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = np.sqrt(-2 * np.log(1 - p[hi]))
    x[hi] = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p[mid] - 0.5; r = q * q
    x[mid] = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    return x


def chi2_cdf(x, k):
    from scipy.stats import chi2
    return float(chi2.cdf(x, k))


def depths(null, data):
    """null: (N,7) ; data: (7,).  Returns the three outlyingness percentiles + aux."""
    mu = null.mean(0); Sig = np.cov(null, rowvar=False); Sinv = np.linalg.pinv(Sig)
    D2n = np.einsum("ij,jk,ik->i", null - mu, Sinv, null - mu)
    d = data - mu; D2d = float(d @ Sinv @ d)
    maha_pct = float(100 * np.mean(D2n < D2d))
    # normal-scores rank Mahalanobis
    N = null.shape[0]
    NS = np.empty_like(null)
    for j in range(null.shape[1]):
        order = np.argsort(np.argsort(null[:, j]))
        NS[:, j] = _ppf((order + 0.5) / N)
    mu2 = NS.mean(0); S2 = np.cov(NS, rowvar=False); Si2 = np.linalg.pinv(S2)
    D2ns = np.einsum("ij,jk,ik->i", NS - mu2, Si2, NS - mu2)
    zd = np.empty(null.shape[1])
    for j in range(null.shape[1]):
        u = (np.mean(null[:, j] < data[j]) * N + 0.5) / N
        u = min(max(u, 0.5 / N), 1 - 0.5 / N); zd[j] = _ppf(np.array([u]))[0]
    D2nsd = float((zd - mu2) @ Si2 @ (zd - mu2))
    ns_pct = float(100 * np.mean(D2ns < D2nsd))
    # spatial (L1) depth on subsample, standardized
    rng = np.random.default_rng(101); scl = null.std(0); scl[scl < 1e-30] = 1e-30
    ref = null[rng.choice(N, min(8000, N), replace=False)] / scl
    def sdepth(row):
        diff = row - ref; nrm = np.linalg.norm(diff, axis=1); nrm[nrm < 1e-12] = 1e-12
        return 1.0 - np.linalg.norm((diff / nrm[:, None]).mean(0))
    nullsub = null[rng.choice(N, min(6000, N), replace=False)] / scl
    dnull = np.array([sdepth(r) for r in nullsub])
    dd = sdepth(data / scl)
    sp_pct = float(100 * np.mean(dnull > dd))     # low depth = outlier -> high pct
    return dict(mahalanobis_D2=D2d, mahalanobis_pct=maha_pct,
                mahalanobis_chi2_pct=100 * chi2_cdf(D2d, null.shape[1]),
                normalscores_pct=ns_pct, spatial_pct=sp_pct)


# ---------------------------------------------------------------------------- parallel null draw
_BAT = None
_CL = None


def _worker(idx):
    rng = np.random.default_rng(np.random.SeedSequence([SEED, idx]))
    alm = synalm_local(_CL, LMAX, rng)
    b = _BAT.compute(alm)
    return idx, np.array([[b[LM][k] for k in VEC] for LM in ELLMAXES])   # (nELL, 7)


# ------------------------------------------------------------------------------------------- run
def main():
    t0 = time.time()
    cl = load_theory_cl(LMAX)
    bat = Battery()
    print(f"[{time.time()-t0:.0f}s] battery init done (design matrices built)", flush=True)

    global _BAT, _CL
    _BAT, _CL = bat, cl

    # ---- DATA ----
    m = hp.read_map(os.path.join(DATA, "smica_2048.fits"), field=0, nest=False) * 1e6  # -> uK, RING
    alm_d = hp.map2alm(m, lmax=LMAX, use_pixel_weights=False)
    data_bat = bat.compute(alm_d)
    print(f"[{time.time()-t0:.0f}s] data battery: {json.dumps({str(k): {kk: round(vv,4) for kk,vv in v.items()} for k,v in data_bat.items()})}", flush=True)

    # ---- NULL ENSEMBLE (parallel, per-index reproducible seeds, resumable) ----
    nELL = len(ELLMAXES)
    if os.path.exists(NPZ):
        z = np.load(NPZ); null = z["null"]        # (N, nELL, 7)
        print(f"[{time.time()-t0:.0f}s] resumed null from npz", flush=True)
    else:
        null = np.full((N_NULL, nELL, len(VEC)), np.nan)
    todo = [i for i in range(N_NULL) if not np.isfinite(null[i, -1, 0])]
    print(f"[{time.time()-t0:.0f}s] null todo={len(todo)} of {N_NULL} on {NPROC} procs", flush=True)
    if todo:
        with Pool(NPROC) as pool:
            done = 0
            for idx, row in pool.imap_unordered(_worker, todo, chunksize=64):
                null[idx] = row; done += 1
                if done % CHUNK_FLUSH == 0:
                    np.savez(NPZ, null=null)
                    print(f"[{time.time()-t0:.0f}s] null {done}/{len(todo)}", flush=True)
        np.savez(NPZ, null=null)
    null = {LM: null[:, i, :] for i, LM in enumerate(ELLMAXES)}
    print(f"[{time.time()-t0:.0f}s] null complete", flush=True)

    # ---- SCORING ----
    res = {"n_null": N_NULL, "seed": SEED, "vec": VEC, "primary_ellmax": PRIMARY,
           "data_battery": data_bat, "per_ellmax": {}}
    for LM in ELLMAXES:
        nl = null[LM]; dv = np.array([data_bat[LM][k] for k in VEC])
        # per-marginal percentiles
        marg = {}
        for j, k in enumerate(VEC):
            p = float(100 * np.mean(nl[:, j] < dv[j]))
            marg[k] = {"data": float(dv[j]), "percentile": p,
                       "tail_pct": p if TAIL[k] == "U" else 100 - p, "tail": TAIL[k]}
        # look-elsewhere union on ensemble: P(any marginal at least as extreme as data in its tail)
        extreme = np.zeros(nl.shape[0], bool)
        for j, k in enumerate(VEC):
            if TAIL[k] == "U":
                extreme |= nl[:, j] >= dv[j]
            else:
                extreme |= nl[:, j] <= dv[j]
        union = float(np.mean(extreme))
        dp = depths(nl, dv)
        res["per_ellmax"][LM] = {"marginals": marg,
                                 "lookelsewhere_union_any_marginal": union,
                                 "joint_depths": dp}
        print(f"[{time.time()-t0:.0f}s] ellmax={LM} maha={dp['mahalanobis_pct']:.2f} "
              f"ns={dp['normalscores_pct']:.2f} spatial={dp['spatial_pct']:.2f} union={union:.3f}", flush=True)

    # ---- VERDICT per frozen decision rule ----
    def tier(p):
        return "SURVIVE" if p >= 99.73 else ("AMBIG" if p > 99.0 else "DISSOLVE")
    prim = res["per_ellmax"][PRIMARY]["joint_depths"]
    tiers = [tier(prim["mahalanobis_pct"]), tier(prim["normalscores_pct"]), tier(prim["spatial_pct"])]
    agree = len(set(tiers)) == 1
    robust = all(res["per_ellmax"][LM]["joint_depths"]["mahalanobis_pct"] >= 99.73 for LM in ELLMAXES)
    if agree and tiers[0] == "DISSOLVE":
        verdict = "DISSOLVED"
    elif tiers.count("SURVIVE") >= 2 and robust:
        verdict = "SURVIVES"
    else:
        verdict = "AMBIGUOUS"
    res["verdict"] = {"verdict": verdict, "primary_tiers": tiers, "depth_agreement": agree,
                      "robust_across_ellmax_survive": bool(robust),
                      "primary_joint_percentiles": {"mahalanobis": prim["mahalanobis_pct"],
                                                    "normalscores": prim["normalscores_pct"],
                                                    "spatial": prim["spatial_pct"]}}
    json.dump(res, open(OUT, "w"), indent=1)
    print(f"[{time.time()-t0:.0f}s] VERDICT={verdict}  tiers={tiers} robust={robust}", flush=True)
    print(json.dumps(res["verdict"], indent=1))


if __name__ == "__main__":
    main()

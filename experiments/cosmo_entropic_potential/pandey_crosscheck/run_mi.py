#!/usr/bin/env python3
"""
Pandey MI-minimum vs. our S-peak cross-check on TNG300-1.

Implements Pandey (2023, arXiv:2307.12959) faithfully — see DECISIONS.md STEP 1.
His MI-minimum epoch is set by the configuration-entropy rate (his Eq. 1, Eqs. 4-6),
NOT by a copula-invariant binned MI. We therefore compute:

  O1 (primary):   configuration entropy S_c(a) = -Sum rho ln rho dV, physical density,
                  and its driver G(a) = <(1+d)ln(1+d)>.  Pandey MI-min epoch = argmax dG/dlna.
  O2 (secondary): Pandey MI functional I(a) = rhobar^2(a) Int 4pi r^2 (1+xi)ln(1+xi) dr.
  O3 (control):   copula-invariant binned Shannon MI at fixed lag (expected monotone).

Same field as the S-peak: TNG300-1 FoF groups, mass-weighted, CIC on Ng^3, L=205 Mpc/h.
Octant (2^3) jackknife for the epoch error. Incremental flush to results.json.
"""
import sys, os, json, glob, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "copula_stress"))
from copula_lib import cic_grid  # noqa: E402

DATA = os.path.join(HERE, "..", "large_volume", "data")
LBOX = 205.0            # Mpc/h
NG = 128               # primary mesh (cell 1.60 Mpc/h)
RESULTS = os.path.join(HERE, "results.json")

# O2 correlation-integral range (quasi-linear "large regions"), Mpc/h
R_MIN, R_MAX = 5.0, 50.0
# O3 lags (Mpc/h) and bins
O3_LAGS = [12.8, 25.6, 51.2]
O3_NBINS = 16


def load_snaps(kind="groups"):
    fs = sorted(glob.glob(os.path.join(DATA, f"tng300_{kind}_*.npz")),
                key=lambda f: int(f.split("_")[-1].split(".")[0]))
    out = []
    for f in fs:
        d = np.load(f)
        out.append(dict(snap=int(d["snap"]), z=float(d["z"]), a=float(d["a"]),
                        pos=d["pos"].astype(float), m=d["m200"].astype(float)))
    return out


def density_field(pos, m, ng, box):
    """CIC overdelta delta = rho/mean-1 (mass-weighted). Returns delta (ng^3)."""
    return cic_grid(pos, box, ng, weights=m)


def G_functional(delta):
    """G = <(1+delta) ln(1+delta)> over cells. Density-field negentropy / config information.
    (1+delta)>=0 by construction; ln at exactly 0 handled as x ln x -> 0.)"""
    x = 1.0 + delta
    x = np.clip(x, 0.0, None)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(x > 0, x * np.log(x), 0.0)
    return float(np.mean(t))


def config_entropy_structure(delta):
    """Structure part of S_c per unit total mass:  -G(a).  (S_c = const + 3M ln a - M G.)"""
    return -G_functional(delta)


def xi_from_field(delta, box, ng, nbin=40, rmax=None):
    """Two-point correlation xi(r) from the CIC overdensity via FFT power spectrum.
    Returns (r_centers, xi(r)) with shot-noise NOT subtracted (Pandey uses the field xi)."""
    if rmax is None:
        rmax = box / 2.0
    dk = np.fft.rfftn(delta)
    pk3d = (dk * np.conj(dk)).real / delta.size
    # xi(r) = IFFT of P(k); use full FFT of the real power spectrum
    # Build full-cube power then inverse-transform to correlation.
    pk_full = np.fft.irfftn(np.fft.rfftn(delta) * np.conj(np.fft.rfftn(delta)),
                            s=delta.shape) / delta.size
    xi3d = pk_full  # autocorrelation of delta = xi on the grid (per-cell variance at r=0)
    # radial average
    n = ng
    freqs = np.fft.fftfreq(n) * n  # integer cell lags
    kz = freqs
    LX = np.abs(freqs)
    # build lag magnitude grid (in cells), fold to [0,n/2]
    ax = np.minimum(np.arange(n), n - np.arange(n))  # min image lag in cells
    LxG, LyG, LzG = np.meshgrid(ax, ax, ax, indexing="ij")
    rcells = np.sqrt(LxG**2 + LyG**2 + LzG**2)
    cell = box / n
    rphys = rcells * cell
    # radial bins
    redges = np.linspace(0, rmax, nbin + 1)
    which = np.digitize(rphys.ravel(), redges) - 1
    xflat = xi3d.ravel()
    rc = 0.5 * (redges[1:] + redges[:-1])
    xir = np.full(nbin, np.nan)
    for b in range(nbin):
        sel = which == b
        if sel.sum() > 0:
            xir[b] = xflat[sel].mean()
    return rc, xir, pk3d  # pk3d unused downstream


def pandey_MI_functional(delta, a, box, ng):
    """O2: I(a) = rhobar^2(a) Int_{rmin}^{rmax} 4pi r^2 (1+xi)ln(1+xi) dr, rhobar ~ a^-3.
    Overall constant dropped; only the a-dependence and shape matter for the epoch."""
    rc, xir, _ = xi_from_field(delta, box, ng, nbin=50, rmax=box / 2.0)
    sel = (rc >= R_MIN) & (rc <= R_MAX) & np.isfinite(xir)
    r = rc[sel]
    xi = xir[sel]
    onexi = np.clip(1.0 + xi, 1e-12, None)
    integrand = 4.0 * np.pi * r**2 * onexi * np.log(onexi)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    integral = trapz(integrand, r)
    rhobar2 = a ** (-6.0)   # (a^-3)^2, constant rho0 dropped
    return float(rhobar2 * integral), float(integral)


def binned_MI_at_lag(delta, lag_cells, nbins):
    """O3: copula-invariant Shannon MI between cell and cell-shifted-by-lag (x-axis lag),
    equal-count binning of ln(1+delta). Averaged over the 3 axis directions."""
    x = np.log(np.clip(1.0 + delta, 1e-12, None))
    mis = []
    for axis in range(3):
        y = np.roll(x, lag_cells, axis=axis)
        xa = x.ravel()
        ya = y.ravel()
        # equal-count bin edges from the marginal
        qs = np.linspace(0, 1, nbins + 1)
        ex = np.quantile(xa, qs)
        ex[0] -= 1e-9
        ex[-1] += 1e-9
        bx = np.clip(np.digitize(xa, ex) - 1, 0, nbins - 1)
        by = np.clip(np.digitize(ya, ex) - 1, 0, nbins - 1)
        joint = np.zeros((nbins, nbins))
        np.add.at(joint, (bx, by), 1.0)
        joint /= joint.sum()
        px = joint.sum(1)
        py = joint.sum(0)
        with np.errstate(divide="ignore", invalid="ignore"):
            mi = 0.0
            nz = joint > 0
            mi = np.sum(joint[nz] * np.log(joint[nz] / (px[:, None] * py[None, :])[nz]))
        mis.append(float(mi))
    return float(np.mean(mis))


def spline_deriv_peak(lna, G):
    """Fit a smoothing spline to G(ln a), return (lna_of_dGdlna_peak, z_peak, dGdlna curve)."""
    from scipy.interpolate import UnivariateSpline
    order = np.argsort(lna)
    x = np.asarray(lna)[order]
    y = np.asarray(G)[order]
    # light smoothing; s scaled to data
    s = 1e-4 * np.var(y) * len(y)
    spl = UnivariateSpline(x, y, k=4, s=s)
    xf = np.linspace(x.min(), x.max(), 2000)
    d1 = spl.derivative(1)(xf)
    ipk = int(np.argmax(d1))
    lna_pk = float(xf[ipk])
    z_pk = float(np.exp(-lna_pk) - 1.0)
    return lna_pk, z_pk, (xf, d1)


def octant_mask(pos, box, drop):
    """Boolean mask keeping points NOT in dropped octant (drop in 0..7)."""
    h = box / 2.0
    ox = (pos[:, 0] >= h).astype(int)
    oy = (pos[:, 1] >= h).astype(int)
    oz = (pos[:, 2] >= h).astype(int)
    oid = ox * 4 + oy * 2 + oz
    return oid != drop


def run(kind="groups", ng=NG):
    snaps = load_snaps(kind)
    print(f"[{kind}] {len(snaps)} snapshots, Ng={ng}, box={LBOX} Mpc/h", flush=True)
    res = dict(kind=kind, ng=ng, box=LBOX, r_range=[R_MIN, R_MAX],
               s_peak_ours=dict(z=0.59, sigma=0.03), snaps=[])
    lna, G_all, Sc_all, I2_all, I2int_all = [], [], [], [], []
    o3_all = {f"{lag}": [] for lag in O3_LAGS}
    for s in snaps:
        t0 = time.time()
        delta = density_field(s["pos"], s["m"], ng, LBOX)
        G = G_functional(delta)
        Sc_struct = -G
        I2, I2int = pandey_MI_functional(delta, s["a"], LBOX, ng)
        o3 = {}
        for lag in O3_LAGS:
            lc = max(1, int(round(lag / (LBOX / ng))))
            o3[f"{lag}"] = binned_MI_at_lag(delta, lc, O3_NBINS)
            o3_all[f"{lag}"].append(o3[f"{lag}"])
        lna.append(np.log(s["a"]))
        G_all.append(G); Sc_all.append(Sc_struct)
        I2_all.append(I2); I2int_all.append(I2int)
        row = dict(snap=s["snap"], z=s["z"], a=s["a"], G=G, Sc_struct=Sc_struct,
                   I2=I2, I2_corr_integral=I2int, o3=o3, npts=int(s["pos"].shape[0]))
        res["snaps"].append(row)
        # incremental flush
        with open(RESULTS, "w") as f:
            json.dump(res, f, indent=2)
        print(f"  snap {s['snap']:3d} z={s['z']:.3f}  G={G:.4e}  I2={I2:.4e} "
              f"o3[25.6]={o3['25.6']:.4f}  ({time.time()-t0:.1f}s)", flush=True)

    lna = np.array(lna); G_all = np.array(G_all)
    zs = np.array([r["z"] for r in res["snaps"]])

    # O1 primary epoch: argmax dG/dln a
    lna_pk, z_pk, (xf, d1) = spline_deriv_peak(lna, G_all)
    # O2 secondary epoch: argmin I(a) (interior only)
    I2arr = np.array(I2_all)
    z_o2 = float(zs[np.argmin(I2arr)])
    interior_o2 = 0 < np.argmin(I2arr) < len(I2arr) - 1

    res["O1_primary"] = dict(observable="argmax dG/dlna (config-entropy-rate extremum)",
                             z_min=z_pk, lna=lna_pk)
    res["O2_secondary"] = dict(observable="argmin Pandey MI functional I(a)",
                               z_min=z_o2, interior=bool(interior_o2))
    with open(RESULTS, "w") as f:
        json.dump(res, f, indent=2)
    print(f"[{kind}] O1 argmax dG/dlna -> z_min={z_pk:.3f}", flush=True)
    print(f"[{kind}] O2 argmin I(a)    -> z_min={z_o2:.3f} (interior={interior_o2})", flush=True)

    # ---- octant jackknife on O1 epoch ----
    jk = []
    for drop in range(8):
        Gj = []
        lnaj = []
        for s in snaps:
            m = octant_mask(s["pos"], LBOX, drop)
            dj = density_field(s["pos"][m], s["m"][m], ng, LBOX)
            Gj.append(G_functional(dj))
            lnaj.append(np.log(s["a"]))
        try:
            _, zjk, _ = spline_deriv_peak(np.array(lnaj), np.array(Gj))
            jk.append(zjk)
            print(f"  jk drop octant {drop}: z_min={zjk:.3f}", flush=True)
        except Exception as e:
            print(f"  jk drop octant {drop}: FAILED {e}", flush=True)
    jk = np.array(jk)
    res["O1_jackknife"] = dict(z_replicates=jk.tolist(),
                               z_mean=float(jk.mean()), z_std=float(jk.std()))
    with open(RESULTS, "w") as f:
        json.dump(res, f, indent=2)
    print(f"[{kind}] O1 jackknife: z_min = {jk.mean():.3f} +/- {jk.std():.3f} "
          f"(8 replicates)", flush=True)
    return res


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "groups"
    ng = int(sys.argv[2]) if len(sys.argv) > 2 else NG
    run(kind, ng)

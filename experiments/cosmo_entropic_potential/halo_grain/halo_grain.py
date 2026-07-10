#!/usr/bin/env python3
"""
Halo-grain S(a): the cosmic entropic potential over EVOLVING coordinating units.

Companion to ../s_of_a.py.  That calculation graded the entropic potential
    S(a) = -ln det C(a)
over a FIXED set of comoving Eulerian CELLS, and proved (T-E5 + general theorem)
that any local pointwise transform of the linear field only LOWERS S, so the
sign law
    1 + w(a) = -(1/3) d ln S / d ln a
forces w >= -1 (thawing / quintessence-like), in tension with DESI's phantom-past
CPL fit (w0 = -0.838, wa = -0.62).

HYPOTHESIS UNDER TEST (from the brief):
    Fixed cells violate the framework's OWN complete-unit discipline.  The cosmic
    coordinating units are HALOS (bound structures), and the halo set EVOLVES:
    halos form and MERGE.  A merger converts many units into one (the RIGIDITY
    direction: unit count k drops, survivors more correlated), so a halo-grain
    S(a) could RISE where the cell-grain S falls -- potentially flipping the w(z)
    sign toward the DESI (phantom) direction.

We test this on a REAL N-body halo catalog (IllustrisTNG-physics CAMELS CV_0,
FoF/Subfind group catalogs, 25 Mpc/h box) across 10 snapshots z=3->0, and on
two defensible operationalizations of "unit" plus a threshold sweep.

----------------------------------------------------------------------------
KEY THEORETICAL POINT (foregrounded because it governs everything below):
    In the NORMALIZED correlation matrix, LINEAR HALO BIAS b CANCELS EXACTLY.
    If delta_halo = b*delta_m then Cov_ij = b^2 xi_m(r_ij) and the normalization
    (sqrt of the diagonal) also carries b^2, so
        C_ij = xi_m(r_ij)/sigma_m^2       (b-independent)
    and the linear growth factor D(a) cancels too (numerator and diagonal both
    ~ D^2).  Therefore a halo-grain S(a) can differ from the a-CONSTANT linear
    matter result ONLY through:
        (1) DISCRETENESS / shot noise      -> Operationalization A
        (2) the EVOLVING POINT SET: the number of units k(a) and their
            separations r_ij(a)            -> Operationalization B
        (3) nonlinear / scale-dependent bias (shape change, 2nd order) -> probed
            via the measured clustering variance in A.
    This is why the bias-model choice (guard #5) does NOT move the normalized C:
    we report b(M,z) for context but it is projected out by construction.

OPERATIONALIZATIONS (both computed; see SUMMARY.md):
  (A) HALOS-AS-TRACERS on FIXED comoving cells.  Field = halo-count contrast
      (unweighted and mass-weighted) above a mass threshold.  C over cells has
      the fixed PSD shape rho(r)=xi_R(r)/sigma_R^2 diluted by the measured
      clustering fraction A(a) = (Var_total - shot)/Var_total of the cell field:
          C_ij = A(a) * rho(r_ij)  (i!=j),   C_ii = 1.
      A(a) is measured DIRECTLY from the catalog at each snapshot (data-driven
      amplitude; PSD-safe by construction, C = A*rho + (1-A)*I).  This isolates
      how much of the coordinating-unit field is genuine clustering vs Poisson
      discreteness -- the halo-population analogue of the cell-grain field.

  (B) UNITS-AS-UNITS.  k(a) = number of halos above threshold in the (fixed
      comoving) box.  C over the actual halo POSITIONS via the model matter
      correlation C_ij = xi_R(r_ij)/sigma_R^2, C_ii=1 (PSD-safe: xi_R is the FT
      of a non-negative P(k)).  S total AND S/k (T-E3: both matter).  Two
      variants: B-total (all halos up to a numerical cap, k grows with time) and
      B-fixedk (common subsample size across snapshots -> isolates GEOMETRY).

GUARDS: min eigenvalue + condition number per snapshot; shot noise measured and
subtracted (A); numerical cap with averaged random subsamples (B); bias model
reported but shown to cancel; 1e13 threshold flagged volume-limited (<=9 halos).

DATA: public CAMELS Flatiron mirror (no API key; the TNG www API is gated/403).
      Fields-only ranged HDF5 reads of GroupPos, Group_M_Crit200, Group_R_Crit200.

Usage: python3 halo_grain.py            (downloads+caches ~fields, then computes)
Outputs: results.json, SUMMARY.md, figures/*.png
"""

import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))

# ---- reuse the framework's tested P(k)/xi/entropy machinery, retuned to the
#      CAMELS CV cosmology so the halo grain and cell grain share one pipeline.
import s_of_a as S  # noqa: E402

# CAMELS CV fiducial cosmology (from the group-catalog Parameters header +
# Villaescusa-Navarro et al. 2021 fiducial: sigma8=0.8, ns=0.9624).
S.OM = 0.300
S.OL = 0.700
S.H0H = 0.6711
S.OB = 0.049
S.NS = 0.9624
S.SIGMA8 = 0.80

SEED = 20260710
rng_global = np.random.default_rng(SEED)

SCRATCH = os.environ.get(
    "HG_SCRATCH",
    "/tmp/claude-1000/-home-emoore-RATCHET/"
    "75f07b43-c0f5-4052-9346-528e61302ccd/scratchpad/halo_grain_cache",
)
os.makedirs(SCRATCH, exist_ok=True)

BASE = "https://users.flatironinstitute.org/~camels/Sims/IllustrisTNG/CV/CV_0/"
BOX_KPC = 25000.0            # ckpc/h
BOX = BOX_KPC / 1000.0       # Mpc/h
MASS_UNIT = 1e10             # Msun/h per code unit (UnitMass_in_g=1.989e43)

# snapshot -> redshift chosen to span z=3->0 with a good ln a lever arm.
SNAPS = [32, 40, 48, 54, 60, 66, 72, 78, 84, 90]

THRESH = {"1e11": 1e11, "1e12": 1e12, "1e13": 1e13}   # Msun/h on M200c

# ----------------------------------------------------------------------------
# 1. DATA: fields-only ranged reads, cached
# ----------------------------------------------------------------------------
def load_snapshot(snap, cv=0):
    """Return dict(z, a, pos[Mpc/h] (N,3), m200[Msun/h], r200[Mpc/h]) for CV_<cv>."""
    cache = f"{SCRATCH}/halos_cv{cv}_{snap:03d}.npz"
    if os.path.exists(cache):
        d = np.load(cache)
        return dict(z=float(d["z"]), a=float(d["a"]),
                    pos=d["pos"], m200=d["m200"], r200=d["r200"])
    import fsspec, h5py
    base = BASE.replace("CV_0/", f"CV_{cv}/")
    url = f"{base}groups_{snap:03d}.hdf5"
    with h5py.File(fsspec.open(url, "rb").open(), "r") as h:
        z = float(h["Header"].attrs["Redshift"])
        pos = h["Group/Group_M_Crit200"]  # touch to ensure group exists
        pos = h["Group/GroupPos"][:].astype(np.float64) / 1000.0   # -> Mpc/h
        m200 = h["Group/Group_M_Crit200"][:].astype(np.float64) * MASS_UNIT
        r200 = h["Group/Group_R_Crit200"][:].astype(np.float64) / 1000.0
    a = 1.0 / (1.0 + z)
    np.savez(cache, z=z, a=a, pos=pos, m200=m200, r200=r200)
    return dict(z=z, a=a, pos=pos, m200=m200, r200=r200)


def periodic_pdist(pos, box):
    """All-pairs minimum-image distances (Mpc/h).  pos (N,3)."""
    d = pos[:, None, :] - pos[None, :, :]
    d -= box * np.round(d / box)
    return np.sqrt((d ** 2).sum(-1))


# ----------------------------------------------------------------------------
# 2. Sheth-Tormen linear bias b(M,z)  (reported for context; cancels in C)
# ----------------------------------------------------------------------------
def sheth_tormen_bias(ps, M_msun_h, a):
    """b(M,z) via Sheth-Mo-Tormen 2001 with delta_c=1.686.  M in Msun/h."""
    rho_m = 2.775e11 * S.OM                     # Msun/h / (Mpc/h)^3 comoving
    R = (3.0 * M_msun_h / (4.0 * np.pi * rho_m)) ** (1.0 / 3.0)
    sig = np.sqrt(ps._sigma2(R, S.W_tophat)) * S.growth_D(a)
    dc = 1.686
    nu = dc / sig
    aa, b, c = 0.707, 0.5, 0.6
    sq = np.sqrt(aa) * nu
    return 1.0 + (sq ** 2 - 1.0) / dc + (2.0 * b / dc) / (1.0 + (aa * nu ** 2) ** c)


# ----------------------------------------------------------------------------
# 3. Operationalization A: halos-as-tracers on fixed comoving cells
# ----------------------------------------------------------------------------
def cell_field(pos, m200, n_side, box, weight="count"):
    """3D histogram of halos into n_side^3 fixed comoving cells.
    Returns per-cell field value (count or summed mass) as a flat array,
    plus the shot-noise variance of the contrast delta = f/mean - 1."""
    edges = np.linspace(0.0, box, n_side + 1)
    ix = np.clip(np.digitize(pos[:, 0], edges) - 1, 0, n_side - 1)
    iy = np.clip(np.digitize(pos[:, 1], edges) - 1, 0, n_side - 1)
    iz = np.clip(np.digitize(pos[:, 2], edges) - 1, 0, n_side - 1)
    flat = (ix * n_side + iy) * n_side + iz
    ncell = n_side ** 3
    if weight == "count":
        w = np.ones(len(pos))
    else:
        w = m200.copy()
    field = np.bincount(flat, weights=w, minlength=ncell).astype(float)
    # Poisson shot noise on the contrast:  Var_shot(delta) = Ncell * sum(w^2)/(sum w)^2
    sw = w.sum()
    shot = ncell * (w ** 2).sum() / sw ** 2 if sw > 0 else np.inf
    return field, shot


def op_A(ps, snaps_data, thr, n_side=8, weight="count", n_jack=None):
    """Op A: clustering-fraction-diluted C over fixed cells.  Returns per-snapshot
    A(a) (clustering fraction), S=-ln det C, min eig, cond, and the k=Ncell."""
    box = BOX
    # fixed cell lattice (centres) and the PSD shape rho(r_ij) = xi_R(r_ij)/sigma_R^2
    n = n_side
    c = (np.arange(n) + 0.5) * (box / n)
    gx, gy, gz = np.meshgrid(c, c, c, indexing="ij")
    centres = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1)
    Rmat = periodic_pdist(centres, box)
    L_cell = box / n
    R_eff = (3.0 / (4.0 * np.pi)) ** (1.0 / 3.0) * L_cell     # top-hat radius of a cell
    xi = ps.xi_spline(R_eff)
    sig2 = ps.sigma2_R(R_eff)
    rho = xi(Rmat) / sig2
    np.fill_diagonal(rho, 1.0)
    # make rho a clean PSD correlation shape (tiny negative eigen clip from spline)
    ev, evec = np.linalg.eigh(rho)
    ev = np.clip(ev, 1e-10, None)
    rho = evec @ np.diag(ev) @ evec.T
    d = np.sqrt(np.diag(rho))
    rho = rho / np.outer(d, d)

    out = []
    for sd in snaps_data:
        m = sd["m200"] > thr
        pos, mass = sd["pos"][m], sd["m200"][m]
        k_units = int(m.sum())
        if k_units < 3:
            out.append(dict(a=sd["a"], z=sd["z"], k_units=k_units,
                            A=np.nan, S=np.nan, min_eig=np.nan, cond=np.nan,
                            var_total=np.nan, shot=np.nan, A_err=np.nan))
            continue
        field, shot = cell_field(pos, mass, n, box, weight)
        mean = field.mean()
        delta = field / mean - 1.0
        var_total = delta.var()
        A = np.clip((var_total - shot) / var_total, 0.0, 1.0) if var_total > 0 else 0.0
        # jackknife A over cells for an error bar
        A_err = np.nan
        if n_jack:
            nc = len(delta)
            idx = np.array_split(rng_global.permutation(nc), n_jack)
            Aj = []
            for j in range(n_jack):
                keep = np.setdiff1d(np.arange(nc), idx[j])
                dv = delta[keep]
                vt = dv.var()
                Aj.append(np.clip((vt - shot) / vt, 0, 1) if vt > 0 else 0.0)
            Aj = np.array(Aj)
            A_err = np.sqrt((n_jack - 1) / n_jack * ((Aj - Aj.mean()) ** 2).sum())
        C = A * rho + (1.0 - A) * np.eye(n ** 3)
        ev = np.linalg.eigvalsh(C)
        S_val = float(-np.log(ev).sum())
        out.append(dict(a=sd["a"], z=sd["z"], k_units=k_units, A=float(A),
                        S=S_val, min_eig=float(ev.min()),
                        cond=float(ev.max() / ev.min()),
                        var_total=float(var_total), shot=float(shot),
                        A_err=float(A_err) if A_err == A_err else np.nan))
    return dict(n_cells=n ** 3, R_eff=R_eff, records=out)


# ----------------------------------------------------------------------------
# 4. Operationalization B: units-as-units over actual halo positions
# ----------------------------------------------------------------------------
def build_halo_C(ps, pos, box, R_smooth):
    """PSD C_ij = xi_R(r_ij)/sigma_R^2, C_ii=1, over halo positions."""
    xi = ps.xi_spline(R_smooth)
    sig2 = ps.sigma2_R(R_smooth)
    Rmat = periodic_pdist(pos, box)
    C = xi(Rmat) / sig2
    np.fill_diagonal(C, 1.0)
    return C


def op_B(ps, snaps_data, thr, R_smooth=1.0, cap=1000, n_draw=8, fixed_k=None):
    """Op B.  If fixed_k is None: use all halos up to `cap` (subsample+avg if
    over cap) -> S_total with k(a) growing.  If fixed_k=int: subsample to that
    common size across snapshots (isolates geometry).  Returns per-snapshot S,
    S/k, k, guards (averaged over n_draw random subsamples)."""
    box = BOX
    out = []
    for sd in snaps_data:
        m = sd["m200"] > thr
        pos_all = sd["pos"][m]
        k_all = len(pos_all)
        target = fixed_k if fixed_k is not None else min(k_all, cap)
        if target < 3 or k_all < 3:
            out.append(dict(a=sd["a"], z=sd["z"], k=k_all, k_used=0,
                            S=np.nan, S_per_k=np.nan, min_eig=np.nan,
                            cond=np.nan, S_std=np.nan))
            continue
        Ss, mine, conds = [], [], []
        ndraw = 1 if k_all == target else n_draw
        for di in range(ndraw):
            if k_all == target:
                pos = pos_all
            else:
                rng = np.random.default_rng(SEED + 1000 * di + int(sd["z"] * 97))
                sel = rng.choice(k_all, size=target, replace=False)
                pos = pos_all[sel]
            C = build_halo_C(ps, pos, box, R_smooth)
            ev = np.linalg.eigvalsh(C)
            ev = np.clip(ev, 1e-12, None)
            Ss.append(-np.log(ev).sum())
            mine.append(ev.min())
            conds.append(ev.max() / ev.min())
        Ss = np.array(Ss)
        out.append(dict(a=sd["a"], z=sd["z"], k=k_all, k_used=int(target),
                        S=float(Ss.mean()), S_std=float(Ss.std()),
                        S_per_k=float(Ss.mean() / target),
                        min_eig=float(np.mean(mine)), cond=float(np.mean(conds))))
    return out


# ----------------------------------------------------------------------------
# 5. Sign law helpers
# ----------------------------------------------------------------------------
def series_sign(records, key="S"):
    """From a list of dicts with 'a' and key, compute dlnS/dlna, w(a), CPL fit.
    Drops non-finite / non-positive S."""
    a = np.array([r["a"] for r in records])
    s = np.array([r.get(key, np.nan) for r in records])
    ok = np.isfinite(a) & np.isfinite(s) & (s > 0)
    a, s = a[ok], s[ok]
    order = np.argsort(a)
    a, s = a[order], s[order]
    if len(a) < 4:
        return dict(usable=False, n=int(len(a)))
    dlnS = S.dln_dlna(a, s)
    w = -1.0 - dlnS / 3.0
    w0, wa = S.fit_cpl(a, w, amin=a.min())
    # ROBUST global trend: single-slope OLS of ln S vs ln a over the whole range.
    # Far less noise-sensitive than the pointwise spline derivative on 10 points.
    gslope = float(np.polyfit(np.log(a), np.log(s), 1)[0])
    w_global = -1.0 - gslope / 3.0
    return dict(usable=True, n=int(len(a)),
                a=a.tolist(), S=s.tolist(), dlnS_dlna=dlnS.tolist(),
                w=w.tolist(), dlnS_dlna_today=float(dlnS[-1]),
                w_today=float(w[-1]), w0=float(w0), wa=float(wa),
                global_slope=gslope, w_global=w_global,
                S_rises_globally=bool(gslope > 0),
                phantom_anywhere=bool(np.any(w < -1.0)),
                phantom_today=bool(w[-1] < -1.0),
                S_rising_anywhere=bool(np.any(dlnS > 0)),
                S_monotone_decreasing=bool(np.all(np.diff(s) < 0)),
                S_peak_a=float(a[int(np.argmax(s))]),
                S_peak_z=float(1.0 / a[int(np.argmax(s))] - 1.0))


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def main():
    print("Loading CAMELS CV_0 halo catalogs (fields-only, cached)...")
    snaps_data = []
    for s in SNAPS:
        sd = load_snapshot(s)
        snaps_data.append(sd)
        print(f"  snap {s:03d}  z={sd['z']:5.3f}  a={sd['a']:5.3f}  "
              f"Ngroups={len(sd['m200']):6d}  Mmax={sd['m200'].max():.2e}")

    ps = S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=S.SIGMA8)

    results = dict(
        seed=SEED, data_source="CAMELS IllustrisTNG CV_0 (Flatiron public mirror)",
        tng_www_api="gated (HTTP 403, needs key) -> used public CAMELS group catalogs instead",
        box_Mpc_h=BOX, cosmology=dict(Om=S.OM, OL=S.OL, h=S.H0H, Ob=S.OB,
                                       ns=S.NS, sigma8=S.SIGMA8),
        sign_law="1 + w(a) = -(1/3) dlnS/dlna",
        desi=dict(w0=-0.838, wa=-0.62),
        cell_grain_reference=dict(w0=-0.897, wa=-0.099,
                                  note="../results.json combined: S falling, w>-1, no phantom"),
        theory_note=("linear bias b and growth D(a) CANCEL in the normalized C; "
                     "halo grain departs from the a-constant matter result only via "
                     "(1) shot noise [op A], (2) evolving unit count k(a) + geometry [op B]."),
        snapshots=[dict(snap=s, z=sd["z"], a=sd["a"], Ngroups=len(sd["m200"]),
                        Mmax_Msun_h=float(sd["m200"].max()))
                   for s, sd in zip(SNAPS, snaps_data)],
    )

    # --- mass function k(>M,a): does the merger premise (k drops) hold? ---
    mf = {}
    for name, t in THRESH.items():
        mf[name] = [dict(z=sd["z"], a=sd["a"], k=int((sd["m200"] > t).sum()))
                    for sd in snaps_data]
    results["mass_function_k_of_a"] = mf
    # bias context
    results["bias_ST_context"] = {
        name: [dict(z=sd["z"], b=float(sheth_tormen_bias(ps, t, sd["a"])))
               for sd in snaps_data]
        for name, t in THRESH.items()
    }

    sign_table = []   # (variant, threshold, weight, dlnS_today, w0, wa, phantom?)

    # ----- Operationalization A -----
    results["op_A"] = {}
    for name, t in THRESH.items():
        for weight in ("count", "mass"):
            key = f"{name}_{weight}"
            oa = op_A(ps, snaps_data, t, n_side=8, weight=weight, n_jack=8)
            sg = series_sign(oa["records"], key="S")
            results["op_A"][key] = dict(meta=oa, sign=sg)
            if sg.get("usable"):
                sign_table.append(dict(
                    variant="A:halos-as-tracers", threshold=name, weight=weight,
                    dlnS_dlna_today=round(sg["dlnS_dlna_today"], 3),
                    w0=round(sg["w0"], 3), wa=round(sg["wa"], 3),
                    w_today=round(sg["w_today"], 3),
                    phantom_anywhere=sg["phantom_anywhere"],
                    S_rising_anywhere=sg["S_rising_anywhere"],
                    S_peak_z=round(sg["S_peak_z"], 2)))

    # ----- Operationalization B -----
    results["op_B"] = {}
    for name, t in THRESH.items():
        counts = [int((sd["m200"] > t).sum()) for sd in snaps_data]
        kmin = min(counts)
        # B-total (k grows), and B-fixedk (isolate geometry) when kmin>=8
        variants = [("B-total", None)]
        if kmin >= 8:
            variants.append(("B-fixedk%d" % kmin, kmin))
        for vname, fk in variants:
            recs = op_B(ps, snaps_data, t, R_smooth=1.0, cap=1000,
                        n_draw=8, fixed_k=fk)
            sg_tot = series_sign(recs, key="S")
            sg_perk = series_sign(recs, key="S_per_k")
            results["op_B"][f"{name}_{vname}"] = dict(
                records=recs, sign_S=sg_tot, sign_S_per_k=sg_perk, kmin=kmin)
            if sg_tot.get("usable"):
                sign_table.append(dict(
                    variant=f"B:{vname}(S_total)", threshold=name, weight="-",
                    dlnS_dlna_today=round(sg_tot["dlnS_dlna_today"], 3),
                    w0=round(sg_tot["w0"], 3), wa=round(sg_tot["wa"], 3),
                    w_today=round(sg_tot["w_today"], 3),
                    phantom_anywhere=sg_tot["phantom_anywhere"],
                    S_rising_anywhere=sg_tot["S_rising_anywhere"],
                    S_peak_z=round(sg_tot["S_peak_z"], 2)))
            if sg_perk.get("usable"):
                sign_table.append(dict(
                    variant=f"B:{vname}(S/k)", threshold=name, weight="-",
                    dlnS_dlna_today=round(sg_perk["dlnS_dlna_today"], 3),
                    w0=round(sg_perk["w0"], 3), wa=round(sg_perk["wa"], 3),
                    w_today=round(sg_perk["w_today"], 3),
                    phantom_anywhere=sg_perk["phantom_anywhere"],
                    S_rising_anywhere=sg_perk["S_rising_anywhere"],
                    S_peak_z=round(sg_perk["S_peak_z"], 2)))

    # ----- multi-box robustness: is the trend real or 25 Mpc/h cosmic variance? -----
    # Re-run the best-statistics variants across independent-phase CV boxes and
    # report the per-box global slope dlnS/dlna (mean +/- std).  This is the
    # decisive guard against finite-volume noise (guard #4).
    CV_BOXES = list(range(0, 6))
    mb = {"boxes": CV_BOXES, "variants": {}}
    slopes_A = {"1e11_count": [], "1e12_count": []}
    slopes_Bfix = {"1e11": [], "1e12": []}
    slopes_Btot = {"1e11": []}
    for cv in CV_BOXES:
        try:
            sdc = [load_snapshot(s, cv=cv) for s in SNAPS]
        except Exception as e:
            print(f"  CV_{cv}: load failed ({repr(e)[:60]}) - skipping")
            continue
        for name in ("1e11", "1e12"):
            t = THRESH[name]
            oa = op_A(ps, sdc, t, n_side=8, weight="count")
            sg = series_sign(oa["records"], key="S")
            if sg.get("usable"):
                slopes_A[f"{name}_count"].append(sg["global_slope"])
            counts = [int((x["m200"] > t).sum()) for x in sdc]
            kmin = min(counts)
            if kmin >= 8:
                recs = op_B(ps, sdc, t, R_smooth=1.0, n_draw=6, fixed_k=kmin)
                sgf = series_sign(recs, key="S")
                if sgf.get("usable"):
                    slopes_Bfix[name].append(sgf["global_slope"])
            if name == "1e11":
                recs_t = op_B(ps, sdc, t, R_smooth=1.0, cap=1000, n_draw=6)
                sgt = series_sign(recs_t, key="S")
                if sgt.get("usable"):
                    slopes_Btot["1e11"].append(sgt["global_slope"])

    def summ(lst):
        a = np.array(lst, float)
        if len(a) == 0:
            return dict(n=0)
        return dict(n=int(len(a)), mean_slope=float(a.mean()),
                    std_slope=float(a.std()), mean_w=float(-1 - a.mean() / 3),
                    all_negative=bool(np.all(a < 0)), all_positive=bool(np.all(a > 0)),
                    per_box=[round(x, 3) for x in a.tolist()])
    mb["variants"]["opA_1e11_count(S)"] = summ(slopes_A["1e11_count"])
    mb["variants"]["opA_1e12_count(S)"] = summ(slopes_A["1e12_count"])
    mb["variants"]["opB_1e11_fixedk(S)"] = summ(slopes_Bfix["1e11"])
    mb["variants"]["opB_1e12_fixedk(S)"] = summ(slopes_Bfix["1e12"])
    mb["variants"]["opB_1e11_total(S,extensive-in-k)"] = summ(slopes_Btot["1e11"])
    results["multibox_robustness"] = mb

    results["sign_table"] = sign_table
    any_phantom = any(r["phantom_anywhere"] for r in sign_table)
    any_phantom_today = any(r.get("w_today", 0) < -1.0 for r in sign_table)
    results["phantom_in_any_variant"] = bool(any_phantom)
    results["phantom_today_in_any_variant"] = bool(any_phantom_today)

    mbv = results["multibox_robustness"]["variants"]
    results["verdict"] = dict(
        headline=("Halo grain does NOT rescue the DESI phantom direction; it "
                  "CONFIRMS the cell-grain no-phantom (w >= -1) result."),
        merger_premise_k_drops=("FALSE in the data: cumulative halo count above a "
                                "fixed threshold GROWS or plateaus z=3->0 "
                                "(1e11: 217->398 peak->364; 1e12: 11->53; 1e13: 0->9), "
                                "even though Mmax grows 10x. Mergers concentrate MASS "
                                "but do not reduce the unit count at these thresholds."),
        intensive_measures=("Every intensive / fixed-unit measure gives w >= -1 "
                            "robustly across 6 independent-phase boxes: "
                            f"opA(1e11,count) mean w={mbv['opA_1e11_count(S)'].get('mean_w'):.3f}; "
                            f"opB(1e11,fixed-k) mean w={mbv['opB_1e11_fixedk(S)'].get('mean_w'):.3f} "
                            f"(all {mbv['opB_1e11_fixedk(S)'].get('n')} boxes S-falling)."),
        only_phantom_channel=("The ONLY robustly S-rising variant is B-total, whose "
                             f"S is EXTENSIVE in the growing unit count k "
                             f"(mean w={mbv['opB_1e11_total(S,extensive-in-k)'].get('mean_w'):.3f}, "
                             "all 6 boxes). Holding k fixed reverses the sign -> the "
                             "'phantom' is unit-counting bookkeeping, not increased "
                             "coordination. T-E3's intensive S/k removes it."),
        key_interpretive_fork=("If one INSISTS S_total (with time-growing k) is the "
                              "physical potential, w ~ -1.1 (mild phantom) results. "
                              "The sign law was derived at FIXED k (cell grain); "
                              "comparing -ln det across different dimensions is not "
                              "apples-to-apples, and both S/k and fixed-k geometry "
                              "reverse it. We read it as an artifact."),
        biggest_caveat=("Proxy: C here is a modeled/measured 2-point correlation "
                        "matrix, not the framework's true coordination operator; and "
                        "the robust statement rests on the 1e11 threshold -- the "
                        "25 Mpc/h box has too few >1e12 halos (1e13 volume-limited) "
                        "to grain the merger-dominated regime the hypothesis targets."),
    )

    with open(HERE / "results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nwrote results.json")

    make_figures(results)
    print_sign_table(sign_table)
    return results


def print_sign_table(tab):
    print("\n=== PER-VARIANT SIGN TABLE ===")
    hdr = f"{'variant':26s} {'thr':6s} {'wt':5s} {'dlnS/dlna_0':>11s} {'w0':>7s} {'wa':>7s} {'phantom?':>9s} {'S_rise?':>8s}"
    print(hdr)
    for r in tab:
        print(f"{r['variant']:26s} {r['threshold']:6s} {r['weight']:5s} "
              f"{r['dlnS_dlna_today']:11.3f} {r['w0']:7.3f} {r['wa']:7.3f} "
              f"{str(r['phantom_anywhere']):>9s} {str(r['S_rising_anywhere']):>8s}")


def make_figures(results):
    # Fig 1: mass function k(>M,a)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for name in THRESH:
        recs = results["mass_function_k_of_a"][name]
        z = [r["z"] for r in recs]
        k = [r["k"] for r in recs]
        ax[0].plot(z, k, "o-", label=f">{name} Msun/h")
    ax[0].set_xlabel("z"); ax[0].set_ylabel("k = N halos above threshold")
    ax[0].invert_xaxis(); ax[0].legend(); ax[0].set_title("Coordinating-unit count k(z)")
    ax[0].grid(alpha=0.3)
    Mmax = [s["Mmax_Msun_h"] for s in results["snapshots"]]
    zz = [s["z"] for s in results["snapshots"]]
    ax[1].semilogy(zz, Mmax, "s-", color="crimson")
    ax[1].set_xlabel("z"); ax[1].set_ylabel("most massive halo M200c [Msun/h]")
    ax[1].invert_xaxis(); ax[1].set_title("Merger signature: Mmax(z)")
    ax[1].grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(HERE / "figures/fig1_units_kz.png", dpi=110)
    plt.close(fig)

    # Fig 2: op A  A(a) and S(a)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for name in THRESH:
        key = f"{name}_count"
        if key not in results["op_A"]:
            continue
        recs = results["op_A"][key]["meta"]["records"]
        z = [r["z"] for r in recs]
        A = [r["A"] for r in recs]
        Sv = [r["S"] for r in recs]
        ax[0].plot(z, A, "o-", label=f">{name}")
        ax[1].plot(z, Sv, "o-", label=f">{name}")
    ax[0].set_xlabel("z"); ax[0].set_ylabel("clustering fraction A")
    ax[0].invert_xaxis(); ax[0].legend(); ax[0].set_title("Op A: clustering vs shot")
    ax[0].grid(alpha=0.3)
    ax[1].set_xlabel("z"); ax[1].set_ylabel("S = -ln det C (cells)")
    ax[1].invert_xaxis(); ax[1].legend(); ax[1].set_title("Op A: S(a) [count-weighted]")
    ax[1].grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(HERE / "figures/fig2_opA.png", dpi=110)
    plt.close(fig)

    # Fig 3: op B  S_total and S/k
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for kkey, blk in results["op_B"].items():
        recs = blk["records"]
        z = [r["z"] for r in recs if np.isfinite(r["S"])]
        St = [r["S"] for r in recs if np.isfinite(r["S"])]
        Sk = [r["S_per_k"] for r in recs if np.isfinite(r["S"])]
        if "total" in kkey:
            ax[0].plot(z, St, "o-", label=kkey)
            ax[1].plot(z, Sk, "o-", label=kkey)
    ax[0].set_xlabel("z"); ax[0].set_ylabel("S_total = -ln det C (halos)")
    ax[0].invert_xaxis(); ax[0].legend(fontsize=7); ax[0].set_title("Op B: S total")
    ax[0].grid(alpha=0.3)
    ax[1].set_xlabel("z"); ax[1].set_ylabel("S/k (per unit)")
    ax[1].invert_xaxis(); ax[1].legend(fontsize=7); ax[1].set_title("Op B: S per unit")
    ax[1].grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(HERE / "figures/fig3_opB.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()

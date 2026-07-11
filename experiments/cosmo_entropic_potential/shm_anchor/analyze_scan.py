#!/usr/bin/env python3
"""
Analyze the SHM retention-anchor scan (CPU): from the per-bin S(a) in results.json,
compute the two money curves as a function of unit mass scale --
  (a) DESI-fit quality: CPL-projection Mahalanobis to DESI (both boxes) + real DESI DR2
      likelihood chi2 (TNG300 bins), and
  (b) S-peak epoch (global max + plateau breadth),
then overlay the SHM efficiency peak epsilon(M) (Moster+2013, Behroozi+2013). Writes
analysis.json and the figures. Idempotent; safe to re-run as compute fills in.
"""
import json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
CEP = HERE.parent
EPOCH = CEP / "epoch_check"
HG = CEP / "halo_grain"
sys.path.insert(0, str(HG)); sys.path.insert(0, str(CEP))
sys.path.insert(0, str(HERE))
import s_of_a as S_mod
import shm_models as SHM

# lift CPL-projection funcs verbatim (defs only), as the pipeline scripts do
src = (EPOCH / "cpl_projection.py").read_text()
cpl = {}
exec(compile(src.split("# 4. Run.")[0], str(EPOCH / "cpl_projection.py"), "exec"), cpl)
make_f_fw = cpl["make_f_fw"]; project_distance = cpl["project_distance"]
project_rho = cpl["project_rho"]; crossing_z = cpl["crossing_z"]

DESI_W = (-0.838, -0.62)
COV = np.array([[0.055**2, -0.7*0.055*0.20], [-0.7*0.055*0.20, 0.20**2]])
COVINV = np.linalg.inv(COV)
def maha(w0, wa):
    d = np.array([w0 - DESI_W[0], wa - DESI_W[1]])
    return float(np.sqrt(d @ COVINV @ d))

OM_PROJ = 0.3155
PLATEAU_TOL = 0.05    # plateau = z-range with S >= (1-tol)*Smax

# real DESI DR2 likelihood (import module; it loads DESI data + builds LCDM baseline)
try:
    import likelihood_fit as LK    # from desi_likelihood_v2 (added to path below)
    HAVE_LK = True
except Exception:
    sys.path.insert(0, str(CEP / "desi_likelihood_v2"))
    try:
        import likelihood_fit as LK
        HAVE_LK = True
    except Exception as e:
        print("likelihood_fit import failed:", e); HAVE_LK = False
LCDM_CHI2 = None
if HAVE_LK:
    LCDM_CHI2 = LK.profile_fixedshape(LK.f_lcdm, use_cmb=True)["chi2"]

def curve_from_records(records):
    """records: dict snap->rec. Return sorted finite (a, S, z, k, n_in, capped)."""
    rows = []
    for k, r in records.items():
        if r.get("S") is None or not np.isfinite(r["S"]) or r["S"] <= 0:
            continue
        rows.append((r["a"], r["S"], r["z"], r["k"], r.get("n_in_bin", r["k"]),
                     bool(r.get("capped", False))))
    rows.sort()
    if not rows:
        return None
    a = np.array([x[0] for x in rows]); Sa = np.array([x[1] for x in rows])
    z = np.array([x[2] for x in rows]); kk = np.array([x[3] for x in rows])
    nin = np.array([x[4] for x in rows]); cap = np.array([x[5] for x in rows])
    return dict(a=a, S=Sa, z=z, k=kk, n_in=nin, capped=cap)

def peak_and_plateau(a, Sa):
    """Global-max epoch + plateau breadth (fine_grid-validated; avoids the wiggle-
    fragile last-sign-change spline finder)."""
    imax = int(np.argmax(Sa))
    z = 1.0 / a - 1.0
    zpeak = float(z[imax])
    interior = 0 < imax < len(Sa) - 1
    thresh = (1 - PLATEAU_TOL) * Sa[imax]
    on = Sa >= thresh
    z_on = z[on]
    return dict(z_peak=zpeak, interior=bool(interior),
                z_plateau_lo=float(z_on.min()), z_plateau_hi=float(z_on.max()),
                S_max=float(Sa[imax]), a_peak=float(a[imax]))

def analyze_bin(rec, do_likelihood=False):
    cv = curve_from_records(rec["records"])
    out = {"center": rec["center"], "lo": rec["lo"], "hi": rec["hi"], "box": rec["box"]}
    if cv is None or len(cv["a"]) < 5:
        out["n_points"] = 0 if cv is None else len(cv["a"])
        out["ok"] = False
        return out
    a, Sa = cv["a"], cv["S"]
    out["n_points"] = len(a)
    out["ok"] = True
    out["n_capped_snaps"] = int(cv["capped"].sum())
    out["k_range"] = [int(cv["k"].min()), int(cv["k"].max())]
    out["n_in_bin_range"] = [int(cv["n_in"].min()), int(cv["n_in"].max())]
    out["a"] = a.tolist(); out["S"] = Sa.tolist(); out["z"] = cv["z"].tolist()
    out.update(peak_and_plateau(a, Sa))
    # CPL projection -> Mahalanobis (representative-error, both boxes)
    f = make_f_fw(a, Sa)
    w0, wa, _ = project_distance(f, Om=OM_PROJ, use_cmb=True)
    out["cpl_dist"] = dict(w0=float(w0), wa=float(wa),
                           cross_z=crossing_z(w0, wa), maha=maha(w0, wa))
    w0r, war, _ = project_rho(f, Om=OM_PROJ)
    out["cpl_rho"] = dict(w0=float(w0r), wa=float(war),
                          cross_z=crossing_z(w0r, war), maha=maha(w0r, war))
    # real DESI DR2 likelihood (TNG300 only)
    if do_likelihood and HAVE_LK:
        f_lk = LK.make_f_fw(a, Sa)
        fw = LK.profile_fixedshape(f_lk, use_cmb=True)
        out["likelihood"] = dict(chi2=float(fw["chi2"]), Om=float(fw["Om"]),
                                 chi2_minus_LCDM=float(fw["chi2"] - LCDM_CHI2),
                                 LCDM_chi2=float(LCDM_CHI2))
    return out

def main():
    res = json.load(open(HERE / "results.json"))
    A = {"provenance": {
            "results": "shm_anchor/results.json (compute_scan.py)",
            "cpl_projection": "epoch_check/cpl_projection.py project_distance (representative "
                              "DESI DR2 fractional errors; Mahalanobis vs DESI (-0.838,-0.62), "
                              "cov diag (0.055,0.20) rho=-0.7)",
            "likelihood": "desi_likelihood_v2/likelihood_fit.py profile_fixedshape (real DESI "
                          "DR2 BAO vector+cov, 13 meas / 7 tracers, + CMB theta* anchor); "
                          "TNG300 bins only; LCDM baseline chi2 = %s" % (
                              None if LCDM_CHI2 is None else round(LCDM_CHI2, 3)),
            "peak_stat": "GLOBAL max epoch + %d%% plateau breadth (global-max is the "
                         "fine_grid-validated robust statistic)" % int(PLATEAU_TOL*100),
            "h": SHM.H_TNG},
         "shm": {}, "tng300_bins": {}, "tng100_bins": {},
         "tng300_thresholds": {}, "jackknife": {}}

    # SHM literature curves (fetched-not-rederived)
    zg = np.linspace(0.0, 3.0, 61)
    A["shm"] = {
        "note": "FETCHED-NOT-REDERIVED. Moster+2013 (arXiv:1205.5807) & Behroozi+2013 "
                "(arXiv:1207.6105) fitted forms; masses in Msun (paper units), also given "
                "in Msun/h at h=0.6774. UniverseMachine (Behroozi+2019) peak ~10^12 Msun "
                "drifting up with z, cited as cross-check only.",
        "z": zg.tolist(),
        "moster_peak_logMh_Msun": [SHM.moster_peak_logMh(z) for z in zg],
        "behroozi_peak_logMh_Msun": [SHM.behroozi_peak_logMh(z) for z in zg],
        "moster_peak_logMh_Msunh": [SHM.Msun_to_Msunh(SHM.moster_peak_logMh(z)) for z in zg],
        "behroozi_peak_logMh_Msunh": [SHM.Msun_to_Msunh(SHM.behroozi_peak_logMh(z)) for z in zg],
        "peaks_z0": {
            "moster_Msun": SHM.moster_peak_logMh(0.0),
            "behroozi_Msun": SHM.behroozi_peak_logMh(0.0),
            "moster_Msunh": SHM.Msun_to_Msunh(SHM.moster_peak_logMh(0.0)),
            "behroozi_Msunh": SHM.Msun_to_Msunh(SHM.behroozi_peak_logMh(0.0))},
        "peaks_z0p5": {
            "moster_Msunh": SHM.Msun_to_Msunh(SHM.moster_peak_logMh(0.5)),
            "behroozi_Msunh": SHM.Msun_to_Msunh(SHM.behroozi_peak_logMh(0.5))},
    }

    for c, rec in sorted(res.get("tng300_bins", {}).items(), key=lambda kv: float(kv[0])):
        A["tng300_bins"][c] = analyze_bin(rec, do_likelihood=True)
    for c, rec in sorted(res.get("tng100_bins", {}).items(), key=lambda kv: float(kv[0])):
        A["tng100_bins"][c] = analyze_bin(rec, do_likelihood=False)
    for tk, rec in sorted(res.get("tng300_thresholds", {}).items(),
                          key=lambda kv: float(kv[1]["thr"])):
        rec2 = {"center": float(np.log10(rec["thr"])), "lo": rec["thr"], "hi": np.inf,
                "box": rec["box"], "records": rec["records"]}
        A["tng300_thresholds"][tk] = analyze_bin(rec2, do_likelihood=True)

    # jackknife on anchor bin -> peak-epoch & maha spread
    for c, jst in res.get("tng300_bins_jackknife", {}).items():
        prim = res["tng300_bins"].get(c)
        if prim is None:
            continue
        cv = curve_from_records(prim["records"])
        if cv is None:
            continue
        # jackknife curves share the same a-grid as primary (per snap)
        snaps = sorted(prim["records"].keys(),
                       key=lambda s: prim["records"][s]["a"])
        a_full = np.array([prim["records"][s]["a"] for s in snaps])
        zpk, mah = [], []
        n_oct = 0
        for o in range(8):
            jk = jst.get(str(o), {})
            if len(jk) < len(snaps):
                continue
            Sj = np.array([jk[s] for s in snaps])
            ok = np.isfinite(Sj) & (Sj > 0)
            aj, Sjo = a_full[ok], Sj[ok]
            if len(aj) < 5:
                continue
            n_oct += 1
            zpk.append(peak_and_plateau(aj, Sjo)["z_peak"])
            f = make_f_fw(aj, Sjo)
            w0, wa, _ = project_distance(f, Om=OM_PROJ, use_cmb=True)
            mah.append(maha(w0, wa))
        if n_oct >= 2:
            jkerr = lambda v: float(np.sqrt((len(v)-1)/len(v) * np.sum((np.array(v)-np.mean(v))**2)))
            A["jackknife"][c] = dict(n_octants=n_oct,
                                     z_peak_mean=float(np.mean(zpk)), z_peak_err68=jkerr(zpk),
                                     maha_mean=float(np.mean(mah)), maha_err68=jkerr(mah))

    (HERE / "analysis.json").write_text(json.dumps(A, indent=1))
    print("wrote analysis.json")

    # ---- compact console table ----
    def show(title, store, likelihood):
        print("=" * 92); print(title)
        hdr = f"{'center':>7} {'npt':>4} {'cap':>4} {'k_max':>7} {'z_peak':>7} {'plateau':>13} {'w0':>7} {'wa':>7} {'maha':>6}"
        if likelihood: hdr += f" {'chi2':>7} {'dLCDM':>7}"
        print(hdr)
        for c, b in store.items():
            if not b.get("ok"):
                print(f"{float(c):7.2f}  (insufficient points: n={b.get('n_points',0)})"); continue
            cd = b["cpl_dist"]
            row = (f"{b['center']:7.2f} {b['n_points']:4d} {b['n_capped_snaps']:4d} "
                   f"{b['k_range'][1]:7d} {b['z_peak']:7.3f} "
                   f"{('[%.2f,%.2f]'%(b['z_plateau_lo'],b['z_plateau_hi'])):>13} "
                   f"{cd['w0']:7.3f} {cd['wa']:7.3f} {cd['maha']:6.2f}")
            if likelihood and "likelihood" in b:
                row += f" {b['likelihood']['chi2']:7.2f} {b['likelihood']['chi2_minus_LCDM']:7.2f}"
            print(row)
    hmsg = (f"SHM peak (Msun/h): Moster z0={A['shm']['peaks_z0']['moster_Msunh']:.2f} "
            f"z0.5={A['shm']['peaks_z0p5']['moster_Msunh']:.2f} | "
            f"Behroozi z0={A['shm']['peaks_z0']['behroozi_Msunh']:.2f} "
            f"z0.5={A['shm']['peaks_z0p5']['behroozi_Msunh']:.2f}")
    print(hmsg)
    show("TNG300 BINS (box 205)", A["tng300_bins"], True)
    show("TNG100 BINS (box 75)", A["tng100_bins"], False)
    show("TNG300 THRESHOLDS (sensitivity, cumulative >M, coarse grid)",
         A["tng300_thresholds"], True)
    if A["jackknife"]:
        print("anchor-bin jackknife:", A["jackknife"])
    return A

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Counterfactual cosmology sweep for the dark-energy law  rho_DE ~ S,
    1 + w(a) = -(1/3) d ln S / d ln a.

Reuses the FROZEN op_B B-total estimator from ../halo_grain/halo_grain.py over
CAMELS IllustrisTNG 1P parameter-variation boxes (Om axis p1, sigma8 axis p2).
Same 25 Mpc/h box, same snapshots, same estimator conventions. CPU only.

Tests law-ness vs coincidence: does S(a) co-vary with each universe's OWN
formation history (mechanism lock S-peak <-> k-peak), in the predicted direction?

See DECISIONS.md for the pre-registered predictions and verdict rule.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CEP = HERE.parent                       # cosmo_entropic_potential/
HG = CEP / "halo_grain"
sys.path.insert(0, str(CEP))
sys.path.insert(0, str(HG))

DATA = HERE / "data"
os.environ.setdefault("HG_SCRATCH", str(DATA / "_hg_scratch"))  # keep halo_grain import off stale path

import s_of_a as S                       # cosmology globals + PowerSpectrum + sign helpers
import halo_grain as HGmod               # frozen op_B / build_halo_C / series_sign

FIG = HERE / "figures"
DATA.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

MIRROR = "https://users.flatironinstitute.org/~camels/Sims/IllustrisTNG/1P/"
SNAPS = HGmod.SNAPS                       # [32,40,48,54,60,66,72,78,84,90], z=3->0
BOX = HGmod.BOX                           # 25 Mpc/h
MASS_UNIT = HGmod.MASS_UNIT               # 1e10 Msun/h
THRESH = 1e11                             # frozen rule's selection at 25 Mpc/h resolution
RULE_MIN_HALOS_Z3 = 200

# --- the 9 unique cosmologies (fiducial p1_0 == p2_0, run once) ---
# sigma8 for p2 is the frozen CAMELS 1P design (header does not store it); Om read from header.
COSMOS = [
    # name,        run dir,     axis,      Om,   sigma8
    ("Om=0.1",    "1P_p1_n2",  "Om",      0.1,  0.8),
    ("Om=0.2",    "1P_p1_n1",  "Om",      0.2,  0.8),
    ("fiducial",  "1P_p1_0",   "both",    0.3,  0.8),
    ("Om=0.4",    "1P_p1_1",   "Om",      0.4,  0.8),
    ("Om=0.5",    "1P_p1_2",   "Om",      0.5,  0.8),
    ("s8=0.6",    "1P_p2_n2",  "sigma8",  0.3,  0.6),
    ("s8=0.7",    "1P_p2_n1",  "sigma8",  0.3,  0.7),
    ("s8=0.9",    "1P_p2_1",   "sigma8",  0.3,  0.9),
    ("s8=1.0",    "1P_p2_2",   "sigma8",  0.3,  1.0),
]

FID_H, FID_NS, FID_OB = 0.6711, 0.9624, 0.049


def load_snapshot(run, snap):
    """Fields-only ranged HDF5 read, cached per (run, snap). Returns z,a,pos,m200."""
    cache = DATA / f"{run}_{snap:03d}.npz"
    if cache.exists():
        d = np.load(cache)
        return dict(z=float(d["z"]), a=float(d["a"]), pos=d["pos"], m200=d["m200"])
    import fsspec, h5py
    url = f"{MIRROR}{run}/groups_{snap:03d}.hdf5"
    with h5py.File(fsspec.open(url, "rb").open(), "r") as h:
        z = float(h["Header"].attrs["Redshift"])
        om0 = float(h["Header"].attrs["Omega0"])
        if "Group/GroupPos" in h:
            pos = h["Group/GroupPos"][:].astype(np.float64) / 1000.0
            m200 = h["Group/Group_M_Crit200"][:].astype(np.float64) * MASS_UNIT
        else:                                    # no groups at this snapshot
            pos = np.zeros((0, 3)); m200 = np.zeros(0)
    a = 1.0 / (1.0 + z)
    np.savez(cache, z=z, a=a, pos=pos, m200=m200, om0=om0)
    return dict(z=z, a=a, pos=pos, m200=m200)


def patch_cosmology(Om, sigma8):
    """Patch s_of_a module globals to this cosmology and rebuild PowerSpectrum.
    Bias & growth cancel in the normalized C; P(k) SHAPE (Om) and the point set carry it."""
    S.OM = Om
    S.OL = 1.0 - Om
    S.H0H = FID_H
    S.OB = FID_OB
    S.NS = FID_NS
    S.SIGMA8 = sigma8
    return S.PowerSpectrum(transfer="eh98", window="tophat", sigma8=sigma8)


def peak_epoch(a_arr, y_arr):
    """z of argmax(y) on the common a-grid + whether it is interior (not at a grid edge)."""
    a = np.asarray(a_arr); y = np.asarray(y_arr, float)
    ok = np.isfinite(y)
    a, y = a[ok], y[ok]
    order = np.argsort(a); a, y = a[order], y[order]
    if len(a) < 3:
        return dict(z=np.nan, a=np.nan, interior=False, n=int(len(a)))
    i = int(np.argmax(y))
    interior = 0 < i < len(a) - 1
    return dict(z=float(1.0 / a[i] - 1.0), a=float(a[i]), interior=interior, n=int(len(a)))


def run_cosmology(name, run, Om, sigma8):
    print(f"\n=== {name}  ({run})  Om={Om}  sigma8={sigma8} ===", flush=True)
    snaps_data = []
    for snap in SNAPS:
        sd = load_snapshot(run, snap)
        snaps_data.append(sd)
        print(f"  snap {snap:03d} z={sd['z']:5.3f} a={sd['a']:5.3f} "
              f"Ngroups={len(sd['m200']):6d} k(>1e11)={int((sd['m200']>THRESH).sum()):5d}"
              + (f" Mmax={sd['m200'].max():.2e}" if len(sd['m200']) else ""), flush=True)

    ps = patch_cosmology(Om, sigma8)

    # k(a) above the frozen threshold + the rule compliance flag
    k_of_a = [dict(z=sd["z"], a=sd["a"], k=int((sd["m200"] > THRESH).sum()))
              for sd in snaps_data]
    a_grid = np.array([r["a"] for r in k_of_a])
    k_arr = np.array([r["k"] for r in k_of_a])
    # z=3 is the highest-z (smallest-a) snapshot
    k_z3 = int(k_arr[np.argmin(a_grid)])
    rule_ok = bool(k_z3 >= RULE_MIN_HALOS_Z3)

    # frozen op_B B-total  (fixed_k=None -> k grows; cap=1000, n_draw=8, R_smooth=1.0)
    recs = HGmod.op_B(ps, snaps_data, THRESH, R_smooth=1.0, cap=1000, n_draw=8, fixed_k=None)
    sg = HGmod.series_sign(recs, key="S")

    S_peak = peak_epoch([r["a"] for r in recs], [r.get("S", np.nan) for r in recs])
    k_peak = peak_epoch(a_grid, k_arr)

    # phantom-divide crossing = S-peak epoch (dlnS/dlna = 0). Interior peak => a real crossing.
    crossing_z = S_peak["z"] if S_peak["interior"] else None

    rec_out = dict(
        name=name, run=run, Om=Om, sigma8=sigma8,
        k_of_a=k_of_a, k_z3=k_z3, rule_endorses_1e11=rule_ok, rule_min=RULE_MIN_HALOS_Z3,
        opB=recs,
        S_peak_z=S_peak["z"], S_peak_a=S_peak["a"], S_peak_interior=S_peak["interior"],
        k_peak_z=k_peak["z"], k_peak_a=k_peak["a"], k_peak_interior=k_peak["interior"],
        crossing_z=crossing_z,
        w_today=sg.get("w_today", np.nan) if sg.get("usable") else np.nan,
        w0=sg.get("w0", np.nan) if sg.get("usable") else np.nan,
        wa=sg.get("wa", np.nan) if sg.get("usable") else np.nan,
        global_slope=sg.get("global_slope", np.nan) if sg.get("usable") else np.nan,
        w_global=sg.get("w_global", np.nan) if sg.get("usable") else np.nan,
        phantom_today=sg.get("phantom_today") if sg.get("usable") else None,
    )
    print(f"  -> k(z=3)={k_z3} rule_ok={rule_ok} | "
          f"S-peak z={S_peak['z']:.3f}(int={S_peak['interior']}) "
          f"k-peak z={k_peak['z']:.3f} | w_today={rec_out['w_today']:.3f} "
          f"crossing_z={crossing_z}", flush=True)
    return rec_out


def main():
    results = dict(
        description="counterfactual cosmology sweep — dark-energy law law-ness test",
        data="CAMELS IllustrisTNG 1P (Flatiron public mirror)",
        box_Mpc_h=BOX, snaps=SNAPS, threshold_Msun_h=THRESH,
        estimator="frozen op_B B-total from ../halo_grain (bias & growth cancel)",
        sign_law="1 + w = -(1/3) dlnS/dlna",
        desi=dict(w0=-0.838, wa=-0.62),
        fixed=dict(h=FID_H, ns=FID_NS, Ob=FID_OB),
        cosmologies=[],
    )
    out_json = HERE / "results.json"
    for name, run, axis, Om, sigma8 in COSMOS:
        rec = run_cosmology(name, run, Om, sigma8)
        rec["axis"] = axis
        results["cosmologies"].append(rec)
        with open(out_json, "w") as f:               # incremental flush
            json.dump(results, f, indent=1, default=float)
    print(f"\nWrote {out_json}", flush=True)
    make_figures(results)
    make_verdict(results)


# ---------------------------------------------------------------------------
def _sweep_rows(results):
    return results["cosmologies"]


def make_figures(results):
    rows = _sweep_rows(results)
    om_rows = [r for r in rows if r["axis"] in ("Om", "both")]
    s8_rows = [r for r in rows if r["axis"] in ("sigma8", "both")]
    om_rows.sort(key=lambda r: r["Om"])
    s8_rows.sort(key=lambda r: r["sigma8"])

    # (a) mechanism lock: S-peak z vs k-peak z, all cosmologies, one line
    fig, ax = plt.subplots(figsize=(6, 6))
    for r in rows:
        if np.isfinite(r["S_peak_z"]) and np.isfinite(r["k_peak_z"]):
            mk = "o" if r["axis"] in ("Om", "both") else "s"
            col = "C0" if r["axis"] in ("Om", "both") else "C3"
            ax.scatter(r["k_peak_z"], r["S_peak_z"], marker=mk, c=col, s=80,
                       edgecolor="k", zorder=3)
            ax.annotate(r["name"], (r["k_peak_z"], r["S_peak_z"]),
                        fontsize=7, xytext=(4, 4), textcoords="offset points")
    lim = [-0.1, 3.1]
    ax.plot(lim, lim, "k--", lw=1, alpha=0.6, label="identity")
    kp = np.array([r["k_peak_z"] for r in rows if np.isfinite(r["S_peak_z"])])
    sp = np.array([r["S_peak_z"] for r in rows if np.isfinite(r["S_peak_z"])])
    if len(kp) >= 3:
        cc = np.corrcoef(kp, sp)[0, 1]
        rms = float(np.sqrt(np.mean((sp - kp) ** 2)))
        ax.set_title(f"Mechanism lock across 9 universes\ncorr={cc:.3f}, RMS Δz={rms:.3f}")
    ax.set_xlabel("k-peak epoch  z (this universe's own formation turnover)")
    ax.set_ylabel("S-peak epoch  z (entropic-potential crossing)")
    ax.set_xlim(lim); ax.set_ylim(lim); ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIG / "fig1_mechanism_lock.png", dpi=130)
    plt.close(fig)

    # (b) crossing epoch vs Om and vs sigma8
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, rws, key, lab in ((axes[0], om_rows, "Om", "Omega_m"),
                              (axes[1], s8_rows, "sigma8", "sigma8")):
        x = [r[key] for r in rws]
        cz = [r["crossing_z"] if r["crossing_z"] is not None else np.nan for r in rws]
        spz = [r["S_peak_z"] for r in rws]
        ax.plot(x, spz, "o-", c="C0", label="S-peak z (crossing)")
        for xi, ci in zip(x, cz):
            if not np.isfinite(ci):
                ax.scatter([xi], [3.0], marker="v", c="grey", zorder=3)
        ax.set_xlabel(lab); ax.set_ylabel("crossing / S-peak epoch  z")
        ax.set_title(f"Covariation vs {lab}\n(prediction: rises with {lab})")
        ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(FIG / "fig2_covariation.png", dpi=130)
    plt.close(fig)

    # (c) w_today across the sweep
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, rws, key, lab in ((axes[0], om_rows, "Om", "Omega_m"),
                              (axes[1], s8_rows, "sigma8", "sigma8")):
        x = [r[key] for r in rws]
        w = [r["w_today"] for r in rws]
        ax.plot(x, w, "o-", c="C2")
        ax.axhline(-1.0, ls="--", c="k", alpha=0.6, label="phantom divide")
        ax.axhline(-0.838, ls=":", c="C3", alpha=0.7, label="DESI w0")
        ax.set_xlabel(lab); ax.set_ylabel("w_today")
        ax.set_title(f"w_today vs {lab}"); ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(FIG / "fig3_w_today.png", dpi=130)
    plt.close(fig)
    print("Wrote figures.", flush=True)


def make_verdict(results):
    rows = _sweep_rows(results)
    kp = np.array([r["k_peak_z"] for r in rows])
    sp = np.array([r["S_peak_z"] for r in rows])
    ok = np.isfinite(kp) & np.isfinite(sp)
    cc = float(np.corrcoef(kp[ok], sp[ok])[0, 1]) if ok.sum() >= 3 else np.nan
    rms = float(np.sqrt(np.mean((sp[ok] - kp[ok]) ** 2))) if ok.sum() else np.nan

    om_rows = sorted([r for r in rows if r["axis"] in ("Om", "both")], key=lambda r: r["Om"])
    s8_rows = sorted([r for r in rows if r["axis"] in ("sigma8", "both")], key=lambda r: r["sigma8"])

    def slope(rws, key, yk):
        x = np.array([r[key] for r in rws], float)
        y = np.array([r[yk] if r[yk] is not None else np.nan for r in rws], float)
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() < 2:
            return np.nan
        return float(np.polyfit(x[m], y[m], 1)[0])

    verdict = dict(
        mechanism_lock_corr=cc, mechanism_lock_rms_dz=rms,
        crossing_vs_Om_slope=slope(om_rows, "Om", "S_peak_z"),
        crossing_vs_sigma8_slope=slope(s8_rows, "sigma8", "S_peak_z"),
        w_today_vs_Om_slope=slope(om_rows, "Om", "w_today"),
        w_today_vs_sigma8_slope=slope(s8_rows, "sigma8", "w_today"),
    )
    results["verdict_stats"] = verdict
    with open(HERE / "results.json", "w") as f:
        json.dump(results, f, indent=1, default=float)
    print("\n==== VERDICT STATS ====")
    print(json.dumps(verdict, indent=1))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Merge the per-snapshot shot-null results, propagate to Delta w by the frozen
w_implication.py recipe, and score the pre-registered ladder in DECISIONS.md."""
import json, os, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_RES = os.path.abspath(os.path.join(HERE, "..", "results.json"))
NULLS = ["S0", "S0f", "S1", "S1b"]
CFG_LABEL = {"A": "line m=6, 4.27 Mpc/h (PRIMARY)", "B": "line m=6, 6.41 Mpc/h",
             "C": "block m=8, 4.27 Mpc/h"}
FROZEN_DW = {"A": -0.005, "B": -0.012, "C": -0.017}   # SUMMARY.md table


def dlnS_dlna_last2(a, S):
    lnS = np.log(np.clip(S, 1e-12, None)); lna = np.log(a)
    return (lnS[-1] - lnS[-2]) / (lna[-1] - lna[-2])


def dlnS_dlna_ols(a, S):
    lnS = np.log(np.clip(S, 1e-12, None)); lna = np.log(a)
    return float(np.polyfit(lna, lnS, 1)[0])


def dlnS_dlna_ends(a, S):
    """endpoint slope z=3 -> z=0: what the frozen SUMMARY table actually reports."""
    lnS = np.log(np.clip(S, 1e-12, None)); lna = np.log(a)
    return (lnS[-1] - lnS[0]) / (lna[-1] - lna[0])


def w_from(a, S_2pt, S_true):
    out = {}
    for lab, f in (("last2", dlnS_dlna_last2), ("ols", dlnS_dlna_ols),
                   ("ends", dlnS_dlna_ends)):
        w2 = -1 - f(a, S_2pt) / 3.0
        wt = -1 - f(a, S_true) / 3.0
        out[lab] = dict(w0_2pt=float(w2), w0_true=float(wt), delta_w=float(wt - w2))
    return out


def main():
    files = sorted(glob.glob(os.path.join(HERE, "results_snap*.json")))
    snaps = [json.load(open(f)) for f in files]
    snaps = [s for s in snaps if s.get("configs")]
    snaps.sort(key=lambda s: -s["z"])          # z descending => a ascending
    out = {"description": "copula_stress tier-3 gap against a shot/Poisson-matched null "
                          "(2026-07-21); frozen continuous null retained side by side.",
           "snapshots": [s["snap"] for s in snaps], "z": [s["z"] for s in snaps],
           "configs": {}, "tie": {}, "ngp": {}, "verdict": {}}

    frozen = json.load(open(FROZEN_RES))["tier3"]
    fz = {}
    for s in frozen["snapshots"]:
        for c in s["configs"]:
            if c["ng"] == 48 and c["template"] == "line" and c["sep"] == 1:
                fz.setdefault("A", {})[round(s["z"], 2)] = c["gap_matched"]
            if c["ng"] == 32 and c["template"] == "line" and c["sep"] == 1:
                fz.setdefault("B", {})[round(s["z"], 2)] = c["gap_matched"]
            if c["ng"] == 48 and c["template"] == "block2":
                fz.setdefault("C", {})[round(s["z"], 2)] = c["gap_matched"]

    print("=" * 100)
    print("copula_stress higher-order gap: FROZEN CONTINUOUS NULL vs SHOT-MATCHED NULL")
    print("=" * 100)

    for cid in ("A", "B", "C"):
        rows = [(s["z"], s["a"], s["configs"][cid]) for s in snaps if cid in s["configs"]]
        if len(rows) < 3:
            continue
        a = np.array([r[1] for r in rows]); z = np.array([r[0] for r in rows])
        Ig = np.array([r[2]["real"]["I_gauss"] for r in rows])
        S_2pt = 2 * Ig
        rec = dict(label=CFG_LABEL[cid], z=list(map(float, z)), a=list(map(float, a)),
                   I_gauss_real=list(map(float, Ig)), rows={}, dw={})

        print(f"\n### config {cid}: {CFG_LABEL[cid]}   (ng={rows[0][2]['cfg']['ng']}, "
              f"N={rows[0][2]['N']}, tied-cell frac {rows[0][2]['tied_frac']:.3f})")
        hdr = (f"{'z':>5} {'I_gauss':>8} {'frozen(json)':>12} {'gap_S0':>9} {'gapc_S0':>9} "
               f"{'gapc_S0f':>9} {'gapc_S1':>9} {'z_S1':>7} {'gapc_S1b':>9} "
               f"{'dIg_S1':>7} {'clip':>6} {'A':>5}")
        print(hdr)
        for (zz, aa, c) in rows:
            fzv = fz.get(cid, {}).get(round(zz, 2), float("nan"))
            print(f"{zz:5.2f} {c['real']['I_gauss']:8.4f} {fzv:12.4f} "
                  f"{c['vs_S0']['gap']:9.4f} {c['vs_S0']['gapc']:9.4f} "
                  f"{c['vs_S0f']['gapc']:9.4f} {c['vs_S1']['gapc']:9.4f} "
                  f"{c['vs_S1']['z']:7.1f} {c['vs_S1b']['gapc']:9.4f} "
                  f"{c['vs_S1']['Ig_rel']:7.3f} {c['S1_cal']['clip_frac']:6.3f} "
                  f"{c['S1_cal']['A']:5.2f}")
            rec["rows"][f"{zz:.2f}"] = {k: c[k] for k in
                                        ("vs_S0", "vs_S0f", "vs_S1", "vs_S1b", "tied_frac")}
            rec["rows"][f"{zz:.2f}"]["I_gauss_real"] = c["real"]["I_gauss"]
            rec["rows"][f"{zz:.2f}"]["S1_cal"] = c["S1_cal"]

        # ---- Delta w propagation (frozen recipe): S_true = 2*(Ig + gap)
        variants = {}
        fzg = [fz.get(cid, {}).get(round(zz, 2), np.nan) for (zz, _, _) in rows]
        if not any(np.isnan(fzg)):
            variants["frozen_json_gap"] = np.array(fzg)   # frozen gaps, frozen recipe
        variants["frozen_raw_S0"] = np.array([r[2]["vs_S0"]["gap"] for r in rows])
        for k in NULLS:
            variants[f"gapc_{k}"] = np.array([r[2][f"vs_{k}"]["gapc"] for r in rows])
        print(f"\n  Delta w (sign law 1+w = -1/3 dlnS/dlna; frozen SUMMARY row = "
              f"{FROZEN_DW[cid]:+.3f})")
        print(f"  {'variant':>16} {'gap(z=0)':>9} {'gap(z=3)':>9} {'dw_ends':>9} "
              f"{'dw_ols':>9} {'dw_last2':>9}")
        for name, g in variants.items():
            S_true = 2 * (Ig + g)
            w = w_from(a, S_2pt, S_true)
            rec["dw"][name] = dict(gap=list(map(float, g)), **w)
            print(f"  {name:>16} {g[-1]:9.4f} {g[0]:9.4f} "
                  f"{w['ends']['delta_w']:+9.4f} {w['ols']['delta_w']:+9.4f} "
                  f"{w['last2']['delta_w']:+9.4f}")
        out["configs"][cid] = rec

    # ---------------- tie-break decomposition ----------------
    print("\n" + "=" * 100)
    print("(a) TIE-BREAK decomposition, primary config A (ng=48 CIC, tied-cell frac shown)")
    print(f"{'z':>5} {'tied':>6} {'frozen':>9} {'ns_avg':>9} {'ns_pos':>9} {'ns_rand':>9} "
          f"{'artifact_frac':>14}")
    tie_fracs = []
    for s in snaps:
        t = s.get("tie")
        if not t:
            continue
        tf = s["configs"]["A"]["tied_frac"]
        print(f"{s['z']:5.2f} {tf:6.3f} {t['frozen']['gap']:9.4f} {t['ns_avg']['gap']:9.4f} "
              f"{t['ns_pos']['gap']:9.4f} {t['ns_rand']['gap']:9.4f} "
              f"{t['tie_artifact_fraction_gap']:14.3f}")
        tie_fracs.append(t["tie_artifact_fraction_gap"])
        out["tie"][f"{s['z']:.2f}"] = {k: t[k] for k in
                                       ("frozen", "ns_avg", "ns_pos", "ns_rand",
                                        "tie_artifact_fraction_gap",
                                        "tie_artifact_fraction_gapc")}

    # ---------------- NGP vs CIC ----------------
    print("\n" + "=" * 100)
    print("(b) ASSIGNMENT sensitivity, primary config A: NGP (no anti-aliasing) vs CIC")
    print(f"{'z':>5} {'tied_NGP':>9} {'tied_CIC':>9} {'gapc_S0_NGP':>12} {'gapc_S1_NGP':>12} "
          f"{'gapc_S0_CIC':>12} {'gapc_S1_CIC':>12}")
    for s in snaps:
        n = s.get("ngp")
        if not n:
            continue
        cA = s["configs"]["A"]
        print(f"{s['z']:5.2f} {n['tied_frac']:9.3f} {cA['tied_frac']:9.3f} "
              f"{n['vs_S0']['gapc']:12.4f} {n['vs_S1']['gapc']:12.4f} "
              f"{cA['vs_S0']['gapc']:12.4f} {cA['vs_S1']['gapc']:12.4f}")
        out["ngp"][f"{s['z']:.2f}"] = dict(tied_ngp=n["tied_frac"], vs_S0=n["vs_S0"],
                                           vs_S1=n["vs_S1"])

    # ---------------- pre-registered verdict ----------------
    print("\n" + "=" * 100)
    print("PRE-REGISTERED VERDICT (thresholds from DECISIONS.md, |dw| = 0.05)")
    v = {}
    for cid in out["configs"]:
        r = out["configs"][cid]
        dw = r["dw"]["gapc_S1"]["ends"]["delta_w"]        # frozen-comparable slope
        dw_ols = r["dw"]["gapc_S1"]["ols"]["delta_w"]
        dw_l2 = r["dw"]["gapc_S1"]["last2"]["delta_w"]
        g = np.array(r["dw"]["gapc_S1"]["gap"])
        zsc = [r["rows"][k]["vs_S1"]["z"] for k in r["rows"]]
        consistent_zero = all(abs(x) < 2 for x in zsc)
        blowup = abs(g[-1]) > 2 * abs(g[0])
        v[cid] = dict(delta_w_ends=float(dw), delta_w_ols=float(dw_ols),
                      delta_w_last2=float(dw_l2),
                      passes_dw=bool(max(abs(dw), abs(dw_ols), abs(dw_l2)) <= 0.05), gapc_S1_z=list(map(float, zsc)),
                      all_z_within_2sigma=bool(consistent_zero), lowz_blowup=bool(blowup))
        print(f"  cfg {cid}: dw(gapc_S1) ends={dw:+.4f} ols={dw_ols:+.4f} last2={dw_l2:+.4f}  "
              f"|dw|<=0.05: {abs(dw) <= 0.05}  all |z|<2 vs S1: {consistent_zero}  "
              f"low-z blowup: {blowup}")
    n_pass = sum(1 for c in v if v[c]["passes_dw"])
    survives = v.get("A", {}).get("passes_dw", False) and n_pass >= 2
    redescribed = survives and v.get("A", {}).get("all_z_within_2sigma", False)
    out["verdict"] = dict(per_config=v, n_configs_pass=n_pass,
                          SURVIVES_AS_STATED=bool(survives and not redescribed),
                          SURVIVES_BUT_REDESCRIBED=bool(redescribed),
                          DEFENSE_FIRES=bool(not survives),
                          tie_artifact_fraction_mean=float(np.mean(tie_fracs)) if tie_fracs else None)
    print(f"\n  => SURVIVES_AS_STATED       : {out['verdict']['SURVIVES_AS_STATED']}")
    print(f"  => SURVIVES_BUT_REDESCRIBED : {out['verdict']['SURVIVES_BUT_REDESCRIBED']}")
    print(f"  => DEFENSE_FIRES            : {out['verdict']['DEFENSE_FIRES']}")
    if tie_fracs:
        print(f"  => tie-artifact fraction (argsort-argsort vs random), mean: "
              f"{np.mean(tie_fracs):+.3f}  [flag threshold 0.30]")

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote results.json")


if __name__ == "__main__":
    main()

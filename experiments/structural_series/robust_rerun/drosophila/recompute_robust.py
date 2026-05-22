"""Robust re-run — Drosophila central-complex in-corridor substrate.

Recomputes within-rung corridor occupation for the Drosophila CX under the
structural-series robust framing: debiased rho (phase-randomized surrogate
floor) + canonical participation-ratio k_eff. See PREREGISTRATION.md — written
and committed before this ran.

Datasets (real data, located on disk):
  v18  Mussells Pires 2024  — paired HDF5, EPG (60D05) + FC2 (VT065306...)
  v19  Ishida et al 2025    — folder-6 CSV, same-fly EPG (eb) + FC3 (fb2/fb5)

Estimator is the canonical one from data_fmri/fmri_corridor.py (subject_rho):
raw F -> dF/F (F0 = 5th pctile), z-score, mean|off-diag| rho_raw, debias by
phase-randomized surrogate floor, canonical k_eff = participation ratio of
covariance eigenvalues. Per recording AND walking-only subset.

Incremental output: results.json is rewritten after every recording.
"""
import json
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

OUT_DIR = Path(__file__).parent
RESULTS_JSON = OUT_DIR / "results.json"

V18_DIR = Path("/home/emoore/coherence-ratchet/.claude/worktrees/"
                "agent-acdef895a126f5e14/experiments/v18_biology/data/"
                "shared_data/EPG_FC2_imaging")
V19_DIR = Path("/home/emoore/coherence-ratchet/.claude/worktrees/"
                "agent-a4753b36bf926c6d6/experiments/v19_biology/data/"
                "ishida_folder6")

N_SURROGATE = 20
SEED = 0
MIN_T = 100
MIN_ROI = 3


# ---------------- canonical estimator (from fmri_corridor.py) ----------------

def raw_F_to_dFF(F, q=5):
    F0 = np.nanpercentile(F, q)
    if F0 <= 1e-9:
        F0 = 1e-9
    return (F - F0) / F0


def phase_randomize(x, rng):
    """Phase-randomize each column: preserves power spectrum, destroys
    cross-column correlation."""
    n = x.shape[0]
    F = np.fft.rfft(x, axis=0)
    amp = np.abs(F)
    rand = rng.uniform(-np.pi, np.pi, size=F.shape)
    rand[0] = 0.0
    if n % 2 == 0:
        rand[-1] = 0.0
    Fs = amp * np.exp(1j * rand)
    return np.fft.irfft(Fs, n=n, axis=0)


def mean_abs_offdiag(C):
    d = C.shape[0]
    return float(np.mean(np.abs(C[~np.eye(d, dtype=bool)])))


def rung_rho(ts, rng):
    """ts: (T x N) raw fluorescence. Returns dict with rho_raw, floor,
    rho_deb, k_eff_emp, k_eff_kish, or None if unusable."""
    ts = np.asarray(ts, dtype=float)
    if ts.ndim != 2 or ts.shape[0] < MIN_T:
        return None
    # raw F -> dF/F per ROI
    dff = np.column_stack([raw_F_to_dFF(ts[:, j]) for j in range(ts.shape[1])])
    # drop NaN rows, then zero-variance ROIs
    keep_rows = ~np.any(~np.isfinite(dff), axis=1)
    dff = dff[keep_rows]
    if dff.shape[0] < MIN_T:
        return None
    sd = dff.std(axis=0)
    dff = dff[:, sd > 1e-8]
    if dff.shape[1] < MIN_ROI:
        return None
    Z = (dff - dff.mean(axis=0)) / dff.std(axis=0)
    T, N = Z.shape
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

    ev = np.linalg.eigvalsh(C)
    ev = ev[ev > 1e-9]
    k_eff_emp = float((ev.sum() ** 2) / (ev ** 2).sum())
    k_eff_kish = float(N / (1.0 + rho_deb * (N - 1.0)))
    return {
        "n_timepoints": int(T), "n_rois": int(N),
        "rho_raw": rho_raw, "floor": floor, "rho_deb": rho_deb,
        "k_eff_emp": k_eff_emp, "k_eff_kish": k_eff_kish,
    }


# ---------------- dataset loaders ----------------

def v18_recordings():
    """Yield (dataset, rung, fly_id, rec_name, X_full, walk_mask)."""
    summary = pd.read_csv(V18_DIR / "summary.csv", index_col=0)
    for _, row in summary.iterrows():
        geno, rec, fly = row["genotype"], row["rec_name"], int(row["fly_id"])
        if geno == "60D05":
            rung, prefix = "EPG", "pb_c1"
        elif geno == "VT065306-AD-VT029306-DBD":
            rung, prefix = "FC2", "fb_c1"
        else:
            continue
        im_path = V18_DIR / geno / f"{rec}_im.h5"
        abf_path = V18_DIR / geno / f"{rec}_abf.h5"
        if not im_path.exists():
            continue
        im = pd.read_hdf(im_path)
        pat = re.compile(rf"^{prefix}_roi_\d+_F$")
        cols = sorted([c for c in im.columns if pat.match(c)],
                      key=lambda s: int(re.search(r"roi_(\d+)", s).group(1)))
        if len(cols) < MIN_ROI:
            continue
        X = im[cols].values.astype(np.float64)
        t_im = im["t"].values
        walk = None
        if abf_path.exists():
            walk = v18_walk_mask(t_im, pd.read_hdf(abf_path))
        yield ("v18_MussellsPires2024", rung, fly, rec, X, walk)


def v18_walk_mask(t_im, abf, win_s=3.0, forw_thresh=15.0):
    """Walking mask on imaging timebase: forward-speed convolution above
    threshold (the activity analogue used by v1's 02b derive_fixation)."""
    t_abf = abf["t"].values
    forw = abf["forw"].values
    dt = float(np.median(np.diff(t_abf)))
    win = max(3, int(round(win_s / dt)))
    kern = np.ones(win) / win
    forw_sm = np.convolve(np.abs(forw), kern, mode="same")
    walking = forw_sm >= forw_thresh
    idx = np.clip(np.searchsorted(t_abf, t_im, side="left"), 0, len(t_abf) - 1)
    return walking[idx]


def v19_recordings():
    """Yield (dataset, rung, fly_id, rec_name, X_full, walk_mask) for the
    Ishida same-fly dual-color recordings. EPG = eb_c1; FC3 = fb2_c1 +
    fb5_c1 stacked (both are FC3 fan-shaped-body layers)."""
    for rec_dir in sorted(V19_DIR.glob("*/*/")):
        im_files = list(rec_dir.glob("*_im.csv"))
        beh_files = list(rec_dir.glob("*_beh.csv"))
        if not im_files:
            continue
        im = pd.read_csv(im_files[0])
        rec = rec_dir.name
        # fly id: each recording date-folder is a distinct fly preparation
        fly = rec
        walk = None
        if beh_files:
            beh = pd.read_csv(beh_files[0])
            if "im_walking" in beh.columns and len(beh) == len(im):
                walk = beh["im_walking"].values.astype(bool)
        rungs = {
            "EPG": [c for c in im.columns if c.endswith("_eb_c1")],
            "FC3": ([c for c in im.columns if c.endswith("_fb2_c1")]
                    + [c for c in im.columns if c.endswith("_fb5_c1")]),
        }
        for rung, cols in rungs.items():
            if len(cols) < MIN_ROI:
                continue
            X = im[cols].values.astype(np.float64)
            yield ("v19_Ishida2025", rung, fly, rec, X, walk)


# ---------------- main ----------------

def main():
    rng = np.random.default_rng(SEED)
    records = []

    def flush():
        RESULTS_JSON.write_text(json.dumps(
            {"n_records": len(records), "records": records},
            indent=2, default=str))

    sources = []
    try:
        sources.append(("v18", list(v18_recordings())))
    except Exception as e:
        print(f"v18 load error: {type(e).__name__}: {e}")
        sources.append(("v18", []))
    try:
        sources.append(("v19", list(v19_recordings())))
    except Exception as e:
        print(f"v19 load error: {type(e).__name__}: {e}")
        sources.append(("v19", []))

    for tag, recs in sources:
        print(f"\n=== {tag}: {len(recs)} (recording x rung) units ===")
        for dataset, rung, fly, rec, X, walk in recs:
            res_full = rung_rho(X, rng)
            res_walk = None
            if walk is not None and walk.shape[0] == X.shape[0] \
                    and walk.sum() >= MIN_T:
                res_walk = rung_rho(X[walk], rng)
            row = {
                "dataset": dataset, "rung": rung, "fly_id": fly,
                "rec_name": rec,
                "full": res_full, "walking_only": res_walk,
                "n_walking": int(walk.sum()) if walk is not None else None,
            }
            records.append(row)
            flush()
            if res_full is None:
                print(f"  {dataset} {rung} {rec}: SKIP (unusable)")
            else:
                w = (f"  walk rho_deb={res_walk['rho_deb']:.3f}"
                     if res_walk else "  walk n/a")
                print(f"  {dataset} {rung:4s} {rec}: "
                      f"rho_raw={res_full['rho_raw']:.3f} "
                      f"floor={res_full['floor']:.3f} "
                      f"rho_deb={res_full['rho_deb']:.3f} "
                      f"k_eff_emp={res_full['k_eff_emp']:.2f} "
                      f"(N={res_full['n_rois']}){w}")

    # ---------------- per-rung summary + verdict ----------------
    def summarize(key):
        out = {}
        groups = {}
        for r in records:
            res = r[key]
            if res is None:
                continue
            gk = (r["dataset"], r["rung"])
            groups.setdefault(gk, []).append(res)
        for (dataset, rung), lst in sorted(groups.items()):
            rd = np.array([x["rho_deb"] for x in lst])
            rr = np.array([x["rho_raw"] for x in lst])
            fl = np.array([x["floor"] for x in lst])
            ke = np.array([x["k_eff_emp"] for x in lst])
            out[f"{dataset}|{rung}"] = {
                "n_recordings": len(lst),
                "rho_raw_median": float(np.median(rr)),
                "floor_median": float(np.median(fl)),
                "rho_deb_median": float(np.median(rd)),
                "rho_deb_min": float(rd.min()),
                "rho_deb_max": float(rd.max()),
                "rho_deb_p95": float(np.percentile(rd, 95)),
                "k_eff_emp_median": float(np.median(ke)),
            }
        return out

    summary_full = summarize("full")
    summary_walk = summarize("walking_only")

    # pre-registered PASS/FAIL on the walking-only (matched-activity) summary;
    # full reported alongside.
    verdict_basis = summary_walk if summary_walk else summary_full
    rung_verdicts = {}
    for key, s in verdict_basis.items():
        med = s["rho_deb_median"]
        off_chaos = med >= 0.05
        off_rigid = (med <= 0.80) and (s["rho_deb_p95"] < 0.90)
        rung_verdicts[key] = {
            "rho_deb_median": med, "off_chaos": off_chaos,
            "off_rigidity": off_rigid,
            "verdict": "PASS" if (off_chaos and off_rigid) else "FAIL",
        }
    overall = ("PASS" if all(v["verdict"] == "PASS"
                             for v in rung_verdicts.values())
               and rung_verdicts else "FAIL")

    final = {
        "n_records": len(records),
        "records": records,
        "summary_full": summary_full,
        "summary_walking_only": summary_walk,
        "rung_verdicts": rung_verdicts,
        "overall_verdict": overall,
    }
    RESULTS_JSON.write_text(json.dumps(final, indent=2, default=str))

    print("\n" + "=" * 70)
    print("PER-RUNG SUMMARY (walking-only / matched-activity)")
    print("=" * 70)
    for key, s in verdict_basis.items():
        v = rung_verdicts[key]
        print(f"  {key:32s} n={s['n_recordings']:2d}  "
              f"rho_raw={s['rho_raw_median']:.3f}  "
              f"floor={s['floor_median']:.3f}  "
              f"rho_deb={s['rho_deb_median']:.3f}  "
              f"[{s['rho_deb_min']:.3f},{s['rho_deb_max']:.3f}]  "
              f"k_eff={s['k_eff_emp_median']:.2f}  -> {v['verdict']}")
    print(f"\nOVERALL VERDICT: {overall}")


if __name__ == "__main__":
    main()

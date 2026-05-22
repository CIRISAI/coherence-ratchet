"""
C. elegans neural in-corridor substrate — robust re-run.
=========================================================

v2 of `papers/Corridor Dynamics.tex` re-runs v1's five-substrate corridor record
under the structural series' robust estimator. This script is the S1 neural
in-corridor re-run for the C. elegans whole-brain calcium substrate.

v1 (run_v15a / run_v15b in experiments/v15_celegans/) measured RAW mean
|pairwise Pearson| per functional class. The robust framing replaces the raw
estimator with the canonical one from
`experiments/structural_series/data_fmri/fmri_corridor.py::subject_rho`:
debiased ρ via a phase-randomized surrogate floor, plus participation-ratio
k_eff. Protocol fixed in PREREGISTRATION.md (committed before this ran).

Real data only. Per-(study,worm) records flushed to JSON as computed.
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

OUT_DIR = Path(__file__).parent
RESULTS_JSON = OUT_DIR / "results_celegans.json"

# The qsimeon/celegans_neural_data parquet is gitignored (669 MB). It lives on
# disk from prior v15 work; this is the same file run_v15a/run_v15b load.
DATA_CANDIDATES = [
    OUT_DIR / "data" / "worm_data_short.parquet",
    Path("/home/emoore/coherence-ratchet/experiments/v15_celegans/"
         "celegans_neural_data/worm_data_short.parquet"),
]
# also scan worktree copies
_wt = Path("/home/emoore/coherence-ratchet/.claude/worktrees")
if _wt.exists():
    DATA_CANDIDATES += sorted(_wt.glob(
        "*/experiments/v15_celegans/celegans_neural_data/worm_data_short.parquet"))

N_SURROGATE = 20          # phase-randomized noise-floor draws (prereg: raised
                          # from fMRI default 5 — strong calcium autocorrelation)
SEED = 0

# ---- v15a/v15b canonical functional-class prefix map (identical) ----
SENSORY = {'ASE', 'ASI', 'ASJ', 'ASK', 'ASG', 'ASH', 'ADL', 'ADF', 'AFD', 'AWA',
           'AWB', 'AWC', 'PHA', 'PHB', 'PHC', 'AVM', 'PVM', 'ALM', 'PLM', 'AQR',
           'PQR', 'FLP', 'PVD', 'URX', 'BAG', 'IL1', 'IL2', 'OLQ', 'OLL', 'CEP',
           'URY', 'URA', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6'}
COMMAND_INT = {'AVA', 'AVB', 'AVD', 'AVE', 'PVC'}
MOTOR = {'VA', 'VB', 'VC', 'VD', 'DA', 'DB', 'DD', 'AS', 'RIM', 'RMD', 'SMD',
         'SMB', 'SAA', 'SAB', 'SIA', 'SIB', 'M1', 'M2', 'M3', 'M4', 'M5', 'MI',
         'MC', 'NSM', 'HSN'}
INTERNEURON = {'AIA', 'AIB', 'AIY', 'AIZ', 'AIM', 'AIN', 'AVH', 'AVF', 'AVG',
               'AVJ', 'AVK', 'AVL', 'RIA', 'RIB', 'RIC', 'RIF', 'RIG', 'RIH',
               'RIP', 'RIR', 'RIS', 'RIV', 'PVN', 'PVP', 'PVQ', 'PVR', 'PVS',
               'PVT', 'PVW', 'LUA', 'ADA', 'BDU', 'ALA', 'DVA', 'DVB', 'DVC',
               'PDA', 'PDB', 'PDE'}
CLASSES = ['sensory', 'interneuron', 'motor', 'command']


def classify_neuron(name):
    n = str(name).upper().strip()
    base = n.rstrip('LRVDP0123456789')
    for c in [base, n[:3], n[:2]]:
        if c in COMMAND_INT:
            return 'command'
        if c in SENSORY:
            return 'sensory'
        if c in MOTOR:
            return 'motor'
        if c in INTERNEURON:
            return 'interneuron'
    return None


def safe_array(v):
    if isinstance(v, np.ndarray):
        return v.astype(float)
    if hasattr(v, '__iter__'):
        return np.array([float(x) for x in v])
    return np.array([float(v)])


# ---- canonical estimator (fmri_corridor.py::subject_rho, phase_randomize) ----
def mean_abs_offdiag(C):
    d = C.shape[0]
    return float(np.mean(np.abs(C[~np.eye(d, dtype=bool)])))


def phase_randomize(x, rng):
    """Phase-randomize a real timeseries: destroys cross-series correlation,
    preserves each series' power spectrum / autocorrelation."""
    n = x.shape[0]
    F = np.fft.rfft(x, axis=0)
    amp = np.abs(F)
    rand = rng.uniform(-np.pi, np.pi, size=F.shape)
    rand[0] = 0.0
    if n % 2 == 0:
        rand[-1] = 0.0
    Fs = amp * np.exp(1j * rand)
    return np.fft.irfft(Fs, n=n, axis=0)


def debiased_rho(traces, rng):
    """traces: list of 1-D arrays (already length-aligned). Returns
    (rho_raw, floor, rho_deb, k_eff_emp, k_eff_kish, n_neurons) or None."""
    if len(traces) < 2:
        return None
    X = np.array(traces)               # (n_neurons, T)
    ts = X.T                           # (T, n_neurons)
    sd = ts.std(axis=0)
    keep = sd > 1e-8
    ts = ts[:, keep]
    if ts.shape[1] < 2 or ts.shape[0] < 30:
        return None
    Z = (ts - ts.mean(axis=0)) / ts.std(axis=0)
    T = Z.shape[0]
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
    k = ts.shape[1]
    k_eff_kish = float(k / (1.0 + rho_deb * (k - 1.0)))
    return rho_raw, floor, rho_deb, k_eff_emp, k_eff_kish, int(k)


def pct(a, q):
    return float(np.percentile(a, q))


def main():
    data_path = next((p for p in DATA_CANDIDATES if p.exists()), None)
    if data_path is None:
        print("BLOCKED — calcium time-series parquet not found. Searched:")
        for p in DATA_CANDIDATES:
            print(f"  {p}")
        Path(OUT_DIR / "BLOCKED.txt").write_text(
            "BLOCKED: worm_data_short.parquet not on disk.\nSearched:\n"
            + "\n".join(str(p) for p in DATA_CANDIDATES) + "\n")
        return

    print(f"Loading {data_path} ...")
    df = pd.read_parquet(data_path)
    df_lab = df[df['is_labeled_neuron']].copy()
    df_lab['class'] = df_lab['neuron'].map(classify_neuron)
    print(f"  {len(df)} rows, {len(df_lab)} labeled-neuron rows.")

    units = list(df_lab.groupby(['source_dataset', 'worm']))
    print(f"  {len(units)} (study, worm) units with labeled neurons.")

    rng = np.random.default_rng(SEED)
    records = []
    out = {"data_source": "qsimeon/celegans_neural_data (worm_data_short.parquet)",
           "data_path": str(data_path), "n_surrogate": N_SURROGATE,
           "estimator": "debiased rho (phase-randomized floor) + participation-"
                        "ratio k_eff; canonical fmri_corridor.py::subject_rho",
           "records": records}

    n_incl = 0
    for (ds, worm), sub in units:
        sub_c = sub.dropna(subset=['class'])
        # collect aligned traces
        traces, classes = [], []
        for _, row in sub_c.iterrows():
            arr = safe_array(row['calcium_data'])
            if len(arr) >= 100 and np.std(arr) > 1e-8:
                traces.append(arr)
                classes.append(row['class'])
        rec = {"study": str(ds), "worm": str(worm),
               "n_classified_neurons": len(traces)}
        if len(traces) < 4:
            rec["included"] = False
            rec["reason"] = f"only {len(traces)} classified neurons (<4)"
            records.append(rec)
            RESULTS_JSON.write_text(json.dumps(out, indent=2))
            continue
        min_len = min(len(t) for t in traces)
        traces = [t[:min_len] for t in traces]
        classes = np.array(classes)

        # whole-brain (all labeled neurons)
        wb = debiased_rho(traces, rng)
        # per functional class
        per_class = {}
        any_class_pair = False
        for cls in CLASSES:
            idx = np.where(classes == cls)[0]
            if len(idx) < 2:
                continue
            any_class_pair = True
            res = debiased_rho([traces[i] for i in idx], rng)
            if res is None:
                continue
            rr, fl, rd, ke, kk, n = res
            per_class[cls] = {"n_neurons": n, "rho_raw": rr, "floor": fl,
                              "rho_deb": rd, "k_eff_emp": ke, "k_eff_kish": kk}

        if wb is None or not any_class_pair:
            rec["included"] = False
            rec["reason"] = "no usable whole-brain matrix or no class pair"
            records.append(rec)
            RESULTS_JSON.write_text(json.dumps(out, indent=2))
            continue

        rr, fl, rd, ke, kk, n = wb
        rec["included"] = True
        rec["T"] = int(min_len)
        rec["whole_brain"] = {"n_neurons": n, "rho_raw": rr, "floor": fl,
                              "rho_deb": rd, "k_eff_emp": ke, "k_eff_kish": kk}
        rec["per_class"] = per_class
        records.append(rec)
        n_incl += 1
        RESULTS_JSON.write_text(json.dumps(out, indent=2))   # flush per unit

    print(f"\n{n_incl} included units of {len(units)}.")

    # ---- aggregate / verdict ----
    incl = [r for r in records if r.get("included")]
    if not incl:
        print("BLOCKED — no units cleared the inclusion gate.")
        out["verdict"] = "BLOCKED"
        RESULTS_JSON.write_text(json.dumps(out, indent=2))
        return

    wb_raw = np.array([r["whole_brain"]["rho_raw"] for r in incl])
    wb_floor = np.array([r["whole_brain"]["floor"] for r in incl])
    wb_deb = np.array([r["whole_brain"]["rho_deb"] for r in incl])
    wb_keff = np.array([r["whole_brain"]["k_eff_emp"] for r in incl])

    iqr = pct(wb_deb, 75) - pct(wb_deb, 25)
    c1 = bool(pct(wb_deb, 5) > 0.05)
    c2 = bool((pct(wb_deb, 95) < 0.90) and (np.median(wb_keff) > 1.5))
    c3 = bool((iqr <= 0.30) and (wb_deb.max() < 0.95))
    # C4: per-class structure survives
    n_with_class_signal = sum(
        1 for r in incl
        if any(v["rho_deb"] > 0.05 for v in r.get("per_class", {}).values()))
    c4 = bool(n_with_class_signal / len(incl) >= 0.60)

    if c1 and c2 and c3:
        verdict = "PASS"
    elif (not c1) or (not c2):
        verdict = "FAIL"
    else:
        verdict = "PARTIAL"

    summary = {
        "n_included": len(incl), "n_units_total": len(units),
        "n_studies": len(set(r["study"] for r in incl)),
        "whole_brain": {
            "rho_raw_median": float(np.median(wb_raw)),
            "rho_raw_range": [float(wb_raw.min()), float(wb_raw.max())],
            "floor_median": float(np.median(wb_floor)),
            "rho_deb_median": float(np.median(wb_deb)),
            "rho_deb_p5": pct(wb_deb, 5), "rho_deb_p25": pct(wb_deb, 25),
            "rho_deb_p75": pct(wb_deb, 75), "rho_deb_p95": pct(wb_deb, 95),
            "rho_deb_range": [float(wb_deb.min()), float(wb_deb.max())],
            "rho_deb_iqr": iqr,
            "k_eff_emp_median": float(np.median(wb_keff)),
            "k_eff_emp_range": [float(wb_keff.min()), float(wb_keff.max())],
        },
        "criteria": {"C1_off_chaos": c1, "C2_off_rigidity": c2,
                     "C3_bounded_band": c3, "C4_per_class_survives": c4,
                     "C4_frac_with_class_signal": n_with_class_signal / len(incl)},
        "verdict": verdict,
    }
    # per-class aggregates (raw vs debiased)
    per_class_agg = {}
    for cls in CLASSES:
        raw = [r["per_class"][cls]["rho_raw"] for r in incl
               if cls in r.get("per_class", {})]
        deb = [r["per_class"][cls]["rho_deb"] for r in incl
               if cls in r.get("per_class", {})]
        flo = [r["per_class"][cls]["floor"] for r in incl
               if cls in r.get("per_class", {})]
        if raw:
            per_class_agg[cls] = {
                "n_worms": len(raw),
                "rho_raw_median": float(np.median(raw)),
                "rho_raw_range": [float(min(raw)), float(max(raw))],
                "floor_median": float(np.median(flo)),
                "rho_deb_median": float(np.median(deb)),
                "rho_deb_range": [float(min(deb)), float(max(deb))],
            }
    summary["per_class"] = per_class_agg
    # per-study whole-brain
    per_study = {}
    for st in sorted(set(r["study"] for r in incl)):
        d = [r["whole_brain"]["rho_deb"] for r in incl if r["study"] == st]
        rw = [r["whole_brain"]["rho_raw"] for r in incl if r["study"] == st]
        per_study[st] = {"n_worms": len(d),
                         "rho_raw_median": float(np.median(rw)),
                         "rho_deb_median": float(np.median(d)),
                         "rho_deb_range": [float(min(d)), float(max(d))]}
    summary["per_study"] = per_study
    out["summary"] = summary
    RESULTS_JSON.write_text(json.dumps(out, indent=2))

    print("\n" + "=" * 70)
    print(f"VERDICT: {verdict}")
    print("=" * 70)
    print(f"  included worms: {len(incl)} / {len(units)} "
          f"({summary['n_studies']} studies)")
    print(f"  whole-brain rho_raw   median {np.median(wb_raw):.3f}")
    print(f"  whole-brain floor     median {np.median(wb_floor):.3f}")
    print(f"  whole-brain rho_DEB   median {np.median(wb_deb):.3f}  "
          f"[{wb_deb.min():.3f}, {wb_deb.max():.3f}]  IQR {iqr:.3f}")
    print(f"  whole-brain k_eff_emp median {np.median(wb_keff):.1f}")
    print(f"  C1 off chaos    {c1}   C2 off rigidity {c2}")
    print(f"  C3 bounded band {c3}   C4 per-class    {c4}")
    print("\n  per-class raw -> debiased:")
    for cls, v in per_class_agg.items():
        print(f"    {cls:<12} raw {v['rho_raw_median']:.3f}  "
              f"floor {v['floor_median']:.3f}  -> deb {v['rho_deb_median']:.3f}"
              f"  (n={v['n_worms']})")
    print(f"\n  results: {RESULTS_JSON}")


if __name__ == "__main__":
    main()

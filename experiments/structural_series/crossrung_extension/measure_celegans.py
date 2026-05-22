"""
measure_celegans.py — Extension Pair: NEURON -> FUNCTIONAL-CLASS (C. elegans).

Cross-rung extension beyond n=2. Pre-registered in PREREGISTRATION.md.

Rung n   = individual labeled neurons (the molecular/constituent rung).
Rung n+1 = functional-class aggregate traces (sensory / interneuron / motor /
           command — the canonical v15a/v15b prefix map, identical to the
           robust_rerun celegans run).
Observation axis = calcium-imaging time-points of one worm.

This is the exact structural parallel of Path 1 Pair A (TCGA molecular ->
pathway): the n+1 rung is an aggregate over member constituents of the n rung.
Class score = mean of z-scored member-neuron traces, parallel to
measure_pairA_tcga.pathway_scores. The cross-rung / within-rung coupling ratio
is computed with the SAME crossrung_lib estimators as Path 1 — no new method.

Per worm:
  W_n      within-rung coupling among neurons (mean over the 4 classes of the
           within-class mean |Pearson|), shuffle-debiased.
  W_{n+1}  within-rung coupling among the class-aggregate traces, debiased.
  W_within = sqrt(W_n * W_{n+1}).
  tau      normalised cross-rung Gaussian MI between the neuron layer and the
           class layer, shuffle-debiased, then class-scramble corrected
           (subtract median tau against random neuron groups of matched sizes)
           — the mechanical-aggregation floor removal, parallel to Pair A's
           gene-set scramble.
  ratio    = tau_corrected / W_within.

Real data only: qsimeon/celegans_neural_data worm_data_short.parquet on disk.
Per-worm records flushed to JSON as computed.
"""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
LIB = (HERE / ".." / "crossrung_series" / "path1_tau").resolve()
sys.path.insert(0, str(LIB))
from crossrung_lib import within_rung_W, cross_rung_tau  # noqa: E402

SEED = 17
N_SCRAMBLE = 20         # mechanical-aggregation floor draws (median over draws;
                        # 20 is the celegans robust-rerun's surrogate count and
                        # is ample for a median — keeps 919 worms inside budget)
MIN_NEURONS_PER_CLASS = 3      # parallel to Pair A MIN_GENES (within-rung W needs >=3)
MIN_CLASSES = 3                # need >=3 classes for an n+1 rung with W and MI
MIN_TRACE_LEN = 100
MIN_OBS_FOR_MI = 12            # Path-1 healthy-tissue minimum

# --- worm_data_short.parquet locations (gitignored 669 MB; lives on disk) ---
DATA_CANDIDATES = [
    pathlib.Path("/home/emoore/coherence-ratchet/experiments/v15_celegans/"
                 "celegans_neural_data/worm_data_short.parquet"),
    pathlib.Path("/home/emoore/coherence-ratchet/experiments/structural_series/"
                 "robust_rerun/celegans/data/worm_data_short.parquet"),
]
_wt = pathlib.Path("/home/emoore/coherence-ratchet/.claude/worktrees")
if _wt.exists():
    DATA_CANDIDATES += sorted(_wt.glob(
        "*/experiments/v15_celegans/celegans_neural_data/worm_data_short.parquet"))
    DATA_CANDIDATES += sorted(_wt.glob(
        "*/experiments/structural_series/robust_rerun/celegans/data/"
        "worm_data_short.parquet"))

# --- canonical v15a/v15b functional-class prefix map (identical) ---
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


def class_scores(Xneurons, class_of_col):
    """Xneurons: obs x neurons. class_of_col: array of class labels per column.
    Returns (obs x classes) aggregate matrix and the class-name list. Each class
    score is the mean of z-scored member-neuron traces per observation."""
    Z = Xneurons - Xneurons.mean(axis=0, keepdims=True)
    sd = Z.std(axis=0, keepdims=True)
    Z = np.divide(Z, sd, out=np.zeros_like(Z), where=sd > 1e-10)
    names, cols = [], []
    for cls in CLASSES:
        idx = np.where(class_of_col == cls)[0]
        if len(idx) < MIN_NEURONS_PER_CLASS:
            continue
        names.append(cls)
        cols.append(Z[:, idx].mean(axis=1))
    if not cols:
        return np.zeros((Xneurons.shape[0], 0)), []
    return np.column_stack(cols), names


def measure_worm(traces, classes, rng):
    """traces: list of length-aligned 1-D arrays (one per neuron).
    classes: array of class labels. Returns the measurement dict, or None."""
    Xn = np.array(traces).T                       # obs x neurons
    m = Xn.shape[0]
    classes = np.asarray(classes)

    # --- W_n: mean over classes of within-class neuron mean|Pearson| ---
    wn_db, class_sizes = [], {}
    for cls in CLASSES:
        idx = np.where(classes == cls)[0]
        if len(idx) < MIN_NEURONS_PER_CLASS:
            continue
        class_sizes[cls] = len(idx)
        r = within_rung_W(Xn[:, idx], rng)
        if np.isfinite(r[2]):
            wn_db.append(r[2])
    if len(class_sizes) < MIN_CLASSES:
        return None
    W_n = float(np.mean(wn_db))

    # --- rung n+1: class-aggregate traces, W_{n+1} ---
    P, pnames = class_scores(Xn, classes)         # obs x classes
    if P.shape[1] < MIN_CLASSES:
        return None
    wm = within_rung_W(P, rng)
    W_np1 = wm[2]
    W_within = float(np.sqrt(max(W_n, 0.0) * max(W_np1, 0.0)))

    # --- cross-rung tau: neuron layer (classified neurons) vs class layer ---
    keep = np.array([c in class_sizes for c in classes])
    Rn = Xn[:, keep]
    tau = cross_rung_tau(Rn, P, m, rng)

    # --- mechanical-aggregation floor: class-scramble correction ---
    sizes = list(class_sizes.values())
    n_neur = Xn.shape[1]
    sr = np.random.default_rng(SEED + 1)
    scramble_taus = []
    for _ in range(N_SCRAMBLE):
        rand_scores = []
        for sz in sizes:
            pick = sr.choice(n_neur, size=min(sz, n_neur), replace=False)
            sub = Xn[:, pick]
            subz = sub - sub.mean(axis=0, keepdims=True)
            sd = subz.std(axis=0, keepdims=True)
            subz = np.divide(subz, sd, out=np.zeros_like(subz),
                             where=sd > 1e-10)
            rand_scores.append(subz.mean(axis=1))
        Pscr = np.column_stack(rand_scores)
        # 12 shuffle nulls inside each scramble draw: the scramble itself is
        # the mechanical-aggregation control and we take a median over draws,
        # so a lighter internal null suffices (the main tau keeps the full 50).
        t = cross_rung_tau(Rn, Pscr, m, sr, n_shuffle=12)
        if np.isfinite(t["tau_debiased"]):
            scramble_taus.append(t["tau_debiased"])
    tau_scramble = float(np.median(scramble_taus)) if scramble_taus else 0.0
    tau_corrected = max(tau["tau_debiased"] - tau_scramble, 0.0)

    ratio = tau_corrected / W_within if W_within > 1e-9 else np.nan
    return dict(
        m_obs=int(m), n_classes=len(pnames), classes=pnames,
        n_neurons_classified=int(keep.sum()),
        class_sizes=class_sizes,
        W_n=W_n, W_np1=float(W_np1), W_within=W_within,
        tau_raw=tau["tau_raw"], tau_floor=tau["tau_floor"],
        tau_debiased=tau["tau_debiased"], tau_scramble=tau_scramble,
        tau_corrected=float(tau_corrected), q_pca=tau["q"],
        tau_noise_dominated=bool(
            tau["tau_raw"] > 1e-9
            and tau["tau_debiased"] / tau["tau_raw"] < 0.3),
        ratio=float(ratio),
    )


def main():
    print("=" * 78)
    print("Extension — C. elegans neuron -> functional-class: cross/within "
          "coupling")
    print("=" * 78)
    data_path = next((p for p in DATA_CANDIDATES if p.exists()), None)
    out_json = HERE / "results_celegans.json"
    if data_path is None:
        print("MISSING — worm_data_short.parquet not on disk. Searched:")
        for p in DATA_CANDIDATES:
            print(f"  {p}")
        out_json.write_text(json.dumps(
            {"pair": "celegans neuron->functional-class", "status": "MISSING",
             "reason": "worm_data_short.parquet not located on disk"},
            indent=2))
        return

    print(f"  loading {data_path}")
    df = pd.read_parquet(data_path)
    df_lab = df[df['is_labeled_neuron']].copy()
    df_lab['class'] = df_lab['neuron'].map(classify_neuron)
    units = list(df_lab.groupby(['source_dataset', 'worm']))
    print(f"  {len(units)} (study, worm) units with labeled neurons.\n")

    out = {"pair": "celegans neuron->functional-class",
           "status": "MEASURED",
           "data_source": "qsimeon/celegans_neural_data "
                          "(worm_data_short.parquet)",
           "data_path": str(data_path),
           "method": "crossrung_lib (Path 1); class-scramble corrected tau",
           "records": []}
    records = out["records"]

    for (ds, worm), sub in units:
        sub_c = sub.dropna(subset=['class'])
        traces, classes = [], []
        for _, row in sub_c.iterrows():
            arr = safe_array(row['calcium_data'])
            if len(arr) >= MIN_TRACE_LEN and np.std(arr) > 1e-8:
                traces.append(arr)
                classes.append(row['class'])
        rec = {"study": str(ds), "worm": str(worm),
               "n_classified_neurons": len(traces)}
        if len(traces) < 4:
            rec["included"] = False
            rec["reason"] = f"only {len(traces)} classified neurons"
            records.append(rec)
            out_json.write_text(json.dumps(out, indent=2))
            continue
        min_len = min(len(t) for t in traces)
        traces = [t[:min_len] for t in traces]
        if min_len < MIN_OBS_FOR_MI:
            rec["included"] = False
            rec["reason"] = f"aligned trace length {min_len} < {MIN_OBS_FOR_MI}"
            records.append(rec)
            out_json.write_text(json.dumps(out, indent=2))
            continue
        try:
            r = measure_worm(traces, classes,
                             np.random.default_rng(SEED))
        except Exception as e:
            rec["included"] = False
            rec["reason"] = f"{type(e).__name__}: {str(e)[:80]}"
            records.append(rec)
            out_json.write_text(json.dumps(out, indent=2))
            continue
        if r is None:
            rec["included"] = False
            rec["reason"] = f"<{MIN_CLASSES} usable functional classes"
            records.append(rec)
            out_json.write_text(json.dumps(out, indent=2))
            continue
        rec["included"] = True
        rec.update(r)
        records.append(rec)
        out_json.write_text(json.dumps(out, indent=2))
        print(f"  {ds}/{worm}: m={r['m_obs']} cls={r['n_classes']} "
              f"W_n={r['W_n']:.3f} W_n+1={r['W_np1']:.3f} "
              f"W_within={r['W_within']:.3f} "
              f"tau_corr={r['tau_corrected']:.3f} "
              f"ratio={r['ratio']:.3f}"
              f"{'  [NOISE-DOM]' if r['tau_noise_dominated'] else ''}")

    incl = [r for r in records if r.get("included")
            and np.isfinite(r.get("ratio", np.nan))]
    ratios = sorted(r["ratio"] for r in incl)
    if ratios:
        med = float(np.median(ratios))
        out["n_worms_measured"] = len(ratios)
        out["median_ratio"] = med
        out["ratio_range"] = [ratios[0], ratios[-1]]
        out["verdict"] = ("O(1) holds" if 0.3 <= med <= 3.0
                          else "O(1) breaks low (g/J<<1)" if med < 0.3
                          else "O(1) breaks high (g/J>>3)")
        print("\n" + "=" * 78)
        print(f"  measured {len(ratios)} worms — median ratio = {med:.3f}, "
              f"range [{ratios[0]:.3f}, {ratios[-1]:.3f}]")
        print(f"  verdict: {out['verdict']}")
    else:
        out["status"] = "MEASURED_NO_USABLE"
        print("\n  no worm produced a usable cross-rung ratio.")
    out_json.write_text(json.dumps(out, indent=2))
    print(f"\n  wrote {out_json}")


if __name__ == "__main__":
    main()

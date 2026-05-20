"""
v15a: C. elegans methodology derisking.

For one well-labeled worm: identify labeled neurons, group by canonical
cell class (sensory, command interneuron, other interneuron, motor),
compute within-rung pairwise correlation (ρ_n) and cross-rung activity
correlation (τ_{n,n+1}).

The framework's structural claim for within-organism multi-rung: each rung's
ρ should sit in some band; cross-rung τ should sit in some band; the bands
should differ between behavioral states (active vs quiescent worms).

No pre-committed numerical bounds. Look at distributions, see what's there.

Data source: qsimeon/celegans_neural_data (HuggingFace, 12 aggregated studies).
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

OUT_DIR = Path(__file__).parent

# ---- Canonical C. elegans cell classes ----
# Standard WormAtlas / White 1986 / Cook 2019 functional groupings.
# Mapping by neuron-name prefix (handles bilateral pairs like AVAL/AVAR → AVA).
SENSORY = {
    # Amphid sensory neurons
    'ASE', 'ASI', 'ASJ', 'ASK', 'ASG', 'ASH', 'ADL', 'ADF', 'AFD', 'AWA', 'AWB', 'AWC',
    # Phasmid sensory
    'PHA', 'PHB', 'PHC',
    # Mechanosensory
    'AVM', 'PVM', 'ALM', 'PLM', 'AQR', 'PQR', 'FLP', 'PVD',
    # Oxygen / CO2 sensors
    'URX', 'BAG', 'AQR',
    # Inner labial / cephalic sensory
    'IL1', 'IL2', 'OLQ', 'OLL', 'CEP', 'URY', 'URA',
    # Pharynx sensory
    'I1', 'I2', 'I3', 'I4', 'I5', 'I6',
}
COMMAND_INT = {'AVA', 'AVB', 'AVD', 'AVE', 'PVC'}  # premotor command interneurons
MOTOR = {
    'VA', 'VB', 'VC', 'VD', 'DA', 'DB', 'DD', 'AS',  # ventral cord motor
    'RIM', 'RMD', 'SMD', 'SMB', 'SAA', 'SAB', 'SIA', 'SIB',  # head motor
    'M1', 'M2', 'M3', 'M4', 'M5', 'MI', 'MC', 'NSM',  # pharynx motor
    'HSN', 'VC',  # egg-laying motor
}
INTERNEURON = {
    'AIA', 'AIB', 'AIY', 'AIZ', 'AIM', 'AIN', 'AVH', 'AVF', 'AVG', 'AVJ', 'AVK', 'AVL',
    'RIA', 'RIB', 'RIC', 'RIF', 'RIG', 'RIH', 'RIP', 'RIR', 'RIS', 'RIV',
    'PVN', 'PVP', 'PVQ', 'PVR', 'PVS', 'PVT', 'PVW', 'LUA',
    'ADA', 'BDU', 'ALA', 'RIM',
    'DVA', 'DVB', 'DVC', 'PDA', 'PDB', 'PDE',
}


def classify_neuron(name):
    """Map neuron name to functional class. C. elegans names follow:
    - Two-letter class + lateral suffix (L/R) for bilateral pairs (AVAL, AVAR → AVA)
    - Three-letter class with numeric (VA1, DA9 → VA, DA)
    - Some special cases (NSML/NSMR → NSM)
    """
    n = name.upper().strip()
    # strip trailing L/R (lateral) and numeric digits
    base = n.rstrip('LRVDP0123456789')
    # try the base prefix
    candidates = [base, n[:3], n[:2]]
    for c in candidates:
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
    """Convert HF parquet's stored numeric arrays to numpy arrays."""
    if isinstance(v, np.ndarray):
        return v.astype(float)
    if hasattr(v, '__iter__'):
        return np.array([float(x) for x in v])
    return np.array([float(v)])


# ---- Load and select one well-labeled worm ----
print("Loading worm_data_short.parquet ...")
df = pd.read_parquet('celegans_neural_data/worm_data_short.parquet')
df_labeled = df[df['is_labeled_neuron']].copy()
print(f"  total rows: {len(df)}, labeled: {len(df_labeled)}")

# Pick a worm with many labeled neurons from a single dataset
worm_counts = df_labeled.groupby(['source_dataset', 'worm']).size().reset_index(name='n_labeled')
worm_counts = worm_counts.sort_values('n_labeled', ascending=False)
print(f"\nTop 5 (dataset, worm, n_labeled_neurons):")
print(worm_counts.head(5).to_string(index=False))

# Pick the top one
top_ds, top_worm, top_n = worm_counts.iloc[0]['source_dataset'], worm_counts.iloc[0]['worm'], worm_counts.iloc[0]['n_labeled']
print(f"\nUsing: {top_ds} / {top_worm} / {top_n} labeled neurons")
sub = df_labeled[(df_labeled['source_dataset'] == top_ds) & (df_labeled['worm'] == top_worm)].copy()

# Classify each neuron
sub['class'] = sub['neuron'].map(classify_neuron)
print(f"\nClass counts in this worm:")
print(sub['class'].value_counts(dropna=False))

# Show some examples
print(f"\nSample neurons by class:")
for cls, grp in sub.groupby('class'):
    print(f"  {cls}: {grp['neuron'].head(8).tolist()}")

# Drop unclassified
sub_c = sub.dropna(subset=['class']).copy()
print(f"\nClassified neurons: {len(sub_c)}")

# ---- Build activity matrix (neurons × time) ----
# All neurons in this worm should have time series of similar length.
# We'll align to the common length.
traces = []
classes = []
neurons = []
for _, row in sub_c.iterrows():
    arr = safe_array(row['calcium_data'])
    if len(arr) < 100:  # need enough timepoints
        continue
    traces.append(arr)
    classes.append(row['class'])
    neurons.append(row['neuron'])

# Align to min length
min_len = min(len(t) for t in traces)
print(f"\nTraces: n={len(traces)}, common length = {min_len}")
X = np.array([t[:min_len] for t in traces])  # (n_neurons, n_time)
print(f"Activity matrix: {X.shape}")
classes = np.array(classes)
neurons = np.array(neurons)

# ---- Compute within-rung and cross-rung correlations ----
unique_classes = sorted(set(classes))
print(f"\nClasses present: {unique_classes}")

# Per-class within-rung pairwise correlation matrix
within_rung_rho = {}
for cls in unique_classes:
    idx = np.where(classes == cls)[0]
    if len(idx) < 2:
        within_rung_rho[cls] = None
        continue
    sub_X = X[idx]
    C = np.corrcoef(sub_X)  # (n_in_class, n_in_class)
    iu = np.triu_indices(len(idx), k=1)
    abs_corr = np.abs(C[iu])
    within_rung_rho[cls] = {
        'n_neurons': len(idx),
        'n_pairs': len(abs_corr),
        'mean_abs_corr': float(abs_corr.mean()),
        'std_abs_corr': float(abs_corr.std()),
        'median_abs_corr': float(np.median(abs_corr)),
    }
print(f"\n--- Within-rung ρ (mean abs pairwise correlation within class) ---")
for cls, v in within_rung_rho.items():
    if v is None:
        print(f"  {cls}: <2 neurons, skipped")
    else:
        print(f"  {cls}: n={v['n_neurons']:>2} neurons, n_pairs={v['n_pairs']:>3}, "
              f"|ρ| = {v['mean_abs_corr']:.3f} ± {v['std_abs_corr']:.3f} "
              f"(median {v['median_abs_corr']:.3f})")

# Cross-rung τ: aggregate per-class activity (mean across class), then pairwise correlation
class_traces = {cls: X[classes == cls].mean(axis=0) for cls in unique_classes if (classes == cls).sum() >= 2}
print(f"\n--- Cross-rung τ (correlation between class-mean activities) ---")
cross_rung = {}
for i, c1 in enumerate(class_traces):
    for c2 in list(class_traces)[i+1:]:
        r, p = pearsonr(class_traces[c1], class_traces[c2])
        cross_rung[f"{c1}↔{c2}"] = {
            'pearson_r': float(r),
            'abs_r': float(abs(r)),
            'p_value': float(p),
        }
        print(f"  {c1:<12} ↔ {c2:<12}: r = {r:+.3f} (|r|={abs(r):.3f}, p={p:.4f})")

# Aggregate
all_within = [v['mean_abs_corr'] for v in within_rung_rho.values() if v is not None]
all_cross = [v['abs_r'] for v in cross_rung.values()]
print(f"\n--- Summary ---")
print(f"Within-rung |ρ| across classes: mean={np.mean(all_within):.3f}, "
      f"range=({min(all_within):.3f}, {max(all_within):.3f})")
print(f"Cross-rung  |τ| across pairs:   mean={np.mean(all_cross):.3f}, "
      f"range=({min(all_cross):.3f}, {max(all_cross):.3f})")

# ---- Plot ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

ax = axes[0]
labels = list(within_rung_rho.keys())
means = [v['mean_abs_corr'] if v else np.nan for v in within_rung_rho.values()]
stds = [v['std_abs_corr'] if v else 0 for v in within_rung_rho.values()]
ns = [v['n_neurons'] if v else 0 for v in within_rung_rho.values()]
bars = ax.bar(labels, means, yerr=stds, capsize=6, alpha=0.7, color='C0')
for bar, n in zip(bars, ns):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
            f'n={n}', ha='center', va='bottom', fontsize=10)
ax.set_ylabel('|ρ| within rung (mean abs pairwise correlation)')
ax.set_title(f'{top_ds} / {top_worm}\nWithin-rung correlation per class')
ax.set_ylim(0, 1.0)
ax.grid(alpha=0.3, axis='y')

ax = axes[1]
pair_labels = list(cross_rung.keys())
pair_abs = [v['abs_r'] for v in cross_rung.values()]
ax.barh(pair_labels, pair_abs, color='C2', alpha=0.7)
ax.set_xlim(0, 1.0)
ax.set_xlabel('|τ| (abs Pearson r between class-mean traces)')
ax.set_title('Cross-rung coupling per class pair')
ax.grid(alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(OUT_DIR / "v15a_methodology.png", dpi=120)
print(f"\nPlot: {OUT_DIR / 'v15a_methodology.png'}")

# Save
out = {
    "data_source": "qsimeon/celegans_neural_data",
    "selected_dataset": str(top_ds),
    "selected_worm": str(top_worm),
    "n_labeled_neurons_total": int(top_n),
    "n_classified_neurons": int(len(sub_c)),
    "n_time_points": int(min_len),
    "class_counts": sub['class'].value_counts(dropna=False).to_dict(),
    "within_rung_rho": {k: v for k, v in within_rung_rho.items()},
    "cross_rung_tau": cross_rung,
    "aggregate_within_rung_mean": float(np.mean(all_within)),
    "aggregate_cross_rung_mean": float(np.mean(all_cross)),
}
with open(OUT_DIR / "results_v15a.json", "w") as f:
    json.dump(out, f, indent=2, default=str)
print(f"Results: {OUT_DIR / 'results_v15a.json'}")

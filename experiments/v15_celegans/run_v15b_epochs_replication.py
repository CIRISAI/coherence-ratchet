"""
v15b+c: behavioral epoch split AND multi-worm replication.

Two questions in one pass:

(b) Within ONE worm, does within-rung ρ stay stable across activity epochs
    while cross-rung τ varies with state? The framework predicts yes. If
    both vary together, the result is global-state confound.

(c) Across MULTIPLE worms, does the within-rung clustering at ~0.5
    replicate? If yes, the v15a single-worm result reflects something
    organism-level; if no, v15a was noise.

State identification is unsupervised: total population activity per time
bin, split into active (top 33%) / intermediate / quiescent (bottom 33%).
This is a rough approximation to behavioral state — locomotion bouts in
C. elegans are activity-high, sleep / lethargus / pumping-only states are
activity-low. Sufficient for testing the framework's distinct-vs-confound
prediction.
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

SENSORY = {'ASE','ASI','ASJ','ASK','ASG','ASH','ADL','ADF','AFD','AWA','AWB','AWC',
    'PHA','PHB','PHC','AVM','PVM','ALM','PLM','AQR','PQR','FLP','PVD',
    'URX','BAG','IL1','IL2','OLQ','OLL','CEP','URY','URA',
    'I1','I2','I3','I4','I5','I6'}
COMMAND_INT = {'AVA','AVB','AVD','AVE','PVC'}
MOTOR = {'VA','VB','VC','VD','DA','DB','DD','AS','RIM','RMD','SMD','SMB','SAA','SAB',
    'SIA','SIB','M1','M2','M3','M4','M5','MI','MC','NSM','HSN'}
INTERNEURON = {'AIA','AIB','AIY','AIZ','AIM','AIN','AVH','AVF','AVG','AVJ','AVK','AVL',
    'RIA','RIB','RIC','RIF','RIG','RIH','RIP','RIR','RIS','RIV',
    'PVN','PVP','PVQ','PVR','PVS','PVT','PVW','LUA',
    'ADA','BDU','ALA','DVA','DVB','DVC','PDA','PDB','PDE'}


def classify_neuron(name):
    n = name.upper().strip()
    base = n.rstrip('LRVDP0123456789')
    for c in [base, n[:3], n[:2]]:
        if c in COMMAND_INT: return 'command'
        if c in SENSORY: return 'sensory'
        if c in MOTOR: return 'motor'
        if c in INTERNEURON: return 'interneuron'
    return None


def safe_array(v):
    if isinstance(v, np.ndarray):
        return v.astype(float)
    if hasattr(v, '__iter__'):
        return np.array([float(x) for x in v])
    return np.array([float(v)])


def load_worm_X(df_labeled, dataset, worm):
    """Return (X (n_neurons, T), classes, neurons) for one worm."""
    sub = df_labeled[(df_labeled['source_dataset'] == dataset) & (df_labeled['worm'] == worm)].copy()
    sub['class'] = sub['neuron'].map(classify_neuron)
    sub = sub.dropna(subset=['class'])
    traces, classes, neurons = [], [], []
    for _, row in sub.iterrows():
        arr = safe_array(row['calcium_data'])
        if len(arr) < 100:
            continue
        traces.append(arr); classes.append(row['class']); neurons.append(row['neuron'])
    if len(traces) < 4:
        return None, None, None
    min_len = min(len(t) for t in traces)
    X = np.array([t[:min_len] for t in traces])
    return X, np.array(classes), np.array(neurons)


def within_cross_summary(X, classes, neurons):
    """Compute within-rung |ρ| and cross-rung |τ| (class-mean) for a given X."""
    unique_classes = sorted(set(classes))
    within = {}
    for cls in unique_classes:
        idx = np.where(classes == cls)[0]
        if len(idx) < 2:
            continue
        C = np.corrcoef(X[idx])
        iu = np.triu_indices(len(idx), k=1)
        within[cls] = {
            'n': int(len(idx)),
            'mean_abs_rho': float(np.abs(C[iu]).mean()),
            'std_abs_rho': float(np.abs(C[iu]).std()),
        }
    # Cross-rung
    class_means = {cls: X[classes == cls].mean(axis=0) for cls in unique_classes if (classes == cls).sum() >= 2}
    cross = {}
    cls_keys = list(class_means)
    for i, c1 in enumerate(cls_keys):
        for c2 in cls_keys[i+1:]:
            if class_means[c1].std() < 1e-10 or class_means[c2].std() < 1e-10:
                continue
            r, _ = pearsonr(class_means[c1], class_means[c2])
            cross[f"{c1}↔{c2}"] = float(abs(r))
    return within, cross


# ---- Load data, find well-labeled worms ----
print("Loading...")
df = pd.read_parquet('celegans_neural_data/worm_data_short.parquet')
df_labeled = df[df['is_labeled_neuron']].copy()
worm_counts = df_labeled.groupby(['source_dataset', 'worm']).size().reset_index(name='n_labeled')
worm_counts = worm_counts.sort_values('n_labeled', ascending=False)
print(f"Top 12 worms by labeled-neuron count:")
print(worm_counts.head(12).to_string(index=False))


# ============================================================
# (b) Behavioral epoch split on ONE worm
# ============================================================
print(f"\n{'='*70}\n(b) BEHAVIORAL EPOCH SPLIT — one worm\n{'='*70}")
ds, worm = worm_counts.iloc[0]['source_dataset'], worm_counts.iloc[0]['worm']
print(f"Worm: {ds} / {worm}")
X, classes, neurons = load_worm_X(df_labeled, ds, worm)
print(f"X shape: {X.shape}, classes: {set(classes)}")

# Total population activity per time bin
pop_activity = np.abs(X).mean(axis=0)  # (T,)
# Active = top 33%, quiescent = bottom 33%, intermediate = middle
q_lo, q_hi = np.quantile(pop_activity, [0.33, 0.67])
mask_active = pop_activity > q_hi
mask_quiet = pop_activity < q_lo
mask_mid = ~mask_active & ~mask_quiet
print(f"\nEpoch sizes: active={mask_active.sum()} timesteps, intermediate={mask_mid.sum()}, quiet={mask_quiet.sum()}")
print(f"Population-activity thresholds: q33={q_lo:.4f}, q67={q_hi:.4f}")

# Recompute within/cross-rung per epoch
results_by_epoch = {}
for name, mask in [('all', np.ones_like(mask_active)), ('active', mask_active),
                    ('intermediate', mask_mid), ('quiet', mask_quiet)]:
    if mask.sum() < 50:
        continue
    X_ep = X[:, mask]
    w, c = within_cross_summary(X_ep, classes, neurons)
    results_by_epoch[name] = {'within': w, 'cross': c, 'n_timesteps': int(mask.sum())}

print(f"\n--- Within-rung |ρ| per class per epoch ---")
print(f"{'class':<12} " + " ".join(f"{ep:>14}" for ep in results_by_epoch))
for cls in sorted({cls for ep in results_by_epoch.values() for cls in ep['within']}):
    row = f"{cls:<12} "
    for ep, ep_res in results_by_epoch.items():
        if cls in ep_res['within']:
            v = ep_res['within'][cls]
            row += f"{v['mean_abs_rho']:>6.3f}±{v['std_abs_rho']:>5.3f}   "
        else:
            row += f"{'—':>14}   "
    print(row)

print(f"\n--- Cross-rung |τ| per pair per epoch ---")
all_pairs = sorted({p for ep in results_by_epoch.values() for p in ep['cross']})
print(f"{'pair':<28} " + " ".join(f"{ep:>10}" for ep in results_by_epoch))
for p in all_pairs:
    row = f"{p:<28} "
    for ep, ep_res in results_by_epoch.items():
        if p in ep_res['cross']:
            row += f"{ep_res['cross'][p]:>10.3f}"
        else:
            row += f"{'—':>10}"
    print(row)


# ============================================================
# (c) Twelve-worm replication
# ============================================================
print(f"\n{'='*70}\n(c) MULTI-WORM REPLICATION — top 12 by labeled-neuron count\n{'='*70}")
multi_worm = []
for i, row in worm_counts.head(12).iterrows():
    ds, worm = row['source_dataset'], row['worm']
    X, classes, neurons = load_worm_X(df_labeled, ds, worm)
    if X is None:
        continue
    w, c = within_cross_summary(X, classes, neurons)
    multi_worm.append({
        'dataset': str(ds), 'worm': str(worm),
        'n_neurons': int(X.shape[0]), 'T': int(X.shape[1]),
        'classes': {k: v for k, v in w.items()},
        'cross_mean': float(np.mean(list(c.values()))) if c else None,
        'cross_std': float(np.std(list(c.values()))) if c else None,
    })

# Print per-worm within-rung means by class
print(f"{'worm':<32} " + "".join(f"{c:>12}" for c in ['sensory','interneuron','motor','command']))
for w in multi_worm:
    label = f"{w['dataset'][:14]:<14}/{w['worm']:<10}"
    row = f"{label:<32} "
    for cls in ['sensory', 'interneuron', 'motor', 'command']:
        if cls in w['classes']:
            row += f"{w['classes'][cls]['mean_abs_rho']:>6.3f}(n={w['classes'][cls]['n']:>2})   "
        else:
            row += f"{'—':>12}   "
    print(row)

# Aggregate: for each class, distribution of within-rung |ρ| across worms
print(f"\nAcross-worm distribution per class:")
for cls in ['sensory','interneuron','motor','command']:
    vals = [w['classes'][cls]['mean_abs_rho'] for w in multi_worm if cls in w['classes']]
    if vals:
        print(f"  {cls:<12}: n_worms={len(vals):>2}, "
              f"|ρ| mean={np.mean(vals):.3f} ± {np.std(vals):.3f}, "
              f"range=({min(vals):.3f}, {max(vals):.3f})")

cross_means = [w['cross_mean'] for w in multi_worm if w['cross_mean'] is not None]
print(f"\nCross-rung |τ| (mean across pairs, distribution across worms):")
print(f"  n_worms={len(cross_means)}, mean={np.mean(cross_means):.3f} ± {np.std(cross_means):.3f}, "
      f"range=({min(cross_means):.3f}, {max(cross_means):.3f})")


# ---- Plot ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: within-rung ρ per class per epoch (epoch split)
ax = axes[0]
classes_order = ['sensory', 'interneuron', 'motor', 'command']
epochs_order = ['all', 'active', 'intermediate', 'quiet']
epoch_colors = {'all': 'k', 'active': 'C3', 'intermediate': 'C2', 'quiet': 'C0'}
for i, ep in enumerate(epochs_order):
    if ep not in results_by_epoch:
        continue
    vals = [results_by_epoch[ep]['within'].get(cls, {}).get('mean_abs_rho', np.nan) for cls in classes_order]
    errs = [results_by_epoch[ep]['within'].get(cls, {}).get('std_abs_rho', 0) for cls in classes_order]
    x = np.arange(len(classes_order)) + (i - 1.5) * 0.18
    ax.bar(x, vals, yerr=errs, width=0.18, capsize=3, label=ep, color=epoch_colors[ep], alpha=0.75)
ax.set_xticks(np.arange(len(classes_order)))
ax.set_xticklabels(classes_order)
ax.set_ylabel('|ρ| within rung')
ax.set_title(f'(b) Within-rung correlation by epoch — {ds}/{worm}')
ax.set_ylim(0, 1)
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis='y')

# Right: across-worm distribution of within-rung ρ per class
ax = axes[1]
data_for_box = []
labels_for_box = []
for cls in classes_order:
    vals = [w['classes'][cls]['mean_abs_rho'] for w in multi_worm if cls in w['classes']]
    if vals:
        data_for_box.append(vals)
        labels_for_box.append(f"{cls}\n(n_worms={len(vals)})")
ax.boxplot(data_for_box, tick_labels=labels_for_box, showmeans=True)
ax.set_ylabel('|ρ| within rung')
ax.set_title(f'(c) Within-rung correlation across {len(multi_worm)} worms')
ax.set_ylim(0, 1)
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUT_DIR / "v15bc_epochs_replication.png", dpi=120)
print(f"\nPlot: {OUT_DIR / 'v15bc_epochs_replication.png'}")

# Save
with open(OUT_DIR / "results_v15bc.json", "w") as f:
    json.dump({
        'epoch_split': {
            'worm': f"{ds}/{worm}",
            'results_by_epoch': results_by_epoch,
        },
        'multi_worm': multi_worm,
    }, f, indent=2, default=str)
print(f"Results: {OUT_DIR / 'results_v15bc.json'}")

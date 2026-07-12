#!/usr/bin/env python3
"""Shared loader for the CIRISAI/reasoning-traces public traces.

Resolves the HuggingFace cache (download-once, work-locally; anonymous access),
loads trace_context.jsonl (per-trace constraint telemetry), and exposes the
constraint-axis definitions + grouping/ordering helpers used by both harnesses.

Ordering note (load-bearing for harness_db): `timestamp` is SCRUBBED to a
placeholder in the public release, so it CANNOT order thoughts within a task.
The integer field `id` is globally unique, monotonic, and within a task tracks
`thought_depth` (0,1,2,...). We order within-task by `id`. This is a creation-
order surrogate for wall-clock time, stated as such.
"""
import os, glob, json
import numpy as np

# ---- data location (download-once cache) -----------------------------------
_CACHE = os.path.expanduser(
    "~/.cache/huggingface/hub/datasets--CIRISAI--reasoning-traces/snapshots")

def _find(fname):
    hits = glob.glob(os.path.join(_CACHE, "*", "data_scrubbed_v1", fname))
    if not hits:
        raise FileNotFoundError(
            f"{fname} not in HF cache. Fetch once with:\n"
            f"  python3 -c \"from huggingface_hub import hf_hub_download as d; "
            f"d(repo_id='CIRISAI/reasoning-traces', "
            f"filename='data_scrubbed_v1/{fname}', repo_type='dataset')\"")
    return sorted(hits)[-1]

def context_path():  return _find("trace_context.jsonl")
def accord_path():   return _find("accord_traces.jsonl")

def load_context():
    return [json.loads(l) for l in open(context_path())]

# ---- constraint axes -------------------------------------------------------
# CORE4: ~100% coverage in every group -> the covariance is complete-case, no
# missingness confound. These are the PRIMARY axes for N_eff.
CORE4 = ["csdma_plausibility_score", "dsdma_domain_alignment",
         "idma_k_eff", "idma_correlation_risk"]
# ALL8: adds the four partially-covered scores. SECONDARY only: coverage varies
# by group (33-78%), so complete-case n and the missingness pattern differ
# across groups -> a confound baked into any 8-axis comparison. Reported with
# its n, never as the headline.
EXTRA4 = ["coherence_score", "entropy_score",
          "epistemic_humility_certainty", "optimization_veto_entropy_ratio"]
ALL8 = CORE4 + EXTRA4

# Version-contaminated axes: idma_* reads differently across agent_version
# (idma_correlation_risk ~=0.22 for v2.0-2.5, ~=0.97 for v2.7). Flag on any
# cross-version comparison. See DECISIONS.md.
VERSION_SENSITIVE = {"idma_k_eff", "idma_correlation_risk"}

def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)

def axis_matrix(rows, axes, complete_case=True):
    """rows -> (X, kept_row_indices). complete_case: keep only rows numeric on
    ALL axes (needed for a clean covariance). Returns X shape (n_kept, k)."""
    X, idx = [], []
    for i, r in enumerate(rows):
        vals = [r.get(a) for a in axes]
        if complete_case and not all(is_num(v) for v in vals):
            continue
        if complete_case:
            X.append([float(v) for v in vals]); idx.append(i)
    return np.asarray(X, float), idx

# ---- grouping / ordering ---------------------------------------------------
def group(rows, agent=None, task_class=None, overridden=None, agent_version=None):
    out = []
    for r in rows:
        if agent is not None and r.get("agent_name") != agent: continue
        if task_class is not None and r.get("task_class") != task_class: continue
        if overridden is not None and bool(r.get("action_was_overridden")) != overridden: continue
        if agent_version is not None and r.get("agent_version") != agent_version: continue
        out.append(r)
    return out

def sequences(rows, min_len=2):
    """Group rows into within-task sequences ordered by `id` (creation-order
    surrogate; timestamp is scrubbed). Returns list of lists, each len>=min_len."""
    from collections import defaultdict
    byt = defaultdict(list)
    for r in rows:
        byt[r.get("task_id")].append(r)
    seqs = []
    for t, v in byt.items():
        if len(v) < min_len: continue
        seqs.append(sorted(v, key=lambda r: r["id"]))
    return seqs

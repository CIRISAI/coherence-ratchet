#!/usr/bin/env python3
"""
Finalize the George two-agent trajectory WITHOUT recomputing the (already complete)
propofol trajectory. Two modes:

  baseline  : compute the propofol-George Session1 awake-baseline levels
              (writes baseline_windows_propofol_george.json + returns levels).
  assemble  : read the ketamine-only results JSON produced by the TRAJ_ONLY=ketamine
              run, splice in the propofol session (reconstructed from the existing
              trajectory_windows_propofol_george.jsonl + Condition.mat markers +
              the propofol baseline), and re-dump the combined results JSON so
              spectral_anesthesia_trajectory_post.py can read BOTH agents.

Real data only; reuses spectral_anesthesia_trajectory verbatim. No commit.
"""
import os, sys, json, glob, re
import numpy as np

os.environ.setdefault("TRAJ_TAG", "_george")
os.environ.setdefault("TRAJ_DATA",
    "/tmp/claude-1000/-home-emoore-coherence-ratchet/"
    "a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/neuro")
import spectral_anesthesia_trajectory as T

HERE = T.HERE
BAND = T.BAND
DATA = os.environ["TRAJ_DATA"]
TAG = "_george"

def s2_chans(s2_dir):
    fs = glob.glob(os.path.join(s2_dir, "ECoG_ch*.mat"))
    nums = sorted(int(re.search(r"ch(\d+)\.mat", os.path.basename(f)).group(1)) for f in fs)
    return nums[:T.MAXCH]

def do_baseline():
    root = os.path.join(DATA, "GEO_PF_ext")
    s1 = T.session_dir(root, 1); s2 = T.session_dir(root, 2)
    chans = s2_chans(s2)
    print(f"propofol George S1 baseline: {len(chans)} chans, s1={os.path.basename(s1)}")
    lv = T.baseline_levels("propofol", s1, BAND, chans, TAG)
    print("done:", lv)

def _sess_meta(agent_root):
    s2 = T.session_dir(agent_root, 2)
    segs, bare = T.read_conditions(s2)
    inj = next((t for lab, t in bare if "Injection" in lab and "Antagonist" not in lab), None)
    deep = next(((t0, t1) for b, t0, t1 in segs if b == "Anesthetized"), (None, None))
    return inj, deep[0], deep[1]

def do_assemble():
    resp = os.path.join(HERE, f"spectral_results_anesthesia_trajectory{TAG}.json")
    results = json.load(open(resp))
    # propofol windows from existing JSONL
    rows = [json.loads(l) for l in open(os.path.join(HERE, "trajectory_windows_propofol_george.jsonl"))]
    inj, d0, d1 = _sess_meta(os.path.join(DATA, "GEO_PF_ext"))
    total_sec = max(r["t_center"] for r in rows) + T.WIN_SEC / 2
    results["sessions"]["propofol"] = dict(
        agent="propofol", n_channels=128, total_sec=float(total_sec),
        injection_t=inj, deep_t0=d0, deep_t1=d1, windows=rows)
    # propofol baseline levels
    bwin = json.load(open(os.path.join(HERE, "baseline_windows_propofol_george.json")))
    def med(key, absv=False):
        v = np.array([abs(r[key]) if absv else r[key] for r in bwin]); return [float(np.median(v)), float(np.std(v)), len(v)]
    results["baseline"]["propofol"] = dict(
        n_win=len(bwin), k_eff=med("k_eff"), rho_kish=med("rho_kish"),
        db_z_winding=med("db_z_winding", True), db_z_circ_sum=med("db_z_circ_sum", True))
    # order sessions propofol first for readability
    results["sessions"] = {k: results["sessions"][k] for k in ["propofol", "ketamine"] if k in results["sessions"]}
    results["baseline"] = {k: results["baseline"][k] for k in ["propofol", "ketamine"] if k in results["baseline"]}
    json.dump(results, open(resp, "w"), indent=1)
    print("assembled both agents into", resp)
    print("  agents:", list(results["sessions"].keys()))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    if mode == "baseline":
        do_baseline()
    elif mode == "assemble":
        do_assemble()
    else:
        print("usage: assemble.py [baseline|assemble]")

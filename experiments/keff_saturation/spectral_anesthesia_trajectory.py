#!/usr/bin/env python3
"""
DYNAMICAL two-axis test: does a real system MOVE THROUGH the 2x2 during a graded
loss of consciousness under anesthesia?  The framework's dynamical claim is that
maintenance (gamma*M, Axis 2 = detailed balance) is what HOLDS the corridor, so as
consciousness fades the DB signal should drop BEFORE or WITH the structural
(k_eff / Axis 1) collapse -- maintenance withdrawal PRECEDES/ACCOMPANIES the rank
collapse, not follows it.

Dynamical complement to the STATIC axis-independence proof
(spectral_axis_independence.py). We slide a window across the CONTINUOUS Session2
recording -- awake (pre-injection) -> injection -> INDUCTION (graded) -> deep
anesthesia -- and read both axes per window, then compare the TIMING of the two
collapses. Session2 is one continuous acquisition (no concatenation gaps); the
long Session1 awake block sets a robust awake baseline LEVEL for both axes.

NeuroTycho (Yanagawa, Fujii; RIKEN) macaque Chibi, 128-ch subdural ECoG, 1 kHz.
  PF Session2: injection@86s, Anesthetized 553-1098s  (induction ~7.8 min)
  KT Session2: injection@24s, Anesthetized 917-1502s  (induction ~14.9 min)

Axis 1 (STRUCTURE): k_eff = participation ratio of the channel correlation
eigenspectrum (spectral_test.corr_eig / participation_ratio); rho_Kish inverted.
Axis 2 (MAINTENANCE): detailed-balance |z| two ways --
  (a) winding-rate z (entropy_production.irreversibility_from_units, k=4;
      block-bootstrap null) -- validated, wants long continuous T,
  (b) direct circulation <x dy - y dx> vs PHASE-RANDOMIZED null -- the robust
      fallback at short window T (spectral_galaxy_db style).

GRAIN CAVEAT (carried honestly): ECoG is a mesoscopic neural FIELD, not single
units. Residual shared-field structure inflates absolute correlation, so only
WITHIN-session temporal DIFFERENCES are read; absolute levels are field/reference
confounded. NO re-reference (CAR injects spurious anticorrelation, biases k_eff).

BAND CAVEAT: the two-pole test found the exit pole was band-dependent. Primary
band = broadband 1-100 Hz (two-pole primary, where propofol's DB drop held);
probe another via TRAJ_BAND="lo,hi".

Reuses estimators verbatim: spectral_test (corr_eig, participation_ratio),
entropy_production (irreversibility_from_units). Circulation null mirrors
spectral_galaxy_db.db_stats. Real data only. Per-window JSONL flush = crash-safe.
"""
import os, sys, json, glob, re, time
import numpy as np
from scipy import signal
from scipy.io import loadmat

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spectral_test import corr_eig, participation_ratio
import entropy_production as ep

# ---------------- config ----------------
FS_RAW   = 1000.0
FS       = float(os.environ.get("TRAJ_FS", 250.0))
BAND     = tuple(float(x) for x in os.environ.get("TRAJ_BAND", "1,100").split(","))
NOTCH_HZ = 50.0
WIN_SEC  = float(os.environ.get("TRAJ_WIN", 20.0))
STEP_SEC = float(os.environ.get("TRAJ_STEP", 5.0))
DB_K     = 4
NNULL    = int(os.environ.get("TRAJ_NNULL", 1000))
MAXCH    = 128

# ---------------- circulation estimator (mirrors spectral_galaxy_db.db_stats) ---
def _modes_local(seg, k=4):
    Z = (seg - seg.mean(1, keepdims=True)) / (seg.std(1, keepdims=True) + 1e-12)
    U, S, Vt = np.linalg.svd(Z, full_matrices=False)
    return (S[:, None] * Vt)[:k]

def _omega(x, y):
    dx = np.diff(x); dy = np.diff(y); xm = x[:-1]; ym = y[:-1]
    den = np.mean(xm**2 + ym**2)
    return float(np.mean(xm*dy - ym*dx) / den) if den > 0 else 0.0

def _phaserand(v, rng):
    F = np.fft.rfft(v); ph = np.exp(1j*rng.uniform(0, 2*np.pi, F.shape)); ph[0] = 1
    return np.fft.irfft(F*ph, n=len(v))

def circ_db(seg, k=4, npair=3, nnull=NNULL, seed=0):
    """Direct circulation vs phase-randomized null on top-k SVD modes. Returns
    (top-pair signed z, summed-|omega| z). Robust at short window T (galaxy-DB
    estimator; validated ruler: OU-eq ~1.2, driven NESS >>2)."""
    rng = np.random.default_rng(seed)
    A = _modes_local(seg, k)
    pairs = [(i, j) for i in range(npair) for j in range(i+1, npair)]
    obs_sum = 0.0; null_sum = np.zeros(nnull); best_z = 0.0
    for (i, j) in pairs:
        obs = _omega(A[i], A[j])
        null = np.array([_omega(_phaserand(A[i], rng), _phaserand(A[j], rng)) for _ in range(nnull)])
        z = (obs - null.mean()) / (null.std() + 1e-12)
        if abs(z) > abs(best_z): best_z = z
        obs_sum += abs(obs); null_sum += np.abs(null)
    zc = (obs_sum - null_sum.mean()) / (null_sum.std() + 1e-12)
    return float(best_z), float(zc)

# ---------------- ECoG loading ----------------
def _asstr(x):
    a = np.asarray(x).ravel()
    if a.size == 1:
        v = a[0]
        return _asstr(v) if isinstance(v, np.ndarray) else str(v)
    return "".join(str(c) for c in a)

def read_conditions(subrec_dir):
    """-> (interval_segs [(base,t0,t1)], bare_markers [(label,t)])."""
    cpath = os.path.join(subrec_dir, "Condition.mat")
    if not os.path.exists(cpath):
        return [], []
    m = loadmat(cpath, squeeze_me=True, struct_as_record=False)
    labels = [_asstr(x).strip() for x in np.atleast_1d(m["ConditionLabel"])]
    times  = np.atleast_1d(np.asarray(m["ConditionTime"], float)).ravel()
    open_ev, segs, bare = {}, [], []
    for lab, t in zip(labels, times):
        t = float(t)
        if lab.endswith("-Start"): open_ev[lab[:-6]] = t
        elif lab.endswith("-End"):
            base = lab[:-4]
            if base in open_ev: segs.append((base, open_ev.pop(base), t))
        else: bare.append((lab, t))
    return segs, bare

def _load_channel(fp):
    m = loadmat(fp, squeeze_me=True)
    cand = [k for k in m if not k.startswith("__")]
    cand.sort(key=lambda k: (0 if "ecog" in k.lower() else 1, -np.asarray(m[k]).size))
    return np.asarray(m[cand[0]], float).ravel()

def _preprocess(x, band):
    b, a = signal.iirnotch(NOTCH_HZ / (FS_RAW / 2), Q=30)
    x = signal.filtfilt(b, a, x)
    sos = signal.butter(4, [band[0] / (FS_RAW / 2), band[1] / (FS_RAW / 2)],
                        btype="band", output="sos")
    x = signal.sosfiltfilt(sos, x)
    q = int(round(FS_RAW / FS))
    return signal.decimate(x, q, ftype="iir", zero_phase=True)

def build_session(session_dir, band, chans=None):
    """Load ONE session dir continuously -> (M [chan x time] at FS, chans,
    segs, bare)."""
    def chan_nums(sd):
        fs = glob.glob(os.path.join(sd, "ECoG_ch*.mat"))
        return {int(re.search(r"ch(\d+)\.mat", os.path.basename(f)).group(1)) for f in fs}
    if chans is None:
        chans = sorted(chan_nums(session_dir))[:MAXCH]
    proc = [ _preprocess(_load_channel(os.path.join(session_dir, f"ECoG_ch{ch}.mat")), band)
             for ch in chans ]
    L = min(len(v) for v in proc)
    M = np.vstack([v[:L] for v in proc])
    segs, bare = read_conditions(session_dir)
    return M, chans, segs, bare

def session_dir(agent_root, n):
    matches = glob.glob(os.path.join(agent_root, "**", f"Session{n}"), recursive=True)
    matches = [m for m in matches if os.path.isdir(m)]
    return matches[0] if matches else None

# ---------------- windowed trajectory ----------------
def good_mask(M):
    return np.isfinite(M).all(1) & (M.std(1) > 1e-9)

def epoch_of(tc, injection_t, deep_t0, deep_t1):
    if injection_t is not None and tc < injection_t: return "awake"
    if deep_t0 is not None and tc >= deep_t0 and tc <= deep_t1: return "deep"
    if injection_t is not None and tc >= injection_t and (deep_t0 is None or tc < deep_t0): return "induction"
    return "post"

def window_metrics(M, s0, win, epoch, seed):
    seg = M[:, s0:s0+win]
    N = seg.shape[0]
    ev, _, _ = corr_eig(seg)
    keff = float(participation_ratio(ev))
    rho_kish = float((N/keff - 1)/(N - 1))
    wz = float(ep.irreversibility_from_units(seg, k=DB_K, seed=0)["z"])
    cz_top, cz_sum = circ_db(seg, k=DB_K, seed=seed)
    return dict(k_eff=keff, rho_kish=rho_kish, db_z_winding=wz,
                db_z_circ_top=cz_top, db_z_circ_sum=cz_sum, epoch=epoch)

def run_trajectory(agent, s2_dir, band, tag):
    """Slide windows across Session2 continuous timeline. Flush JSONL per window."""
    M, chans, segs, bare = build_session(s2_dir, band)
    mask = good_mask(M); M = M[mask]
    N, Ttot = M.shape
    inj = next((t for lab, t in bare if "Injection" in lab and "Antagonist" not in lab), None)
    deep = next(((t0, t1) for base, t0, t1 in segs if base == "Anesthetized"), (None, None))
    deep_t0, deep_t1 = deep
    print(f"\n### {agent} Session2  {N}/{len(chans)} ch  {Ttot/FS:.0f}s "
          f"({Ttot/FS/60:.1f} min)  inj@{inj}  deep {deep_t0}-{deep_t1}")
    win = int(WIN_SEC*FS); step = int(STEP_SEC*FS)
    starts = list(range(0, Ttot - win + 1, step))
    # cap trajectory at end of deep epoch (ignore the gap-to-recovery tail)
    if deep_t1 is not None:
        starts = [s for s in starts if (s+win)/FS <= deep_t1 + 5]
    print(f"  {len(starts)} windows (win={WIN_SEC}s step={STEP_SEC}s) up to t={deep_t1}s")
    jf = open(os.path.join(HERE, f"trajectory_windows_{agent}{tag}.jsonl"), "w")
    rows = []
    t0 = time.time()
    for wi, s0 in enumerate(starts):
        tc = (s0 + win/2)/FS
        ep_ = epoch_of(tc, inj, deep_t0, deep_t1)
        m = window_metrics(M, s0, win, ep_, seed=wi)
        m.update(w=wi, t_center=float(tc))
        rows.append(m)
        jf.write(json.dumps(m) + "\n"); jf.flush()
        if wi % 15 == 0 or wi == len(starts)-1:
            print(f"    w{wi:3d} t={tc:6.1f} [{ep_:9s}] keff={m['k_eff']:5.2f} "
                  f"rhoK={m['rho_kish']:.3f} |wind|={abs(m['db_z_winding']):4.2f} "
                  f"|circ|={abs(m['db_z_circ_sum']):4.2f}")
    jf.close()
    print(f"  ({time.time()-t0:.0f}s)")
    return dict(agent=agent, n_channels=int(N), total_sec=float(Ttot/FS),
                injection_t=inj, deep_t0=deep_t0, deep_t1=deep_t1,
                windows=rows, chans=chans, mask_idx=[int(i) for i in np.where(mask)[0]])

def baseline_levels(agent, s1_dir, band, chans, tag):
    """Robust awake-baseline levels from Session1 (long awake block).
    Non-overlapping 20s windows over the whole awake session."""
    M, _, segs, bare = build_session(s1_dir, band, chans=chans)
    mask = good_mask(M); M = M[mask]
    N, Ttot = M.shape
    win = int(WIN_SEC*FS)
    # windows fully inside an 'awake' interval
    awake_iv = [(t0, t1) for base, t0, t1 in segs if base.startswith("Awake")]
    rows = []
    for (a, b) in awake_iv:
        i0, i1 = int(a*FS), int(min(b, Ttot/FS)*FS)
        for s0 in range(i0, i1 - win + 1, win):
            m = window_metrics(M, s0, win, "awake_s1", seed=10000+len(rows))
            m["t_center"] = float((s0+win/2)/FS)
            rows.append(m)
    def med(key, absv=False):
        v = np.array([abs(r[key]) if absv else r[key] for r in rows])
        return float(np.median(v)), float(np.std(v)), len(v)
    lv = dict(n_win=len(rows),
              k_eff=med("k_eff"), rho_kish=med("rho_kish"),
              db_z_winding=med("db_z_winding", True), db_z_circ_sum=med("db_z_circ_sum", True))
    print(f"  Session1 awake baseline ({len(rows)} win): "
          f"k_eff={lv['k_eff'][0]:.2f} |wind|={lv['db_z_winding'][0]:.2f} "
          f"|circ|={lv['db_z_circ_sum'][0]:.2f}")
    # save baseline windows too
    json.dump(rows, open(os.path.join(HERE, f"baseline_windows_{agent}{tag}.json"), "w"), indent=1)
    return lv

# ---------------- ordering analysis ----------------
def smooth(y, k=3):
    return np.array([np.median(y[max(0,i-k//2):i+k//2+1]) for i in range(len(y))])

def crossing(rows, key, awake_level, deep_states, use_abs=True, restrict=None):
    """First time the smoothed |key| trajectory crosses the midpoint between the
    awake baseline level and the deep-epoch median. restrict=(lo,hi) time window."""
    ts = np.array([r["t_center"] for r in rows])
    y  = np.array([abs(r[key]) if use_abs else r[key] for r in rows], float)
    dv = np.array([abs(r[key]) if use_abs else r[key] for r in rows if r["epoch"] in deep_states])
    if len(dv) == 0 or not np.isfinite(awake_level):
        return dict(t_cross=None, note="no deep windows or no baseline")
    deep_level = float(np.median(dv))
    mid = 0.5*(awake_level + deep_level)
    ys = smooth(y, 3)
    lo, hi = (restrict if restrict else (ts.min(), ts.max()))
    t_cross = None
    for i in range(1, len(ts)):
        if ts[i] < lo or ts[i] > hi: continue
        if (ys[i-1]-mid)*(ys[i]-mid) < 0:
            f = (mid - ys[i-1])/(ys[i]-ys[i-1])
            t_cross = float(ts[i-1] + f*(ts[i]-ts[i-1])); break
    return dict(t_cross=t_cross, awake_level=float(awake_level), deep_level=deep_level,
                mid=float(mid), separation=float(abs(deep_level-awake_level)),
                direction="down" if deep_level < awake_level else "up")

def analyze(traj, base):
    rows = traj["windows"]
    inj = traj["injection_t"]; d0 = traj["deep_t0"]; d1 = traj["deep_t1"]
    # search the induction window (injection -> a bit past deep onset)
    restrict = (inj if inj else 0, (d0 + 60) if d0 else traj["total_sec"])
    out = {"restrict": restrict}
    out["k_eff"]       = crossing(rows, "k_eff",        base["k_eff"][0],       {"deep"}, use_abs=False, restrict=restrict)
    out["db_winding"]  = crossing(rows, "db_z_winding", base["db_z_winding"][0], {"deep"}, use_abs=True, restrict=restrict)
    out["db_circ_sum"] = crossing(rows, "db_z_circ_sum",base["db_z_circ_sum"][0],{"deep"}, use_abs=True, restrict=restrict)
    return out

def main():
    data_root = os.environ.get("TRAJ_DATA",
        "/tmp/claude-1000/-home-emoore-coherence-ratchet/"
        "a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/neuro")
    tag  = os.environ.get("TRAJ_TAG", "")
    band = BAND
    agents = [("propofol", os.path.join(data_root, os.environ.get("TRAJ_PF_DIR","PF_ext"))),
              ("ketamine", os.path.join(data_root, os.environ.get("TRAJ_KT_DIR","KT_ext")))]
    only = os.environ.get("TRAJ_ONLY")  # e.g. "propofol"
    results = {"meta": dict(
        source="NeuroTycho Yanagawa/Fujii macaque Chibi 128ch ECoG 1kHz",
        fs=FS, band=list(band), notch=NOTCH_HZ, win_sec=WIN_SEC, step_sec=STEP_SEC,
        db_k=DB_K, nnull=NNULL, reref="none (per-channel z-score)",
        axis1="k_eff = participation ratio of channel corr spectrum (spectral_test)",
        axis2a="winding |z| (entropy_production.irreversibility_from_units k=4, block-bootstrap null)",
        axis2b="direct circulation |z| vs phase-randomized null (spectral_galaxy_db style)"),
        "sessions": {}, "baseline": {}, "ordering": {}}
    outp = os.path.join(HERE, f"spectral_results_anesthesia_trajectory{tag}.json")

    for agent, root in agents:
        if only and agent != only: continue
        s2 = session_dir(root, 2); s1 = session_dir(root, 1)
        if not s2:
            print(f"!! no Session2 under {root}; skip {agent}"); continue
        traj = run_trajectory(agent, s2, band, tag)
        base = baseline_levels(agent, s1, band, traj["chans"], tag) if s1 else \
               {k: (float("nan"),float("nan"),0) for k in ("k_eff","rho_kish","db_z_winding","db_z_circ_sum")}
        results["sessions"][agent] = {k:v for k,v in traj.items() if k not in ("chans","mask_idx")}
        results["baseline"][agent] = base
        results["ordering"][agent] = analyze(traj, base)
        json.dump(results, open(outp, "w"), indent=1)   # flush after each agent
        print(f"  flushed after {agent}")

    print("\nwrote", outp)
    print("\n=== ORDERING VERDICT (does gamma*M / DB drop BEFORE / WITH / AFTER k_eff?) ===")
    for agent in results["ordering"]:
        o = results["ordering"][agent]
        print(f"\n{agent}:  (induction search window {o['restrict'][0]:.0f}-{o['restrict'][1]:.0f}s)")
        for lbl, key in [("k_eff (Axis1)","k_eff"), ("DB winding (Axis2a)","db_winding"),
                         ("DB circ (Axis2b)","db_circ_sum")]:
            r = o[key]; tc = r.get("t_cross")
            print(f"  {lbl:22s}: cross@{('%.1f'%tc) if tc is not None else 'None':>7s}s  "
                  f"awake={r.get('awake_level',float('nan')):.2f} deep={r.get('deep_level',float('nan')):.2f} "
                  f"sep={r.get('separation',float('nan')):.2f} {r.get('direction','')}")
        tk = o["k_eff"].get("t_cross"); tw = o["db_winding"].get("t_cross"); tcz = o["db_circ_sum"].get("t_cross")
        for name, tdb in [("winding", tw), ("circ", tcz)]:
            if tk is None or tdb is None:
                print(f"  ordering vs {name}: UNRESOLVED (a crossing is undefined)")
            else:
                d = tdb - tk
                verdict = "WITH" if abs(d) < WIN_SEC else ("AFTER k_eff" if d > 0 else "BEFORE k_eff")
                print(f"  ordering vs {name}: DB drops {verdict}  (t_DB-t_keff = {d:+.1f}s)")

if __name__ == "__main__":
    main()

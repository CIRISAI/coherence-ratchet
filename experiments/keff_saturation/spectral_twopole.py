#!/usr/bin/env python3
"""
TWO-POLE dynamics test on macaque ECoG anesthesia data (NeuroTycho / Yanagawa,
Fujii; monkey Chibi, 128-ch subdural array, 1 kHz).

The dynamics claim is now the two-pole form  dρ/dt = α − γ·M.  At M=0 (maintenance
withdrawn) the system leaves the corridor toward the pole selected by sign(α):
  RIGIDITY  (ρ→1, k_eff→1)  — synchronizing agents (propofol: GABA-A slow-wave sync)
  CHAOS     (ρ→0, k_eff→N)  — desynchronizing agents (ketamine: dissociative,
                              high-frequency desynchronization).

STRONG (falsifiable) prediction, not just "exits somewhere":
  propofol  → ρ↑ / k_eff↓  (rigidity pole)
  ketamine  → ρ↓ / k_eff↑  (chaos pole)
Two agents going to two DIFFERENT poles is the signature with predictive content.

Maintenance-withdrawal signature (should hold for EITHER pole): detailed-balance
|z| DROPS under anesthesia (less active γ·M, closer to reversible/equilibrium).

Grain fix vs the earlier arousal test: NEURAL field potentials (subdural ECoG),
not volume-conducted scalp EEG. Perturbation fix: clean graded pharmacology with
DIFFERENT AGENTS predicted to hit DIFFERENT poles, not post-anoxic damage.

Matched preprocessing across ALL states (awake / drug / recovery): identical
channel set, band, notch, downsample, window length; per-channel z-score; NO
re-reference (common-average reference would inject spurious anticorrelation and
bias k_eff). Only WITHIN-session, matched awake-vs-drug DIFFERENCES are read;
absolute k_eff is field/reference confounded. Analysis core reused verbatim from
spectral_test.py (corr_eig, participation_ratio) and entropy_production.py
(irreversibility_from_units, k=4).

Real data only. No commit, no .lean edits.
"""
import os, sys, json, zipfile, glob, re
import numpy as np
from scipy import signal
from scipy.io import loadmat

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spectral_test import corr_eig, participation_ratio
import entropy_production as ep

FS_RAW   = 1000.0     # NeuroTycho anesthesia sampling rate (Hz)
FS       = float(os.environ.get("TWOPOLE_FS", 250.0))  # analysis rate after decimation
# BAND matched across states; override with TWOPOLE_BAND="lo,hi" to probe the band
# where a mechanism lives (e.g. gamma 30-90 for ketamine desynchronization).
BAND     = tuple(float(x) for x in os.environ.get("TWOPOLE_BAND", "1,100").split(","))
NOTCH_HZ = 50.0       # RIKEN Wako mains
WIN_SEC  = 20.0       # analysis window length (matched)
N_WIN    = 12         # windows per state (matched; fewer if a state is short)
DB_K     = 4          # top modes for detailed-balance winding
RNG      = np.random.default_rng(0)

# --- condition-label -> coarse state (matched pooling) ----------------------
# NeuroTycho labels carry -Start/-End suffixes and are split across per-agent
# sub-recordings (Session1 awake baseline, Session2 injection+anesthetized+
# recovery, Session3 recovery-open). We pair Start/End into intervals and pool
# by the base label. Same implant across sub-recordings -> channels correspond.
STATE_OF = {
    "AwakeEyesOpened": "awake", "AwakeEyesClosed": "awake",
    "Anesthetized": "drug",
    "RecoveryEyesOpened": "recovery", "RecoveryEyesClosed": "recovery",
}
# labels we never analyze (transient injection epochs)
SKIP = {"AnestheticInjection", "AntagonistInjection", "Injection"}


def _asstr(x):
    """MATLAB cell/char -> python str."""
    a = np.asarray(x).ravel()
    if a.size == 1:
        v = a[0]
        if isinstance(v, np.ndarray):
            return _asstr(v)
        return str(v)
    return "".join(str(c) for c in a)


def read_conditions(subrec_dir):
    """Parse one sub-recording's Condition.mat into (base_label, t0, t1) intervals.
    Labels come as '<Base>-Start' / '<Base>-End' pairs with ConditionTime [sec]."""
    cpath = os.path.join(subrec_dir, "Condition.mat")
    if not os.path.exists(cpath):
        return [], cpath
    m = loadmat(cpath, squeeze_me=True, struct_as_record=False)
    labels = [ _asstr(x).strip() for x in np.atleast_1d(m["ConditionLabel"]) ]
    times  = np.atleast_1d(np.asarray(m["ConditionTime"], float)).ravel()
    open_ev = {}
    segs = []
    for lab, t in zip(labels, times):
        t = float(t)
        if lab.endswith("-Start"):
            open_ev[lab[:-6]] = t
        elif lab.endswith("-End"):
            base = lab[:-4]
            if base in open_ev:
                segs.append((base, open_ev.pop(base), t))
        else:
            # bare marker (e.g. AnestheticInjection) — no interval
            continue
    return segs, cpath


def _load_channel(fp):
    """Load one ECoG_chN.mat -> 1D float array (auto-detect the data var)."""
    m = loadmat(fp, squeeze_me=True)
    cand = [k for k in m if not k.startswith("__")]
    # prefer a var whose name contains 'ECoG'
    cand.sort(key=lambda k: (0 if "ecog" in k.lower() else 1, -np.asarray(m[k]).size))
    arr = np.asarray(m[cand[0]], float).ravel()
    return arr


def _preprocess(x, fs_raw=FS_RAW, fs=FS, band=BAND, notch=NOTCH_HZ):
    """1D raw -> notch, bandpass, decimate to fs. Applied identically per channel."""
    # notch
    b, a = signal.iirnotch(notch / (fs_raw / 2), Q=30)
    x = signal.filtfilt(b, a, x)
    # bandpass
    sos = signal.butter(4, [band[0] / (fs_raw / 2), band[1] / (fs_raw / 2)],
                        btype="band", output="sos")
    x = signal.sosfiltfilt(sos, x)
    # decimate
    q = int(round(fs_raw / fs))
    x = signal.decimate(x, q, ftype="iir", zero_phase=True)
    return x


def _subrecordings(agent_dir):
    """Return the SessionK sub-recording dirs (each holds Condition.mat + channels)."""
    subs = sorted(glob.glob(os.path.join(agent_dir, "**", "Session*"), recursive=True))
    subs = [d for d in subs if os.path.isdir(d) and os.path.exists(os.path.join(d, "Condition.mat"))]
    if not subs:
        # fall back: agent_dir itself holds the channels
        if os.path.exists(os.path.join(agent_dir, "Condition.mat")):
            subs = [agent_dir]
    return subs


def build_state_matrices(agent_dir, max_channels=128):
    """Aggregate states ACROSS sub-recordings. Returns dict state ->
    (channels x time) matrix at FS, the channel numbers used, and a printable
    segment table. For each state we concatenate the matched-channel samples from
    every sub-recording interval carrying that state."""
    subs = _subrecordings(agent_dir)
    if not subs:
        raise FileNotFoundError("no Session* sub-recordings under %s" % agent_dir)

    # per state: list of (subrec_dir, t0, t1); also a printable table
    state_ivs = {}
    table = []
    for sd in subs:
        segs, _ = read_conditions(sd)
        for base, t0, t1 in segs:
            st = STATE_OF.get(base)
            table.append((os.path.basename(sd), base, t0, t1, st or "-"))
            if st and (t1 - t0) >= WIN_SEC:
                state_ivs.setdefault(st, []).append((sd, t0, t1))
    if not state_ivs:
        raise RuntimeError("no analyzable state intervals in %s" % agent_dir)

    # channel numbers present in ALL involved sub-recordings (matched set)
    involved = sorted({sd for ivs in state_ivs.values() for sd, _, _ in ivs})
    def chan_nums(sd):
        fs = glob.glob(os.path.join(sd, "ECoG_ch*.mat"))
        return {int(re.search(r"ch(\d+)\.mat", os.path.basename(f)).group(1)) for f in fs}
    common = set.intersection(*[chan_nums(sd) for sd in involved])
    chans = sorted(common)[:max_channels]

    # loop channel-outer, sub-recording-inner; accumulate per-state sample vectors
    per_state = {st: [[] for _ in chans] for st in state_ivs}
    for ci, ch in enumerate(chans):
        # preprocess this channel once per involved sub-recording (cache)
        cache = {}
        for st, ivs in state_ivs.items():
            chunks = []
            for sd, t0, t1 in ivs:
                if sd not in cache:
                    cache[sd] = _preprocess(_load_channel(os.path.join(sd, f"ECoG_ch{ch}.mat")))
                proc = cache[sd]
                i0, i1 = int(t0 * FS), int(min(t1, len(proc) / FS) * FS)
                chunks.append(proc[i0:i1])
            per_state[st][ci] = np.concatenate(chunks) if chunks else np.array([])

    mats = {}
    for st in per_state:
        L = min(len(c) for c in per_state[st])
        mats[st] = np.vstack([c[:L] for c in per_state[st]])   # channels x time
    return mats, chans, table


def good_channel_mask(mats):
    """Channels finite & non-constant in EVERY state (matched channel set)."""
    N = next(iter(mats.values())).shape[0]
    mask = np.ones(N, bool)
    for M in mats.values():
        mask &= np.isfinite(M).all(1) & (M.std(1) > 1e-9)
    return mask


def window_metrics(M, win_samp, n_win):
    """Split channels x time into n_win non-overlapping windows; per window compute
    k_eff (PR of correlation eigenvalues), mean off-diagonal |corr| and signed ρ̄,
    ρ_Kish, and detailed-balance |z|."""
    N, T = M.shape
    n_have = T // win_samp
    n = min(n_win, n_have)
    res = []
    for w in range(n):
        seg = M[:, w * win_samp:(w + 1) * win_samp]
        ev, _, _ = corr_eig(seg)
        keff = participation_ratio(ev)
        # mean off-diagonal correlation
        Z = (seg - seg.mean(1, keepdims=True)) / (seg.std(1, keepdims=True) + 1e-12)
        C = (Z @ Z.T) / seg.shape[1]
        iu = np.triu_indices(N, 1)
        rho_bar = float(C[iu].mean())
        rho_absbar = float(np.abs(C[iu]).mean())
        # Kish inversion: keff = k/(1+rho(k-1)) -> rho = (k/keff - 1)/(k-1)
        rho_kish = float((N / keff - 1) / (N - 1))
        z = ep.irreversibility_from_units(seg, k=DB_K)["z"]
        res.append(dict(k_eff=float(keff), rho_bar=rho_bar, rho_absbar=rho_absbar,
                        rho_kish=rho_kish, db_z=float(z)))
    return res


def summarize(res):
    def m(key):
        v = np.array([r[key] for r in res], float)
        return float(np.mean(v)), float(np.std(v)), v
    out = {}
    for key in ("k_eff", "rho_bar", "rho_absbar", "rho_kish", "db_z"):
        mean, sd, v = m(key)
        out[key] = dict(mean=mean, sd=sd)
    out["db_absz_median"] = float(np.median(np.abs([r["db_z"] for r in res])))
    out["n_win"] = len(res)
    return out


def run_session(name, agent, sess_dir):
    print(f"\n### {name}  (agent={agent})  dir={sess_dir}")
    mats, chans, table = build_state_matrices(sess_dir)
    print("  segments (across sub-recordings):")
    for sub, lab, t0, t1, tag in table:
        print(f"    {sub:9s} {lab:22s} {t0:8.1f}s -> {t1:8.1f}s   [{tag}]")
    for st, M in mats.items():
        print(f"    state {st:9s}: {M.shape[0]} ch x {M.shape[1]/FS:.0f}s")
    mask = good_channel_mask(mats)
    print(f"  good channels (matched, all states): {int(mask.sum())} / {mask.size}")
    win_samp = int(WIN_SEC * FS)
    out = {"session": name, "agent": agent, "dir": os.path.basename(sess_dir),
           "n_channels": int(mask.sum()), "channels_total": int(mask.size),
           "fs": FS, "band": BAND, "win_sec": WIN_SEC, "states": {}}
    per_state_win = {}
    for st, M in mats.items():
        Mg = M[mask]
        res = window_metrics(Mg, win_samp, N_WIN)
        per_state_win[st] = res
        s = summarize(res)
        out["states"][st] = s
        print(f"  {st:9s}: k_eff={s['k_eff']['mean']:5.2f}±{s['k_eff']['sd']:.2f}  "
              f"rho_bar={s['rho_bar']['mean']:+.3f}  rho_kish={s['rho_kish']['mean']:.3f}  "
              f"|DBz|med={s['db_absz_median']:.2f}  (n={s['n_win']})")
    out["_windows"] = per_state_win
    return out


def mannwhitney(a, b):
    """Two-sided Mann-Whitney U (no scipy dependency edge-cases); returns p."""
    from scipy.stats import mannwhitneyu
    try:
        return float(mannwhitneyu(a, b, alternative="two-sided").pvalue)
    except Exception:
        return float("nan")


def contrast(out, base="awake", drug="drug"):
    """awake vs drug within a session: effect direction + significance."""
    W = out["_windows"]
    if base not in W or drug not in W:
        return None
    c = {}
    for key in ("k_eff", "rho_bar", "rho_kish", "rho_absbar"):
        a = np.array([r[key] for r in W[base]])
        b = np.array([r[key] for r in W[drug]])
        pooled_sd = np.sqrt((a.var() + b.var()) / 2) + 1e-12
        d = (b.mean() - a.mean()) / pooled_sd    # drug - awake (Cohen's d)
        c[key] = dict(awake=float(a.mean()), drug=float(b.mean()),
                      delta=float(b.mean() - a.mean()), cohen_d=float(d),
                      mw_p=mannwhitney(a, b))
    az = np.abs([r["db_z"] for r in W[base]]); bz = np.abs([r["db_z"] for r in W[drug]])
    c["db_absz"] = dict(awake=float(np.median(az)), drug=float(np.median(bz)),
                        delta=float(np.median(bz) - np.median(az)),
                        mw_p=mannwhitney(az, bz))
    return c


def main():
    data_root = os.environ.get("TWOPOLE_DATA",
        "/tmp/claude-1000/-home-emoore-coherence-ratchet/"
        "a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/neuro")
    sessions = [("Chibi_propofol", "propofol", os.path.join(data_root, "PF_ext")),
                ("Chibi_ketamine", "ketamine", os.path.join(data_root, "KT_ext"))]
    results = {"meta": dict(source="NeuroTycho Yanagawa/Fujii macaque Chibi 128ch ECoG 1kHz",
                            fs=FS, band=BAND, notch=NOTCH_HZ, win_sec=WIN_SEC,
                            n_win=N_WIN, db_k=DB_K, reref="none (per-channel z-score)"),
               "sessions": {}, "contrasts": {}}
    for name, agent, d in sessions:
        if not os.path.isdir(d):
            print(f"!! missing {d} -- skipping"); continue
        out = run_session(name, agent, d)
        c = contrast(out)
        out.pop("_windows_saved", None)
        # keep windows for json but drop bulky arrays already summarized
        results["sessions"][name] = {k: v for k, v in out.items() if k != "_windows"}
        results["sessions"][name]["windows"] = out["_windows"]
        results["contrasts"][name] = c
        if c:
            print(f"  --> awake→{agent}:  "
                  f"Δk_eff={c['k_eff']['delta']:+.2f} (d={c['k_eff']['cohen_d']:+.2f}, p={c['k_eff']['mw_p']:.3g})  "
                  f"Δρ_kish={c['rho_kish']['delta']:+.3f} (d={c['rho_kish']['cohen_d']:+.2f})  "
                  f"Δ|DBz|={c['db_absz']['delta']:+.2f}")

    tag = os.environ.get("TWOPOLE_TAG", "")
    outpath = os.path.join(HERE, f"spectral_results_twopole{tag}.json")
    json.dump(results, open(outpath, "w"), indent=1)
    print("\nwrote", outpath)

    # ---- verdict ----------------------------------------------------------
    print("\n=== TWO-POLE VERDICT ===")
    def pole(c):
        dk = c["k_eff"]["delta"]; dr = c["rho_kish"]["delta"]
        if dk < 0 and dr > 0:  return "RIGIDITY (k_eff↓, ρ↑)"
        if dk > 0 and dr < 0:  return "CHAOS (k_eff↑, ρ↓)"
        return "mixed/unclear"
    for name, agent, _ in sessions:
        c = results["contrasts"].get(name)
        if not c: continue
        predicted = "RIGIDITY" if agent == "propofol" else "CHAOS"
        obs = pole(c)
        match = "MATCH" if predicted in obs else "MISS"
        print(f"  {agent:9s}: predicted {predicted:8s} | observed {obs:22s} -> {match}"
              f" | Δ|DBz|={c['db_absz']['delta']:+.2f} ({'drop' if c['db_absz']['delta']<0 else 'rise'})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
DECISIVE tautology-vs-content test for the k_eff-saturation universality.

Question: is neural effective dimensionality k_eff BOUNDED BY / DRIVEN BY the
dimensionality of the shared driver (the stimulus), or is the low-rank
saturation INTRINSIC (invariant to the driver)?
  - CONTENT (mechanistic law): k_eff tracks the shared-driver dimensionality.
  - TAUTOLOGY / intrinsic     : k_eff is ~flat across driver dimensionality.

CLEAN DESIGN (fixes the ZAPBench attempt, which used a fragile driver_dim~1):
  * Known, controllable stimulus battery with a WELL-ESTABLISHED dimensionality
    ordering (do NOT estimate driver_dim from fragile regressors):
        spontaneous (0-dim) < gratings (low, 1-2 params)
                            < natural scenes (mid) < natural movies (high).
  * WITHIN-RECORDING: same neurons, different stimulus blocks -> the grain /
    subsample confound that makes the ABSOLUTE k_eff of a cortex patch
    uninterpretable CANCELS, because we read the RELATIVE change of k_eff
    across stimulus types on the SAME units, same N, matched T.

Data: Allen Brain Observatory Visual Coding, 2-photon dF/F. Each experiment is
a session-type (A/B/C) with a different stimulus subset; every type contains
spontaneous + gratings + natural stimuli -> a within-recording ladder.
NWB fetched from api.brain-map.org (same path as spectral_test_allen.py),
extracted, deleted. Incremental flush to spectral_results_content.json.

Estimator core (corr_eig, participation_ratio, mp_edge, phase_randomize) is
REUSED VERBATIM from spectral_test.py. No fabricated data in the verdict.

k_eff readouts per stimulus block (same neurons, matched T):
  k_eff_cov     : PR of the covariance spectrum = framework's 1/Tr(rho_norm^2).
                  Raw; noise-inflated for 2p dF/F (reported for reference).
  eff_rank_surr : # correlation eigenvalues above a phase-randomized surrogate
                  floor (mean of the surrogate's top eigenvalue over reps).
                  NOISE-DEBIASED effective rank -- the PRIMARY readout, since
                  raw PR of 2p data is unusable without debiasing.
  keff_signal   : PR restricted to signal eigenvalues (ev - floor)_+ ; a
                  debiased continuous k_eff.
"""
import json
import os
import subprocess

import numpy as np
from scipy.stats import spearmanr, wilcoxon

from spectral_test import (corr_eig, participation_ratio, mp_edge,
                           phase_randomize)

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(HERE, "..", "structural_series", "data_allen", "results.json")
OUT = os.path.join(HERE, "spectral_results_content.json")
SUMMARY = os.path.join(HERE, "spectral_content_summary.md")
NWB_DIR = "/tmp/allen_nwb_mech"
API = "https://api.brain-map.org"
RNG = np.random.default_rng(0)
MIN_ROIS = 20
N_SURR = 6          # phase-randomization reps for the noise floor
T_CAP = 8000        # cap matched T (keeps q=N/T small, bounds runtime)

os.makedirs(NWB_DIR, exist_ok=True)

# Canonical stimulus-dimensionality ordering (the axis; NOT estimated).
STIM_RANK = {
    "spontaneous": 0,          # no driver
    "drifting_gratings": 1,    # low-dim: orientation x temporal-freq
    "static_gratings": 1,      # low-dim: orientation x spatial-freq x phase
    "natural_scenes": 2,       # mid: 118 natural images
    "natural_movie_one": 3,    # high: natural movie
    "natural_movie_two": 3,
    "natural_movie_three": 3,
    # locally_sparse_noise excluded from the ordinal test (ambiguous dim).
}
DFF = "processing/brain_observatory_pipeline/DfOverF/imaging_plane_1/data"


def api_get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "60", url],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def download_nwb(exp_id):
    path = os.path.join(NWB_DIR, f"{exp_id}.nwb")
    if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
        return path
    q = (f"{API}/api/v2/data/query.json?criteria=model::OphysExperiment,"
         f"rma::criteria,%5Bid$eq{exp_id}%5D,rma::include,"
         f"well_known_files(well_known_file_type)")
    d = api_get(q)
    link = None
    for m in d["msg"]:
        for w in m.get("well_known_files", []):
            if w.get("well_known_file_type", {}).get("name") == "NWBOphys":
                link = w["download_link"]
    if link is None:
        raise RuntimeError(f"no NWBOphys file for experiment {exp_id}")
    subprocess.run(["curl", "-sL", "--max-time", "600", "-o", path, API + link],
                   capture_output=True, text=True)
    if not os.path.exists(path) or os.path.getsize(path) < 1_000_000:
        raise RuntimeError(f"download failed for {exp_id}")
    return path


def stim_frames(f, name, ntot):
    """Sorted dF/F column indices during one stimulus presentation."""
    g = f[f"stimulus/presentation/{name}_stimulus"]
    fd = g["frame_duration"][:].astype(np.int64)
    if name == "spontaneous":                     # (2,2): [start; stop] block
        a, b = int(fd[0, 0]), int(fd[1, 0])
        idx = np.arange(a, b)
    else:                                         # per-trial / per-frame rows
        chunks = []
        for a, b in fd:
            if b <= a:
                b = a + 1
            chunks.append(np.arange(a, b))
        idx = np.unique(np.concatenate(chunks))
    return idx[(idx >= 0) & (idx < ntot)]


def match_T(idx, T):
    """First T frames of the block, CONTIGUOUS in stimulus time.

    Contiguous (not evenly-strided) so the temporal-autocorrelation structure
    is treated identically across blocks -- an evenly-spaced subsample would
    silently decorrelate the long (movie/grating) blocks but not the short
    (spontaneous) one, biasing every downstream spectral quantity.
    """
    return idx[:T] if len(idx) > T else idx


def autocorr_stride(X, thresh=0.2, cap=40):
    """Frames until the mean (over neurons) autocorrelation drops below thresh.

    Used to temporally DECORRELATE each block to ~independent samples, so the
    noise floor is comparable across stimuli with different temporal dynamics
    (natural movies are far smoother than gratings/spontaneous -> otherwise
    their higher autocorrelation inflates the surrogate floor and artefactually
    suppresses their detectable shared dimensionality).
    """
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)
    T = Z.shape[1]
    for lag in range(1, min(cap, T // 4)):
        ac = float(np.mean(np.sum(Z[:, :-lag] * Z[:, lag:], 1) / (T - lag)))
        if ac < thresh:
            return max(1, lag)
    return cap


def keff_block(X):
    """k_eff readouts for one neurons x frames block.

    Two families:
      * FULL-T (autocorrelation-aware): raw covariance PR (framework's
        1/Tr(rho^2)) and eff_rank vs a phase-randomized floor.
      * DECIMATED (autocorrelation-removed, the FAIR cross-stimulus metric):
        temporally decorrelate to ~independent frames, then eff_rank vs the
        analytic Marchenko-Pastur white-noise edge.
    """
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
    X = X[good]
    N, T = X.shape
    if N < MIN_ROIS:
        return None
    ev, _, _ = corr_eig(X)                       # correlation eigenvalues desc
    C_cov = np.cov(X)
    wcov = np.clip(np.linalg.eigvalsh(C_cov), 0, None)
    k_eff_cov = float(wcov.sum() ** 2 / np.sum(wcov * wcov))
    # phase-randomized surrogate floor (mean top-eig over reps) -- autocorr-aware
    tops = [float(corr_eig(phase_randomize(X))[0].max()) for _ in range(N_SURR)]
    floor = float(np.mean(tops))
    eff_rank_surr = int((ev > floor).sum())
    sig = np.clip(ev - floor, 0, None)
    keff_signal = float(sig.sum() ** 2 / np.sum(sig * sig)) if sig.sum() > 0 else 0.0
    # temporally-decorrelated (fair) family
    stride = autocorr_stride(X)
    Xd = X[:, ::stride]
    Nd, Td = Xd.shape
    evd, _, _ = corr_eig(Xd)
    edge_d = mp_edge(Nd, Td)
    eff_rank_dec = int((evd > edge_d).sum())
    Cd = np.cov(Xd)
    wd = np.clip(np.linalg.eigvalsh(Cd), 0, None)
    k_eff_cov_dec = float(wd.sum() ** 2 / np.sum(wd * wd))
    return dict(N=int(N), T=int(T), k_eff_cov=k_eff_cov,
                eff_rank_surr=eff_rank_surr, surr_floor=floor,
                keff_signal=keff_signal, autocorr_stride=int(stride),
                T_dec=int(Td), eff_rank_dec=eff_rank_dec,
                mp_edge_dec=float(edge_d), k_eff_cov_dec=k_eff_cov_dec,
                top_eigs=[float(x) for x in ev[:8]])


def process_session(sid):
    import h5py
    path = download_nwb(sid)
    with h5py.File(path, "r") as f:
        stype = f["general/session_type"][()]
        stype = stype.decode() if isinstance(stype, bytes) else str(stype)
        ntot = f[DFF].shape[1]
        present = [k[:-len("_stimulus")]
                   for k in f["stimulus/presentation"].keys()
                   if k.endswith("_stimulus")]
        present = [s for s in present if s in STIM_RANK]
        # matched T = min block length across this session's usable stimuli
        frames = {s: stim_frames(f, s, ntot) for s in present}
        frames = {s: idx for s, idx in frames.items() if len(idx) >= MIN_ROIS}
        if len(frames) < 2:
            return dict(id=sid, session_type=stype, excluded="too_few_blocks")
        Tm = min(T_CAP, min(len(idx) for idx in frames.values()))
        blocks = {}
        for s, idx in frames.items():
            sel = match_T(idx, Tm)
            X = f[DFF][:, sel].astype(np.float64)
            m = keff_block(X)
            if m is not None:
                m["rank"] = STIM_RANK[s]
                blocks[s] = m
    if len(blocks) < 2:
        return dict(id=sid, session_type=stype, excluded="too_few_valid_blocks")
    ranks = [blocks[s]["rank"] for s in blocks]
    def wsp(key):
        vals = [blocks[s][key] for s in blocks]
        return (float(spearmanr(ranks, vals).correlation)
                if len(set(ranks)) > 1 else float("nan"))
    return dict(id=sid, session_type=stype, T_matched=int(Tm),
                N=blocks[next(iter(blocks))]["N"], blocks=blocks,
                within_spearman_dec=wsp("eff_rank_dec"),   # FAIR primary
                within_spearman_surr=wsp("eff_rank_surr"),
                within_spearman_cov=wsp("k_eff_cov"))


def main():
    orig = json.load(open(ORIG))
    sessions = [(r["id"], r["area"]) for r in orig
                if "dff" in r and isinstance(r["dff"], dict)]
    print(f"mechanism (content-vs-tautology) test on {len(sessions)} Allen sessions\n")

    results = []
    done = set()
    if os.path.exists(OUT):
        try:
            prev = json.load(open(OUT))
            results = prev.get("sessions", [])
            done = {r["id"] for r in results}
            print(f"resuming -- {len(done)} sessions already done\n")
        except Exception:
            results = []

    for sid, area in sessions:
        if sid in done:
            continue
        try:
            rec = process_session(sid)
            rec["area"] = area
            if "blocks" in rec:
                order = sorted(rec["blocks"], key=lambda s: rec["blocks"][s]["rank"])
                desc = "  ".join(
                    f"{s}(r{rec['blocks'][s]['rank']}):"
                    f"dec={rec['blocks'][s]['eff_rank_dec']},"
                    f"cov={rec['blocks'][s]['k_eff_cov']:.1f}"
                    for s in order)
                print(f"{sid} {area:6s} {rec['session_type']:16s} N={rec['N']} "
                      f"T={rec['T_matched']}  rho_dec={rec['within_spearman_dec']:+.2f} "
                      f"rho_cov={rec['within_spearman_cov']:+.2f}")
                print(f"    {desc}")
            else:
                print(f"{sid} {area:6s} EXCLUDED: {rec.get('excluded')}")
        except Exception as ex:
            rec = dict(id=sid, area=area,
                       failed=f"{type(ex).__name__}: {str(ex)[:140]}")
            print(f"{sid} {area:6s} FAILED: {rec['failed']}")
        results.append(rec)
        with open(OUT, "w") as fp:
            json.dump(dict(substrate="Allen Brain Observatory mouse visual "
                           "cortex 2p dF/F -- within-recording k_eff vs "
                           "stimulus-driver dimensionality", sessions=results),
                      fp, indent=1)
            fp.flush()
            os.fsync(fp.fileno())
        try:
            os.remove(os.path.join(NWB_DIR, f"{sid}.nwb"))
        except OSError:
            pass

    analyse(results)


def analyse(results):
    ok = [r for r in results if "blocks" in r]
    if not ok:
        print("\nno valid sessions -- BLOCKED")
        return
    rank_of = STIM_RANK
    # metrics: eff_rank_dec = FAIR debiased effective rank (autocorr-removed);
    #          eff_rank_surr = autocorr-aware debiased rank (reference);
    #          k_eff_cov = framework's raw covariance PR (variance-weighted).
    METRICS = ["eff_rank_dec", "eff_rank_surr", "k_eff_cov", "k_eff_cov_dec"]
    per_stim = {}
    for r in ok:
        for s, m in r["blocks"].items():
            d = per_stim.setdefault(s, {k: [] for k in METRICS})
            for k in METRICS:
                d[k].append(m[k])

    # stimulus-type ordinal Spearman: mean metric per stimulus type vs its rank
    types = sorted(per_stim, key=lambda s: (rank_of[s], s))
    ranks_t = [rank_of[s] for s in types]
    ord_sp = {}
    for k in METRICS:
        means = [float(np.mean(per_stim[s][k])) for s in types]
        sp = spearmanr(ranks_t, means)
        ord_sp[k] = [float(sp.correlation), float(sp.pvalue)]

    # within-session Spearman (each recording is its own control)
    ws = {"eff_rank_dec": "within_spearman_dec",
          "eff_rank_surr": "within_spearman_surr",
          "k_eff_cov": "within_spearman_cov"}
    ws_arr = {k: np.array([r[v] for r in ok if np.isfinite(r[v])])
              for k, v in ws.items()}

    # PAIRED grain-cancelling contrasts (same neurons, matched T), on the FAIR
    # metric: natural (rank 3) / scenes (2) / gratings (1) / spontaneous (0).
    def paired(rk_hi, rk_lo, key):
        hi, lo = [], []
        for r in ok:
            H = [m[key] for m in r["blocks"].values() if m["rank"] == rk_hi]
            L = [m[key] for m in r["blocks"].values() if m["rank"] == rk_lo]
            if H and L:
                hi.append(np.mean(H)); lo.append(np.mean(L))
        return np.array(hi), np.array(lo)
    contrasts = {}
    for label, (rh, rl) in {"natural_vs_gratings": (3, 1),
                            "natural_vs_spont": (3, 0),
                            "gratings_vs_spont": (1, 0),
                            "scenes_vs_gratings": (2, 1)}.items():
        hi, lo = paired(rh, rl, "eff_rank_dec")
        if len(hi) >= 3:
            dlt = hi - lo
            try:
                p = float(wilcoxon(hi, lo).pvalue)
            except Exception:
                p = float("nan")
            contrasts[label] = dict(n=len(hi), mean_hi=float(hi.mean()),
                                    mean_lo=float(lo.mean()),
                                    mean_delta=float(dlt.mean()),
                                    frac_positive=float((dlt > 0).mean()),
                                    wilcoxon_p=p)

    print("\n" + "=" * 74)
    print(f"{len(ok)} usable sessions.")
    print("\nPooled k_eff by stimulus type (mean +/- sd over sessions):")
    for s in types:
        d = per_stim[s]
        print(f"  r{rank_of[s]} {s:20s} n={len(d['eff_rank_dec']):2d}  "
              f"eff_rank_dec={np.mean(d['eff_rank_dec']):5.1f}+/-{np.std(d['eff_rank_dec']):4.1f}"
              f"  eff_rank_surr={np.mean(d['eff_rank_surr']):5.1f}"
              f"  k_eff_cov={np.mean(d['k_eff_cov']):5.1f}")
    print("\nStimulus-type ordinal Spearman (stim rank vs mean metric):")
    for k in METRICS:
        print(f"  {k:16s}: rho={ord_sp[k][0]:+.3f} p={ord_sp[k][1]:.3g}")
    print("\nWithin-session Spearman (each recording its own control):")
    for k, a in ws_arr.items():
        print(f"  {k:16s}: mean {a.mean():+.3f} +/- {a.std():.3f} "
              f"(n={len(a)}); frac>0 = {(a>0).mean():.2f}")
    print("\nPaired grain-cancelling contrasts (FAIR eff_rank_dec, same neurons):")
    for lab, c in contrasts.items():
        print(f"  {lab:22s} n={c['n']:2d}  hi={c['mean_hi']:5.1f} lo={c['mean_lo']:5.1f}"
              f"  delta={c['mean_delta']:+5.1f}  frac+={c['frac_positive']:.2f}"
              f"  wilcoxon_p={c['wilcoxon_p']:.3g}")

    # VERDICT on the FAIR metric (eff_rank_dec), cross-checked against raw PR.
    lead = ord_sp["eff_rank_dec"][0]
    ws_mean = ws_arr["eff_rank_dec"].mean()
    ns = contrasts.get("natural_vs_spont", {})
    cov_lead = ord_sp["k_eff_cov"][0]
    monotonic = lead > 0.5 and ws_mean > 0.25 and ns.get("frac_positive", 0) >= 0.65
    flat = abs(lead) < 0.4 and abs(ws_mean) < 0.25
    if monotonic:
        verdict = "CONTENT"
        note = ("debiased effective rank increases with shared-driver "
                "dimensionality; k_eff TRACKS the driver -> mechanistic law")
    elif flat:
        verdict = "NEAR-TAUTOLOGICAL"
        note = ("debiased effective rank is ~invariant to shared-driver "
                "dimensionality; saturation is intrinsic, not driver-set. "
                f"(Note: raw variance-weighted k_eff_cov ordinal rho={cov_lead:+.2f} "
                "-- any driver-tracking lives in variance concentration, not "
                "in the count of shared dimensions.)")
    else:
        verdict = "MIXED"
        note = (f"debiased rank ordinal rho={lead:+.2f}, raw k_eff_cov rho="
                f"{cov_lead:+.2f}: partial / metric-dependent driver-tracking")
    print(f"\nVERDICT: {verdict}\n{note}")

    summary = dict(n_sessions=len(ok),
                   per_stimulus={s: dict(rank=rank_of[s], n=len(per_stim[s]["eff_rank_dec"]),
                       **{f"{k}_mean": float(np.mean(per_stim[s][k])) for k in METRICS},
                       **{f"{k}_sd": float(np.std(per_stim[s][k])) for k in METRICS})
                       for s in types},
                   ordinal_spearman=ord_sp,
                   within_session_spearman={k: dict(mean=float(a.mean()),
                       sd=float(a.std()), fracpos=float((a > 0).mean()), n=len(a))
                       for k, a in ws_arr.items()},
                   contrasts=contrasts, verdict=verdict, verdict_note=note)
    payload = json.load(open(OUT))
    payload["summary"] = summary
    with open(OUT, "w") as fp:
        json.dump(payload, fp, indent=1)
    write_summary(summary)
    print(f"\nwrote {OUT} and {SUMMARY}")


def write_summary(s):
    ps = s["per_stimulus"]
    order = sorted(ps, key=lambda k: (ps[k]["rank"], k))
    osp = s["ordinal_spearman"]
    wss = s["within_session_spearman"]
    lines = [
        "# Allen Brain Observatory -- MECHANISM test: does k_eff track the shared driver?",
        "",
        "Question (tautology-vs-content crux): is neural effective dimensionality "
        "`k_eff` DRIVEN BY the dimensionality of the shared stimulus (a mechanistic "
        "LAW -> content), or INTRINSIC / invariant to it (near-tautological)?",
        "",
        "**Design.** Within-recording: same neurons, same N, matched (contiguous) T, "
        "different stimulus blocks. The absolute k_eff of a cortex patch is "
        "grain-confounded, but the RELATIVE change across stimulus types on the SAME "
        "neurons is not -- the grain/subsample confound cancels. Driver dimensionality "
        "is the WELL-ESTABLISHED stimulus-type ORDERING (not a fragile estimate): "
        "spontaneous (0) < gratings (1) < natural scenes (2) < natural movies (3).",
        "",
        f"**Substrate.** Allen Brain Observatory 2-photon dF/F, mouse visual cortex "
        f"(VISp/VISl/VISpm/VISal). {s['n_sessions']} usable sessions (session-types "
        f"A/B/C).",
        "",
        "**Debiasing.** Raw PR of 2p dF/F is noise-inflated. Two debiased readouts: "
        "`eff_rank_dec` (PRIMARY, FAIR) = # correlation eigenvalues above the analytic "
        "Marchenko-Pastur white-noise edge AFTER temporally decorrelating each block "
        "to ~independent frames -- this removes the autocorrelation asymmetry (natural "
        "movies are far smoother than gratings, which otherwise inflates their noise "
        "floor and artefactually suppresses their rank). `eff_rank_surr` = # eigenvalues "
        "above a phase-randomized floor (autocorrelation-AWARE, reference). `k_eff_cov` "
        "= framework's raw covariance participation ratio (variance-weighted).",
        "",
        "## Pooled k_eff by stimulus type",
        "",
        "| rank | stimulus | n | eff_rank_dec (FAIR) | eff_rank_surr | k_eff_cov (raw PR) |",
        "|------|----------|---|---------------------|---------------|--------------------|",
    ]
    for k in order:
        d = ps[k]
        lines.append(f"| {d['rank']} | {k} | {d['n']} | "
                     f"{d['eff_rank_dec_mean']:.1f} +/- {d['eff_rank_dec_sd']:.1f} | "
                     f"{d['eff_rank_surr_mean']:.1f} | {d['k_eff_cov_mean']:.1f} |")
    lines += [
        "",
        "## The test",
        "",
        f"- **Stimulus-type ordinal Spearman** (stim-dim rank vs mean metric):",
        f"    - eff_rank_dec (FAIR): rho = **{osp['eff_rank_dec'][0]:+.3f}** "
        f"(p={osp['eff_rank_dec'][1]:.3g})",
        f"    - eff_rank_surr        : rho = {osp['eff_rank_surr'][0]:+.3f}",
        f"    - k_eff_cov (raw PR)   : rho = {osp['k_eff_cov'][0]:+.3f}",
        f"- **Within-session Spearman** (each recording its own control):",
        f"    - eff_rank_dec (FAIR): mean **{wss['eff_rank_dec']['mean']:+.3f}** "
        f"+/- {wss['eff_rank_dec']['sd']:.3f} (n={wss['eff_rank_dec']['n']}); "
        f"frac>0 = {wss['eff_rank_dec']['fracpos']:.2f}",
        f"    - k_eff_cov          : mean {wss['k_eff_cov']['mean']:+.3f} "
        f"+/- {wss['k_eff_cov']['sd']:.3f}; frac>0 = {wss['k_eff_cov']['fracpos']:.2f}",
        "",
        "### Paired grain-cancelling contrasts (FAIR eff_rank_dec, same neurons)",
        "",
        "| contrast | n | hi | lo | delta | frac +Delta | Wilcoxon p |",
        "|----------|---|----|----|-------|-------------|------------|",
    ]
    for lab, c in s["contrasts"].items():
        lines.append(f"| {lab} | {c['n']} | {c['mean_hi']:.1f} | {c['mean_lo']:.1f} | "
                     f"{c['mean_delta']:+.1f} | {c['frac_positive']:.2f} | {c['wilcoxon_p']:.3g} |")
    lines += ["", f"## VERDICT: {s['verdict']}", "", s["verdict_note"] + "."]
    with open(SUMMARY, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

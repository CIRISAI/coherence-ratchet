#!/usr/bin/env python3
"""
Criticality-vs-low-rank SPECTRAL discriminator on the Allen Brain Observatory
mouse visual-cortex data -- the "owed test" flagged in StructuralClaims.lean.

The mean-pairwise-rho run (data_allen/) placed Allen at the CHAOS pole
(median debiased rho ~ 0.023). But the framework's canonical observable is
k_eff-of-covariance / effective rank, and cortex is the textbook case where the
two diverge: small pairwise correlation, strong low-rank population structure.
This settles whether Allen is LOW-RANK (novel), CRITICAL, or genuinely NOISE.

Analysis core is REUSED VERBATIM from spectral_test.py (the C. elegans run):
  corr_eig, participation_ratio, mp_edge, phase_randomize, subsample_pr, and
  the synthetic calibrators. Only the data loader differs (Allen NWB, not the
  Kato parquet). No fabricated data in the verdict; synthetics ONLY calibrate
  the estimator.

Data: two-photon dF/F on the spontaneous (grey-screen) epoch, the SAME 25
sessions / SAME epoch as data_allen/results.json. NWB files fetched directly
from the Allen Brain Observatory API (no credentials), extracted, then deleted
to save disk. Incremental flush to spectral_results_allen.json so a restart
recovers finished sessions.
"""
import json
import os
import subprocess

import numpy as np

# ---- reuse the EXACT analysis core from the C. elegans spectral test --------
from spectral_test import (corr_eig, participation_ratio, mp_edge,
                           phase_randomize, subsample_pr,
                           synth_lowrank, synth_powerlaw, synth_noise)

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(HERE, "..", "structural_series", "data_allen", "results.json")
OUT = os.path.join(HERE, "spectral_results_allen.json")
SUMMARY = os.path.join(HERE, "spectral_allen_summary.md")
NWB_DIR = "/tmp/allen_nwb_spectral"
API = "https://api.brain-map.org"
RNG = np.random.default_rng(0)
MIN_ROIS = 20   # spectral test needs enough units for a subsampling curve

os.makedirs(NWB_DIR, exist_ok=True)


# ---- Allen NWB loader (from allen_keff_retest/keff_retest.py) ---------------
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


def load_spont_dff(path):
    """neurons x frames dF/F on the spontaneous epoch."""
    import h5py
    with h5py.File(path, "r") as f:
        dff = f["processing/brain_observatory_pipeline/DfOverF/"
                "imaging_plane_1/data"][:]
        fd = f["stimulus/presentation/spontaneous_stimulus/frame_duration"][:]
    s0, s1 = int(fd[0, 0]), int(fd[1, 0])
    return np.asarray(dff[:, s0:s1], dtype=np.float64)


# ---- subsampling-exponent helper (same fit rule as spectral_test.main) ------
SIZE_GRID = [10, 15, 20, 30, 40, 60, 80, 100, 120, 150, 180, 200, 240]


def beta_from_curve(X, N):
    sizes = [s for s in SIZE_GRID if s <= N]
    curve = subsample_pr(X, sizes)
    cn = np.array([c[0] for c in curve], float)
    cp = np.array([c[1] for c in curve], float)
    upper = cn >= max(20, cn.max() // 3)
    beta = (np.polyfit(np.log10(cn[upper]), np.log10(cp[upper]), 1)[0]
            if upper.sum() >= 3 else float("nan"))
    return float(beta), curve


def session_spectral(X):
    """All spectral readouts for one neurons x frames matrix."""
    # drop constant/NaN units
    good = np.isfinite(X).all(1) & (X.std(1) > 1e-9)
    X = X[good]
    if X.shape[0] < MIN_ROIS:
        return None
    ev, N, T = corr_eig(X)                       # correlation-matrix eigenvalues
    pr_corr = participation_ratio(ev)            # PR of correlation spectrum
    # PR of the COVARIANCE spectrum == the "owed" canonical k_eff
    C_cov = np.cov(X)
    wcov = np.clip(np.linalg.eigvalsh(C_cov), 0, None)
    k_eff_cov = float(wcov.sum() ** 2 / np.sum(wcov * wcov))
    edge = mp_edge(N, T)                          # Marchenko-Pastur upper edge
    eff_rank_mp = int((ev > edge).sum())
    # phase-randomized surrogate noise floor
    Xs = phase_randomize(X)
    evs, *_ = corr_eig(Xs)
    surr_top = float(evs.max())
    surr_rank_mp = int((evs > edge).sum())
    eff_rank_surr = int((ev > surr_top).sum())
    beta, curve = beta_from_curve(X, N)
    return dict(N=int(N), T=int(T), PR_corr=float(pr_corr),
                k_eff_cov=k_eff_cov, mp_edge=float(edge),
                eff_rank_mp=eff_rank_mp, eff_rank_surr=eff_rank_surr,
                surr_rank_mp=surr_rank_mp, surr_top_eig=surr_top,
                beta_sub=beta, top_eigs=[float(x) for x in ev[:8]],
                subsample=curve)


def calibrate(N, T):
    """Calibrate the estimator on synthetics AT THE DATA'S (N, T)."""
    print(f"=== CALIBRATION at data scale N={N}, T={T} ===")
    cal = {}
    for name, X in [("low-rank r=3", synth_lowrank(N, T)),
                    ("power-law a=1.0", synth_powerlaw(N, T, 1.0)),
                    ("power-law a=0.6", synth_powerlaw(N, T, 0.6)),
                    ("pure noise", synth_noise(N, T))]:
        m = session_spectral(X)
        cal[name] = dict(PR_corr=m["PR_corr"], eff_rank_surr=m["eff_rank_surr"],
                         eff_rank_mp=m["eff_rank_mp"], beta_sub=m["beta_sub"])
        print(f"  {name:16s}: PR={m['PR_corr']:7.2f}  "
              f"eff_rank_surr={m['eff_rank_surr']:3d}  "
              f"eff_rank_mp={m['eff_rank_mp']:3d}  beta={m['beta_sub']:6.3f}")
    print("  (expect: low-rank beta~0 small rank; power-law beta 0.3-0.8; "
          "noise beta~1 rank~0)\n")
    return cal


def main():
    orig = json.load(open(ORIG))
    sessions = [(r["id"], r["area"]) for r in orig
                if "dff" in r and isinstance(r["dff"], dict)]
    print(f"spectral discriminator on {len(sessions)} Allen sessions\n")

    # calibrate at a representative large N and the median T
    cal = calibrate(200, 9000)

    results = []
    done = set()
    if os.path.exists(OUT):
        try:
            prev = json.load(open(OUT))
            results = prev.get("sessions", prev) if isinstance(prev, dict) else prev
            done = {r["id"] for r in results if "N" in r}
            print(f"resuming -- {len(done)} sessions already done\n")
        except Exception:
            results = []

    print(f"{'id':>10s} {'area':6s} {'N':>4s} {'T':>5s} {'PR':>6s} "
          f"{'kcov':>6s} {'MPrk':>4s} {'srrk':>4s} {'beta':>6s}")
    for i, (sid, area) in enumerate(sessions):
        if sid in done:
            continue
        try:
            path = download_nwb(sid)
            X = load_spont_dff(path)
            m = session_spectral(X)
            if m is None:
                rec = dict(id=sid, area=area, excluded="too_few_units")
            else:
                rec = dict(id=sid, area=area, **m)
                print(f"{sid:>10d} {area:6s} {m['N']:4d} {m['T']:5d} "
                      f"{m['PR_corr']:6.2f} {m['k_eff_cov']:6.2f} "
                      f"{m['eff_rank_mp']:4d} {m['eff_rank_surr']:4d} "
                      f"{m['beta_sub']:6.3f}")
        except Exception as ex:
            rec = dict(id=sid, area=area,
                       failed=f"{type(ex).__name__}: {str(ex)[:120]}")
            print(f"{sid:>10d} {area:6s} FAILED: {rec['failed']}")
        results.append(rec)
        payload = dict(substrate="Allen Brain Observatory mouse visual cortex "
                       "(2p dF/F, spontaneous epoch)",
                       calibration=cal, sessions=results)
        with open(OUT, "w") as f:
            json.dump(payload, f, indent=1)
            f.flush()
            os.fsync(f.fileno())
        try:
            os.remove(os.path.join(NWB_DIR, f"{sid}.nwb"))
        except OSError:
            pass

    analyse(results, cal)


def analyse(results, cal):
    ok = [r for r in results if "N" in r]
    if not ok:
        print("no valid session -- BLOCKED")
        return
    N = np.array([r["N"] for r in ok])
    keff_cov = np.array([r["k_eff_cov"] for r in ok])
    eff_mp = np.array([r["eff_rank_mp"] for r in ok])
    eff_surr = np.array([r["eff_rank_surr"] for r in ok])
    surr_mp = np.array([r["surr_rank_mp"] for r in ok])
    betas = np.array([r["beta_sub"] for r in ok if np.isfinite(r["beta_sub"])])

    n = len(betas)
    bmean, bsd = float(betas.mean()), float(betas.std())
    se = bsd / np.sqrt(n)
    ci = (bmean - 1.96 * se, bmean + 1.96 * se)

    print("\n" + "=" * 70)
    print(f"{len(ok)} sessions. N range [{N.min()}, {N.max()}] "
          f"median {int(np.median(N))}, T~{int(np.median([r['T'] for r in ok]))}")
    print(f"k_eff (PR of covariance)      : median {np.median(keff_cov):.2f}, "
          f"range [{keff_cov.min():.2f}, {keff_cov.max():.2f}]")
    print(f"effective rank vs MP edge     : median {np.median(eff_mp):.1f}, "
          f"range [{eff_mp.min()}, {eff_mp.max()}] "
          f"(surrogate MP rank median {np.median(surr_mp):.1f})")
    print(f"effective rank vs surr floor  : median {np.median(eff_surr):.1f}, "
          f"range [{eff_surr.min()}, {eff_surr.max()}]")
    print(f"beta (PR-subsampling exponent): mean {bmean:.3f} +/- {bsd:.3f}  "
          f"95% CI [{ci[0]:.3f}, {ci[1]:.3f}]  (n={n})")

    # verdict logic (same thresholds as the C. elegans run + rank check)
    lowrank_beta = cal["low-rank r=3"]["beta_sub"]
    if ci[1] < 0.30 and np.median(eff_mp) < 0.5 * np.median(N):
        verdict = "LOW-RANK"
        note = ("few spikes over flat MP bulk; beta CI below 0.30 "
                "(saturation); effective rank small vs N")
    elif ci[0] > 0.20 and ci[1] < 0.90:
        verdict = "CRITICALITY"
        note = "power-law spectrum, beta in the 0.3-0.8 critical band"
    elif ci[0] > 0.80:
        verdict = "NOISE"
        note = "beta ~ 1 (extensive), rank ~ 0"
    else:
        verdict = "INCONCLUSIVE"
        note = "beta CI straddles regime boundaries"
    print(f"\nVERDICT: {verdict}  -- {note}")

    stats = dict(n_sessions=len(ok), N_min=int(N.min()), N_max=int(N.max()),
                 N_median=float(np.median(N)),
                 T_median=float(np.median([r['T'] for r in ok])),
                 k_eff_cov_median=float(np.median(keff_cov)),
                 k_eff_cov_range=[float(keff_cov.min()), float(keff_cov.max())],
                 eff_rank_mp_median=float(np.median(eff_mp)),
                 eff_rank_mp_range=[int(eff_mp.min()), int(eff_mp.max())],
                 eff_rank_surr_median=float(np.median(eff_surr)),
                 surr_rank_mp_median=float(np.median(surr_mp)),
                 beta_mean=bmean, beta_sd=bsd, beta_ci95=list(ci), beta_n=n,
                 verdict=verdict, verdict_note=note)

    payload = dict(substrate="Allen Brain Observatory mouse visual cortex "
                   "(2p dF/F, spontaneous epoch)", calibration=cal,
                   summary=stats, sessions=results)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=1)
    write_summary(stats, cal)
    print(f"\nwrote {OUT} and {SUMMARY}")


def write_summary(s, cal):
    lines = [
        "# Allen Brain Observatory -- spectral criticality-vs-low-rank verdict",
        "",
        f"Substrate: mouse visual cortex (VISp/VISl/VISpm/VISal), 2-photon dF/F, "
        f"spontaneous grey-screen epoch. Real Allen NWB, {s['n_sessions']} "
        f"sessions. N in [{s['N_min']}, {s['N_max']}] (median "
        f"{s['N_median']:.0f}), T ~ {s['T_median']:.0f} frames.",
        "",
        f"- **k_eff (PR of covariance)**: median **{s['k_eff_cov_median']:.1f}** "
        f"(range {s['k_eff_cov_range'][0]:.1f}-{s['k_eff_cov_range'][1]:.1f}) "
        f"-- the specific owed quantity.",
        f"- **Effective rank vs MP edge**: median {s['eff_rank_mp_median']:.0f} "
        f"(surrogate MP rank median {s['surr_rank_mp_median']:.0f}).",
        f"- **Effective rank vs surrogate floor**: median "
        f"{s['eff_rank_surr_median']:.0f} (range {s['eff_rank_mp_range'][0]}-"
        f"{s['eff_rank_mp_range'][1]}).",
        f"- **beta (PR-subsampling exponent)**: mean **{s['beta_mean']:.3f}** "
        f"+/- {s['beta_sd']:.3f}, 95% CI [{s['beta_ci95'][0]:.3f}, "
        f"{s['beta_ci95'][1]:.3f}] (n={s['beta_n']}).",
        f"- Calibration at N=200: low-rank beta={cal['low-rank r=3']['beta_sub']:.3f}, "
        f"power-law(1.0)={cal['power-law a=1.0']['beta_sub']:.3f}, "
        f"power-law(0.6)={cal['power-law a=0.6']['beta_sub']:.3f}, "
        f"noise={cal['pure noise']['beta_sub']:.3f}.",
        "",
        f"## VERDICT: {s['verdict']}",
        "",
        s['verdict_note'] + ".",
    ]
    with open(SUMMARY, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

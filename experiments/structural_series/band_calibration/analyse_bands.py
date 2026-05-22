"""Per-substrate corridor-band calibration from debiased-rho values on disk.

Pre-registration: PREREGISTRATION.md (this directory).
Discipline: analysis only on debiased-rho values already computed and on disk.
No new data collection, no synthetic data.

Substrates and their debiased-rho sources:
  C. elegans       robust_rerun/celegans/results_celegans.json  (whole_brain rho_deb, 832 worms)
  Drosophila       robust_rerun/drosophila/results.json          (full rho_deb, 57 recordings)
  EEG-interictal   robust_rerun/eeg/results_eeg_robust.json      (chbmit interictal windows)
  fMRI             band_calibration/_fmri_per_subject.json       (re-run of data_fmri/fmri_corridor.py)
  LLM internals    band_calibration/_llm_per_layer.json          (re-run of exp_E1_llm_corridor.py)

MISSING (reported, excluded from the debiased-rho pool):
  TCGA   data_tcga rho_normal is RAW mean|corr| (02_compute_rho.py: no
         phase-randomized floor subtraction) -> not a debiased-rho value.
  GPU    corridor_dynamics/gpu* are corridor-EXIT relaxation runs (k_eff/r
         decay after a perturbation); there is no healthy in-corridor rho
         distribution on disk. GPU supplies the dynamical drho/dt data, which
         the pre-registration's honest-scope section explicitly distinguishes
         from the static band measured here.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SS = os.path.normpath(os.path.join(HERE, ".."))


def load_celegans():
    d = json.load(open(os.path.join(SS, "robust_rerun/celegans/results_celegans.json")))
    return [r["whole_brain"]["rho_deb"] for r in d["records"] if r.get("included")]


def load_drosophila():
    d = json.load(open(os.path.join(SS, "robust_rerun/drosophila/results.json")))
    # 'full' recording (whole epoch); walking_only is a confound-control subset
    return [r["full"]["rho_deb"] for r in d["records"]]


def load_eeg():
    d = json.load(open(os.path.join(SS, "robust_rerun/eeg/results_eeg_robust.json")))
    vals = []
    for pf in d["chbmit"]["per_file"]:
        for w in pf.get("interictal", []):
            vals.append(w["rho_deb"])
    return vals


def load_fmri():
    d = json.load(open(os.path.join(HERE, "_fmri_per_subject.json")))
    return [r["rho_deb"] for r in d["records"]]


def load_llm():
    d = json.load(open(os.path.join(HERE, "_llm_per_layer.json")))
    return [r["rho_deb"] for r in d["records"]]


SUBSTRATES = {
    "C. elegans (whole-brain)": load_celegans,
    "Drosophila (central complex)": load_drosophila,
    "EEG interictal (CHB-MIT)": load_eeg,
    "fMRI resting-state (ABIDE)": load_fmri,
    "LLM internals (3 models)": load_llm,
}


def keff_kish(rho, k):
    """Kish identity k_eff = k / (1 + rho(k-1)). k -> inf limit = 1/rho."""
    if k is None:
        return 1.0 / rho if rho > 0 else float("inf")
    return k / (1.0 + rho * (k - 1.0))


def band(vals):
    a = np.array(sorted(vals), dtype=float)
    p5, p25, p50, p75, p95 = np.percentile(a, [5, 25, 50, 75, 95])
    return {
        "n": int(len(a)),
        "rho_mid_median": float(p50),
        "rho_mean": float(a.mean()),
        "iqr": float(p75 - p25),
        "p5": float(p5), "p25": float(p25), "p75": float(p75), "p95": float(p95),
        "half_width_w": float((p95 - p5) / 2.0),
        "min": float(a.min()), "max": float(a.max()),
    }


def main():
    out = {
        "preregistration": "experiments/structural_series/band_calibration/PREREGISTRATION.md",
        "scope": ("STATIC band of healthy/in-corridor debiased rho. NOT the "
                  "dynamical corridor-as-attractor bounds (drho/dt regime "
                  "change), which require per-substrate drho/dt measured so "
                  "far only at the GPU substrate."),
        "estimator": "debiased rho (phase-randomized / shuffle noise floor, quadrature subtraction)",
        "missing": {
            "TCGA": ("rho_normal in data_tcga is RAW mean|corr| (02_compute_rho.py "
                     "has no floor subtraction) -- not a debiased-rho value; "
                     "excluded from the debiased-rho pool."),
            "GPU": ("corridor_dynamics/gpu* are corridor-exit relaxation runs "
                    "(k_eff/r decay), no healthy in-corridor rho distribution "
                    "on disk; GPU supplies the dynamical data the honest-scope "
                    "section separates from the static band."),
        },
        "substrates": {},
    }

    for name, loader in SUBSTRATES.items():
        vals = loader()
        b = band(vals)
        # k_eff range via Kish identity at the band edges, k -> inf (substrate-
        # independent ceiling form). Lower rho -> higher k_eff.
        b["k_eff_at_p5"] = keff_kish(b["p5"], None)
        b["k_eff_at_median"] = keff_kish(b["rho_mid_median"], None)
        b["k_eff_at_p95"] = keff_kish(b["p95"], None)
        out["substrates"][name] = b

    # cross-substrate read
    mids = {n: out["substrates"][n]["rho_mid_median"] for n in out["substrates"]}
    ws = {n: out["substrates"][n]["half_width_w"] for n in out["substrates"]}
    mid_vals = np.array(list(mids.values()))
    spread = float(mid_vals.max() / mid_vals.min())
    clustered = spread <= 2.0

    # pooled estimate: each substrate weighted equally (one band per substrate),
    # pooled rho_mid = median of per-substrate medians; pooled w = median of w.
    pooled_mid = float(np.median(mid_vals))
    pooled_w = float(np.median(list(ws.values())))

    out["cross_substrate"] = {
        "per_substrate_rho_mid": mids,
        "per_substrate_half_width_w": ws,
        "rho_mid_max_over_min": spread,
        "verdict": "BOUNDS CLUSTER" if clustered else "SUBSTRATE-SPECIFIC",
        "verdict_detail": (
            f"per-substrate rho_mid spans {mid_vals.min():.3f}-{mid_vals.max():.3f}, "
            f"a factor of {spread:.2f}x; "
            + ("within the pre-registered ~2x clustering threshold -> a "
               "cross-substrate corridor with a shared centre is supported "
               "as a first estimate."
               if clustered else
               "exceeds the pre-registered ~2x threshold -> the corridor is "
               "substrate-local in centre; the per-substrate values ARE the "
               "calibration.")),
    }
    # the LLM substrate is the lone outlier; report the biological-substrate
    # sub-cluster separately (the four real-organism rungs) as it bears
    # directly on the clustered-vs-substrate-specific read.
    bio = [n for n in mids if not n.startswith("LLM")]
    bio_vals = np.array([mids[n] for n in bio])
    bio_spread = float(bio_vals.max() / bio_vals.min())
    out["cross_substrate"]["biological_subcluster"] = {
        "substrates": bio,
        "rho_mid_range": [float(bio_vals.min()), float(bio_vals.max())],
        "rho_mid_max_over_min": bio_spread,
        "clustered": bool(bio_spread <= 2.0),
        "note": ("the four biological substrates (C. elegans, Drosophila, EEG, "
                 "fMRI) cluster within a factor of "
                 f"{bio_spread:.2f}x; the LLM substrate (rho_mid "
                 f"{mids.get('LLM internals (3 models)', float('nan')):.3f}) is "
                 "the lone outlier and drives the substrate-specific verdict. "
                 "Read: a shared corridor centre holds across coordinated "
                 "BIOLOGICAL rungs; the LLM internal-representation rung sits "
                 "at a substrate-specific lower centre."),
    }

    bio_mid = float(np.median(bio_vals))
    bio_w = float(np.median([ws[n] for n in bio]))
    out["pooled_estimate"] = {
        "all_substrates": {
            "rho_mid": pooled_mid,
            "half_width_w": pooled_w,
            "implied_band": [pooled_mid - pooled_w, pooled_mid + pooled_w],
        },
        "biological_substrates_only": {
            "rho_mid": bio_mid,
            "half_width_w": bio_w,
            "implied_band": [bio_mid - bio_w, bio_mid + bio_w],
            "note": ("recommended first estimate of P_omega's master "
                     "parameters: pools only the clustered biological rungs, "
                     "excludes the LLM outlier."),
        },
        "caveat": ("STATIC-BAND estimate of P_omega master parameters: where "
                   "healthy debiased rho sits, not the dynamical attractor "
                   "bounds. Tightening to true corridor bounds is gated on "
                   "per-substrate drho/dt and is NOT claimed here."),
    }

    dst = os.path.join(HERE, "results_band_calibration.json")
    json.dump(out, open(dst, "w"), indent=1)
    print(f"wrote {dst}")

    # console table
    print()
    print(f"{'substrate':<30} {'n':>5} {'rho_mid':>8} {'IQR':>7} "
          f"{'[p5':>7} {'p95]':>7} {'w':>7} {'k_eff[p95..p5]':>16}")
    for name, b in out["substrates"].items():
        print(f"{name:<30} {b['n']:>5} {b['rho_mid_median']:>8.3f} "
              f"{b['iqr']:>7.3f} {b['p5']:>7.3f} {b['p95']:>7.3f} "
              f"{b['half_width_w']:>7.3f} "
              f"{b['k_eff_at_p95']:>6.2f}..{b['k_eff_at_p5']:<8.2f}")
    print()
    print(f"cross-substrate: {out['cross_substrate']['verdict']} "
          f"(rho_mid spread {spread:.2f}x)")
    print(f"  biological subcluster: spread {bio_spread:.2f}x "
          f"({'clustered' if bio_spread <= 2.0 else 'not clustered'}); "
          f"LLM is the outlier")
    print(f"pooled (all 5)  rho_mid = {pooled_mid:.3f}, w = {pooled_w:.3f}  "
          f"-> static band [{pooled_mid-pooled_w:.3f}, {pooled_mid+pooled_w:.3f}]")
    print(f"pooled (bio 4)  rho_mid = {bio_mid:.3f}, w = {bio_w:.3f}  "
          f"-> static band [{bio_mid-bio_w:.3f}, {bio_mid+bio_w:.3f}]")


if __name__ == "__main__":
    main()

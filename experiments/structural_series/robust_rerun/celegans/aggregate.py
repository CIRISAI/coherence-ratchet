"""
Aggregate the per-(study,worm) records in results_celegans.json into the
verdict summary. Split out from run_celegans_robust.py so the 832-worm
debiased-rho computation (already flushed per-unit) need not be re-run after a
serialization fix. Pure read of the flushed records — no recomputation.
"""
import json
from pathlib import Path

import numpy as np

OUT_DIR = Path(__file__).parent
RESULTS_JSON = OUT_DIR / "results_celegans.json"
CLASSES = ['sensory', 'interneuron', 'motor', 'command']


def pct(a, q):
    return float(np.percentile(a, q))


def main():
    out = json.loads(RESULTS_JSON.read_text())
    records = out["records"]
    incl = [r for r in records if r.get("included")]
    n_units_total = len(records)

    wb_raw = np.array([r["whole_brain"]["rho_raw"] for r in incl])
    wb_floor = np.array([r["whole_brain"]["floor"] for r in incl])
    wb_deb = np.array([r["whole_brain"]["rho_deb"] for r in incl])
    wb_keff = np.array([r["whole_brain"]["k_eff_emp"] for r in incl])

    iqr = pct(wb_deb, 75) - pct(wb_deb, 25)
    c1 = bool(pct(wb_deb, 5) > 0.05)
    c2 = bool((pct(wb_deb, 95) < 0.90) and (np.median(wb_keff) > 1.5))
    c3 = bool((iqr <= 0.30) and (wb_deb.max() < 0.95))
    n_with_class_signal = sum(
        1 for r in incl
        if any(v["rho_deb"] > 0.05 for v in r.get("per_class", {}).values()))
    c4 = bool(n_with_class_signal / len(incl) >= 0.60)

    if c1 and c2 and c3:
        verdict = "PASS"
    elif (not c1) or (not c2):
        verdict = "FAIL"
    else:
        verdict = "PARTIAL"

    summary = {
        "n_included": len(incl), "n_units_total": n_units_total,
        "n_studies": len(set(r["study"] for r in incl)),
        "whole_brain": {
            "rho_raw_median": float(np.median(wb_raw)),
            "rho_raw_range": [float(wb_raw.min()), float(wb_raw.max())],
            "floor_median": float(np.median(wb_floor)),
            "rho_deb_median": float(np.median(wb_deb)),
            "rho_deb_p5": pct(wb_deb, 5), "rho_deb_p25": pct(wb_deb, 25),
            "rho_deb_p75": pct(wb_deb, 75), "rho_deb_p95": pct(wb_deb, 95),
            "rho_deb_range": [float(wb_deb.min()), float(wb_deb.max())],
            "rho_deb_iqr": iqr,
            "k_eff_emp_median": float(np.median(wb_keff)),
            "k_eff_emp_range": [float(wb_keff.min()), float(wb_keff.max())],
        },
        "criteria": {"C1_off_chaos": c1, "C2_off_rigidity": c2,
                     "C3_bounded_band": c3, "C4_per_class_survives": c4,
                     "C4_frac_with_class_signal":
                         n_with_class_signal / len(incl)},
        "verdict": verdict,
    }
    per_class_agg = {}
    for cls in CLASSES:
        raw = [r["per_class"][cls]["rho_raw"] for r in incl
               if cls in r.get("per_class", {})]
        deb = [r["per_class"][cls]["rho_deb"] for r in incl
               if cls in r.get("per_class", {})]
        flo = [r["per_class"][cls]["floor"] for r in incl
               if cls in r.get("per_class", {})]
        ke = [r["per_class"][cls]["k_eff_emp"] for r in incl
              if cls in r.get("per_class", {})]
        if raw:
            per_class_agg[cls] = {
                "n_worms": len(raw),
                "rho_raw_median": float(np.median(raw)),
                "rho_raw_range": [float(min(raw)), float(max(raw))],
                "floor_median": float(np.median(flo)),
                "rho_deb_median": float(np.median(deb)),
                "rho_deb_p5": pct(deb, 5), "rho_deb_p95": pct(deb, 95),
                "rho_deb_range": [float(min(deb)), float(max(deb))],
                "k_eff_emp_median": float(np.median(ke)),
                "frac_off_chaos": float(np.mean(np.array(deb) > 0.05)),
            }
    summary["per_class"] = per_class_agg

    per_study = {}
    for st in sorted(set(r["study"] for r in incl)):
        d = [r["whole_brain"]["rho_deb"] for r in incl if r["study"] == st]
        rw = [r["whole_brain"]["rho_raw"] for r in incl if r["study"] == st]
        fl = [r["whole_brain"]["floor"] for r in incl if r["study"] == st]
        per_study[st] = {"n_worms": len(d),
                         "rho_raw_median": float(np.median(rw)),
                         "floor_median": float(np.median(fl)),
                         "rho_deb_median": float(np.median(d)),
                         "rho_deb_range": [float(min(d)), float(max(d))]}
    summary["per_study"] = per_study
    out["summary"] = summary
    RESULTS_JSON.write_text(json.dumps(out, indent=2))

    print("=" * 70)
    print(f"VERDICT: {verdict}")
    print("=" * 70)
    print(f"  included worms: {len(incl)} / {n_units_total} "
          f"({summary['n_studies']} studies)")
    print(f"  whole-brain rho_raw   median {np.median(wb_raw):.3f}  "
          f"[{wb_raw.min():.3f}, {wb_raw.max():.3f}]")
    print(f"  whole-brain floor     median {np.median(wb_floor):.3f}")
    print(f"  whole-brain rho_DEB   median {np.median(wb_deb):.3f}  "
          f"[{wb_deb.min():.3f}, {wb_deb.max():.3f}]  IQR {iqr:.3f}")
    print(f"    p5={pct(wb_deb,5):.3f} p25={pct(wb_deb,25):.3f} "
          f"p75={pct(wb_deb,75):.3f} p95={pct(wb_deb,95):.3f}")
    print(f"  whole-brain k_eff_emp median {np.median(wb_keff):.1f}  "
          f"[{wb_keff.min():.1f}, {wb_keff.max():.1f}]")
    print(f"  C1 off chaos {c1}  C2 off rigidity {c2}  "
          f"C3 bounded {c3}  C4 per-class {c4} "
          f"({n_with_class_signal}/{len(incl)})")
    print("\n  per-class  raw -> floor -> debiased  (median):")
    for cls, v in per_class_agg.items():
        print(f"    {cls:<12} raw {v['rho_raw_median']:.3f}  "
              f"floor {v['floor_median']:.3f}  -> deb {v['rho_deb_median']:.3f}"
              f"  [{v['rho_deb_range'][0]:.3f}, {v['rho_deb_range'][1]:.3f}]"
              f"  n={v['n_worms']}  off-chaos {v['frac_off_chaos']*100:.0f}%")
    print("\n  per-study whole-brain  raw -> debiased  (median):")
    for st, v in per_study.items():
        print(f"    {st:<20} raw {v['rho_raw_median']:.3f}  "
              f"floor {v['floor_median']:.3f}  -> deb {v['rho_deb_median']:.3f}"
              f"  n={v['n_worms']}")
    print(f"\n  results: {RESULTS_JSON}")


if __name__ == "__main__":
    main()

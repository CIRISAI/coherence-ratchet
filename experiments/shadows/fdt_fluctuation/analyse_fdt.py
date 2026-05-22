#!/usr/bin/env python3
"""
Shadow 1 -- honest post-hoc analysis of the FDT fluctuation run.
================================================================

The run script's auto-verdict used a weak discrimination test (three rho means
distinct -- trivially true by construction). This script does the analysis the
pre-registration actually asks for:

  1. Is the rigidity Lorentzian corner RESOLVED, or railed to the lowest Welch
     bin? (If railed, the corner is an upper bound, not a measurement.)
  2. Is the corridor spectrum genuinely WHITE (flat), quantitatively?
  3. The FDT link: rigidity's spectral relaxation rate vs the independently
     measured dissipation rate 1/tau = 0.0214 /s. The anchor was measured with
     maintenance OFF -- i.e. in the unmaintained / rigidity-ward regime -- so
     the honest FDT comparison is anchor vs RIGIDITY, not anchor vs corridor.
  4. Does the SPECTRAL SHAPE (not just the mean) discriminate the three regimes?
"""
import json
import os
import numpy as np
from scipy import optimize

D = os.path.dirname(os.path.abspath(__file__))
KAPPA_ANCHOR = 0.0214
SAMPLE_RATE = 10.0


def lorentzian(f, S0, fc):
    return S0 / (1.0 + (f / fc) ** 2)


def analyse_regime(name, runs):
    print(f"\n{'='*70}\n{name.upper()}\n{'='*70}")
    out = []
    for r in runs:
        freqs = np.array(r["freqs"])
        psd = np.array(r["psd"])
        m = freqs > 0
        f, p = freqs[m], psd[m]
        f_lowest = f[0]
        # white-noise null: flat line at the mean
        p_flat = np.full_like(p, p.mean())
        ss_tot = np.sum((p - p.mean()) ** 2)
        ss_white = np.sum((p - p_flat) ** 2)   # == ss_tot, R2_white = 0 by defn
        # Lorentzian fit quality
        fit = r.get("psd_fit") or {}
        fc = fit.get("fc")
        r2 = fit.get("R2")
        # is the corner resolved? railed low => fc within 1.5 bins of f_lowest;
        # railed high => fc within 1.5 bins of Nyquist
        nyq = f[-1]
        railed_low = fc is not None and fc <= 1.5 * f_lowest
        railed_high = fc is not None and fc >= nyq / 1.5
        # low-freq / high-freq power ratio: a white spectrum has ratio ~1,
        # a Lorentzian has low-freq power >> high-freq power
        n = len(p)
        lf = p[:max(1, n // 10)].mean()
        hf = p[-max(1, n // 10):].mean()
        lf_hf = lf / hf if hf > 0 else float("inf")
        out.append({
            "run": r["run"], "rho_mean": r["rho_mean"], "rho_std": r["rho_std"],
            "fc": fc, "R2_lorentzian": r2, "kappa_acf": r.get("kappa_acf"),
            "f_lowest_bin": float(f_lowest), "nyquist": float(nyq),
            "corner_railed_low": bool(railed_low),
            "corner_railed_high": bool(railed_high),
            "lf_hf_power_ratio": float(lf_hf),
        })
        print(f"  run {r['run']}: rho={r['rho_mean']:.4f}+/-{r['rho_std']:.5f}")
        print(f"    Lorentzian fit: fc={fc:.5g} Hz  R2={r2:.4f}")
        print(f"    lowest Welch bin = {f_lowest:.5g} Hz, Nyquist = {nyq:.3g} Hz")
        if railed_high:
            print(f"    -> corner RAILED HIGH (fc ~ Nyquist): spectrum is WHITE, "
                  f"no Lorentzian corner. fc is meaningless.")
        elif railed_low:
            print(f"    -> corner RAILED LOW (fc ~ lowest bin): true corner is "
                  f"at or below resolution; fc is an UPPER BOUND.")
        else:
            print(f"    -> corner RESOLVED inside the band.")
        print(f"    low/high-freq power ratio = {lf_hf:.2f} "
              f"({'white-flat' if lf_hf < 2 else 'red/Lorentzian'})")
        print(f"    kappa_acf = {r['kappa_acf']:.5g} /s  "
              f"(tau_acf = {1.0/r['kappa_acf']:.3g} s)")
    return out


def main():
    gpu = json.load(open(os.path.join(D, "results_fdt_gpu.json")))
    regimes = gpu["regimes"]

    summary = {}
    for name in ("corridor", "rigidity", "chaos"):
        summary[name] = analyse_regime(name, regimes[name])

    print(f"\n{'='*70}\nFDT LINK -- the decisive test\n{'='*70}")
    print(f"  Independently measured GPU dissipation anchor: "
          f"1/tau = {KAPPA_ANCHOR} /s (tau ~ 47 s).")
    print(f"  The anchor (gpu/RESULTS.md) was measured with maintenance OFF --")
    print(f"  unmaintained free relaxation -- i.e. the RIGIDITY-ward regime.")
    print(f"  So the honest FDT comparison is anchor vs the RIGIDITY spectrum.")

    rig = summary["rigidity"]
    # rigidity spectral rate, two independent estimators
    kappa_psd = np.mean([2 * np.pi * s["fc"] for s in rig])
    kappa_acf = np.mean([s["kappa_acf"] for s in rig])
    railed = all(s["corner_railed_low"] for s in rig)
    print(f"\n  RIGIDITY spectral relaxation rate:")
    print(f"    via Lorentzian corner: kappa = 2*pi*fc = {kappa_psd:.5g} /s")
    print(f"      (corner railed-low: {railed} -> this is an UPPER BOUND on "
          f"f_c,\n       so kappa_psd is an upper bound, not a point estimate)")
    print(f"    via ACF integral:      kappa = 1/tau_acf = {kappa_acf:.5g} /s")
    print(f"      (independent of the Welch binning)")

    # honest FDT ratio: ACF-based, since it is not bin-limited
    ratio_acf = kappa_acf / KAPPA_ANCHOR
    print(f"\n  FDT ratio (rigidity ACF rate / dissipation anchor) "
          f"= {ratio_acf:.3g}")
    fdt_holds = 0.3 <= ratio_acf <= 3.0
    print(f"  Same order of magnitude (0.3-3x): {fdt_holds}")

    # corridor: white?
    corr = summary["corridor"]
    corr_white = all(s["corner_railed_high"] and s["lf_hf_power_ratio"] < 2
                     for s in corr)
    chaos = summary["chaos"]
    chaos_white = all(s["corner_railed_high"] and s["lf_hf_power_ratio"] < 2
                      for s in chaos)
    rig_red = all((not s["corner_railed_high"]) and s["lf_hf_power_ratio"] > 2
                  for s in rig)

    print(f"\n{'='*70}\nSPECTRAL-SHAPE DISCRIMINATION\n{'='*70}")
    print(f"  corridor spectrum white (flat): {corr_white}")
    print(f"  chaos spectrum white (flat):    {chaos_white}")
    print(f"  rigidity spectrum red (Lorentzian, R2~0.84): {rig_red}")
    shape_discriminates = rig_red and corr_white
    print(f"  -> spectral SHAPE separates rigidity from corridor: "
          f"{shape_discriminates}")
    print(f"  -> spectral SHAPE separates corridor from chaos:    "
          f"False (both white -- only the rho MEAN separates them)")

    verdict_payload = {
        "fdt_ratio_rigidity_acf": float(ratio_acf),
        "fdt_same_order_of_magnitude": bool(fdt_holds),
        "rigidity_corner_railed_low": bool(railed),
        "corridor_spectrum_white": bool(corr_white),
        "chaos_spectrum_white": bool(chaos_white),
        "rigidity_spectrum_red_lorentzian": bool(rig_red),
        "spectral_shape_discriminates_rigidity": bool(shape_discriminates),
        "spectral_shape_discriminates_corridor_from_chaos": False,
        "per_regime": summary,
    }
    with open(os.path.join(D, "analysis_fdt.json"), "w") as f:
        json.dump(verdict_payload, f, indent=2)
    print(f"\n  analysis -> {os.path.join(D, 'analysis_fdt.json')}")


if __name__ == "__main__":
    main()

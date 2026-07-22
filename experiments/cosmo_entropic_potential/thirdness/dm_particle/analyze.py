#!/usr/bin/env python3
"""
PREDICTION 4 — stage 3: read the ladder against the frozen pass/fail in DECISIONS.md.

  (a) SHOT ARTIFACT: A(nbar) declines monotonically; |G| < 3 vs the primary shot null N1 at
      the two highest densities; fitted A_inf within 3 sigma of 0 (or of the null asymptote).
  (b) PHYSICAL THIRD: |A(nmax) - A(nmax/10)| < 0.25*|A(nmax)|; |G| > 5 at the two highest
      densities against BOTH shot nulls, same sign; G not declining over the top decade;
      A_inf nonzero at > 5 sigma.
  (c) otherwise AMBIGUOUS.
"""
import json, os, sys
from pathlib import Path
import numpy as np
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent


def load(path):
    return json.loads(Path(path).read_text())


def ladder(res, kind="cic", ng=64):
    """Replicate-averaged signed copula skew per density, with replicate scatter."""
    R8 = f"{res['meta']['R_used'][1]:g}"
    by = {}
    for r in res["rows"]:
        if r["kind"] != kind or r["ng"] != ng:
            continue
        by.setdefault(r["frac"], []).append(r)
    out = []
    for f in sorted(by):
        rows = by[f]
        vals = np.array([x["real"][R8] for x in rows])
        r0 = [x for x in rows if x["rep"] == 0][0]
        out.append(dict(
            frac=f, nbar=float(np.mean([x["nbar"] for x in rows])),
            A=float(vals.mean()),
            A_sd=float(vals.std(ddof=1)) if len(vals) > 1 else float("nan"),
            nrep=len(vals),
            sigma_delta=r0["sigma_delta"], frac_empty=r0["frac_empty"],
            nulls={k: dict(mean=r0["nulls"][k]["mean"][R8], std=r0["nulls"][k]["std"][R8],
                           n=r0["nulls"][k]["n"]) for k in r0["nulls"]},
            G={k: r0["G"][k][R8] for k in r0["G"]}))
    return out, R8


def fit_asymptote(lad):
    n = np.array([r["nbar"] for r in lad])
    A = np.array([r["A"] for r in lad])
    sd = np.array([r["A_sd"] if np.isfinite(r["A_sd"]) and r["A_sd"] > 0
                   else np.nanmax([r["A_sd"] for r in lad]) for r in lad])
    sd = np.where(np.isfinite(sd) & (sd > 0), sd, 0.01 * np.abs(A).max())

    def model(x, Ainf, B, p):
        return Ainf + B * x ** (-p)
    try:
        popt, pcov = curve_fit(model, n, A, p0=[0.0, A[0], 0.5], sigma=sd,
                               absolute_sigma=True, maxfev=100000)
        perr = np.sqrt(np.diag(pcov))
        return dict(A_inf=float(popt[0]), A_inf_err=float(perr[0]),
                    B=float(popt[1]), p=float(popt[2]), p_err=float(perr[2]),
                    chi2=float(np.sum(((A - model(n, *popt)) / sd) ** 2)), dof=len(n) - 3)
    except Exception as e:
        return dict(error=str(e))


def verdict(lad, fit):
    A = np.array([r["A"] for r in lad])
    nb = np.array([r["nbar"] for r in lad])
    G1 = np.array([r["G"]["N1"] for r in lad])
    G1a = np.array([r["G"]["N1a"] for r in lad])
    notes = []
    mono = bool(np.all(np.diff(np.abs(A)) <= 0.05 * np.abs(A).max()))
    top2_small = bool(np.all(np.abs(G1[-2:]) < 3))
    top2_big = bool(np.all(np.abs(G1[-2:]) > 5) and np.all(np.abs(G1a[-2:]) > 5)
                    and np.all(np.sign(G1[-2:]) == np.sign(G1[-1])))
    # saturation: top density vs the density one decade below
    i_dec = int(np.argmin(np.abs(np.log10(nb) - (np.log10(nb[-1]) - 1))))
    sat = bool(abs(A[-1] - A[i_dec]) < 0.25 * abs(A[-1])) if A[-1] != 0 else False
    Gflat = bool(abs(G1[-1]) >= abs(G1[i_dec]))
    Ainf_sig = (abs(fit.get("A_inf", 0)) / fit["A_inf_err"]
                if fit.get("A_inf_err", 0) > 0 else float("nan"))
    a = mono and top2_small and (Ainf_sig < 3)
    b = sat and top2_big and Gflat and (Ainf_sig > 5)
    notes.append(f"monotone decline: {mono}")
    notes.append(f"|G_N1| < 3 at top two densities: {top2_small} "
                 f"(G = {G1[-2]:+.2f}, {G1[-1]:+.2f})")
    notes.append(f"|G| > 5 vs BOTH shot nulls at top two: {top2_big} "
                 f"(N1a G = {G1a[-2]:+.2f}, {G1a[-1]:+.2f})")
    notes.append(f"saturation |A_max - A_dec|<0.25|A_max|: {sat} "
                 f"(A = {A[-1]:+.4f} vs {A[i_dec]:+.4f} at nbar={nb[i_dec]:.2f})")
    notes.append(f"G not declining over top decade: {Gflat}")
    notes.append(f"A_inf = {fit.get('A_inf', float('nan')):+.4f} "
                 f"+- {fit.get('A_inf_err', float('nan')):.4f}  ({Ainf_sig:.1f} sigma); "
                 f"p = {fit.get('p', float('nan')):.3f} +- {fit.get('p_err', float('nan')):.3f} "
                 f"(pure Poisson shot => p = 0.5)")
    v = "(a) SHOT ARTIFACT" if a and not b else \
        "(b) PHYSICAL THIRD" if b and not a else "(c) AMBIGUOUS"
    return v, notes


def report(path):
    res = load(path)
    print(f"\n=== {res['meta']['sim']} snap {res['meta']['snap']} z={res['meta']['z']:.3f} "
          f"box={res['meta']['box_mpch']} Mpc/h  N={res['meta']['ntot']} ===")
    print(f"R used (scaled from the frozen 4/8/16 in a 205 box): "
          f"{[round(r,3) for r in res['meta']['R_used']]} Mpc/h")
    out = {}
    for kind, ng in (("cic", 64), ("ngp", 64), ("cic", 128)):
        lad, R8 = ladder(res, kind, ng)
        if not lad:
            continue
        tag = f"{kind.upper()} NG={ng}"
        print(f"\n--- {tag}   (verdict scale R = {R8} Mpc/h) ---")
        print(f"{'nbar':>10} {'empty':>7} {'sig_d':>7} {'A(real)':>10} {'+-rep':>8} "
              f"{'N1':>10} {'+-':>8} {'G_N1':>9} {'N1a':>10} {'G_N1a':>9} "
              f"{'N0':>9} {'N2':>9}")
        for r in lad:
            print(f"{r['nbar']:10.3f} {r['frac_empty']:7.3f} {r['sigma_delta']:7.3f} "
                  f"{r['A']:+10.4f} {r['A_sd']:8.4f} "
                  f"{r['nulls']['N1']['mean']:+10.4f} {r['nulls']['N1']['std']:8.4f} "
                  f"{r['G']['N1']:+9.2f} {r['nulls']['N1a']['mean']:+10.4f} "
                  f"{r['G']['N1a']:+9.2f} {r['nulls']['N0']['mean']:+9.4f} "
                  f"{r['nulls']['N2']['mean']:+9.4f}")
        fit = fit_asymptote(lad)
        v, notes = verdict(lad, fit)
        print(f"\n  fit A(nbar) = A_inf + B*nbar^-p :  {fit}")
        for n in notes:
            print("   -", n)
        print(f"  VERDICT [{tag}]: {v}")
        out[tag] = dict(ladder=lad, fit=fit, verdict=v, notes=notes)
    # all R for the primary column
    print("\n--- all smoothing scales, CIC NG=64 (real / N1 mean / G) ---")
    for r in res["rows"]:
        if r["kind"] == "cic" and r["ng"] == 64 and r["rep"] == 0:
            s = " | ".join(f"R={k}: {r['real'][k]:+.4f} / {r['nulls']['N1']['mean'][k]:+.4f}"
                           f" / {r['G']['N1'][k]:+7.2f}" for k in r["real"])
            print(f"  nbar={r['nbar']:9.3f}  {s}")
    with open(HERE / (Path(path).stem + "_verdict.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return out


if __name__ == "__main__":
    for p in (sys.argv[1:] or sorted(str(x) for x in HERE.glob("results_*.json"))):
        report(p)

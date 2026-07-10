#!/usr/bin/env python3
r"""
SPARC coherence-residual test — does effective dark mass track KINEMATICALLY
COHERENT baryons rather than total baryonic mass?

===============================================================================
PRE-REGISTERED PREDICTION (fixed BEFORE any residual was computed; verbatim from
papers/notes/bullet_cluster_correction.md §"The test this makes available today"
and gravity_dark_matter_reading.md §8.3-8.4):
===============================================================================

  The ledger reading claims effective dark mass tracks the KINEMATICALLY
  COHERENT baryonic component (cold, ordered, low sigma/v -> high copula
  coordination S), NOT total baryonic mass. Mass-weighted rules (Newtonian
  baryons, MOND/RAR) contain no such term; under the null the coherence
  correlation is exactly zero.

  Operationalization:
    - COHERENT   baryons: cold rotationally-supported disk stars + cold H I gas.
    - THERMALIZED baryons: pressure/dispersion-supported bulge (hot, random ->
      Maxwellian -> independence -> LOW S). Does NOT source dark mass.

  DERIVED SIGNS (written down before fitting; derivation in SUMMARY.md):
    Let  Delta = log10 g_obs - log10 g_RAR_fit(g_bar)   (excess over mass-weighted RAR).
    At FIXED g_bar, swapping mass from a coherent to a thermalized carrier removes
    dark-mass sourcing under the ledger but not under the null.

    P1  partial rho(Delta, f_bul)  <  0     (thermalized fraction -> LESS dark mass)
    P2  partial rho(Delta, f_gas)  >= 0      (cold H I is COHERENT -> counts; must
                                              NOT behave like the bulge)
    P3  INTERNAL CONSISTENCY: sign(rho_bul) != sign(rho_gas). If they carry the
        SAME sign after controls, "coherence" is an empty relabelling of a
        surface-brightness / mass proxy and the claim is EMPTY.

  INTERPRETATION BANDS (fixed in advance, applied to the partial Spearman rho for
  f_bul, the discriminating variable):
    |partial rho| < 0.1                         -> NULL (no coherence term)
    0.1 <= |partial rho| < 0.3                  -> WEAK
    |partial rho| >= 0.3 and CI excludes 0      -> SUPPORTED (with correct sign)

  POWER / FLOOR (honest scope, respected from reading §8.3):
    SPARC RAR observed scatter   ~0.13 dex   (McGaugh+16, Lelli+17a)
    after marginalizing Ups*,D,i  0.057 dex   (Li & McGaugh 2018)
    intrinsic scatter             0.034 dex   (Desmond 2023)
    => SYSTEMATIC FLOOR ~0.10 dex is 3-4x the intrinsic signal. Any coherence
       effect that lives BELOW the floor is uninterpretable. If the test cannot
       resolve the predicted effect it is declared UNDERPOWERED, NOT a null.

===============================================================================
DATA: SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157). VizieR J/AJ/152/157
      machine-readable table2.dat (mass models, 3391 rows) + table1.dat (175-gal
      sample properties). Downloaded from cdsarc.cds.unistra.fr; cross-checked
      against astroweb.case.edu/SPARC. NO SYNTHETIC DATA. If a required column is
      missing the script stops rather than imputing.

Conventions (SPARC standard, ReadMe notes):
  - Vdisk, Vbul tabulated at M/L = 1; scaled by Ups_disk = 0.5, Ups_bul = 0.7.
  - Vgas already includes the 1.33 helium factor.
  - Baryonic accel keeps the SIGN of the gas term (central H I holes give Vgas<0):
        Vbar^2 = Ups_d*Vdisk^2 + Ups_b*Vbul^2 + Vgas*|Vgas|
  - g = (V[km/s]*1e3)^2 / (r[kpc]*KPC_M)   in m/s^2.

Run:  python3 sparc_coherence.py     (numpy/scipy/pandas/matplotlib; seed 20260710)
Outputs: results.json, SUMMARY.md is written by hand, figures/*.png.
"""
import json, os
import numpy as np
from scipy import optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
FIG  = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
SEED = 20260710
RNG  = np.random.default_rng(SEED)

KPC_M = 3.0856775814913673e19       # kpc -> m
G_DAGGER = 1.2e-10                    # m/s^2, McGaugh+16 RAR acceleration scale
UPS_D, UPS_B = 0.5, 0.7              # SPARC standard stellar M/L at 3.6um

# ---------------------------------------------------------------------------
# 1. Load SPARC fixed-width tables (byte ranges from the VizieR ReadMe).
# ---------------------------------------------------------------------------
def load_table1():
    """Per-galaxy properties. Returns dict name -> {Dist,inc,e_i,L36,SBeff,MHI,Vflat,Qual,Type}."""
    out = {}
    with open(os.path.join(DATA, "table1.dat")) as f:
        for ln in f:
            if not ln.strip():
                continue
            out[ln[0:11].strip()] = dict(
                Type = int(ln[12:14]),
                Dist = float(ln[15:21]),
                inc  = float(ln[30:34]),
                e_i  = float(ln[35:39]),
                L36  = float(ln[40:47]),
                SBeff= float(ln[62:70]),
                MHI  = float(ln[86:93]),
                Vflat= float(ln[100:105]),
                Qual = int(ln[112:115]),
            )
    return out

def load_table2():
    """Mass-model rows. Returns dict name -> arrays (Rad,Vobs,e_Vobs,Vgas,Vdisk,Vbulge,SBdisk,SBbulge)."""
    cols = {k: {} for k in ("Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge","SBdisk","SBbulge")}
    order = []
    with open(os.path.join(DATA, "table2.dat")) as f:
        for ln in f:
            if not ln.strip():
                continue
            nm = ln[0:11].strip()
            if nm not in cols["Rad"]:
                for k in cols: cols[k][nm] = []
                order.append(nm)
            cols["Rad"][nm].append(float(ln[19:25]))
            cols["Vobs"][nm].append(float(ln[26:32]))
            cols["e_Vobs"][nm].append(float(ln[33:38]))
            cols["Vgas"][nm].append(float(ln[39:45]))
            cols["Vdisk"][nm].append(float(ln[46:52]))
            cols["Vbulge"][nm].append(float(ln[53:59]))
            cols["SBdisk"][nm].append(float(ln[60:67]))
            cols["SBbulge"][nm].append(float(ln[68:76]))
    gal = {}
    for nm in order:
        gal[nm] = {k: np.asarray(cols[k][nm], float) for k in cols}
    return gal

# ---------------------------------------------------------------------------
# 2. Build the per-point analysis table.
# ---------------------------------------------------------------------------
def accel(v_kms, r_kpc):
    return (v_kms * 1e3) ** 2 / (r_kpc * KPC_M)

def build(t1, t2, qmax=2, inc_min=30.0, ferr_max=0.10):
    """Canonical RAR sample selection (McGaugh+16, Lelli+17a): Qual<=2, inclination
    >= 30 deg (face-on galaxies have unreliable V_obs), and per-point fractional
    velocity error e_Vobs/Vobs <= 0.10. These cuts are what reproduce the published
    ~0.11-0.13 dex scatter; they are the instrument, not a tuning knob."""
    rows = []
    for nm, g in t2.items():
        if nm not in t1:
            continue
        meta = t1[nm]
        if meta["Qual"] > qmax or meta["inc"] < inc_min:
            continue
        r   = g["Rad"]
        vg, vd, vb = g["Vgas"], g["Vdisk"], g["Vbulge"]
        vbar2 = UPS_D * vd**2 + UPS_B * vb**2 + vg * np.abs(vg)   # signed gas term
        vobs  = g["Vobs"]
        with np.errstate(divide="ignore", invalid="ignore"):
            ferr = g["e_Vobs"] / np.where(vobs > 0, vobs, np.nan)
        good  = ((r > 0) & (vobs > 0) & (vbar2 > 0) & np.isfinite(vbar2)
                 & (ferr <= ferr_max) & np.isfinite(ferr))
        for i in np.where(good)[0]:
            gbar = accel(np.sqrt(vbar2[i]), r[i])
            gobs = accel(vobs[i], r[i])
            comp_gas  = vg[i] * abs(vg[i])
            comp_disk = UPS_D * vd[i] ** 2
            comp_bul  = UPS_B * vb[i] ** 2
            rows.append(dict(
                name=nm, Type=meta["Type"], Qual=meta["Qual"], inc=meta["inc"],
                Dist=meta["Dist"], SBeff=meta["SBeff"], L36=meta["L36"], MHI=meta["MHI"],
                r=r[i], gbar=gbar, gobs=gobs,
                lgbar=np.log10(gbar), lgobs=np.log10(gobs),
                # coherence proxies (fractions of the mass-weighted baryonic accel):
                f_bul = comp_bul / vbar2[i],
                f_gas = comp_gas / vbar2[i],
                f_disk= comp_disk / vbar2[i],
                e_Vobs=g["e_Vobs"][i], Vobs=vobs[i],
            ))
    return rows

# ---------------------------------------------------------------------------
# 3. RAR fit + residual (instrument check).
# ---------------------------------------------------------------------------
def rar_func(gbar, gdag):
    """McGaugh+2016 RAR: g_obs = g_bar / (1 - exp(-sqrt(g_bar/gdag)))."""
    x = np.sqrt(gbar / gdag)
    return gbar / (1.0 - np.exp(-x))

def fit_rar(gbar, gobs):
    """Fit gdag by least squares in log space; return gdag, residual dex, scatter."""
    lgobs = np.log10(gobs)
    def resid(p):
        gdag = 10 ** p[0]
        return np.log10(rar_func(gbar, gdag)) - lgobs
    sol = optimize.least_squares(resid, x0=[np.log10(G_DAGGER)])
    gdag = 10 ** sol.x[0]
    delta = lgobs - np.log10(rar_func(gbar, gdag))     # residual in dex
    return gdag, delta

# ---------------------------------------------------------------------------
# 4. Partial Spearman correlation with galaxy-clustered bootstrap CI.
# ---------------------------------------------------------------------------
def _rank(a):
    return stats.rankdata(a)

def partial_spearman(y, x, controls):
    """Spearman partial correlation of y,x controlling for columns of `controls`
    (list of 1d arrays). Rank-transform everything, regress out controls linearly,
    correlate residuals (Pearson on ranks == Spearman partial)."""
    Y = _rank(y); X = _rank(x)
    if controls:
        C = np.column_stack([_rank(c) for c in controls])
        C = np.column_stack([np.ones(len(Y)), C])
        # residualize
        by, *_ = np.linalg.lstsq(C, Y, rcond=None)
        bx, *_ = np.linalg.lstsq(C, X, rcond=None)
        Yr = Y - C @ by
        Xr = X - C @ bx
    else:
        Yr, Xr = Y - Y.mean(), X - X.mean()
    if Yr.std() < 1e-12 or Xr.std() < 1e-12:
        return np.nan
    return float(np.corrcoef(Yr, Xr)[0, 1])

def boot_partial(df_arrays, ykey, xkey, ctrl_keys, groups, nboot=2000):
    """Cluster (by galaxy) bootstrap of the partial Spearman. df_arrays: dict of arrays.
    groups: array of galaxy names (cluster id)."""
    y = df_arrays[ykey]; x = df_arrays[xkey]
    ctrls = [df_arrays[k] for k in ctrl_keys]
    point = partial_spearman(y, x, ctrls)
    uniq = np.unique(groups)
    idx_by_g = {gname: np.where(groups == gname)[0] for gname in uniq}
    stats_b = []
    for _ in range(nboot):
        pick = RNG.choice(uniq, size=len(uniq), replace=True)
        sel = np.concatenate([idx_by_g[g] for g in pick])
        yb, xb = y[sel], x[sel]
        cb = [c[sel] for c in ctrls]
        r = partial_spearman(yb, xb, cb)
        if np.isfinite(r):
            stats_b.append(r)
    stats_b = np.array(stats_b)
    lo, hi = np.percentile(stats_b, [2.5, 97.5])
    p_two = 2 * min((stats_b > 0).mean(), (stats_b < 0).mean())
    return dict(rho=point, ci=[float(lo), float(hi)], p=float(min(1.0, p_two)),
                nboot=len(stats_b))

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    t1, t2 = load_table1(), load_table2()
    assert len(t1) == 175, f"expected 175 galaxies in table1, got {len(t1)}"

    rows = build(t1, t2, qmax=2)
    if not rows:
        raise SystemExit("no rows survived quality/positivity cuts")
    keys = rows[0].keys()
    A = {k: np.array([r[k] for r in rows], dtype=object if k == "name" else float) for k in keys}
    A["name"] = np.array([r["name"] for r in rows])
    ngal = len(np.unique(A["name"]))
    npts = len(rows)

    # ---- instrument check: RAR fit + scatter ----
    gdag, delta = fit_rar(A["gbar"], A["gobs"])
    A["delta"] = delta
    obs_scatter = float(np.std(delta))
    # also the fixed-gdag (standard 1.2e-10) scatter, for a second reference
    delta_std = A["lgobs"] - np.log10(rar_func(A["gbar"], G_DAGGER))
    scatter_std = float(np.std(delta_std))

    instrument = dict(
        gdag_fit=float(gdag), gdag_fit_e10=float(np.log10(gdag)),
        rar_scatter_dex_fitted=obs_scatter,
        rar_scatter_dex_stdgdag=scatter_std,
        n_points=npts, n_galaxies=ngal,
        reference_band="0.11-0.13 dex (McGaugh+16, Lelli+17a)",
        instrument_ok=bool(0.10 <= obs_scatter <= 0.16),
    )

    # ---- coherence proxy distributions ----
    bulge_pts = int((A["f_bul"] > 1e-6).sum())
    bulge_gals = int(len(np.unique(A["name"][A["f_bul"] > 1e-6])))
    proxy_summary = dict(
        n_points_with_bulge=bulge_pts, n_galaxies_with_bulge=bulge_gals,
        f_bul=dict(min=float(A["f_bul"].min()), max=float(A["f_bul"].max()),
                   mean=float(A["f_bul"].mean())),
        f_gas=dict(min=float(A["f_gas"].min()), max=float(A["f_gas"].max()),
                   mean=float(A["f_gas"].mean())),
        f_disk=dict(min=float(A["f_disk"].min()), max=float(A["f_disk"].max()),
                    mean=float(A["f_disk"].mean())),
        corr_fbul_fgas=float(stats.spearmanr(A["f_bul"], A["f_gas"]).statistic),
    )

    # ---- the test: partial Spearman of delta vs coherence proxies ----
    # PRIMARY controls (pre-registered, per brief): inclination + quality.
    ctrl_primary = ["inc", "Qual"]
    # ROBUSTNESS controls: add g_bar (removes the acceleration-regime confound that
    # bulges live at high g_bar / gas at low g_bar) and surface brightness SBeff.
    ctrl_robust  = ["inc", "Qual", "lgbar", "SBeff"]

    def run_block(ctrls, label):
        block = {"controls": ctrls, "label": label}
        for xkey in ("f_bul", "f_gas", "f_disk"):
            block[xkey] = boot_partial(A, "delta", xkey, ctrls, A["name"], nboot=3000)
        # unadjusted (no controls) too, for transparency
        return block

    tests = dict(
        raw=run_block([], "no controls (raw Spearman)"),
        primary=run_block(ctrl_primary, "pre-registered: control inc + Qual"),
        robust=run_block(ctrl_robust, "robustness: + lgbar + SBeff"),
    )

    # ---- bulge-only subsample (where f_bul actually varies) ----
    # The f_bul test is only powered where bulges exist. Restrict to galaxies with
    # a bulge and re-run f_bul so the correlation is not diluted by the ~80% of
    # points with f_bul==0.
    bmask = np.array([nm in set(np.unique(A["name"][A["f_bul"] > 1e-6])) for nm in A["name"]])
    if bmask.sum() > 30:
        Ab = {k: A[k][bmask] for k in A}
        bulge_only = {}
        for lbl, ctrls in (("primary", ctrl_primary), ("robust", ctrl_robust)):
            bulge_only[lbl] = boot_partial(Ab, "delta", "f_bul", ctrls, Ab["name"], nboot=3000)
        bulge_only["n_points"] = int(bmask.sum())
        bulge_only["n_galaxies"] = int(len(np.unique(A["name"][bmask])))
    else:
        bulge_only = {"note": "too few bulge points for a subsample test"}

    # ---- verdict logic ----
    rho_bul = tests["primary"]["f_bul"]["rho"]
    ci_bul  = tests["primary"]["f_bul"]["ci"]
    rho_gas = tests["primary"]["f_gas"]["rho"]
    ci_gas  = tests["primary"]["f_gas"]["ci"]
    same_sign = (np.sign(rho_bul) == np.sign(rho_gas))

    # sensitivity: what partial-rho does the delta scatter let us resolve?
    # For n_eff galaxies clusters, the sampling sd of Spearman ~ 1/sqrt(n_eff-1).
    n_eff = ngal
    rho_resolvable = 1.0 / np.sqrt(max(n_eff - 1, 1))   # ~2-sigma-ish detectable |rho|

    def band(rho, ci):
        if not np.isfinite(rho):
            return "UNDEFINED"
        excl0 = (ci[0] > 0) or (ci[1] < 0)
        if abs(rho) >= 0.3 and excl0:
            return "STRONG"
        if abs(rho) >= 0.1:
            return "WEAK"
        return "NULL"

    band_bul = band(rho_bul, ci_bul)
    sign_ok  = rho_bul < 0            # P1: negative predicted
    gas_ok   = rho_gas >= 0           # P2: gas not negative

    # Overall verdict:
    #  - floor first: the residual scatter is dominated by the ~0.10 dex systematic
    #    floor; effect sizes in dex below that are uninterpretable regardless of rho.
    #  - EMPTY-VARIABLE if f_bul and f_gas carry the SAME sign after controls.
    #  - SUPPORTED only if band>=WEAK-to-STRONG, sign matches, opposite to gas.
    #  - else NULL, unless power says UNDERPOWERED.
    if same_sign:
        verdict = "EMPTY-VARIABLE"
    elif band_bul == "STRONG" and sign_ok and gas_ok:
        verdict = "SUPPORTED"
    elif band_bul in ("WEAK", "STRONG") and sign_ok and gas_ok:
        verdict = "WEAK-SUPPORT"
    elif abs(rho_bul) < rho_resolvable and band_bul == "NULL":
        verdict = "UNDERPOWERED"
    else:
        verdict = "NULL"

    out = dict(
        seed=SEED,
        prediction=dict(
            P1="partial rho(delta, f_bul) < 0",
            P2="partial rho(delta, f_gas) >= 0",
            P3="sign(rho_bul) != sign(rho_gas), else EMPTY-VARIABLE",
            bands="|rho|<0.1 NULL; 0.1-0.3 WEAK; >=0.3 & CI excl 0 STRONG",
        ),
        instrument=instrument,
        proxies=proxy_summary,
        tests=tests,
        bulge_only_subsample=bulge_only,
        sensitivity=dict(
            systematic_floor_dex=0.10,
            intrinsic_scatter_dex=0.034,
            measured_rar_scatter_dex=obs_scatter,
            rho_resolvable_2sig=float(rho_resolvable),
            n_galaxies=ngal,
            note=("Effect sizes are reported as partial rho AND in dex. Any dex-scale "
                  "effect below the 0.10 dex floor is systematics-limited."),
        ),
        verdict_components=dict(
            rho_bul=rho_bul, ci_bul=ci_bul, band_bul=band_bul,
            sign_matches_P1=bool(sign_ok), rho_gas=rho_gas, ci_gas=ci_gas,
            gas_matches_P2=bool(gas_ok), same_sign_EMPTY=bool(same_sign),
        ),
        verdict=verdict,
    )

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=2)

    # ---- figures ----
    make_figures(A, gdag, tests, instrument)

    # ---- console ----
    print(f"SPARC loaded: {len(t1)} galaxies (table1), {npts} points / {ngal} galaxies after Q<=2 cut.")
    print(f"[instrument] RAR fit gdag={gdag:.3e} m/s^2, scatter={obs_scatter:.3f} dex "
          f"(std-gdag {scatter_std:.3f}); ref 0.11-0.13 dex -> ok={instrument['instrument_ok']}")
    print(f"[proxies] {bulge_gals} galaxies with bulge; f_bul/f_gas Spearman={proxy_summary['corr_fbul_fgas']:.2f}")
    for lbl in ("raw", "primary", "robust"):
        b = tests[lbl]
        print(f"[{lbl:7s}] f_bul rho={b['f_bul']['rho']:+.3f} CI{np.round(b['f_bul']['ci'],3).tolist()} "
              f"| f_gas rho={b['f_gas']['rho']:+.3f} CI{np.round(b['f_gas']['ci'],3).tolist()}")
    if "primary" in bulge_only:
        bo = bulge_only["primary"]
        print(f"[bulge-only] f_bul rho={bo['rho']:+.3f} CI{np.round(bo['ci'],3).tolist()} "
              f"(n={bulge_only['n_points']} pts / {bulge_only['n_galaxies']} gal)")
    print(f"[power] rho resolvable at 2sig ~ {rho_resolvable:.3f} (n_gal={ngal})")
    print(f"VERDICT: {verdict}")
    return out


def make_figures(A, gdag, tests, instrument):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Fig 1: RAR instrument check
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(A["lgbar"], A["lgobs"], s=4, alpha=0.25, color="#3b6ea5", edgecolor="none")
    xs = np.linspace(A["lgbar"].min(), A["lgbar"].max(), 200)
    ax.plot(xs, np.log10(rar_func(10**xs, gdag)), "k-", lw=1.5,
            label=f"RAR fit g$^\\dagger$={gdag:.2e}")
    ax.plot(xs, xs, "k--", lw=0.8, alpha=0.6, label="1:1 (Newtonian)")
    ax.set_xlabel(r"$\log_{10}\, g_{\rm bar}\ \rm[m/s^2]$")
    ax.set_ylabel(r"$\log_{10}\, g_{\rm obs}\ \rm[m/s^2]$")
    ax.set_title(f"SPARC RAR  (scatter {instrument['rar_scatter_dex_fitted']:.3f} dex, "
                 f"{instrument['n_galaxies']} gal, Q$\\leq$2)")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_rar_instrument.png"), dpi=130)
    plt.close(fig)

    # Fig 2: residual vs f_bul and f_gas
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, key, col, ttl in ((axes[0], "f_bul", "#b5495b", "bulge fraction (thermalized)"),
                              (axes[1], "f_gas", "#3a923a", "gas fraction (cold H I, coherent)")):
        ax.axhline(0, color="k", lw=0.6, alpha=0.5)
        ax.scatter(A[key], A["delta"], s=5, alpha=0.25, color=col, edgecolor="none")
        r = tests["primary"][key]["rho"]; ci = tests["primary"][key]["ci"]
        ax.set_xlabel(f"$f_{{\\rm {key.split('_')[1]}}}$")
        ax.set_title(f"{ttl}\npartial $\\rho$={r:+.3f} CI[{ci[0]:+.2f},{ci[1]:+.2f}]", fontsize=9)
    axes[0].set_ylabel(r"RAR residual $\Delta=\log g_{\rm obs}-\log g_{\rm RAR}$ [dex]")
    fig.suptitle("Coherence-residual test (controls: inclination + quality)", fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_residual_vs_proxies.png"), dpi=130)
    plt.close(fig)

    # Fig 3: partial-rho summary across control sets
    fig, ax = plt.subplots(figsize=(7, 4.5))
    labels = ["raw", "primary", "robust"]
    xk = ["f_bul", "f_gas", "f_disk"]
    colors = {"f_bul": "#b5495b", "f_gas": "#3a923a", "f_disk": "#3b6ea5"}
    width = 0.25
    for j, k in enumerate(xk):
        rhos = [tests[l][k]["rho"] for l in labels]
        cis  = [tests[l][k]["ci"] for l in labels]
        xpos = np.arange(len(labels)) + (j - 1) * width
        err = np.array([[r - c[0] for r, c in zip(rhos, cis)],
                        [c[1] - r for r, c in zip(rhos, cis)]])
        ax.bar(xpos, rhos, width, color=colors[k], alpha=0.85, label=k)
        ax.errorbar(xpos, rhos, yerr=err, fmt="none", ecolor="k", elinewidth=0.8, capsize=2)
    ax.axhline(0, color="k", lw=0.8)
    ax.axhspan(-0.1, 0.1, color="gray", alpha=0.15, label="NULL band |ρ|<0.1")
    ax.set_xticks(np.arange(len(labels))); ax.set_xticklabels(labels)
    ax.set_ylabel(r"partial Spearman $\rho$ (vs $\Delta$)")
    ax.set_title("Coherence proxies vs RAR residual, by control set")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_partial_rho_summary.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

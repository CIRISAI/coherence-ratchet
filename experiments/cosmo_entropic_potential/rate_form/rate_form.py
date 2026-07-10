#!/usr/bin/env python3
"""
rate_form.py — the RATE-form sign law for w(a).

STOCK form (papers/notes/lambda_maintenance_wz.md, s_of_a.py):
    rho_DE(a) ~ S(a)                       =>   1 + w = -(1/3) dlnS/dlna
    computed result: S monotone FALLING => w > -1 always (thawing), no phantom.

RATE form (this file): the framework's OWN equilibrium condition is a POWER,
    corridor_requires_maintenance:  gamma*M = alpha   (work per unit time).
So map dark energy to the MAINTENANCE POWER, not the stock:
    rho_DE(a) ~ P_maint(a)                 =>   1 + w = -(1/3) dlnP_maint/dlna.

Three operationalizations of P_maint, each derived not asserted:
  (a) EQUILIBRIUM:   P ~ gamma*M = alpha = |dS/dt|_free  = |dlnS/dlna| * S * H(a)
                     (a-time reading includes H; a-efold reading drops it)
  (b) DYNAMICAL-TIME: P ~ S / tau_dyn,  tau_dyn ~ 1/sqrt(G rho_m) ~ a^{3/2}
  (c) DISSIPATION:   P ~ entropy-production rate of the NESS = gamma*M(S_ss);
                     scaling argument only, calibrated off the Lindblad sweep.

Everything inherits the §1.1 comoving-normalization caveat of the stock note:
rho_DE ~ P_maint equates a DENSITY with an extensive power, so it is well-posed
only per COMOVING volume, and that choice (not physical volume) is what makes a
constant-power structure give w = -1. Restated, not repaired.

Reuses the already-computed cell-grain S(a) from ../results.json ["combined"]
(lognormal nonlinear + Gaussian causal mask, the same S the stock note uses) and
the H(a), CPL, and log-derivative machinery from ../s_of_a.py.

F-11: forward content only. dlnP/dlna is a steady-state readout of a forward
continuity equation; no backward P_omega, no D4, no F-19.
"""

import json
import sys
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))

from s_of_a import E, dln_dlna, fit_cpl, OM, OL, DESI_W0, DESI_WA  # noqa: E402


def w_from_P(a, P):
    """Sign law on any density-proxy P(a): 1 + w = -(1/3) dlnP/dlna."""
    return -1.0 - dln_dlna(a, P) / 3.0


def crossing_z(a, w):
    """Redshift(s) where w crosses -1 (phantom divide). Linear interp in a."""
    f = w + 1.0
    zs = []
    for i in range(len(a) - 1):
        if f[i] == 0.0:
            zs.append(1.0 / a[i] - 1.0)
        elif f[i] * f[i + 1] < 0.0:
            t = -f[i] / (f[i + 1] - f[i])
            ac = a[i] + t * (a[i + 1] - a[i])
            zs.append(1.0 / ac - 1.0)
    return zs


def summarize(name, a, P, note=""):
    P = np.asarray(P, dtype=float)
    w = w_from_P(a, P)
    w0, wa = fit_cpl(a, w)
    zc = crossing_z(a, w)
    phantom_past = bool(np.any(w[:-1] < -1.0))
    onePlusW0 = 1.0 + w0
    ratio = wa / onePlusW0 if abs(onePlusW0) > 1e-6 else float("nan")
    d = dict(
        name=name, note=note,
        w0=float(w0), wa=float(wa), w_today=float(w[-1]),
        onePlusW0_today=float(1.0 + w[-1]),
        sign_1plusw_today=int(np.sign(1.0 + w[-1])),
        phantom_past=phantom_past,
        w_min=float(w.min()), w_max=float(w.max()),
        crossing_z=[float(z) for z in zc],
        wa_over_1plusw0=float(ratio),
        w=w.tolist(),
    )
    print(f"\n[{name}] {note}")
    print(f"    w0={w0:+.3f}  wa={wa:+.3f}  w_today={w[-1]:+.3f}  "
          f"1+w_today={1.0+w[-1]:+.3f} (sign {int(np.sign(1.0+w[-1])):+d})")
    print(f"    w range [{w.min():+.3f}, {w.max():+.3f}]  phantom_past={phantom_past}")
    print(f"    crossing z={['%.3f'%z for z in zc] or 'none'}  "
          f"wa/(1+w0)={ratio:+.3f}")
    return d


def main():
    res = json.load(open(PARENT / "results.json"))
    comb = res["combined"]
    a = np.array(comb["a_grid"])
    S = np.array(comb["S"])
    g = np.array(comb["dlnS_dlna"])          # = dlnS/dlna, negative (S falls)
    H = E(a)                                  # H/H0

    z_eq = res["background"]["z_matter_lambda_equality"]     # 0.296
    z_acc = res["background"]["z_accel_onset"]               # 0.632
    z_desi_lo, z_desi_hi = 0.2, 0.5

    out = {
        "provenance": "S(a) from ../results.json['combined'] (nonlinear lognormal + "
                      "Gaussian event-horizon mask); H(a), CPL, dln/dlna from ../s_of_a.py",
        "normalization_caveat": (
            "rho_DE ~ P_maint equates a density with an extensive power; well-posed "
            "only per COMOVING volume. Same hidden step as stock note §1.1/§7(a): the "
            "comoving choice is what forces w=-1 for constant-power structure."),
        "F11": "forward content only; steady-state readout of forward continuity eqn.",
        "epochs": dict(z_matter_lambda_equality=z_eq, z_accel_onset=z_acc,
                       z_desi_crossing_window=[z_desi_lo, z_desi_hi]),
        "cosmology": dict(Om=OM, OL=OL),
        "a_grid": a.tolist(),
        "S": S.tolist(), "dlnS_dlna": g.tolist(), "H_over_H0": H.tolist(),
    }

    # ---- reference: STOCK form recomputed here (sanity vs results.json) ------
    out["stock"] = summarize("stock", a, S,
                             "rho_DE ~ S  (reproduces the falling-S thawing result)")

    # ---- candidate (a): EQUILIBRIUM,  P ~ |dS/dt| = |g| S H -----------------
    # This is the literal "maintenance power = drift rate S would have if maintenance
    # stopped." The free-drift rate in cosmology is gravitational: dS/dt = (dS/dlna)*H.
    P_a_time = np.abs(g) * S * H
    out["cand_a_time"] = summarize(
        "cand_a_time", a, P_a_time,
        "P ~ |dS/dt| = |dlnS/dlna|*S*H  (drift rate PER UNIT TIME; carries H)")

    # a-efold variant: the SAME drift measured per e-fold of expansion, dropping H.
    # This is the hidden dt-vs-dlna choice; it changes the answer, so it is exposed.
    P_a_efold = np.abs(g) * S
    out["cand_a_efold"] = summarize(
        "cand_a_efold", a, P_a_efold,
        "P ~ |dS/dlna|*S  (drift rate PER E-FOLD; H dropped -- the hidden time choice)")

    # ---- candidate (b): DYNAMICAL TIME,  P ~ S / tau_dyn --------------------
    # tau_dyn ~ 1/sqrt(G rho_m); rho_m ~ a^-3 EXACTLY (matter dilutes as a^-3
    # independent of dark energy), so tau_dyn ~ a^{3/2}, dln(tau)/dlna = +3/2 exactly.
    tau_dyn = a ** 1.5
    P_b = S / tau_dyn
    out["cand_b"] = summarize(
        "cand_b", a, P_b,
        "P ~ S/tau_dyn, tau_dyn~a^{3/2} (mean-density dynamical time)")

    # b-frozen variant: if tau_dyn is the VIRIAL time of collapsed halos it is ~frozen
    # (halos keep ~fixed internal density post-collapse), dln(tau)/dlna ~ 0 => stock.
    out["cand_b_frozen"] = summarize(
        "cand_b_frozen", a, S,
        "P ~ S/tau_frozen (virialized halos: tau const) -> collapses to stock form")

    # ---- candidate (c): DISSIPATION, scaling from the Lindblad NESS sweep ----
    # NESS entropy production at steady state = maintenance power = gamma*M.
    # The lyapunov_check 'align' sweep gives S_ss(gamma*M) monotone decreasing.
    # Invert: fit ln(gamma*M) = m * ln(S_ss) + b over the corridor points, so
    # dln(P)/dlna = dln(gamma*M)/dlnS_ss * dlnS/dlna = m * g.
    lyap = json.load(open(PARENT.parent / "open_system_pomega" /
                          "lyapunov_check" / "results.json"))
    grid = lyap["grid_align"]
    gM = np.array([p["gamma_M"] for p in grid])
    Sss = np.array([p["S_det_k6"] for p in grid])
    ok = (gM > 0) & (Sss > 1e-6)
    m_slope, b_int = np.polyfit(np.log(Sss[ok]), np.log(gM[ok]), 1)
    # scaling: gamma*M ~ S_ss^m  =>  P(a) ~ S(a)^m ; sign law on that:
    P_c = S ** m_slope
    out["cand_c"] = summarize(
        "cand_c", a, P_c,
        f"P ~ gamma*M ~ S^m, m={m_slope:.3f} (inverted Lindblad NESS sweep; SCALING only)")
    out["cand_c"]["ness_inversion_slope_m"] = float(m_slope)
    out["cand_c"]["ness_note"] = (
        "m<0: gamma*M rises as S_ss falls. Cosmologically S falls => gamma*M rises => "
        "P rises => w<-1 (phantom) for ALL a: mirror image of the stock form, NOT a "
        "crossing. LAB-SYSTEM scaling; the S_ss(gamma*M) curve is a 6-spin Lindblad "
        "NESS, not the cosmic field. Leap flagged.")

    # ---- consistency trap (task 4): where does cand_a cross w=-1? -----------
    # Stock w=-1 <=> dS/dt=0 (extremum of S); S is monotone so it never crosses.
    # Rate-(a) w=-1 <=> d|dS/dt|/dt=0 (inflection of S in TIME); can exist while S
    # is monotone. Compare its crossing epoch to equality / onset / DESI window.
    zc_a = out["cand_a_time"]["crossing_z"]
    zc_ae = out["cand_a_efold"]["crossing_z"]
    out["consistency_trap"] = dict(
        stock_crossing="none (S monotone => dS/dt never zero => w>-1 always)",
        rate_a_time_crossing_z=zc_a,
        rate_a_efold_crossing_z=zc_ae,
        interpretation=(
            "Rate form crosses w=-1 at an INFLECTION of S(t), which can exist even "
            "though S(t) is monotone -- this is the only way the framework gets a "
            "crossing at all. Whether it lands in DESI's z~0.2-0.5 window is the test."),
        lands_in_desi_window_a_time=bool(any(z_desi_lo <= z <= z_desi_hi for z in zc_a)),
        lands_in_desi_window_a_efold=bool(any(z_desi_lo <= z <= z_desi_hi for z in zc_ae)),
    )

    # ---- verdict table ------------------------------------------------------
    desi_ratio = DESI_WA / (1.0 + DESI_W0)
    stock_ratio = res["cpl_line"]["mean"]
    rows = []
    for key in ["stock", "cand_a_time", "cand_a_efold", "cand_b", "cand_b_frozen", "cand_c"]:
        d = out[key]
        rows.append(dict(
            candidate=key,
            sign_1plusw_today=d["sign_1plusw_today"],
            phantom_past=d["phantom_past"],
            crossing_z=d["crossing_z"],
            wa_over_1plusw0=d["wa_over_1plusw0"]))
    out["verdict_table"] = dict(
        desi_wa_over_1plusw0=float(desi_ratio),
        stock_wa_over_1plusw0=float(stock_ratio),
        desi_target="w<-1 in past, crossing at z~0.2-0.5, w>-1 today; wa/(1+w0)~-3.83",
        rows=rows)

    # any candidate matching DESI direction?
    matches = []
    for r in rows:
        got_phantom = r["phantom_past"]
        got_crossing = any(z_desi_lo <= z <= z_desi_hi for z in r["crossing_z"])
        got_today = r["sign_1plusw_today"] > 0
        if got_phantom and got_today:
            matches.append(dict(candidate=r["candidate"],
                                crossing_in_window=got_crossing))
    out["desi_direction_matches"] = matches

    with open(HERE / "results.json", "w") as f:
        json.dump(out, f, indent=2)

    # ---- figure -------------------------------------------------------------
    zg = 1.0 / a - 1.0
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for key, lab, sty in [("stock", "stock ρ~S", "k-"),
                          ("cand_a_time", "(a) ρ~|dS/dt|", "C0-"),
                          ("cand_a_efold", "(a') ρ~|dS/dlna|·S", "C0--"),
                          ("cand_b", "(b) ρ~S/τ_dyn", "C1-"),
                          ("cand_c", "(c) ρ~γM~S^m", "C2-")]:
        ax[0].plot(zg, out[key]["w"], sty, label=lab)
    wd = DESI_W0 + DESI_WA * (1 - a)
    ax[0].plot(zg, wd, "r:", lw=2, label=f"DESI CPL ({DESI_W0},{DESI_WA})")
    ax[0].axhline(-1, color="grey", lw=0.8)
    ax[0].axvspan(z_desi_lo, z_desi_hi, color="red", alpha=0.08)
    ax[0].set_xlabel("z"); ax[0].set_ylabel("w"); ax[0].set_xlim(0, zg.max())
    ax[0].set_ylim(-1.8, 0.2); ax[0].legend(fontsize=7)
    ax[0].set_title("Rate-form w(z): does any go phantom in the past?")

    for key, lab, sty in [("stock", "S", "k-"),
                          ("cand_a_time", "|dS/dt|", "C0-"),
                          ("cand_b", "S/τ_dyn", "C1-")]:
        P = {"stock": S, "cand_a_time": P_a_time, "cand_b": P_b}[key]
        ax[1].plot(zg, P / P[-1], sty, label=lab)
    ax[1].axvline(z_eq, color="purple", ls=":", label=f"m-Λ eq z={z_eq:.2f}")
    ax[1].axvline(z_acc, color="green", ls="--", label=f"accel onset z={z_acc:.2f}")
    ax[1].set_xlabel("z"); ax[1].set_ylabel("P(a)/P(1)"); ax[1].set_xlim(0, zg.max())
    ax[1].legend(fontsize=7); ax[1].set_title("The maintenance-power proxies")
    fig.tight_layout(); fig.savefig(HERE / "fig_rate_form.png", dpi=140)
    plt.close(fig)

    print("\n--- VERDICT ---")
    print(f"DESI target wa/(1+w0) = {desi_ratio:+.2f}; stock = {stock_ratio:+.2f}")
    print(f"DESI-direction matches (phantom past + w>-1 today): {matches or 'NONE'}")
    print("wrote results.json + fig_rate_form.png")
    return out


if __name__ == "__main__":
    main()

"""
Figures for the copula stress test. Money figure: gap vs scale vs redshift (tier 3).
Plus tier-1 estimator validation and tier-2 lognormal demonstration.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
R = json.load(open(os.path.join(HERE, "results.json")))


def fig_tier1():
    t = R.get("tier1")
    if not t:
        return
    cases = [c for c in t["cases"] if c["family"] == "kish"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    # panel 1: KSG vs analytic (identity line)
    for N, col in zip([2000, 8000, 32000], ["#d1495b", "#edae49", "#00798c"]):
        xs = [c["I_analytic"] for c in cases if c["N"] == N]
        ys = [c["ksg_mean"] for c in cases if c["N"] == N]
        es = [c["ksg_sd"] for c in cases if c["N"] == N]
        ax[0].errorbar(xs, ys, yerr=es, fmt="o", ms=4, capsize=2,
                       color=col, label=f"N={N}", alpha=0.8)
    lim = [0, max(c["I_analytic"] for c in cases) * 1.05]
    ax[0].plot(lim, lim, "k--", lw=1, label="identity")
    ax[0].set_xlabel(r"analytic  $I=-\frac12\ln\det C$  (nats)")
    ax[0].set_ylabel("KSG estimate (nats)")
    ax[0].set_title("Tier 1: KSG recovers the Gaussian multi-information")
    ax[0].legend(fontsize=8)
    # panel 2: bias vs N by dimension
    for m, col in zip([2, 3, 5, 8], ["#003f5c", "#7a5195", "#ef5675", "#ffa600"]):
        for N in [2000, 8000, 32000]:
            bs = [abs(c["ksg_bias"]) for c in cases if c["m"] == m and c["N"] == N]
            if bs:
                ax[1].scatter([N] * len(bs), bs, color=col, s=18, alpha=0.7,
                              label=f"m={m}" if N == 2000 else None)
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("N samples"); ax[1].set_ylabel("|KSG bias| (nats)")
    ax[1].set_title("Bias shrinks with N, grows with dimension")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig1_tier1_estimator.png"), dpi=110)
    plt.close(fig)
    print("wrote fig1")


def fig_tier2():
    t = R.get("tier2")
    if not t or "walltime_s" not in t:
        return
    cases = t["cases"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    # panel 1: copula gap ~ 0 across sigma (marginal non-Gaussianity)
    sig = sorted(set(c["sigma"] for c in cases))
    for m, col in zip([3, 5, 8], ["#003f5c", "#bc5090", "#ffa600"]):
        for rho in sorted(set(c["rho"] for c in cases if c["m"] == m)):
            xs = [c["sigma"] for c in cases if c["m"] == m and c["rho"] == rho]
            ys = [c["copula_gap"] for c in cases if c["m"] == m and c["rho"] == rho]
            ax[0].plot(xs, ys, "o-", color=col, alpha=0.5, ms=4)
    ax[0].axhline(0, color="k", lw=0.8)
    ax[0].set_xlabel(r"$\sigma$ (lognormal marginal non-Gaussianity)")
    ax[0].set_ylabel(r"copula gap  $I_{\rm KSG}-I_{\rm Gauss\,copula}$")
    ax[0].set_title("Tier 2: ZERO copula gap despite non-Gaussian marginals")
    # panel 2: Pearson error grows with sigma (the wrong ruler)
    for m, col in zip([3, 5, 8], ["#003f5c", "#bc5090", "#ffa600"]):
        xs, ys = [], []
        for c in sorted([c for c in cases if c["m"] == m], key=lambda c: c["sigma"]):
            xs.append(c["sigma"]); ys.append(c["pearson_rel_error"])
        ax[1].scatter(xs, ys, color=col, s=20, alpha=0.6, label=f"m={m}")
    ax[1].axhline(0, color="k", lw=0.8)
    ax[1].set_xlabel(r"$\sigma$")
    ax[1].set_ylabel(r"Pearson relative error  $(I_{\rm pear}-I_{\rm true})/I_{\rm true}$")
    ax[1].set_title("Field-Pearson ruler is WRONG; rank ruler is right")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig2_tier2_lognormal.png"), dpi=110)
    plt.close(fig)
    print("wrote fig2")


def fig_tier3():
    t = R.get("tier3")
    if not t:
        return
    snaps = t["snapshots"]
    zs = np.array([s["z"] for s in snaps])
    # THE MONEY FIGURE: gap_matched vs separation, colored by redshift.
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    cmap = plt.cm.viridis
    # line templates only for the scale axis
    seps_all = sorted(set(c["separation_mpc"] for s in snaps for c in s["configs"]
                          if c["template"] == "line"))
    for s in snaps:
        z = s["z"]
        col = cmap((3.0 - z) / 3.0)
        pts = [(c["separation_mpc"], c["gap_matched"], c["gap_matched_z"])
               for c in s["configs"] if c["template"] == "line"]
        pts.sort()
        if pts:
            x, y, zz = zip(*pts)
            ax[0].plot(x, y, "o-", color=col, ms=4, alpha=0.85,
                       label=f"z={z:.2f}")
    ax[0].axhline(0, color="k", lw=0.8)
    ax[0].set_xlabel("cell separation (Mpc/h)")
    ax[0].set_ylabel(r"copula gap  $I_{\rm KSG}-I_{\rm KSG}^{\rm surrogate}$ (nats)")
    ax[0].set_title("Tier 3: N-body copula gap vs SCALE and REDSHIFT")
    ax[0].legend(fontsize=7, ncol=2)
    # gap vs z at smallest separation (most nonlinear), one line per ng
    for ng, col in zip([16, 32, 48], ["#003f5c", "#bc5090", "#ffa600"]):
        pts = []
        for s in snaps:
            cs = [c for c in s["configs"] if c["template"] == "line"
                  and c["ng"] == ng]
            if cs:
                c = min(cs, key=lambda c: c["separation_mpc"])
                pts.append((s["z"], c["gap_matched"], c["gap_matched_z"]))
        pts.sort()
        if pts:
            x, y, zz = zip(*pts)
            ax[1].plot(x, y, "o-", color=col, ms=5,
                       label=f"ng={ng} (cell {205/ng:.1f} Mpc)")
    ax[1].axhline(0, color="k", lw=0.8)
    ax[1].set_xlabel("redshift z")
    ax[1].set_ylabel("copula gap at smallest separation (nats)")
    ax[1].set_title("Gap vs redshift (adjacent cells)")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig3_copula_gap_money.png"), dpi=120)
    plt.close(fig)
    print("wrote fig3 (money figure)")


if __name__ == "__main__":
    fig_tier1()
    fig_tier2()
    fig_tier3()
    print("figures done")

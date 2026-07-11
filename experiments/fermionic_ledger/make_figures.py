"""make_figures.py — figures for the fermionic ledger result. Reads the result
JSONs and recomputes the closed-form family curves. Matplotlib only."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fermionic_core import h_nu, LN2
from uniform_family import family_nu, multi_information_family
from fermionic_core import logdet_potential_from_nu

plt.rcParams.update({"figure.dpi": 130, "font.size": 9})


def fig_two_pole():
    """F1 (capped) vs F2 (divergent) vs bosonic (divergent) — the split + cap."""
    s = np.linspace(0, 0.999, 400)
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    for k in (10, 100, 1000):
        IF = np.array([multi_information_family(k, si)[0] for si in s])
        ax[0].plot(s, IF, label=f"k={k}")
    ax[0].axhline(LN2, ls="--", c="k", lw=0.8, label="ln2 (k→∞ cap)")
    ax[0].set_title("F1 fermionic multi-information $I_F$\n(rigidity pole CAPPED by exclusion)")
    ax[0].set_xlabel("collective polarization s = ν₀"); ax[0].set_ylabel("$I_F$ (nats)")
    ax[0].legend(fontsize=7)
    # F2 log-det vs bosonic S
    rho = np.linspace(0, 0.985, 400)
    k = 100
    LF = np.array([logdet_potential_from_nu(family_nu(k, si)) for si in s])
    Sbos = -np.log(1 + rho * (k - 1)) - (k - 1) * np.log(1 - rho)
    ax[1].plot(s, np.clip(LF, 0, 40), label="F2 $-\\ln\\det(I-M^2)$ (fermionic)")
    ax[1].plot(rho, np.clip(Sbos, 0, 40), ls=":", label="bosonic $S=-\\ln\\det C$")
    ax[1].set_ylim(0, 40)
    ax[1].set_title("Both DIVERGE at rigidity\n(the bosonic degeneracy that F1 breaks)")
    ax[1].set_xlabel("s (fermionic) / ρ (bosonic)"); ax[1].set_ylabel("potential")
    ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig("figures/fig1_two_pole_split.png"); plt.close(fig)


def fig_saturation():
    """Kish-analog: dims_removed saturates at μ(s)²=(1-h(s)/ln2)², ≤1."""
    d = json.load(open("uniform_family_results.json"))["S2_saturation"]
    fig, ax = plt.subplots(figsize=(5, 3.6))
    ks = d["klist"]
    for s in d["svals"]:
        cur = d["curves"][f"s={s}"]
        ax.semilogx(ks, cur["dims_removed"], "o-", ms=3, label=f"s={s}")
        mu2 = (1 - float(h_nu(s)) / LN2) ** 2
        ax.axhline(mu2, ls="--", lw=0.7, c=ax.lines[-1].get_color())
    ax.axhline(1.0, ls=":", c="k", lw=0.8, label="exclusion ceiling = 1")
    ax.set_title("Fermionic Kish-analog: dimensions removed by coordination\n"
                 "saturates at μ(s)²=(1−h(s)/ln2)² ≤ 1 (dashed) per collective mode")
    ax.set_xlabel("k (constituents)"); ax.set_ylabel("k − k_eff  (dims removed)")
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout(); fig.savefig("figures/fig2_saturation_law.png"); plt.close(fig)


def fig_bridge():
    d = json.load(open("bridge_results.json"))["kitaev"]
    rows = d["rows"]
    p = [r["p"] for r in rows]
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    I = np.array([r["I_reg"] for r in rows])
    Sc = np.array([r["Scl_Z"] for r in rows])
    Sc = np.clip(Sc, None, np.nanpercentile(Sc[np.isfinite(Sc)], 95))
    ax.plot(p, I / np.nanmax(I), "o-", ms=3, label="fermionic $I_F$ (region), norm")
    ax.plot(p, Sc / np.nanmax(Sc), "s--", ms=3,
            label="classical $S=-\\ln\\det C$ (occupation), norm")
    ax.axvline(2.0, ls=":", c="k", lw=0.8, label="topological transition μ=2t")
    sp = d["spearman"]["Scl_Z"]["vs_I_reg"]
    ax.set_title(f"S4 bridge on the Kitaev chain\nclassical S tracks fermionic $I_F$ at |Spearman|={abs(sp):.2f}")
    ax.set_xlabel("μ (chemical potential)"); ax.set_ylabel("normalized")
    ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig("figures/fig3_kitaev_bridge.png"); plt.close(fig)


def fig_hubbard():
    d = json.load(open("validation_results.json"))["V3_hubbard"]["rows"]
    U = [r["U"] for r in d]
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.plot(U, [r["I_true"] for r in d], "o-", ms=3, label="true multi-information")
    ax.plot(U, [r["I_gaussian"] for r in d], "s--", ms=3, label="Gaussian $I_F$ (one-body cov)")
    ax.plot(U, [r["nongaussian_gap_S"] for r in d], "^:", ms=3, label="non-Gaussian gap $S_F-S_{vN}$")
    ax.set_title("V3 Hubbard (non-Gaussian): the one-body ledger's blind spot\n"
                 "coordination migrates to the higher-order (Mott) sector")
    ax.set_xlabel("U (interaction)"); ax.set_ylabel("nats")
    ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig("figures/fig4_hubbard_blindness.png"); plt.close(fig)


if __name__ == "__main__":
    import os
    os.makedirs("figures", exist_ok=True)
    fig_two_pole(); print("fig1 two-pole/split")
    fig_saturation(); print("fig2 saturation law")
    fig_bridge(); print("fig3 kitaev bridge")
    fig_hubbard(); print("fig4 hubbard blindness")
    print("figures done.")

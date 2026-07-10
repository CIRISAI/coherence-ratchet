"""Figures for the entanglement-ledger test. Reads results.json."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = json.load(open("experiments/entanglement_ledger/results.json"))
FIG = "experiments/entanglement_ledger/figures/"
CAP = 8.0  # visual cap for the rigidity pole (S -> inf)


def capped(vals):
    return [CAP if (v is None) else min(v, CAP) for v in vals]


# ---------------------------------------------------------------------------
# FIG 1 — GHZ blind spot: classical-S swings pole<->vacuum while the quantum
#         entanglement is constant and maximal.
# ---------------------------------------------------------------------------
ghz = D["families"]["GHZ"]
th = np.array(ghz["basis_sweep"]["theta"])
Ssw = np.array([CAP if v is None else min(v, CAP) for v in ghz["basis_sweep"]["S"]])
fig, ax = plt.subplots(figsize=(7, 4.3))
ax.plot(th, Ssw, "-o", ms=3, color="#c0392b", label="classical-S  (our instrument)")
ax.axhline(ghz["quantum"]["S_half"], ls="--", color="#2980b9",
           label=f"quantum S_vN(half) = ln2 = {ghz['quantum']['S_half']:.2f}  (const)")
ax.axhline(ghz["quantum"]["T_total"] / 6, ls=":", color="#27ae60",
           label=f"quantum total-corr / qubit = ln2  (const, maximal)")
ax.annotate("Z basis:\nRIGIDITY POLE\n(S = +inf)", (th[0], CAP),
            xytext=(0.15, 7.0), fontsize=8, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.annotate("X basis:\nVACUUM (S = 0)\nyet maximal GME", (th[-1], 0.0),
            xytext=(1.05, 1.8), fontsize=8, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.set_xlabel("measurement axis theta  (0 = Z basis,  pi/2 = X basis)")
ax.set_ylabel("entropy (nats)")
ax.set_title("GHZ (N=6): classical-S is blind to maximal multipartite entanglement\n"
             "one basis reads a pole, another reads the vacuum; neither reads the interior")
ax.set_ylim(-0.3, CAP + 0.4)
ax.legend(fontsize=8, loc="center right")
fig.tight_layout()
fig.savefig(FIG + "fig1_ghz_blind_spot.png", dpi=140)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 2 — family bars: quantum entanglement present vs classical-S seen.
# ---------------------------------------------------------------------------
fams = ["product", "W", "GHZ", "cluster", "random_Haar"]
Ttot = [D["families"][f]["quantum"]["T_total"] for f in fams]
Qpair = [D["families"][f]["quantum"]["Q_pair"] for f in fams]
# classical-S in the X basis (a MUB, the natural transverse basis); this is
# where GHZ (0) and W (1.05) part ways. Z basis is the pole story (fig 1).
SX = [D["families"][f]["classical_S"]["X"] for f in fams]
SX = [0.0 if v is None else v for v in SX]
x = np.arange(len(fams))
w = 0.27
fig, ax = plt.subplots(figsize=(7.5, 4.3))
ax.bar(x - w, Ttot, w, label="quantum total correlation  (all orders)", color="#27ae60")
ax.bar(x, Qpair, w, label="quantum pairwise MI  sum I(i:j)", color="#2980b9")
ax.bar(x + w, SX, w, label="classical-S  (X basis, a MUB)", color="#c0392b")
ax.set_xticks(x)
ax.set_xticklabels(fams)
ax.set_ylabel("entropy (nats)")
ax.set_title("Classical-S sees pairwise entanglement, is blind to multipartite\n"
             "GHZ / cluster / random: maximal T, classical-S(X) ~ 0;  W (bipartite): seen")
ax.legend(fontsize=8)
for xi, f in enumerate(fams):
    if D["families"][f]["classical_S"]["Z_is_pole"]:
        ax.text(xi + w, SX[xi] + 0.15, "Z=pole", ha="center", fontsize=6, color="#c0392b")
fig.tight_layout()
fig.savefig(FIG + "fig2_family_bars.png", dpi=140)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 3 — TFIM: the two corridors overlaid, broken vs symmetric sector.
# ---------------------------------------------------------------------------
g = np.array(D["tfim"]["g"])
brk = D["tfim"]["broken"]
sym = D["tfim"]["symmetric"]


def norm(v):
    v = np.array([np.nan if x is None else x for x in v], float)
    m = np.nanmax(v)
    return v / m if m and m > 0 else v


fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
# broken sector (physical criticality corridor)
ax = axs[0]
ax.plot(g, norm(brk["S_half"]), "-", color="#2980b9", lw=2, label="quantum S_vN(half)")
ax.plot(g, norm(brk["Q_pair"]), "--", color="#16a085", lw=1.6, label="quantum pairwise MI")
ax.plot(g, norm(brk["classical_S_Z"]), "-o", ms=3, color="#c0392b",
        label="classical-S (Z basis)")
ax.axvline(1.0, ls=":", color="k", alpha=0.5)
ax.set_title("SYMMETRY-BROKEN sector (physical)\nCONVERGENT: both corridors peak at g=1")
ax.set_xlabel("transverse field g")
ax.set_ylabel("normalised to own max")
ax.legend(fontsize=8)
ax.text(1.02, 0.05, "criticality g=1", fontsize=7, rotation=90)
# symmetric sector (cat-dominated)
ax = axs[1]
ax.plot(g, norm(sym["S_half"]), "-", color="#2980b9", lw=2, label="quantum S_vN(half)")
ax.plot(g, norm(capped(sym["classical_S_Z"])), "-o", ms=3, color="#c0392b",
        label="classical-S (Z basis, capped)")
ax.plot(g, norm(sym["zz_order"]), ":", color="#8e44ad", lw=1.8,
        label="classical order param <Z0 Z_{N-1}>")
ax.axvline(1.0, ls=":", color="k", alpha=0.5)
ax.set_title("Z2-SYMMETRIC sector (GHZ cat)\nclassical-S tracks the ORDER PARAMETER, monotone")
ax.set_xlabel("transverse field g")
ax.legend(fontsize=8)
fig.suptitle("TFIM (N=10) across the quantum phase transition: physics vs bookkeeping "
             "is sector- and basis-dependent", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(FIG + "fig3_tfim_corridors.png", dpi=140)
plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 4 — classical-S basis x coupling surface (broken sector), entanglement
#         peak marked.
# ---------------------------------------------------------------------------
theta = np.array(D["tfim"]["theta"])
surf = np.array([[np.nan if v is None else min(v, CAP) for v in row]
                 for row in brk["S_surface"]])
fig, ax = plt.subplots(figsize=(7.5, 4.6))
im = ax.pcolormesh(g, theta, surf.T, shading="auto", cmap="viridis")
fig.colorbar(im, ax=ax, label="classical-S  (capped at %.0f)" % CAP)
# overlay: per-g argmax basis, and the quantum entanglement peak
Shalf = np.array([np.nan if x is None else x for x in brk["S_half"]], float)
gpeak = g[np.nanargmax(Shalf)]
ax.axvline(gpeak, color="w", ls="--", lw=1.5)
ax.text(gpeak + 0.02, 0.1, "quantum S_vN(half) peak", color="w", fontsize=8, rotation=90)
ax.set_xlabel("transverse field g")
ax.set_ylabel("measurement axis theta (0=Z, pi/2=X)")
ax.set_title("classical-S over (basis, coupling), TFIM broken sector\n"
             "a ridge of classical-S coincides with the quantum entanglement peak")
fig.tight_layout()
fig.savefig(FIG + "fig4_basis_coupling_surface.png", dpi=140)
plt.close(fig)

print("wrote 4 figures to", FIG)

"""
Extension — the corridor shape observable at the particle-physics rung.
=======================================================================

The framework's shape observable is substrate-agnostic: any distribution over
constituents has a participation ratio k_eff = 1/Σpᵢ² and a Kish correlation
ρ = (N/k_eff − 1)/(N−1). At the CMB it was the 2ℓ+1 mode powers. Here it is
particle decay-channel branching fractions.

Claim 4 (fractal recurrence) asserts the corridor recurs at every coordinated
rung. This TESTS it at the particle rung; it does not assume it.

CONFOUND, found on the first run and controlled here. The raw branching-
fraction count is wildly heterogeneous — B⁺ has 249 tabulated decay modes, Ξ⁻
has 5 — and k_eff inflates with the channel count, so a raw ρ measures how
COMPLETELY the decay table has been MEASURED, not a physical property. Control:
compute ρ on a FIXED number of top channels per particle (N_FIX), so every
particle's ρ is the concentration of its decay among its N_FIX leading modes —
a fair, completeness-independent comparison.

Honest outcome space: at fixed N, particle decay concentration clusters in a
bounded ρ band (corridor recurs), piles at a pole (it does not), or splits by
class. There is no clean isotropic baseline here as there was for the CMB, so
this is a corridor-EXISTENCE test, not a drift test.

Data: PDG 2025 (`pdg` package), level-0 exclusive modes, inclusive modes and
upper limits dropped.
"""
import numpy as np
import pdg

api = pdg.connect()
INCLUSIVE = (">=0", "≥0", "anything", "(particles)", " X ", "neutrals")
N_FIX = 6                                    # fixed channel count


def kish(p):
    p = np.asarray(p, float)
    p = p / p.sum()
    N = len(p)
    k_eff = 1.0 / np.sum(p ** 2)
    rho = (N / k_eff - 1.0) / (N - 1.0)
    return k_eff, rho


def decay_values(name):
    p = api.get_particle_by_name(name)
    vals = []
    for b in p.exclusive_branching_fractions():
        if getattr(b, "subdecay_level", 1) != 0 or getattr(b, "is_limit", True):
            continue
        v = b.value
        if v is None or v <= 0:
            continue
        if any(tok in (b.description or "") for tok in INCLUSIVE):
            continue
        vals.append(v)
    return sorted(vals, reverse=True)


PARTICLES = [
    "tau-", "rho(770)0", "omega(782)", "phi(1020)", "K+", "K(S)0", "K(L)0",
    "D0", "D+", "D_s+", "B+", "B0", "B_s0", "J/psi(1S)", "psi(2S)",
    "Upsilon(1S)", "Sigma+", "Omega-", "Lambda_c+", "W+", "Z", "H0",
    "Delta(1232)++", "n", "Sigma(1385)+", "chi_c0(1P)", "Upsilon(4S)",
]

print("=" * 78)
print(f"Particle-physics corridor: decay concentration at fixed N = {N_FIX}")
print("=" * 78)
print(f"  {'particle':<16}{'k_eff':>8}{'rho':>9}{'top BF':>9}   regime")
rows = []
for name in PARTICLES:
    try:
        d = decay_values(name)
        if len(d) < N_FIX:
            continue
        top = d[:N_FIX]
        k_eff, rho = kish(top)
        regime = ("rigidity" if rho > 0.55 else
                  "chaos" if rho < 0.12 else "corridor")
        rows.append((name, k_eff, rho, regime))
        print(f"  {name:<16}{k_eff:>8.2f}{rho:>9.3f}{top[0]/sum(top):>9.3f}"
              f"   {regime}")
    except Exception:
        pass

print()
print("  flavour-mixing rows (|V_ij|^2, exact unitary distributions, N=3):")
MIX = {
    "CKM u-row": [0.97435, 0.22501, 0.003732],
    "CKM c-row": [0.22487, 0.97349, 0.04183],
    "CKM t-row": [0.00858, 0.04111, 0.999118],
    "PMNS e-row": [0.681, 0.297, 0.022],
    "PMNS mu-row": [0.114, 0.359, 0.527],
    "PMNS tau-row": [0.205, 0.344, 0.451],
}
mix = []
for label, V in MIX.items():
    k_eff, rho = kish(np.array(V) ** 2)
    mix.append((label, rho))
    print(f"  {label:<16}{k_eff:>8.2f}{rho:>9.3f}")

print()
print("=" * 78)
print("READING")
print("=" * 78)
rho_all = [r[2] for r in rows]
nr = sum(r[3] == "rigidity" for r in rows)
nc = sum(r[3] == "corridor" for r in rows)
nx = sum(r[3] == "chaos" for r in rows)
print(f"  {len(rows)} particles with >= {N_FIX} clean decay channels, "
      f"rho on the top {N_FIX}:")
print(f"  rho range [{min(rho_all):.3f}, {max(rho_all):.3f}], "
      f"median {np.median(rho_all):.3f}, mean {np.mean(rho_all):.3f}, "
      f"std {np.std(rho_all):.3f}.")
print(f"  regime split: rigidity {nr}, corridor {nc}, chaos {nx}.")
ckm = np.mean([r for l, r in mix if l.startswith("CKM")])
pmns = np.mean([r for l, r in mix if l.startswith("PMNS")])
print(f"  mixing: CKM rows mean rho {ckm:.2f}, PMNS rows mean rho {pmns:.2f}.")
print()
print("  Verdict — read off the numbers above, not assumed:")
if nr > 0.6 * len(rows):
    print("  decay concentration piles at the rigidity pole -- the corridor")
    print("  does NOT recur cleanly at the particle-decay rung.")
elif nc > 0.6 * len(rows) and np.std(rho_all) < 0.20:
    print("  decay concentration clusters in a bounded interior band -- the")
    print("  corridor recurs at the particle-decay rung.")
else:
    print("  decay concentration is SPREAD across the full range, no tight")
    print("  cluster -- the corridor does not recur as a tight band here; what")
    print("  the particle-decay rung shows is a broad distribution, not an")
    print("  attractor band. (Unlike the CMB shape sector, there is no clean")
    print("  isotropic baseline to define the band against.)")
print()
print("  CKM rows sit at rigidity (quarks barely mix); PMNS rows sit lower")
print("  (neutrinos mix strongly) -- two clusters, the known quark/neutrino")
print("  mixing contrast restated as rho. Not itself a corridor.")

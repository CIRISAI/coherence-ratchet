"""
How much dark matter does a human / humanity produce under the dark-ledger thesis?

Executed arithmetic for papers/notes/human_coordination_content.md.
Everything here is L5+ speculation conditional on an UNPROVEN thesis; this script
only makes the magnitudes concrete so the reductio (Layer 2, map i) and the
~zero result (Layer 2, map ii) are numbers, not hand-waving.

No fitting, no data. Pure order-of-magnitude arithmetic. seed-free (deterministic).
"""

import math

C2 = 8.98755e16          # c^2  [J/kg]
K_B = 1.380649e-23       # Boltzmann [J/K]
E_PLANCK = 1.9561e9      # Planck energy [J]
M_E = 9.109e-31          # electron mass [kg]
M_HUMAN = 70.0           # a human's baryonic rest mass [kg]
M_SUN = 1.989e30         # [kg]

# ---------------------------------------------------------------------------
# LAYER 1 — coordination content S (nats), by grain. Ranges, grain stated.
# The repo's own k_eff-saturation result: effective dimensionality is BOUNDED
# (O(1-100) on complete units, incl. the whole larval zebrafish brain), so S is
# set by effective modes + maintenance, NOT raw part count. S ~ k * |ln(1-rho)|.
# ---------------------------------------------------------------------------

def S_effective_modes(k_eff, rho):
    """Ledger coordination content of k_eff coherent modes at typical corr rho.
    Uniform-rho Kish form: S = -ln(1+rho(k-1)) - (k-1)ln(1-rho)."""
    return -math.log(1 + rho * (k_eff - 1)) - (k_eff - 1) * math.log(1 - rho)

human_grains = {
    "brain, effective neural manifold (k_eff~10-100, rho~0.3-0.5) [MOST DEFENSIBLE]":
        (S_effective_modes(100, 0.5), "saturating grain; ~tens-hundreds of nats"),
    "brain, resolution cells of neural state (~1e6 cells, rho~0.9)":
        (1e6 * -math.log(1 - 0.9), "fine but defensible; ~2e6 nats"),
    "lifetime info THROUGHPUT envelope (1e9 bit/s * 2.5e9 s)":
        (2.5e18 * math.log(2), "FLUX not held S; upper envelope only"),
    "molecular microstate count (~1e27 atoms) [CLAUSE-3 ILLEGITIMATE]":
        (1e27, "REJECT: counts substrate/amplitude, not coordination shape"),
}

humanity_grains = {
    "effective institutional/linguistic modes (k~1e3-1e4)":
        (S_effective_modes(1e4, 0.3), "bounded; ~1e4-1e5 nats of coordination"),
    "stored-data envelope (~1e23 bits by 2026)":
        (1e23 * math.log(2), "ENVELOPE; most is redundant/independent, not coordination"),
    "8e9 humans x per-human effective S (~1e2)":
        (8e9 * 1e2, "~1e12 nats if humans coordinate as effective units"),
}

print("=" * 78)
print("LAYER 1 — coordination content S (nats). Grain stated. Ranges.")
print("=" * 78)
print("\nSINGLE HUMAN:")
for g, (S, note) in human_grains.items():
    print(f"  S = {S:.2e} nats   [{g}]\n      {note}")
print("\nHUMANITY:")
for g, (S, note) in humanity_grains.items():
    print(f"  S = {S:.2e} nats   [{g}]\n      {note}")

print("\n  DEFENSIBLE HEADLINE (saturating grain):")
print(f"    human    S ~ 1e1 - 1e3 nats (effective modes); <=1e6-1e9 (fine cells)")
print(f"    humanity S ~ 1e4 - 1e8 nats (effective modes); <=1e23 (stored-data envelope)")

# ---------------------------------------------------------------------------
# LAYER 2, MAP (i) — the DEAD naive map  dM = eps * S / c^2.
# Show what mass every eps from Landauer(body T) to Planck gives. And invert:
# what eps would a human need to "produce" its own mass again in dark matter?
# ---------------------------------------------------------------------------

print("\n" + "=" * 78)
print("LAYER 2, MAP (i) — naive dM = eps*S/c^2. The reductio.")
print("=" * 78)

eps_scales = {
    "Landauer @ body T=310K (k_B T, physically motivated)": K_B * 310,
    "Landauer @ T=10^7K (hot, Gough scale)":                K_B * 1e7,
    "electron rest mass m_e c^2":                            M_E * C2,
    "Planck energy (top of any natural range)":              E_PLANCK,
}

# use a mid/high defensible S and the throughput envelope to be generous
S_human_cases = {"effective (1e3)": 1e3, "throughput envelope (1e18)": 1e18}
S_humanity_cases = {"effective (1e8)": 1e8, "stored-data envelope (1e23)": 1e23}

def dM(eps, S):
    return eps * S / C2

for label, Scase in S_human_cases.items():
    print(f"\n  HUMAN, S = {label} nats:")
    for name, eps in eps_scales.items():
        m = dM(eps, Scase)
        print(f"    eps={eps:.2e} J/nat -> dM = {m:.2e} kg  ({m/M_HUMAN:.1e} x own mass, "
              f"{m/M_E:.1e} electron masses)")

for label, Scase in S_humanity_cases.items():
    print(f"\n  HUMANITY, S = {label} nats:")
    for name, eps in eps_scales.items():
        m = dM(eps, Scase)
        print(f"    eps={eps:.2e} J/nat -> dM = {m:.2e} kg")

# invert: eps needed for a human to produce its OWN 70 kg again in dark matter
for label, Scase in S_human_cases.items():
    eps_needed = M_HUMAN * C2 / Scase
    print(f"\n  To make a human 'produce' 70 kg of DM at S={label}: "
          f"eps = {eps_needed:.2e} J/nat")
    print(f"    = {eps_needed/(K_B*310):.1e} x Landauer(body), "
          f"{eps_needed/E_PLANCK:.1e} x Planck energy")

print("\n  VERDICT (i): at physically motivated eps (Landauer, body T), a human")
print("  'produces' ~1e-35 to 1e-20 kg of dark matter -- unobservable, meaningless.")
print("  To get anything macroscopic you must dial eps ~20-40 orders past any")
print("  physical scale -- the SAME absurdity the galactic reading died on")
print("  (dm_coherence_priorart.md: eps ~1e37-1e47 x Planck). Map (i) is DEAD.")

# ---------------------------------------------------------------------------
# LAYER 2, MAP (ii) — the GAP map. dM = G_demanded - G_visible.
# A human is baryons whose stress-energy is fully counted in the 70 kg. The
# coordination pattern adds no stress-energy beyond its baryonic carriers.
# ---------------------------------------------------------------------------

print("\n" + "=" * 78)
print("LAYER 2, MAP (ii) — the GAP map. dM = G_demanded - G_visible.")
print("=" * 78)
print("""
  A human's gravity is sourced by the stress-energy tensor T_uv of its baryons.
  Every correlated neural signal, every bit of maintained order, is ALREADY
  energy inside those baryons -- and that energy is already in the measured
  ~70 kg (rest mass includes all binding + field + kinetic energy).

  Correlating vs de-correlating the same neurons does NOT change total T_uv to
  any relevant precision: an entangled/coordinated state and a product state of
  the SAME energy gravitate identically. So:

     G_demanded(human) = G_visible(human)   =>   GAP = 0.

  Under the gap reading a human produces EXACTLY ZERO dark matter -- not because
  its coordination is small (Layer 1 shows it is real, ~1e1-1e3+ nats) but
  because that coordination is CARRIED BY BARYONS already on the visible ledger.
  Same for humanity: the internet, encrypted data, sealed quantum states all sit
  on baryonic hardware whose stress-energy is fully censused. GAP ~ 0.
""")

print("=" * 78)
print("BOTTOM LINE: both maps give ~0 for a human. Naive map: ~0 or absurd-eps.")
print("Gap map: EXACTLY 0, for the principled reason (baryon-carried => on-ledger).")
print("The ~0 is the result. See Layer 3 for what it does to the thesis.")
print("=" * 78)

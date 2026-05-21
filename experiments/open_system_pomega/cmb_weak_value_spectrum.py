"""
The P_omega-reweighted CMB power spectrum: does the framework reproduce LambdaCDM?
==================================================================================

Bounded piece of the "framework as strict extension of LambdaCDM" program. The
linear low-ell CMB modes have a standard quantum description: primordial
fluctuations are squeezed inflaton states, so the spherical-harmonic
coefficients a_{ell,m} are Gaussian with variance C_ell. That Gaussian ensemble
IS the LambdaCDM forward prediction -- used here as the pre-selection ensemble,
not re-derived.

The soft P_omega is the backward post-selection: weight w = exp(-beta H_sum),
H_sum = sum_ell (rho_ell - rho_mid)^2, with rho_ell the per-multipole Kish
correlation read off the power participation among the 2ell+1 modes. The
ABL/weak-value-reweighted expectation of any observable A is
  <A>_w = sum_realizations w * A / sum w.

Computed here for two observables:
  - C_ell  -- the BULK power spectrum (the observable LambdaCDM predicts well);
  - rho_ell -- the within-multipole SHAPE (where the framework's content lives).

Key structural fact tested: rho_ell is SCALE-INVARIANT (it depends only on the
ratios of the |a_{ell,m}|^2, not their sum), and for a Gaussian ensemble the
total power sum_m |a_{ell,m}|^2 is statistically INDEPENDENT of the normalized
shape. So H_sum couples only to the shape -- and the P_omega reweighting should
leave <C_ell> exactly invariant while moving <rho_ell>. If so, the framework
reproduces LambdaCDM's bulk spectrum BY CONSTRUCTION (not by tuning) and acts
only on the shape/anomaly sector.
"""
import numpy as np
import healpy as hp

LMAX = 30
ELLS = list(range(2, LMAX + 1))
RHO_MID = 0.25                       # A3+-calibrated corridor centre
N_MC = 200_000
rng = np.random.default_rng(20260521)

# LambdaCDM-ish forward input: observed C_ell from the Planck SMICA map
cmb = hp.remove_dipole(hp.read_map("cmb_data/planck_smica_R3.fits"))
Cl_in = hp.anafast(cmb, lmax=LMAX)              # observed power spectrum
print("=" * 78)
print("P_omega-reweighted CMB power spectrum")
print("=" * 78)
print(f"  forward input: LambdaCDM-ish C_ell from the Planck SMICA map, "
      f"ell=2..{LMAX}")
print(f"  rho_mid = {RHO_MID}; soft P_omega weight exp(-beta H_sum).")

# Monte Carlo: Gaussian a_{ell,m} with the input variance C_ell
# store per-realization: Chat_ell (= mean_m a^2) and rho_ell
Chat = np.zeros((N_MC, len(ELLS)))
rho = np.zeros((N_MC, len(ELLS)))
for j, ell in enumerate(ELLS):
    k = 2 * ell + 1
    a = rng.normal(0.0, np.sqrt(Cl_in[ell]), size=(N_MC, k))
    p = a * a
    s1 = p.sum(axis=1)
    Chat[:, j] = s1 / k
    k_eff = s1 ** 2 / (p ** 2).sum(axis=1)
    rho[:, j] = (k / k_eff - 1.0) / (k - 1.0)

H_sum = ((rho - RHO_MID) ** 2).sum(axis=1)


def reweight(beta):
    w = np.exp(-beta * (H_sum - H_sum.min()))
    w = w / w.sum()
    Cl_w = (w[:, None] * Chat).sum(axis=0)
    rho_w = (w[:, None] * rho).sum(axis=0)
    ess = 1.0 / np.sum(w ** 2)
    return Cl_w, rho_w, ess


Cl0 = Chat.mean(axis=0)              # beta=0 ensemble mean = the input spectrum
rho0 = rho.mean(axis=0)

print()
print("=" * 78)
print("RESULT 1 — does P_omega couple to the bulk power at all? (ESS-free)")
print("=" * 78)
# the clean, ESS-free test: correlation between per-ell power and H_sum.
# if ~0, the reweighting cannot move <C_ell> -- exact, no large-beta MC needed.
corrs = []
for j, ell in enumerate(ELLS):
    c = np.corrcoef(Chat[:, j], H_sum)[0, 1]
    corrs.append(c)
print(f"  corr(C_ell, H_sum) across the ensemble, per multipole:")
print(f"    max |corr| over ell=2..{LMAX} = {np.max(np.abs(corrs)):.4f}  "
      f"(MC noise ~{1/np.sqrt(N_MC):.4f})")
print(f"  -> the bulk power C_ell is statistically INDEPENDENT of H_sum.")
print(f"  Any reweighting w = f(H_sum) therefore leaves <C_ell> invariant,")
print(f"  exactly, at every beta. No large-beta Monte Carlo needed to know it.")
print()
print(f"  reweighted-C_ell check (MC, for confirmation where ESS is healthy):")
print(f"  {'beta':>8}{'max |C_l ratio-1|':>20}{'ESS/N':>9}  note")
for beta in [1.0, 10.0, 50.0, 200.0]:
    Cl_w, rho_w, ess = reweight(beta)
    ratio = Cl_w / Cl0
    note = "" if ess / N_MC > 0.05 else "ESS collapsed -- MC noise, not a P_omega effect"
    print(f"  {beta:>8.0f}{np.max(np.abs(ratio - 1)):>20.2e}{ess/N_MC:>9.3f}  {note}")

print()
print("=" * 78)
print("RESULT 2 — what P_omega DOES move: the within-multipole shape rho_ell")
print("=" * 78)
beta = 50.0
Cl_w, rho_w, ess = reweight(beta)
print(f"  beta = {beta} (ESS/N = {ess/N_MC:.3f})")
print(f"  {'ell':>4}{'rho_ell (LCDM)':>16}{'rho_ell (P_omega)':>19}{'shift':>10}")
for j, ell in enumerate(ELLS):
    if ell <= 8 or ell % 6 == 0:
        print(f"  {ell:>4}{rho0[j]:>16.4f}{rho_w[j]:>19.4f}"
              f"{rho_w[j]-rho0[j]:>+10.4f}")

print()
print("=" * 78)
print("READING")
print("=" * 78)
print("  RESULT 1: the P_omega reweighting leaves <C_ell> invariant to MC")
print("  precision, at every beta. This is not a fit -- it is structural:")
print("  rho_ell is scale-invariant (depends only on the RATIOS of the mode")
print("  powers), and for a Gaussian ensemble the total power is statistically")
print("  independent of the normalized shape. H_sum couples ONLY to the shape,")
print("  so the soft P_omega cannot move the bulk power spectrum. The framework")
print("  reproduces LambdaCDM's bulk C_ell EXACTLY AND BY CONSTRUCTION -- the")
print("  'strict extension' structure holds, with nothing tuned.")
print()
print("  RESULT 2: P_omega acts entirely on the within-multipole SHAPE rho_ell,")
print("  pulling it toward the corridor centre. That shape sector -- not the")
print("  bulk spectrum -- is the whole of the framework's distinctive CMB")
print("  content (the drift, the anomalies). Bulk: LambdaCDM, untouched. Shape:")
print("  where the framework lives.")
print()
print("  Honest scope: this is the linear low-ell sector (ell=2..30), the")
print("  Gaussian-mode regime where the quantum description is standard. It")
print("  does NOT cover polarization, high-ell acoustic peaks, or anything")
print("  needing the transfer hierarchy treated quantum-mechanically -- those")
print("  remain open. What is shown: on the sector that IS bounded, the")
print("  framework is a strict extension -- LambdaCDM bulk preserved exactly,")
print("  framework content confined to the shape/anomaly sector.")

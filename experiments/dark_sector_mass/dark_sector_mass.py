#!/usr/bin/env python3
"""
Dark-sector mass from the DE scale via the fermionic coordination ledger.

NEUTRAL DISCOVERY MODE. Question: does the coherence-ratchet dark-sector synthesis
predict a dark-matter particle mass, by linking the dark-energy density rho_Lambda
to the fermionic phase-space (Tremaine-Gunn) floor Q_max(m) ~ m^4?

Every line labels DERIVATION vs ASSUMPTION vs STANDARD-PHYSICS (fetched, cited).
No fit, no synthetic data. All arithmetic shown; results -> results.json.
"""
import json
import math

# ----------------------------------------------------------------------------
# 0. Constants (SI + natural units). Natural units: hbar = c = 1, everything eV.
# ----------------------------------------------------------------------------
hbar_c_eV_m = 1.9732698e-7      # eV * m   (hbar c = 197.327 MeV fm)
c_m_s       = 2.99792458e8      # m/s
eV_per_J    = 1.0 / 1.602176634e-19
pc_m        = 3.0856775814913673e16   # m
Msun_kg     = 1.98892e30        # kg
G_SI        = 6.67430e-11       # m^3 kg^-1 s^-2
kB_J_K      = 1.380649e-23

# conversions to natural units (eV)
inv_m_in_eV = hbar_c_eV_m               # 1 m^-1 = hbar_c eV  -> actually 1/m = hbar_c_eV_m eV
m_in_inv_eV = 1.0 / hbar_c_eV_m         # 1 m   = (1/hbar_c) eV^-1
# mass: 1 kg c^2 in eV
def kg_to_eV(mkg):  # rest energy in eV
    return mkg * c_m_s**2 * eV_per_J

Msun_eV = kg_to_eV(Msun_kg)             # solar rest energy in eV
pc_inv_eV = pc_m * m_in_inv_eV          # 1 pc in eV^-1
M_Pl_reduced_eV = 2.435323e27           # reduced Planck mass, eV

notes = {}

# ----------------------------------------------------------------------------
# 1. STANDARD PHYSICS (fetched / textbook, flagged not-rederived where noted)
# ----------------------------------------------------------------------------
# 1a. Dark-energy density. Planck 2018: Omega_L=0.6847, h=0.6736.
h_hubble   = 0.6736
Omega_L    = 0.6847
# rho_crit = 1.05371e4 * h^2 eV/cm^3  (standard; = 1.05371e-5 h^2 GeV cm^-3)
rho_crit_eV_cm3 = 1.05371e4 * h_hubble**2
rho_L_eV_cm3    = Omega_L * rho_crit_eV_cm3
# eV/cm^3 -> eV^4 : 1 cm = 1e-2 m ; 1 cm^-1 in eV = 1e-2 / hbar_c? careful:
# 1 cm = 1e-2 m = 1e-2 * m_in_inv_eV eV^-1 ; cm^3 = (that)^3 eV^-3
cm_inv_eV = 1e-2 * m_in_inv_eV          # 1 cm in eV^-1
eVcm3_to_eV4 = 1.0 / cm_inv_eV**3       # (eV / cm^3) -> eV^4
rho_L_eV4  = rho_L_eV_cm3 * eVcm3_to_eV4
rho_L_qtr_meV = (rho_L_eV4**0.25) * 1e3
notes['rho_Lambda'] = "STANDARD (Planck2018 Omega_L,h). rho_L^(1/4) reproduces the textbook 2.24 meV."

# 1b. Tremaine-Gunn / fermionic phase-space floor.
# Fine-grained max phase-space density (number) f<=g/(2 pi hbar)^3, g=2 (spin-1/2).
# Coarse-grained MASS phase-space density Q = rho/sigma^3 (obs definition).
# Primitive fermionic max, common convention (Boyarsky+2009, Tremaine-Gunn):
#     Q_max = g * m^4 / [ (2 pi)^(3/2) hbar^3 ]     (mass / (length^3 velocity^3))
# In natural units (hbar=1, velocity dimensionless) Q has dimension eV^4, same as m^4.
g_dof = 2.0
def Qmax_of_m(m_eV):
    """fermionic max coarse-grained mass phase-space density, natural units eV^4,
    for velocity measured in units of c (dimensionless). STANDARD form."""
    return g_dof * m_eV**4 / (2.0*math.pi)**1.5
notes['Qmax_form'] = ("STANDARD: Q_max = g m^4 / (2 pi)^{3/2} (natural units, sigma in c). "
                      "O(1) convention-dependent coefficient; flagged, does not move the verdict.")

# 1c. Dwarf-spheroidal observed phase-space density (classic TG anchors).
# Segue-1-like: rho ~ 0.1 Msun/pc^3 core, sigma ~ 4 km/s (compact, DM-dominated).
# Also a classical dSph: rho ~ 0.02 Msun/pc^3, sigma ~ 10 km/s.
def Q_obs_natural(rho_Msun_pc3, sigma_km_s):
    rho_eV4 = rho_Msun_pc3 * Msun_eV / pc_inv_eV**3      # mass density -> eV^4
    sigma_dimless = (sigma_km_s*1e3) / c_m_s             # v/c
    return rho_eV4 / sigma_dimless**3, rho_eV4, sigma_dimless

dwarfs = {
    'Segue1_like': dict(rho_Msun_pc3=0.1,  sigma_km_s=4.0),
    'classical_dSph': dict(rho_Msun_pc3=0.02, sigma_km_s=10.0),
}
tg_bounds = {}
for name, d in dwarfs.items():
    Qobs, rho_eV4, sig = Q_obs_natural(**d)
    # TG bound: Q_obs <= Q_max = g m^4/(2pi)^{3/2}  ->  m >= (Q_obs (2pi)^{3/2}/g)^{1/4}
    m_lb_eV = (Qobs * (2*math.pi)**1.5 / g_dof)**0.25
    tg_bounds[name] = dict(Q_obs_eV4=Qobs, rho_eV4=rho_eV4, sigma_over_c=sig,
                           m_lower_bound_eV=m_lb_eV)
notes['TG_bound'] = ("STANDARD (reproduces literature m>~100-400 eV, Boyarsky2009/DiPaolo2017 "
                     "robust model-independent bound m>~100 eV from Segue-1/Willman-1).")

# allowed window for warm/fermionic DM to BE the dark matter:
# lower: TG phase-space ~ 0.1-0.4 keV; upper: Lyman-alpha structure formation ~ few-10 keV.
window_keV = (0.3, 10.0)
notes['window'] = "STANDARD: [~0.3, ~10] keV (TG lower / Lyman-alpha upper). Fetched, not rederived."

# ----------------------------------------------------------------------------
# 2. THE LEDGER LINK -- the load-bearing, currently-underived step.
#    Enumerate candidate links. For EACH: predicted m + REQUIRED ASSUMPTION.
#
#    Ledger facts available (from the framework):
#      - DE leg (DERIVED-within-framework, but normalization UNDETERMINED):
#            rho_DE = kappa * S,  S dimensionless (-ln det C), kappa = free eV^4 constant.
#            [lambda_maintenance_wz.md 7(a): kappa is fixed by hand to reproduce w=-1;
#             NOTHING in the ledger sets its scale.]
#      - Fermionic exclusion (DERIVED tonight): rigidity cap = ln2 per collective mode
#            (dimensionless); dims removed <= 1 per mode (dimensionless).
#      - Corridor: rho in (0.1,0.43), k_eff ceiling ~10 (all DIMENSIONLESS).
#    KEY OBSERVATION (derivation): EVERY quantity the ledger emits is dimensionless.
#    A mass requires an external dimensionful anchor. rho_Lambda and Q_max(m) and m^4
#    are ALL eV^4 in natural units, so any bridge between them is a pure DIMENSIONLESS
#    ratio -- which the ledger must supply. Does it? Test each candidate.
# ----------------------------------------------------------------------------
ln2 = math.log(2.0)
links = {}

# --- Candidate (c1): naive dimensional / scale match  rho_Lambda ~ Q_max(m) ---
# ASSUMPTION: identify the DE energy density with the fermionic phase-space floor
#   directly, treating both as the same eV^4 object, bridge factor = O(1) (or =g/(2pi)^{3/2}).
m_c1 = (rho_L_eV4 * (2*math.pi)**1.5 / g_dof)**0.25   # solve rho_L = Qmax(m)
links['c1_naive_dimensional'] = dict(
    m_eV=m_c1, m_keV=m_c1/1e3,
    assumption="rho_Lambda = Q_max(m) as raw eV^4 objects (bridge O(1)). "
               "No velocity/entropy scale inserted.",
    derivable=False,
    verdict_window="OUTSIDE (predicts meV, ~6 orders below keV)",
    note="This IS the known DE<->neutrino-mass meV coincidence (rho_L^1/4 ~ m_nu scale). "
         "Not new ledger content.")

# --- Candidate (a): rho_Lambda = (ln2 per mode)*(energy per mode)*(mode number density) ---
# maintenance reading: DE density = entropy-cap per mode * energy/mode * n_modes.
# The mode number density set by the fermionic degeneracy floor requires a Fermi momentum
# p_F, i.e. a velocity scale. REQUIRED ASSUMPTION: an energy-per-mode E_mode.
# Sub-case (a-i): E_mode = de Sitter/Hubble temperature T_dS = H0/2pi.
H0_eV = h_hubble * 100e3 / (1e6*pc_m) * m_in_inv_eV**0 * (hbar_c_eV_m/ (c_m_s))  # placeholder
# do it cleanly: H0 [1/s] -> eV : H0_s = h*100 km/s/Mpc
H0_s = h_hubble*100e3/(1e6*pc_m)          # 1/s
H0_eV = H0_s * (hbar_c_eV_m / c_m_s)      # hbar H0 in eV : hbar[eV s]=hbar_c/c
T_dS_eV = H0_eV/(2*math.pi)
# rho_L = ln2 * T_dS * n  -> n = rho_L/(ln2 T_dS); degenerate fermion n=g pF^3/6pi^2 -> pF ~ m
n_ai = rho_L_eV4/(ln2*T_dS_eV)            # eV^3
pF_ai = (6*math.pi**2 * n_ai/g_dof)**(1.0/3.0)
links['a_i_maint_TdS'] = dict(
    m_eV=pF_ai, m_keV=pF_ai/1e3,
    assumption="E_mode = de Sitter temperature H0/2pi (INSERTED scale); "
               "mode density = degenerate fermion; identify Fermi momentum with m.",
    derivable=False,
    verdict_window="OUTSIDE (predicts ~%.1e eV)"%pF_ai)

# Sub-case (a-ii): E_mode = m itself -> rho_L = ln2 * m * n = ln2 * rho_DM (m cancels!)
rho_DM_eV4 = (0.2645/Omega_L)*rho_L_eV4   # Omega_c=0.2645
links['a_ii_maint_Em_equals_m'] = dict(
    m_eV=None, m_keV=None,
    assumption="E_mode = m: then rho_L = ln2 * n * m = ln2 * rho_DM. m CANCELS.",
    derivable=False,
    predicts_mass=False,
    check_ratio="rho_L/(ln2*rho_DM) = %.3f (should be 1 if link held; observed ratio of "
                "rho_L to ln2*rho_DM)"%(rho_L_eV4/(ln2*rho_DM_eV4)),
    verdict_window="NO MASS PREDICTED (m cancels); and the density identity misses by the ratio above")

# --- Candidate (b): (ln2/mode)*(DM number density) as an energy density ---
# rho_Lambda = ln2 * n_DM * E?  identical structure to (a): needs E per mode. If E=m, same as a-ii.
links['b_lnn2_times_nDM'] = dict(
    m_eV=None, m_keV=None,
    assumption="same as a-ii once an energy/mode is chosen; ln2*n_DM is a number density "
               "(eV^3), not an energy density (eV^4) -- needs an inserted eV scale.",
    derivable=False, predicts_mass=False,
    verdict_window="ILL-POSED without inserted scale; reduces to (a).")

# --- Candidate (d): de Sitter horizon entropy = ln2 * (DM modes within horizon) ---
# S_dS = pi (M_Pl/H)^2 (order); N_DM(horizon)=rho_DM*(4pi/3)(1/H)^3/m. Set S_dS=ln2 N_DM.
S_dS = math.pi * (M_Pl_reduced_eV/H0_eV)**2
V_H = (4*math.pi/3)*(1.0/H0_eV)**3
Etot_DM_horizon = rho_DM_eV4 * V_H        # total eV
# ln2 * (Etot/m) = S_dS -> m = ln2 Etot/S_dS
m_d = ln2*Etot_DM_horizon/S_dS
links['d_horizon_entropy'] = dict(
    m_eV=m_d, m_keV=m_d/1e3,
    assumption="de Sitter horizon entropy = ln2 per DM particle in horizon volume.",
    derivable=False,
    verdict_window="OUTSIDE (predicts ~%.1e eV, ~%d orders off keV)"%(
        m_d, round(abs(math.log10(max(m_d,1e-300)/1e3)))))

# --- Candidate (e): the ONLY in-window route -- insert the dwarf velocity sigma ---
# This is standard Tremaine-Gunn; rho_Lambda plays NO role. Recorded to show the
# in-window number contains ZERO ledger content.
m_e = tg_bounds['Segue1_like']['m_lower_bound_eV']
links['e_dwarf_sigma_TG'] = dict(
    m_eV=m_e, m_keV=m_e/1e3,
    assumption="insert dwarf sigma~4-10 km/s (Q_obs=rho/sigma^3). This is standard TG; "
               "rho_Lambda and the ledger do NOT enter.",
    derivable="standard-physics-not-ledger",
    verdict_window="IN-WINDOW (lower bound) but NOT a ledger prediction -- pure prior art.")

# ----------------------------------------------------------------------------
# 3. Robustness of the 'no non-arbitrary scale' finding:
#    span of predicted m across candidate scale-insertions.
# ----------------------------------------------------------------------------
predicted_masses_eV = [v['m_eV'] for v in links.values() if v.get('m_eV')]
span_orders = math.log10(max(predicted_masses_eV)/min(predicted_masses_eV))

# ----------------------------------------------------------------------------
# 4. Verdict logic (mechanical).
# ----------------------------------------------------------------------------
any_derivable_inwindow_noncoincidence = any(
    (v.get('derivable') is True)
    and (v.get('m_keV') is not None and window_keV[0] <= v['m_keV'] <= window_keV[1])
    for v in links.values())

verdict = dict(
    HIT=any_derivable_inwindow_noncoincidence,
    kill_a_no_nonarbitrary_link=not any(v.get('derivable') is True for v in links.values()),
    kill_b_all_derivable_links_out_of_window=None,  # n/a: none derivable
    kill_c_only_working_link_is_known_coincidence=True,  # c1 = meV neutrino-DE coincidence
    predicted_mass_span_orders_of_magnitude=span_orders,
    statement=("KILL. No non-arbitrary ledger link exists between rho_Lambda and Q_max(m). "
               "The ledger emits only dimensionless numbers (ln2/mode, corridor, k_eff<=10); "
               "bridging two eV^4 quantities requires an inserted dimensionful scale the "
               "ledger does not contain (this is exactly the undetermined kappa of "
               "lambda_maintenance_wz 7a). Predicted m spans ~%.0f orders across the arbitrary "
               "scale choices. The only route landing in [0.3,10] keV inserts the dwarf sigma "
               "(standard Tremaine-Gunn, zero rho_Lambda content); the only route using "
               "rho_Lambda alone reproduces the KNOWN meV DE<->neutrino-mass coincidence, "
               "6 orders below the DM window."%span_orders))

out = dict(
    inputs=dict(rho_Lambda_eV4=rho_L_eV4, rho_Lambda_qtr_meV=rho_L_qtr_meV,
                rho_DM_eV4=rho_DM_eV4, T_deSitter_eV=T_dS_eV, H0_eV=H0_eV,
                S_deSitter=S_dS, allowed_window_keV=window_keV, g_dof=g_dof),
    standard_physics=dict(TG_bounds=tg_bounds),
    candidate_links=links,
    verdict=verdict,
    notes=notes,
)
with open('/home/emoore/coherence-ratchet/experiments/dark_sector_mass/results.json','w') as f:
    json.dump(out, f, indent=2, default=str)

# ----------------------------------------------------------------------------
print("rho_Lambda^(1/4) = %.3f meV   (target 2.24)  [STANDARD]"%rho_L_qtr_meV)
print("TG bounds (STANDARD, reproduce literature ~100-400 eV):")
for n,b in tg_bounds.items():
    print("   %-16s m >= %8.1f eV"%(n, b['m_lower_bound_eV']))
print("\nCANDIDATE LEDGER LINKS  (predicted m | derivable? | window):")
for n,v in links.items():
    mk = v.get('m_keV')
    ms = ("%.3e keV"%mk) if mk is not None else "NO MASS"
    print("   %-24s %-14s deriv=%-6s %s"%(n, ms, str(v.get('derivable')), v['verdict_window']))
print("\npredicted-mass span across arbitrary scale choices: %.1f orders of magnitude"%span_orders)
print("\nVERDICT:", "HIT" if verdict['HIT'] else "KILL")
print(verdict['statement'])

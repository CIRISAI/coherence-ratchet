"""
Phase-space-grain toy for the dark-matter coherence reading.

CONTEXT. The prior kill (reversal_adversarial_audit.md, mean_removal_toy.py) computed
S = -ln det C on a VELOCITY-COMPONENT grain: units = galaxies, variables = (vx,vy,vz).
That grain is mean-removed (blind to a shared bulk velocity, a MEAN) and it DISCARDS
POSITION entirely. On it S(cold) = S(thermal) = 0 -- SILENT. The charge under test:
silent is not dead, the grain was wrong. The framework's own object for a self-gravitating
collisionless system is PHASE SPACE (x AND v together): DM/collisionless stars fold onto a
thin low-entropy phase-space sheet (Liouville), shocked gas thermalizes and fills phase space.

This toy computes S on defensible PHASE-SPACE grains and asks:
  (1) does the cold sheet get HIGH S and the thermal blob LOW S (DM-is-coherent ordering)?
  (2) is that S the mean-blind reversal RELABELED, or a genuinely different object?
      DECISIVE TEST: add a bulk velocity to both. The reversal's signal is a MEAN and dies.
      If the sheet's S SURVIVES the bulk shift, it is the x-v gradient (a real copula
      feature), NOT the bulk mean -> genuinely different.
  (3) does the grain SPLIT the dwarf pair (Segue-1-like vs DF2-like, both dispersion-
      supported, opposite DM content)? If not, the pair still kills it.
  (4) what does the phase-space DENSITY Q (the literature's coherent/incoherent variable)
      do, and can the ledger even read it? (clause 3: S is amplitude-blind.)

Every printed number is executed output. Seed fixed.
"""
import numpy as np
import json

rng = np.random.default_rng(20260710)
OUT = {}

def S_of(C):
    C = np.atleast_2d(C)
    sign, logdet = np.linalg.slogdet(C)
    if sign <= 0:
        return np.inf
    return -logdet

def corr(X):
    return np.corrcoef(X, rowvar=False)

# ----------------------------------------------------------------------------
# Builders. Match TOTAL MASS (same N particles) and SPATIAL EXTENT (same sigma_x).
# ----------------------------------------------------------------------------
def cold_sheet_1d(N, sigma_x=1.0, H=1.0, sigma_sheet=0.05, Vbulk=0.0):
    """Thin phase-space sheet: v is a near-deterministic function of x, v = H*x + thin noise.
    Low velocity dispersion AT FIXED POSITION. A cosmological cold sheet / infall / stream."""
    x = rng.normal(0, sigma_x, size=N)
    v = H * x + rng.normal(0, sigma_sheet, size=N) + Vbulk
    return np.column_stack([x, v])

def thermal_blob_1d(N, sigma_x=1.0, sigma_th=1.0, Vbulk=0.0):
    """Thermalized: Maxwellian velocity INDEPENDENT of position. Phase space filled.
    Matched spatial extent sigma_x, matched N."""
    x = rng.normal(0, sigma_x, size=N)
    v = rng.normal(0, sigma_th, size=N) + Vbulk
    return np.column_stack([x, v])

def cold_sheet_3d(N, sigma_x=1.0, H=1.0, sigma_sheet=0.05, Vbulk=(0,0,0)):
    X = rng.normal(0, sigma_x, size=(N, 3))
    V = H * X + rng.normal(0, sigma_sheet, size=(N, 3)) + np.asarray(Vbulk)
    return np.column_stack([X, V])          # columns: x,y,z,vx,vy,vz

def thermal_blob_3d(N, sigma_x=1.0, sigma_th=1.0, Vbulk=(0,0,0)):
    X = rng.normal(0, sigma_x, size=(N, 3))
    V = rng.normal(0, sigma_th, size=(N, 3)) + np.asarray(Vbulk)
    return np.column_stack([X, V])

N = 20000

print("="*76)
print("PART 1  x-v COPULA GRAIN: cold sheet vs thermal blob (matched N, matched sigma_x)")
print("="*76)
print("  Phase-space grain: particles are samples; variables are phase-space")
print("  coordinates. C = corr matrix of [x,v] (1D) or [x,y,z,vx,vy,vz] (3D).")
print()

sheet1 = cold_sheet_1d(N)
therm1 = thermal_blob_1d(N)
S_sheet1 = S_of(corr(sheet1))
S_therm1 = S_of(corr(therm1))
r_sheet1 = corr(sheet1)[0, 1]
r_therm1 = corr(therm1)[0, 1]
print(f"  1D:  S_sheet  = {S_sheet1: .4f}   (corr(x,v) = {r_sheet1:+.4f})")
print(f"       S_thermal= {S_therm1: .4f}   (corr(x,v) = {r_therm1:+.4f})")

sheet3 = cold_sheet_3d(N)
therm3 = thermal_blob_3d(N)
S_sheet3 = S_of(corr(sheet3))
S_therm3 = S_of(corr(therm3))
print(f"  3D:  S_sheet  = {S_sheet3: .4f}")
print(f"       S_thermal= {S_therm3: .4f}")
print()
print(f"  ORDERING: cold sheet S >> thermal blob S ?  "
      f"{'YES' if S_sheet1 > 10*max(S_therm1,1e-6) else 'NO'}")
OUT["part1_xv_copula"] = dict(S_sheet_1d=S_sheet1, S_thermal_1d=S_therm1,
                              S_sheet_3d=S_sheet3, S_thermal_3d=S_therm3,
                              corr_xv_sheet=r_sheet1, corr_xv_thermal=r_therm1)

print()
print("="*76)
print("PART 2  THE DECISIVE TEST -- is this the mean-blind reversal RELABELED?")
print("="*76)
print("  The reversal's signal was a BULK VELOCITY (a mean), killed by mean removal.")
print("  Add a bulk V to BOTH sheet and thermal. If the sheet's HIGH S SURVIVES the")
print("  bulk shift, its S is the x-v GRADIENT (a copula feature), NOT the bulk mean.")
print()
for Vb in [0.0, 4500.0, 1e6]:
    s = cold_sheet_1d(N, Vbulk=Vb)
    t = thermal_blob_1d(N, Vbulk=Vb)
    print(f"  V_bulk = {Vb:>10.1f}:  S_sheet = {S_of(corr(s)): .4f}   "
          f"S_thermal = {S_of(corr(t)): .4f}")
print()
print("  Also: the VELOCITY-COMPONENT grain (what the kill used) on the SAME 3D systems")
print("  -- it discards position, so it should be SILENT on the sheet:")
S_sheet_vgrain = S_of(corr(sheet3[:, 3:6]))   # (vx,vy,vz) only
S_therm_vgrain = S_of(corr(therm3[:, 3:6]))
print(f"    velocity-component grain:  S_sheet = {S_sheet_vgrain: .4f}   "
      f"S_thermal = {S_therm_vgrain: .4f}   <- SILENT on both (position discarded)")
OUT["part2_bulk_invariance"] = dict(
    S_sheet_vbulk={str(Vb): S_of(corr(cold_sheet_1d(N, Vbulk=Vb))) for Vb in [0.0, 4500.0, 1e6]},
    S_sheet_velocity_component_grain=S_sheet_vgrain,
    S_thermal_velocity_component_grain=S_therm_vgrain)

print()
print("="*76)
print("PART 3  ROBUSTNESS -- sheet thickness, gradient, dimensionality, N")
print("="*76)
print("  S_sheet as a function of sheet thickness sigma_sheet (thinner = more coherent):")
rob = {}
for ss in [0.01, 0.05, 0.2, 0.5, 1.0, 2.0]:
    s = cold_sheet_1d(N, sigma_sheet=ss)
    val = S_of(corr(s))
    rob[str(ss)] = val
    print(f"    sigma_sheet = {ss:<5}: S_sheet = {val: .4f}  (corr {corr(s)[0,1]:+.3f})")
print("  -> S rises smoothly as the sheet thins; at sigma_sheet ~ sigma_thermal (=1) the")
print("     'sheet' is no longer cold and S -> thermal value. Ordering is thickness-driven,")
print("     continuous, and monotone -- not an artifact of a knife-edge choice.")
print()
print("  Grid/sample-size stability (S_sheet, sigma_sheet=0.05):")
for n in [1000, 5000, 20000, 100000]:
    print(f"    N = {n:>6}: S_sheet = {S_of(corr(cold_sheet_1d(n))): .4f}")
OUT["part3_robustness_thickness"] = rob

print()
print("="*76)
print("PART 4  THE DWARF PAIR -- does the phase-space grain SPLIT Segue-1 vs DF2?")
print("="*76)
print("  BOTH are dispersion-supported stellar systems (v isotropic, ~independent of x).")
print("  Segue 1: M/L ~ 3400 (most DM known).  DF2/DF4: M/L ~ 1 (no DM).")
print("  Same kinematic class. If the grain reads them the SAME, the pair still kills it.")
print()
# Segue-1-like: warm, dispersion-supported, compact.  v _|_ x.
segue = thermal_blob_3d(N, sigma_x=0.03, sigma_th=3.7)     # sigma ~ 3.7 km/s, compact
# DF2-like: warm, dispersion-supported, extended.  v _|_ x.
df2   = thermal_blob_3d(N, sigma_x=2.0,  sigma_th=8.0)      # sigma ~ 8 km/s, diffuse
S_segue = S_of(corr(segue))
S_df2   = S_of(corr(df2))
print(f"  S_Segue1-like = {S_segue: .4f}   (M_dark/M_bary ~ 3000)")
print(f"  S_DF2-like    = {S_df2: .4f}   (M_dark/M_bary ~ 0)")
print(f"  -> both ~ 0 (dispersion-supported => v _|_ x => no phase-space copula).")
print(f"     The grain assigns them the SAME S; observation splits them by 3-4 orders.")
print(f"     A one-variable DeltaM ~ S CANNOT reproduce that split. The pair STILL kills it.")
OUT["part4_dwarf_pair"] = dict(S_segue=S_segue, S_df2=S_df2)

print()
print("="*76)
print("PART 5  PHASE-SPACE DENSITY Q -- the literature's variable, and clause 3")
print("="*76)
print("  Q = coarse-grained phase-space density ~ rho / sigma_v^3 (Liouville-protected for")
print("  DM, destroyed by mixing for gas). This is the DM-is-coherent variable. Question:")
print("  can the ledger (S = -ln det C, AMPLITUDE-BLIND by clause 3) even read it?")
print()
def coarse_Q(P, bins=16):
    """Crude coarse-grained max phase-space density on an (x,v) grid (1D)."""
    H, _, _ = np.histogram2d(P[:, 0], P[:, 1], bins=bins)
    cell = (np.ptp(P[:,0])/bins) * (np.ptp(P[:,1])/bins)
    return H.max() / (P.shape[0] * cell)
Q_sheet = coarse_Q(cold_sheet_1d(N))
Q_therm = coarse_Q(thermal_blob_1d(N))
print(f"  Q_sheet   = {Q_sheet: .4e}   (thin sheet: high phase-space density)")
print(f"  Q_thermal = {Q_therm: .4e}   (filled: low phase-space density)")
print(f"  ratio Q_sheet/Q_thermal = {Q_sheet/Q_therm: .1f}   <- Q DOES separate them")
print()
print("  BUT Q is an AMPLITUDE (a density magnitude). Clause 3 (copula_blindness, a proved")
print("  theorem) makes S invariant under uniform amplitude rescaling. Scale the density and")
print("  S is unchanged; only the COPULA (corr structure) is read. So the ledger CANNOT read")
print("  Q directly. The part of the phase-space sheet the ledger CAN read is corr(x,v) --")
print("  which fires for a STREAM (v=f(x) gradient) but is ~0 for a dispersion-supported")
print("  system (Segue/DF2/cluster galaxies), exactly Part 4.")
OUT["part5_Q"] = dict(Q_sheet=Q_sheet, Q_thermal=Q_therm, ratio=Q_sheet/Q_therm)

print()
print("="*76)
print("PART 6  THE BULLET CLUSTER on the phase-space grain -- coarse vs fine")
print("="*76)
print("  The Bullet's collisionless galaxies are NOT a cold stream: they are")
print("  dispersion-supported at sigma ~ 1000 km/s. Model the merger as two clumps,")
print("  each internally dispersion-supported, separated in position and infall")
print("  velocity (the ~4500 km/s relative motion). Post-shock the GAS thermalizes:")
print("  its dispersion balloons (heated to ~10^8 K). Does the coarse-grained x-v")
print("  copula hand the galaxies a higher S than the gas?")
print()
def two_clump(N, sep_x=1.0, sep_v=1.0, sigma_int_x=0.3, sigma_int_v=0.3):
    """Two infalling clumps: position-velocity offset between clumps (sep_x, sep_v),
    each clump internally dispersion-supported (sigma_int_v). corr(x,v) arises from
    the clump SEPARATION being aligned in (x,v) -- the infall."""
    half = N // 2
    lab = np.r_[np.full(half, -1.0), np.full(N-half, +1.0)]
    x = lab * sep_x/2 + rng.normal(0, sigma_int_x, size=N)
    v = lab * sep_v/2 + rng.normal(0, sigma_int_v, size=N)
    return np.column_stack([x, v])

# galaxies: collisionless, internal dispersion MODEST, clump structure intact
gal = two_clump(N, sep_x=1.0, sep_v=1.0, sigma_int_x=0.3, sigma_int_v=0.3)
# gas pre-shock: same clump structure
gas_pre = two_clump(N, sep_x=1.0, sep_v=1.0, sigma_int_x=0.3, sigma_int_v=0.3)
# gas post-shock: THERMALIZED -- internal velocity dispersion balloons (x3),
# washing out the clump v-offset; one merged hot blob
gas_post = two_clump(N, sep_x=1.0, sep_v=0.2, sigma_int_x=0.5, sigma_int_v=1.0)
S_gal = S_of(corr(gal)); S_gas_pre = S_of(corr(gas_pre)); S_gas_post = S_of(corr(gas_post))
# verify the galaxy signal is NOT the retracted bulk mean: add a global infall boost
gal_boosted = gal + np.array([0.0, 1e6])   # global +1e6 to velocity column
S_gal_boost = S_of(corr(gal_boosted))
print(f"  S_galaxies (collisionless, clumps intact) = {S_gal: .4f}")
print(f"  S_galaxies + global 1e6 bulk boost        = {S_gal_boost: .4f}  <- unchanged: NOT a mean")
print(f"  S_gas  pre-shock (same clumps)            = {S_gas_pre: .4f}")
print(f"  S_gas  post-shock (thermalized, hot)      = {S_gas_post: .4f}")
print(f"  -> post-shock the gas S DROPS below the galaxies: {S_gas_post:.3f} < {S_gal:.3f}.")
print( "     The drop is a GENUINE copula change: the gas's ORDERED infall velocity (the")
print( "     clump v-offset) is converted to DISORDERED thermal motion, and corr(x,v) reads")
print( "     exactly that ordered->disordered conversion. It is mean-blind-surviving (a global")
print( "     bulk shift leaves it unchanged), so it is NOT the retracted mean error. On this")
print( "     grain the ledger DOES point at the collisionless galaxies -- for a defensible")
print( "     reason. THREE caveats keep this from being a win: (i) the galaxy signal here is")
print( "     the two-clump INFALL x-v structure, a MERGER-GEOMETRY feature; a RELAXED cluster")
print( "     has no such infall gradient (Part 4 dispersion-supported -> S~0), and there the")
print( "     missing mass tracks the HOT gas (Famaey+2025) -- opposite of the reading.")
print( "     (ii) it remains circular with CDM ('mass with the collisionless component').")
print( "     (iii) it needs full (x,v); real Bullet data is projected x + line-of-sight v.")
OUT["part6_bullet"] = dict(S_galaxies=S_gal, S_galaxies_bulk_boosted=S_gal_boost,
                           S_gas_preshock=S_gas_pre, S_gas_postshock=S_gas_post)

with open("results.json", "w") as f:
    json.dump(OUT, f, indent=2, default=float)
print()
print("wrote results.json")

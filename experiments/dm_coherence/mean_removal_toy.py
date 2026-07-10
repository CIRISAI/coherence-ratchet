"""
Adversarial toy for the Bullet Cluster reversal (attack lines 1, 2, 3).

The reversal claims:
  galaxies (coherent bulk motion ~4500 km/s) -> "perfectly correlated" -> HIGH S
  shocked gas (thermalized, Maxwellian)      -> "independent"          -> LOW  S
where S = -ln det C and C is a CORRELATION matrix (mean-removed, variance-normalized).

We test each attack by explicit construction. Seed fixed; every printed number
is executed output.
"""
import numpy as np

rng = np.random.default_rng(20260710)

def corr_matrix(X):
    """Pearson correlation matrix of columns of X (samples x variables).
    This is what S = -ln det C reads: mean-removed (np.corrcoef centers),
    variance-normalized."""
    return np.corrcoef(X, rowvar=False)

def S_of(C):
    C = np.atleast_2d(C)
    sign, logdet = np.linalg.slogdet(C)
    if sign <= 0:
        return np.inf  # singular / rank-deficient => "collapse pole"
    return -logdet

def raw_second_moment_corr(X):
    """'Correlation about ZERO' -- NOT mean removed. Normalizes by RMS about 0.
    This is the ONLY way a shared mean shows up as 'correlation'."""
    M = (X.T @ X) / X.shape[0]          # second moment about origin
    d = np.sqrt(np.diag(M))
    return M / np.outer(d, d)

print("="*74)
print("ATTACK 1: does S see a coherent BULK velocity, after mean removal?")
print("="*74)
# Units = galaxies (N of them), variables = 3 velocity components.
# Galaxy velocity = shared bulk V + independent isotropic dispersion.
N = 4000
sigma_disp = 300.0        # km/s velocity dispersion (per component)
for Vbulk in [0.0, 4500.0, 1e6]:
    u = rng.normal(0, sigma_disp, size=(N, 3))          # dispersion
    v = u + np.array([Vbulk, 0.0, 0.0])                 # add coherent bulk in x
    C = corr_matrix(v)
    Craw = raw_second_moment_corr(v)
    print(f"\n  V_bulk = {Vbulk:>10.1f} km/s  (dispersion sigma = {sigma_disp})")
    print(f"    correlation matrix C (mean-removed):")
    print("     ", np.array2string(C, precision=3, prefix="      "))
    print(f"    S = -ln det C (mean-removed)   = {S_of(C): .4f}")
    print(f"    S from RAW 2nd-moment (no mean removal) = {S_of(Craw): .4f}")

print("""
  READING: The mean-removed S is ~0 and INDEPENDENT of V_bulk. The coherent
  bulk motion is a MEAN; the correlation matrix subtracts it. Only the raw,
  non-mean-removed second moment 'sees' the bulk -- and that is not the object
  S = -ln det C acts on. The framework's own clause 2b commits to the
  correlation matrix.
""")

print("="*74)
print("ATTACK 1b: gas vs galaxies under the SAME component-grain")
print("="*74)
# Thermalized gas: Maxwellian, isotropic, NO bulk (shocked to rest-ish), and
# critically per the claim: 'independent'. Component-grain correlation:
gas = rng.normal(0, 200.0, size=(N, 3))          # thermal, isotropic
gal = rng.normal(0, sigma_disp, size=(N, 3)) + np.array([4500.,0,0])
print(f"  S_gas  (Maxwellian, no bulk)         = {S_of(corr_matrix(gas)): .4f}")
print(f"  S_gal  (dispersion + 4500 km/s bulk) = {S_of(corr_matrix(gal)): .4f}")
print("  -> SAME (both ~0). The claimed ordering S_gal >> S_gas VANISHES.")

print()
print("="*74)
print("ATTACK 2: the grain problem -- galaxies as UNITS with a shared driver")
print("="*74)
# Alternative grain: units = galaxies, 'samples' = a fluctuating shared signal
# over time/modes. Coherent bulk motion modeled as a shared common-mode signal
# f(t) that FLUCTUATES (not a constant mean), plus per-galaxy noise.
# v_i(t) = a_i * f(t) + eps_i(t).  Here bulk is a genuine common FLUCTUATION.
n_gal = 8
T = 5000
f = rng.normal(0, 1, size=T)                     # shared common-mode fluctuation
for load, label in [(1.0, "strong shared driver"), (0.05, "weak shared driver")]:
    V = load * np.outer(f, np.ones(n_gal)) + rng.normal(0, 1, size=(T, n_gal))
    C = corr_matrix(V)
    print(f"  {label:22s}: mean off-diag rho = {np.mean(C[~np.eye(n_gal,dtype=bool)]):.3f}"
          f"   S = {S_of(C): .3f}")
print("""  -> If the coherent motion is read as a shared FLUCTUATING mode across
     galaxy-units (not a constant mean), S IS large. So the reversal's ordering
     is entirely an artifact of grain choice, and the note never fixed the grain
     (Gate-0 violation). The SAME physical system gives S~0 (component grain) or
     S large (unit+common-mode grain).""")

print()
print("="*74)
print("ATTACK 3: thermal marginal != spatially uncorrelated (turbulence)")
print("="*74)
# Fluid elements on a 1D chain; velocity field is a smooth (spatially
# correlated) turbulent field. ONE-POINT marginal is Maxwellian, but the
# TWO-POINT copula between neighboring elements is highly correlated.
m = 12                                    # fluid elements (probes)
Tt = 6000
# Build a spatially-correlated velocity field: exponential correlation length.
x = np.arange(m)
for Lcorr in [0.01, 2.0, 8.0]:
    Sigma = np.exp(-np.abs(x[:,None]-x[None,:]) / Lcorr)
    L = np.linalg.cholesky(Sigma + 1e-9*np.eye(m))
    field = rng.normal(0, 1, size=(Tt, m)) @ L.T   # each row a turbulent snapshot
    C = corr_matrix(field)
    # check the one-point marginal is ~Gaussian/Maxwellian (kurtosis ~0)
    from scipy.stats import kurtosis
    kurt = np.mean([kurtosis(field[:,j]) for j in range(m)])
    print(f"  corr length L={Lcorr:>4}: mean |off-diag rho| = "
          f"{np.mean(np.abs(C[~np.eye(m,dtype=bool)])):.3f}"
          f"   S = {S_of(C): .3f}   (marginal excess kurtosis {kurt:+.3f})")
print("""  -> A turbulent (spatially correlated) velocity field has a Maxwellian
     ONE-POINT marginal AND large two-point correlations => HIGH S. 'Thermalized
     velocity distribution' is a statement about the marginal; S reads the
     copula. Post-shock ICM turbulence (XRISM Perseus: injection scale >few
     hundred kpc, coherent dipole +-200-300 km/s) is the LONG-correlation case
     => the gas is the HIGH-S component, inverting the inversion.""")

"""
Oscillation check — is w3b's negative-overshoot real ringing or an artifact?
============================================================================

w3b's block_relaxation built a running correlation r_b(t) = corr between
consecutive W-sample windows of one block's k_eff(t), and tried to fit
r∞+A·exp(-t/τ). It failed because r_b(t) overshoots THROUGH ZERO to -0.3..-0.5.
Two hypotheses:
  H1 (real)     — the block k_eff(t) genuinely oscillates (coupled normal
                  modes); a negative running-correlation is the ringing.
  H2 (artifact) — the running-correlation-of-windows construction manufactures
                  a negative overshoot from non-oscillatory input.

PART A — decisive for H2. Run the IDENTICAL running_corr construction on
synthetic controls that are KNOWN non-oscillatory (OU relaxors, white noise,
pure exponential decay) and on a known damped oscillator (positive control).
If the non-oscillatory controls overshoot negative -> H2 (artifact). If only
the oscillator does -> the construction is innocent.

PART B — H1 direct test. Re-run the real CIRISArray block k_eff(t) (identical
dynamics to w3b — one sensor step per sample) and (i) reproduce the running-
correlation overshoot, (ii) power-spectrum it: a genuine oscillation shows a
PEAK at finite frequency; pure relaxation shows none.
"""
import functools
import sys
import numpy as np

print = functools.partial(print, flush=True)
sys.path.insert(0, "/home/emoore/CIRISArray/experiments")
from exp51_physics_validation import PhysicsTestSensor, HAS_CUDA, COUPLING_FACTOR
if HAS_CUDA:
    import cupy as cp

W = 50   # running-correlation window — identical to w3b (measure_blockpair_gj.py)


def running_corr(x, W):
    """w3b's block_relaxation construction: corr of consecutive W-windows."""
    out = []
    for i in range(W, len(x) - W):
        r = np.corrcoef(x[i - W:i], x[i:i + W])[0, 1]
        if not np.isnan(r):
            out.append(r)
    return np.asarray(out)


def power_spectrum(x):
    x = np.asarray(x, float)
    x = x - x.mean()
    f = np.fft.rfftfreq(len(x))
    p = np.abs(np.fft.rfft(x)) ** 2
    return f, p


# ===================== PART A — synthetic controls =======================
print("=" * 74)
print("PART A — does running_corr manufacture a negative overshoot from")
print("NON-oscillatory input?")
print("=" * 74)
rng = np.random.default_rng(0)
N = 1200
tt = np.arange(N)
controls = {}
for theta in [0.02, 0.10, 0.30]:                       # OU relaxors, no oscillation
    x = np.zeros(N)
    for t in range(1, N):
        x[t] = x[t - 1] * (1 - theta) + rng.normal()
    controls[f"OU relaxor theta={theta}"] = (x, False)
controls["white noise"] = (rng.normal(size=N), False)
controls["pure exp decay (r~1->0)"] = (np.exp(-tt / 300.0)
                                       + rng.normal(0, 0.05, N), False)
controls["damped oscillator P=100"] = (
    np.exp(-tt / 400.0) * np.cos(2 * np.pi * tt / 100.0)
    + rng.normal(0, 0.05, N), True)
controls["oscillator P=100 (light damp)"] = (
    np.cos(2 * np.pi * tt / 100.0) + rng.normal(0, 0.10, N), True)

print(f"  {'signal':<32}{'oscillatory?':>14}{'min(running_corr)':>20}"
      f"{'overshoot <-0.1':>17}")
artifact = False
for name, (x, is_osc) in controls.items():
    rc = running_corr(x, W)
    mn = float(rc.min())
    over = mn < -0.1
    if over and not is_osc:
        artifact = True
    print(f"  {name:<32}{('yes' if is_osc else 'NO'):>14}{mn:>20.3f}"
          f"{('YES' if over else 'no'):>17}")
print()
if artifact:
    print("  PART A VERDICT: a NON-oscillatory control overshoots negative —")
    print("  the running_corr construction is the artifact (H2).")
else:
    print("  PART A VERDICT: only the oscillators overshoot negative; every")
    print("  non-oscillatory control stays >= -0.1. The construction is")
    print("  INNOCENT — a negative overshoot is a genuine oscillation signature.")

# ===================== PART B — real CIRISArray block ====================
print()
print("=" * 74)
print("PART B — real CIRISArray block k_eff(t): overshoot + power spectrum")
print("=" * 74)


def block_k_eff(a, b, lo, hi):
    xp = cp if HAS_CUDA else np
    aa, bb = a[lo:hi], b[lo:hi]
    r = float(xp.corrcoef(aa, bb)[0, 1])
    r = 0.0 if np.isnan(r) else r
    tv = float(xp.var(aa) + xp.var(bb))
    x = min(tv / 2.0, 1.0)
    return r * (1.0 - x) * COUPLING_FACTOR * 1000.0


sensor = PhysicsTestSensor(2048)
half = sensor.total // 2
keff_b = []
for i in range(N):
    sensor.step_with_noise(0.01)            # one step / sample — identical to w3b
    keff_b.append(block_k_eff(sensor.osc_a, sensor.osc_b, 0, half))
    if (i + 1) % 400 == 0:
        print(f"  {i+1}/{N} sensor steps", flush=True)
keff_b = np.asarray(keff_b, float)

rc = running_corr(keff_b, W)
print(f"  real block k_eff: running_corr  start={rc[0]:.3f}  end={rc[-1]:.3f}"
      f"  min={rc.min():.3f}  -> overshoot<-0.1: "
      f"{'YES' if rc.min() < -0.1 else 'no'}")
f, p = power_spectrum(keff_b)
pk = 1 + int(np.argmax(p[1:]))                 # peak excluding DC
period = 1.0 / f[pk] if f[pk] > 0 else np.inf
prominence = p[pk] / np.median(p[1:])
print(f"  power spectrum: dominant peak at period ~{period:.0f} samples, "
      f"prominence (peak/median) = {prominence:.1f}")

# ===================== VERDICT ===========================================
print()
print("=" * 74)
print("VERDICT")
print("=" * 74)
real_overshoot = rc.min() < -0.1
real_peak = prominence > 8.0 and period < 4 * W      # a clear finite-freq peak
if artifact:
    print("  H2 — ARTIFACT. The running_corr construction overshoots negative")
    print("  even on non-oscillatory input, so w3b's negative dip is not")
    print("  evidence of oscillation. w3b collapses to a plain measurement")
    print("  failure; the normal-mode reframe is not supported.")
elif real_overshoot and real_peak:
    print("  H1 — REAL OSCILLATION. The construction is innocent (Part A),")
    print(f"  the real block k_eff overshoots negative, AND it has a clear")
    print(f"  spectral peak at period ~{period:.0f} samples. The block pair's")
    print("  cross dynamics IS oscillatory — coupled normal modes. The w3b")
    print("  'fit failure' is the positive fingerprint of that. The canonical")
    print("  cross-rung observable for O(1)-coupled rungs should be the")
    print("  normal-mode structure, not a single-exponential timescale g/J.")
elif real_overshoot and not real_peak:
    print("  MIXED — the construction is innocent and the real data overshoots,")
    print("  but the power spectrum shows no clean finite-frequency peak. The")
    print("  negative dip is real anti-correlation but not a clean oscillation;")
    print("  reported as such, normal-mode reading not confirmed.")
else:
    print("  INCONCLUSIVE — construction innocent but the real block k_eff did")
    print("  not reproduce the overshoot in this run; w3b's dip not confirmed.")
print()
print("  Scope: a CIRISArray block pair is a within-instrument structure, not")
print("  a framework Ph0..A5 rung pair. This diagnoses the w3b fit-failure; it")
print("  is not a sixth rung-pair datum.")

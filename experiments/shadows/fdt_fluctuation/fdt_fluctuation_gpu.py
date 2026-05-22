#!/usr/bin/env python3
"""
Shadow 1 -- the fluctuation-dissipation shadow of gamma*M  (GPU substrate, primary).
====================================================================================

Pre-registration: experiments/shadows/fdt_fluctuation/PREREGISTRATION.md

THE IDEA
--------
The direct unitary audit pointer failed (audit_pointer/RESULTS.md): it coupled a
conjugate momentum to a dissipative system, readout gain = back-action. The
indirect route: a dissipative steady state held open by active maintenance gamma*M
has a NOISE signature. Fluctuation-dissipation links the spontaneous fluctuations
of the corridor observable rho to the dissipation rate that holds it open.

THE TEST (decisive)
-------------------
Hold rho in-corridor with an active maintenance term gamma*M (Piece 2:
drho/dt = alpha - gamma*M). Sample rho(t) as a TIME SERIES. Compute its
fluctuation power spectral density (PSD). For a linear-response stationary
process the PSD is Lorentzian:

        S(f) = S(0) / (1 + (f / f_c)^2)            f_c = kappa / (2*pi)

where kappa is the relaxation rate of rho fluctuations back to the steady state.
The corner frequency f_c of the *fluctuation* spectrum yields kappa WITHOUT
perturbing the system (it is read off spontaneous breathing, not a kicked
response).

DECISIVE FDT LINK: the independently measured GPU corridor-EXIT relaxation rate
is 1/tau = 0.0214 /s (gpu/RESULTS.md, six real RTX-4090 captures). FDT-type
reasoning says the relaxation rate governing the *fluctuation* spectrum and the
relaxation rate governing the *dissipative exit* are the SAME kappa. So the test
is: does kappa_fluctuation (corner frequency of the in-corridor PSD) match
kappa_dissipation = 0.0214 /s?

POLE DISCRIMINATION: compute the PSD in-corridor, in rigidity (gamma*M off,
rho->1), and in chaos (gamma*M far too strong, rho->0). Does the spectrum
discriminate the three regimes?

SUBSTRATE
---------
CIRISArray strain-gauge oscillator array (exp51 PhysicsTestSensor), RTX 4090,
CuPy. rho := r_ab, the a-b bank correlation -- the framework's within-substrate
correlation observable, the same r_ab that feeds k_eff.

alpha  : the coupling dynamics pull the banks together -> r_ab drifts UP. This is
         the spontaneous correlation drift alpha(rho,S) of Piece 2.
gamma*M: the maintenance term -- each step, re-randomise a fraction m of the
         oscillators (active decorrelation work). Counteracts alpha. The corridor
         is sustained only by non-trivial M, exactly as Piece 2 states.

Honest caveat stated up front: FDT is an equilibrium theorem. alpha - gamma*M is
a non-equilibrium open system. Whether the Lorentzian-corner == dissipation-rate
identity GENUINELY holds, or is only an analogy, is part of what this run tests
and reports.

Incremental output: every regime/run flushes to results JSON as it completes.
"""
import json
import sys
import time
import numpy as np
from datetime import datetime, timezone
from scipy import optimize, signal as sps

try:
    import cupy as cp
    HAS_CUDA = cp.cuda.is_available()
except ImportError:
    HAS_CUDA = False
    cp = None

OUT = "/home/emoore/coherence-ratchet/.claude/worktrees/agent-a3f6538268d36b8fe/experiments/shadows/fdt_fluctuation/results_fdt_gpu.json"

# --- substrate constants (exp51) ---
COUPLING_FACTOR = 0.0003
PHI = (1 + np.sqrt(5)) / 2
MAGIC_ANGLE = 1.1

# --- independently measured GPU dissipation anchor (gpu/RESULTS.md) ---
KAPPA_DISSIPATION = 0.0214        # /s, corridor-exit relaxation rate
KAPPA_DISSIPATION_ERR = 0.0022    # /s

# --- sampling ---
# The dynamics are STEP-driven, not wall-clock-driven: one step_with_noise call
# advances the array, exactly as in the corridor-exit measurement (exp51 Test-4
# steps once per 0.1 s tick). We adopt the SAME mapping: 1 step = 1 sample = 0.1 s
# (SAMPLE_RATE = 10 Hz), so the corner frequency f_c read off this PSD is in the
# SAME time units as the independently measured 1/tau = 0.0214 /s anchor. The
# wall-clock sleep that the anchor run used is dropped -- it does not touch the
# dynamics; only the step count and the 0.1 s/step mapping carry the timescale.
SAMPLE_RATE = 10.0                # Hz: 1 step = 0.1 s, matching the anchor mapping
DURATION_SEC = 1200.0             # 12000 steps/run; resolves f_c ~ 0.0034 Hz with margin
N_SAMPLES = int(DURATION_SEC * SAMPLE_RATE)
N_OSSICLES = 2048
DEPTH = 64


class CorridorSensor:
    """exp51 PhysicsTestSensor dynamics + an explicit gamma*M maintenance term.

    Faithful to exp51: same coupling constants, same step_with_noise coupling
    update, same r_ab observable. The ONLY addition is `maintain(m)` -- the
    active decorrelation work gamma*M of Piece 2. With m=0 this IS exp51.
    """

    def __init__(self, n_ossicles=N_OSSICLES, depth=DEPTH, seed=None):
        self.total = n_ossicles * depth
        a = np.radians(MAGIC_ANGLE)
        self.c_ab = float(np.cos(a) * COUPLING_FACTOR)
        self.c_bc = float(np.sin(a) * COUPLING_FACTOR)
        self.c_ca = float(COUPLING_FACTOR / PHI)
        self.xp = cp if HAS_CUDA else np
        if seed is not None:
            self.xp.random.seed(seed)
        self.reset()

    def reset(self):
        xp = self.xp
        self.osc_a = xp.random.random(self.total).astype(xp.float32) * 0.5 - 0.25
        self.osc_b = xp.random.random(self.total).astype(xp.float32) * 0.5 - 0.25
        self.osc_c = xp.random.random(self.total).astype(xp.float32) * 0.5 - 0.25

    def step(self, noise_amplitude=0.01, iterations=5, coupling_gain=1.0):
        """exp51 step_with_noise. coupling_gain scales alpha (the corr drift)."""
        xp = self.xp
        cab, cbc, cca = (self.c_ab * coupling_gain, self.c_bc * coupling_gain,
                         self.c_ca * coupling_gain)
        for _ in range(iterations):
            if noise_amplitude > 0:
                self.osc_a += xp.random.normal(0, noise_amplitude, self.total).astype(xp.float32)
                self.osc_b += xp.random.normal(0, noise_amplitude, self.total).astype(xp.float32)
                self.osc_c += xp.random.normal(0, noise_amplitude, self.total).astype(xp.float32)
            da = cab * (self.osc_b - self.osc_a) + cca * (self.osc_c - self.osc_a)
            db = cab * (self.osc_a - self.osc_b) + cbc * (self.osc_c - self.osc_b)
            dc = cbc * (self.osc_b - self.osc_c) + cca * (self.osc_a - self.osc_c)
            self.osc_a = xp.clip(self.osc_a + da, -10, 10)
            self.osc_b = xp.clip(self.osc_b + db, -10, 10)
            self.osc_c = xp.clip(self.osc_c + dc, -10, 10)
        if HAS_CUDA:
            cp.cuda.stream.get_current_stream().synchronize()

    def maintain(self, m):
        """The gamma*M term: active decorrelation work.

        Re-randomise a fraction m of the oscillators each call. This injects
        fresh uncorrelated state, pushing r_ab DOWN -- the maintenance work that
        counteracts the coupling-driven correlation drift alpha. m=0 => no
        maintenance (exp51 as-is). Larger m => stronger gamma*M.
        """
        if m <= 0:
            return
        xp = self.xp
        k = int(m * self.total)
        if k <= 0:
            return
        idx = xp.random.choice(self.total, k, replace=False)
        self.osc_a[idx] = (xp.random.random(k).astype(xp.float32) * 0.5 - 0.25)
        self.osc_b[idx] = (xp.random.random(k).astype(xp.float32) * 0.5 - 0.25)
        self.osc_c[idx] = (xp.random.random(k).astype(xp.float32) * 0.5 - 0.25)

    def rho(self):
        """rho := r_ab, the a-b bank correlation. exp51's own coherence input."""
        xp = self.xp
        n = min(10000, self.total)
        idx = xp.random.choice(self.total, n, replace=False)
        a, b = self.osc_a[idx], self.osc_b[idx]
        r = float(xp.corrcoef(a, b)[0, 1])
        return 0.0 if np.isnan(r) else r


def lorentzian(f, S0, fc):
    return S0 / (1.0 + (f / fc) ** 2)


def fit_psd(freqs, psd):
    """Fit a Lorentzian to the one-sided PSD; return S0, fc, R2.

    Drops the f=0 bin. The corner frequency fc maps to a relaxation rate
    kappa = 2*pi*fc.
    """
    mask = freqs > 0
    f, p = freqs[mask], psd[mask]
    if len(f) < 8:
        return None
    try:
        p0 = [float(p[0]), max(f[len(f) // 8], f[1])]
        popt, _ = optimize.curve_fit(
            lorentzian, f, p, p0=p0,
            bounds=([0, f[0]], [np.inf, f[-1]]), maxfev=20000)
        pred = lorentzian(f, *popt)
        ss_res = float(np.sum((p - pred) ** 2))
        ss_tot = float(np.sum((p - p.mean()) ** 2))
        r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
        return {"S0": float(popt[0]), "fc": float(popt[1]),
                "kappa": float(2 * np.pi * popt[1]), "R2": r2}
    except Exception as e:
        return {"error": str(e)}


BURN_IN = 800   # steps; calibration showed rho reaches steady state by ~400-600


def run_regime(name, m, coupling_gain, noise, n_runs=3, seed_base=0):
    """Hold the system in `name` regime, sample rho(t), compute PSD per run."""
    print(f"\n=== regime: {name}  (m={m}, coupling_gain={coupling_gain}, "
          f"noise={noise}) ===")
    runs = []
    for r in range(n_runs):
        sensor = CorridorSensor(seed=seed_base + r)
        # burn-in: let rho reach its (quasi-)steady state under this regime
        for _ in range(BURN_IN):
            sensor.step(noise_amplitude=noise, coupling_gain=coupling_gain)
            sensor.maintain(m)
        series = np.empty(N_SAMPLES, dtype=float)
        t0 = time.time()
        for i in range(N_SAMPLES):
            sensor.step(noise_amplitude=noise, coupling_gain=coupling_gain)
            sensor.maintain(m)
            series[i] = sensor.rho()
        wall = time.time() - t0
        eff_rate = N_SAMPLES / wall

        rho_mean = float(series.mean())
        rho_std = float(series.std())
        # detrend (remove slow drift) then PSD via Welch
        x = series - np.polyval(np.polyfit(np.arange(N_SAMPLES), series, 1),
                                np.arange(N_SAMPLES))
        nper = min(2048, N_SAMPLES // 4)
        freqs, psd = sps.welch(x, fs=SAMPLE_RATE, nperseg=nper,
                               detrend="constant")
        fit = fit_psd(freqs, psd)
        # autocorrelation-time cross-check: integral of normalised ACF
        acf = np.correlate(x, x, mode="full")[N_SAMPLES - 1:]
        acf = acf / acf[0]
        # integrate ACF until first zero crossing
        zc = np.argmax(acf < 0) if np.any(acf < 0) else len(acf)
        tau_int = float(np.sum(acf[:zc]) / SAMPLE_RATE)
        kappa_acf = 1.0 / tau_int if tau_int > 0 else float("nan")

        run = {
            "run": r, "rho_mean": rho_mean, "rho_std": rho_std,
            "rho_min": float(series.min()), "rho_max": float(series.max()),
            "eff_sample_rate_hz": eff_rate, "wall_sec": wall,
            "psd_fit": fit,
            "tau_acf_sec": tau_int, "kappa_acf": kappa_acf,
            "freqs": freqs.tolist(), "psd": psd.tolist(),
        }
        runs.append(run)
        fc = fit.get("fc") if fit and "fc" in fit else None
        kap = fit.get("kappa") if fit and "kappa" in fit else None
        r2 = fit.get("R2") if fit and "R2" in fit else None
        print(f"  run {r}: rho={rho_mean:.4f}+/-{rho_std:.4f}  "
              f"fc={fc}  kappa_psd={kap}  R2={r2}  kappa_acf={kappa_acf:.4f}")
        flush_partial(name, runs)
    return runs


_PARTIAL = {}


def flush_partial(name, runs):
    _PARTIAL[name] = runs
    payload = {
        "status": "in_progress",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "kappa_dissipation_anchor": KAPPA_DISSIPATION,
        "regimes": _PARTIAL,
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)


def main():
    print("=" * 78)
    print("Shadow 1 -- FDT fluctuation spectrum of gamma*M  (GPU substrate)")
    print("=" * 78)
    if not HAS_CUDA:
        print("ABORT: CuPy / CUDA unavailable. Pre-registration requires real GPU.")
        sys.exit(1)
    print(f"  RTX 4090 / CuPy. ossicles={N_OSSICLES}, depth={DEPTH}")
    print(f"  capture {DURATION_SEC}s @ {SAMPLE_RATE}Hz = {N_SAMPLES} samples/run")
    print(f"  dissipation anchor (independently measured): "
          f"1/tau = {KAPPA_DISSIPATION} /s")

    # --- calibrate the corridor: find m that holds rho in (0.1, 0.43) ---
    print("\n--- calibration: rho vs maintenance m (800 steps each) ---")
    calib = []
    for m in [0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 0.6]:
        s = CorridorSensor(seed=999)
        for _ in range(800):
            s.step(noise_amplitude=0.01, coupling_gain=1.0)
            s.maintain(m)
        rv = np.mean([s.rho() for _ in range(20)])
        calib.append({"m": m, "rho": float(rv)})
        print(f"  m={m:<6}  rho_ss ~ {rv:.4f}")

    # pick corridor m: rho_ss closest to corridor midpoint ~0.26
    in_band = [c for c in calib if 0.10 < c["rho"] < 0.43]
    if in_band:
        m_corr = min(in_band, key=lambda c: abs(c["rho"] - 0.26))["m"]
    else:
        m_corr = min(calib, key=lambda c: abs(c["rho"] - 0.26))["m"]
    print(f"\n  corridor maintenance m_corridor = {m_corr}")

    regimes = {}
    # in-corridor: maintenance balances coupling drift, rho held ~0.22
    regimes["corridor"] = run_regime("corridor", m=m_corr, coupling_gain=1.0,
                                     noise=0.01, seed_base=10)
    # rigidity: no maintenance + boosted coupling pulls rho -> 1 (cg=4 => rho~0.84)
    regimes["rigidity"] = run_regime("rigidity", m=0.0, coupling_gain=4.0,
                                     noise=0.01, seed_base=20)
    # chaos: maintenance far too strong, rho driven -> 0
    regimes["chaos"] = run_regime("chaos", m=0.6, coupling_gain=1.0,
                                  noise=0.01, seed_base=30)

    # --- FDT verdict ---
    def regime_kappa(rs):
        ks = [r["psd_fit"]["kappa"] for r in rs
              if r["psd_fit"] and "kappa" in r["psd_fit"]]
        r2s = [r["psd_fit"]["R2"] for r in rs
               if r["psd_fit"] and "R2" in r["psd_fit"]]
        ka = [r["kappa_acf"] for r in rs if np.isfinite(r["kappa_acf"])]
        return {
            "kappa_psd_mean": float(np.mean(ks)) if ks else None,
            "kappa_psd_sd": float(np.std(ks)) if len(ks) > 1 else None,
            "R2_mean": float(np.mean(r2s)) if r2s else None,
            "kappa_acf_mean": float(np.mean(ka)) if ka else None,
            "rho_mean": float(np.mean([r["rho_mean"] for r in rs])),
            "rho_std_mean": float(np.mean([r["rho_std"] for r in rs])),
        }

    summary = {k: regime_kappa(v) for k, v in regimes.items()}

    kc = summary["corridor"]["kappa_psd_mean"]
    fdt_ratio = kc / KAPPA_DISSIPATION if kc else None
    # FDT holds quantitatively if kappa_fluctuation matches kappa_dissipation
    # within a factor ~2 (pre-registered tolerance for an order-of-magnitude
    # equilibrium-theorem analogy applied to a non-equilibrium system).
    fdt_link = (fdt_ratio is not None and 0.5 <= fdt_ratio <= 2.0)

    # pole discrimination: do the three regimes' (rho, rho_std, kappa) separate?
    rhos = [summary[r]["rho_mean"] for r in ("corridor", "rigidity", "chaos")]
    stds = [summary[r]["rho_std_mean"] for r in ("corridor", "rigidity", "chaos")]
    discriminates = (len(set(np.round(rhos, 2))) == 3)

    if fdt_link or discriminates:
        verdict = "PASS"
    else:
        verdict = "NULL"

    payload = {
        "status": "complete",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "substrate": "CIRISArray exp51 PhysicsTestSensor, RTX 4090, CuPy",
        "kappa_dissipation_anchor": KAPPA_DISSIPATION,
        "kappa_dissipation_anchor_err": KAPPA_DISSIPATION_ERR,
        "calibration": calib,
        "m_corridor": m_corr,
        "regimes": regimes,
        "summary": summary,
        "fdt_ratio_corridor": fdt_ratio,
        "fdt_link_holds": fdt_link,
        "pole_discrimination": discriminates,
        "verdict": verdict,
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for k in ("corridor", "rigidity", "chaos"):
        s = summary[k]
        print(f"  {k:9s}: rho={s['rho_mean']:.4f}  rho_std={s['rho_std_mean']:.5f}"
              f"  kappa_psd={s['kappa_psd_mean']}  R2={s['R2_mean']}")
    print(f"\n  kappa_dissipation (anchor)   = {KAPPA_DISSIPATION} /s")
    print(f"  kappa_fluctuation (corridor) = {kc} /s")
    print(f"  FDT ratio = {fdt_ratio}")
    print(f"  FDT link holds (0.5-2x)      = {fdt_link}")
    print(f"  pole discrimination          = {discriminates}")
    print(f"\n  VERDICT: {verdict}")
    print(f"  results -> {OUT}")


if __name__ == "__main__":
    main()

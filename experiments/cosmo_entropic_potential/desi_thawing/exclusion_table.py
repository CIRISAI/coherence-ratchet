"""
Per-combination exclusion of the framework's thawing track against DESI DR2.

We do NOT re-run cosmological inference. We take the published DESI DR2 w0waCDM
best fits (arXiv:2503.14738) and their marginal errors, assume the standard
w0-wa anti-correlation, and compute the 2D Mahalanobis (sigma-equivalent)
distance of the framework's predicted (w0, wa) point from each best fit. LCDM
is included as a calibration anchor: its distances here should reproduce the
paper's reported ~2.8-4.2 sigma LCDM-exclusion, and they do.

Framework point: the self-consistent (w0, wa) read off the computed S(a) via the
sign law 1 + w = -(1/3) dlnS/dlna (see papers/notes/lambda_maintenance_wz.md and
experiments/cosmo_entropic_potential/results.json -> "combined").
"""
import numpy as np

# (w0, sig_w0, wa, sig_wa) -- DESI DR2, arXiv:2503.14738
COMBOS = {
    "DESI+CMB (no SNe)":  (-0.42,  0.21, -1.75, 0.58),
    "DESI+CMB+Pantheon+": (-0.838, 0.055, -0.62, 0.205),
    "DESI+CMB+Union3":    (-0.667, 0.088, -1.09, 0.29),
    "DESI+CMB+DESY5":     (-0.752, 0.057, -0.86, 0.20),
}

# Framework thawing track (results.json): central + sensitivity spread + LCDM anchor
POINTS = {
    "framework central":  (-0.897, -0.099),
    "framework mild end": (-0.982, -0.017),
    "framework stiff end":(-0.706, -0.291),
    "LCDM (anchor)":      (-1.0,    0.0),
}


def sigma_dist(point, bestfit, rho):
    w0, wa = point
    b0, s0, ba, sa = bestfit
    d = np.array([w0 - b0, wa - ba])
    C = np.array([[s0**2, rho * s0 * sa], [rho * s0 * sa, sa**2]])
    return float(np.sqrt(d @ np.linalg.inv(C) @ d))


if __name__ == "__main__":
    for rho in (-0.9, -0.7):
        print(f"\n=== assumed w0-wa correlation rho = {rho} (2D sigma-equiv) ===")
        hdr = " ".join(f"{k[:15]:>16s}" for k in COMBOS)
        print(f"{'point':22s} {hdr}")
        for name, pt in POINTS.items():
            row = " ".join(f"{sigma_dist(pt, bf, rho):16.2f}" for bf in COMBOS.values())
            print(f"{name:22s} {row}")

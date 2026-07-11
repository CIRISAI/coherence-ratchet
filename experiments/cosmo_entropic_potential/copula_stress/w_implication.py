"""
Deliverable #4: does the copula gap move the S(a) / w(z) headline, and in which
direction? The sign law (lambda_maintenance_wz.md eq. 2):

    1 + w(a) = -(1/3) d ln S / d ln a.

The pipeline reads S_2pt(a) = 2 * I_gauss_copula(a) (the rank/2-point log-det).
The TRUE all-orders object is S_true(a) = 2 * I_true(a) = S_2pt(a) + 2*gap(a).
We compute d ln S / d ln a for BOTH on a fixed template held across redshift, and
report the shift in (1+w) today. A gap that GROWS toward low z steepens the rise of
S and pushes 1+w more negative (phantom, AWAY from DESI); a flat/shrinking gap does
not move the headline.

Reads results.json['tier3'], writes results.json['w_implication'].
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")


def dlnS_dlna(a, S):
    """central-difference d ln S / d ln a, evaluated at the last (lowest-z) point."""
    a = np.asarray(a); S = np.asarray(S)
    lnS = np.log(np.clip(S, 1e-12, None)); lna = np.log(a)
    # slope at the a=1 end via last two points
    return (lnS[-1] - lnS[-2]) / (lna[-1] - lna[-2])


def main():
    R = json.load(open(RESULTS))
    t = R.get("tier3")
    if not t:
        print("no tier3 yet"); return
    snaps = sorted(t["snapshots"], key=lambda s: s["z"])  # ascending z
    # group configs by (ng, template, sep) so we hold the geometry fixed across z
    keys = set()
    for s in snaps:
        for c in s["configs"]:
            keys.add((c["ng"], c["template"], c["sep"]))

    out = {"description": "S(a)/w(z) implication of the copula gap, per fixed template",
           "sign_law": "1+w = -(1/3) dlnS/dlna", "configs": []}
    for (ng, tmpl, sep) in sorted(keys):
        rows = []
        for s in snaps:
            for c in s["configs"]:
                if (c["ng"], c["template"], c["sep"]) == (ng, tmpl, sep):
                    rows.append((s["z"], c))
        rows.sort(key=lambda r: -r[0])   # a ascending => z descending
        if len(rows) < 3:
            continue
        z = np.array([r[0] for r in rows])
        a = 1.0 / (1.0 + z)
        I_gauss = np.array([r[1]["I_gauss_copula"] for r in rows])
        gap = np.array([r[1]["gap_matched"] for r in rows])
        S_2pt = 2 * I_gauss
        S_true = 2 * (I_gauss + gap)
        d2 = dlnS_dlna(a, S_2pt)
        dt = dlnS_dlna(a, S_true)
        w_2pt = -1 - d2 / 3.0
        w_true = -1 - dt / 3.0
        rec = dict(ng=ng, template=tmpl, sep=sep,
                   sep_mpc=float(rows[0][1]["separation_mpc"]),
                   z=list(map(float, z)),
                   S_2pt=list(map(float, S_2pt)),
                   gap_matched=list(map(float, gap)),
                   dlnS_dlna_2pt=float(d2), dlnS_dlna_true=float(dt),
                   w0_2pt=float(w_2pt), w0_true=float(w_true),
                   delta_w0=float(w_true - w_2pt),
                   gap_frac_of_S_today=float(2 * gap[-1] / max(S_2pt[-1], 1e-9)))
        out["configs"].append(rec)
        print(f"ng={ng} {tmpl} sep={sep} sepMpc={rec['sep_mpc']:.1f}: "
              f"dlnS/dlna 2pt={d2:+.3f} true={dt:+.3f} | "
              f"w0 2pt={w_2pt:+.3f} true={w_true:+.3f} (dw0={w_true-w_2pt:+.3f}) | "
              f"gap/S today={rec['gap_frac_of_S_today']:+.3f}")
    R["w_implication"] = out
    with open(RESULTS, "w") as f:
        json.dump(R, f, indent=2)
    print("\nwrote w_implication")


if __name__ == "__main__":
    main()

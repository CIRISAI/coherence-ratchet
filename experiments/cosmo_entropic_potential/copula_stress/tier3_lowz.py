"""Tier-3 low-z runner: measure the copula gap at the decisive redshifts
(z~0.5 peak, z=0) and merge into the existing tier3 (which has z=3). Reuses the
exact machinery of tier3_nbody.py; low-z FIRST so the redshift trend survives a
timeout. Incremental flush per snapshot."""
import json, os, time
import numpy as np
from copula_lib import cic_grid
import tier3_nbody as t3
line_template = t3.line_template
block_template = t3.block_template

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")
DATA = os.path.join(HERE, "..", "large_volume", "data")
BOX = 205.0
k_knn = 4
rng = np.random.default_rng(20260710)

# decisive redshifts: 067~z0.5 (S-peak), 099 z=0, plus 059~z0.7, 042~z1.36
order = ["099", "067", "059", "042", "033"]

res = json.load(open(RESULTS))
tier3 = res["tier3"]
done = {s["snap"] for s in tier3["snapshots"]}

ng_list = [16, 32, 48]
sep_list = [1, 2, 4]
m_line = 6

for s in order:
    if s in done:
        continue
    f = os.path.join(DATA, f"tng300_groups_{s}.npz")
    if not os.path.exists(f):
        print("missing", s); continue
    d = np.load(f); pos = d["pos"]; z = float(d["z"])
    rec_s = {"snap": s, "z": z, "n_halos": int(pos.shape[0]), "configs": []}
    t0 = time.time()
    for ng in ng_list:
        field = cic_grid(pos, BOX, ng, weights=None); cell = BOX / ng
        for sep in sep_list:
            if (m_line - 1) * sep >= ng:
                continue
            offs = line_template(m_line, sep)
            r = t3.measure_gap(field, offs, k_knn, rng, cell)
            r.update(ng=ng, template="line", sep=sep, separation_mpc=float(sep * cell))
            rec_s["configs"].append(r)
        offs = block_template(2)
        r = t3.measure_gap(field, offs, k_knn, rng, cell)
        r.update(ng=ng, template="block2", sep=1, separation_mpc=float(cell))
        rec_s["configs"].append(r)
    tier3["snapshots"].append(rec_s)
    res["tier3"] = tier3
    tmp = RESULTS + ".tmp"; json.dump(res, open(tmp, "w"), indent=1); os.replace(tmp, RESULTS)
    fine = [c for c in rec_s["configs"] if c["sep"] == 1 and c["template"] == "line" and c["ng"] == 48]
    fc = fine[0] if fine else rec_s["configs"][0]
    print(f"z={z:5.2f} DONE {time.time()-t0:.0f}s | finest(4.3Mpc) rbar={fc['mean_offdiag_rankcorr']:+.3f} "
          f"Igauss={fc['I_gauss_copula']:.3f} gap_m={fc['gap_matched']:+.4f} "
          f"({100*fc['gap_matched']/max(fc['I_gauss_copula'],1e-9):+.1f}%)", flush=True)
print("lowz done")

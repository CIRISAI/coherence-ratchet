"""
FIRST TOY MEASUREMENT of the coherence-ratchet double-entry EXCHANGE RATE.

  X = <within-halo x-v coherence DESTROYED per formation event (DEBIT)>
      / <inter-halo coordination CREATED per halo formed (CREDIT)>

This is a FIRST TOY-GRADE NUMBER with honest error bars, NOT a law. See SUMMARY.md
for the loud caveats and DECISIONS.md for methodological choices.

CREDIT side: on disk (TNG300-1), dS_total/dk in the formation epoch.
DEBIT side: TNG100-1 particle data. Track a FIXED set of DM particles (the main
progenitor's particles at z~1) forward to z~0.5 and measure the DROP in the x-v copula
S = -ln det C(x,y,z,vx,vy,vz) as that same material virializes. Grain reused verbatim
from experiments/dm_coherence/phasespace/phasespace_grain.py.

Incremental flush to results.json after every halo. TNG key read from env, never written.
"""
import os, io, json, time, sys
import numpy as np
import requests, h5py

KEY = os.environ["TNG_KEY"]
H = {"api-key": KEY}
BASE = "https://www.tng-project.org/api/TNG100-1/"
L = 75000.0          # ckpc/h box
h = 0.6774
SNAP_AFTER, Z_AFTER = 67, 0.5030    # virialized
SNAP_BEFORE, Z_BEFORE = 50, 0.9973  # assembling / infalling
RNG_SEED = 20260710
N_FIX = 5000         # fixed subsample across all halos and both epochs
N_ALT = 2000         # sensitivity test
OUT = os.path.join(os.path.dirname(__file__), "results.json")
RESULTS = {}

def flush():
    with open(OUT, "w") as f:
        json.dump(RESULTS, f, indent=2, default=float)

def get(url, params=None, tries=4):
    for t in range(tries):
        try:
            r = requests.get(url, headers=H, params=params, timeout=90)
            if r.status_code == 200:
                return r
            time.sleep(2 + 3*t)
        except Exception:
            time.sleep(2 + 3*t)
    raise RuntimeError("failed: " + url)

def S_of(C):
    sign, logdet = np.linalg.slogdet(np.atleast_2d(C))
    return np.inf if sign <= 0 else -logdet

def copula_S(dp, vv, N, rng):
    n = dp.shape[0]
    if n > N:
        idx = rng.choice(n, N, replace=False)
        dp, vv = dp[idx], vv[idx]
    X = np.column_stack([dp, vv])          # x,y,z,vx,vy,vz  (grain of phasespace_grain.py)
    return S_of(np.corrcoef(X, rowvar=False)), dp.shape[0]

def recenter(pos, c):
    return (pos - c + L/2) % L - L/2

def fetch_group(snap, grnr):
    r = get(BASE + "snapshots/%d/halos/%d/cutout.hdf5" % (snap, grnr),
            params={"dm": "Coordinates,Velocities,ParticleIDs"})
    f = h5py.File(io.BytesIO(r.content), "r")
    pos = f["PartType1/Coordinates"][:]; vel = f["PartType1/Velocities"][:]
    ids = f["PartType1/ParticleIDs"][:]
    f.close()
    return ids, pos, vel, len(r.content)

# ---------------------------------------------------------------- CREDIT (on disk)
def credit_side():
    lv = os.path.join(os.path.dirname(__file__), "..", "large_volume", "results.json")
    d = json.load(open(lv))
    recs = d["stage2_primary"]["records"]
    cap = d["cap"]
    thr = d["stage2_primary"]["thr"]
    # adjacent-pair dS/dk, excluding cap-saturated k and the declining (merger) branch
    pairs = []
    for i in range(len(recs)-1):
        a0, a1 = recs[i], recs[i+1]
        dk = a1["k"] - a0["k"]
        capped = (a1["k"] >= cap*0.999) or (a0["k"] >= cap*0.999)
        if dk > 0 and not capped:
            pairs.append(dict(a_lo=a0["a"], a_hi=a1["a"], z_lo=a0["z"], z_hi=a1["z"],
                              dS=a1["S"]-a0["S"], dk=dk, dSdk=(a1["S"]-a0["S"])/dk,
                              sbar_hi=a1["S"]/a1["k"]))
    # formation epoch = growing branch, z in ~0.5-1.7 (the double-entry-relevant window)
    form = [p for p in pairs if p["z_hi"] < 1.75 and p["dk"] > 0 and p["dSdk"] > 0]
    dSdk_vals = [p["dSdk"] for p in form]
    # jackknife spread on dS/dk using the stored jackknife S(a) realisations
    jk = d["stage2_primary"]["jackknife"]
    ks = [r["k"] for r in recs]
    jk_dSdk = []
    for key, Svals in jk.items():
        vv = []
        for i in range(len(recs)-1):
            if recs[i+1]["k"] >= cap*0.999 or recs[i]["k"] >= cap*0.999: continue
            if recs[i+1]["z"] >= 1.75: continue
            dk = ks[i+1]-ks[i]
            if dk > 0:
                vv.append((Svals[i+1]-Svals[i])/dk)
        if vv: jk_dSdk.append(np.mean(vv))
    credit = float(np.mean(dSdk_vals))
    credit_sd = float(np.std(dSdk_vals))
    jk_sd = float(np.std(jk_dSdk)) if jk_dSdk else None
    RESULTS["credit"] = dict(
        note="dS_total/dk = nats added to inter-halo halo-grain ledger per halo formed, "
             "TNG300-1 threshold %.3e Msun/h, formation epoch z<1.75 growing branch, cap-excluded" % thr,
        threshold_Msun_over_h=thr, snap_pairs=form,
        dSdk_mean_nats_per_halo=credit, dSdk_sd_across_pairs=credit_sd,
        dSdk_jackknife_sd=jk_sd,
        sbar_per_halo_nats=float(np.mean([p["sbar_hi"] for p in form])))
    flush()
    print("CREDIT dS/dk = %.4f +/- %.4f (pair spread) nats/halo formed" % (credit, credit_sd))
    return credit, credit_sd

# ------------------------------------------------------------- sample selection
def select_halos(n_target=18, pool=30):
    r = get(BASE + "snapshots/%d/subhalos/" % SNAP_AFTER,
            params={"limit": pool, "primary_flag": 1, "mass__gt": 33,
                    "mass__lt": 70, "order_by": "-mass"})
    cands = [x["id"] for x in r.json()["results"]]
    sel = []
    for sid in cands:
        if len(sel) >= n_target: break
        try:
            rr = get(BASE + "snapshots/%d/subhalos/%d/sublink/mpb.hdf5" % (SNAP_AFTER, sid))
            f = h5py.File(io.BytesIO(rr.content), "r")
            snaps = f["SnapNum"][:]; m200 = f["Group_M_Crit200"][:]; grnr = f["SubhaloGrNr"][:]
            def at(sn):
                i = np.where(snaps == sn)[0]
                return (float(m200[i[0]]), int(grnr[i[0]])) if len(i) else (None, None)
            m67, g67 = at(SNAP_AFTER); m50, g50 = at(SNAP_BEFORE); f.close()
            if m67 and m50:
                p67, p50 = m67/h*1e10, m50/h*1e10
                if 5e11 < p67 < 1.15e12:
                    sel.append(dict(subid=sid, grnr_after=g67, grnr_before=g50,
                                    M200c_after_Msun=p67, M200c_before_Msun=p50,
                                    crossed_7e11=bool(p50 < 7e11 < p67)))
        except Exception as e:
            print("  skip", sid, e)
    RESULTS["sample"] = dict(snap_before=SNAP_BEFORE, z_before=Z_BEFORE,
                             snap_after=SNAP_AFTER, z_after=Z_AFTER,
                             N_fix=N_FIX, N_alt=N_ALT, halos=sel)
    flush()
    print("selected %d halos (%d crossed 7e11 in the window)" %
          (len(sel), sum(x["crossed_7e11"] for x in sel)))
    return sel

# ------------------------------------------------------------- DEBIT per halo
def debit_side(sel):
    rng = np.random.default_rng(RNG_SEED)
    rng2 = np.random.default_rng(RNG_SEED)   # independent stream for N_ALT
    per = []
    for k, hlo in enumerate(sel):
        try:
            ids_b, pos_b, vel_b, nb = fetch_group(SNAP_BEFORE, hlo["grnr_before"])
            ids_a, pos_a, vel_a, na = fetch_group(SNAP_AFTER, hlo["grnr_after"])
        except Exception as e:
            print("  fetch fail halo", hlo["subid"], e); continue
        cen_b = np.median(pos_b, axis=0); cen_a = np.median(pos_a, axis=0)
        common, ia, ib = np.intersect1d(ids_a, ids_b, return_indices=True)
        if len(common) < N_FIX:
            print("  too few tracked (%d) halo %d" % (len(common), hlo["subid"])); continue
        dp_b = recenter(pos_b[ib], cen_b); vv_b = vel_b[ib]
        dp_a = recenter(pos_a[ia], cen_a); vv_a = vel_a[ia]
        S_b, nu = copula_S(dp_b, vv_b, N_FIX, rng)
        S_a, _  = copula_S(dp_a, vv_a, N_FIX, rng)
        # N sensitivity
        S_b2, _ = copula_S(dp_b, vv_b, N_ALT, rng2)
        S_a2, _ = copula_S(dp_a, vv_a, N_ALT, rng2)
        rec = dict(subid=hlo["subid"], M200c_after_Msun=hlo["M200c_after_Msun"],
                   M200c_before_Msun=hlo["M200c_before_Msun"], crossed_7e11=hlo["crossed_7e11"],
                   n_progenitor=int(len(ids_b)), n_tracked=int(len(common)),
                   frac_survive=float(len(common)/len(ids_b)),
                   S_before=float(S_b), S_after=float(S_a), debit_nats=float(S_b - S_a),
                   S_before_N2000=float(S_b2), S_after_N2000=float(S_a2),
                   debit_nats_N2000=float(S_b2 - S_a2))
        per.append(rec)
        RESULTS["debit_per_halo"] = per
        flush()
        print("  halo %d  M200c_after=%.2fe11  debit=%+.4f  (before %.3f -> after %.3f)  survive %.0f%%"
              % (hlo["subid"], hlo["M200c_after_Msun"]/1e11, S_b-S_a, S_b, S_a, 100*len(common)/len(ids_b)))
    return per

def summarize(per, credit, credit_sd):
    deb = np.array([p["debit_nats"] for p in per])
    deb2 = np.array([p["debit_nats_N2000"] for p in per])
    debit = float(np.mean(deb)); debit_sd = float(np.std(deb))
    debit_se = debit_sd/np.sqrt(len(deb))
    X = debit/credit
    # error propagation (independent): rel var add
    relvar = (debit_se/debit)**2 + (credit_sd/credit)**2 if debit != 0 else float("nan")
    X_err = abs(X)*np.sqrt(relvar)
    RESULTS["exchange_rate"] = dict(
        n_halos=len(per),
        debit_mean_nats_per_halo=debit, debit_sd=debit_sd, debit_se=debit_se,
        debit_mean_N2000=float(np.mean(deb2)),
        credit_nats_per_halo=credit, credit_sd=credit_sd,
        X_nats_debit_per_nat_credit=X, X_err=float(X_err),
        frac_positive_debit=float(np.mean(deb > 0)),
        note="FIRST TOY MEASUREMENT. X = within-halo x-v coherence destroyed per unit "
             "inter-halo coordination created, per formation event.")
    flush()
    print("\n=== EXCHANGE RATE (FIRST TOY) ===")
    print("DEBIT  = %.4f +/- %.4f nats/halo (sd %.4f, n=%d, %.0f%% positive)"
          % (debit, debit_se, debit_sd, len(deb), 100*np.mean(deb > 0)))
    print("CREDIT = %.4f +/- %.4f nats/halo" % (credit, credit_sd))
    print("X      = %.3f +/- %.3f  (nats debit per nat credit)" % (X, X_err))
    print("N-sensitivity: debit(N=5000)=%.4f  debit(N=2000)=%.4f" % (debit, float(np.mean(deb2))))

if __name__ == "__main__":
    RESULTS["title"] = "FIRST TOY MEASUREMENT: double-entry exchange rate (coherence-ratchet)"
    RESULTS["date"] = "2026-07-10"
    flush()
    credit, credit_sd = credit_side()
    sel = select_halos()
    per = debit_side(sel)
    if per:
        summarize(per, credit, credit_sd)
    print("done ->", OUT)

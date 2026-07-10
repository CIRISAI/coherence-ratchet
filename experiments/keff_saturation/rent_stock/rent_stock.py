#!/usr/bin/env python3
"""
RENT TRACKS STOCK? — the neural-rung replication of exp118 (LedgerLaw clause 5).

Clause 5 ("THE INTERIOR IS RENTED") is an algebraic tautology given the posited ODE
dρ/dt = α − γM: at a zero of the drift, γM = α.  Its *interpretive* load — carried in
LedgerLaw.lean as "the rent tracks the held STOCK (moderate confidence)" and in the
ReceiptsReading as `the_rent_is_itemized` — rests on **exactly one substrate**: exp118,
a 16-sensor GPU timing array, 12 points, P_maint vs S_held partial r = +0.84 controlling
rate and temperature.

THE PREDICTION (rent-tracks-stock), stated so it can fail:
    Across windows, WITHIN a session, the maintenance signal (γM proxy) correlates
    POSITIVELY with the held coordination stock S, controlling for epoch/time.

THE SUBSTRATE: macaque 128-ch subdural ECoG (NeuroTycho, Yanagawa/Fujii, RIKEN),
continuous Session2 through anesthetic induction, for 2 animals x 2 agents:
    Chibi  propofol 20120730PF   Chibi  ketamine 20120719KT
    George propofol 20120731PF   George ketamine 20120724KT

STOCK, two routes (k = 128 channels, stated):
  (a) S_closed  — invert Kish:  ρ_Kish = (k − k_eff) / (k_eff (k − 1))
                  then          S = −ln(1 + ρ(k−1)) − (k−1) ln(1 − ρ)
                  This is −ln det of the EQUICORRELATION matrix carrying that ρ.
                  NOTE (stated, not hidden): S_closed is a strictly INCREASING function
                  of ρ_Kish, which is a strictly DECREASING function of k_eff.  Hence a
                  *Spearman* partial against S_closed is, identically, minus the Spearman
                  partial against k_eff.  The closed route therefore adds no rank
                  information beyond k_eff.  It is reported because the scan specified it.
  (b) S_direct  — the real thing: S = −ln det C = −Σ_i ln λ_i on the window's 128×128
                  channel correlation matrix.  NOT a monotone function of k_eff.  Needs
                  the raw ECoG; recomputed here.  This is the preferred stock.

MAINTENANCE (γM proxy), four routes.  Caveat (i) of the scan is mandatory and load-bearing:
a detailed-balance |z| is a SIGNIFICANCE score, not an entropy-production RATE; it conflates
effect size with the surrogate noise floor.  So we report, alongside the two published |z|:
  z_wind    |z| of the net winding rate  (published; entropy_production.irreversibility_from_units)
  z_circ    |z| of the summed circulation vs phase-randomized null (published; the "trustworthy" one)
  mag_wind  |winding rate| × fs           [rad/s]   — a RATE, no null, no noise floor
  mag_circ  Σ_pairs |ω_ij| × fs           [rad/s]   — a RATE, no null, no noise floor
  epr       plug-in D_KL(P_ij ‖ P_ji) × fs [nats/s] — a genuine entropy-production RATE,
            coarse-grained on the top-2 SVD modes × 3 quantile bins (9 states), debiased
            against a detailed-balance (symmetrized-Markov) surrogate floor.  Bias is
            documented and subtracted; the raw and debiased values are both stored.

STATISTICS
  Primary: within-session SPEARMAN PARTIAL corr(maintenance, S | time).  Time is the
  confound the scan names: both drift with induction.  Window index ≡ rank(t_center), so
  controlling for rank(t) *is* controlling for epoch order.
  Secondary: additionally residualize on epoch dummies (awake/induction/deep).
  CIs: MOVING BLOCK BOOTSTRAP over windows (20 s windows at 5 s step ⇒ 75% overlap ⇒
  strong autocorrelation).  Block length L chosen per session from the integrated
  autocorrelation time (Sokal window) of the two rank series; L and τ_int are reported.
  Pooling: fixed-effect inverse-variance Fisher-z using the bootstrap SE of atanh(r)
  (the SE already carries the autocorrelation).  DerSimonian–Laird random effects and
  Cochran's Q / I² are reported alongside, because 4 sessions cannot estimate τ² well and
  the heterogeneity IS the result.

CAVEAT (ii), enforced structurally: ECoG is a mesoscopic FIELD; absolute correlation is
inflated and reference-confounded.  Only WITHIN-session variation is read.  No absolute S
is compared across sessions or animals anywhere in this script or its outputs.

No tuning.  Fixed seed.  Real data only.  A FAIL is a result.
"""
import os, sys, json, glob, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
sys.path.insert(0, PARENT)

SEED = 20260710
FS = 250.0                      # decimated rate used by the trajectory pipeline
K_CHANNELS = 128                # stated: k = number of ECoG channels

# ---------------------------------------------------------------- stock
def S_closed(rho, k=K_CHANNELS):
    """−ln det of the equicorrelation matrix with correlation rho.  Strictly
    increasing in rho on (0, 1)."""
    rho = np.asarray(rho, float)
    return -np.log1p(rho * (k - 1)) - (k - 1) * np.log1p(-rho)

def rho_kish(k_eff, k=K_CHANNELS):
    """Invert Kish: k_eff = k / (1 + rho(k−1))  ⇒  rho = (k − k_eff)/(k_eff (k−1))."""
    k_eff = np.asarray(k_eff, float)
    return (k - k_eff) / (k_eff * (k - 1))

# ---------------------------------------------------------------- rank stats
def _rank(x):
    from scipy.stats import rankdata
    return rankdata(np.asarray(x, float))

def _resid(y, X):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta

def spearman_partial(x, y, controls):
    """Spearman partial: rank-transform x,y; residualize both on [1, controls]; Pearson.
    `controls` is a (n, p) design of already-appropriate columns (ranks / dummies)."""
    rx, ry = _rank(x), _rank(y)
    X = np.column_stack([np.ones(len(rx))] + [np.asarray(c, float) for c in controls.T])
    ex, ey = _resid(rx, X), _resid(ry, X)
    sx, sy = ex.std(), ey.std()
    if sx < 1e-12 or sy < 1e-12:
        return np.nan
    return float(np.dot(ex, ey) / (len(ex) * sx * sy))

def tau_int(x, cmax=None):
    """Integrated autocorrelation time with an automatic Sokal window."""
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    if x.std() < 1e-12:
        return 1.0
    f = np.fft.rfft(x, 2 * n)
    acf = np.fft.irfft(f * np.conj(f))[:n].real
    acf /= acf[0]
    c = 5.0 if cmax is None else cmax
    tau = 1.0
    for M in range(1, n):
        tau = 1.0 + 2.0 * acf[1:M + 1].sum()
        if M >= c * max(tau, 1.0):
            break
    return float(max(tau, 1.0))

def block_len(series_list, n):
    """L = ceil(2 * max tau_int) over the supplied series, clipped to [4, n//5].
    Floor of 4: the windows overlap 75%, so 4 consecutive windows share no sample."""
    t = max(tau_int(s) for s in series_list)
    L = int(np.ceil(2.0 * t))
    return int(np.clip(L, 4, max(5, n // 5))), float(t)

def block_bootstrap_partial(x, y, t, epoch_dummies, L, nboot=2000, seed=SEED, use_epoch=False):
    """Moving-block bootstrap over window index.  Recompute the partial on each replicate,
    rebuilding rank(t) and the dummies from the resampled rows."""
    rng = np.random.default_rng(seed)
    n = len(x)
    nb = int(np.ceil(n / L))
    out = np.empty(nboot)
    for b in range(nboot):
        starts = rng.integers(0, n - L + 1, nb)
        idx = np.concatenate([np.arange(s, s + L) for s in starts])[:n]
        xb, yb, tb = x[idx], y[idx], t[idx]
        ctrl = [_rank(tb)]
        if use_epoch:
            for j in range(epoch_dummies.shape[1]):
                ctrl.append(epoch_dummies[idx, j])
        C = np.column_stack(ctrl)
        # guard: a replicate can lose an epoch level -> constant dummy column
        keep = [j for j in range(C.shape[1]) if C[:, j].std() > 1e-12]
        out[b] = spearman_partial(xb, yb, C[:, keep])
    return out[np.isfinite(out)]

def fisher_pool(rs, ses):
    """Fixed-effect inverse-variance Fisher-z + DerSimonian-Laird RE + Cochran Q."""
    z = np.arctanh(np.clip(np.asarray(rs, float), -0.999999, 0.999999))
    se = np.asarray(ses, float)
    w = 1.0 / se ** 2
    zf = float(np.sum(w * z) / np.sum(w))
    se_f = float(np.sqrt(1.0 / np.sum(w)))
    Q = float(np.sum(w * (z - zf) ** 2))
    df = len(z) - 1
    C = float(np.sum(w) - np.sum(w ** 2) / np.sum(w))
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    I2 = float(max(0.0, (Q - df) / Q) * 100) if Q > 0 else 0.0
    wr = 1.0 / (se ** 2 + tau2)
    zr = float(np.sum(wr * z) / np.sum(wr))
    se_r = float(np.sqrt(1.0 / np.sum(wr)))
    from scipy.stats import norm, chi2
    return dict(
        fe_r=float(np.tanh(zf)), fe_z=zf, fe_se=se_f,
        fe_ci=[float(np.tanh(zf - 1.96 * se_f)), float(np.tanh(zf + 1.96 * se_f))],
        fe_p=float(2 * norm.sf(abs(zf / se_f))),
        re_r=float(np.tanh(zr)), re_se=se_r,
        re_ci=[float(np.tanh(zr - 1.96 * se_r)), float(np.tanh(zr + 1.96 * se_r))],
        re_p=float(2 * norm.sf(abs(zr / se_r))),
        Q=Q, Q_df=df, Q_p=float(chi2.sf(Q, df)) if df > 0 else 1.0,
        I2_pct=I2, tau2=tau2)

# ---------------------------------------------------------------- raw recompute
_RAW = {}
def _lazy_raw():
    """Import the trajectory module verbatim so preprocessing is bit-identical."""
    if not _RAW:
        os.environ.setdefault("TRAJ_FS", "250.0")
        os.environ.setdefault("TRAJ_BAND", "1,100")
        import spectral_anesthesia_trajectory as T
        import entropy_production as ep
        from spectral_test import corr_eig, participation_ratio
        _RAW.update(T=T, ep=ep, corr_eig=corr_eig, pr=participation_ratio)
    return _RAW["T"], _RAW["ep"], _RAW["corr_eig"], _RAW["pr"]

def epr_plugin(traj2, n_bins=3, nsim=32, seed=0):
    """Plug-in entropy production rate, per transition, on a coarse-grained state space.

    EP = Σ_ij P_ij ln(P_ij / P_ji)  (Lynn et al. 2021 PNAS estimator; reuses the
    discretize/_counts/_ep helpers already validated in entropy_production.py).

    BIAS: the plug-in EP is positively biased at finite T, because sampling noise alone
    makes P_ij ≠ P_ji even under detailed balance.  We estimate the bias directly, as the
    entropy_production docstring prescribes: symmetrize the observed transition counts
    (a chain with detailed balance BY CONSTRUCTION, same stationary distribution and same
    dwell structure), simulate `nsim` trajectories of the same length from it, recompute
    EP → floor_mean IS the finite-sample bias, floor_sd its spread.  Reported `epr` =
    EP_obs − floor_mean, per transition.  With T ≈ 5000 transitions and M = 9 states the
    floor is O(M²/2T) ≈ 0.01 nats/transition — small, but the same order as some observed
    EPs, so it is subtracted rather than ignored, and both raw and floor are stored.
    """
    _, ep, _, _ = _lazy_raw()
    rng = np.random.default_rng(seed)
    states = ep.discretize(traj2, n_bins)
    M = n_bins ** traj2.shape[1]
    C = ep._counts(states, M)
    eps = 1e-9
    ep_obs = ep._ep(C, eps)

    Csym = 0.5 * (C + C.T)
    row = Csym.sum(1)
    live = row > 0
    P = np.zeros((M, M))
    P[live] = Csym[live] / row[live, None]
    P[~live] = 1.0 / M                      # dead states: uniform (never entered anyway)
    pi = row / row.sum()
    cdf = np.cumsum(P, axis=1)
    cdf[:, -1] = 1.0
    T = len(states)
    # all nsim chains advanced together: T python steps, each vectorized over nsim
    s = np.searchsorted(np.cumsum(pi), rng.random(nsim))
    chains = np.empty((nsim, T), dtype=np.int64)
    chains[:, 0] = s
    U = rng.random((T, nsim))
    for t in range(1, T):
        s = (cdf[s] < U[t][:, None]).sum(1)
        chains[:, t] = s
    floor = np.array([ep._ep(ep._counts(chains[b], M), eps) for b in range(nsim)])
    fm, fs = float(floor.mean()), float(floor.std())
    return dict(ep_raw=float(ep_obs), floor_mean=fm, floor_sd=fs,
                epr=float(ep_obs - fm), epr_z=float((ep_obs - fm) / (fs + 1e-12)),
                n_states=int(M), n_trans=int(T - 1))

def circ_magnitude(seg, k=4, npair=3):
    """Σ over the 3 top-mode pairs of |ω_ij|, the SAME ω that
    spectral_anesthesia_trajectory.circ_db normalises into its z — but the raw magnitude,
    with no surrogate denominator.  ω = ⟨x dy − y dx⟩ / ⟨x² + y²⟩ is rad per sample."""
    T, _, _, _ = _lazy_raw()
    A = T._modes_local(seg, k)
    tot, per = 0.0, []
    for i in range(npair):
        for j in range(i + 1, npair):
            w = T._omega(A[i], A[j])
            per.append(float(w)); tot += abs(w)
    return float(tot), per

def recompute_session(raw_root, agent, jsonl_rows, cache_dir, verbose=True):
    """Recompute per-window S_direct + rate-valued maintenance from the raw ECoG.
    Windows are regenerated by the same rule as the original run and CHECKED against the
    published k_eff and winding |z|, so pipeline drift is caught, not papered over."""
    T, ep, corr_eig, participation_ratio = _lazy_raw()
    s2 = T.session_dir(raw_root, 2)
    if s2 is None:
        return None, {"error": "no Session2"}
    cache = os.path.join(cache_dir, f"M_{agent}_{os.path.basename(raw_root)}.npy")
    if os.path.exists(cache):
        M = np.load(cache)
    else:
        M, _chans, _segs, _bare = T.build_session(s2, T.BAND)
        M = M[T.good_mask(M)]
        np.save(cache, M)
    segs, bare = T.read_conditions(s2)
    inj = next((t for lab, t in bare if "Injection" in lab and "Antagonist" not in lab), None)
    deep_t0, deep_t1 = next(((t0, t1) for base, t0, t1 in segs if base == "Anesthetized"), (None, None))

    N, Ttot = M.shape
    win, step = int(T.WIN_SEC * T.FS), int(T.STEP_SEC * T.FS)
    starts = [s for s in range(0, Ttot - win + 1, step)]
    if deep_t1 is not None:
        starts = [s for s in starts if (s + win) / T.FS <= deep_t1 + 5]
    assert len(starts) == len(jsonl_rows), f"{agent}: {len(starts)} starts vs {len(jsonl_rows)} rows"

    out = []
    t0 = time.time()
    for wi, s0 in enumerate(starts):
        seg = M[:, s0:s0 + win]
        evs, _Nn, _Tn = corr_eig(seg)
        keff = float(participation_ratio(evs))
        lam = np.clip(evs, 1e-12, None)
        s_direct = float(-np.log(lam).sum())
        mag_c, _per = circ_magnitude(seg, k=T.DB_K)
        w = ep.irreversibility_from_units(seg, k=T.DB_K, seed=0)
        modes2 = ep.top_modes(seg, k=2)
        e = epr_plugin(modes2, n_bins=3, nsim=32, seed=SEED + wi)
        out.append(dict(
            w=wi, k_eff_recomputed=keff, S_direct=s_direct,
            mag_circ_rad_per_s=mag_c * T.FS,
            mag_wind_rad_per_s=float(abs(w["winding_rate"])) * T.FS,
            epr_nats_per_s=e["epr"] * T.FS,
            epr_raw_nats_per_s=e["ep_raw"] * T.FS,
            epr_floor_nats_per_s=e["floor_mean"] * T.FS,
            epr_z=e["epr_z"], n_states=e["n_states"], n_trans=e["n_trans"],
            wind_z_recomputed=float(w["z"]),
            k_eff_published=jsonl_rows[wi]["k_eff"],
            wind_z_published=jsonl_rows[wi]["db_z_winding"]))
        if verbose and (wi % 40 == 0 or wi == len(starts) - 1):
            print(f"    {agent} w{wi:3d}/{len(starts)} keff={keff:6.3f} "
                  f"(Δpub={abs(keff-jsonl_rows[wi]['k_eff']):.1e}) S_dir={s_direct:7.2f} "
                  f"magC={mag_c*T.FS:.4f} EPR={e['epr']*T.FS:.4f} "
                  f"floor={e['floor_mean']*T.FS:.4f} [{time.time()-t0:.0f}s]", flush=True)
    dk = np.array([abs(r["k_eff_recomputed"] - r["k_eff_published"]) for r in out])
    dz = np.array([abs(r["wind_z_recomputed"] - r["wind_z_published"]) for r in out])
    return out, dict(max_abs_keff_delta=float(dk.max()), median_abs_keff_delta=float(np.median(dk)),
                     max_abs_windz_delta=float(dz.max()),
                     n_windows=len(out), injection_t=inj, deep=[deep_t0, deep_t1],
                     n_channels_used=int(N), elapsed_s=float(time.time() - t0))

# ---------------------------------------------------------------- driver
PROXIES = [("z_circ", "|z| circulation (published)", "significance"),
           ("z_wind", "|z| winding (published)", "significance"),
           ("mag_circ", "Σ|ω| circulation rate [rad/s]", "rate"),
           ("mag_wind", "|winding rate| [rad/s]", "rate"),
           ("epr", "plug-in EPR, debiased [nats/s]", "rate")]

def load_sessions(base):
    S = {}
    for animal, tag in [("chibi", ""), ("george", "_george")]:
        for agent in ["propofol", "ketamine"]:
            p = os.path.join(base, f"trajectory_windows_{agent}{tag}.jsonl")
            rows = [json.loads(l) for l in open(p)]
            S[(animal, agent)] = rows
    return S

def analyse(name, rows, raw, nboot):
    n = len(rows)
    t = np.array([r["t_center"] for r in rows])
    keff = np.array([r["k_eff"] for r in rows])
    rho = rho_kish(keff)
    s_cl = S_closed(rho)
    ep_lbl = [r["epoch"] for r in rows]
    lev = ["awake", "induction", "deep"]
    D = np.column_stack([[1.0 if e == l else 0.0 for e in ep_lbl] for l in lev[1:]])

    maint = {"z_circ": np.abs([r["db_z_circ_sum"] for r in rows]),
             "z_wind": np.abs([r["db_z_winding"] for r in rows])}
    stocks = {"S_closed": s_cl}
    if raw is not None:
        maint["mag_circ"] = np.array([r["mag_circ_rad_per_s"] for r in raw])
        maint["mag_wind"] = np.array([r["mag_wind_rad_per_s"] for r in raw])
        maint["epr"] = np.array([r["epr_nats_per_s"] for r in raw])
        stocks["S_direct"] = np.array([r["S_direct"] for r in raw])

    res = {"n_windows": n, "epochs": {l: int(sum(e == l for e in ep_lbl)) for l in lev},
           "t_span_s": [float(t.min()), float(t.max())],
           "k_channels": K_CHANNELS,
           "keff_range": [float(keff.min()), float(keff.max())],
           "rho_kish_range": [float(rho.min()), float(rho.max())],
           "S_closed_range": [float(s_cl.min()), float(s_cl.max())],
           "partials": {}, "descriptives": {}}
    if "S_direct" in stocks:
        sd = stocks["S_direct"]
        res["S_direct_range"] = [float(sd.min()), float(sd.max())]
        res["spearman_Sdirect_vs_Sclosed"] = float(np.corrcoef(_rank(sd), _rank(s_cl))[0, 1])
        res["spearman_Sdirect_vs_keff"] = float(np.corrcoef(_rank(sd), _rank(keff))[0, 1])

    for mk, mv in maint.items():
        res["descriptives"][mk] = {
            "awake_median": float(np.median(mv[[e == "awake" for e in ep_lbl]])) if any(e == "awake" for e in ep_lbl) else None,
            "deep_median": float(np.median(mv[[e == "deep" for e in ep_lbl]])),
            "all_median": float(np.median(mv))}

    for sk, sv in stocks.items():
        for mk, mv in maint.items():
            L, tau = block_len([_rank(mv), _rank(sv)], n)
            ctrl_t = np.column_stack([_rank(t)])
            r_t = spearman_partial(mv, sv, ctrl_t)
            r_te = spearman_partial(mv, sv, np.column_stack([_rank(t), D]))
            bt = block_bootstrap_partial(mv, sv, t, D, L, nboot=nboot, use_epoch=False)
            bte = block_bootstrap_partial(mv, sv, t, D, L, nboot=nboot, use_epoch=True,
                                          seed=SEED + 7)
            zb = np.arctanh(np.clip(bt, -0.999999, 0.999999))
            res["partials"][f"{mk}|{sk}"] = dict(
                r_partial_time=r_t, r_partial_time_epoch=r_te,
                ci95=[float(np.percentile(bt, 2.5)), float(np.percentile(bt, 97.5))],
                ci95_time_epoch=[float(np.percentile(bte, 2.5)), float(np.percentile(bte, 97.5))],
                boot_se_fisherz=float(zb.std()),
                p_boot_sign=float(2 * min(np.mean(bt <= 0), np.mean(bt >= 0))),
                block_len=L, tau_int=tau, n_boot=len(bt),
                raw_spearman=float(np.corrcoef(_rank(mv), _rank(sv))[0, 1]))
    return res

def main():
    base = PARENT
    nboot = int(os.environ.get("RS_NBOOT", 2000))
    scratch = os.environ.get("RS_SCRATCH",
        "/tmp/claude-1000/-home-emoore-RATCHET/75f07b43-c0f5-4052-9346-528e61302ccd/scratchpad")
    cache = os.path.join(scratch, "cache"); os.makedirs(cache, exist_ok=True)

    OLD = ("/tmp/claude-1000/-home-emoore-coherence-ratchet/"
           "a15f19f3-8fff-4354-9d5c-e860763082eb/scratchpad/neuro")
    NEW = os.path.join(scratch, "neuro")
    RAW = {("george", "propofol"): os.path.join(OLD, "GEO_PF_ext"),
           ("george", "ketamine"): os.path.join(OLD, "GEO_KT_ext"),
           ("chibi", "propofol"): os.path.join(NEW, "PF_ext"),
           ("chibi", "ketamine"): os.path.join(NEW, "KT_ext")}

    sess = load_sessions(base)
    print("=== DATA INVENTORY ===")
    for kk, rows in sess.items():
        print(f"  {kk[0]:7s} {kk[1]:9s}  N={len(rows):4d} windows  "
              f"t=[{rows[0]['t_center']:.0f},{rows[-1]['t_center']:.0f}]s  k={K_CHANNELS} ch")

    raws, recon = {}, {}
    for kk, root in RAW.items():
        ok = os.path.isdir(root) and glob.glob(os.path.join(root, "**", "Session2"), recursive=True)
        if not ok:
            print(f"  [raw MISSING] {kk} -> {root}"); raws[kk] = None; continue
        print(f"\n=== RAW RECOMPUTE {kk} ===", flush=True)
        r, meta = recompute_session(root, kk[1], sess[kk], cache)
        raws[kk] = r; recon["/".join(kk)] = meta
        print(f"  pipeline check: max|Δk_eff| vs published = {meta['max_abs_keff_delta']:.3e}")

    results = {"meta": dict(
        seed=SEED, fs=FS, k_channels=K_CHANNELS, n_boot=nboot,
        hypothesis="rent-tracks-stock: partial corr(maintenance, S | time) > 0 within session",
        stock_closed="S = -ln(1+rho(k-1)) - (k-1)ln(1-rho), rho = (k-k_eff)/(k_eff(k-1))",
        stock_direct="S = -ln det C = -sum ln lambda_i on the 128x128 window corr matrix",
        maintenance=[dict(key=k, label=l, kind=t) for k, l, t in PROXIES],
        note_monotone=("S_closed is a strictly increasing function of rho_Kish, itself strictly "
                       "decreasing in k_eff; therefore Spearman-partial(m, S_closed | t) = "
                       "-Spearman-partial(m, k_eff | t) EXACTLY. Only S_direct adds rank information."),
        caveat_i="DB |z| is a significance score, not a rate; rate proxies (mag_*, epr) are the disciplined read",
        caveat_ii="ECoG field grain: within-session variation only; no absolute S compared across sessions",
        recompute_check=recon), "sessions": {}}

    for kk, rows in sess.items():
        nm = "/".join(kk)
        print(f"\n=== ANALYSE {nm} ===", flush=True)
        results["sessions"][nm] = analyse(nm, rows, raws[kk], nboot)
        for pk, pv in results["sessions"][nm]["partials"].items():
            print(f"   {pk:22s} r={pv['r_partial_time']:+.3f} "
                  f"CI[{pv['ci95'][0]:+.3f},{pv['ci95'][1]:+.3f}] L={pv['block_len']}")

    # ------- pooling
    pools = {}
    for sk in ["S_closed", "S_direct"]:
        for mk, _, _ in PROXIES:
            key = f"{mk}|{sk}"
            items = [(nm, s["partials"][key]) for nm, s in results["sessions"].items()
                     if key in s["partials"]]
            if len(items) < 2: continue
            rs = [p["r_partial_time"] for _, p in items]
            ses = [max(p["boot_se_fisherz"], 1e-6) for _, p in items]
            pools[key] = dict(sessions=[nm for nm, _ in items], r=rs, se_fisherz=ses,
                              **fisher_pool(rs, ses))
            for agent in ["propofol", "ketamine"]:
                sub = [(nm, p) for nm, p in items if nm.endswith(agent)]
                if len(sub) >= 2:
                    pools[key][f"pooled_{agent}"] = fisher_pool(
                        [p["r_partial_time"] for _, p in sub],
                        [max(p["boot_se_fisherz"], 1e-6) for _, p in sub])
    results["pooled"] = pools

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    print("\nwrote results.json")

    dump = {"/".join(k): v for k, v in raws.items() if v}
    if dump:
        with open(os.path.join(HERE, "raw_window_metrics.json"), "w") as f:
            json.dump(dump, f)
        print("wrote raw_window_metrics.json")
    return results

if __name__ == "__main__":
    main()

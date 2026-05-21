"""
measure_timescale_gj.py — Paths 2-3, Pair B: the canonical TIMESCALE g/J at the
LLM internal -> external rung pair (A3int -> A3ext).

Canonical Claim 6 quantity (StructuralClaims.lean + PROTOCOL.md): g and J as
TIMESCALES. g = cross-rung coupling (internal drives external); J = within-rung
relaxation rate (relaxation timescale^-1). Path 1 measured a coupling RATIO;
this run measures the canonical timescale ratio at the only runnable pair.

The time axis is the GENERATED token sequence: each model generates N_GEN
tokens autoregressively with output_hidden_states. Token position is time t.

Constructions, the window-domination GATE, and the verdict rule are fixed by
PREREGISTRATION.md (committed in a preceding commit; git history is the proof).
Real open HuggingFace weights only. Honest null is a valid outcome.
"""
import functools
import json
import pathlib
import sys

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print = functools.partial(print, flush=True)

HERE = pathlib.Path(__file__).resolve().parent
# Path 1's audited estimators, reused verbatim for the coupling-ratio g/J
sys.path.insert(0, str(HERE.parent / "path1_tau"))
from crossrung_lib import within_rung_W, cross_rung_tau  # noqa: E402

# ---- fixed parameters (PREREGISTRATION.md §7; no tuning) -------------------
SEED = 17
N_GEN = 512
LAYER_FRAC = 0.5            # mid-depth layer = num_hidden_layers // 2
D_SUB = 256                 # hidden-unit / logit-coord subsample
W_TOK = 32                  # family II sliding window
MARGIN = 2.0                # window-domination gate margin
N_SHUFFLE = 50              # g block-shuffle null
N_SURROGATE = 100           # phase-randomised surrogate null for tau_ac
BLOCK = 16                  # g null block length
MODELS = ["gpt2", "EleutherAI/pythia-160m", "Qwen/Qwen2.5-0.5B"]

PROMPTS = [
    "The history of the river valley began when",
    "She opened the wooden box on the table and found",
    "In the laboratory the experiment showed that",
    "The old cartographer unrolled the map and explained",
    "Across the northern plains the migrating herds",
    "The engineer inspected the bridge and noticed",
    "Long ago, before the first cities were built,",
    "The astronomer pointed the telescope toward",
]

torch.set_grad_enabled(False)


# ============================================================================
# generation: the time axis
# ============================================================================
DEV = "cuda" if torch.cuda.is_available() else "cpu"


def generate_sequence(model, tok, prompt, layer, rng_torch):
    """Generate N_GEN tokens autoregressively with output_hidden_states.
    Returns hidden[T,H] (mid layer) and logits[T,V], one row per generated
    token. Temperature sampling, T=1.0 (PREREG §1)."""
    ids = tok(prompt, return_tensors="pt").input_ids.to(DEV)
    hidden, logits, gen_ids = [], [], []
    cur = ids
    for _ in range(N_GEN):
        out = model(cur, output_hidden_states=True)
        h = out.hidden_states[layer][0, -1].float().cpu().numpy()
        lg = out.logits[0, -1].float()
        hidden.append(h)
        logits.append(lg.cpu().numpy())
        p = torch.softmax(lg / 1.0, dim=-1)
        nxt = int(torch.multinomial(p.cpu(), 1, generator=rng_torch))
        gen_ids.append(nxt)
        cur = torch.cat([cur, torch.tensor([[nxt]], device=DEV)], dim=1)
        if cur.shape[1] > 1024:
            cur = cur[:, -1024:]
    return np.asarray(hidden), np.asarray(logits), gen_ids


# ============================================================================
# observables (PREREG §2)
# ============================================================================
def _zscore1d(x):
    x = np.asarray(x, dtype=float)
    s = x.std()
    return (x - x.mean()) / s if s > 1e-12 else x - x.mean()


def family_I(hidden, logits):
    """Windowless per-token projection onto each rung's top PC. PREREG §2.1."""
    def top_pc_proj(M):
        Mc = M - M.mean(axis=0, keepdims=True)
        # top PC via SVD; project rows onto it
        U, S, Vt = np.linalg.svd(Mc, full_matrices=False)
        return Mc @ Vt[0]
    s_int = _zscore1d(top_pc_proj(hidden))
    s_ext = _zscore1d(top_pc_proj(logits))
    return s_int, s_ext


def family_II(hidden, logits, rng):
    """Windowed mean-|Pearson| correlation scalar per rung. PREREG §2.2."""
    hv = hidden.var(axis=0)
    sel_h = np.argsort(hv)[::-1][:D_SUB]
    Xn = hidden[:, sel_h]
    lv = logits.var(axis=0)
    sel_l = np.argsort(lv)[::-1][:D_SUB]
    Xm = logits[:, sel_l]

    def mean_abs_corr(W):
        Wc = W - W.mean(axis=0, keepdims=True)
        sd = Wc.std(axis=0)
        keep = sd > 1e-10
        if keep.sum() < 2:
            return np.nan
        Wc = Wc[:, keep] / sd[keep]
        C = np.corrcoef(Wc, rowvar=False)
        iu = np.triu_indices_from(C, k=1)
        return float(np.nanmean(np.abs(C[iu])))

    T = Xn.shape[0]
    c_int, c_ext = [], []
    for t in range(W_TOK, T):
        c_int.append(mean_abs_corr(Xn[t - W_TOK:t]))
        c_ext.append(mean_abs_corr(Xm[t - W_TOK:t]))
    c_int = _zscore1d(np.nan_to_num(c_int, nan=np.nanmean(c_int)))
    c_ext = _zscore1d(np.nan_to_num(c_ext, nan=np.nanmean(c_ext)))
    return c_int, c_ext


# ============================================================================
# relaxation rate J  (PREREG §3.1) — autocorrelation e-folding + OU
# ============================================================================
def autocorr(x):
    """Biased ACF of mean-subtracted x, lags 0..len(x)-1."""
    x = x - x.mean()
    n = len(x)
    v = x.var()
    if v <= 1e-14:
        return np.zeros(n)
    full = np.correlate(x, x, mode="full")[n - 1:]
    return full / (v * n)


def tau_ac_efold(x):
    """e-folding autocorrelation time tau_ac (in tokens). Fit
    ACF(lag)=exp(-lag/tau_ac) from lag 0 to first zero-crossing (capped)."""
    acf = autocorr(x)
    n = len(acf)
    zc = np.where(acf <= 0)[0]
    lag_max = zc[0] if len(zc) else n // 4
    lag_max = max(lag_max, 3)
    lag_max = min(lag_max, n // 4 if n // 4 > 3 else n - 1)
    lags = np.arange(0, lag_max)
    a = acf[lags]
    a = np.clip(a, 1e-6, None)
    # linear fit of log(ACF) vs lag through the origin region; slope = -1/tau
    # use lag>=1 weighted by ACF magnitude
    mask = lags >= 1
    if mask.sum() < 2:
        return np.nan
    coef = np.polyfit(lags[mask], np.log(a[mask]), 1)
    slope = coef[0]
    if slope >= -1e-9:
        return np.inf  # no decay -> infinite correlation time
    return float(-1.0 / slope)


def tau_int(x):
    """Integrated autocorrelation time, fit-free cross-check."""
    acf = autocorr(x)
    zc = np.where(acf <= 0)[0]
    lag_max = zc[0] if len(zc) else len(acf) // 4
    return float(1.0 + 2.0 * acf[1:lag_max].sum()) if lag_max > 1 else 1.0


def ou_theta(x):
    """OU mean-reversion theta via lag-1 autoregression. PREREG §3.1(b)."""
    x = x - x.mean()
    dx = x[1:] - x[:-1]
    xt = x[:-1]
    denom = (xt ** 2).sum()
    if denom <= 1e-14:
        return np.nan
    slope = (dx * xt).sum() / denom
    return float(-slope)


# ============================================================================
# cross-rung coupling g  (PREREG §3.2) — lagged predictive coupling
# ============================================================================
def _partial_r2(x_int, x_ext):
    """Reduction in 1-step residual variance for x_ext from adding x_int.
    restricted: x_ext_{t+1} ~ x_ext_t ; full: + x_int_t."""
    y = x_ext[1:]
    e_t = x_ext[:-1]
    i_t = x_int[:-1]

    def resid_var(X):
        X = np.column_stack([np.ones(len(y)), X])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        r = y - X @ beta
        return r.var()

    v_restr = resid_var(e_t)
    v_full = resid_var(np.column_stack([e_t, i_t]))
    if v_restr <= 1e-14:
        return 0.0
    return float(max(1.0 - v_full / v_restr, 0.0))


def cross_rung_g(x_int, x_ext, rng):
    """Debiased internal->external coupling g (block-shuffle null). PREREG §3.2."""
    g_raw = _partial_r2(x_int, x_ext)
    n = len(x_int)
    nulls = []
    for _ in range(N_SHUFFLE):
        # contiguous-block permutation of the internal series
        n_blocks = int(np.ceil(n / BLOCK))
        order = rng.permutation(n_blocks)
        blocks = [x_int[b * BLOCK:(b + 1) * BLOCK] for b in range(n_blocks)]
        x_int_s = np.concatenate([blocks[o] for o in order])[:n]
        nulls.append(_partial_r2(x_int_s, x_ext))
    g_floor = float(np.mean(nulls))
    g = max(g_raw - g_floor, 0.0)
    noise_dom = bool(g_raw > 1e-9 and g / g_raw < 0.3)
    return dict(g_raw=g_raw, g_floor=g_floor, g=g,
                g_noise_dominated=noise_dom)


# ============================================================================
# surrogate null for tau_ac  (PREREG §4, second gate condition)
# ============================================================================
def phase_randomise(x, rng):
    """Phase-randomised surrogate: preserve power spectrum, destroy dynamics."""
    X = np.fft.rfft(x - x.mean())
    phases = rng.uniform(0, 2 * np.pi, len(X))
    phases[0] = 0.0
    if len(x) % 2 == 0:
        phases[-1] = 0.0
    Xs = np.abs(X) * np.exp(1j * phases)
    return np.fft.irfft(Xs, n=len(x))


def surrogate_tau_band(x, rng):
    """5-95% band of tau_ac over N_SURROGATE phase-randomised surrogates."""
    taus = []
    for _ in range(N_SURROGATE):
        s = phase_randomise(x, rng)
        t = tau_ac_efold(s)
        if np.isfinite(t):
            taus.append(t)
    if len(taus) < 10:
        return np.nan, np.nan
    return float(np.percentile(taus, 5)), float(np.percentile(taus, 95))


# ============================================================================
# per-sequence measurement
# ============================================================================
def measure_family(x_int, x_ext, w_eff, rng):
    """J_internal, J_external, g, gate verdict for one observable family."""
    tau_int_rung = tau_ac_efold(x_int)
    tau_ext_rung = tau_ac_efold(x_ext)
    J_int = 1.0 / tau_int_rung if np.isfinite(tau_int_rung) and tau_int_rung > 0 else np.nan
    J_ext = 1.0 / tau_ext_rung if np.isfinite(tau_ext_rung) and tau_ext_rung > 0 else np.nan
    J_within = (float(np.sqrt(J_int * J_ext))
                if np.isfinite(J_int) and np.isfinite(J_ext) else np.nan)

    theta_int = ou_theta(x_int)
    theta_ext = ou_theta(x_ext)
    tint_int = tau_int(x_int)
    tint_ext = tau_int(x_ext)

    g = cross_rung_g(x_int, x_ext, rng)
    g_rate = -np.log(1.0 - min(g["g"], 0.999)) if g["g"] > 0 else 0.0
    timescale_gj = g_rate / J_within if (np.isfinite(J_within) and J_within > 1e-12) else np.nan

    # gate condition 1: tau_ac > MARGIN * w_eff for BOTH rungs
    gate_thresh = MARGIN * w_eff
    gate1_int = np.isfinite(tau_int_rung) and tau_int_rung > gate_thresh
    gate1_ext = np.isfinite(tau_ext_rung) and tau_ext_rung > gate_thresh

    # gate condition 2: real tau_ac outside the surrogate 5-95% band
    s_int_lo, s_int_hi = surrogate_tau_band(x_int, rng)
    s_ext_lo, s_ext_hi = surrogate_tau_band(x_ext, rng)
    gate2_int = (np.isfinite(tau_int_rung) and np.isfinite(s_int_hi)
                 and not (s_int_lo <= tau_int_rung <= s_int_hi))
    gate2_ext = (np.isfinite(tau_ext_rung) and np.isfinite(s_ext_hi)
                 and not (s_ext_lo <= tau_ext_rung <= s_ext_hi))

    passes_gate = bool(gate1_int and gate1_ext and gate2_int and gate2_ext
                       and not g["g_noise_dominated"])

    return dict(
        tau_ac_int=float(tau_int_rung), tau_ac_ext=float(tau_ext_rung),
        J_int=float(J_int) if np.isfinite(J_int) else None,
        J_ext=float(J_ext) if np.isfinite(J_ext) else None,
        J_within=float(J_within) if np.isfinite(J_within) else None,
        theta_int=theta_int, theta_ext=theta_ext,
        tau_int_int=tint_int, tau_int_ext=tint_ext,
        g_raw=g["g_raw"], g_floor=g["g_floor"], g=g["g"],
        g_rate=float(g_rate), g_noise_dominated=g["g_noise_dominated"],
        timescale_gj=float(timescale_gj) if np.isfinite(timescale_gj) else None,
        w_eff=w_eff, gate_thresh=float(gate_thresh),
        gate1_int=bool(gate1_int), gate1_ext=bool(gate1_ext),
        surrogate_band_int=[s_int_lo, s_int_hi],
        surrogate_band_ext=[s_ext_lo, s_ext_hi],
        gate2_int=bool(gate2_int), gate2_ext=bool(gate2_ext),
        passes_gate=passes_gate,
    )


def coupling_ratio_gj(hidden, logits, rng):
    """Path 1's coupling-RATIO g/J on the SAME generated sequence. PREREG §3.3.
    Reuses crossrung_lib verbatim."""
    hv = hidden.var(axis=0)
    Xn = hidden[:, np.argsort(hv)[::-1][:D_SUB]]
    lv = logits.var(axis=0)
    Xm = logits[:, np.argsort(lv)[::-1][:D_SUB]]
    wn = within_rung_W(Xn, rng)
    wm = within_rung_W(Xm, rng)
    W_within = float(np.sqrt(max(wn[2], 0.0) * max(wm[2], 0.0)))
    tau = cross_rung_tau(Xn, Xm, hidden.shape[0], rng)
    ratio = (tau["tau_debiased"] / W_within
             if W_within > 1e-9 else np.nan)
    return dict(W_n=wn[2], W_np1=wm[2], W_within=W_within,
                tau_MI_raw=tau["tau_raw"], tau_MI=tau["tau_debiased"],
                coupling_ratio_gj=float(ratio) if np.isfinite(ratio) else None)


def degenerate(gen_ids):
    """Repetition-collapse check: <8 distinct ids in the last 64 tokens."""
    tail = gen_ids[-64:]
    return len(set(tail)) < 8


# ============================================================================
# main
# ============================================================================
def main():
    print("=" * 78)
    print("Paths 2-3, Pair B — canonical TIMESCALE g/J at the LLM int->ext pair")
    print("=" * 78)
    np_rng = np.random.default_rng(SEED)
    rows = []

    for name in MODELS:
        print(f"\n[{name}] loading ...")
        try:
            tok = AutoTokenizer.from_pretrained(name)
            model = AutoModelForCausalLM.from_pretrained(
                name, torch_dtype=torch.float32).to(DEV)
            model.eval()
            print(f"  [{name} loaded on {DEV}]", flush=True)
        except Exception as e:
            print(f"  NOT RUN — load failed: {type(e).__name__}: {str(e)[:80]}")
            continue
        n_layers = model.config.num_hidden_layers
        layer = max(1, int(n_layers * LAYER_FRAC))

        for pi, prompt in enumerate(PROMPTS):
            g_torch = torch.Generator().manual_seed(SEED + pi)
            hidden, logits, gen_ids = generate_sequence(
                model, tok, prompt, layer, g_torch)
            deg = degenerate(gen_ids)

            rng = np.random.default_rng(SEED + pi)
            sI_int, sI_ext = family_I(hidden, logits)
            sII_int, sII_ext = family_II(hidden, logits, rng)

            res_I = measure_family(sI_int, sI_ext, w_eff=1.0,
                                   rng=np.random.default_rng(SEED + pi))
            res_II = measure_family(sII_int, sII_ext, w_eff=float(W_TOK),
                                    rng=np.random.default_rng(SEED + 1000 + pi))
            ratio = coupling_ratio_gj(hidden, logits,
                                      np.random.default_rng(SEED + pi))

            row = dict(model=name, prompt_idx=pi, prompt=prompt,
                       n_layers=n_layers, layer=layer, n_gen=N_GEN,
                       degenerate=bool(deg),
                       family_I=res_I, family_II=res_II,
                       coupling_ratio=ratio)
            rows.append(row)
            # INCREMENTAL WRITE — rewrite the results file after every cell,
            # so a kill/restart leaves a recoverable partial result.
            out = HERE / "results_timescale_gj.json"
            out.write_text(json.dumps(rows, indent=2))
            tg = res_I["timescale_gj"]
            print(f"  p{pi}: famI tau_ac int={res_I['tau_ac_int']:.1f} "
                  f"ext={res_I['tau_ac_ext']:.1f} gate={'PASS' if res_I['passes_gate'] else 'fail'}"
                  f" | g={res_I['g']:.3f} timescale_g/J="
                  f"{tg:.3f}" if tg is not None else
                  f"  p{pi}: famI tau_ac int={res_I['tau_ac_int']:.1f} "
                  f"ext={res_I['tau_ac_ext']:.1f} gate=fail | g={res_I['g']:.3f}",
                  flush=True)
            print(f"        famII tau_ac int={res_II['tau_ac_int']:.1f} "
                  f"ext={res_II['tau_ac_ext']:.1f} thr={res_II['gate_thresh']:.0f} "
                  f"gate={'PASS' if res_II['passes_gate'] else 'fail'}"
                  f" | coupling-ratio g/J={ratio['coupling_ratio_gj']}",
                  flush=True)
            print(f"  [{len(rows)} cells written to {out.name}]", flush=True)

    print(f"\nall {len(rows)} cells complete", flush=True)
    summarise(rows)


def summarise(rows):
    print("\n" + "=" * 78)
    print("SUMMARY — gate verdict and g/J comparison")
    print("=" * 78)
    valid = [r for r in rows if not r["degenerate"]]
    n_deg = len(rows) - len(valid)
    print(f"sequences: {len(rows)} total, {n_deg} degenerate (excluded), "
          f"{len(valid)} in verdict")

    for fam in ("family_I", "family_II"):
        passed = [r for r in valid if r[fam]["passes_gate"]]
        print(f"\n{fam}: {len(passed)}/{len(valid)} sequences clear the "
              f"window-domination gate")
        if len(passed) >= 13:
            tgj = [r[fam]["timescale_gj"] for r in passed
                   if r[fam]["timescale_gj"] is not None]
            if tgj:
                print(f"  -> PASSES (>=13). timescale g/J median "
                      f"{np.median(tgj):.3f}, range "
                      f"[{min(tgj):.3f}, {max(tgj):.3f}]")
        else:
            print(f"  -> FAILS gate (need >=13). window-dominated null for "
                  f"this family.")

    crat = [r["coupling_ratio"]["coupling_ratio_gj"] for r in valid
            if r["coupling_ratio"]["coupling_ratio_gj"] is not None]
    if crat:
        print(f"\ncoupling-ratio g/J (Path 1 method, same sequences): "
              f"median {np.median(crat):.3f}, range "
              f"[{min(crat):.3f}, {max(crat):.3f}]")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Shadow 1 -- FDT fluctuation spectrum of gamma*M  (LLM internals, SECONDARY).
============================================================================

Pre-registration: experiments/shadows/fdt_fluctuation/PREREGISTRATION.md

The GPU substrate is primary (its corridor-exit dissipation rate is measured, so
the FDT link is checkable). The LLM is secondary: there is NO independently
measured corridor-exit relaxation rate at the LLM substrate -- the LLM
corridor-exit attempt FAILED (open_system_pomega/corridor_exit_rate_llm.py: a
windowed k_eff was too noisy to be a corridor trajectory). So for the LLM the
FDT-link half of the test is not available; only the POLE-DISCRIMINATION half
is. This run asks the narrower question: does the fluctuation spectrum of an
in-layer rho time series, over a generation runway, discriminate in-corridor
generation from rigidity (greedy repetition) and chaos (high-temperature)?

Honest scope, stated up front: the prior LLM corridor work flagged the
window-noise problem. This run uses the per-token within-layer attention-head
correlation as rho (a single-token observable, no sliding window), so the
window-domination failure mode does not apply -- but the LLM half remains
secondary and carries no FDT anchor. NULL on the LLM half is fully expected and
does not bear on the GPU verdict.

rho := the debiased mean |off-diagonal correlation| across attention-head
output vectors within one layer, at one token position. The "time" axis is
token index over a generation runway. Real model weights, real generation, no
synthetic data.
"""
import json
import os
import sys
import numpy as np
from datetime import datetime, timezone
from scipy import optimize, signal as sps

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_fdt_llm.json")

MODEL = "Qwen/Qwen2.5-0.5B"
PROMPT = ("The history of metallurgy begins with the discovery that certain "
          "rocks, when heated, yield workable metal. ")
N_TOKENS = 512          # generation runway = the time axis
LAYER_FRAC = 0.5        # mid-stack layer to probe


def head_rho(attn_out, n_heads):
    """rho at one token: debiased mean |off-diag corr| across head subvectors.

    attn_out: (hidden,) vector = the layer's attention output for one token.
    Split into n_heads sub-vectors; correlation across heads is the
    within-layer correlation observable.
    """
    h = attn_out.shape[0]
    d = h // n_heads
    M = attn_out[:n_heads * d].reshape(n_heads, d).astype(np.float64)
    Mc = M - M.mean(axis=1, keepdims=True)
    sd = Mc.std(axis=1)
    keep = sd > 1e-9
    if keep.sum() < 3:
        return np.nan
    Mc = Mc[keep] / sd[keep, None]
    C = (Mc @ Mc.T) / Mc.shape[1]
    n = C.shape[0]
    off = C[~np.eye(n, dtype=bool)]
    raw = float(np.mean(np.abs(off)))
    # phase-randomised floor
    Ms = np.column_stack([np.random.permutation(Mc[:, j])
                          for j in range(Mc.shape[1])])
    Cs = (Ms @ Ms.T) / Ms.shape[1]
    floor = float(np.mean(np.abs(Cs[~np.eye(n, dtype=bool)])))
    return float(np.sqrt(max(raw ** 2 - floor ** 2, 0.0)))


def lorentzian(f, S0, fc):
    return S0 / (1.0 + (f / fc) ** 2)


def fit_psd(freqs, psd):
    mask = freqs > 0
    f, p = freqs[mask], psd[mask]
    if len(f) < 6:
        return None
    try:
        popt, _ = optimize.curve_fit(
            lorentzian, f, p, p0=[float(p[0]), f[len(f) // 4]],
            bounds=([0, f[0]], [np.inf, f[-1]]), maxfev=20000)
        pred = lorentzian(f, *popt)
        ss_res = float(np.sum((p - pred) ** 2))
        ss_tot = float(np.sum((p - p.mean()) ** 2))
        r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
        return {"S0": float(popt[0]), "fc": float(popt[1]), "R2": r2}
    except Exception as e:
        return {"error": str(e)}


def generate_with_rho(model, tok, layer_idx, n_heads, mode):
    """Generate a runway; capture per-token within-layer rho.

    mode: 'corridor' (sampled, temp 0.8) | 'rigidity' (greedy) |
          'chaos' (temp 2.0).
    """
    device = next(model.parameters()).device
    ids = tok(PROMPT, return_tensors="pt").input_ids.to(device)
    rhos = []
    captured = {}

    def hook(_m, _inp, out):
        o = out[0] if isinstance(out, tuple) else out
        captured["attn"] = o.detach()

    layer = model.model.layers[layer_idx]
    handle = layer.self_attn.register_forward_hook(hook)
    try:
        for _ in range(N_TOKENS):
            with torch.no_grad():
                logits = model(ids).logits[:, -1, :]
            attn = captured["attn"][0, -1, :].float().cpu().numpy()
            rhos.append(head_rho(attn, n_heads))
            if mode == "rigidity":
                nxt = torch.argmax(logits, dim=-1, keepdim=True)
            else:
                temp = 0.8 if mode == "corridor" else 2.0
                probs = torch.softmax(logits / temp, dim=-1)
                nxt = torch.multinomial(probs, 1)
            ids = torch.cat([ids, nxt], dim=1)
    finally:
        handle.remove()
    return np.array(rhos, dtype=float)


def analyse(series, label):
    s = series[np.isfinite(series)]
    if len(s) < 32:
        return {"label": label, "error": "too few finite samples", "n": len(s)}
    x = s - np.polyval(np.polyfit(np.arange(len(s)), s, 1), np.arange(len(s)))
    nper = min(128, len(s) // 4)
    freqs, psd = sps.welch(x, fs=1.0, nperseg=nper, detrend="constant")
    fit = fit_psd(freqs, psd)
    acf = np.correlate(x, x, mode="full")[len(x) - 1:]
    acf = acf / acf[0]
    zc = np.argmax(acf < 0) if np.any(acf < 0) else len(acf)
    tau_int = float(np.sum(acf[:zc]))
    return {
        "label": label, "n": int(len(s)),
        "rho_mean": float(s.mean()), "rho_std": float(s.std()),
        "rho_min": float(s.min()), "rho_max": float(s.max()),
        "psd_fit": fit, "tau_acf_tokens": tau_int,
        "freqs": freqs.tolist(), "psd": psd.tolist(),
    }


def main():
    print("=" * 78)
    print("Shadow 1 -- FDT fluctuation spectrum (LLM internals, SECONDARY)")
    print("=" * 78)
    if not torch.cuda.is_available():
        print("WARN: no CUDA; running on CPU (slower, still real).")
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  model={MODEL}  device={dev}  runway={N_TOKENS} tokens")

    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, torch_dtype=torch.float32).to(dev).eval()
    n_layers = len(model.model.layers)
    n_heads = model.config.num_attention_heads
    layer_idx = int(n_layers * LAYER_FRAC)
    print(f"  layers={n_layers}, probing layer {layer_idx}, heads={n_heads}")

    results = {}
    for mode in ("corridor", "rigidity", "chaos"):
        print(f"\n  --- generating: {mode} ---")
        torch.manual_seed(0)
        np.random.seed(0)
        series = generate_with_rho(model, tok, layer_idx, n_heads, mode)
        a = analyse(series, mode)
        results[mode] = a
        fc = a["psd_fit"].get("fc") if a.get("psd_fit") else None
        print(f"    rho={a.get('rho_mean')}+/-{a.get('rho_std')}  "
              f"fc={fc}  tau_acf={a.get('tau_acf_tokens')}")
        with open(OUT, "w") as f:
            json.dump({"status": "in_progress", "model": MODEL,
                       "results": results}, f, indent=2)

    # pole discrimination on the LLM half
    rhos = [results[m].get("rho_mean") for m in ("corridor", "rigidity", "chaos")]
    discriminates = all(r is not None for r in rhos) and \
        len(set(np.round(rhos, 2))) == 3

    payload = {
        "status": "complete",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL, "n_tokens": N_TOKENS, "layer": layer_idx,
        "note": ("Secondary substrate. No independently measured LLM "
                 "corridor-exit rate exists, so no FDT anchor; only "
                 "pole-discrimination is testable here."),
        "results": results,
        "pole_discrimination": bool(discriminates),
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\n  LLM pole discrimination (rho separates 3 regimes) = {discriminates}")
    print(f"  results -> {OUT}")


if __name__ == "__main__":
    main()

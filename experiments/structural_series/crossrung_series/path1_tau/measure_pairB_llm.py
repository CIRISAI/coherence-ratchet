"""
measure_pairB_llm.py — Pair B: LLM INTERNAL -> EXTERNAL (A3int -> A3ext).

Rung n   = transformer hidden-state structure (internal representation).
Rung n+1 = next-token logit-distribution structure (external output).
Observation axis = token positions of a fixed diverse text.

Computes, per model:
  W_n      within-rung coupling among hidden units (shuffle-debiased)
  W_{n+1}  within-rung coupling among top-variance logit coordinates
  W_within = sqrt(W_n * W_{n+1})       (geometric mean, debiased values)
  tau      normalised cross-rung Gaussian MI, shuffle-debiased
  ratio    = tau / W_within

Constructions and debiasing are exactly as in PREREGISTRATION.md §2-3.
Real open weights from HuggingFace; out-of-sample relative to E1's published
LLM result is not claimed — these are the same E1 models, reused deliberately
so the within-rung W is comparable to the existing series.
"""
import json
import pathlib
import sys

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from crossrung_lib import within_rung_W, cross_rung_tau  # noqa: E402

SEED = 17
D_SUB = 256          # subsampled units / logit coords (pre-registered)
MODELS = ["gpt2", "EleutherAI/pythia-160m", "Qwen/Qwen2.5-0.5B"]

SENTENCES = [
    "The river carried silt from the mountains down to the river delta.",
    "Copper conducts electricity better than iron but worse than silver.",
    "Migratory birds navigate using the earth's magnetic field and the stars.",
    "A wooden bridge spanned the narrow gorge above the rushing water.",
    "Photosynthesis converts sunlight, water, and carbon dioxide into sugar.",
    "The library kept its oldest manuscripts in a cool, dry basement room.",
    "Tectonic plates move a few centimetres each year across the mantle.",
    "She tuned the violin carefully before the evening concert began.",
    "Glaciers store a large fraction of the planet's fresh water supply.",
    "The market sold spices, woven cloth, dried fish, and clay pottery.",
    "Neurons communicate through electrical pulses and chemical messengers.",
    "The old clock tower chimed twelve times at noon over the quiet square.",
    "Bees return to the hive and signal the direction of flowers by dancing.",
    "Sandstone forms over ages as grains of sand compress into solid rock.",
    "The engineer checked the pressure valves before starting the turbine.",
    "Coral reefs shelter a quarter of all known species of ocean fish.",
    "A gentle rain fell through the night and cleared by early morning.",
    "The cartographer drew the coastline from measurements taken at sea.",
    "Yeast ferments sugar into alcohol and carbon dioxide as it grows.",
    "The telescope gathered faint light from a galaxy millions of years away.",
]
TEXT = " ".join(SENTENCES)


def measure_model(name, rng):
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32)
    model.eval()
    ids = tok(TEXT, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        out = model(**ids, output_hidden_states=True)
    hs = out.hidden_states                       # tuple, layers x (1,T,H)
    logits = out.logits[0].numpy()               # (T, vocab)
    n_layers = len(hs)
    mid = n_layers // 2                          # mid-depth internal rung
    hidden = hs[mid][0].numpy()                  # (T, H)
    m = hidden.shape[0]

    # rung n: hidden units, subsample D_SUB highest-variance units
    hv = hidden.var(axis=0)
    sel_h = np.argsort(hv)[::-1][:D_SUB]
    Xn = hidden[:, sel_h]

    # rung n+1: logits, top D_SUB highest-variance vocabulary coordinates
    lv = logits.var(axis=0)
    sel_l = np.argsort(lv)[::-1][:D_SUB]
    Xm = logits[:, sel_l]

    wn = within_rung_W(Xn, rng)
    wm = within_rung_W(Xm, rng)
    W_within = float(np.sqrt(max(wn[2], 0.0) * max(wm[2], 0.0)))
    tau = cross_rung_tau(Xn, Xm, m, rng)
    ratio = tau["tau_debiased"] / W_within if W_within > 1e-9 else np.nan

    return dict(
        model=name, n_layers=n_layers, mid_layer=mid, m_tokens=int(m),
        W_n_raw=wn[0], W_n_floor=wn[1], W_n=wn[2],
        W_np1_raw=wm[0], W_np1_floor=wm[1], W_np1=wm[2],
        W_within=W_within,
        tau_raw=tau["tau_raw"], tau_floor=tau["tau_floor"],
        tau=tau["tau_debiased"], q_pca=tau["q"],
        tau_noise_dominated=bool(
            tau["tau_raw"] > 1e-9
            and tau["tau_debiased"] / tau["tau_raw"] < 0.3),
        ratio=float(ratio),
    )


def main():
    torch.set_grad_enabled(False)
    print("=" * 78)
    print("Pair B — LLM internal -> external: cross-rung vs within-rung coupling")
    print("=" * 78)
    rows = []
    for name in MODELS:
        rng = np.random.default_rng(SEED)
        try:
            r = measure_model(name, rng)
        except Exception as e:
            print(f"  {name}: FAILED {type(e).__name__}: {str(e)[:80]}")
            continue
        rows.append(r)
        print(f"\n  {name}  (layer {r['mid_layer']}/{r['n_layers']}, "
              f"m={r['m_tokens']} tokens, q_pca={r['q_pca']})")
        print(f"    W_n (hidden)   raw {r['W_n_raw']:.3f} "
              f"floor {r['W_n_floor']:.3f} -> debiased {r['W_n']:.3f}")
        print(f"    W_n+1 (logits) raw {r['W_np1_raw']:.3f} "
              f"floor {r['W_np1_floor']:.3f} -> debiased {r['W_np1']:.3f}")
        print(f"    W_within (geom mean)         = {r['W_within']:.3f}")
        print(f"    tau  raw {r['tau_raw']:.3f} floor {r['tau_floor']:.3f} "
              f"-> debiased {r['tau']:.3f}"
              f"{'  [NOISE-DOMINATED]' if r['tau_noise_dominated'] else ''}")
        print(f"    ratio = tau / W_within       = {r['ratio']:.3f}")

    if rows:
        ratios = [r["ratio"] for r in rows if np.isfinite(r["ratio"])]
        med = float(np.median(ratios))
        print("\n" + "=" * 78)
        print(f"  Pair B median ratio over {len(ratios)} models = {med:.3f}")
        verdict = ("Simon (within dominates)" if med < 0.5 else
                   "framework (cross dominates)" if med > 1.5 else
                   "middle band")
        print(f"  ratio range [{min(ratios):.3f}, {max(ratios):.3f}]  "
              f"-> pre-registered verdict: {verdict}")

    out = HERE / "results_pairB.json"
    out.write_text(json.dumps(rows, indent=2))
    print(f"\n  wrote {out}")


if __name__ == "__main__":
    main()

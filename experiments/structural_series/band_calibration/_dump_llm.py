"""Re-run E1 LLM corridor and dump per-layer debiased rho to JSON.
Replicates exp_E1_llm_corridor.py exactly. No new data, no synthetic data."""
import json, os
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

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
MODELS = ["gpt2", "EleutherAI/pythia-160m", "Qwen/Qwen2.5-0.5B"]


def _mean_abs_offdiag(Hc):
    n = Hc.shape[0]
    C = (Hc.T @ Hc) / n
    d = C.shape[0]
    return float(np.mean(np.abs(C[~np.eye(d, dtype=bool)])))


def layer_rho(H, rng):
    Hc = H - H.mean(axis=0, keepdims=True)
    sd = Hc.std(axis=0)
    keep = sd > 1e-8
    Hc = Hc[:, keep] / sd[keep]
    raw = _mean_abs_offdiag(Hc)
    Hs = np.column_stack([rng.permutation(Hc[:, j]) for j in range(Hc.shape[1])])
    floor = _mean_abs_offdiag(Hs)
    debiased = float(np.sqrt(max(raw ** 2 - floor ** 2, 0.0)))
    d = Hc.shape[1]
    k_eff_kish = float(d / (1.0 + debiased * (d - 1.0)))
    return raw, floor, debiased, d, k_eff_kish


torch.set_grad_enabled(False)
rng = np.random.default_rng(0)
records = []
for name in MODELS:
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModel.from_pretrained(name, torch_dtype=torch.float32)
    model.eval()
    ids = tok(TEXT, return_tensors="pt", truncation=True, max_length=512)
    out = model(**ids, output_hidden_states=True)
    hs = out.hidden_states
    for ell in range(1, len(hs)):
        r, f, d, dim, kk = layer_rho(hs[ell][0].float().numpy(), rng)
        records.append({"model": name, "layer": ell, "rho_raw": r,
                        "floor": f, "rho_deb": d, "n_units": dim,
                        "k_eff_kish": kk})
    print(f"{name}: {len(hs)-1} layers", flush=True)

out = os.path.join(os.path.dirname(__file__), "_llm_per_layer.json")
json.dump({"n": len(records), "records": records}, open(out, "w"), indent=1)
print(f"wrote {out}: n={len(records)} layers", flush=True)

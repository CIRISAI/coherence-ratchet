"""Run the sensor-lift signature experiment for one model.

Usage:  python run.py <provider>:<model> [--smoke] [--limit N]

  provider ∈ {openai, together}
  model: vendor-specific slug

Examples:
  python run.py openai:gpt-4o
  python run.py together:meta-llama/Llama-3.3-70B-Instruct-Turbo

Reads:  corpus.json
Writes: results/<slug_safe>.json, results/<slug_safe>.log
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
CORPUS = ROOT / "corpus.json"

N_POSITIONS = 10
TOP_K_DEFAULT = 20
TOP_K_PER_PROVIDER = {"together": 5}  # Together caps top_logprobs at 5
SMOOTHING = 1e-5
MAX_RETRIES = 4
BASE_BACKOFF = 2.0
TIMEOUT = 60

PROVIDERS = {
    "openai":     ("https://api.openai.com/v1/chat/completions",          ".openai_key"),
    "together":   ("https://api.together.xyz/v1/chat/completions",        ".together_key"),
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions",       ".ratchet_openrouter_key"),
}


def load_key(provider: str) -> str:
    return (Path.home() / PROVIDERS[provider][1]).read_text().strip()


def safe_slug(provider: str, model: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "__", f"{provider}__{model}")


def call_api(provider: str, api_key: str, model: str, prompt: str) -> dict:
    url = PROVIDERS[provider][0]
    top_k = TOP_K_PER_PROVIDER.get(provider, TOP_K_DEFAULT)
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": N_POSITIONS,
        "temperature": 0.0,
        "logprobs": True,
        "top_logprobs": top_k,
    }
    data = json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 coherence-ratchet/1.0",
    }
    if provider == "openrouter":
        headers["X-Title"] = "coherence-ratchet sensor-lift"
    req = urllib.request.Request(url, data=data, headers=headers)
    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last_err = e
            sleep_s = BASE_BACKOFF * (2 ** attempt)
            sys.stderr.write(f"  retry {attempt+1}/{MAX_RETRIES} after {sleep_s:.1f}s: {e}\n")
            time.sleep(sleep_s)
    raise RuntimeError(f"API failed after {MAX_RETRIES} retries: {last_err}")


def extract_position_dists(resp: dict) -> list[dict[str, float]]:
    """Return [{token: logprob, ...}, ...] per response position.

    Handles two shapes:
      (a) OpenAI chat completions:
          choices[0].logprobs.content[i] = {token, logprob, top_logprobs: [{token, logprob}, ...]}
      (b) Together legacy / completions-style:
          choices[0].logprobs = {tokens: [...], token_logprobs: [...], top_logprobs: [{tok: lp, ...}, ...]}
    """
    try:
        choice = resp["choices"][0]
    except (KeyError, IndexError):
        return []
    lp = choice.get("logprobs")
    if not lp:
        return []

    # Shape (a): OpenAI / OpenRouter
    if isinstance(lp, dict) and lp.get("content"):
        dists: list[dict[str, float]] = []
        for pos in lp["content"]:
            d: dict[str, float] = {}
            for entry in pos.get("top_logprobs") or []:
                d[entry["token"]] = entry["logprob"]
            if "token" in pos and "logprob" in pos and pos["token"] not in d:
                d[pos["token"]] = pos["logprob"]
            dists.append(d)
        return dists

    # Shape (b): Together legacy
    if isinstance(lp, dict) and lp.get("top_logprobs"):
        top = lp["top_logprobs"]
        tokens = lp.get("tokens") or []
        token_logprobs = lp.get("token_logprobs") or []
        dists = []
        for i, pos_top in enumerate(top):
            d = {}
            if isinstance(pos_top, dict):
                d = dict(pos_top)
            # ensure chosen token in dist
            if i < len(tokens) and i < len(token_logprobs):
                tok = tokens[i]
                lp_val = token_logprobs[i]
                if tok is not None and lp_val is not None and tok not in d:
                    d[tok] = lp_val
            dists.append(d)
        return dists

    return []


def kl_divergence(p: dict[str, float], q: dict[str, float]) -> float:
    if not p or not q:
        return float("nan")
    log_smooth = math.log(SMOOTHING)
    kl = 0.0
    for tok, log_p in p.items():
        p_v = math.exp(log_p)
        log_q = q.get(tok, log_smooth)
        q_v = math.exp(log_q)
        if p_v > 0 and q_v > 0:
            kl += p_v * (math.log(p_v) - math.log(q_v))
    return kl


def kl_pair(dists_a: list[dict[str, float]], dists_b: list[dict[str, float]]) -> tuple[float, list[float]]:
    n = min(len(dists_a), len(dists_b))
    if n == 0:
        return float("nan"), []
    per = [kl_divergence(dists_a[t], dists_b[t]) for t in range(n)]
    valid = [v for v in per if not math.isnan(v)]
    mean = sum(valid) / len(valid) if valid else float("nan")
    return mean, per


def run(provider: str, model: str, smoke: bool, limit: int | None) -> None:
    api_key = load_key(provider)
    corpus = json.loads(CORPUS.read_text())
    slug = safe_slug(provider, model)
    out_path = ROOT / "results" / f"{slug}.json"
    log_path = ROOT / "results" / f"{slug}.log"
    out_path.parent.mkdir(exist_ok=True)

    categories = list(corpus.keys())
    n_instances = 20
    if smoke:
        categories = categories[:1]
        n_instances = 1
    elif limit is not None:
        n_instances = min(n_instances, limit)

    results: list[dict] = []
    t_start = time.time()
    with open(log_path, "w") as logf:
        logf.write(f"provider={provider}\nmodel={model}\nsmoke={smoke}\nlimit={limit}\nstart={time.ctime()}\n\n")
        logf.flush()
        for category in categories:
            for i in range(n_instances):
                p_self = corpus[category]["P_self"][i]
                p_ext  = corpus[category]["P_ext"][i]
                p_a    = corpus[category]["P_a"][i]
                p_b    = corpus[category]["P_b"][i]

                try:
                    r_self = call_api(provider, api_key, model, p_self)
                    r_ext  = call_api(provider, api_key, model, p_ext)
                    r_a    = call_api(provider, api_key, model, p_a)
                    r_b    = call_api(provider, api_key, model, p_b)
                except Exception as e:  # noqa: BLE001
                    logf.write(f"[FAIL] {category} i={i}: {e}\n")
                    logf.flush()
                    continue

                d_self = extract_position_dists(r_self)
                d_ext  = extract_position_dists(r_ext)
                d_a    = extract_position_dists(r_a)
                d_b    = extract_position_dists(r_b)

                kl_self_mean, kl_self_per = kl_pair(d_self, d_ext)
                kl_base_mean, kl_base_per = kl_pair(d_a, d_b)
                delta = kl_self_mean - kl_base_mean

                rec = {
                    "category": category,
                    "instance": i,
                    "kl_self": kl_self_mean,
                    "kl_base": kl_base_mean,
                    "delta": delta,
                    "kl_self_per_pos": kl_self_per,
                    "kl_base_per_pos": kl_base_per,
                    "n_positions_self": len(d_self),
                    "n_positions_ext": len(d_ext),
                    "n_positions_a": len(d_a),
                    "n_positions_b": len(d_b),
                }
                results.append(rec)
                elapsed = time.time() - t_start
                logf.write(
                    f"[{elapsed:7.1f}s] {category:15s} i={i:2d}  "
                    f"kl_self={kl_self_mean:7.4f}  kl_base={kl_base_mean:7.4f}  "
                    f"delta={delta:+8.4f}  n_pos=({len(d_self)},{len(d_ext)},{len(d_a)},{len(d_b)})\n"
                )
                logf.flush()

                if (i + 1) % 5 == 0 or smoke:
                    with open(out_path, "w") as f:
                        json.dump({"provider": provider, "model": model, "smoke": smoke,
                                   "results": results}, f, indent=2)

        with open(out_path, "w") as f:
            json.dump({"provider": provider, "model": model, "smoke": smoke,
                       "results": results}, f, indent=2)
        logf.write(f"\ndone={time.ctime()}  total={time.time()-t_start:.1f}s  n_records={len(results)}\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="provider:model (e.g. openai:gpt-4o)")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--limit", type=int, default=None,
                    help="Max instances per category (default 20)")
    args = ap.parse_args()
    if ":" not in args.target:
        ap.error("target must be provider:model")
    provider, model = args.target.split(":", 1)
    if provider not in PROVIDERS:
        ap.error(f"unknown provider; choose from {list(PROVIDERS)}")
    run(provider, model, smoke=args.smoke, limit=args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())

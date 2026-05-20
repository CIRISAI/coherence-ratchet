"""Run v2 sensor-lift experiment for one model.

Usage: python run_v2.py <slot> [--smoke]

slot ∈ {gpt-4o, gpt-4.1, llama, qwen, sonnet}

Routes:
  gpt-4o, gpt-4.1     → OpenAI direct, logprobs path
  llama, qwen         → Together direct, logprobs path (top_k=5)
  sonnet              → Anthropic direct, sample-based empirical KL path
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parent
CORPUS = ROOT / "corpus_v2.json"
RESULTS_DIR = ROOT / "results_v2"
HOME = Path.home()

N_POSITIONS = 10        # logprobs path: response positions
TOP_K_OPENAI = 20
TOP_K_TOGETHER = 5
N_SAMPLES_SAMPLE_BASED = 50   # Anthropic empirical-KL path (pre-registered)
N_SAMPLE_CONCURRENCY = 10     # parallel API calls within sample batch
LAPLACE_ALPHA = 0.5
SMOOTHING = 1e-5
MAX_RETRIES = 4
BASE_BACKOFF = 2.0
TIMEOUT = 60

SLOTS = {
    "gpt-4o":   ("openai",     "gpt-4o",                                  "logprobs"),
    "gpt-4.1":  ("openai",     "gpt-4.1",                                 "logprobs"),
    "llama":    ("together",   "meta-llama/Llama-3.3-70B-Instruct-Turbo", "logprobs"),
    "qwen":     ("together",   "Qwen/Qwen2.5-7B-Instruct-Turbo",          "logprobs"),
    # Anthropic native API has zero credit; routed via OpenRouter for the
    # sample-based path. OpenRouter strips logprobs from Anthropic backends
    # but the sample-based path doesn't need logprobs.
    "sonnet":   ("openrouter", "anthropic/claude-sonnet-4.5",             "sample"),
}

PROVIDER_CFG = {
    "openai":     {"url": "https://api.openai.com/v1/chat/completions",
                   "key": ".openai_key"},
    "together":   {"url": "https://api.together.xyz/v1/chat/completions",
                   "key": ".together_key"},
    "openrouter": {"url": "https://openrouter.ai/api/v1/chat/completions",
                   "key": ".ratchet_openrouter_key"},
}


def safe_slug(slot: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "__", slot)


def load_key(provider: str) -> str:
    return (HOME / PROVIDER_CFG[provider]["key"]).read_text().strip()


def http_post(url: str, headers: dict, body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last_err = e
            sleep_s = BASE_BACKOFF * (2 ** attempt)
            sys.stderr.write(f"    retry {attempt+1}/{MAX_RETRIES} after {sleep_s:.1f}s: {e}\n")
            time.sleep(sleep_s)
    raise RuntimeError(f"API failed: {last_err}")


# -------- LOGPROBS PATH --------

def call_logprobs(provider: str, model: str, prompt: str, api_key: str) -> dict:
    cfg = PROVIDER_CFG[provider]
    top_k = TOP_K_TOGETHER if provider == "together" else TOP_K_OPENAI
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": N_POSITIONS,
        "temperature": 0.0,
        "logprobs": True,
        "top_logprobs": top_k,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 cr/2.0",
    }
    return http_post(cfg["url"], headers, body)


def extract_dists_logprobs(resp: dict) -> list[dict[str, float]]:
    try:
        choice = resp["choices"][0]
        lp = choice.get("logprobs")
    except (KeyError, IndexError):
        return []
    if not lp:
        return []
    if isinstance(lp, dict) and lp.get("content"):
        out = []
        for pos in lp["content"]:
            d = {}
            for entry in pos.get("top_logprobs") or []:
                d[entry["token"]] = entry["logprob"]
            if "token" in pos and "logprob" in pos and pos["token"] not in d:
                d[pos["token"]] = pos["logprob"]
            out.append(d)
        return out
    if isinstance(lp, dict) and lp.get("top_logprobs"):
        top = lp["top_logprobs"]
        tokens = lp.get("tokens") or []
        tok_lp = lp.get("token_logprobs") or []
        out = []
        for i, pos_top in enumerate(top):
            d = dict(pos_top) if isinstance(pos_top, dict) else {}
            if i < len(tokens) and i < len(tok_lp):
                t, p = tokens[i], tok_lp[i]
                if t is not None and p is not None and t not in d:
                    d[t] = p
            out.append(d)
        return out
    return []


def kl_dist(p: dict[str, float], q: dict[str, float]) -> float:
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


def kl_pair_logprobs(p1_dists, p2_dists):
    n = min(len(p1_dists), len(p2_dists))
    if n == 0:
        return float("nan")
    per = [kl_dist(p1_dists[t], p2_dists[t]) for t in range(n)]
    valid = [v for v in per if not math.isnan(v)]
    return sum(valid) / len(valid) if valid else float("nan")


# -------- SAMPLE-BASED PATH (Anthropic) --------

def call_sample_chat(provider: str, model: str, prompt: str, api_key: str) -> str:
    """Sample one completion at temperature 1, max_tokens=1, via OpenAI-compat shape."""
    cfg = PROVIDER_CFG[provider]
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1,
        "temperature": 1.0,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 cr/2.0",
    }
    if provider == "openrouter":
        headers["X-Title"] = "cr-sensor-lift-v2"
    resp = http_post(cfg["url"], headers, body)
    try:
        msg = resp["choices"][0].get("message") or {}
        return (msg.get("content") or "")[:50]
    except Exception:  # noqa: BLE001
        return ""


def empirical_dist(provider: str, model: str, prompt: str, api_key: str, n_samples: int) -> dict[str, float]:
    """Build Laplace-smoothed empirical distribution over first generated token.
    Parallelizes the n_samples API calls via thread pool."""
    counts: Counter[str] = Counter()
    def one_sample(_):
        try:
            tok = call_sample_chat(provider, model, prompt, api_key).strip().split()[0:1]
            return tok[0] if tok else ""
        except Exception:  # noqa: BLE001
            return None
    with ThreadPoolExecutor(max_workers=N_SAMPLE_CONCURRENCY) as ex:
        for tok_str in ex.map(one_sample, range(n_samples)):
            if tok_str is not None:
                counts[tok_str] += 1
    # Laplace smoothing over observed vocab + 1
    V = len(counts) + 1
    total = n_samples + LAPLACE_ALPHA * V
    return {t: (c + LAPLACE_ALPHA) / total for t, c in counts.items()}


def kl_pair_sample(p_dist: dict[str, float], q_dist: dict[str, float]) -> float:
    if not p_dist or not q_dist:
        return float("nan")
    smoothed = LAPLACE_ALPHA / (sum(q_dist.values()) * len(q_dist) + 1)
    kl = 0.0
    for tok, p_v in p_dist.items():
        q_v = q_dist.get(tok, smoothed)
        if p_v > 0 and q_v > 0:
            kl += p_v * (math.log(p_v) - math.log(q_v))
    return kl


# -------- main --------

def run(slot: str, smoke: bool) -> int:
    provider, model, path = SLOTS[slot]
    api_key = load_key(provider)
    corpus = json.loads(CORPUS.read_text())["corpus"]
    slug = safe_slug(slot)
    out_path = RESULTS_DIR / f"{slug}.json"
    log_path = RESULTS_DIR / f"{slug}.log"
    RESULTS_DIR.mkdir(exist_ok=True)

    results: list[dict] = []
    t0 = time.time()
    classes = list(corpus.keys())[:1] if smoke else list(corpus.keys())

    with open(log_path, "w") as logf:
        logf.write(f"slot={slot} provider={provider} model={model} path={path}\n")
        logf.write(f"smoke={smoke} start={time.ctime()}\n\n")
        logf.flush()
        for cls_name in classes:
            cls = corpus[cls_name]
            n_inst = len(cls["P_self"])
            if smoke:
                n_inst = 1
            for i in range(n_inst):
                p_self = cls["P_self"][i]
                p_ext  = cls["P_ext"][i]
                p_a    = cls["P_a"][i]
                p_b    = cls["P_b"][i]
                try:
                    if path == "logprobs":
                        d_self = extract_dists_logprobs(call_logprobs(provider, model, p_self, api_key))
                        d_ext  = extract_dists_logprobs(call_logprobs(provider, model, p_ext,  api_key))
                        d_a    = extract_dists_logprobs(call_logprobs(provider, model, p_a,    api_key))
                        d_b    = extract_dists_logprobs(call_logprobs(provider, model, p_b,    api_key))
                        kl_self = kl_pair_logprobs(d_self, d_ext)
                        kl_base = kl_pair_logprobs(d_a,    d_b)
                    else:  # sample-based
                        e_self = empirical_dist(provider, model, p_self, api_key, N_SAMPLES_SAMPLE_BASED)
                        e_ext  = empirical_dist(provider, model, p_ext,  api_key, N_SAMPLES_SAMPLE_BASED)
                        e_a    = empirical_dist(provider, model, p_a,    api_key, N_SAMPLES_SAMPLE_BASED)
                        e_b    = empirical_dist(provider, model, p_b,    api_key, N_SAMPLES_SAMPLE_BASED)
                        kl_self = kl_pair_sample(e_self, e_ext)
                        kl_base = kl_pair_sample(e_a,    e_b)
                except Exception as e:  # noqa: BLE001
                    logf.write(f"[FAIL] {cls_name} i={i}: {e}\n")
                    logf.flush()
                    continue
                delta = kl_self - kl_base if (math.isfinite(kl_self) and math.isfinite(kl_base)) else float("nan")
                rec = {
                    "class": cls_name, "instance": i,
                    "kl_self": kl_self, "kl_base": kl_base, "delta": delta,
                }
                results.append(rec)
                el = time.time() - t0
                logf.write(f"[{el:8.1f}s] {cls_name:25s} i={i:2d}  kl_self={kl_self:8.4f}  "
                           f"kl_base={kl_base:8.4f}  delta={delta:+8.4f}\n")
                logf.flush()
                if (i + 1) % 5 == 0 or smoke:
                    out_path.write_text(json.dumps({
                        "slot": slot, "provider": provider, "model": model, "path": path,
                        "smoke": smoke, "results": results,
                    }, indent=2))
        out_path.write_text(json.dumps({
            "slot": slot, "provider": provider, "model": model, "path": path,
            "smoke": smoke, "results": results,
        }, indent=2))
        logf.write(f"\ndone={time.ctime()} total={time.time()-t0:.1f}s n={len(results)}\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slot", choices=list(SLOTS.keys()))
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    return run(args.slot, args.smoke)


if __name__ == "__main__":
    raise SystemExit(main())

"""Probe more Together serverless models for logprobs."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

KEY = (Path.home() / ".together_key").read_text().strip()
URL = "https://api.together.xyz/v1/chat/completions"

MODELS = [
    "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    "Qwen/Qwen2.5-7B-Instruct-Turbo",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2-72B-Instruct",
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
    "databricks/dbrx-instruct",
    "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
]


def probe(model: str) -> str:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": "The capital of France is"}],
        "max_tokens": 3,
        "temperature": 0.0,
        "logprobs": True,
        "top_logprobs": 5,
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 coherence-ratchet/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:150]}"
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"
    try:
        choice = data["choices"][0]
        lp = choice.get("logprobs")
        if not lp:
            return "no logprobs"
        if lp.get("content"):
            top0 = lp["content"][0].get("top_logprobs") or []
            return f"✓ content K={len(top0)}" if top0 else "content but no top"
        if lp.get("tokens") and lp.get("top_logprobs"):
            top0 = lp["top_logprobs"][0] if lp["top_logprobs"] else {}
            return f"✓ legacy shape n_tok={len(lp['tokens'])} K={len(top0) if isinstance(top0, dict) else 0}"
        return f"shape: {list(lp.keys())}"
    except Exception as e:  # noqa: BLE001
        return f"err: {e}"


for m in MODELS:
    print(f"{m:60s}  {probe(m)}")

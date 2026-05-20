"""Probe direct provider APIs for logprobs support.

Tests:
  - Together AI (Llama 3.3 70B, Qwen 2.5 72B, DeepSeek V3)
  - OpenAI (gpt-4o, gpt-4o-mini)
  - Groq (Llama 3.3 70B)
  - DeepInfra (Llama)

All use OpenAI-compatible chat-completion shape.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HOME = Path.home()

PROVIDERS = [
    # (name, base_url, key_path, models)
    ("openai", "https://api.openai.com/v1/chat/completions", ".openai_key",
     ["gpt-4o", "gpt-4o-mini"]),
    ("together", "https://api.together.xyz/v1/chat/completions", ".together_key",
     [
         "meta-llama/Llama-3.3-70B-Instruct-Turbo",
         "Qwen/Qwen2.5-72B-Instruct-Turbo",
         "deepseek-ai/DeepSeek-V3",
     ]),
    ("groq", "https://api.groq.com/openai/v1/chat/completions", ".groq_key",
     ["llama-3.3-70b-versatile", "qwen-2.5-32b"]),
    ("deepinfra", "https://api.deepinfra.com/v1/openai/chat/completions", ".deepinfra_key",
     ["meta-llama/Llama-3.3-70B-Instruct", "deepseek-ai/DeepSeek-V3"]),
]


def probe(base_url: str, api_key: str, model: str) -> str:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": "The capital of France is"}],
        "max_tokens": 3,
        "temperature": 0.0,
        "logprobs": True,
        "top_logprobs": 5,
    }
    req = urllib.request.Request(
        base_url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) coherence-ratchet/1.0",
            "Accept": "application/json",
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
        # Some providers (Together) put it under 'content', some under 'tokens'
        content = lp.get("content")
        if content:
            top0 = content[0].get("top_logprobs") or []
            return f"✓ content shape, pos={len(content)} K={len(top0)}" if top0 else f"content but no top (n={len(content)})"
        if lp.get("tokens"):
            return f"✓ tokens shape, n={len(lp.get('tokens'))}, top={len(lp.get('top_logprobs') or [])}"
        return f"unknown shape: {list(lp.keys())}"
    except Exception as e:  # noqa: BLE001
        return f"shape err: {e}"


def main() -> int:
    for name, url, keyf, models in PROVIDERS:
        try:
            key = (HOME / keyf).read_text().strip()
        except FileNotFoundError:
            print(f"--- {name}: NO KEY at ~/{keyf} ---")
            continue
        print(f"--- {name} ({url}) ---")
        for m in models:
            out = probe(url, key, m)
            print(f"  {m:55s}  {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

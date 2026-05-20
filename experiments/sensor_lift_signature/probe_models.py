"""Probe whether each candidate model returns top_logprobs via OpenRouter.

Sends one minimal request per model with logprobs+top_logprobs requested.
Prints a one-line verdict per model.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

KEY_PATH = Path.home() / ".ratchet_openrouter_key"
URL = "https://openrouter.ai/api/v1/chat/completions"

CANDIDATES = [
    "openai/gpt-4o",
    "google/gemini-pro-1.5",
    "google/gemini-2.0-flash-001",
    "meta-llama/llama-3.3-70b-instruct",
    "qwen/qwen-2.5-72b-instruct",
    "deepseek/deepseek-chat",
    "mistralai/mistral-large",
    "anthropic/claude-sonnet-4.5",
]

PROMPT = "The capital of France is"


def probe(api_key: str, model: str) -> tuple[bool, int, str]:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": 3,
        "temperature": 0.0,
        "logprobs": True,
        "top_logprobs": 5,
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Title": "logprobs-probe",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")[:200]
        return False, 0, f"HTTP {e.code}: {body_text}"
    except Exception as e:  # noqa: BLE001
        return False, 0, f"{type(e).__name__}: {e}"
    try:
        choice = data["choices"][0]
        lp = choice.get("logprobs")
        if not lp:
            return False, 0, "no logprobs field"
        content = lp.get("content") or []
        if not content:
            return False, 0, "empty logprobs.content"
        top0 = content[0].get("top_logprobs") or []
        n_top = len(top0)
        if n_top == 0:
            return False, len(content), f"no top_logprobs (content has {len(content)} entries)"
        return True, n_top, f"{len(content)} positions, top_K={n_top}"
    except (KeyError, IndexError, TypeError) as e:
        return False, 0, f"unexpected shape: {e}"


def main() -> int:
    api_key = KEY_PATH.read_text().strip()
    print(f"{'model':45s}  ok    detail")
    print("-" * 100)
    for m in CANDIDATES:
        ok, _, detail = probe(api_key, m)
        flag = "✓" if ok else "✗"
        print(f"{m:45s}  {flag}   {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

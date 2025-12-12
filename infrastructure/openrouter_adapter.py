# infrastructure/openrouter_adapter.py
import os
import requests
import json
from typing import List

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"  # root domain to avoid DNS blocks

class OpenRouterLLM:
    def __init__(self, api_key: str = None, model: str = "mistralai/devstral-2512:free"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")
        self.model = model

    def generate(self, messages: List[dict], max_tokens: int = 512, temperature: float = 0.0) -> str:
        """
        messages: list of {"role":"user"/"system"/"assistant", "content": "text"}
        returns assistant content
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)

        resp.raise_for_status()
        data = resp.json()
        # The OpenRouter response is OpenAI-compatible: choices[0].message.content
        # handle different shapes robustly:
        try:
            choice = data.get("choices", [None])[0]
            if not choice:
                return "ERROR: No choices returned by LLM."
            message = choice.get("message") or {}
            content = message.get("content")
            # support content as str or list
            if isinstance(content, list):
                return " ".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in content])
            if isinstance(content, dict):
                return content.get("text", "") or str(content)
            return content or ""
        except Exception as e:
            # fallback: return raw json
            return json.dumps(data, indent=2)

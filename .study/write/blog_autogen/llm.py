"""통합 LLM 클라이언트 — OpenAI / Anthropic / Gemini 공통 인터페이스."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Provider = Literal["openai", "anthropic", "gemini"]


@dataclass
class LLMConfig:
    provider: Provider
    model: str
    api_key: str
    temperature: float = 0.3
    max_tokens: int = 16000


class LLMClient:
    def __init__(self, cfg: LLMConfig):
        self.cfg = cfg

    def complete(self, system: str, user: str) -> str:
        p = self.cfg.provider
        if p == "openai":
            return self._openai(system, user)
        if p == "anthropic":
            return self._anthropic(system, user)
        if p == "gemini":
            return self._gemini(system, user)
        raise ValueError(f"unknown provider: {p}")

    def _openai(self, system: str, user: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.cfg.api_key)
        resp = client.chat.completions.create(
            model=self.cfg.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=self.cfg.temperature,
            max_tokens=self.cfg.max_tokens,
        )
        return resp.choices[0].message.content or ""

    def _anthropic(self, system: str, user: str) -> str:
        import anthropic

        client = anthropic.Anthropic(api_key=self.cfg.api_key)
        resp = client.messages.create(
            model=self.cfg.model,
            system=system,
            max_tokens=self.cfg.max_tokens,
            temperature=self.cfg.temperature,
            messages=[{"role": "user", "content": user}],
        )
        parts = []
        for block in resp.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)
        return "".join(parts)

    def _gemini(self, system: str, user: str) -> str:
        import google.generativeai as genai

        genai.configure(api_key=self.cfg.api_key)
        model = genai.GenerativeModel(
            model_name=self.cfg.model,
            system_instruction=system,
        )
        resp = model.generate_content(
            user,
            generation_config={
                "temperature": self.cfg.temperature,
                "max_output_tokens": self.cfg.max_tokens,
            },
        )
        return resp.text or ""


PROVIDER_MODELS: dict[Provider, list[str]] = {
    "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "o4-mini"],
    "anthropic": [
        "claude-opus-4-20250514",
        "claude-sonnet-4-20250514",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
    ],
    "gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
}

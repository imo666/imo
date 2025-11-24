"""LLM client utilities for StoryViz."""
from __future__ import annotations

from typing import Protocol

import requests

from backend.models import ProjectFull
from backend.story_parser import build_prompt_for_story_to_project, parse_llm_response_to_project


class LLMClient(Protocol):
    """Generic interface for large language model clients."""

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 4000) -> str:
        """Generate text from a prompt."""


class LocalLLMClient:
    """Client for interacting with a local Ollama-compatible server."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3") -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 4000) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=60
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError("Failed to generate response from local LLM") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError("LLM response was not valid JSON") from exc

        text = data.get("response")
        if not isinstance(text, str):
            raise RuntimeError("LLM response missing 'response' text")

        return text


def generate_project_from_script(
    script: str, client: LLMClient, temperature: float = 0.2, max_tokens: int = 4000
) -> ProjectFull:
    """Generate a :class:`ProjectFull` based on a story script."""

    prompt = build_prompt_for_story_to_project(script)
    raw_response = client.generate(prompt, temperature=temperature, max_tokens=max_tokens)
    return parse_llm_response_to_project(raw_response)

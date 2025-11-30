"""Simple OpenAI API helper.

This module provides a thin wrapper around the OpenAI Python client so it can be
swapped in once credentials are available.
"""

from __future__ import annotations

from typing import Optional

from openai import OpenAI


class OpenAIClient:
    """Helper for interacting with OpenAI models."""

    def __init__(self, model: str = "gpt-4.1", *, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, *, temperature: float = 0.2, max_tokens: int = 4000) -> str:
        """Generate a completion from the configured model.

        Args:
            prompt: The user prompt to send to the model.
            temperature: Sampling temperature for creativity.
            max_tokens: Maximum number of output tokens to generate.

        Returns:
            The model's textual response.
        """

        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        response = self.client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            max_output_tokens=max_tokens,
            temperature=temperature,
        )

        return response.output_text

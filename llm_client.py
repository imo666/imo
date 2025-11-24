"""Client interface for interacting with language models in StoryViz."""

from typing import Protocol


class LLMClient(Protocol):
    """Protocol describing minimal LLM client behavior."""

    def generate(
        self, prompt: str, temperature: float = 0.2, max_tokens: int = 2000
    ) -> str:
        """Generate a text response for the given prompt.

        Args:
            prompt: The input prompt provided to the language model.
            temperature: Controls randomness in generation.
            max_tokens: Maximum number of tokens to produce.

        Returns:
            The generated text from the model.
        """
        ...

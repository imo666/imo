import json
from typing import Any

import requests


class LocalLLMClient:
    """
    Cliente para un LLM open source desplegado localmente (por ejemplo, Ollama con un modelo tipo 'llama3').
    Implementa la interfaz LLMClient.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 4000) -> str:
        """
        Llama al endpoint /api/generate del servidor Ollama en modo streaming.
        Concatena el campo 'response' de cada chunk JSON hasta que 'done' sea True.
        Devuelve el texto completo generado por el modelo.
        """
        url = f"{self.base_url}/api/generate"
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        generated_text = []
        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line)
            generated_text.append(data.get("response", ""))

            if data.get("done"):
                break

        return "".join(generated_text)

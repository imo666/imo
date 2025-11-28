import json
from typing import Optional

import requests


class LocalLLMClient:
    """
    Cliente para un LLM open source desplegado localmente (por ejemplo, Ollama con un modelo tipo 'llama3').
    Implementa la interfaz LLMClient.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 4000) -> str:
        """
        Llama al endpoint /api/generate del servidor Ollama en modo streaming.
        Concatena el campo 'response' de cada chunk JSON hasta que 'done' sea True.
        Devuelve el texto completo generado por el modelo.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        url = f"{self.base_url}/api/generate"
        response_text: list[str] = []

        with requests.post(url, json=payload, stream=True, timeout=300) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                data = json.loads(line)
                chunk: Optional[str] = data.get("response")
                if chunk:
                    response_text.append(chunk)
                if data.get("done"):
                    break

        return "".join(response_text)

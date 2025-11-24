from __future__ import annotations

import requests
from typing import List

from .story_parser import (
    InvalidProjectDataError,
    build_prompt_for_story_to_project,
    parse_llm_response_to_project,
)


class LocalLLMClient:
    def __init__(self, model: str, base_url: str = "http://localhost:11434", timeout: int = 60) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, *, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        try:
            response = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.RequestException as exc:
            raise requests.RequestException(f"Error al llamar al LLM local: {exc}") from exc


def generate_project_from_script(
    script: str,
    llm: LocalLLMClient,
    *,
    duracion_objetivo: int,
    plataformas_destino: List[str],
) -> object:
    prompt = build_prompt_for_story_to_project(
        script=script,
        duracion_objetivo=duracion_objetivo,
        plataformas_destino=plataformas_destino,
    )

    try:
        llm_output = llm.generate(prompt)
        return parse_llm_response_to_project(llm_output)
    except requests.RequestException as exc:
        raise requests.RequestException(f"Fallo de red al comunicarse con el LLM: {exc}") from exc
    except InvalidProjectDataError as exc:
        raise InvalidProjectDataError(
            f"La respuesta del LLM no se pudo convertir en ProjectFull: {exc}"
        ) from exc


__all__ = ["LocalLLMClient", "generate_project_from_script"]


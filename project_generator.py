"""Utilities for constructing project prompts from script descriptions."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Protocol


class LLMClient(Protocol):
    """Minimal protocol for LLM clients used by project generation."""

    def complete(self, prompt: str) -> str:
        """Return the model completion for the provided prompt."""
        ...


@dataclass
class ProjectFull:
    """Normalized project information returned by the language model."""

    titulo: str
    resumen: str
    duracion_objetivo: int
    plataformas_destino: List[str]


class ProjectValidationError(ValueError):
    """Raised when the LLM response cannot be validated into a ProjectFull."""


def _build_prompt(script: str, duracion_objetivo: int, plataformas_destino: List[str]) -> str:
    objetivos = "\n".join(
        [
            "Por favor, genera un resumen detallado del proyecto a partir del siguiente guion:",
            script.strip(),
            "",
            f"La duración objetivo del proyecto es de {duracion_objetivo} días.",
            "Las plataformas de destino son: " + ", ".join(plataformas_destino),
            "Responde únicamente en JSON con las claves: 'titulo', 'resumen', 'duracion_objetivo' y 'plataformas_destino'.",
        ]
    )
    return objetivos


def _parse_project(json_payload: str) -> ProjectFull:
    try:
        data = json.loads(json_payload)
    except json.JSONDecodeError as exc:
        raise ProjectValidationError("La respuesta del LLM no es un JSON válido.") from exc

    missing_keys = {"titulo", "resumen", "duracion_objetivo", "plataformas_destino"} - data.keys()
    if missing_keys:
        raise ProjectValidationError(f"Faltan campos requeridos en la respuesta: {', '.join(sorted(missing_keys))}.")

    if not isinstance(data["plataformas_destino"], list):
        raise ProjectValidationError("'plataformas_destino' debe ser una lista.")

    return ProjectFull(
        titulo=str(data["titulo"]),
        resumen=str(data["resumen"]),
        duracion_objetivo=int(data["duracion_objetivo"]),
        plataformas_destino=[str(item) for item in data["plataformas_destino"]],
    )


def generate_project_from_script(
    script: str,
    llm: LLMClient,
    duracion_objetivo: int,
    plataformas_destino: List[str],
) -> ProjectFull:
    """
    Construye el prompt, llama al LLM y devuelve un ProjectFull validado.
    """
    prompt = _build_prompt(script=script, duracion_objetivo=duracion_objetivo, plataformas_destino=plataformas_destino)
    raw_response = llm.complete(prompt)
    return _parse_project(raw_response)

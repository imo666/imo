"""Utilities to build prompts and parse StoryViz project data."""
from __future__ import annotations

import json
from textwrap import dedent
from typing import List

from backend.models import ProjectFull


class InvalidProjectDataError(Exception):
    """Se lanza cuando el JSON devuelto por el LLM no cumple el esquema de ProjectFull."""


PROMPT_HEADER = "Convierte este script en un JSON que siga EXACTAMENTE el esquema ProjectFull"


def build_prompt_for_story_to_project(
    script: str, duracion_objetivo: int, plataformas_destino: List[str]
) -> str:
    """Construye un prompt en español para convertir un guion en ProjectFull."""

    scene_limit_rule = (
        "- Si la duración objetivo es de 90 segundos o menos, limita el JSON a un máximo de 8 escenas."
    )
    prompt = dedent(
        f"""
        Rol: {PROMPT_HEADER}.
        Reglas estrictas:
        - Devuelve únicamente JSON VÁLIDO. No incluyas texto fuera del JSON ni explicaciones.
        - {scene_limit_rule if duracion_objetivo <= 90 else "- Usa el número de escenas que necesites, pero optimiza la duración."}
        - Las duraciones de las escenas deben aproximar la duración objetivo total (segundos): {duracion_objetivo}.
        - Rellena todos los campos obligatorios de ProjectManifest y SceneV3.
        - Usa valores razonables por defecto cuando falte información en el script.
        - Plataformas destino sugeridas: {plataformas_destino}.

        Esquema esperado (resumen):
        {{
          "manifest": {{
            "title": str,
            "description": str,
            "duration_seconds": int,
            "target_platforms": list[str]
          }},
          "scenes": [
            {{
              "id": str,
              "title": str,
              "description": str,
              "duration_seconds": int,
              "visual_style": str | null,
              "audio_cues": str | null
            }},
            ...
          ]
        }}

        Ejemplo de JSON (sólo ilustrativo, adapta a tu respuesta):
        {{
          "manifest": {{
            "title": "Búsqueda submarina",
            "description": "Una exploradora desciende por un templo sumergido para recuperar un artefacto legendario.",
            "duration_seconds": 90,
            "target_platforms": ["tiktok", "youtube_short"]
          }},
          "scenes": [
            {{
              "id": "s1",
              "title": "Inmersión",
              "description": "La exploradora se sumerge entre ruinas iluminadas por su linterna.",
              "duration_seconds": 30,
              "visual_style": "Tonos azules, luz tenue",
              "audio_cues": "Efectos de burbujas, música de tensión"
            }},
            {{
              "id": "s2",
              "title": "La cámara sellada",
              "description": "Encuentra el artefacto protegido por un campo de energía.",
              "duration_seconds": 30,
              "visual_style": "Brillos verdes, runas antiguas",
              "audio_cues": "Zumbido energético, respiración contenida"
            }}
          ]
        }}

        Script original:
        {script}
        """
    ).strip()
    return prompt


def parse_llm_response_to_project(json_str: str) -> ProjectFull:
    """Parsea la respuesta JSON del LLM y devuelve un ProjectFull validado."""

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive branch
        raise InvalidProjectDataError(f"JSON inválido: {exc}") from exc

    try:
        return ProjectFull(**data)
    except Exception as exc:  # pragma: no cover - pydantic validation errors
        raise InvalidProjectDataError(f"Datos incompatibles con ProjectFull: {exc}") from exc


if __name__ == "__main__":
    script = "Una exploradora desciende a una ciudad sumergida para recuperar un artefacto."
    prompt = build_prompt_for_story_to_project(script, 90, ["tiktok", "youtube_short"])
    print(prompt)

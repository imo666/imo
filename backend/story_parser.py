import json
import re
from typing import List

from .models import ProjectFull, Scene


class InvalidProjectDataError(Exception):
    """Raised when the LLM output cannot be converted into a ProjectFull object."""


def build_prompt_for_story_to_project(script: str, duracion_objetivo: int, plataformas_destino: List[str]) -> str:
    plataformas = ", ".join(plataformas_destino)
    return (
        "Eres un guionista asistente. Convierte la siguiente historia en un JSON que represente un proyecto audiovisual. "
        "Sigue este esquema: {\"titulo\": str, \"logline\": str, \"escenas\": ["
        "{\"orden\": int, \"duracion_estimada_segundos\": int, \"tipo_plano_dominante\": str, \"peso_narrativo\": float}]}. "
        "No incluyas comentarios ni texto adicional, solo el JSON. "
        f"Duración objetivo: {duracion_objetivo} segundos. Plataformas destino: {plataformas}. Historia: {script}"
    )


def _extract_json_block(text: str) -> str:
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if match:
        return match.group(1)
    return text.strip()


def parse_llm_response_to_project(response_text: str) -> ProjectFull:
    try:
        cleaned = _extract_json_block(response_text)
        data = json.loads(cleaned)
    except (json.JSONDecodeError, TypeError) as exc:
        raise InvalidProjectDataError(f"No se pudo interpretar la respuesta del LLM como JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise InvalidProjectDataError("El formato del proyecto debe ser un objeto JSON.")

    titulo = data.get("titulo")
    logline = data.get("logline")
    escenas_raw = data.get("escenas", [])

    if not isinstance(titulo, str) or not isinstance(logline, str):
        raise InvalidProjectDataError("El proyecto debe incluir los campos 'titulo' y 'logline' como cadenas.")

    if not isinstance(escenas_raw, list):
        raise InvalidProjectDataError("El campo 'escenas' debe ser una lista.")

    escenas: List[Scene] = []
    for escena in escenas_raw:
        if not isinstance(escena, dict):
            raise InvalidProjectDataError("Cada escena debe ser un objeto con sus propiedades.")

        try:
            orden = int(escena["orden"])
            duracion_estimada_segundos = int(escena["duracion_estimada_segundos"])
            tipo_plano_dominante = str(escena["tipo_plano_dominante"])
            peso_narrativo = float(escena["peso_narrativo"])
        except (KeyError, ValueError, TypeError) as exc:
            raise InvalidProjectDataError(
                "Cada escena debe incluir 'orden', 'duracion_estimada_segundos', 'tipo_plano_dominante' y 'peso_narrativo'."
            ) from exc

        escenas.append(
            Scene(
                orden=orden,
                duracion_estimada_segundos=duracion_estimada_segundos,
                tipo_plano_dominante=tipo_plano_dominante,
                peso_narrativo=peso_narrativo,
            )
        )

    return ProjectFull(titulo=titulo, logline=logline, escenas=escenas)


__all__ = [
    "InvalidProjectDataError",
    "build_prompt_for_story_to_project",
    "parse_llm_response_to_project",
]


"""StoryViz helpers for parsing LLM output into backend models."""
from __future__ import annotations

import json
from typing import Any

from backend.models import ProjectFull


class InvalidProjectDataError(Exception):
    """Se lanza cuando el JSON devuelto por el LLM no cumple el esquema de ProjectFull."""


def _load_response_json(response_text: str) -> Any:
    """Carga la respuesta del LLM como JSON.

    Args:
        response_text: Cadena devuelta por el LLM.

    Raises:
        InvalidProjectDataError: Si el texto no es JSON válido.

    Returns:
        Objeto Python resultante de `json.loads`.
    """

    try:
        return json.loads(response_text)
    except json.JSONDecodeError as exc:
        msg = "La respuesta del LLM no es un JSON válido."
        raise InvalidProjectDataError(msg) from exc


def parse_project(response_text: str) -> ProjectFull:
    """Parsea la respuesta del LLM y la transforma en un ``ProjectFull``.

    Args:
        response_text: Texto completo devuelto por el LLM.

    Raises:
        InvalidProjectDataError: Si el JSON no respeta el esquema esperado.

    Returns:
        Instancia validada de :class:`ProjectFull`.
    """

    data = _load_response_json(response_text)
    try:
        return ProjectFull.from_dict(data)
    except Exception as exc:  # pragma: no cover - defensive, should be rare.
        msg = "El JSON no cumple con el esquema de ProjectFull."
        raise InvalidProjectDataError(msg) from exc

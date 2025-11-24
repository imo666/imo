from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Protocol, Type, TypeVar
import textwrap

T = TypeVar("T")


class LLMClient(Protocol):
    """Cliente mínimo de LLM con salida estructurada.

    La implementación debe ofrecer un método ``structured_output`` que acepte un
    esquema y un prompt, devolviendo una instancia validada del esquema.
    """

    def structured_output(self, schema: Type[T], prompt: str) -> T:  # pragma: no cover - interface
        ...


@dataclass
class ProjectFull:
    """Representación mínima del proyecto generado."""

    script: str
    duracion_objetivo: int
    plataformas_destino: List[str] = field(default_factory=list)
    descripcion: str | None = None

    @classmethod
    def model_validate(cls: Type[T], value: Any) -> T:
        if isinstance(value, cls):
            return value
        if not isinstance(value, dict):
            raise TypeError("ProjectFull.model_validate espera un diccionario o instancia de ProjectFull")
        return cls(**value)  # type: ignore[arg-type]


def _build_prompt(script: str, duracion_objetivo: int, plataformas_destino: List[str]) -> str:
    plataformas = ", ".join(plataformas_destino) if plataformas_destino else "ninguna"
    return textwrap.dedent(
        f"""
        A partir del siguiente guion quiero que propongas un proyecto educativo completo.

        Guion:
        {script}

        Duración objetivo (minutos): {duracion_objetivo}
        Plataformas de destino: {plataformas}

        Devuelve el resultado siguiendo el esquema ProjectFull en español.
        """
    ).strip()


def generate_project_from_script(
    script: str,
    llm: LLMClient,
    duracion_objetivo: int,
    plataformas_destino: List[str],
) -> ProjectFull:
    """
    Construye el prompt, llama al LLM y devuelve un ProjectFull validado.
    """

    prompt = _build_prompt(script, duracion_objetivo, plataformas_destino)
    project = llm.structured_output(ProjectFull, prompt)

    # Si el cliente devuelve un diccionario u otro tipo, intentamos validarlo.
    if isinstance(project, ProjectFull):
        return project

    return ProjectFull.model_validate(project)

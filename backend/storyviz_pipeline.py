"""Pipeline principal para generar proyectos StoryViz.

Este módulo une la generación de proyectos a partir de un guion con la
construcción de tomas (shots) necesarias para producción.
"""
from dataclasses import dataclass
from typing import List

from backend.image_prompt_builder import generate_shots_for_project
from backend.llm_client import LLMClient, generate_project_from_script
from backend.models import ProjectFull, ProjectManifest, SceneV3, ShotV3


@dataclass
class StoryVizProject:
    """Resultado completo de la pipeline de StoryViz."""

    project: ProjectFull
    shots: list[ShotV3]


def build_storyviz_project(
    script: str,
    llm: LLMClient,
    duracion_objetivo: int,
    plataformas_destino: List[str],
) -> StoryVizProject:
    """
    Ejecuta la pipeline completa StoryViz:
    1) Usa el LLM para convertir el script en un ProjectFull.
    2) Genera todos los ShotV3 a partir del manifest y las escenas.
    3) Devuelve un StoryVizProject que contiene todo lo necesario para producción.
    """
    project: ProjectFull = generate_project_from_script(
        script=script,
        llm=llm,
        duracion_objetivo=duracion_objetivo,
        plataformas_destino=plataformas_destino,
    )

    shots: list[ShotV3] = generate_shots_for_project(
        manifest=project.manifest,
        scenes=project.scenes,
    )

    return StoryVizProject(project=project, shots=shots)

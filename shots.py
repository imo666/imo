"""Utilities for assembling shot lists for a project.

This module provides a small helper to walk over a list of scenes and
collect the individual shots defined for each scene.  The logic is
intentionally minimal so it can work with lightweight data containers or
more featureful models that expose a ``shots`` attribute.
"""
from dataclasses import dataclass, field
from typing import Iterable, List


@dataclass
class ShotV3:
    """Simple data container for a generated shot."""

    id: str
    scene_id: str
    description: str = ""


def _normalize_scene_shots(scene: "SceneV3") -> Iterable[ShotV3]:
    """Return an iterable of shots defined by a scene if present.

    The helper accepts any object that exposes a ``shots`` attribute.  If the
    attribute is missing or set to ``None`` an empty iterable is returned to
    keep the caller code straightforward.
    """

    scene_shots = getattr(scene, "shots", None)
    if scene_shots is None:
        return []
    return scene_shots


@dataclass
class SceneV3:
    """Minimal representation of a scene containing shots."""

    id: str
    shots: List[ShotV3] = field(default_factory=list)


@dataclass
class ProjectManifest:
    """Lightweight manifest describing a project."""

    id: str


def generate_shots_for_project(manifest: ProjectManifest, scenes: List[SceneV3]) -> List[ShotV3]:
    """
    Genera todos los shots para un proyecto completo recorriendo la lista de escenas.
    """
    del manifest  # manifest is currently unused but kept for API completeness

    project_shots: List[ShotV3] = []
    for scene in scenes:
        project_shots.extend(_normalize_scene_shots(scene))
    return project_shots

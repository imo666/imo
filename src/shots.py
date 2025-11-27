"""
Utility structures and helpers for building shot breakdowns for a project.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence


@dataclass
class ProjectManifest:
    """Basic metadata for a project that will be used to build shot identifiers."""

    project_id: str
    title: str | None = None


@dataclass
class ShotV3:
    """Representation of a single shot in a scene."""

    id: str | None
    scene_id: str
    index: int
    description: str | None = None


@dataclass
class SceneV3:
    """Scene container that tracks the shots associated with it."""

    id: str
    name: str
    shots: List[ShotV3] = field(default_factory=list)


def _generate_scene_shots(manifest: ProjectManifest, scene: SceneV3, offset: int) -> List[ShotV3]:
    """Build a list of shots for a single scene with stable identifiers.

    Shots lacking an explicit identifier are assigned one derived from the
    project and scene order so that the resulting sequence is predictable.
    """

    generated: List[ShotV3] = []
    base = f"{manifest.project_id}-scene-{scene.id}"

    for shot_index, shot in enumerate(scene.shots, start=1):
        shot_id = shot.id or f"{base}-shot-{shot_index:03d}"
        generated.append(
            ShotV3(
                id=shot_id,
                scene_id=scene.id,
                index=offset + len(generated),
                description=shot.description,
            )
        )

    return generated


def generate_shots_for_project(manifest: ProjectManifest, scenes: Sequence[SceneV3]) -> List[ShotV3]:
    """
    Genera todos los shots para un proyecto completo recorriendo la lista de escenas.
    """

    project_shots: List[ShotV3] = []
    for scene in scenes:
        project_shots.extend(_generate_scene_shots(manifest, scene, len(project_shots)))
    return project_shots

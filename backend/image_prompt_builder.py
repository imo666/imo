"""Utilities to translate a project outline into SDXL/Juggernaut-ready image prompts.

The module revolves around three small data classes that mirror the structures
produced by the language model:

* ``ProjectFull`` represents the full project with metadata and scenes.
* ``SceneV3`` represents a textual description of a scene.
* ``ShotV3`` encapsulates a single visual shot with the prompt that can be sent
  directly to a diffusion pipeline.

The ``ImagePromptBuilder`` class exposes helpers to attach rich prompts to every
scene in a project. The generated prompts are intentionally verbose and include
cinematic language that tends to work well with SDXL and Juggernaut pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import islice, product
from typing import Iterable, List, Optional, Sequence


# Default vocabularies used to fan out each scene into multiple shots.
DEFAULT_SHOT_TYPES: Sequence[str] = (
    "wide establishing shot",
    "medium two-shot",
    "close-up on main subject",
    "over-the-shoulder viewpoint",
    "insert of key detail",
)

DEFAULT_CAMERA_MOVEMENTS: Sequence[str] = (
    "static tripod",
    "slow dolly-in",
    "handheld follow",
    "crane rise",
    "steadycam orbit",
)


@dataclass
class ShotV3:
    """Represents a single shot ready to be rendered by an image model."""

    shot_type: str
    camera_movement: str
    prompt: str
    notes: Optional[str] = None


@dataclass
class SceneV3:
    """Represents a textual scene breakdown produced by the LLM."""

    id: str
    title: str
    description: str
    environment: Optional[str] = None
    mood: Optional[str] = None
    beats: Optional[List[str]] = None
    shots: List[ShotV3] = field(default_factory=list)


@dataclass
class ProjectFull:
    """Represents the complete project with all scenes."""

    title: str
    genre: Optional[str]
    visual_style: Optional[str]
    scenes: List[SceneV3]


class ImagePromptBuilder:
    """Generate cinematic prompts for SDXL/Juggernaut pipelines."""

    def __init__(
        self,
        shot_types: Sequence[str] = DEFAULT_SHOT_TYPES,
        camera_movements: Sequence[str] = DEFAULT_CAMERA_MOVEMENTS,
        extra_positive_tokens: Optional[Sequence[str]] = None,
    ) -> None:
        self.shot_types = tuple(shot_types)
        self.camera_movements = tuple(camera_movements)
        self.extra_positive_tokens = tuple(extra_positive_tokens or ())

    def generate_shots_for_project(
        self,
        project: ProjectFull,
        shots_per_scene: int = 3,
    ) -> ProjectFull:
        """Populate every scene in a project with multiple shots.

        The original ``project`` object is updated in-place and also returned for
        convenience so the function can be chained with other transformations.
        """

        for scene in project.scenes:
            scene.shots = self.generate_shots_for_scene(project, scene, shots_per_scene)
        return project

    def generate_shots_for_scene(
        self,
        project: ProjectFull,
        scene: SceneV3,
        shots_per_scene: int = 3,
    ) -> List[ShotV3]:
        """Create a list of ``ShotV3`` entries for a single scene."""

        combinations: Iterable[tuple[str, str]] = product(self.shot_types, self.camera_movements)
        shots: List[ShotV3] = []

        for shot_type, camera_movement in islice(combinations, shots_per_scene):
            prompt = self._build_prompt(project, scene, shot_type, camera_movement)
            shots.append(
                ShotV3(
                    shot_type=shot_type,
                    camera_movement=camera_movement,
                    prompt=prompt,
                )
            )

        return shots

    def _build_prompt(
        self,
        project: ProjectFull,
        scene: SceneV3,
        shot_type: str,
        camera_movement: str,
    ) -> str:
        """Format a verbose prompt tuned for SDXL and Juggernaut models."""

        parts: List[str] = [
            f"{project.title} | {shot_type} with {camera_movement}",
            scene.description,
        ]

        if scene.environment:
            parts.append(f"location: {scene.environment}")
        if scene.mood:
            parts.append(f"mood: {scene.mood}")
        if scene.beats:
            parts.append(f"beats: {'; '.join(scene.beats)}")
        if project.genre:
            parts.append(f"genre: {project.genre}")
        if project.visual_style:
            parts.append(f"visual style: {project.visual_style}")

        cinematic_tone = (
            "cinematic lighting, anamorphic depth of field, 8k uhd, photorealistic, "
            "sdxl, juggernaut-xl, artstation trending"
        )
        parts.append(cinematic_tone)

        if self.extra_positive_tokens:
            parts.append(", ".join(self.extra_positive_tokens))

        return ", ".join(filter(None, parts))


__all__ = [
    "ImagePromptBuilder",
    "ProjectFull",
    "SceneV3",
    "ShotV3",
]

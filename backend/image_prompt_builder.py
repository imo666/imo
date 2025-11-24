"""Utilities for generating camera-ready image prompts.

This module expects a :class:`ProjectFull` object produced by a language
model. Each scene is expanded into a list of :class:`ShotV3` entries that
contain the shot type, camera movement, and a render-ready prompt for
SDXL or Juggernaut style models.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from typing import Iterable, List, Sequence


DEFAULT_SHOT_TYPES: Sequence[str] = (
    "establishing wide shot",
    "medium two-shot",
    "intimate close-up",
    "over-the-shoulder composition",
    "dramatic low-angle shot",
    "aerial/drone overview",
    "macro detail cutaway",
)

DEFAULT_CAMERA_MOVEMENTS: Sequence[str] = (
    "static tripod",
    "slow cinematic push-in",
    "gentle dolly sideways",
    "steadycam following movement",
    "orbiting pan",
    "slow tilt up",
)

STYLE_SUFFIX = {
    "sdxl": "Ultra-detailed, photorealistic, shot on 35mm, cinematic lighting, SDXL style, 8k, DOF",
    "juggernaut": "Juggernaut XL realism, crisp focus, filmic grain, dramatic lighting, 4k master",
}


@dataclass
class ShotV3:
    """A single camera shot with a ready-to-render prompt."""

    id: str
    shot_type: str
    camera_movement: str
    prompt: str


@dataclass
class SceneV3:
    """Structured scene description produced by the LLM."""

    id: str
    title: str
    summary: str
    location: str | None = None
    time_of_day: str | None = None
    mood: str | None = None
    key_elements: List[str] = field(default_factory=list)
    shots: List[ShotV3] = field(default_factory=list)


@dataclass
class ProjectFull:
    """A project containing multiple scenes."""

    id: str
    title: str
    synopsis: str
    scenes: List[SceneV3]


def _rng_from_scene(scene_id: str) -> random.Random:
    """Create a deterministic RNG seeded from the scene id."""

    digest = hashlib.sha256(scene_id.encode("utf-8")).digest()
    seed = int.from_bytes(digest[:8], "big")
    return random.Random(seed)


def build_prompt(
    scene: SceneV3,
    shot_type: str,
    camera_movement: str,
    style: str = "sdxl",
) -> str:
    """Build a SDXL or Juggernaut-friendly prompt for a shot.

    Args:
        scene: The source scene metadata.
        shot_type: The camera framing to emphasize.
        camera_movement: Motion direction or technique.
        style: Either ``"sdxl"`` or ``"juggernaut"``.

    Returns:
        A formatted prompt string ready for image generation.
    """

    style_key = style.lower()
    style_tail = STYLE_SUFFIX.get(style_key, STYLE_SUFFIX["sdxl"])

    details: list[str] = [scene.summary]
    if scene.location:
        details.append(f"Location: {scene.location}.")
    if scene.time_of_day:
        details.append(f"Time of day: {scene.time_of_day}.")
    if scene.mood:
        details.append(f"Mood: {scene.mood}.")
    if scene.key_elements:
        details.append("Key elements: " + ", ".join(scene.key_elements) + ".")

    base_description = " ".join(details)
    movement = f"Camera movement: {camera_movement}." if camera_movement else ""

    return (
        f"{shot_type} of the scene. {movement} "
        f"{base_description} {style_tail}"
    ).strip()


def generate_shots_for_scene(
    scene: SceneV3,
    *,
    shots_per_scene: int = 3,
    shot_types: Iterable[str] | None = None,
    camera_movements: Iterable[str] | None = None,
    style: str = "sdxl",
) -> List[ShotV3]:
    """Generate a list of :class:`ShotV3` entries for a scene."""

    rng = _rng_from_scene(scene.id)
    shot_type_pool = tuple(shot_types or DEFAULT_SHOT_TYPES)
    camera_pool = tuple(camera_movements or DEFAULT_CAMERA_MOVEMENTS)

    shots: list[ShotV3] = []
    for index in range(shots_per_scene):
        shot_type = shot_type_pool[index % len(shot_type_pool)]
        camera_move = camera_pool[rng.randint(0, len(camera_pool) - 1)]
        prompt = build_prompt(scene, shot_type, camera_move, style=style)
        shots.append(
            ShotV3(
                id=f"{scene.id}_shot_{index + 1}",
                shot_type=shot_type,
                camera_movement=camera_move,
                prompt=prompt,
            )
        )
    return shots


def generate_shots_for_project(
    project: ProjectFull,
    *,
    shots_per_scene: int = 3,
    shot_types: Iterable[str] | None = None,
    camera_movements: Iterable[str] | None = None,
    style: str = "sdxl",
) -> ProjectFull:
    """Populate each scene in the project with generated shots.

    The function mutates the provided project object and also returns it
    for convenience.
    """

    for scene in project.scenes:
        scene.shots = generate_shots_for_scene(
            scene,
            shots_per_scene=shots_per_scene,
            shot_types=shot_types,
            camera_movements=camera_movements,
            style=style,
        )
    return project


__all__ = [
    "ProjectFull",
    "SceneV3",
    "ShotV3",
    "build_prompt",
    "generate_shots_for_project",
    "generate_shots_for_scene",
]

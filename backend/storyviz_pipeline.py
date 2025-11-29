"""Story visualization pipeline utilities.

This module provides a lightweight, dependency-free pipeline that turns a raw
story text into structured scene breakdowns and image prompts. The design
mirrors the intended end-to-end flow:

    1. Texto de historia
    2. → LLM (local / open source)
    3. → ProjectFull (manifest + scenes)
    4. → ShotV3 con prompts de imagen listos para SDXL/Juggernaut
    5. → impresos con demo_storyviz_pipeline.py

Actual LLM and image generation backends can be swapped in later. For now we
use a deterministic stub that keeps the demo runnable without external
services.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence


@dataclass
class ProjectManifest:
    """High-level project metadata."""

    title: str
    author: str = "automatic"
    language: str = "es"


@dataclass
class Scene:
    """Narrative unit extracted from the story."""

    scene_id: int
    title: str
    summary: str
    beats: List[str]


@dataclass
class ShotV3:
    """Image-friendly description for a single beat."""

    shot_id: str
    scene_id: int
    beat_index: int
    description: str
    image_prompt: str
    negative_prompt: str = "blurry, low quality, distorted, watermark"
    aspect_ratio: str = "16:9"


@dataclass
class ProjectFull:
    """Container holding the manifest and all scenes."""

    manifest: ProjectManifest
    scenes: List[Scene] = field(default_factory=list)


class LLMClient:
    """Deterministic LLM placeholder.

    In production this class can wrap a local model (exposed via OpenAI API or
    llama.cpp) or a remote inference service. Methods return simple heuristic
    results to keep the pipeline reproducible for demos.
    """

    def summarize_scene(self, text: str) -> str:
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        if not sentences:
            return "Resumen no disponible."
        if len(sentences) == 1:
            return sentences[0]
        return f"{sentences[0]} ... {sentences[-1]}"

    def title_scene(self, summary: str, index: int) -> str:
        if summary:
            seed = summary.split()[0].capitalize()
            return f"Escena {index + 1}: {seed}"
        return f"Escena {index + 1}"

    def beatify(self, text: str) -> List[str]:
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
        if sentences:
            return sentences
        # Fallback: single beat from raw text
        return [text.strip() or "Momento clave"]

    def prompt_for_beat(self, beat: str) -> str:
        base = beat[:1].lower() + beat[1:]
        return (
            "cinematic still, detailed, volumetric lighting, "
            "style of a prestige streaming series, "
            f"depicts: {base}"
        )


class StoryVizPipeline:
    """Transforms raw story text into structured scenes and shots."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()

    def split_into_scenes(self, story_text: str) -> List[str]:
        """Divide the story into coarse scenes.

        A blank line marks a new scene. If no blank lines exist, the story is
        sliced every ~4 sentences to keep scenes digestible.
        """
        paragraphs: List[str] = [p.strip() for p in story_text.split("\n\n") if p.strip()]
        if len(paragraphs) > 1:
            return paragraphs

        sentences = [s.strip() for s in story_text.split(".") if s.strip()]
        if not sentences:
            return []

        chunk = 4
        grouped = [". ".join(sentences[i : i + chunk]) + "." for i in range(0, len(sentences), chunk)]
        return grouped

    def build_project(self, story_text: str, title: str | None = None) -> ProjectFull:
        scenes_text = self.split_into_scenes(story_text)
        manifest = ProjectManifest(title=title or "Historia sin título")

        scenes: List[Scene] = []
        for idx, raw_scene in enumerate(scenes_text):
            summary = self.llm.summarize_scene(raw_scene)
            beats = self.llm.beatify(raw_scene)
            scene = Scene(
                scene_id=idx + 1,
                title=self.llm.title_scene(summary, idx),
                summary=summary,
                beats=beats,
            )
            scenes.append(scene)

        return ProjectFull(manifest=manifest, scenes=scenes)

    def expand_shots(self, project: ProjectFull) -> List[ShotV3]:
        shots: List[ShotV3] = []
        for scene in project.scenes:
            for beat_index, beat in enumerate(scene.beats):
                shot_id = f"S{scene.scene_id:02d}-B{beat_index + 1:02d}"
                shots.append(
                    ShotV3(
                        shot_id=shot_id,
                        scene_id=scene.scene_id,
                        beat_index=beat_index,
                        description=beat,
                        image_prompt=self.llm.prompt_for_beat(beat),
                    )
                )
        return shots

    def run(self, story_text: str, title: str | None = None) -> tuple[ProjectFull, List[ShotV3]]:
        project = self.build_project(story_text, title=title)
        shots = self.expand_shots(project)
        return project, shots


def format_project(project: ProjectFull) -> str:
    lines = [f"Proyecto: {project.manifest.title} ({project.manifest.language})"]
    for scene in project.scenes:
        lines.append(f"\n[{scene.scene_id}] {scene.title}")
        lines.append(f"  Resumen: {scene.summary}")
        for beat_idx, beat in enumerate(scene.beats):
            lines.append(f"    ({beat_idx + 1}) {beat}")
    return "\n".join(lines)


def format_shots(shots: Sequence[ShotV3]) -> str:
    lines: List[str] = []
    for shot in shots:
        lines.append(f"\n{shot.shot_id} (Escena {shot.scene_id}, beat {shot.beat_index + 1})")
        lines.append(f"  Descripción: {shot.description}")
        lines.append(f"  Prompt: {shot.image_prompt}")
        lines.append(f"  Negative: {shot.negative_prompt}")
        lines.append(f"  Ratio: {shot.aspect_ratio}")
    return "\n".join(lines)


__all__ = [
    "ProjectManifest",
    "Scene",
    "ShotV3",
    "ProjectFull",
    "LLMClient",
    "StoryVizPipeline",
    "format_project",
    "format_shots",
]

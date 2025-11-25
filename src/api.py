from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, HTTPException

router = APIRouter()


@dataclass
class ScenePrompt:
    scene_id: str
    prompt: str
    output_path: Path


@dataclass
class SceneVideo:
    scene_id: str
    engine: str
    output_path: Path


def _project_root(project_id: str) -> Path:
    return Path("projects") / project_id


def _load_json(path: Path) -> Dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"No se encontró {path.name}") from exc
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Error al leer {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"{path.name} tiene un formato inválido") from exc


def _build_image_prompts(manifest: Dict, scenes: Dict, project_path: Path) -> List[ScenePrompt]:
    shots = scenes.get("shots", [])
    prompts: List[ScenePrompt] = []

    for shot in shots:
        shot_id = shot.get("id", "desconocido")
        description = shot.get("description", "")
        style = manifest.get("style", "")
        prompt_text = f"[{shot_id}] {description} {style}".strip()
        output = project_path / "images" / f"{shot_id}.png"
        prompts.append(ScenePrompt(scene_id=shot_id, prompt=prompt_text, output_path=output))

    return prompts


def _build_video_requests(scenes: Dict, project_path: Path) -> List[SceneVideo]:
    shots = scenes.get("shots", [])
    videos: List[SceneVideo] = []

    for shot in shots:
        shot_id = shot.get("id", "desconocido")
        engine = shot.get("video_engine_strategy") or shot.get("engine_hints") or "default"
        output = project_path / "videos" / f"{shot_id}.mp4"
        videos.append(SceneVideo(scene_id=shot_id, engine=str(engine), output_path=output))

    return videos


@router.post("/projects/{project_id}/generate-images")
def generate_images(project_id: str):
    """
    1) Lee ProjectManifest y Scenes_v3
    2) Construye prompts por toma
    3) Llama a tu pipeline de imágenes (ComfyUI / book2video_ultra_images refactorizado)
    4) Devuelve estado + rutas de las imágenes generadas
    """

    project_path = _project_root(project_id)
    manifest = _load_json(project_path / "ProjectManifest.json")
    scenes = _load_json(project_path / "Scenes_v3.json")

    prompts = _build_image_prompts(manifest, scenes, project_path)

    return {
        "project_id": project_id,
        "status": "queued",
        "prompts": [prompt.prompt for prompt in prompts],
        "images": [
            {"scene_id": prompt.scene_id, "output_path": str(prompt.output_path)}
            for prompt in prompts
        ],
    }


@router.post("/projects/{project_id}/generate-videos")
def generate_videos(project_id: str):
    """
    Similar, pero usando el video_engine_strategy y engine_hints de cada toma.
    """

    project_path = _project_root(project_id)
    scenes = _load_json(project_path / "Scenes_v3.json")

    videos = _build_video_requests(scenes, project_path)

    return {
        "project_id": project_id,
        "status": "queued",
        "videos": [
            {
                "scene_id": video.scene_id,
                "engine": video.engine,
                "output_path": str(video.output_path),
            }
            for video in videos
        ],
    }

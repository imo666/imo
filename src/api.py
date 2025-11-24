"""
FastAPI router that demonstrates project image and video generation endpoints.

The implementation is intentionally lightweight: it loads project metadata,
constructs prompts per shot, calls stub pipelines, and returns a structured
response with the resulting asset paths.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from fastapi import APIRouter, HTTPException

router = APIRouter()


def _load_json(path: Path, label: str) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"{label} no encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"{label} inválido: {exc}") from exc


def _project_paths(project_id: str) -> Tuple[Path, Path, Path]:
    project_dir = Path("projects") / project_id
    manifest_path = project_dir / "ProjectManifest.json"
    scenes_path = project_dir / "Scenes_v3.json"
    return project_dir, manifest_path, scenes_path


def _build_prompts(scenes: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    prompts: List[Dict[str, Any]] = []
    for index, scene in enumerate(scenes):
        base_prompt = scene.get("prompt") or scene.get("description") or "Escena"
        camera = scene.get("camera") or scene.get("camera_notes") or ""
        style = scene.get("style") or scene.get("aesthetic") or ""
        composed = " ".join(part for part in (base_prompt, camera, style) if part).strip()
        prompts.append(
            {
                "scene_id": scene.get("id", index),
                "prompt": composed,
                "engine_hints": scene.get("engine_hints", {}),
                "video_engine_strategy": scene.get("video_engine_strategy", ""),
            }
        )
    return prompts


def _write_placeholder(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _simulate_image_pipeline(project_dir: Path, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for prompt in prompts:
        asset_path = project_dir / "generated" / "images" / f"scene_{prompt['scene_id']}.png"
        _write_placeholder(asset_path, f"Imagen generada para: {prompt['prompt']}")
        results.append({"scene_id": prompt["scene_id"], "path": str(asset_path)})
    return results


def _simulate_video_pipeline(project_dir: Path, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for prompt in prompts:
        asset_path = project_dir / "generated" / "videos" / f"scene_{prompt['scene_id']}.mp4"
        strategy = prompt.get("video_engine_strategy") or "default"
        hints = prompt.get("engine_hints") or {}
        _write_placeholder(
            asset_path,
            f"Video generado usando estrategia '{strategy}' y hints {hints}: {prompt['prompt']}",
        )
        results.append(
            {
                "scene_id": prompt["scene_id"],
                "path": str(asset_path),
                "engine_strategy": strategy,
                "engine_hints": hints,
            }
        )
    return results


@router.post("/projects/{project_id}/generate-images")
def generate_images(project_id: str) -> Dict[str, Any]:
    """
    1) Lee ProjectManifest y Scenes_v3.
    2) Construye prompts por toma.
    3) Llama a tu pipeline de imágenes (simulada aquí) para generar arte.
    4) Devuelve estado + rutas de las imágenes generadas.
    """

    project_dir, manifest_path, scenes_path = _project_paths(project_id)
    _load_json(manifest_path, "ProjectManifest")
    scenes = _load_json(scenes_path, "Scenes_v3")

    prompts = _build_prompts(scenes if isinstance(scenes, list) else scenes.get("scenes", []))
    images = _simulate_image_pipeline(project_dir, prompts)

    return {"status": "completed", "project_id": project_id, "images": images}


@router.post("/projects/{project_id}/generate-videos")
def generate_videos(project_id: str) -> Dict[str, Any]:
    """
    Similar, pero usando el video_engine_strategy y engine_hints de cada toma.
    """

    project_dir, manifest_path, scenes_path = _project_paths(project_id)
    _load_json(manifest_path, "ProjectManifest")
    scenes = _load_json(scenes_path, "Scenes_v3")

    prompts = _build_prompts(scenes if isinstance(scenes, list) else scenes.get("scenes", []))
    videos = _simulate_video_pipeline(project_dir, prompts)

    return {"status": "completed", "project_id": project_id, "videos": videos}

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException

from app.models.project import ProjectManifest

# De momento, simulemos una "DB" en memoria
PROJECTS_DB: Dict[str, ProjectManifest] = {}

router = APIRouter(tags=["projects"])


@router.post("/projects", response_model=ProjectManifest)
def create_project(manifest: ProjectManifest) -> ProjectManifest:
    """Crear un nuevo proyecto, inicializando marcas de tiempo y evitando IDs duplicados."""

    if manifest.project_id in PROJECTS_DB:
        raise HTTPException(status_code=400, detail="project_id ya existe")

    now = datetime.utcnow()
    manifest.created_at = now
    manifest.updated_at = now

    PROJECTS_DB[manifest.project_id] = manifest
    return manifest


@router.get("/projects", response_model=List[ProjectManifest])
def list_projects() -> List[ProjectManifest]:
    """Listar todos los proyectos almacenados."""

    return list(PROJECTS_DB.values())


@router.get("/projects/{project_id}", response_model=ProjectManifest)
def get_project(project_id: str) -> ProjectManifest:
    """Obtener un proyecto específico o devolver 404 si no existe."""

    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return PROJECTS_DB[project_id]


@router.put("/projects/{project_id}", response_model=ProjectManifest)
def update_project(project_id: str, manifest_update: ProjectManifest) -> ProjectManifest:
    """Actualizar un proyecto existente conservando la marca de creación."""

    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if manifest_update.project_id != project_id:
        raise HTTPException(status_code=400, detail="project_id no coincide con la ruta")

    existing = PROJECTS_DB[project_id]
    merged_manifest = existing.copy(update=manifest_update.model_dump(exclude_unset=True))
    merged_manifest.created_at = existing.created_at
    merged_manifest.updated_at = datetime.utcnow()

    PROJECTS_DB[project_id] = merged_manifest
    return merged_manifest


@router.delete("/projects/{project_id}")
def delete_project(project_id: str) -> dict[str, str]:
    """Eliminar un proyecto existente o devolver 404 si no existe."""

    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    del PROJECTS_DB[project_id]
    return {"status": "ok"}

"""Pydantic models for StoryViz projects."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ProjectManifest(BaseModel):
    """Metadata about the project."""

    title: str = Field(..., description="Título del proyecto")
    description: str = Field(..., description="Descripción breve del proyecto")
    duration_seconds: int = Field(..., ge=0, description="Duración total objetivo en segundos")
    target_platforms: List[str] = Field(..., description="Plataformas de destino del video")


class SceneV3(BaseModel):
    """Represents an individual scene."""

    id: str = Field(..., description="Identificador único de la escena")
    title: str = Field(..., description="Título corto de la escena")
    description: str = Field(..., description="Descripción de lo que ocurre")
    duration_seconds: int = Field(..., ge=0, description="Duración aproximada de la escena")
    visual_style: Optional[str] = Field(None, description="Referencias visuales o estilo")
    audio_cues: Optional[str] = Field(None, description="Instrucciones de audio/locución")

    @validator("id")
    def id_not_empty(cls, value: str) -> str:  # noqa: D417
        if not value.strip():
            raise ValueError("id must not be empty")
        return value


class ProjectFull(BaseModel):
    """Full project definition including manifest and scenes."""

    manifest: ProjectManifest
    scenes: List[SceneV3]

    @validator("scenes")
    def at_least_one_scene(cls, value: List[SceneV3]) -> List[SceneV3]:  # noqa: D417
        if not value:
            raise ValueError("At least one scene is required")
        return value

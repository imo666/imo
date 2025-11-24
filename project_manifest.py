from typing import List, Literal, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class InputStorySource(BaseModel):
    tipo: Literal["texto_directo", "archivo", "url", "api"] = "texto_directo"
    resumen: Optional[str] = None


class ProjectMetadata(BaseModel):
    autor: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    notas: Optional[str] = None


class ProjectManifest(BaseModel):
    project_id: str
    titulo: str
    logline: Optional[str] = None

    modo: Literal["creador", "escritor"] = "creador"
    target_platform: Literal[
        "tiktok", "youtube_long", "youtube_short", "instagram_reel", "custom"
    ] = "tiktok"
    aspect_ratio: str = "9:16"  # podría validarse más estrictamente
    duracion_objetivo_seg: int = 60
    idioma: str = "es"

    style_preset_id: Optional[str] = None
    character_profiles: List[str] = Field(default_factory=list)

    input_story_source: InputStorySource

    scenes_file: str = "scenes_v3.json"

    image_engine_profile: str = "sdxl_plus_realvis"
    video_engine_strategy: str = "router_v1"
    scoring_profile: str = "storytelling_default_v1"
    llm_profile: str = "story_segmenter_v1"

    estado_proyecto: Literal[
        "draft",
        "segmenting",
        "ready_for_images",
        "generating_images",
        "ready_for_videos",
        "generating_videos",
        "rendered",
        "archived",
    ] = "draft"

    created_at: datetime
    updated_at: datetime

    metadatos: ProjectMetadata = Field(default_factory=ProjectMetadata)

"""Modelos de StoryViz usando Pydantic v2 y Python 3.11."""
from typing import List, Literal, Optional

from pydantic import BaseModel


class ProjectManifest(BaseModel):
    """Manifiesto principal del proyecto narrativo en StoryViz."""

    project_id: str
    titulo: str
    logline: str
    objetivo_contenido: Literal["entretener", "informar", "vender", "inspirar", "educar"]
    audiencia_principal: str
    plataformas_destino: List[
        Literal["tiktok", "reels", "youtube_short", "youtube_long", "instagram", "otros"]
    ]
    duracion_objetivo_segundos: int
    ratio_aspecto: Literal["9:16", "16:9", "1:1"]
    estilo_visual_base: str
    nivel_control: Literal["simple", "avanzado"]
    script_original: str


class SceneV3(BaseModel):
    """Representa una escena con información narrativa y visual."""

    scene_id: str
    orden: int
    peso_narrativo: Literal["bajo", "medio", "alto", "climax"]
    descripcion_narrativa: str
    objetivo_emocional: str
    duracion_estimada_segundos: float
    estilo_visual_objetivo: str
    tipo_plano_dominante: Literal["detalle", "primer_plano", "plano_medio", "plano_general"]
    quality_budget: Literal["bajo", "medio", "alto"]
    image_model_profile: str
    video_preview_model: Optional[str]
    video_final_model: Optional[str]


class ShotV3(BaseModel):
    """Describe un plano individual dentro de una escena."""

    shot_id: str
    orden: int
    tipo_plano: Literal["detalle", "primer_plano", "plano_medio", "plano_general"]
    movimiento_camara: str
    descripcion_visual: str
    prompt_base_imagen: str
    prompt_base_video: Optional[str]


class ProjectFull(BaseModel):
    """Modelo completo que agrupa el manifiesto y las escenas del proyecto."""

    manifest: ProjectManifest
    scenes: List[SceneV3]

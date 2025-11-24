"""
Model definitions for StoryViz.
"""

# Using Pydantic v2 for model definitions.
from typing import List, Literal, Optional

from pydantic import BaseModel


class ProjectManifest(BaseModel):
    """Datos principales y restricciones del proyecto de video en StoryViz."""

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
    """Escena dentro de un proyecto, con metas narrativas y de producción."""

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
    tipo_accion: Literal["dialogo", "monologo", "accion_camara", "transicion"]
    render_strategy: Literal["preview_only", "final_direct", "preview_then_final"]
    video_preview_model: Optional[str] = None
    video_final_model: Optional[str] = None


class ShotV3(BaseModel):
    """Toma individual con detalles visuales y de cámara."""

    shot_id: str
    orden: int
    tipo_plano: Literal["detalle", "primer_plano", "plano_medio", "plano_general"]
    movimiento_camara: str
    descripcion_visual: str
    prompt_base_imagen: str
    prompt_base_video: Optional[str] = None


class ProjectFull(BaseModel):
    """Representación completa de un proyecto con manifest y escenas."""

    manifest: ProjectManifest
    scenes: List[SceneV3]

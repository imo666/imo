from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ShotEngineHints(BaseModel):
    """Hints for selecting and ranking the video generation engine."""

    video_engine_preferido: Optional[Literal["ltx", "mochi", "wan", "hunyuan"]] = None
    prioridad_scoring: Optional[str] = None


class ShotMetadata(BaseModel):
    """Additional metadata collected for a shot."""

    comentarios: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class Shot(BaseModel):
    """Represents a single shot within a scene."""

    id: str

    modelo_imagen: str = "realvis"
    frames: int = 3

    tipo_plano: Optional[str] = None  # descripción humana
    shot_size: Optional[str] = None  # "extreme_wide", "medium", etc.
    camera_angle: Optional[str] = None  # "low", "eye", "high", "bird_eye", "dutch"
    camera_position: Optional[str] = None  # "frontal", "tres_cuartos", "perfil", "espalda"
    lens_type: Optional[str] = None  # "35mm", "50mm", "wide", "tele", etc.

    funcion_narrativa: Optional[str] = None  # "establecer_lugar", "entrada_personaje", ...
    intensidad_emocional: float = 0.0  # 0.0–1.0

    personajes_en_toma: List[str] = Field(default_factory=list)
    referencia_visual_anterior: bool = False

    detalle: str

    duracion_segundos: float = 3.0
    fps: int = 24
    motion_strength: float = 0.5

    engine_hints: ShotEngineHints = Field(default_factory=ShotEngineHints)
    metadatos: ShotMetadata = Field(default_factory=ShotMetadata)


class Scene(BaseModel):
    """A scene in a story, containing multiple shots."""

    id: str
    nombre: str

    acto: int = 1
    rol_narrativo: Optional[str] = None  # "setup", "conflicto", "climax", ...
    beat: Optional[str] = None

    descripcion: str
    ritmo: Literal["lento", "medio", "rapido"] = "medio"
    tono_emocional: Optional[str] = None

    complejidad_visual: Literal["baja", "media", "alta"] = "media"
    tipo_movimiento_esperado: Literal["estatico", "leve", "intenso"] = "leve"

    duracion_objetivo_seg: Optional[float] = None

    tomas: List[Shot] = Field(default_factory=list)


class ScenesDocument(BaseModel):
    """Top-level container for a scripted project with multiple scenes."""

    proyecto: str
    personajes_globales: Optional[str] = None
    estilo_global: Optional[str] = None
    notas_narrativas: Optional[str] = None

    escenas: List[Scene] = Field(default_factory=list)


__all__ = [
    "ScenesDocument",
    "Scene",
    "Shot",
    "ShotMetadata",
    "ShotEngineHints",
]

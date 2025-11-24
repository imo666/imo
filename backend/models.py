from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProjectManifest:
    """Información global del proyecto cinematográfico."""

    title: str
    logline: Optional[str] = None
    style: Optional[str] = None
    color_palette: Optional[str] = None
    lighting_style: Optional[str] = None
    camera_lens: Optional[str] = None
    composition: Optional[str] = None
    visual_inspirations: Optional[List[str]] = None
    negative_prompts: Optional[List[str]] = None


@dataclass
class ShotV3:
    """Representa un plano individual en la escena."""

    index: int
    tipo_plano: str
    descripcion: str
    prompt: Optional[str] = None
    negative_prompt: Optional[str] = None


@dataclass
class SceneV3:
    """Escena con su contexto visual y lista de planos."""

    scene_id: str
    resumen: str
    entorno: Optional[str] = None
    iluminacion: Optional[str] = None
    color: Optional[str] = None
    camara: Optional[str] = None
    composicion: Optional[str] = None
    estilo_visual: Optional[str] = None
    shots: List[ShotV3] = field(default_factory=list)

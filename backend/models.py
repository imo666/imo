from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProjectManifest:
    """
    Datos de alto nivel para un proyecto StoryViz.

    Los campos son opcionales para permitir que el generador de prompts funcione
    incluso cuando falten detalles en el manifiesto.
    """

    title: str
    genre: Optional[str] = None
    visual_style: Optional[str] = None
    color_palette: Optional[str] = None
    lighting: Optional[str] = None
    camera_style: Optional[str] = None
    target_model: Optional[str] = None
    negative_prompt: Optional[str] = None
    keywords: List[str] = field(default_factory=list)


@dataclass
class SceneV3:
    """
    Representa una escena dentro del proyecto.

    `shots` puede contener descripciones predefinidas para cada plano, por
    ejemplo: {"tipo_plano": "primer plano", "detalle": "el protagonista mira"}.
    """

    id: str
    title: str
    description: str
    location: Optional[str] = None
    time_of_day: Optional[str] = None
    mood: Optional[str] = None
    visual_style: Optional[str] = None
    beats: List[str] = field(default_factory=list)
    shots: List[dict] = field(default_factory=list)


@dataclass
class ShotV3:
    """Plano individual con un prompt cinematográfico listo para imagen."""

    order: int
    tipo_plano: str
    prompt: str
    negative_prompt: Optional[str] = None
    notes: Optional[str] = None


__all__ = ["ProjectManifest", "SceneV3", "ShotV3"]

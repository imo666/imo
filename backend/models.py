from dataclasses import dataclass, field
from typing import List


@dataclass
class Scene:
    orden: int
    duracion_estimada_segundos: int
    tipo_plano_dominante: str
    peso_narrativo: float


@dataclass
class ProjectFull:
    titulo: str
    logline: str
    escenas: List[Scene] = field(default_factory=list)


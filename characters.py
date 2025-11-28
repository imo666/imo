from typing import List, Optional

from pydantic import BaseModel, Field


class CharacterReferenceVisual(BaseModel):
    """Referencia visual de un personaje."""

    tipo: str  # "imagen_subida", "url", ...
    path: str  # ruta local o URL
    uso: Optional[str] = None  # "ip_adapter_face", "inspiracion", etc.


class CharacterEngineBindings(BaseModel):
    """Recursos del motor asociados al personaje."""

    ip_adapter_profile_id: Optional[str] = None
    lora_ids: List[str] = Field(default_factory=list)


class CharacterProfile(BaseModel):
    """Perfil narrativo y técnico de un personaje."""

    id: str
    nombre: Optional[str] = None
    rol: Optional[str] = None  # "protagonista", "secundario", ...

    descripcion: Optional[str] = None
    rasgos_clave: List[str] = Field(default_factory=list)

    referencias_visuales: List[CharacterReferenceVisual] = Field(default_factory=list)
    estilo_ropa_base: Optional[str] = None
    paleta_color_personaje: List[str] = Field(default_factory=list)

    engine_bindings: CharacterEngineBindings = Field(default_factory=CharacterEngineBindings)

    notas: Optional[str] = None


class CharactersDocument(BaseModel):
    """Documento que agrupa múltiples personajes."""

    personajes: List[CharacterProfile] = Field(default_factory=list)

# StoryViz · Contratos de Datos v1

Versión: 1.0  
Estado: BORRADOR ESTABLE (base para futuras extensiones)  
Autor: [Tú]

Este documento define los **contratos de datos canónicos** de StoryViz.
Son la referencia que deben respetar:

- El backend (FastAPI, DB, colas).
- Los workers GPU (ComfyUI, pipelines de imagen/vídeo).
- Los agentes de IA (Sophia v3, Book2Video Master, etc.).
- Cualquier herramienta externa que quiera integrarse con StoryViz.

Hay tres bloques principales:

1. `ProjectManifest` – definición de un proyecto StoryViz.
2. `Scenes_v3` – definición del guion técnico visual (escenas/tomas).
3. `CharacterProfile` – definición de personajes clave.

---

## 1. ProjectManifest

Representa un proyecto completo en StoryViz:  
desde el texto inicial hasta los vídeos y clips finales.

### 1.1. Estructura general (informal)

```jsonc
{
  "project_id": "uuid",
  "titulo": "La noche que cambió todo",
  "logline": "Una chica entra a un bar y su vida cambia en 10 minutos.",
  "modo": "creador",               // "creador" | "escritor"
  "target_platform": "tiktok",     // "tiktok" | "youtube_long" | "youtube_short" | "instagram_reel" | "custom"
  "aspect_ratio": "9:16",          // "16:9" | "9:16" | "1:1" | etc.
  "duracion_objetivo_seg": 60,
  "idioma": "es",
  "style_preset_id": "cinematic_tiktok_v1",
  "character_profiles": ["protagonista", "amiga"],
  "input_story_source": {
    "tipo": "texto_directo",       // "texto_directo" | "archivo" | "url" | "api"
    "resumen": "Texto pegado por el usuario en la UI"
  },
  "scenes_file": "scenes_v3.json", // ruta relativa dentro del proyecto
  "image_engine_profile": "sdxl_plus_realvis",
  "video_engine_strategy": "router_v1",
  "scoring_profile": "storytelling_default_v1",
  "llm_profile": "story_segmenter_v1",
  "estado_proyecto": "draft",      // ver enumeración abajo
  "created_at": "2025-11-23T10:32:00Z",
  "updated_at": "2025-11-23T10:32:00Z",
  "metadatos": {
    "autor": "Nombre o alias del usuario",
    "tags": ["terror", "nocturno", "bar"],
    "notas": "Cualquier comentario libre"
  }
}
```

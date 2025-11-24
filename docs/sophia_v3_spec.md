# Sophia v3: Estructura de proyectos audiovisuales

Este documento resume la estructura de datos para proyectos, escenas y personajes usada por Sophia v3.

## 1. ProjectManifest

### 1.1 Campos y enumeraciones
- `project_id` (string, uuid): Identificador único global del proyecto.
- `titulo` (string): Nombre legible del proyecto.
- `logline` (string): Resumen corto de la historia (1–2 frases).
- `modo` (string):
  - `escritor` → historias largas, estructura de actos/beats más marcada.
  - `creador` → contenido más corto, optimizado para plataformas tipo TikTok/Reels.
- `target_platform` (string): Controla presets de duración, ratio, etc. Ejemplos: `tiktok`, `youtube_short`, `youtube_long`, `instagram_reel`, `custom`.
- `aspect_ratio` (string): Convención "16:9", "9:16", "1:1", etc.
- `duracion_objetivo_seg` (number): Duración objetivo total del vídeo final (aprox).
- `idioma` (string, ISO 639–1): `es`, `en`, etc. Afecta prompts y tono.
- `style_preset_id` (string): ID de un preset de estilo global (definido en otra tabla/JSON).
- `character_profiles` (array[string]): IDs de personajes definidos en CharacterProfile.
- `input_story_source` (objeto):
  - `tipo`: `texto_directo` | `archivo` | `url` | `api`.
  - `resumen`: pequeña descripción (no hace falta guardar el texto entero aquí).
- `scenes_file` (string): Ruta al archivo Scenes_v3 que describe escenas/tomas.
- `image_engine_profile` (string): Perfil de motor de imagen (modelo SDXL + configuración).
- `video_engine_strategy` (string): Estrategia de selección de modelo de vídeo (`router_v1` que decide LTX/Mochi/Wan/Hunyuan según escena/toma).
- `scoring_profile` (string): Perfil de scoring estético/alignment que se aplicará.
- `llm_profile` (string): Perfil de LLM/proceso usado para segmentar la historia y generar Scenes_v3.
- `estado_proyecto` (string): Valores recomendados: `draft`, `segmenting`, `ready_for_images`, `generating_images`, `ready_for_videos`, `generating_videos`, `rendered`, `archived`.
- `created_at`, `updated_at` (string, ISO 8601): Timestamps de auditoría.
- `metadatos` (objeto libre): Solo para información auxiliar que no controle la lógica del sistema.

### 1.2 Ejemplo mínimo
```json
{
  "project_id": "a3d5f7b2-19e4-4c8e-a2d9-91b27c8e52aa",
  "titulo": "La noche que cambió todo",
  "logline": "Una chica tímida entra en un bar de neón y algo sobrenatural ocurre.",
  "modo": "creador",
  "target_platform": "tiktok",
  "aspect_ratio": "9:16",
  "duracion_objetivo_seg": 60,
  "idioma": "es",
  "style_preset_id": "cinematic_tiktok_v1",
  "character_profiles": ["protagonista", "amiga"],
  "input_story_source": {
    "tipo": "texto_directo",
    "resumen": "Historia pegada por el usuario en la interfaz."
  },
  "scenes_file": "scenes_v3.json",
  "image_engine_profile": "sdxl_plus_realvis",
  "video_engine_strategy": "router_v1",
  "scoring_profile": "storytelling_default_v1",
  "llm_profile": "story_segmenter_v1",
  "estado_proyecto": "draft",
  "created_at": "2025-11-23T10:32:00Z",
  "updated_at": "2025-11-23T10:32:00Z",
  "metadatos": {
    "autor": "Ico",
    "tags": ["neón", "sobrenatural"],
    "notas": "Primer experimento de TikTok storytime."
  }
}
```

## 2. Scenes_v3
Representa el guion técnico visual de la historia.

### 2.1 Estructura general
```json
{
  "proyecto": "La noche que cambió todo",
  "personajes_globales": "Protagonista: chica 20 años, pelo rizado, chaqueta roja. Amiga: chico 22 años, sudadera negra.",
  "estilo_global": "realista, nocturno, luces de neón azul y rosa, atmósfera cinematográfica.",
  "notas_narrativas": "Historia breve pensada para formato vertical tipo TikTok.",
  "escenas": [ /* array de Scene */ ]
}
```

### 2.2 Scene
```json
{
  "id": "escena_1",
  "nombre": "Llegada al local",
  "acto": 1,
  "rol_narrativo": "setup",
  "beat": "introduccion_protagonista",
  "descripcion": "La protagonista llega a un bar pequeño con luces de neón, algo nerviosa, buscando a su amigo.",
  "ritmo": "medio",
  "tono_emocional": "tenso",
  "complejidad_visual": "media",
  "tipo_movimiento_esperado": "leve",
  "duracion_objetivo_seg": 10,
  "tomas": [ /* array de Shot */ ]
}
```

### 2.3 Shot (Toma)
```json
{
  "id": "A",
  "modelo_imagen": "realvis",
  "frames": 3,
  "tipo_plano": "gran plano general",
  "shot_size": "extreme_wide",
  "camera_angle": "high_angle",
  "camera_position": "frontal",
  "lens_type": "35mm",
  "funcion_narrativa": "establecer_lugar",
  "intensidad_emocional": 0.4,
  "personajes_en_toma": [],
  "referencia_visual_anterior": false,
  "detalle": "Vista del bar desde la calle, lluvia ligera, neón azul y rosa.",
  "duracion_segundos": 3.0,
  "fps": 24,
  "motion_strength": 0.4,
  "engine_hints": {
    "video_engine_preferido": "ltx",
    "prioridad_scoring": "composicion"
  },
  "metadatos": {
    "comentarios": "Plano de apertura, se puede usar como establishing shot.",
    "tags": ["lluvia", "neon", "bar_exterior"]
  }
}
```

### 2.4 Ejemplo de Scenes_v3 con 2 tomas
```json
{
  "proyecto": "La noche que cambió todo",
  "personajes_globales": "Protagonista: chica 20 años, pelo rizado, chaqueta roja. Amiga: chico 22 años, sudadera negra.",
  "estilo_global": "realista, nocturno, luces de neón azul y rosa, atmósfera cinematográfica.",
  "notas_narrativas": "Primer experimento en formato vertical.",
  "escenas": [
    {
      "id": "escena_1",
      "nombre": "Llegada al local",
      "acto": 1,
      "rol_narrativo": "setup",
      "beat": "introduccion_protagonista",
      "descripcion": "La protagonista llega al bar bajo la lluvia y se detiene frente al neón.",
      "ritmo": "medio",
      "tono_emocional": "tenso",
      "complejidad_visual": "media",
      "tipo_movimiento_esperado": "leve",
      "duracion_objetivo_seg": 10,
      "tomas": [
        {
          "id": "A",
          "modelo_imagen": "realvis",
          "frames": 3,
          "tipo_plano": "gran plano general",
          "shot_size": "extreme_wide",
          "camera_angle": "high",
          "camera_position": "frontal",
          "lens_type": "35mm",
          "funcion_narrativa": "establecer_lugar",
          "intensidad_emocional": 0.4,
          "personajes_en_toma": [],
          "referencia_visual_anterior": false,
          "detalle": "Vista del bar desde la calle, lluvia ligera, neón azul y rosa.",
          "duracion_segundos": 3.0,
          "fps": 24,
          "motion_strength": 0.4,
          "engine_hints": {
            "video_engine_preferido": "ltx"
          },
          "metadatos": {
            "comentarios": "Plano de apertura.",
            "tags": ["establecer_lugar"]
          }
        },
        {
          "id": "B",
          "modelo_imagen": "realvis",
          "frames": 3,
          "tipo_plano": "plano medio",
          "shot_size": "medium",
          "camera_angle": "eye",
          "camera_position": "tres_cuartos",
          "lens_type": "50mm",
          "funcion_narrativa": "entrada_personaje",
          "intensidad_emocional": 0.6,
          "personajes_en_toma": ["protagonista"],
          "referencia_visual_anterior": true,
          "detalle": "La protagonista abre la puerta del bar, se ve su cara ligeramente nerviosa.",
          "duracion_segundos": 4.0,
          "fps": 24,
          "motion_strength": 0.6,
          "engine_hints": {
            "video_engine_preferido": "wan"
          },
          "metadatos": {
            "comentarios": "Plano hero de la protagonista.",
            "tags": ["entrada_personaje"]
          }
        }
      ]
    }
  ]
}
```

## 3. CharacterProfile
### 3.1 Estructura general
```json
{
  "personajes": [
    {
      "id": "protagonista",
      "nombre": "Lucía",
      "rol": "protagonista",
      "descripcion": "Chica de 20 años, pelo rizado castaño, ojos claros, lleva chaqueta roja y mochila pequeña.",
      "rasgos_clave": [
        "tímida pero valiente",
        "ligeramente introvertida",
        "gesto de preocupación frecuente"
      ],
      "referencias_visuales": [
        {
          "tipo": "imagen_subida",
          "path": "assets/personajes/lucia_ref1.png",
          "uso": "ip_adapter_face"
        }
      ],
      "estilo_ropa_base": "casual urbano, chaqueta roja, vaqueros, zapatillas",
      "paleta_color_personaje": ["#D7263D", "#1F1F1F", "#F5F5F5"],
      "engine_bindings": {
        "ip_adapter_profile_id": "lucia_face_v1",
        "lora_ids": ["lucia_style_lora_v1"]
      },
      "notas": "La protagonista debe mantenerse reconocible en todas las escenas."
    }
  ]
}
```

## 4. Convenciones y extensibilidad
- Añade nuevos campos primero aquí (v2, v3…), explica para qué sirven e indica qué partes del sistema deben conocerlos (backend, pipelines, UX).
- Usa snake_case para claves JSON en español (`duracion_segundos`, `tipo_movimiento_esperado`).
- IDs cortos en inglés donde convenga (`router_v1`, `wan`, `ltx`).
- Si una parte del sistema no conoce un campo debe poder ignorarlo sin romperse.
- Los campos críticos deben documentarse como obligatorios en la especificación.

Esta base sirve para construir modelos Pydantic (`ProjectManifest`, `Scene`, `Shot`, `CharacterProfile`) y los endpoints FastAPI correspondientes (`/projects`, `/projects/{id}/scenes`, etc.).

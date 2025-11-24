from typing import List


def build_prompt_for_story_to_project(
    script: str,
    duracion_objetivo: int,
    plataformas_destino: List[str],
) -> str:
    """
    Construye el prompt maestro que se envía al LLM para convertir un script narrativo
    en un ProjectFull (ProjectManifest + Scenes_v3) listo para StoryViz.
    """
    plataformas_str = ", ".join(plataformas_destino)

    prompt = f"""
Eres STORYVIZ_SCENE_PLANNER, un modelo experto en narrativa audiovisual y planificación de escenas
para la plataforma StoryViz.

TU TAREA:
A partir de un SCRIPT NARRATIVO vas a devolver un ÚNICO JSON que siga EXACTAMENTE este esquema:

{{
  "manifest": {{
    "project_id": "string",
    "titulo": "string",
    "logline": "string",
    "objetivo_contenido": "entretener" | "informar" | "vender" | "inspirar" | "educar",
    "audiencia_principal": "string",
    "plataformas_destino": ["tiktok","reels","youtube_short","youtube_long","instagram","otros"],
    "duracion_objetivo_segundos": number,
    "ratio_aspecto": "9:16" | "16:9" | "1:1",
    "estilo_visual_base": "string",
    "nivel_control": "simple" | "avanzado",
    "script_original": "string"
  }},
  "scenes": [
    {{
      "scene_id": "string",
      "orden": number,
      "peso_narrativo": "bajo" | "medio" | "alto" | "climax",
      "descripcion_narrativa": "string",
      "objetivo_emocional": "string",
      "duracion_estimada_segundos": number,
      "estilo_visual_objetivo": "string",
      "tipo_plano_dominante": "detalle" | "primer_plano" | "plano_medio" | "plano_general",
      "quality_budget": "bajo" | "medio" | "alto",
      "image_model_profile": "string",
      "tipo_accion": "dialogo" | "monologo" | "accion_camara" | "transicion",
      "render_strategy": "preview_only" | "final_direct" | "preview_then_final",
      "video_preview_model": "string | null",
      "video_final_model": "string | null"
    }}
  ]
}}

REGLAS IMPORTANTES:

1. FORMATO
- Devuelve SOLO el JSON, sin texto antes ni después.
- No incluyas comentarios, ni claves adicionales, ni campos nulos inventados.
- Usa comillas dobles para todas las cadenas.

2. ESCENAS Y DURACIONES
- Si la duración objetivo es menor o igual a 90 segundos, genera MÁXIMO 8 escenas.
- Suma de "duracion_estimada_segundos" ≈ DURACION_OBJETIVO_SEGUNDOS (tolerancia ±15%).
- Las primeras escenas suelen ser introducción, las últimas resolución/clímax.

3. CAMPOS NARRATIVOS
- "descripcion_narrativa": 1–3 frases claras que describan lo que se ve en esa escena.
- "objetivo_emocional": palabra o frase corta (p.ej. "tensión", "misterio", "esperanza", "peligro").
- "peso_narrativo":
  - "climax" normalmente en 1 escena (máx 2) hacia el final.
  - "alto" para escenas clave de giro.
  - "medio" para desarrollo.
  - "bajo" para transiciones.

4. CAMPOS CINEMATOGRÁFICOS
- "tipo_plano_dominante":
  - "detalle": manos, objetos, ojos, pequeños detalles.
  - "primer_plano": rostro y expresión emocional.
  - "plano_medio": personaje de cintura para arriba, diálogo y acciones moderadas.
  - "plano_general": ambiente, entorno, establishing shot.
- Elige el tipo de plano dominante que mejor represente el momento de la escena.

5. MULTI-MODELO (IMAGEN Y VÍDEO)
- "image_model_profile":
  - Usa "auto" por defecto.
  - Si el estilo parece muy realista/cinematográfico, puedes sugerir "juggernaut_cinematic_v1".
  - Si es muy estilizado (anime, ilustración), puedes usar algo como "anime_stylized_v1".
- "render_strategy":
  - Para la mayoría de escenas usa "preview_then_final".
  - Usa "preview_only" solo en escenas de muy bajo peso narrativo o transición.
  - Usa "final_direct" en escenas simples donde no haga falta preview.
- "video_preview_model":
  - Por defecto: "ltx_standard_v1".
- "video_final_model":
  - Si "peso_narrativo" es "climax" o "alto" y la escena es importante:
    - Usa "hunyuan_hero_v1" para escenas cortas (≤ 5s) muy intensas.
    - Usa "mochi_cinematic_v1" para el resto de escenas importantes.
  - Si el peso es "medio" o "bajo", puedes usar:
    - "mochi_standard_v1" o dejarlo null si solo se usará el preview.

6. QUALITY BUDGET
- "quality_budget":
  - "alto" para escenas de "climax" o "alto".
  - "medio" para desarrollo normal.
  - "bajo" para transiciones o escenas de poco peso.

7. CAMPOS DEL MANIFEST
- "project_id": puedes usar un id simple tipo "auto_001".
- "titulo": título corto sugerido para el vídeo (no más de 80 caracteres).
- "logline": 1 frase que resuma el conflicto central y el gancho.
- "objetivo_contenido": elige la que mejor encaje según el script.
- "audiencia_principal": describe brevemente el tipo de público (por ejemplo "fans de ciencia ficción", "emprendedores", etc.).
- "plataformas_destino": respeta esta lista EXACTA de valores permitidos.
- "duracion_objetivo_segundos": usa el valor de entrada.
- "ratio_aspecto":
  - Si alguna plataforma es "tiktok" o "reels" → "9:16".
  - Si solo hay "youtube_long" → "16:9".
  - En caso mixto entre shorts y largo, prioriza "9:16".
- "estilo_visual_base": una frase corta (p.ej. "realista_cinematico_oscuro", "anime_luminoso").
- "nivel_control": usa "simple" por defecto.

EJEMPLO DE SALIDA (EJEMPLO ILUSTRATIVO, ADÁPTALO AL SCRIPT REAL):

{{
  "manifest": {{
    "project_id": "auto_001",
    "titulo": "La ciudad sumergida",
    "logline": "Una exploradora desciende a una ciudad oculta bajo el mar y debe elegir entre salvarse o sacrificarlo todo.",
    "objetivo_contenido": "entretener",
    "audiencia_principal": "fans de aventuras y ciencia ficción",
    "plataformas_destino": ["tiktok","youtube_short"],
    "duracion_objetivo_segundos": {duracion_objetivo},
    "ratio_aspecto": "9:16",
    "estilo_visual_base": "realista_cinematico_azul",
    "nivel_control": "simple",
    "script_original": "AQUÍ VA EL SCRIPT ORIGINAL COMPLETO"
  }},
  "scenes": [
    {{
      "scene_id": "scene_01",
      "orden": 1,
      "peso_narrativo": "medio",
      "descripcion_narrativa": "La exploradora se equipa y se lanza al océano en una noche tormentosa.",
      "objetivo_emocional": "anticipación",
      "duracion_estimada_segundos": 12.0,
      "estilo_visual_objetivo": "realista_cinematico_azul",
      "tipo_plano_dominante": "plano_general",
      "quality_budget": "medio",
      "image_model_profile": "juggernaut_cinematic_v1",
      "tipo_accion": "accion_camara",
      "render_strategy": "preview_then_final",
      "video_preview_model": "ltx_standard_v1",
      "video_final_model": "mochi_cinematic_v1"
    }},
    {{
      "scene_id": "scene_02",
      "orden": 2,
      "peso_narrativo": "climax",
      "descripcion_narrativa": "Frente al núcleo brillante de la ciudad, la exploradora duda entre activar el artefacto o huir.",
      "objetivo_emocional": "tension",
      "duracion_estimada_segundos": 10.0,
      "estilo_visual_objetivo": "realista_cinematico_azul",
      "tipo_plano_dominante": "primer_plano",
      "quality_budget": "alto",
      "image_model_profile": "juggernaut_cinematic_v1",
      "tipo_accion": "monologo",
      "render_strategy": "preview_then_final",
      "video_preview_model": "ltx_standard_v1",
      "video_final_model": "hunyuan_hero_v1"
    }}
  ]
}}

AHORA, APLICA ESTAS MISMAS REGLAS AL SIGUIENTE CASO REAL:

DURACION_OBJETIVO_SEGUNDOS: {duracion_objetivo}
PLATAFORMAS_DESTINO: [{plataformas_str}]

SCRIPT_NARRATIVO:
"""{script}"""

Recuerda:
- Devuelve SOLO el JSON válido.
- No escribas explicaciones adicionales.
"""
    return prompt.strip()

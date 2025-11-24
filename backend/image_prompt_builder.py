from typing import List

from backend.models import ProjectManifest, SceneV3, ShotV3


def build_base_image_prompt(
    manifest: ProjectManifest,
    scene: SceneV3,
    tipo_plano: str,
) -> str:
    """
    Construye un prompt base para SDXL/Juggernaut usando bloques cinematográficos:
    - Sujeto/acción
    - Entorno/escenario
    - Iluminación
    - Color / mood
    - Cámara y objetivo
    - Composición
    - Estilo visual / modelo
    """
    sujeto_accion = scene.description or scene.title
    entorno = scene.location or "entorno sin especificar"
    iluminacion = manifest.lighting or scene.time_of_day or "iluminación cinematográfica suave"
    mood = scene.mood or manifest.genre or "dramático"
    camara = manifest.camera_style or "lente anamórfico, profundidad de campo"
    composicion = f"{tipo_plano}, composición dinámica, regla de los tercios"

    estilo = scene.visual_style or manifest.visual_style or "realismo detallado"
    modelo = manifest.target_model or "SDXL, Juggernaut"
    color = manifest.color_palette or "color grading cinematográfico"
    keywords = ", ".join(manifest.keywords) if manifest.keywords else ""

    bloques = [
        f"Sujeto y acción: {sujeto_accion}.",
        f"Entorno: {entorno}.",
        f"Iluminación: {iluminacion}.",
        f"Color y mood: {color}, tono {mood}.",
        f"Cámara: {camara}.",
        f"Composición: {composicion}.",
        f"Estilo visual: {estilo}, modelo {modelo}.",
    ]

    if keywords:
        bloques.append(f"Palabras clave: {keywords}.")

    return " ".join(bloques)


def build_shots_from_scene(manifest: ProjectManifest, scene: SceneV3) -> List[ShotV3]:
    """
    Genera una lista de ShotV3 con prompts listos para SDXL/Juggernaut.

    La escena puede aportar descripciones de planos en ``scene.shots``; si no
    existen, se usan los ``beats`` o un plano genérico basado en la descripción.
    Cada prompt aplica el bloque base y añade una acción específica para el plano.
    """
    fuentes = scene.shots or [
        {"tipo_plano": "plano medio", "detalle": beat} for beat in scene.beats
    ]

    if not fuentes:
        fuentes = [{"tipo_plano": "plano medio", "detalle": scene.description}]

    shots: List[ShotV3] = []
    for indice, fuente in enumerate(fuentes, start=1):
        tipo_plano = fuente.get("tipo_plano") or "plano medio"
        detalle = (
            fuente.get("detalle")
            or fuente.get("descripcion")
            or scene.description
            or scene.title
        )

        base_prompt = build_base_image_prompt(manifest, scene, tipo_plano)
        prompt = " ".join(
            [
                base_prompt,
                f"Acción del plano: {detalle}.",
                "Cinema quality, 8k, ultra detailed, high dynamic range, aspect ratio 16:9.",
            ]
        )

        shots.append(
            ShotV3(
                order=indice,
                tipo_plano=tipo_plano,
                prompt=prompt,
                negative_prompt=manifest.negative_prompt,
                notes=fuente.get("notas"),
            )
        )

    return shots

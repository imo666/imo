"""Utilidades para construir prompts de imagen cinematográficos."""

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
    partes: List[str] = []

    partes.append(
        f"Escena {scene.scene_id}: {scene.resumen.strip()}"
        if scene.scene_id
        else scene.resumen.strip()
    )
    partes.append(f"Plano {tipo_plano}".strip())

    if scene.entorno:
        partes.append(f"Entorno: {scene.entorno.strip()}")
    if scene.iluminacion or manifest.lighting_style:
        estilo_luz = scene.iluminacion or manifest.lighting_style
        partes.append(f"Iluminación: {estilo_luz.strip()}")
    if scene.color or manifest.color_palette:
        palette = scene.color or manifest.color_palette
        partes.append(f"Color / mood: {palette.strip()}")
    if scene.camara or manifest.camera_lens:
        camara = scene.camara or manifest.camera_lens
        partes.append(f"Cámara y objetivo: {camara.strip()}")
    if scene.composicion or manifest.composition:
        comp = scene.composicion or manifest.composition
        partes.append(f"Composición: {comp.strip()}")

    estilo_visual: List[str] = []
    if scene.estilo_visual:
        estilo_visual.append(scene.estilo_visual.strip())
    if manifest.style:
        estilo_visual.append(manifest.style.strip())
    if manifest.visual_inspirations:
        estilo_visual.extend([ref.strip() for ref in manifest.visual_inspirations if ref.strip()])
    if estilo_visual:
        partes.append("Estilo visual: " + ", ".join(estilo_visual))

    partes.append(
        "Estilo fotográfico cinematográfico, ultra detallado, calidad película, textura realista"
    )

    return ", ".join(part for part in partes if part)


def build_shot_prompts_from_scene(manifest: ProjectManifest, scene: SceneV3) -> List[ShotV3]:
    """Genera prompts de imagen para cada plano de una escena."""
    shot_results: List[ShotV3] = []

    for shot in scene.shots:
        base_prompt = build_base_image_prompt(manifest, scene, shot.tipo_plano)
        prompt = f"{shot.descripcion.strip()}. {base_prompt}"

        negativo: List[str] = []
        if manifest.negative_prompts:
            negativo.extend([item.strip() for item in manifest.negative_prompts if item.strip()])
        negativo_text = ", ".join(negativo) if negativo else None

        shot_results.append(
            ShotV3(
                index=shot.index,
                tipo_plano=shot.tipo_plano,
                descripcion=shot.descripcion,
                prompt=prompt,
                negative_prompt=negativo_text,
            )
        )

    return shot_results

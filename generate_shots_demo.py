"""Demostración minimalista de generación de prompts para planos."""
from dataclasses import dataclass
from typing import List


@dataclass
class ProjectManifest:
    """Metadatos básicos del proyecto utilizados para contextualizar los prompts."""

    estilo_visual: str
    relacion_aspecto: str


@dataclass
class Shot:
    """Plano individual dentro de una escena."""

    descripcion: str
    personajes: List[str]


@dataclass
class SceneV3:
    """Escena compuesta por varios planos."""

    titulo: str
    shots: List[Shot]


def generate_shots_for_scene(manifest: ProjectManifest, scene: SceneV3) -> List[str]:
    """Genera prompts de ejemplo para cada plano de una escena.

    Args:
        manifest: Información global del proyecto (estilo, relación de aspecto, etc.).
        scene: Escena con los planos a describir.

    Returns:
        Una lista de prompts en texto listos para usar en un modelo generativo.
    """

    prompts = []
    for index, shot in enumerate(scene.shots, start=1):
        descripcion_personajes = ", ".join(shot.personajes) if shot.personajes else "Sin personajes"
        prompt = (
            f"[{scene.titulo}] Plano {index}: {shot.descripcion}. "
            f"Personajes: {descripcion_personajes}. "
            f"Estilo: {manifest.estilo_visual}. Relación de aspecto: {manifest.relacion_aspecto}."
        )
        prompts.append(prompt)
    return prompts


if __name__ == "__main__":
    # Crea un ProjectManifest y una SceneV3 mínimos de ejemplo (hardcodeados)
    # Llama a generate_shots_for_scene y muestra por pantalla los prompts generados.
    manifest = ProjectManifest(
        estilo_visual="Estilo cómic retro con colores saturados",
        relacion_aspecto="16:9",
    )

    escena = SceneV3(
        titulo="Encuentro en la azotea",
        shots=[
            Shot(
                descripcion="Toma panorámica de la ciudad al atardecer",
                personajes=[],
            ),
            Shot(
                descripcion="Los protagonistas conversan mientras el viento mueve sus abrigos",
                personajes=["Alicia", "Bruno"],
            ),
        ],
    )

    prompts_generados = generate_shots_for_scene(manifest, escena)
    for prompt in prompts_generados:
        print(prompt)

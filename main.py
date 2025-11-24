from dataclasses import dataclass
from typing import List


@dataclass
class ProjectManifest:
    """Minimal project metadata required to craft prompts."""

    title: str
    genre: str
    visual_style: str


@dataclass
class Shot:
    """Simple description of a shot within a scene."""

    description: str
    duration_seconds: int


@dataclass
class SceneV3:
    """Minimal representation of a scene containing multiple shots."""

    scene_id: str
    summary: str
    shots: List[Shot]


def generate_shots_for_scene(manifest: ProjectManifest, scene: SceneV3) -> List[str]:
    """Create text prompts for each shot in a scene.

    The prompts embed project context so the generated output is self contained.
    """

    prompts: List[str] = []
    for idx, shot in enumerate(scene.shots, start=1):
        prompt = (
            f"Proyecto: {manifest.title} ({manifest.genre}). "
            f"Estilo visual: {manifest.visual_style}. "
            f"Escena {scene.scene_id}: {scene.summary}. "
            f"Plano {idx}: {shot.description} (\u2248{shot.duration_seconds}s)."
        )
        prompts.append(prompt)

    return prompts


if __name__ == "__main__":
    # Crea un ProjectManifest y una SceneV3 mínimos de ejemplo (hardcodeados)
    manifest = ProjectManifest(
        title="La Ciudad Dormida",
        genre="Ciencia ficción",
        visual_style="Ilustración digital nocturna con neón",
    )

    scene = SceneV3(
        scene_id="01",
        summary="La protagonista llega a la ciudad y observa las luces desde un mirador",
        shots=[
            Shot(
                description="Plano general de la ciudad iluminada bajo un cielo estrellado",
                duration_seconds=6,
            ),
            Shot(
                description="Primer plano de la protagonista sonriendo mientras el viento mueve su abrigo",
                duration_seconds=4,
            ),
            Shot(
                description="Paneo lento hacia las calles llenas de neón y tráfico aéreo",
                duration_seconds=5,
            ),
        ],
    )

    # Llama a generate_shots_for_scene y muestra por pantalla los prompts generados.
    for prompt in generate_shots_for_scene(manifest, scene):
        print(prompt)

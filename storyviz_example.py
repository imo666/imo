from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Shot:
    description: str
    image_prompt: str


@dataclass
class Scene:
    title: str
    synopsis: str
    shots: List[Shot] = field(default_factory=list)


@dataclass
class StoryvizProject:
    title: str
    logline: str
    scenes: List[Scene]


class LocalLLMClient:
    """Stub client that would normally talk to a local LLM service."""

    def __init__(self, model_name: str = "local-llm") -> None:
        self.model_name = model_name

    def generate_storyviz(self) -> StoryvizProject:
        """Return an example StoryViz project without real LLM calls."""
        return StoryvizProject(
            title="El Faro del Horizonte",
            logline=(
                "Una joven cartógrafa descubre un faro que solo aparece al amanecer, "
                "y debe decidir si seguir su luz hacia lo desconocido."
            ),
            scenes=[
                Scene(
                    title="Niebla en la costa",
                    synopsis="La bruma oculta el pueblo mientras el faro late en la distancia.",
                    shots=[
                        Shot(
                            description="La cartógrafa observa el faro entre la niebla",
                            image_prompt=(
                                "a lone cartographer on a rocky coast at dawn, "
                                "mist swirling around a distant lighthouse"
                            ),
                        ),
                        Shot(
                            description="Las olas golpean mientras ella dibuja",
                            image_prompt=(
                                "waves crashing against dark rocks, "
                                "young woman sketching by lantern light"
                            ),
                        ),
                    ],
                ),
                Scene(
                    title="La decisión",
                    synopsis="Al salir el sol, el faro revela un sendero que nadie había visto.",
                    shots=[
                        Shot(
                            description="El faro alineado con el sol naciente",
                            image_prompt=(
                                "sunrise aligning with an old lighthouse, "
                                "golden rays cutting through sea mist"
                            ),
                        ),
                        Shot(
                            description="La cartógrafa inicia el viaje",
                            image_prompt=(
                                "young explorer stepping onto a hidden stone path, "
                                "morning light, determined expression"
                            ),
                        ),
                    ],
                ),
            ],
        )


def build_storyviz_project(client: LocalLLMClient) -> StoryvizProject:
    """Wrapper to obtain a StoryViz project using the given client."""
    return client.generate_storyviz()


if __name__ == "__main__":
    # Script de ejemplo corto: simula la creación de un proyecto StoryViz.
    # Si se dispone de un cliente real, sustituir LocalLLMClient por la integración deseada.
    client = LocalLLMClient(model_name="storyviz-local")
    project = build_storyviz_project(client)

    print("Ejemplo de proyecto StoryViz listo.")
    print(f"Título: {project.title}")
    print(f"Logline: {project.logline}")
    print(f"Número de escenas: {len(project.scenes)}")
    print(
        f"Número de planos: {sum(len(scene.shots) for scene in project.scenes)}"
    )

    print("Prompts de imagen de ejemplo:")
    sample_shots = [shot for scene in project.scenes for shot in scene.shots][:2]
    for idx, shot in enumerate(sample_shots, start=1):
        print(f"  {idx}. {shot.image_prompt}")

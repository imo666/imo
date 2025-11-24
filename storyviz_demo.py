from dataclasses import dataclass, field
from typing import List


@dataclass
class Shot:
    prompt: str


@dataclass
class Scene:
    shots: List[Shot] = field(default_factory=list)


@dataclass
class StoryvizProject:
    title: str
    logline: str
    scenes: List[Scene] = field(default_factory=list)


# TODO: Replace with a real LocalLLMClient implementation when available.
class LocalLLMClient:
    def __init__(self, model_name: str = "gpt-local"):
        self.model_name = model_name


# Temporary story builder with placeholder data.
def build_storyviz_project(client: LocalLLMClient | None = None) -> StoryvizProject:
    del client  # Placeholder to acknowledge the argument until a real client is wired in.

    scenes = [
        Scene(shots=[
            Shot(prompt="Wide dusk shot of a solitary lighthouse against stormy seas"),
            Shot(prompt="Close-up of lantern light flickering as waves crash")
        ]),
        Scene(shots=[
            Shot(prompt="Interior: navigator studies a faded map by candlelight")
        ])
    ]

    return StoryvizProject(
        title="El Faro de la Tormenta",
        logline=(
            "Un farero veterano se enfrenta a la noche más oscura mientras ayuda a un barco perdido a llegar a puerto"
        ),
        scenes=scenes,
    )


if __name__ == "__main__":
    # Script de ejemplo corto (3-4 frases)
    # Crear un LocalLLMClient (o dejar un TODO si no se quiere llamar realmente).
    # Llamar a build_storyviz_project y mostrar:
    # - título
    # - logline
    # - nº de escenas
    # - nº de planos
    # - ejemplo de 1-2 prompts de imagen
    client = LocalLLMClient()
    project = build_storyviz_project(client)

    num_scenes = len(project.scenes)
    num_shots = sum(len(scene.shots) for scene in project.scenes)
    sample_prompts = [shot.prompt for scene in project.scenes for shot in scene.shots][:2]

    print(f"Título: {project.title}")
    print(f"Logline: {project.logline}")
    print(f"Número de escenas: {num_scenes}")
    print(f"Número de planos: {num_shots}")

    for idx, prompt in enumerate(sample_prompts, start=1):
        print(f"Prompt {idx}: {prompt}")

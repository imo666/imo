"""Script de demostración para la pipeline StoryViz."""

from backend.llm_client import LocalLLMClient
from backend.storyviz_pipeline import build_storyviz_project


def main() -> None:
    script = (
        "Una joven exploradora desciende a una ciudad sumergida para recuperar un artefacto perdido. "
        "Mientras el oxígeno se agota, debe decidir entre salvar su propia vida o sacrificarlo todo por la ciudad."
    )

    # Instancia del LLM local (por ahora asumimos un modelo tipo 'llama3' en Ollama)
    llm = LocalLLMClient(model="llama3")

    project = build_storyviz_project(
        script=script,
        llm=llm,
        duracion_objetivo=90,
        plataformas_destino=["tiktok", "youtube_short"],
    )

    print("=== MANIFEST ===")
    print("Título:", project.project.manifest.titulo)
    print("Logline:", project.project.manifest.logline)
    print("Escenas:", len(project.project.scenes))

    print("\n=== ESCENAS ===")
    for scene in project.project.scenes:
        print(
            f"- Escena {scene.orden} ({scene.scene_id}): "
            f"{scene.duracion_estimada_segundos}s, "
            f"peso={scene.peso_narrativo}, "
            f"plano={scene.tipo_plano_dominante}, "
            f"quality={scene.quality_budget}, "
            f"preview={scene.video_preview_model}, final={scene.video_final_model}"
        )

    print("\n=== SHOTS (primeros 5) ===")
    for shot in project.shots[:5]:
        print(
            f"* {shot.shot_id} | orden={shot.orden} | tipo={shot.tipo_plano} | mov={shot.movimiento_camara}"
        )
        print("  Prompt:", shot.prompt_base_imagen[:180], "...")
        print()


if __name__ == "__main__":
    main()

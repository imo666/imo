from backend.llm_client import LocalLLMClient, generate_project_from_script


def main() -> None:
    script = (
        "Una joven descubre una nota escondida en un libro de la biblioteca. "
        "La pista la lleva a investigar un misterio que conecta a su familia con la ciudad. "
        "Con la ayuda de un amigo, decide seguir las señales pese a sus dudas."
    )

    llm = LocalLLMClient(model="llama3")
    project = generate_project_from_script(
        script=script,
        llm=llm,
        duracion_objetivo=90,
        plataformas_destino=["tiktok", "youtube_short"],
    )

    print(f"Título: {project.titulo}")
    print(f"Logline: {project.logline}")
    print(f"Número de escenas: {len(project.escenas)}")
    for escena in project.escenas:
        print(
            f"Escena {escena.orden}: {escena.duracion_estimada_segundos}s, "
            f"plano {escena.tipo_plano_dominante}, peso {escena.peso_narrativo}"
        )


if __name__ == "__main__":
    main()


"""Utilities for building prompts for story projection workflows."""

from textwrap import dedent


def build_prompt_for_story_to_project(
    script: str,
    duracion_objetivo: int,
    plataformas_destino: list[str],
) -> str:
    """
    Construye un prompt descriptivo para transformar un guion narrativo en un
    plan de proyecto audiovisual.

    Args:
        script: Texto del guion o narrativa de entrada.
        duracion_objetivo: Duración objetivo total del proyecto en segundos.
        plataformas_destino: Lista de plataformas donde se publicará el
            contenido.

    Returns:
        Prompt en español listo para ser usado por un modelo de lenguaje que
        genere la descomposición del guion en escenas y tareas.
    """

    plataformas_listado = "\n".join(
        f"- {plataforma}" for plataforma in plataformas_destino
    ) if plataformas_destino else "- Sin plataformas específicas"

    return dedent(
        f"""
        Actúa como un productor audiovisual. Recibirás un guion y debes devolver
        un plan accionable en español que incluya escenas, tiempos estimados y
        entregables para las plataformas indicadas.

        Instrucciones:
        - Mantén la coherencia narrativa del guion original.
        - Ajusta el ritmo para que la duración total se acerque a
          {duracion_objetivo} segundos.
        - Propón formatos o cortes específicos según cada plataforma destino.
        - Usa viñetas claras y tiempos estimados en segundos para cada escena.

        Datos de entrada:
        Guion base:
        """{script.strip()}"""

        Plataformas objetivo:
        {plataformas_listado}

        Responde únicamente con el plan estructurado, sin explicaciones
        adicionales.
        """
    ).strip()

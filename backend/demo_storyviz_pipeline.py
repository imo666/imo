"""Command-line demo for the story visualization pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path

from storyviz_pipeline import StoryVizPipeline, format_project, format_shots


DEFAULT_STORY = """En un pequeño pueblo costero, Ana repara su viejo faro. \
Cada noche lo enciende esperando que su hermano perdido vuelva del mar. \
Un barco misterioso aparece en el horizonte. \
Ana duda, pero decide enviar señales de luz.

El barco responde con destellos. \
La niebla se abre y revela a su hermano, más viejo pero vivo. \
Se abrazan en el muelle mientras el faro ilumina el amanecer."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo de StoryViz pipeline")
    parser.add_argument(
        "story",
        nargs="?",
        help="Ruta a un archivo de texto con la historia. Si no se provee, se usa un ejemplo integrado.",
    )
    parser.add_argument("--titulo", default="Reencuentro en la niebla", help="Título del proyecto narrativo")
    return parser.parse_args()


def load_story(path: str | None) -> str:
    if not path:
        return DEFAULT_STORY
    return Path(path).read_text(encoding="utf-8")


def main() -> None:
    args = parse_args()
    story_text = load_story(args.story)

    pipeline = StoryVizPipeline()
    project, shots = pipeline.run(story_text, title=args.titulo)

    print("=== MANIFIESTO + ESCENAS ===")
    print(format_project(project))

    print("\n=== SHOTS V3 ===")
    print(format_shots(shots))


if __name__ == "__main__":
    main()

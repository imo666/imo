"""Model definitions for StoryViz backend parsing.

The models are intentionally lightweight and rely solely on the Python
standard library to ease portability inside the StoryViz toolkit.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Chapter:
    """Represents a single chapter or scene block for StoryViz."""

    title: str
    summary: Optional[str] = None
    scenes: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chapter":
        if not isinstance(data, dict):
            raise ValueError("Chapter data must be a dictionary.")
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Chapter title must be a non-empty string.")
        summary = data.get("summary")
        if summary is not None and not isinstance(summary, str):
            raise ValueError("Chapter summary must be a string when provided.")
        scenes_raw = data.get("scenes", [])
        if not isinstance(scenes_raw, list) or not all(isinstance(scene, str) for scene in scenes_raw):
            raise ValueError("Chapter scenes must be a list of strings.")
        return cls(title=title.strip(), summary=summary, scenes=[scene.strip() for scene in scenes_raw])


@dataclass
class ProjectFull:
    """Full project payload returned by the LLM for StoryViz."""

    name: str
    description: Optional[str] = None
    audience: Optional[str] = None
    chapters: List[Chapter] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectFull":
        if not isinstance(data, dict):
            raise ValueError("Project data must be a dictionary.")
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Project name must be a non-empty string.")
        description = data.get("description")
        if description is not None and not isinstance(description, str):
            raise ValueError("Project description must be a string when provided.")
        audience = data.get("audience")
        if audience is not None and not isinstance(audience, str):
            raise ValueError("Project audience must be a string when provided.")
        chapters_raw = data.get("chapters", [])
        if not isinstance(chapters_raw, list):
            raise ValueError("Project chapters must be a list of dictionaries.")
        chapters = [Chapter.from_dict(chapter) for chapter in chapters_raw]
        return cls(
            name=name.strip(),
            description=description,
            audience=audience,
            chapters=chapters,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "audience": self.audience,
            "chapters": [
                {
                    "title": chapter.title,
                    "summary": chapter.summary,
                    "scenes": list(chapter.scenes),
                }
                for chapter in self.chapters
            ],
        }

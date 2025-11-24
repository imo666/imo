from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class InputStorySource(BaseModel):
    """Represents an external source of story content for a project."""

    source_type: str = Field(..., description="Short identifier for the source type, e.g. 's3' or 'local'.")
    location: str = Field(..., description="URI or path where the story content can be retrieved.")


class ProjectMetadata(BaseModel):
    """Lightweight metadata describing the project owner and purpose."""

    owner: Optional[str] = Field(None, description="Owner or team responsible for the project.")
    description: Optional[str] = Field(None, description="Human-friendly description of the project.")


class ProjectManifest(BaseModel):
    """High-level manifest describing a story generation project."""

    project_id: str = Field(..., description="Unique identifier for the project.")
    name: str = Field(..., description="Display name for the project.")
    sources: List[InputStorySource] = Field(default_factory=list, description="Story data sources.")
    metadata: Optional[ProjectMetadata] = Field(None, description="Optional metadata about the project.")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the project was created.")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the project was last updated.")

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "demo-project",
                "name": "Proyecto de ejemplo",
                "sources": [
                    {"source_type": "local", "location": "./stories"},
                ],
                "metadata": {
                    "owner": "equipo-narrativa",
                    "description": "Proyecto de demostración con historias locales.",
                },
            }
        }

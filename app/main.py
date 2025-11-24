from __future__ import annotations

from fastapi import FastAPI

from app.routers import projects

app = FastAPI(title="Projects API", version="0.1.0")

app.include_router(projects.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok"}

from fastapi import FastAPI

app = FastAPI(title="IMO API")


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a simple greeting to confirm the app is running."""
    return {"message": "Hello from FastAPI"}


@app.get("/health")
def read_health() -> dict[str, str]:
    """Health endpoint useful for readiness and liveness probes."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

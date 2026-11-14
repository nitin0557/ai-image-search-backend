from fastapi import FastAPI

from app.api.v1.router import router
from app.db.database import init_db

app = FastAPI(title="AI Image Search Backend", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root():
    return {"service": "ai-image-search", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1")

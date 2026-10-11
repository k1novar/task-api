from fastapi import FastAPI

from app.config import get_settings
from app.routers import tasks

settings = get_settings()

app = FastAPI(title="Task API", version="0.1.0", debug=settings.debug)

app.include_router(tasks.router)

@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
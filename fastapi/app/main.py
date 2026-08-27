from fastapi import FastAPI

from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.chat import router as chat_router


app = FastAPI(
    title="HealthLens AI Service",
    version="1.0.0",
)


app.include_router(ingestion_router)
app.include_router(chat_router)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
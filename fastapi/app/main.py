from fastapi import FastAPI

from app.api.routes.ingestion import router as ingestion_router


app = FastAPI(
    title="HealthLens AI Service",
    version="1.0.0",
)


app.include_router(ingestion_router)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
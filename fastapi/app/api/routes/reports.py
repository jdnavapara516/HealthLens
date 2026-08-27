from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_database
from app.vectorstore.models import DocumentChunk


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/chunks")
def get_document_chunks(
    db: Session = Depends(get_database),
):
    statement = select(DocumentChunk)

    chunks = db.scalars(statement).all()

    return {
        "count": len(chunks),
        "chunks": chunks,
    }
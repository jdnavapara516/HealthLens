from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pypdf.errors import PdfStreamError
from sqlalchemy.orm import Session

from app.embeddings.service import EmbeddingService
from app.ingestion.chunker import DocumentChunker
from app.ingestion.service import extract_text_from_pdf
from app.vectorstore.database import SessionLocal
from app.vectorstore.service import VectorStoreService


router = APIRouter(
    prefix="/api/v1/ingestion",
    tags=["Ingestion"],
)


class ProcessReportRequest(BaseModel):
    report_id: int
    user_id: int
    file_path: str


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/process")
def process_report(
    request: ProcessReportRequest,
    db: Session = Depends(get_db),
):
    try:
        # 1. Extract text from PDF
        try:
            pages = extract_text_from_pdf(request.file_path)
        except (FileNotFoundError, OSError, ValueError, PdfStreamError) as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to read report PDF: {exc}",
            ) from exc

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF.",
            )

        # 2. Split text into chunks
        chunker = DocumentChunker()
        chunks = chunker.split_pages(pages)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No chunks were created from the PDF.",
            )

        # 3. Generate embeddings
        embedding_service = EmbeddingService()

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = embedding_service.embed_documents(texts)

        if len(embeddings) != len(chunks) or any(
            len(embedding) != 768 for embedding in embeddings
        ):
            raise ValueError(
                "Embedding service returned an unexpected number or dimension "
                "of embeddings. Expected one 768-dimensional vector per chunk."
            )

        # 4. Store chunks + embeddings
        vector_store = VectorStoreService(db)

        documents = vector_store.add_chunks(
            user_id=request.user_id,
            report_id=request.report_id,
            chunks=chunks,
            embeddings=embeddings,
        )

        return {
            "status": "completed",
            "report_id": request.report_id,
            "chunks_processed": len(documents),
            "embedding_dimension": len(embeddings[0]),
        }

    except HTTPException:
        raise

    except RuntimeError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Report processing failed: {str(e)}",
        )

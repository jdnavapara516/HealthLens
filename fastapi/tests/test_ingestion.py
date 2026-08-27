from app.embeddings.service import EmbeddingService
from app.ingestion.chunker import DocumentChunker
from app.ingestion.service import extract_text_from_pdf
from app.vectorstore.database import SessionLocal
from app.vectorstore.service import VectorStoreService


PDF_PATH = "tests/sample_report.pdf"


def main():
    # 1. Extract text
    pages = extract_text_from_pdf(PDF_PATH)

    print("Pages:", len(pages))

    # 2. Split text into chunks
    chunker = DocumentChunker()

    chunks = chunker.split_pages(pages)

    print("Chunks:", len(chunks))

    # 3. Generate embeddings
    embedding_service = EmbeddingService()

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = embedding_service.embed_documents(texts)

    print("Embeddings:", len(embeddings))
    print("Embedding dimension:", len(embeddings[0]))

    # 4. Store everything in PostgreSQL
    db = SessionLocal()

    try:
        vector_store = VectorStoreService(db)

        documents = vector_store.add_chunks(
            user_id=1,
            report_id=1,
            chunks=chunks,
            embeddings=embeddings,
        )

        print("Stored chunks:", len(documents))

    finally:
        db.close()


if __name__ == "__main__":
    main()
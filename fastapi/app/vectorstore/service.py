from sqlalchemy import select
from sqlalchemy.orm import Session

from app.vectorstore.models import DocumentChunk


class VectorStoreService:

    def __init__(self, db: Session):
        self.db = db

    def add_chunks(
        self,
        user_id: int,
        report_id: int,
        chunks: list[dict],
        embeddings: list[list[float]],
    ) -> list[DocumentChunk]:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must be equal"
            )

        documents = []

        for chunk, embedding in zip(chunks, embeddings):
            document = DocumentChunk(
                user_id=user_id,
                report_id=report_id,
                content=chunk["content"],
                page=chunk.get("page"),
                section=chunk.get("section"),
                embedding=embedding,
            )

            self.db.add(document)
            documents.append(document)

        self.db.commit()

        for document in documents:
            self.db.refresh(document)

        return documents

    def get_by_report(
        self,
        report_id: int,
    ) -> list[DocumentChunk]:

        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.report_id == report_id)
            .order_by(DocumentChunk.page)
        )

        return list(self.db.scalars(statement).all())
from app.embeddings.service import EmbeddingService
from app.graph.state import ChatGraphState
from app.vectorstore.service import VectorStoreService


def retrieve_context(state: ChatGraphState, *, embedding_service: EmbeddingService, vector_store: VectorStoreService) -> ChatGraphState:
    query_embedding = embedding_service.embed_query(state["message"])
    matches = vector_store.search_similar(
        user_id=state["user_id"],
        report_id=state["report_id"],
        query_embedding=query_embedding,
        limit=5,
    )
    return {"query_embedding": query_embedding, "matches": matches}
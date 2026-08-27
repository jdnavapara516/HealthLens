from langgraph.graph import END, START, StateGraph

from app.embeddings.service import EmbeddingService
from app.graph.nodes.generate import generate_answer
from app.graph.nodes.retrieve import retrieve_context
from app.graph.state import ChatGraphState
from app.llm.service import GroqReportService
from app.vectorstore.service import VectorStoreService


def build_chat_graph(db) :
    embedding_service = EmbeddingService()
    vector_store = VectorStoreService(db)
    groq_service = GroqReportService()

    graph = StateGraph(ChatGraphState)
    graph.add_node(
        "retrieve",
        lambda state: retrieve_context(
            state,
            embedding_service=embedding_service,
            vector_store=vector_store,
        ),
    )
    graph.add_node(
        "generate",
        lambda state: generate_answer(state, groq_service=groq_service),
    )
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
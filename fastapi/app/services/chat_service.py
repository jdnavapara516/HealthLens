from app.graph.workflow import build_chat_graph


class ChatService:
    def __init__(self, db):
        self.db = db
        self.graph = build_chat_graph(db)

    def answer(self, user_id: int, report_id: int, message: str, history: list[dict]):
        result = self.graph.invoke({
            "user_id": user_id,
            "report_id": report_id,
            "message": message,
            "history": history[-20:],
        })
        matches = result.get("matches", [])
        return result["answer"], [
            {"chunk_id": chunk.id, "page": chunk.page}
            for chunk, _distance in matches
        ]

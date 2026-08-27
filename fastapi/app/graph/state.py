from typing import TypedDict


class ChatGraphState(TypedDict, total=False):
    user_id: int
    report_id: int
    message: str
    history: list[dict]
    query_embedding: list[float]
    matches: list[tuple[object, float]]
    answer: str
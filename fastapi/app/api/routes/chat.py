from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.vectorstore.database import SessionLocal


router = APIRouter(prefix="/api/v1", tags=["Chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/chat', response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        answer, sources = ChatService(db).answer(
            user_id=request.user_id,
            report_id=request.report_id,
            message=request.message.strip(),
            history=[item.model_dump() for item in request.history],
        )
        return ChatResponse(answer=answer, sources=sources)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail='Unable to generate an answer right now.',
        ) from exc

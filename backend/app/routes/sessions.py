
from fastapi import APIRouter, HTTPException
from app.schemas import SessionAttentionSummaryRequest, StartSessionRequest
from app.db.conn import db_session
from app.repository import SessionRepository, TelemetryRepository
from app.routes.bootstrap import LOCAL_CLIENT_ID

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/start", status_code=201)
def start_session(payload: StartSessionRequest):
    with db_session() as db:
        session = SessionRepository.create(db, client_id=LOCAL_CLIENT_ID, session_topic=payload.session_topic)
        TelemetryRepository.create(db, session_id=session.session_id)
        return {
            "session_id": str(session.session_id),
            "topic": session.session_topic,
            "status": session.status.value,
            "created_at": session.created_at.isoformat() if session.created_at else None}

@router.post("/current", status_code=200)
def get_current_session():
    with db_session() as db:
        current = SessionRepository.get_current_active(db)
        if not current:
            raise HTTPException(status_code=404, detail="No active session found")
        
        return {"session_id": str(current.session_id), "topic": current.session_topic, "status": current.status.value}

@router.post("/attention-summary", status_code=200)
def save_attention_summary(payload: SessionAttentionSummaryRequest):
    with db_session() as db:
        current = SessionRepository.get_current_active(db)

        if not current:
            raise HTTPException(status_code=404, detail="No active session to attach summary")

        current.distracted_seconds = payload.distracted_seconds
        current.avg_attention = payload.avg_attention
        current.samples_count = payload.samples_count
        db.flush()
        TelemetryRepository.create(db, session_id=current.session_id)

        return {"message": "Attention summary saved.",
                "session_id": str(current.session_id),
                "focused_seconds": str(current.focused_seconds),
                "distracted_seconds": str(current.distracted_seconds),
                "avg_attention": str(current.avg_attention),
        }


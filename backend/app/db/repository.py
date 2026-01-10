# Repository for database operations

from typing import Any, Dict, List, Optional
from datetime import datetime, time as dt_time
from sqlalchemy.orm import Session
import uuid

from app.models import (Client, Session as SessionModel, ChatHistory, Plan, 
    PomodoroCycle, TelemetryEvent,
    SessionStatus, MessageRole, PomodoroPhase)

class ClientRepository:
    """Database operations for Client"""
    
    @staticmethod
    def get_by_id(db: Session, client_id: uuid.UUID) -> Optional[Client]:
        return db.query(Client).filter(Client.client_id == client_id).first()
    
    @staticmethod
    def get_by_name(db: Session, client_name: str) -> Optional[Client]:
        return db.query(Client).filter(Client.client_name == client_name).first()
    
    @staticmethod
    def create(db: Session, client_id: Optional[uuid.UUID] = None, client_name: str = None) -> Client:
        client = Client(
            client_id=client_id or uuid.uuid4(),
            client_name=client_name
        )
        db.add(client)
        db.flush()
        return client
    
class SessionRepository:
    """Database operations for Session"""
    
    @staticmethod
    def get_by_id(db: Session, session_id: uuid.UUID) -> Optional[SessionModel]:
        return db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    
    @staticmethod
    def create(db: Session, session_topic: str, status: SessionStatus = SessionStatus.ACTIVE) -> SessionModel:
        session = SessionModel(
            session_topic=session_topic,
            status=status,
            created_at=datetime.utcnow()
        )
        db.add(session)
        db.flush()
        return session
    
    @staticmethod
    def complete(db: Session, session_id: uuid.UUID) -> SessionModel:
        session = SessionRepository.get_by_id(db, session_id)
        if not session:
            return None
        
        session.status = SessionStatus.COMPLETED
        session.completed_at = datetime.utcnow()
         # Calculate duration
        if session.created_at:
            duration_seconds = int((session.completed_at - session.created_at).total_seconds())
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            seconds = duration_seconds % 60
            session.duration = dt_time(hour=hours, minute=minutes, second=seconds)
        
        db.flush()
        return session
    
    @staticmethod
    def abort(db: Session, session_id: uuid.UUID) -> SessionModel:
        session = SessionRepository.get_by_id(db, session_id)
        if session:
            session.status = SessionStatus.ABORTED
            session.completed_at = datetime.utcnow()
            db.flush()
        return session
    
class PlanRepository:
    """Database operations for Plan"""
    
    @staticmethod
    def create(db: Session, session_id: uuid.UUID, pomodoro_pattern: str, qualitative_guide: str) -> Plan:
        plan = Plan(
            session_id=session_id,
            pomodoro_pattern=pomodoro_pattern,
            qualitative_guide=qualitative_guide,
            updated_at=datetime.utcnow()
        )
        db.add(plan)
        db.flush()
        return plan
    
    @staticmethod
    def get_by_session(db: Session, session_id: uuid.UUID) -> Optional[Plan]:
        return db.query(Plan).filter(Plan.session_id == session_id).first()

class PomodoroCycleRepository:
    """Database operations for Pomodoro Cycles"""
    
    @staticmethod
    def create(db: Session, session_id: uuid.UUID, phase: PomodoroPhase, minutes: int) -> PomodoroCycle:
        cycle = PomodoroCycle(
            session_id=session_id,
            phase=phase,
            minutes=minutes,
            started_at=datetime.utcnow()
        )
        db.add(cycle)
        db.flush()
        return cycle
    
    @staticmethod
    def get_current(db: Session, session_id: uuid.UUID) -> Optional[PomodoroCycle]:
        return db.query(PomodoroCycle).filter(
            PomodoroCycle.session_id == session_id
        ).order_by(PomodoroCycle.started_at.desc()).first()
    
    @staticmethod
    def complete_and_start_next(db: Session, cycle_id: uuid.UUID, session_id: uuid.UUID, next_phase: PomodoroPhase, next_minutes: int) -> tuple[PomodoroCycle, PomodoroCycle]:
        # Complete current
        current = db.query(PomodoroCycle).filter(PomodoroCycle.cycle_id == cycle_id).first()
        if current:
            current.completed = True
            current.ends_at = datetime.utcnow()
        
        # Start next
        next_cycle = PomodoroCycleRepository.create(db, session_id, next_phase, next_minutes)
        db.flush()
        
        return current, next_cycle

class ChatHistoryRepository:
    """Database operations for Chat History"""
    
    @staticmethod
    def create(db: Session, client_id: uuid.UUID, session_id: uuid.UUID, role: MessageRole, chat_log: str) -> ChatHistory:
        chat = ChatHistory(
            client_id=client_id,
            session_id=session_id,
            role=role,
            chat_log=chat_log
        )
        db.add(chat)
        db.flush()
        return chat
    
    @staticmethod
    def get_by_session(db: Session, session_id: uuid.UUID) -> List[ChatHistory]:
        return db.query(ChatHistory).filter(
            ChatHistory.session_id == session_id
        ).order_by(ChatHistory.chat_id).all()

class TelemetryRepository:
    """Database operations for Telemetry Events"""
    
    @staticmethod
    def create(db: Session, session_id: uuid.UUID) -> TelemetryEvent:
        telemetry = TelemetryEvent(
            session_id=session_id,
            created_at=datetime.utcnow()
        )
        db.add(telemetry)
        db.flush()
        return telemetry
    
    @staticmethod
    def count_by_session(db: Session, session_id: uuid.UUID) -> int:
        return db.query(TelemetryEvent).filter(
            TelemetryEvent.session_id == session_id
        ).count()

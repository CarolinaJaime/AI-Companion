from pydantic import BaseModel, Field
from uuid import UUID

class StartSessionRequest(BaseModel):
    session_topic: str 

class SessionAttentionSummaryRequest(BaseModel):
    session_id: UUID
    focused_seconds: int 
    distracted_seconds: int
    avg_attention: float  # average % 0..100
    samples_count: int

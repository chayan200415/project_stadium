from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    language: str = "English"

class ChatResponse(BaseModel):
    response: str

class IncidentCreate(BaseModel):
    type: str
    location: str
    description: str

class IncidentResponse(BaseModel):
    id: int
    type: str
    location: str
    status: str
    reported_at: datetime
    description: str
    ai_plan: Optional[str] = None

    class Config:
        orm_mode = True

class CrowdDataResponse(BaseModel):
    location: str
    occupancy_percent: float

class DashboardSummaryResponse(BaseModel):
    summary: str

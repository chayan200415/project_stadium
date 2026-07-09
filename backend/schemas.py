from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    language: str = Field("English", max_length=50)

class ChatResponse(BaseModel):
    response: str

class IncidentCreate(BaseModel):
    type: str = Field(..., min_length=2, max_length=100)
    location: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=1000)

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

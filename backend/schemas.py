"""
Pydantic validation schemas for StadiumGPT API.

Defines request and response models with strict input validation
including field constraints, regex patterns, and length limits.
"""

import re
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Schema for AI chat assistant requests."""

    message: str = Field(..., min_length=1, max_length=1000, description="The user's question or message.")
    language: str = Field("English", max_length=50, description="Target language for the AI response.")

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        """Strip leading/trailing whitespace from the message."""
        return v.strip()


class ChatResponse(BaseModel):
    """Schema for AI chat assistant responses."""

    response: str = Field(..., description="The AI-generated response text.")


class IncidentCreate(BaseModel):
    """Schema for creating a new incident report."""

    type: str = Field(..., min_length=2, max_length=100, description="Incident category (e.g., Medical, Security).")
    location: str = Field(..., min_length=2, max_length=100, description="Incident location within the stadium.")
    description: str = Field(..., min_length=5, max_length=1000, description="Detailed incident description.")

    @field_validator("type", "location")
    @classmethod
    def validate_alphanumeric_fields(cls, v: str) -> str:
        """Ensure type and location contain only safe characters (letters, numbers, spaces, hyphens)."""
        sanitized = v.strip()
        if not re.match(r"^[a-zA-Z0-9\s\-,.]+$", sanitized):
            raise ValueError("Field must contain only letters, numbers, spaces, hyphens, commas, and periods.")
        return sanitized

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, v: str) -> str:
        """Strip whitespace from the description."""
        return v.strip()


class IncidentResponse(BaseModel):
    """Schema for incident response data returned from the API."""

    id: int
    type: str
    location: str
    status: str
    reported_at: datetime
    description: str
    ai_plan: Optional[str] = None

    model_config = {"from_attributes": True}


class CrowdDataResponse(BaseModel):
    """Schema for crowd occupancy data for a single zone."""

    location: str = Field(..., description="The stadium zone name.")
    occupancy_percent: float = Field(..., ge=0, le=100, description="Occupancy percentage (0-100).")


class DashboardSummaryResponse(BaseModel):
    """Schema for the AI-generated match day summary."""

    summary: str = Field(..., description="AI-generated match day operations summary.")

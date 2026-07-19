"""
SQLAlchemy ORM models for StadiumGPT.

Defines the database schema for incidents and crowd sensor data
used throughout the stadium management system.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base


class Incident(Base):
    """
    Represents a reported stadium incident.

    Stores incident details including type, location, description,
    and an optional AI-generated emergency response plan.

    Attributes:
        id: Unique identifier for the incident.
        type: Category of the incident (e.g., 'Medical', 'Security').
        location: Where the incident occurred within the stadium.
        status: Current status of the incident ('active', 'resolved').
        reported_at: UTC timestamp when the incident was reported.
        description: Detailed description of the incident.
        ai_plan: AI-generated emergency response plan (optional).
    """

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default="active")
    reported_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    description = Column(String, nullable=False)
    ai_plan = Column(String, nullable=True)

    def __repr__(self) -> str:
        """Return a human-readable representation of the Incident."""
        return f"<Incident(id={self.id}, type='{self.type}', location='{self.location}', status='{self.status}')>"


class CrowdData(Base):
    """
    Represents a crowd sensor data reading for a stadium zone.

    Stores real-time occupancy data for different areas within
    the stadium to enable crowd intelligence and safety monitoring.

    Attributes:
        id: Unique identifier for the data point.
        location: The stadium zone name (e.g., 'Gate A', 'Food Court East').
        occupancy_percent: Current occupancy as a percentage (0-100).
        timestamp: UTC timestamp when the reading was taken.
    """

    __tablename__ = "crowd_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True, nullable=False)
    occupancy_percent = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        """Return a human-readable representation of the CrowdData."""
        return f"<CrowdData(id={self.id}, location='{self.location}', occupancy={self.occupancy_percent}%)>"

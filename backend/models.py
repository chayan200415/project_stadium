from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from backend.database import Base
from datetime import datetime

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    location = Column(String)
    status = Column(String, default="active")
    reported_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    ai_plan = Column(String, nullable=True)

class CrowdData(Base):
    __tablename__ = "crowd_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    occupancy_percent = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

"""
Incident management routes for StadiumGPT.

Provides endpoints for reporting stadium incidents and retrieving
incident history. Each new incident triggers AI-generated emergency
response plan creation.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.database import get_db
from backend.models import Incident
from backend.schemas import IncidentCreate, IncidentResponse
from backend.services.ai_service import get_incident_plan_prompt, generate_response

logger = logging.getLogger("stadiumgpt.routes.incident")

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/", response_model=IncidentResponse)
@limiter.limit("5/minute")
def report_incident(
    request: Request,
    incident: IncidentCreate,
    db: Session = Depends(get_db),
) -> IncidentResponse:
    """
    Report a new stadium incident and generate an AI response plan.

    Creates a new incident record in the database and uses the AI
    Incident Commander to generate a structured emergency response plan.

    Args:
        request: The incoming HTTP request (required for rate limiting).
        incident: Validated incident data (type, location, description).
        db: Database session dependency.

    Returns:
        IncidentResponse: The created incident with AI-generated response plan.

    Raises:
        HTTPException: 500 if there is a database error.
    """
    logger.info("New incident reported: type=%s, location=%s", incident.type, incident.location)

    # Generate AI Plan
    prompt = get_incident_plan_prompt(incident.type, incident.location, incident.description)
    ai_plan = generate_response(prompt)

    try:
        db_incident = Incident(
            type=incident.type,
            location=incident.location,
            description=incident.description,
            ai_plan=ai_plan,
        )
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
    except Exception as e:
        db.rollback()
        logger.error("Database error while creating incident: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to save incident. Please try again.")

    logger.info("Incident created successfully: id=%d", db_incident.id)
    response = IncidentResponse.model_validate(db_incident)
    return response


@router.get("/", response_model=List[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)) -> List[IncidentResponse]:
    """
    Retrieve all incidents ordered by most recent first.

    Args:
        db: Database session dependency.

    Returns:
        List of IncidentResponse objects.
    """
    logger.info("Retrieving all incidents")
    incidents = db.query(Incident).order_by(Incident.reported_at.desc()).all()
    return incidents

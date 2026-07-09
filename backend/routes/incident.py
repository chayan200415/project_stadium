from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Incident
from backend.schemas import IncidentCreate, IncidentResponse
from backend.services.ai_service import get_incident_plan_prompt, generate_response

router = APIRouter()

@router.post("/", response_model=IncidentResponse)
def report_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    # Generate AI Plan
    prompt = get_incident_plan_prompt(incident.type, incident.location, incident.description)
    ai_plan = generate_response(prompt)

    db_incident = Incident(
        type=incident.type,
        location=incident.location,
        description=incident.description
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    # Convert to Pydantic and attach plan (not saved to DB in this MVP to save space)
    response = IncidentResponse.from_orm(db_incident)
    response.ai_plan = ai_plan
    return response

@router.get("/", response_model=list[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).order_by(Incident.reported_at.desc()).all()
    return incidents

from fastapi import APIRouter
import random
from backend.services.ai_service import generate_response

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary():
    prompt = """
    You are the StadiumGPT Match Day Coordinator. 
    Generate a quick 3-4 sentence match day summary. 
    Mention: Crowd is energetic (85% full), Weather is clear, 
    Transport is flowing well, No major incidents. 
    Make it sound professional and actionable for stadium staff.
    """
    summary = generate_response(prompt)
    return {"summary": summary}

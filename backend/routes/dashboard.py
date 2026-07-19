"""
Dashboard routes for StadiumGPT.

Provides the AI Match Day Summary endpoint that generates
a high-level stadium operations overview for staff.
"""

import logging
from fastapi import APIRouter

from backend.services.ai_service import generate_response

logger = logging.getLogger("stadiumgpt.routes.dashboard")

router = APIRouter()


@router.get("/summary")
def get_dashboard_summary() -> dict:
    """
    Generate an AI-powered match day operations summary.

    Creates a professional summary for stadium staff covering
    crowd status, weather, transport, and incident overview.

    Returns:
        dict: Contains a 'summary' key with the AI-generated text.
    """
    prompt = """
    You are the StadiumGPT Match Day Coordinator.
    Generate a quick 3-4 sentence match day summary.
    Mention: Crowd is energetic (85% full), Weather is clear,
    Transport is flowing well, No major incidents.
    Make it sound professional and actionable for stadium staff.
    """
    logger.info("Generating dashboard summary")
    summary = generate_response(prompt)
    return {"summary": summary}

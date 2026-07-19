"""
Crowd intelligence routes for StadiumGPT.

Provides endpoints for real-time crowd occupancy data and
AI-powered crowd analysis insights with congestion alerts.
"""

import logging
import random
from typing import List

from fastapi import APIRouter

from backend.schemas import CrowdDataResponse
from backend.services.ai_service import get_crowd_insight_prompt, generate_response

logger = logging.getLogger("stadiumgpt.routes.crowd")

router = APIRouter()

# Stadium zone names for mock data generation
STADIUM_ZONES = [
    "Gate A", "Gate B", "Gate C", "Gate D",
    "Food Court East", "Food Court West",
    "VIP Lounge", "Merchandise",
]


def get_mock_crowd_data() -> List[dict]:
    """
    Generate simulated crowd occupancy data for all stadium zones.

    Returns:
        List of dicts with 'location' and 'occupancy_percent' keys.
    """
    return [
        {"location": zone, "occupancy_percent": round(random.uniform(20, 98), 1)}
        for zone in STADIUM_ZONES
    ]


@router.get("/", response_model=List[CrowdDataResponse])
def get_crowd_status() -> List[dict]:
    """
    Get current crowd occupancy data for all stadium zones.

    Returns simulated sensor data showing occupancy percentages
    for gates, food courts, VIP areas, and merchandise zones.

    Returns:
        List of CrowdDataResponse objects with zone occupancy data.
    """
    logger.info("Crowd status requested")
    return get_mock_crowd_data()


@router.get("/insight")
def get_crowd_insight() -> dict:
    """
    Get AI-generated crowd analysis insights.

    Analyzes current crowd data and generates natural-language
    recommendations, including congestion alerts for zones
    exceeding 85% capacity.

    Returns:
        dict: Contains an 'insight' key with the AI analysis text.
    """
    data = get_mock_crowd_data()
    data_str = "\n".join([f"{d['location']}: {d['occupancy_percent']}%" for d in data])
    logger.info("Generating crowd insight for %d zones", len(data))
    prompt = get_crowd_insight_prompt(data_str)
    insight = generate_response(prompt)
    return {"insight": insight}

"""
Indoor navigation routes for StadiumGPT.

Provides route planning endpoints for navigating within the stadium,
including standard routes and accessible alternatives for fans
with mobility requirements.
"""

import logging
from fastapi import APIRouter, Query

logger = logging.getLogger("stadiumgpt.routes.navigation")

router = APIRouter()


@router.get("/")
def get_navigation_info(
    start: str = Query(..., min_length=1, max_length=100, description="Starting location within the stadium."),
    end: str = Query(..., min_length=1, max_length=100, description="Destination within the stadium."),
) -> dict:
    """
    Get indoor navigation directions between two stadium locations.

    Returns step-by-step directions for both standard and accessible
    routes, along with estimated travel time.

    Args:
        start: Starting location name (e.g., 'Gate 5').
        end: Destination name (e.g., 'Section 112, Row B').

    Returns:
        dict: Navigation data including steps, estimated time,
              and an accessible route alternative.
    """
    logger.info("Navigation requested: %s -> %s", start, end)

    # Mock routing data for MVP
    return {
        "start": start,
        "end": end,
        "steps": [
            f"Head North from {start}",
            "Take the stairs to Level 2",
            "Walk 50 meters straight",
            f"You have arrived at {end}",
        ],
        "estimated_time_mins": 4,
        "accessible_route": [
            f"Head North from {start}",
            "Take Elevator A to Level 2",
            "Walk 50 meters straight",
            f"You have arrived at {end}",
        ],
    }

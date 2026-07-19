"""
Transportation hub routes for StadiumGPT.

Provides endpoints for real-time transportation status including
metro lines, bus routes, and parking availability around the stadium.
"""

import logging
from typing import List

from fastapi import APIRouter

logger = logging.getLogger("stadiumgpt.routes.transport")

router = APIRouter()

# Simulated transport data for the MVP
TRANSPORT_OPTIONS = [
    {"route": "Metro Line Red", "status": "On Time"},
    {"route": "Metro Line Blue", "status": "Delayed by 5m"},
    {"route": "Bus Route 42", "status": "Heavy Traffic"},
    {"route": "North Parking", "status": "Available (45%)"},
    {"route": "South Parking", "status": "Full (99%)"},
]


@router.get("/")
def get_transport_status() -> List[dict]:
    """
    Get current transportation status for all routes and parking.

    Returns simulated status data for metro lines, bus routes,
    and parking lots serving the stadium.

    Returns:
        List of dicts with 'route' and 'status' keys.
    """
    logger.info("Transport status requested")
    return TRANSPORT_OPTIONS

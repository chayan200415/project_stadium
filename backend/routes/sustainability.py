"""
Sustainability dashboard routes for StadiumGPT.

Provides endpoints for environmental metrics (power, water, waste,
food surplus) and AI-generated sustainability optimization insights.
"""

import logging
import random

from fastapi import APIRouter

from backend.services.ai_service import get_sustainability_insight_prompt, generate_response

logger = logging.getLogger("stadiumgpt.routes.sustainability")

router = APIRouter()


def get_sustainability_metrics() -> dict:
    """
    Generate simulated sustainability metrics for the stadium.

    Returns:
        dict: Power usage (kW), water usage (L), waste (kg),
              and surplus food portions.
    """
    return {
        "power_usage_kw": random.randint(500, 1500),
        "water_usage_l": random.randint(2000, 8000),
        "waste_generation_kg": random.randint(100, 500),
        "surplus_food_portions": random.randint(50, 300),
    }


@router.get("/")
def get_sustainability_data() -> dict:
    """
    Get current sustainability metrics for the stadium.

    Returns simulated environmental data covering power,
    water, waste generation, and food surplus.

    Returns:
        dict: Current sustainability metrics.
    """
    logger.info("Sustainability data requested")
    return get_sustainability_metrics()


@router.get("/insight")
def get_sustainability_insight() -> dict:
    """
    Get AI-generated sustainability optimization recommendations.

    Analyzes current environmental metrics and provides actionable
    recommendations to reduce power consumption, water usage,
    and waste generation.

    Returns:
        dict: Contains an 'insight' key with AI recommendations.
    """
    data = get_sustainability_metrics()
    data_str = (
        f"Power: {data['power_usage_kw']}kW\n"
        f"Water: {data['water_usage_l']}L\n"
        f"Waste: {data['waste_generation_kg']}kg\n"
        f"Surplus Food: {data['surplus_food_portions']} portions"
    )
    logger.info("Generating sustainability insight")
    prompt = get_sustainability_insight_prompt(data_str)
    insight = generate_response(prompt)
    return {"insight": insight}

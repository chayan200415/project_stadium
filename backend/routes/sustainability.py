from fastapi import APIRouter
import random
from backend.services.ai_service import get_sustainability_insight_prompt, generate_response

router = APIRouter()

def get_sustainability_metrics():
    return {
        "power_usage_kw": random.randint(500, 1500),
        "water_usage_l": random.randint(2000, 8000),
        "waste_generation_kg": random.randint(100, 500),
        "surplus_food_portions": random.randint(50, 300)
    }

@router.get("/")
def get_sustainability_data():
    return get_sustainability_metrics()

@router.get("/insight")
def get_sustainability_insight():
    data = get_sustainability_metrics()
    data_str = f"Power: {data['power_usage_kw']}kW\nWater: {data['water_usage_l']}L\nWaste: {data['waste_generation_kg']}kg\nSurplus Food: {data['surplus_food_portions']} portions"
    prompt = get_sustainability_insight_prompt(data_str)
    insight = generate_response(prompt)
    return {"insight": insight}

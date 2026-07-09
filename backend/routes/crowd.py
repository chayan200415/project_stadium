from fastapi import APIRouter
import random
from typing import List
from backend.schemas import CrowdDataResponse
from backend.services.ai_service import get_crowd_insight_prompt, generate_response

router = APIRouter()

# Mock data generator
def get_mock_crowd_data():
    gates = ["Gate A", "Gate B", "Gate C", "Gate D", "Food Court East", "Food Court West", "VIP Lounge", "Merchandise"]
    return [{"location": gate, "occupancy_percent": round(random.uniform(20, 98), 1)} for gate in gates]

@router.get("/", response_model=List[CrowdDataResponse])
def get_crowd_status():
    return get_mock_crowd_data()

@router.get("/insight")
def get_crowd_insight():
    data = get_mock_crowd_data()
    data_str = "\n".join([f"{d['location']}: {d['occupancy_percent']}%" for d in data])
    prompt = get_crowd_insight_prompt(data_str)
    insight = generate_response(prompt)
    return {"insight": insight}

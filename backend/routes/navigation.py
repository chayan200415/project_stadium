from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_navigation_info(start: str, end: str):
    # Mock routing data for MVP
    return {
        "start": start,
        "end": end,
        "steps": [
            f"Head North from {start}",
            "Take the stairs to Level 2",
            "Walk 50 meters straight",
            f"You have arrived at {end}"
        ],
        "estimated_time_mins": 4,
        "accessible_route": [
            f"Head North from {start}",
            "Take Elevator A to Level 2",
            "Walk 50 meters straight",
            f"You have arrived at {end}"
        ]
    }

from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/")
def get_transport_status():
    options = ["Metro Line Red", "Metro Line Blue", "Bus Route 42", "North Parking", "South Parking"]
    statuses = ["On Time", "Delayed by 5m", "Heavy Traffic", "Available (45%)", "Full (99%)"]
    
    return [
        {"route": options[0], "status": statuses[0]},
        {"route": options[1], "status": statuses[1]},
        {"route": options[2], "status": statuses[2]},
        {"route": options[3], "status": statuses[3]},
        {"route": options[4], "status": statuses[4]},
    ]

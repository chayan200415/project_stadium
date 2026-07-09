from fastapi import APIRouter
from backend.schemas import ChatRequest, ChatResponse
from backend.services.ai_service import get_fan_assistant_prompt, generate_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest):
    prompt = get_fan_assistant_prompt(request.message, request.language)
    ai_response = generate_response(prompt)
    return ChatResponse(response=ai_response)

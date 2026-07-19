"""
Chat route for StadiumGPT AI Fan Assistant.

Provides a conversational AI endpoint that answers fan questions
about the stadium, directions, services, and the FIFA World Cup 2026.
"""

import logging
from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.schemas import ChatRequest, ChatResponse
from backend.services.ai_service import get_fan_assistant_prompt, generate_response

logger = logging.getLogger("stadiumgpt.routes.chat")

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/", response_model=ChatResponse)
@limiter.limit("10/minute")
def chat_with_assistant(request: Request, chat_request: ChatRequest) -> ChatResponse:
    """
    Send a message to the AI Fan Assistant and receive a response.

    The assistant can answer questions about stadium navigation,
    food options, seat locations, and general FIFA World Cup info.
    Responses can be translated to the requested language.

    Args:
        request: The incoming HTTP request (required for rate limiting).
        chat_request: Validated chat message and language preference.

    Returns:
        ChatResponse: The AI-generated response.
    """
    logger.info("Chat request received (language: %s, length: %d)", chat_request.language, len(chat_request.message))
    prompt = get_fan_assistant_prompt(chat_request.message, chat_request.language)
    ai_response = generate_response(prompt)
    return ChatResponse(response=ai_response)

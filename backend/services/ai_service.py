"""
AI Service for StadiumGPT.

Provides a centralized interface to the Google Gemini API for generating
AI-powered responses across all stadium management features, including
fan assistance, incident response, crowd analysis, and sustainability insights.
"""

import os
import logging
import re

import google.generativeai as genai
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

logger = logging.getLogger("stadiumgpt.ai_service")

# Validate API key at module load time (fail fast)
_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    logger.warning(
        "GEMINI_API_KEY is not set. AI features will return fallback responses."
    )
else:
    genai.configure(api_key=_api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# Maximum allowed response length (characters)
MAX_RESPONSE_LENGTH = 5000


def _sanitize_prompt_input(text: str) -> str:
    """
    Sanitize user-provided text before including it in AI prompts.

    Strips control characters and excessive whitespace to prevent
    prompt injection and ensure clean AI inputs.

    Args:
        text: Raw user input text.

    Returns:
        Sanitized text safe for prompt inclusion.
    """
    # Remove control characters (except newlines and tabs)
    sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # Collapse multiple spaces/newlines
    sanitized = re.sub(r"\n{3,}", "\n\n", sanitized)
    sanitized = re.sub(r" {3,}", "  ", sanitized)
    return sanitized.strip()


@lru_cache(maxsize=128)
def generate_response(prompt: str) -> str:
    """
    Generate an AI response using Google Gemini.

    Uses LRU caching to avoid redundant API calls for identical prompts.
    Falls back to a user-friendly error message if the API call fails.

    Args:
        prompt: The complete prompt string to send to Gemini.

    Returns:
        The AI-generated response text, truncated to MAX_RESPONSE_LENGTH.
    """
    if not _api_key:
        logger.error("Cannot generate AI response: GEMINI_API_KEY is not configured.")
        return "AI service is not configured. Please contact the administrator."

    try:
        logger.info("Generating AI response (prompt length: %d chars)", len(prompt))
        response = model.generate_content(prompt)
        result = response.text

        # Enforce response size limit
        if len(result) > MAX_RESPONSE_LENGTH:
            logger.warning("AI response truncated from %d to %d chars", len(result), MAX_RESPONSE_LENGTH)
            result = result[:MAX_RESPONSE_LENGTH] + "..."

        return result
    except Exception as e:
        logger.error("Error generating AI response: %s", str(e))
        return "I am currently unable to process this request due to an AI service error."


# --- Prompt Templates ---

def get_fan_assistant_prompt(question: str, language: str) -> str:
    """
    Build the prompt for the AI Fan Assistant.

    Args:
        question: The fan's question about the stadium.
        language: Target language for the response translation.

    Returns:
        A formatted prompt string for the Gemini API.
    """
    safe_question = _sanitize_prompt_input(question)
    safe_language = _sanitize_prompt_input(language)

    return f"""
You are the official StadiumGPT AI Assistant for the FIFA World Cup 2026.
Your audience is a fan inside the stadium.
Provide a helpful, polite, and concise answer to the following question.
If the question is about directions, provide clear logical steps.
Translate your final response to: {safe_language}.

User Question: {safe_question}
"""


def get_incident_plan_prompt(incident_type: str, location: str, description: str) -> str:
    """
    Build the prompt for the AI Incident Commander.

    Args:
        incident_type: Category of incident (e.g., 'Medical', 'Security').
        location: Where in the stadium the incident occurred.
        description: Detailed description of the incident.

    Returns:
        A formatted prompt string for generating an emergency response plan.
    """
    safe_type = _sanitize_prompt_input(incident_type)
    safe_location = _sanitize_prompt_input(location)
    safe_description = _sanitize_prompt_input(description)

    return f"""
You are the AI Incident Commander for StadiumGPT.
An incident has just been reported.
Type: {safe_type}
Location: {safe_location}
Description: {safe_description}

Generate a structured emergency response plan for the staff.
Include:
1. Immediate Actions
2. Nearest medical/security team deployment
3. Crowd diversion recommendations
4. Emergency checklist
"""


def get_crowd_insight_prompt(crowd_data: str) -> str:
    """
    Build the prompt for AI Crowd Intelligence analysis.

    Args:
        crowd_data: Formatted string of zone occupancy data.

    Returns:
        A formatted prompt string for generating crowd insights.
    """
    safe_data = _sanitize_prompt_input(crowd_data)

    return f"""
You are the StadiumGPT Crowd Intelligence System.
Analyze the following real-time crowd sensor data:
{safe_data}

Generate a brief, natural-language insight (2-3 sentences max) about the current situation. Include actionable recommendations for stadium managers if any area is over 85% capacity.
"""


def get_sustainability_insight_prompt(sustainability_data: str) -> str:
    """
    Build the prompt for AI Sustainability analysis.

    Args:
        sustainability_data: Formatted string of sustainability metrics.

    Returns:
        A formatted prompt string for generating sustainability recommendations.
    """
    safe_data = _sanitize_prompt_input(sustainability_data)

    return f"""
You are the StadiumGPT Sustainability AI.
Analyze the following metrics:
{safe_data}

Provide 2-3 actionable recommendations to improve sustainability and reduce waste/power consumption right now.
"""

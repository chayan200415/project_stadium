import os
import google.generativeai as genai
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')

@lru_cache(maxsize=128)
def generate_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "I am currently unable to process this request due to an AI service error."

# --- Prompts ---

def get_fan_assistant_prompt(question: str, language: str) -> str:
    return f"""
You are the official StadiumGPT AI Assistant for the FIFA World Cup 2026.
Your audience is a fan inside the stadium.
Provide a helpful, polite, and concise answer to the following question.
If the question is about directions, provide clear logical steps.
Translate your final response to: {language}.

User Question: {question}
"""

def get_incident_plan_prompt(incident_type: str, location: str, description: str) -> str:
    return f"""
You are the AI Incident Commander for StadiumGPT.
An incident has just been reported.
Type: {incident_type}
Location: {location}
Description: {description}

Generate a structured emergency response plan for the staff.
Include:
1. Immediate Actions
2. Nearest medical/security team deployment
3. Crowd diversion recommendations
4. Emergency checklist
"""

def get_crowd_insight_prompt(crowd_data: str) -> str:
    return f"""
You are the StadiumGPT Crowd Intelligence System.
Analyze the following real-time crowd sensor data:
{crowd_data}

Generate a brief, natural-language insight (2-3 sentences max) about the current situation. Include actionable recommendations for stadium managers if any area is over 85% capacity.
"""

def get_sustainability_insight_prompt(sustainability_data: str) -> str:
    return f"""
You are the StadiumGPT Sustainability AI.
Analyze the following metrics:
{sustainability_data}

Provide 2-3 actionable recommendations to improve sustainability and reduce waste/power consumption right now.
"""

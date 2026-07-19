"""
Central API router for StadiumGPT.

Aggregates all feature routers into a single API router with
organized prefixes and OpenAPI tags for documentation.
"""

from fastapi import APIRouter

from backend.routes import chat, crowd, incident, transport, sustainability, navigation, dashboard

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(crowd.router, prefix="/crowd", tags=["crowd"])
api_router.include_router(incident.router, prefix="/incident", tags=["incident"])
api_router.include_router(transport.router, prefix="/transport", tags=["transport"])
api_router.include_router(sustainability.router, prefix="/sustainability", tags=["sustainability"])
api_router.include_router(navigation.router, prefix="/navigation", tags=["navigation"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

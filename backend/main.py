"""
StadiumGPT API - FastAPI Application Entry Point.

Configures the FastAPI application with security middleware,
CORS settings, rate limiting, and API route registration.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from backend.database import engine, Base
from backend.routes.api import api_router

load_dotenv()

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("stadiumgpt")

# Rate limiter instance (shared across routes)
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler: creates DB tables on startup."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
    yield
    logger.info("Application shutting down.")


app = FastAPI(
    title="StadiumGPT API",
    description="Generative AI-enabled smart stadium operations API for FIFA World Cup 2026.",
    version="1.0.0",
    lifespan=lifespan,
)

# Attach rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS with explicit methods and headers
origins = [
    "http://localhost:5173",
    "https://project-stadium-b27wz072v-chayan2004.vercel.app",
    "https://project-stadium.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Trusted Host middleware to prevent host header attacks
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "testserver",
        "project-stadium.onrender.com",
        "*.vercel.app",
    ],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add comprehensive security headers to every HTTP response.

    Includes protections against clickjacking, MIME sniffing,
    XSS attacks, and enforces HTTPS transport security.
    """
    response: Response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self' https://project-stadium.onrender.com"
    )
    return response


app.include_router(api_router, prefix="/api")


@app.get("/", tags=["health"])
def read_root() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: A welcome message confirming the API is running.
    """
    return {"message": "Welcome to StadiumGPT API"}

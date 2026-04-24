"""
Main Application Entry Point (Tony)
=====================================
FastAPI application factory with middleware, events, and route registration.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.database import create_tables, engine
from app.api.router import api_router
from loguru import logger
import sys

# Configure Loguru
logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level=settings.LOG_LEVEL)
logger.add(settings.LOG_FILE, rotation="10 MB", retention="10 days", level=settings.LOG_LEVEL, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events - startup and shutdown."""
    # Startup: Create database tables
    await create_tables()
    logger.info(f"[*] {settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    logger.info(f"[*] Environment: {settings.APP_ENV}")
    logger.info(f"[*] Docs: http://{settings.HOST}:{settings.PORT}/docs")

    yield
    # Shutdown: Cleanup
    await engine.dispose()
    logger.info(f"[*] {settings.APP_NAME} shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "🛒 A full-featured E-Commerce REST API built with FastAPI. "
        "Supports JWT authentication, role-based access control, "
        "user management, and more."
    ),
    docs_url=None, # Disabled default Swagger UI in favor of Scalar
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ========================
# Middleware
# ========================

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.middleware.logging_middleware import LoggingMiddleware
app.add_middleware(LoggingMiddleware)



# ========================
# Exception Handlers
# ========================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with clean messages."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "detail": "Validation error",
            "errors": errors,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global fallback exception handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "detail": "An unexpected error occurred. Please try again later.",
        },
    )


# ========================
# Include Routers
# ========================

app.include_router(api_router)


# ========================
# Root & Health Endpoints
# ========================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "E-Commerce REST API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/docs", include_in_schema=False)
async def scalar_html():
    """Scalar documentation page."""
    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>API Docs</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <script id="api-reference" data-url="/openapi.json"></script>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """
    return HTMLResponse(html)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

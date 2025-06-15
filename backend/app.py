import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import routers
from api.routes import chat, search
from core.config.settings import AppSettings
from core.logging.logger import logger

# Create FastAPI app
app = FastAPI(title=AppSettings.PROJECT_NAME, openapi_url=f"{AppSettings.API_V1_STR}/openapi.json")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=AppSettings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(chat.router, prefix=AppSettings.API_V1_STR)
app.include_router(search.router, prefix=AppSettings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting up application...")
    # Add any startup initialization here


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down application...")
    # Add any cleanup code here


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

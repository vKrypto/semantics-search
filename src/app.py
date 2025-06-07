import os

# Add the src directory to Python path for imports
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.routers.search import router as search_router

app = FastAPI(title="Semantic Search API")

# setup cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve static files from static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(search_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates

from application.services.search_service import SearchService
from core.config.settings import AppSettings
from core.logging.logger import logger
from domain.models.search import SearchRequest, SearchResponse, SearchType

router = APIRouter(
    prefix=f"{AppSettings.VERSION_STR}/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}},
)

# Mount templates
templates_path = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


@lru_cache
def _get_search_service() -> SearchService:
    """Dependency to get search service instance."""
    return SearchService(SearchType.COSINE)


@router.get("/")
async def get_search_interface(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@router.post("/", response_model=SearchResponse)
async def search(_: Request, q: str = Query(None, alias="q")) -> SearchResponse:
    search_service: SearchService = _get_search_service()
    if q is not None:
        search_request = SearchRequest(query=q)
    else:
        raise ValueError("Either request body or query parameter 'q' must be provided")
    logger.info(f"Received search request: {q}")
    return await search_service.search(search_request)

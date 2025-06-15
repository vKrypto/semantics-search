from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates

from application.services.search_service import SearchService
from core.logging.logger import logger
from domain.models.search import SearchRequest, SearchResponse
from infrastructure.search import SearchStrategyFactory

router = APIRouter(
    prefix="/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}},
)

# Mount templates
templates_path = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


async def get_search_service() -> SearchService:
    """Dependency to get search service instance."""
    search_strategy = SearchStrategyFactory.create_strategy("cosine")
    return SearchService(search_strategy)


@router.get("/")
async def get_search_interface(request: Request, q: Optional[str] = Query(None, alias="q")):
    """Get the search interface template or perform search if query provided."""
    if not q:
        return templates.TemplateResponse("search.html", {"request": request})

    search_service = await get_search_service()
    search_request = SearchRequest(query=q)
    return await search_service.search(search_request)


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest, search_service: SearchService = Depends(get_search_service)) -> SearchResponse:
    """Process a search request."""
    logger.info(f"Received search request: {request.query}")
    return await search_service.search(request)

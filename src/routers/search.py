import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from main import search_title

router = APIRouter(
    prefix="",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)


# Mount templates
templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page: serving frontend
    """
    return templates.TemplateResponse("search.html", {"request": request})


@router.get("/search")
async def search(q: Optional[str] = Query(None, alias="q")):
    """
    Search the title of the documents
    Args:
        q: The query to search for
    Returns:
        A dictionary containing the results and the server time
    """
    if not q:
        return {"results": [], "server_time": 0}

    start_time = time.time()
    results = search_title(q)
    server_time = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
    return {"results": list(results), "server_time": server_time}  # Server processing time in milliseconds

import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from search import search_title

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)

# Mount templates
templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


@router.get("/")
@router.post("/")
async def chat(request: Request, q: Optional[str] = Query(None, alias="q")):
    """
    Search the title of the documents
    Args:
        q: The query to search for
    Returns:
        A dictionary containing the results and the server time
    """
    # If no query or GET request without query, return the template
    if request.method == "GET" and not q:
        return templates.TemplateResponse("search.html", {"request": request})

    if not q:
        return {"results": [], "server_time": 0}

    start_time = time.time()
    response = search_title(q)
    server_time = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
    return {"results": response, "server_time": server_time}

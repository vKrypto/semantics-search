import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sentence_transformers import SentenceTransformer

from main import TRANSFORMER_MODEL, search_title

app = FastAPI(title="Semantic Search API")

# Create templates directory
templates_path = Path(__file__).parent / "templates"
templates_path.mkdir(exist_ok=True)

# Mount templates
templates = Jinja2Templates(directory=str(templates_path))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search")
async def search(q: Optional[str] = Query(None, alias="q")):
    if not q:
        return {"results": [], "server_time": 0}

    start_time = time.time()
    results = search_title(q)
    # Convert results to a more frontend-friendly format
    formatted_results = []
    for item in results:
        formatted_results.append(
            {
                "title": item.get("_source", {}).get("title", "No title"),
                "description": item.get("_source", {}).get("description", "No description"),
                "score": round(item.get("_score", 0) - 1, 2),  #  converting to --> [-1, 1] scale again
            }
        )

    server_time = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
    return {"results": formatted_results, "server_time": server_time}  # Server processing time in milliseconds


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

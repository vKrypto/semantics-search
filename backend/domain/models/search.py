from typing import List, Optional

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """A single search result."""

    title: str = Field(..., description="The title of the document")
    content: str = Field(..., description="The content snippet")
    score: float = Field(..., description="The relevance score")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata about the result")


class SearchRequest(BaseModel):
    """A search request from the user."""

    query: str = Field(..., description="The search query")
    search_type: str = Field(default="hybrid", description="Type of search to perform (hybrid/cosine/euclidean)")
    limit: int = Field(default=5, description="Maximum number of results to return")


class SearchResponse(BaseModel):
    """A search response to the user."""

    results: List[SearchResult] = Field(default_factory=list, description="List of search results")
    server_time: float = Field(..., description="Server processing time in milliseconds")
    total_results: int = Field(..., description="Total number of results found")
    query: str = Field(..., description="The original search query")

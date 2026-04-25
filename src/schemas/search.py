from pydantic import BaseModel
from typing import Optional

class BaseSearchRequest(BaseModel):
    top_k: int = 5
    filters: Optional[dict] = None

class SearchRequest(BaseSearchRequest):
    query: str

class VectorSearchRequest(BaseSearchRequest):
    vector: list[float]

class SearchResult(BaseModel):
    id: str
    score: float
    content: str
    metadata: dict

class SearchResponse(BaseModel):
    results: list[SearchResult]
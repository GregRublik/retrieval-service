from pydantic import BaseModel
from typing import Optional

class BaseSearchRequest(BaseModel):
    top_k: int = 5
    filters: Optional[dict] = None

class SearchRequest(BaseSearchRequest):
    query: str
    collection: str

class VectorSearchRequest(BaseSearchRequest):
    vector: list[float]

class SearchResult(BaseModel):
    id: int
    score: float
    content: dict
    metadata: dict

class SearchResponse(BaseModel):
    results: list[SearchResult]
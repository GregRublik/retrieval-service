from pydantic import BaseModel
from typing import Optional, List

class SearchResult(BaseModel):
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    score: Optional[float] = None

class RawPage(BaseModel):
    url: str
    html: str
    score: float
    title: str

class ExtractedDocument(BaseModel):
    url: str
    title: str
    content: str
    score: float

class WebSearchRequest(BaseModel):
    query: str
    question: Optional[str] = None
    top_k: int

class WebSearchResponse(BaseModel):
    data: List[ExtractedDocument]

class ResultWebSearch(BaseModel):
    url: str
    title: str
    content: str
    score: float

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

class ExtractedDocument(BaseModel):
    url: str
    title: str
    text: str

class WebSearchRequest(BaseModel):
    query: str

class WebSearchResponse(BaseModel):
    data: List[ExtractedDocument]

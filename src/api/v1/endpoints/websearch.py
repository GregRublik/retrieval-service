from fastapi import APIRouter, Depends

from schemas.response import APIResponse, ok
from schemas.websearch import WebSearchRequest, WebSearchResponse
from services.websearch import WebSearchService

from depends import get_websearch_service


router = APIRouter(prefix="/web")


@router.post("/search/", response_model=APIResponse[WebSearchResponse])
async def search(
        payload: WebSearchRequest,
        websearch_service: WebSearchService = Depends(get_websearch_service),
):
    """Search info to internet"""
    return ok(await websearch_service.process(payload))

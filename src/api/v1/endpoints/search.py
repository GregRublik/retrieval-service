from fastapi import APIRouter, Depends

from services.search import SearchService
from schemas.search import SearchRequest, SearchResponse, VectorSearchRequest
from schemas.response import APIResponse, ok

from depends import get_search_service


router = APIRouter(prefix="/search")


@router.post("/", response_model=APIResponse[SearchResponse])
async def search(
        payload: SearchRequest,
        search_service: SearchService = Depends(get_search_service),
):
    return ok(await search_service.search(payload))


@router.get("/vector", response_model=APIResponse[SearchResponse])
async def search_by_vector(
    payload: VectorSearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    return ok(await search_service.search_by_vector(payload))


@router.post("/hybrid")
async def hybrid_search(

):
    # query, top_k, alpha
    pass


@router.get("/with_scope")
async def search_with_scope(

):
    # query, scope
    pass


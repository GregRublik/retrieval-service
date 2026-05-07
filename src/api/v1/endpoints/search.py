from fastapi import APIRouter, Depends
from depends import get_search_service
from services.search import SearchService
from schemas.search import SearchRequest, SearchResponse, VectorSearchRequest

router = APIRouter(prefix="/search")

@router.post("/", response_model=SearchResponse)
async def search(
        payload: SearchRequest,
        search_service: SearchService = Depends(get_search_service),
):
    # try:
        return await search_service.search(payload)
    # except Exception as e: qdrant_client.http.exceptions.UnexpectedResponse: # todo не найдена коллекция

@router.get("/vector", response_model=SearchResponse)
async def search_by_vector(
    payload: VectorSearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    return await search_service.search_by_vector(payload)


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


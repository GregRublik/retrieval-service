from fastapi import APIRouter, Depends, status
from qdrant_client.http.exceptions import UnexpectedResponse

from services.search import SearchService
from schemas.search import SearchRequest, SearchResponse, VectorSearchRequest, SearchQueryTextRequest
from schemas.response import APIResponse, ok

from exceptions import APIException, QdrantCollectionNotFoundException
from depends import get_search_service


router = APIRouter(prefix="/search")


@router.post("/query/", response_model=APIResponse[SearchResponse])
async def search(
        payload: SearchRequest,
        search_service: SearchService = Depends(get_search_service),
):
    try:
        return ok(await search_service.search(payload))
    except QdrantCollectionNotFoundException as e:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            error=e.detail
        )

@router.post("/semantic_in_texts/")
async def semantic_search_in_texts(
    payload: SearchQueryTextRequest,
    search_service: SearchService = Depends(get_search_service),
):
    try:
        return ok(await search_service.search_by_query_in_text(payload))
    finally:
        pass


@router.post("/vector/", response_model=APIResponse[SearchResponse])
async def search_by_vector(
    payload: VectorSearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    try:
        return ok(await search_service.search_by_vector(payload))
    except QdrantCollectionNotFoundException as e:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            error=e.detail
        )

@router.post("/hybrid/")
async def hybrid_search(

):
    # query, top_k, alpha
    pass


@router.get("/with_scope/")
async def search_with_scope(

):
    # query, scope
    pass


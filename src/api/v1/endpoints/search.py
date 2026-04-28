from fastapi import APIRouter, Depends
from depends import get_search_service
from services.search import SearchService
from schemas.search import SearchRequest, SearchResponse

router = APIRouter(prefix="/search")

@router.post("/", response_model=SearchResponse)
async def search(
        payload: SearchRequest,
        search_service: SearchService = Depends(get_search_service),
):
    return await search_service.search(payload)


@router.get("/vector")
async def search_by_vector(

):
    # vector, top_k, filters
    pass


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


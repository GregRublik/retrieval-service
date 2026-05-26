from fastapi import APIRouter, Depends
from datetime import datetime

from schemas.health import ResponseHealth, ResponseReady, ResponseLive, Status, DependencyCheck
from schemas.response import APIResponse, ok
from services.health import HealthService
from depends import get_health_service


router = APIRouter()


@router.get("/health/", response_model=APIResponse[ResponseHealth])
async def health():
    return ok(
        ResponseHealth(
            service="retrieval-service",
            timestamp=datetime.now()
        )
    )


@router.get("/ready/", response_model=APIResponse[ResponseReady])
async def readiness(
    health_service: HealthService = Depends(get_health_service),
):
    qdrant_healthy = await health_service.check_qdrant()
    dependencies = [
        DependencyCheck(name="qdrant", healthy=qdrant_healthy),
    ]
    status = Status.ready if all(d.healthy for d in dependencies) else Status.degraded
    return ok(
        ResponseReady(
            status=status,
            timestamp=datetime.now(),
            dependencies=dependencies,
        )
    )


@router.get("/live/", response_model=APIResponse[ResponseLive])
async def liveness():
    return ok(
        ResponseLive(
            status=Status.live,
            timestamp=datetime.now(),
            dependencies=[],
        )
    )

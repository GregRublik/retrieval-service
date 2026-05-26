from datetime import datetime
from pydantic import BaseModel
from enum import StrEnum

class Status(StrEnum):
    ready = "ready"
    live = "live"
    degraded = "degraded"

class DependencyCheck(BaseModel):
    name: str
    healthy: bool

class ResponseHealth(BaseModel):
    service: str
    timestamp: datetime

class ResponseReady(BaseModel):
    status: Status
    timestamp: datetime
    dependencies: list[DependencyCheck]

class ResponseLive(ResponseReady):
    status: Status = Status.live

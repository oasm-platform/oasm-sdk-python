from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkerAliveRequest:
    """Request payload for a worker keep-alive signal."""
    token: str

@dataclass
class WorkerAliveResponse:
    """Response from the API after a keep-alive signal."""
    alive: str

@dataclass
class WorkerJoinRequest:
    """Request payload for joining a worker."""
    api_key: str

@dataclass
class WorkerJoinResponse:
    """Response returned after a worker successfully joins."""
    id: str
    created_at: datetime
    updated_at: datetime
    last_seen_at: datetime
    token: str
    current_jobs_count: int
    type: str
    scope: str
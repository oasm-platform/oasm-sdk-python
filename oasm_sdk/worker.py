from datetime import datetime
from .models import WorkerAliveResponse, WorkerJoinResponse
from .client import Client
from .exceptions import raise_for_error, APIError


def worker_alive(client: Client, token: str) -> WorkerAliveResponse:
    """
    Sends a keep-alive request to the API.
    
    Args:
        client: The OASM client instance.
        token: The worker's token.
    
    Returns:
        A WorkerAliveResponse object on success.
    
    Raises:
        APIError: If the request fails or returns an error status.
    """
    url = f"{client.api_url}/api/workers/alive"
    req_body = {"token": token}
    try:
        resp = client.session.post(url, json=req_body)
        raise_for_error(resp)
        return WorkerAliveResponse(**resp.json())
    except Exception as e:
        if isinstance(e, APIError):
            raise
        raise APIError(message=f"Worker alive request failed: {e}") from e

def worker_join(client: Client) -> WorkerJoinResponse:
    """
    Sends a join request to the API.
    
    Args:
        client: The OASM client instance.
    
    Returns:
        A WorkerJoinResponse object on success.
    
    Raises:
        APIError: If the request fails or returns an error status.
    """
    if not client.api_key:
        raise ValueError("API key is required for joining a worker")
        
    url = f"{client.api_url}/api/workers/join"
    req_body = {"apiKey": client.api_key}
    try:
        resp = client.session.post(url, json=req_body)
        raise_for_error(resp)
        # Parse the JSON response and convert to a WorkerJoinResponse object
        response_data = resp.json()
        return WorkerJoinResponse(
            id=response_data.get("id", ""),
            created_at=datetime.fromisoformat(response_data.get("createdAt", "")),
            updated_at=datetime.fromisoformat(response_data.get("updatedAt", "")),
            last_seen_at=datetime.fromisoformat(response_data.get("lastSeenAt", "")),
            token=response_data.get("token", ""),
            current_jobs_count=response_data.get("currentJobsCount", 0),
            type=response_data.get("type", ""),
            scope=response_data.get("scope", "")
        )
    except Exception as e:
        if isinstance(e, APIError):
            raise
        raise APIError(message=f"Worker join request failed: {e}") from e
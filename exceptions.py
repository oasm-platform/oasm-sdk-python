class APIError(Exception):
    """
    APIError represents an error response returned by the API.
    It extends the base Exception class.
    """
    def __init__(self, message: str, error_type: str = "Unknown", status_code: int = 0):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.status_code = status_code

    def __str__(self) -> str:
        """Provides a formatted string representation of the API error."""
        return f"api error: {self.message} ({self.error_type}, {self.status_code})"

def raise_for_error(response) -> None:
    """
    Checks if the HTTP response indicates an error and raises an APIError if so.
    """
    if 200 <= response.status_code < 300:
        return
    
    try:
        error_data = response.json()
        raise APIError(
            message=error_data.get("message", "An unexpected API error occurred"),
            error_type=error_data.get("error", "Unknown"),
            status_code=response.status_code
        )
    except Exception:
        raise APIError(
            message=f"Failed to parse error response. Status code: {response.status_code}",
            status_code=response.status_code
        )
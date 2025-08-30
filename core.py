import urllib.parse
from typing import Callable
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util import Retry

Option = Callable[["Client"], None]

def WithApiUrl(api_url: str) -> Option:
    """Sets the base API URL for the Client."""
    def option(c: "Client") -> None:    
        if not api_url:
            raise ValueError("API URL cannot be empty")
        parsed_url = urllib.parse.urlparse(api_url)
        if not parsed_url.scheme:
            raise ValueError("API URL must include a scheme (e.g., http:// or https://)")
        c.api_url = api_url.rstrip('/')
    return option

def WithApiKey(api_key: str) -> Option:
    """Sets the API key for the Client."""
    def option(c: "Client") -> None:
        if not api_key:
            raise ValueError("Invalid API key")
        c.api_key = api_key
    return option

def WithRequest(session: Session) -> Option:
    """Sets a custom requests session for the Client."""
    def option(c: "Client") -> None:
        if not isinstance(session, Session):
            raise TypeError("Request session must be a requests.Session object")
        c.session = session
    return option

class Client:
    """
    Client represents an HTTP client wrapper with configurable options.
    It uses requests for HTTP operations and can be customized with an API URL and API key.
    """
    def __init__(self, *opts: Option):
        """
        Creates a new Client instance with the given options.
        Example:
            client = Client(
                WithApiUrl("https://api.example.com"),
                WithApiKey("my-secret-key")
            )
        The functional options allow you to configure the client in a flexible and extensible way.
        """
        # Default session with retry logic
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        
        self.session = Session()
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.api_url = "http://localhost:6276"
        self.api_key = ""

        # Apply options
        for opt in opts:
            opt(self)

    def health(self) -> bool:
        """
        Checks the health status of the API.
        Returns:
            True if the API is healthy, False otherwise.
        """
        from .exceptions import APIError 
        
        url = f"{self.api_url}/api/health"
        try:
            resp = self.session.get(url)
            resp.raise_for_status()
            return resp.text.strip() == "OK"
        except Exception as e:
            raise APIError(message=f"Health check failed: {e}") from e
import urllib.parse
from typing import Callable
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

Option = Callable[["Client"], None]

def with_api_url(api_url: str) -> Option:
    """
    Sets the base API URL for the Client.

    Args:
        api_url: The API base URL, e.g., "https://api.example.com".

    Returns:
        A callable that sets the client's API URL.
    """
    def option(c: "Client") -> None:
        if not api_url:
            raise ValueError("API URL cannot be empty.")
        parsed_url = urllib.parse.urlparse(api_url)
        if not parsed_url.scheme:
            raise ValueError("API URL must include a scheme (e.g., http:// or https://).")
        c.api_url = api_url.rstrip('/')
    return option

def with_api_key(api_key: str) -> Option:
    """
    Sets the API key for the Client.

    Args:
        api_key: The API key string.

    Returns:
        A callable that sets the client's API key.
    """
    def option(c: "Client") -> None:
        if not api_key:
            raise ValueError("Invalid API key.")
        c.api_key = api_key
    return option

def with_session(session: Session) -> Option:
    """
    Sets a custom requests session for the Client.

    Args:
        session: A custom requests.Session object.

    Returns:
        A callable that sets the client's session.
    """
    def option(c: "Client") -> None:
        if not isinstance(session, Session):
            raise TypeError("The provided session must be a requests.Session object.")
        c.session = session
    return option

class Client:
    """
    Client represents an HTTP client wrapper with configurable options.
    It uses the `requests` library for HTTP operations and can be customized
    with an API URL and API key via functional options.
    """
    def __init__(self, *opts: Option):
        """
        Creates a new Client instance with the given options.
        The functional options (with_api_url, with_api_key, etc.) allow you
        to configure the client in a flexible and extensible way.
        
        Args:
            *opts: A variable number of functional options.
        """
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        
        self.session = Session()
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.api_url = "http://localhost:6276"
        self.api_key = ""

        for opt in opts:
            opt(self)
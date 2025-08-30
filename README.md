# OASM SDK for Python

The OASM SDK for Python provides a convenient interface to interact with the OASM (Open API Service Manager) API. This SDK allows you to easily manage workers and communicate with the OASM service.

## Features

- Easy-to-use client for OASM API
- Functional options pattern for flexible client configuration
- Built-in retry mechanism for robust API communication
- Support for worker registration and keep-alive signals
- Comprehensive error handling with custom exceptions
- Full type hints for better development experience

## Installation

To install the OASM SDK, you can use pip:

```bash
pip install oasm-sdk
```

Or if you have the source code:

```bash
pip install .
```

### Requirements

- Python 3.8 or higher
- requests>=2.31.0
- urllib3>=1.26.0

## Quick Start

### Creating a Client

```python
from oasm_sdk.client import Client, with_api_url, with_api_key

# Create a client with default settings
client = Client()

# Create a client with custom settings
client = Client(
    with_api_url("http://localhost:6276"),  # Replace with your API URL
    with_api_key("your-api-key-here")       # Replace with your API key
)
```

### Health Check

```python
try:
    is_healthy = client.health()
    print(f"API is {'healthy' if is_healthy else 'unhealthy'}")
except Exception as e:
    print(f"Health check failed: {e}")
```

### Worker Management

#### Joining a Worker

```python
from oasm_sdk.worker import worker_join

try:
    response = worker_join(client)
    print(f"Worker joined with ID: {response.id}")
    print(f"Worker token: {response.token}")
except Exception as e:
    print(f"Failed to join worker: {e}")
```

#### Sending Keep-Alive Signal

```python
from oasm_sdk.worker import worker_alive

try:
    token = "your-worker-token"
    response = worker_alive(client, token)
    print(f"Keep-alive response: {response.alive}")
except Exception as e:
    print(f"Keep-alive failed: {e}")
```

## Running the Example

To run the example code:

```bash
python examples/main.py
```

Make sure to update the API URL and API key in the example file before running it.

## API Reference

### Client

The `Client` class is the main entry point for interacting with the OASM API.

#### Constructor

```python
Client(*opts: Option)
```

Creates a new client instance with the provided options.

#### Options

- `with_api_url(api_url: str)`: Sets the base API URL
- `with_api_key(api_key: str)`: Sets the API key
- `with_session(session: Session)`: Sets a custom requests session

#### Methods

- `health() -> bool`: Checks the health status of the API

### Worker Functions

- `worker_join(client: Client) -> WorkerJoinResponse`: Registers a new worker
- `worker_alive(client: Client, token: str) -> WorkerAliveResponse`: Sends a keep-alive signal

### Exceptions

- `APIError`: Raised when the API returns an error response

## Development

### Running Tests

To run the tests, use:

```bash
python -m pytest
```

### Dependencies

To install development dependencies:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

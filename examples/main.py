from oasm_sdk.client import Client, with_api_url, with_api_key
from oasm_sdk.worker import worker_join, worker_alive

def main():
    # Initialize the client with API credentials
    client = Client(
        with_api_url("http://localhost:6276"),  # Replace with your API URL
        with_api_key("LkOjR9w8sWvpCTSWYsU4KrvYlSJFnsU1")      # Replace with your API key
    )

    try:
        # Example 1: Check API health
        print("Checking API health...")
        is_healthy = client.health()
        print(f"API is {'healthy' if is_healthy else 'not healthy'}")

        # Example 2: Worker operations
        print("\nJoining as a worker...")
        worker = worker_join(client)
        print(f"Worker joined successfully! Worker ID: {worker.id}")
        print(f"Worker token: {worker.token}")

        # Example 3: Send keep-alive
        print("\nSending keep-alive...")
        response = worker_alive(client, worker.token)
        print(f"Keep-alive response: {response.alive}")

        # Example 4: Using client for custom API calls
        print("\nMaking a custom API call...")
        response = client.session.get(f"{client.api_url}/api/endpoint", 
                                    headers={"Authorization": f"Bearer {worker.token}"})
        response.raise_for_status()
        print(f"Custom API response: {response.json()}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
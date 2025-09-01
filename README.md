# OASM SDK for Python

`oasm-sdk-python` is the official Python client for interacting with the **OASM Platform** API. It provides convenient wrappers for worker management endpoints such as **join** and **keep-alive**.

---

## Installation

Use `pip` to install:

```bash
pip install oasm-sdk
```

Then import it in your project:

```python
import oasm_sdk
```

---

## Usage

### Initialize Client

```python
import oasm_sdk

def main():
    # Create a new client with API URL and API key
    client = oasm_sdk.Client(
        oasm_sdk.with_api_url("https://api.oasm.dev"),
        oasm_sdk.with_api_key("your-api-key")
    )

    # Join worker
    try:
        join_resp = oasm_sdk.worker_join(client)
        print(f"Worker joined: {join_resp.id}")

        # Send keep-alive
        alive_resp = oasm_sdk.worker_alive(client, join_resp.token)
        print(f"Worker alive: {alive_resp.alive}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

---

## License

[MIT](./LICENSE)

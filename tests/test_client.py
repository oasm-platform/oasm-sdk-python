import unittest
from oasm_sdk.client import Client, with_api_url, with_api_key, with_session
from requests.sessions import Session

class TestClient(unittest.TestCase):
    """
    Test suite for the Client class and its functional options.
    """

    def test_new_client_default_config(self):
        """
        Test that a new client is initialized with default values.
        """
        client = Client()
        self.assertEqual(client.api_url, "http://localhost:6276")
        self.assertEqual(client.api_key, "")
        self.assertIsInstance(client.session, Session)

    def test_with_api_url_option(self):
        """
        Test that with_api_url correctly sets the API URL.
        """
        test_url = "https://api.oasm.com"
        client = Client(with_api_url(test_url))
        self.assertEqual(client.api_url, test_url)

        # Test URL with trailing slash
        client = Client(with_api_url("https://api.oasm.com/"))
        self.assertEqual(client.api_url, "https://api.oasm.com")

        with self.assertRaises(ValueError):
            Client(with_api_url(""))

    def test_with_api_key_option(self):
        """
        Test that with_api_key correctly sets the API key.
        """
        test_key = "test_api_key_123"
        client = Client(with_api_key(test_key))
        self.assertEqual(client.api_key, test_key)

        with self.assertRaises(ValueError):
            Client(with_api_key(""))

    def test_with_session_option(self):
        """
        Test that with_session correctly sets a custom session object.
        """
        custom_session = Session()
        client = Client(with_session(custom_session))
        self.assertIs(client.session, custom_session)

        with self.assertRaises(TypeError):
            Client(with_session(None))
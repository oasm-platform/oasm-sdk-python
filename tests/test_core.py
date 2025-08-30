import unittest
from unittest.mock import patch
from oasm_sdk.client import Client
from oasm_sdk.exceptions import APIError

class TestClientCoreMethods(unittest.TestCase):
    """
    Test suite for core methods of the Client class.
    """

    @patch("requests.sessions.Session.get")
    def test_health_success(self, mock_get):
        """
        Test that health() returns True for a successful API response.
        """
        # Configure the mock to return a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "OK"

        client = Client()
        is_healthy = client.health()
        self.assertTrue(is_healthy)
        
        # Verify that the correct URL was called
        mock_get.assert_called_once_with(client.api_url + "/api/health")

    @patch("requests.sessions.Session.get")
    def test_health_failure_status(self, mock_get):
        """
        Test that health() raises an error for a non-200 status code.
        """
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal Server Error"

        client = Client()
        with self.assertRaises(APIError) as cm:
            client.health()
        
        self.assertEqual(cm.exception.status_code, 500)

    @patch("requests.sessions.Session.get")
    def test_health_failure_network_error(self, mock_get):
        """
        Test that health() raises an error on a network issue.
        """
        # Simulate a network error by raising an exception
        from requests.exceptions import ConnectionError
        mock_get.side_effect = ConnectionError("Connection refused")

        client = Client()
        with self.assertRaises(APIError) as cm:
            client.health()
        
        self.assertIn("Health check failed", str(cm.exception))
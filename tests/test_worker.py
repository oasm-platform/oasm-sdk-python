import unittest
from unittest.mock import patch
from oasm_sdk.worker import worker_join, worker_alive
from oasm_sdk.client import Client
from oasm_sdk.exceptions import APIError

class TestWorkerMethods(unittest.TestCase):
    """
    Test suite for worker-related API calls.
    """
    
    def setUp(self):
        # Set up a client with a valid API key for testing
        self.client = Client()
        self.client.api_key = "LkOjR9w8sWvpCTSWYsU4KrvYlSJFnsU1"

    @patch("requests.sessions.Session.post")
    def test_worker_join_success(self, mock_post):
        """
        Test that worker_join returns a valid WorkerJoinResponse on success.
        """
        # Mock a successful API response
        mock_response = {
            "id": "test_id_123",
            "createdAt": "2023-01-01T10:00:00Z",
            "updatedAt": "2023-01-01T10:00:00Z",
            "lastSeenAt": "2023-01-01T10:00:00Z",
            "token": "LkOjR9w8sWvpCTSWYsU4KrvYlSJFnsU1",
            "currentJobsCount": 0,
            "type": "test_type",
            "scope": "test_scope"
        }
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response

        response = worker_join(self.client)
        
        self.assertEqual(response.id, "test_id_123")
        self.assertEqual(response.token, mock_response["token"])
        self.assertEqual(response.type, "test_type")

    @patch("requests.sessions.Session.post")
    def test_worker_join_failure(self, mock_post):
        """
        Test that worker_join raises an APIError on API failure.
        """
        # Mock a failed API response
        mock_post.return_value.status_code = 401
        # Create a mock for the json method
        mock_json = mock_post.return_value.json
        mock_json.return_value = {
            "message": "Invalid API key",
            "error": "AuthenticationError",
            "statusCode": 401
        }

        with self.assertRaises(APIError) as cm:
            worker_join(self.client)
        
        self.assertIn("Invalid API key", str(cm.exception))
        self.assertEqual(cm.exception.status_code, 401)

    @patch("requests.sessions.Session.post")
    def test_worker_alive_success(self, mock_post):
        """
        Test that worker_alive returns a valid WorkerAliveResponse on success.
        """
        # Mock a successful API response
        mock_response = {"alive": "OK"}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        response = worker_alive(self.client, "some_token")
        
        self.assertEqual(response.alive, "OK")

    @patch("requests.sessions.Session.post")
    def test_worker_alive_failure(self, mock_post):
        """
        Test that worker_alive raises an APIError on API failure.
        """
        # Mock a failed API response
        mock_post.return_value.status_code = 400
        # Create a mock for the json method
        mock_json = mock_post.return_value.json
        mock_json.return_value = {
            "message": "Invalid worker token",
            "error": "InvalidRequestError",
            "statusCode": 400
        }

        with self.assertRaises(APIError) as cm:
            worker_alive(self.client, "invalid_token")

        self.assertIn("Invalid worker token", str(cm.exception))
        self.assertEqual(cm.exception.status_code, 400)
import unittest
from unittest.mock import patch

from app import app


class BotReplyTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_missing_payload_returns_validation_error(self):
        response = self.client.post("/get-response", json=None)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please type a message.", response.get_json()["error"])

    def test_empty_message_returns_validation_error(self):
        response = self.client.post("/get-response", json={"message": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please type a message.", response.get_json()["error"])

    @patch("app.get_chatbot_response", return_value="Test reply")
    @patch("app.save_log")
    def test_valid_message_returns_response(self, mock_save_log, mock_get_chatbot_response):
        response = self.client.post("/get-response", json={"message": "hello"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["response"], "Test reply")
        mock_get_chatbot_response.assert_called_once_with("hello")
        mock_save_log.assert_called_once_with("hello", "Test reply")


if __name__ == "__main__":
    unittest.main()

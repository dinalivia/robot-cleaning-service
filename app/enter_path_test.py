import unittest
from unittest.mock import patch, MagicMock
from app.main import execute_commands, app
from flask import json


class TestEnterPathEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_enter_path_invalid_input(self):
        payload = {
            "start": {"x": 0, "y": 0},
            "commmands": [{"direction": "invalid", "steps": 1}],
        }
        response = self.app.post(
            "/tibber-developer-test/enter-path",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    @patch("app.main.execute_commands", side_effect=MemoryError)
    def test_enter_path_memory_error(self, mock_execute_commands):
        payload = {
            "start": {"x": 0, "y": 0},
            "commmands": [{"direction": "north", "steps": 1}],
        }
        response = self.app.post(
            "/tibber-developer-test/enter-path",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Internal server error")

    @patch("app.main.db.session.add", side_effect=Exception("DB error"))
    def test_enter_path_db_error(self, mock_db):
        payload = {
            "start": {"x": 0, "y": 0},
            "commmands": [{"direction": "north", "steps": 1}],
        }
        response = self.app.post(
            "/tibber-developer-test/enter-path",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Internal server error")

    def test_enter_path_empty_commands(self):
        payload = {"start": {"x": 0, "y": 0}, "commmands": []}
        response = self.app.post(
            "/tibber-developer-test/enter-path",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["result"], 1)  # Only the start position

    @patch("app.main.Execution")
    @patch("app.main.db")
    def test_enter_path_successful(self, mock_db, mock_execution):
        mock_execution.return_value = MagicMock(timestamp="2023-01-01T00:00:00Z")
        payload = {
            "start": {"x": 0, "y": 0},
            "commmands": [
                {"direction": "north", "steps": 1},
                {"direction": "east", "steps": 1},
            ],
        }
        response = self.app.post(
            "/tibber-developer-test/enter-path",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("result", data)
        self.assertEqual(data["result"], 3)


if __name__ == "__main__":
    unittest.main()

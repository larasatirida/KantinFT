import json
import unittest
from unittest.mock import patch
from src.lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    def make_event(self, method, path, body=None):
        return {
            "version": "2.0",
            "rawPath": path,
            "requestContext": {
                "http": {
                    "method": method,
                    "path": path
                }
            },
            "body": json.dumps(body) if body is not None else None,
            "isBase64Encoded": False
        }

    @patch("src.lambda_function.create_order")
    def test_create_order(self, mock_create_order):
        data = {
            "customer_name": "Rila",
            "tenant_name": "Masakan Jawa",
            "food_name": "Nasi Ayam",
            "quantity": 2,
            "unit_price": 15000,
            "pickup_time": "2026-11-25T12:00:00+07:00"
        }

        mock_create_order.return_value = {
            "order_id": "abc123",
            "total_price": 30000,
            "status": "PENDING"
        }

        event = self.make_event("POST", "/orders", data)
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 201)
        self.assertEqual(
            json.loads(result["body"])["data"]["order_id"],
            "abc123"
        )
        mock_create_order.assert_called_once_with(data)

    @patch("src.lambda_function.create_order")
    def test_invalid_order(self, mock_create_order):
        mock_create_order.side_effect = ValueError("Invalid input")

        event = self.make_event("POST", "/orders", {})
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 400)

    def test_invalid_json(self):
        event = self.make_event("POST", "/orders")
        event["body"] = "invalid json"

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 400)

    def test_get_orders(self):
        event = self.make_event("GET", "/orders")
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 501)

    def test_update_order(self):
        event = self.make_event("PUT", "/orders/abc123")
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 501)

    def test_delete_order(self):
        event = self.make_event("DELETE", "/orders/abc123")
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 501)

    def test_invalid_route(self):
        event = self.make_event("GET", "/unknown")
        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 404)


if __name__ == "__main__":
    unittest.main()
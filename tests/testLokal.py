import unittest
import json

from src.lambda_function import lambda_handler


class TestLambda(unittest.TestCase):

    def test_routes(self):
        routes = [
            ("POST", "POST /orders"),
            ("GET", "GET /orders"),
            ("PUT", "PUT /orders/{id}"),
            ("DELETE", "DELETE /orders/{id}")
        ]

        for method, route in routes:
            with self.subTest(method=method):
                event = {
                    "version": "2.0",
                    "routeKey": route,
                    "requestContext": {
                        "http": {
                            "method": method
                        }
                    }
                }

                result = lambda_handler(event, None)

                self.assertEqual(result["statusCode"], 200)
                print(json.loads(result["body"]))

    def test_invalid_route(self):
        event = {
            "version": "2.0",
            "routeKey": "GET /unknown",
            "requestContext": {
                "http": {
                    "method": "GET"
                }
            }
        }

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 404)


if __name__ == "__main__":
    unittest.main()
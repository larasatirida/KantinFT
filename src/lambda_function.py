import json
import logging
from .order_service import create_order

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    path = event.get("rawPath", "")

    try:
        if method == "POST" and path == "/orders":
            data = json.loads(event.get("body") or "{}")
            order = create_order(data)

            return response(201, {
                "message": "Order created successfully",
                "data": order
            })

        elif method == "GET" and path == "/orders":
            return response(501, {
                "message": "Read orders not implemented yet"
            })

        elif method == "PUT" and path.startswith("/orders/"):
            return response(501, {
                "message": "Update order not implemented yet"
            })

        elif method == "DELETE" and path.startswith("/orders/"):
            return response(501, {
                "message": "Delete order not implemented yet"
            })

        return response(404, {
            "message": "Route not found"
        })

    except json.JSONDecodeError:
        return response(400, {
            "message": "Invalid JSON format"
        })

    except ValueError as error:
        return response(400, {
            "message": str(error)
        })

    except Exception:
        logger.exception("Failed to process request")

        return response(500, {
            "message": "Internal server error"
        })
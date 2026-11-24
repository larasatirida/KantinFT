import json
def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    #Ambil HTTP method dan route dari API Gateway
    method = event.get("requestContext", {}).get(
        "http", {}
    ).get("method")

    route = event.get("routeKey", "")

    #Create order
    if method == "POST" and route == "POST /orders":
        return response(200, {
            "message": "Create order endpoint is ready"
        })

    #Read orders
    elif method == "GET" and route == "GET /orders":
        return response(200, {
            "message": "Get orders endpoint is ready"
        })

    #Update order
    elif method == "PUT" and route == "PUT /orders/{id}":
        return response(200, {
            "message": "Update order endpoint is ready"
        })

    #Delete order
    elif method == "DELETE" and route == "DELETE /orders/{id}":
        return response(200, {
            "message": "Delete order endpoint is ready"
        })

    #Route tidak ditemukan
    return response(404, {
        "message": "Route not found"
    })
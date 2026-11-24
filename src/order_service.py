from uuid import uuid4
from datetime import datetime, timezone
from .database import get_table
from .validators import validate_order


def create_order(data):
    validate_order(data)

    now = datetime.now(timezone.utc).isoformat()

    order = {
        "order_id": str(uuid4()),
        "customer_name": data["customer_name"].strip(),
        "tenant_name": data["tenant_name"].strip(),
        "food_name": data["food_name"].strip(),
        "quantity": data["quantity"],
        "unit_price": data["unit_price"],
        "total_price": (
            data["quantity"] * data["unit_price"]
        ),
        "pickup_time": data["pickup_time"],
        "status": "PENDING",
        "created_at": now,
        "updated_at": now
    }

    table = get_table()

    table.put_item(
        Item=order,
        ConditionExpression="attribute_not_exists(order_id)"
    )

    return order
import json
import uuid
from datetime import datetime, timezone
from .database import BUCKET_NAME, get_s3_client, get_order_key
from .validators import validate_order

def create_order(data):
    validate_order(data)

    order_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    order = {
        "order_id": order_id,
        "customer_name": data["customer_name"].strip(),
        "tenant_name": data["tenant_name"].strip(),
        "food_name": data["food_name"].strip(),
        "quantity": data["quantity"],
        "unit_price": data["unit_price"],
        "total_price": data["quantity"] * data["unit_price"],
        "pickup_time": data["pickup_time"],
        "status": "PENDING",
        "created_at": now,
        "updated_at": now
    }

    s3 = get_s3_client()

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=get_order_key(order_id),
        Body=json.dumps(order).encode("utf-8"),
        ContentType="application/json"
    )

    return order
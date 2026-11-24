from datetime import datetime
REQUIRED_FIELDS = [
    "customer_name",
    "tenant_name",
    "food_name",
    "quantity",
    "unit_price",
    "pickup_time"
]

VALID_STATUSES = [
    "PENDING",
    "PROCESSING",
    "READY",
    "COMPLETED"
]

UPDATABLE_FIELDS = REQUIRED_FIELDS + ["status"]


def validate_order(data, partial=False):
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")

    if not partial:
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(f"{field} is required")

    allowed_fields = (
        UPDATABLE_FIELDS if partial else REQUIRED_FIELDS
    )

    for field in data:
        if field not in allowed_fields:
            raise ValueError(f"{field} is not allowed")

    if partial and not data:
        raise ValueError("No fields to update")

    # Validasi atribut teks
    for field in [
        "customer_name",
        "tenant_name",
        "food_name"
    ]:
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field} must be a non-empty string"
                )

    # Validasi jumlah dan harga
    for field in ["quantity", "unit_price"]:
        if field in data:
            value = data[field]

            if type(value) is not int or value <= 0:
                raise ValueError(
                    f"{field} must be a positive integer"
                )

    # Validasi waktu pengambilan
    if "pickup_time" in data:
        try:
            value = data["pickup_time"]
            parsed = datetime.fromisoformat(value)

            if "T" not in value or parsed.tzinfo is None:
                raise ValueError()

        except (ValueError, TypeError):
            raise ValueError(
                "pickup_time must be an ISO 8601 timestamp "
                "with timezone"
            )

    # Validasi status
    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            raise ValueError("Invalid order status")
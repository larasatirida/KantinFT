import os
import boto3

BUCKET_NAME = os.environ.get(
    "BUCKET_NAME",
    "kantinft-orders-2785"
)

ORDERS_PREFIX = "orders/"


def get_s3_client():
    return boto3.client("s3")


def get_order_key(order_id):
    return f"{ORDERS_PREFIX}{order_id}.json"
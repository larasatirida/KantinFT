import os
import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "KantinOrders")

def get_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(TABLE_NAME)
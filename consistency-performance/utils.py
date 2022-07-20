import os
import random
import secrets
import string
import time

import boto3

ITEM_SIZE = 1024  # 1KB
TABLE_NAME = os.environ["TABLE_NAME"]

client = boto3.client("dynamodb")


def build_item():
    id = secrets.token_hex(20)
    gsipk = secrets.token_hex(20)
    data = "".join([random.choice(string.ascii_letters) for _ in range(ITEM_SIZE)])

    return {
        "Id": {"S": id},
        "GSIPK": {"S": gsipk},
        "Data": {"S": data},
    }


def test_main_table(wait=0):
    item = build_item()

    client.put_item(TableName=TABLE_NAME, Item=item)

    time.sleep(wait)

    response = client.get_item(TableName=TABLE_NAME, Key={"Id": item['Id']})

    return response.get("Item") == item


def test_gsi(wait=0):
    item = build_item()

    client.put_item(TableName=TABLE_NAME, Item=item)

    time.sleep(wait)

    response = client.query(
        TableName=TABLE_NAME,
        IndexName="GSI1",
        KeyConditionExpression="GSIPK = :gsipk",
        ExpressionAttributeValues={":gsipk": item["GSIPK"]},
    )

    print(response)

    return response.get("Items") and response.get("Items")[0] == item

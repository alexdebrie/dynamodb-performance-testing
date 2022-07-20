import os
import uuid

import boto3

TABLE = os.environ['TABLE_NAME']


def get_client():
    client = boto3.client('dynamodb')
    client.describe_table(TableName=TABLE)
    return client


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


# Need this one for TransactWriteItems failures to be recorded with timeit
def exception_wrapper(func, *args, **kwargs):
    def wrapped():
        try:
            return func(*args, **kwargs)
        except:
            pass
    return wrapped


def make_put_item():
    return {
        'TableName': TABLE,
        'Item': {
            'Id': {
                'S': str(uuid.uuid4())
            }
        }
    }


def make_batch_items(count):
    items = []
    for i in range(count):
        items.append({
            'PutRequest': {
                'Item': {
                    'Id': {
                        'S': str(uuid.uuid4())
                    } 
                }
            }
        })
    return {
        'RequestItems': {
            TABLE: items
        }
    }


def make_transact_items(count, fail=False):
    items = []
    for i in range(count):
        items.append({
            'Put': {
                'TableName': TABLE,
                'Item': {
                    'Id': {
                        'S': str(uuid.uuid4())
                    } 
                }
            }
        })
    if fail:
        items[0]['Put']['ConditionExpression'] = 'attribute_exists(Id)'
    
    return {
        'TransactItems': items
    }

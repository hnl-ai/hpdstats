import boto3
import botocore


def check_if_item_exists(table_name, key):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key=key)
    except botocore.exceptions.ClientError as e:
        return False
    else:
        if 'Item' not in response:
            return False
        return response['Item']


def insert_item(table_name, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(
        Item=item
    )

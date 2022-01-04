# -*- coding: utf-8 -*-
"""The dynamodb utility module."""

import boto3
import botocore


def check_if_item_exists(table_name, key):
    """Checks if the given key exists in a table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    if not key:
        return False

    try:
        response = table.get_item(Key=key)
    except botocore.exceptions.ClientError as error:
        print(error)
        return False
    else:
        if 'Item' not in response:
            return False
        return response['Item']


def insert_item(table_name, item):
    """Inserts the given item into in a table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(
        Item=item
    )

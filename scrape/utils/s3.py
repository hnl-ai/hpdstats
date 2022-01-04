# -*- coding: utf-8 -*-
"""The s3 utility module."""

import boto3
import botocore


def check_if_key_exists(bucket_name, key):
    """Checks if the given key exists in an s3 bucket."""
    s3_resource = boto3.resource('s3')
    try:
        s3_resource.Object(bucket_name, key).load()
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == "404":
            return False
    return True


def upload_file(bucket_name, key, file, content_type):
    """Uploads the given file into in an s3 bucket."""
    s3_resource = boto3.resource('s3')
    s3_bucket = s3_resource.Bucket(bucket_name)

    s3_bucket.put_object(
        Key=key, Body=file,
        ContentType=content_type,
        ACL='public-read'
    )

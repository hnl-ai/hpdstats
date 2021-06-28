import boto3
import botocore


def check_if_key_exists(bucket_name, key):
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket_name, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
    else:
        return True


def upload_file(bucket_name, key, file, content_type):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    bucket.put_object(
        Key=key, Body=file,
        ContentType=content_type,
        ACL='public-read'
    )

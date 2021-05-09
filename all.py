from boto3 import client
import boto3
import os

bucket="honolulupd-arrest-logs"

conn = client('s3')
s3 = boto3.resource('s3')
for key in conn.list_objects(Bucket=bucket)['Contents']:
    fileKey = key['Key']
    date = ('-'.join(fileKey.split('-')[0:3]))
    s3.Bucket(bucket).download_file(fileKey, date + '.pdf')
    os.system('python3 text.py ' + date)


from flask import Flask
from flask_caching import Cache
import boto3
import simplejson as json

from routes import *

app = Flask(__name__, static_url_path='/static')
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

app.register_blueprint(routes)


@cache.cached(timeout=3600, key_prefix='all_records')  # Cache for 1 hour
def get_all_records():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('honolulupd.org-records')

    response = table.scan()
    allRecords = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        allRecords.extend(response['Items'])

    return allRecords


@app.route('/data')
def data():
    return {
        "allRecords": get_all_records()
    }


@cache.cached(timeout=3600, key_prefix='all_archives')
def get_all_archives():
    bucket = "honolulupd-arrest-logs"
    conn = boto3.client('s3')
    keys = []
    for key in conn.list_objects(Bucket=bucket)['Contents']:
        keys.append(key['Key'])
    return keys


@app.route('/archives')
def archives():
    return {
        "archives": get_all_archives()
    }


if __name__ == "__main__":
    app.run()

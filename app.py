from flask import Flask, send_from_directory
from flask_caching import Cache
import boto3
import simplejson as json

from os.path import join

app = Flask(__name__, static_url_path='/static')
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route("/", defaults={'path': 'index.html'})
@app.route("/<path>")
def index(path):
    return send_from_directory(app.static_folder, path)

@app.route("/table", defaults={'path': 'index.html'})
@app.route("/table/<path>")
def table(path):
    return send_from_directory(join(app.static_folder, 'table'), path)

@app.route('/map', defaults={'path': 'index.html'})
@app.route("/map/<path>")
def map(path):
    return send_from_directory(join(app.static_folder, 'map'), path)

@app.route('/archive', defaults={'path': 'index.html'})
@app.route("/archive/<path>")
def archive(path):
    return send_from_directory(join(app.static_folder, 'archive'), path)

@cache.cached(timeout=3600, key_prefix='all_records') # Cache for 1 hour
def get_all_records():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('honolulupd.org-records')
    response = table.scan()
    return json.dumps(response.get('Items', []))

@app.route('/data')
def data():
    return {
    	"allRecords": get_all_records()
	}

@cache.cached(timeout=3600, key_prefix='all_archives')
def get_all_archives():
    bucket="honolulupd-arrest-logs"
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

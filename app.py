from flask import Flask, current_app
from flask_caching import Cache
import boto3
import simplejson as json

app = Flask(__name__, static_url_path='/public')
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/")
@app.route('/index.html')
def index():
    return current_app.send_static_file('index.html')

@app.route("/table")
def table():
    return current_app.send_static_file('table/table.html')

@app.route('/map')
def map():
    return current_app.send_static_file('map/map.html')

@app.route('/archive')
def archive():
    return current_app.send_static_file('archive/archive.html')

@app.route('/index.js')
def indexjs():
    return current_app.send_static_file('index.js')

@app.route('/table.js')
def tablejs():
    return current_app.send_static_file('table/table.js')

@app.route('/map.js')
def mapjs():
    return current_app.send_static_file('map/map.js')

@app.route('/map.css')
def mapcss():
    return current_app.send_static_file('map/map.css')


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

@cache.cached(timeout=3600, key_prefix='all_archives') #
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
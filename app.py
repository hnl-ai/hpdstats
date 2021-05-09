from flask import Flask, current_app
import boto3

app = Flask(__name__, static_url_path='/public')

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

@app.route('/data')
def data():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('honolulupd.org-records')
    response = table.scan()
    return {
    	"allRecords": response.get('Items', [])
	}



if __name__ == "__main__":
	app.run()
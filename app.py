from flask import Flask, request, Response, json
from influxdb import InfluxDBClient
import datetime

app = Flask(__name__)

db_name = 'sensors'
client = InfluxDBClient(host='db', port=8086)
client.create_database(db_name)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/api/v1/tempsensor', methods=['POST'])
def tempsensor_post():
    req_data = request.get_json()
    print(req_data)

    date = datetime.datetime.now().isoformat()

    point = [{
        "measurement": "tempSensor",
        "tags": {
            "room": "bedroom"
        },
        "time": date,
        "fields": {
            "temperature": req_data["temperature"],
            "humidity": req_data["humidity"],
            "dewPoint": req_data["dewPoint"]
        }
    }]

    client.switch_database(db_name)
    print(client.write_points(point))
    return "True"

@app.route('/api/v1/tempsensor', methods=['GET'])
def tempsensor_get():

    client.switch_database(db_name)
    results = client.query('SELECT * FROM "sensors"."autogen"."tempSensor" WHERE time > now() - 14d')
    points = list(results.get_points())
    return Response(json.dumps(points),  mimetype='application/json')
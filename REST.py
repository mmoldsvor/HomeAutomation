from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
import json


device_handler = None
sensor_handler = None
config_handler = None

app = Flask(__name__)
CORS(app)


@app.route('/DT/sensorData', methods=['POST'])
def sensor_data():
    """
    Request a touch event
    :return: 200 OK on success
    """
    json_data = json.loads(request.data)
    if 'event' in json_data:
        event = json_data['event']

        if event['eventType'] == 'touch':
            # Extract only the name of the sensor
            sensor_name = event['targetName'].split('/')[-1]
            sensor = sensor_handler.data.get(sensor_name)
            if sensor is not None:
                for identifier in sensor.connections:
                    device_handler.action(identifier)

    return jsonify({'result': 'success'})


@app.route('/devices/list', methods=['GET'])
def list_devices():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    device_handler.discover_devices()
    save_data()
    return jsonify({'devices': {identifier: device.info_dict() for identifier, device in device_handler.data.items()}})


@app.route('/device/<identifier>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def handle_device(identifier):
    device = device_handler.data.get(identifier)
    data = validate_json(request.data)

    if request.method == 'POST' or request.method == 'PUT':
        device_type = data.get('device_type', 'Device')
        name = data.get('name', 'Unnamed')

        if not device_handler.is_unique(identifier):
            if request.method == 'PUT':
                return result(device_handler.add_device(identifier, device_type, name), 200)
            else:
                return result(f'Identifier {identifier} is not a unique id.', 400)

        return result(device_handler.add_device(identifier, device_type, name), 201)

    elif request.method == 'GET' and device is not None:
        return result(device.info_dict(), 200)

    elif request.method == 'DELETE' and device is not None:
        return result(device_handler.remove_by_identifier(identifier), 200)

    elif request.method == 'PATCH' and device is not None:
        if 'name' in data:
            device.name = data['name']
        if 'device_type' in data:
            device_handler.change_device_type(identifier, data['device_type'])
        return result(device.info_dict(), 200)
    save_data()
    abort(404)


@app.route('/sensors/list', methods=['GET'])
def list_sensors():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    sensor_handler.discover_sensors()
    save_data()
    return jsonify({'devices': {identifier: sensor.info_dict() for identifier, sensor in sensor_handler.data.items()}})


@app.route('/sensor/<identifier>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def handle_sensor(identifier):
    sensor = sensor_handler.data.get(identifier)
    data = validate_json(request.data)

    if request.method == 'POST' or request.method == 'PUT':
        sensor_type = data.get('sensor_type', 'Sensor')
        name = data.get('name', 'Unnamed')

        if not sensor_handler.is_unique(identifier):
            if request.method == 'PUT':
                return result(sensor_handler.add_sensor(identifier, sensor_type, name), 200)
            else:
                return result(f'Identifier {identifier} is not a unique id.', 400)

        return result(sensor_handler.add_device(identifier, sensor_type, name), 201)

    elif request.method == 'GET' and sensor is not None:
        return result(sensor.info_dict(), 200)

    elif request.method == 'DELETE' and sensor is not None:
        return result(sensor_handler.remove_by_identifier(identifier), 200)

    elif request.method == 'PATCH' and sensor is not None:
        if 'name' in data:
            sensor.name = data['name']
        if 'sensor_type' in data:
            sensor_handler.change_sensor_type(identifier, data['sensor_type'])
        return result(sensor.info_dict(), 200)
    save_data()
    abort(404)


@app.route('/connect/<identifier>', methods=['POST', 'PUT'])
def connect(identifier):
    sensor = sensor_handler.data.get(identifier)

    data = validate_json(request.data)
    connections = data.get('devices', {})

    if sensor is not None:
        if request.method == 'POST':
            sensor_handler.connect(identifier, connections)
        elif request.method == 'PUT':
            sensor.connections = connections
        return result(sensor.info_dict(), 200)
    abort(404)


@app.route('/upload', methods=['PUT'])
def upload_configuration():
    data = validate_json(request.data)
    if 'sensors' in data:
        sensor_handler.data = data['sensors']
    if 'devices' in data:
        device_handler.data = data['devices']
    save_data()


@app.route('/device/<identifier>/<event>', methods=['POST'])
def device_event(identifier, event):
    if event == 'action':
        device_handler.action(identifier)
    return result('success', 200)


def validate_json(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}


def result(value, status_code):
    return jsonify({'result': value}), status_code


def save_data():
    config_handler.save_data(device_handler.data, sensor_handler.data)

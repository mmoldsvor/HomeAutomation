from flask import Flask, request, jsonify, abort
from flask_basicauth import BasicAuth

import json


device_handler = None
sensor_handler = None
config_handler = None

app = Flask(__name__)


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

    return response(('result', 'success'))


@app.route('/devices/list', methods=['GET'])
def list_devices():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    return jsonify({'devices': {identifier: device.info_dict() for identifier, device in device_handler.data.items()}})


@app.route('/device/<identifier>', methods=['GET', 'POST', 'DELETE'])
def get_device(identifier):
    """
    Returns all information regarding the specified device
    :param identifier: The identifier unique to the device
    :return: 200 OK - The information in a json format, on success
             else 404 NOT FOUND
    """

    if request.method == 'GET':
        device = device_handler.data.get(identifier)
        if device is not None:
            return jsonify(device.info_dict())
        else:
            abort(404)

    elif request.method == 'POST':
        try:
            data = json.loads(request.data)
        except json.JSONDecodeError:
            return response(('result', 'Data not provided, or invalid input'), status_code=400)

        # Checks if identifier already exists
        if not device_handler.is_unique(identifier):
            return response(('result', 'Identifier has to be unique'), status_code=400)

        # Checks if required data is available
        if 'device_type' not in data:
            return response(('result', '"device_type" parameter is missing'), status_code=400)

        device_type = data['device_type']
        name = device_type
        if 'name' in data:
            name = data['name']

        device_info = device_handler.add_device(identifier, device_type, name)
        if device_info is not None:
            config_handler.save_data(device_handler.data, sensor_handler.data)
            return jsonify(device_info), 201
        else:
            return response(('result', '"device_type" provided was not a valid Device class'), status_code=400)

    elif request.method == 'DELETE':
        for sensor in sensor_handler.data:
            sensor.remove_connection(identifier)
        device_info = device_handler.remove_by_identifier(identifier)
        if device_info is not None:
            config_handler.save_data(device_handler.data, sensor_handler.data)
            return jsonify(device_info)
        else:
            abort(404)


@app.route('/sensors/list', methods=['GET'])
def list_sensors():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    sensor_handler.discover_sensors()
    return jsonify({'sensors': {identifier: sensor.info_dict() for identifier, sensor in sensor_handler.data.items()}})


@app.route('/sensor/<identifier>', methods=['GET', 'POST', 'DELETE'])
def request_sensor(identifier):
    if request.method == 'GET':
        sensor = sensor_handler.data.get(identifier)
        if sensor is not None:
            return jsonify(sensor.info_dict())
        else:
            abort(404)

    elif request.method == 'POST':
        try:
            data = json.loads(request.data)
        except json.JSONDecodeError:
            return response(('result', 'Data not provided, or invalid input'), status_code=400)

        # Checks if identifier already exists
        if not sensor_handler.is_unique(identifier):
            return response(('result', 'Identifier has to be unique'), status_code=400)

        # Checks if required data is available
        if 'device_type' not in data:
            return response(('result', '"device_type" parameter is missing'), status_code=400)

        sensor_type = data['device_type']
        name = sensor_type
        if 'name' in data:
            name = data['name']

        sensor_info = sensor_handler.add_sensor(identifier, sensor_type, name)
        if sensor_info is not None:
            config_handler.save_data(device_handler.data, sensor_handler.data)
            return jsonify(sensor_info), 201
        else:
            return response(('result', '"class_name" provided was not a valid Sensor class'), status_code=400)

    elif request.method == 'DELETE':
        sensor_info = sensor_handler.remove_by_identifier(identifier)
        if sensor_info is not None:
            config_handler.save_data(device_handler.data, sensor_handler.data)
            return jsonify(sensor_info)
        else:
            abort(404)


@app.route('/sensor/pair/<identifier>', methods=['POST'])
def pair_sensor(identifier):
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return response(('result', 'Data not provided, or invalid input'), status_code=400)

    if 'device' not in data:
        return response(('result', 'Device identifier not specified'), status_code=400)

    sensor = sensor_handler.data.get(identifier)
    device = device_handler.data.get(data['device'])

    if sensor is not None and device is not None:
        sensor.connections.append(device)
        config_handler.save_data(device_handler.data, sensor_handler.data)
        return sensor.info_dict()
    abort(404)


@app.route('/device/<identifier>/<function>', methods=['POST'])
def device_request(identifier, function):
    if function == 'action':
        device_handler.action(identifier)

    return response(('result', 'success'))


def response(*args, status_code=200):
    return jsonify({key: value for (key, value) in args}), status_code

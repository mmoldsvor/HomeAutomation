from flask import Flask, request, jsonify, abort
from flask_basicauth import BasicAuth

import configparser
import json

device_handler = None
sensor_handler = None
telldus_interface = None

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('.config/config.ini')

app.config['BASIC_AUTH_USERNAME'] = config['basic_auth']['username']
app.config['BASIC_AUTH_PASSWORD'] = config['basic_auth']['password']
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


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
            sensor = sensor_handler.get_by_identifier(sensor_name)
            if sensor is not None:
                sensor.on_event(telldus_interface.request_action)

    return response(('result', 'success'))


@app.route('/devices/list', methods=['GET'])
def list_devices():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    return jsonify({'devices': {key: value for device in device_handler.data
                                for (key, value) in device.info_dict().items()}})


@app.route('/device/<identifier>', methods=['GET', 'POST'])
def request_device(identifier):
    """
    Returns all information regarding the specified device
    :param identifier: The identifier unique to the device
    :return: 200 OK - The information in a json format, on success
             else 404 NOT FOUND
    """
    if request.method == 'GET':
        device = device_handler.get_by_identifier(identifier)
        if device is not None:
            return jsonify(device.info_dict())
        else:
            abort(404)

    elif request.method == 'POST':
        device_type = request.args.get('class_name')
        name = request.args.get('name')
        device_info = device_handler.add_data(device_type, identifier, name)
        print(device_info)
        if device_info is not None:
            return device_info
        else:
            return response(('result', 'Not unique identifier, or missing parameters'), status_code=400)


@app.route('/sensors/list', methods=['GET'])
def list_sensors():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    return jsonify({'sensors': {key: value for sensor in sensor_handler.data
                                for (key, value) in sensor.info_dict().items()}})


@app.route('/sensor/<identifier>', methods=['GET', 'POST'])
def request_sensor(identifier):
    if request.method == 'GET':
        sensor = sensor_handler.get_by_identifier(identifier)
        if sensor is not None:
            return jsonify(sensor.info_dict())
        else:
            abort(404)

    elif request.method == 'POST':
        sensor_type = request.args.get('class_name')
        name = request.args.get('name')
        sensor_info = sensor_handler.add_data(sensor_type, identifier, name, [])
        if sensor_info is not None:
            return sensor_info
        else:
            return response(('result', 'Not unique identifier, or missing parameters'), status_code=400)


@app.route('/pair/<sensor_identifier>/<device_identifier>', methods=['POST'])
def pair_sensor(sensor_identifier, device_identifier):
    sensor = sensor_handler.get_by_identifier(sensor_identifier)
    device = device_handler.get_by_identifier(device_identifier)

    if sensor is not None and device is not None:
        sensor.connections.append(device)
        return sensor.info_dict()
    abort(404)


@app.route('/device/<identifier>/<function>', methods=['POST'])
def device_request(identifier, function):
    device = device_handler.get_by_identifier(identifier)

    if function == 'action':
        # Checks if the device.toggle_state exists and is callable
        if callable(getattr(device, "action", None)):
            device.action(telldus_interface.request_action)
        else:
            abort(404)

    return response(('result', 'success'))


def response(*args, status_code=200):
    return jsonify({key: value for (key, value) in args}), status_code

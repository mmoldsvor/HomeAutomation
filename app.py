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
            sensor = sensor_handler.get_by_identifier(event['targetName'])
            if sensor is not None:
                sensor.on_event(telldus_interface.request_action)

    return response(('result', 'success'))


@app.route('/devices/list', methods=['GET'])
def list_devices():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    print(device_handler.data)
    return jsonify({'devices':[device.info_dict() for device in device_handler.data]})


@app.route('/device/<identifier>', methods=['GET', 'POST'])
def get_device(identifier):
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
        raise NotImplemented


@app.route('/sensors/list', methods=['GET'])
def list_sensors():
    """
    Returns a list of all available devices on the network
    :return: 200 OK - List of all devices, on success
    """
    return jsonify({'sensors': [sensor.info_dict() for sensor in sensor_handler.data]})


@app.route('/sensor/<identifier>', methods=['GET, POST'])
def get_sensor(identifier):
    if request.method == 'GET':
        sensor = sensor_handler.get_by_identifier(identifier)
        if sensor is not None:
            return jsonify(sensor.info_dict())
        else:
            abort(404)

    elif request.method == 'POST':
        raise NotImplemented


@app.route('/device/<identifier>/<function>', methods=['POST'])
def update_device(identifier, function):
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

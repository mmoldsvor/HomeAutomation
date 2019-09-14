from flask import Flask, request, jsonify, abort
from flask_basicauth import BasicAuth

import configparser
import json

app = Flask(__name__)
main_handler = None

config = configparser.ConfigParser()
config.read('.config/config.ini')

app.config['BASIC_AUTH_USERNAME'] = config['basic_auth']['username']
app.config['BASIC_AUTH_PASSWORD'] = config['basic_auth']['password']
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


@app.route('/sensorData', methods=['POST'])
def interact_socket():
    main_handler.sensor_data(request.data)
    return response(('result', 'success'))


@app.route('/devices/list', methods=['GET'])
def list_devices():
    return jsonify(main_handler.list_devices())


@app.route('/device/<identifier>', methods=['GET', 'POST'])
def get_device(identifier):
    if request.method == 'GET':
        device_info = main_handler.get_device(identifier)
        if device_info is not None:
            return jsonify(device_info)
        else:
            abort(404)


@app.route('/device/<identifier>/<function>', methods=['POST'])
def update_device(identifier, function):
    device = main_handler.device_handler.get_by_identifier(identifier)

    if function == 'toggle':
        # Checks if the device.toggle_state exists and is callable
        if callable(getattr(device, "toggle_state", None)):
            device.toggle_state(main_handler.telldus_interface.request_action)
        else:
            abort(404)

    if function == 'addSensor':
        sensor_id = json.loads(request.data)['sensor_id']
        if device is not None and sensor_id is not None:
            device.sensors.append(sensor_id)
            return response(('result', 'created'), status_code=201)
        else:
            abort(404)

    return response(('result', 'success'))


def response(*args, status_code=200):
    return jsonify({key: value for (key, value) in args}), status_code

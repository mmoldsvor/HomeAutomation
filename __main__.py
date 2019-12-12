from home_controller import ConfigHandler, DeviceHandler, SensorHandler, DeviceRequest, DTSensorRequest
from home_communication import TelldusInterface

import sys

if __name__ == '__main__':
    required_config_params = {'telldus': ['public_key', 'private_key', 'token', 'secret'],
                              'basic_auth': ['username', 'password'],
                              'dt': ['project_id', 'service_account_email', 'key_id', 'key_secret']}

    if len(sys.argv) > 1:
        config_handler = ConfigHandler(required_config_params, sys.argv[1])
    else:
        config_handler = ConfigHandler(required_config_params, '.config')
    config_handler.validate()

    print('CONFIG CURRENTLY IN USE:')
    print(config_handler)

    device_data, sensor_data = config_handler.load_data()

    dt_requests = DTSensorRequest(project_id=config_handler.config['dt']['project_id'],
                                  service_account_email=config_handler.config['dt']['service_account_email'],
                                  service_account_key_id=config_handler.config['dt']['key_id'],
                                  service_account_key_secret=config_handler.config['dt']['key_secret'])
    dt_requests.request_access_token()
    sensor_request = DeviceRequest([dt_requests])

    device_request = DeviceRequest([])

    device_handler = DeviceHandler(device_data, device_request)
    sensor_handler = SensorHandler(sensor_data, sensor_request, device_handler)

    telldus_interface = TelldusInterface(public_key=config_handler.config['telldus']['public_key'],
                                         private_key=config_handler.config['telldus']['private_key'],
                                         token=config_handler.config['telldus']['token'],
                                         token_secret=config_handler.config['telldus']['secret'])

    sensor_handler.discover_sensors()

    import app as flask_app

    flask_app.device_handler = device_handler
    flask_app.sensor_handler = sensor_handler
    flask_app.telldus_interface = telldus_interface
    flask_app.config_handler = config_handler

    flask_app.app.run(host='0.0.0.0', port=80)

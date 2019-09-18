from home_controller import ConfigHandler, DeviceHandler, SensorHandler
from home_communication import TelldusInterface


if __name__ == '__main__':
    required_config_params = {'telldus': ['public_key', 'private_key', 'token', 'secret'],
                              'basic_auth': ['username', 'password']}

    config_handler = ConfigHandler('.config', required_config_params)
    config_handler.validate()

    device_data, sensor_data = config_handler.load_data()

    device_handler = DeviceHandler(device_data)
    sensor_handler = SensorHandler(sensor_data, device_handler)

    telldus_interface = TelldusInterface(public_key=config_handler.config['telldus']['public_key'],
                                         private_key=config_handler.config['telldus']['private_key'],
                                         token=config_handler.config['telldus']['token'],
                                         token_secret=config_handler.config['telldus']['secret'])

    import app as flask_app

    flask_app.device_handler = device_handler
    flask_app.sensor_handler = sensor_handler
    flask_app.telldus_interface = telldus_interface
    flask_app.config_handler = config_handler

    flask_app.app.run(host='0.0.0.0')

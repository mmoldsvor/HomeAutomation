from telldus_interface import TelldusInterface
from handlers import DeviceHandler, SensorHandler

import pickle
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('.config/config.ini')

    device_data = []
    sensor_data = []
    try:
        with open(r'data.pickle', 'rb') as input_file:
            device_data = pickle.load(input_file)
            sensor_data = pickle.load(input_file)
    except FileNotFoundError:
        with open(r'data.pickle', 'wb') as output_file:
            pickle.dump([], output_file)
            pickle.dump([], output_file)

    device_handler = DeviceHandler(device_data)
    sensor_handler = SensorHandler(sensor_data, device_handler)

    telldus_interface = TelldusInterface(public_key=config['telldus']['public_key'],
                                         private_key=config['telldus']['private_key'],
                                         token=config['telldus']['token'],
                                         token_secret=config['telldus']['secret'])

    import app as flask_app

    flask_app.device_handler = device_handler
    flask_app.sensor_handler = sensor_handler
    flask_app.telldus_interface = telldus_interface

    flask_app.app.run(host='0.0.0.0')


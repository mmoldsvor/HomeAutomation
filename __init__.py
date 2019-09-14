from telldus_interface import TelldusInterface
from device_handler import DeviceHandler
from main_handler import MainHandler

import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('.config/config.ini')
    logger = "test"

    device_handler = DeviceHandler()

    telldus_interface = TelldusInterface(public_key=config['telldus']['public_key'],
                                         private_key=config['telldus']['private_key'],
                                         token=config['telldus']['token'],
                                         token_secret=config['telldus']['secret'],
                                         logging=logger)

    main_handler = MainHandler(config, device_handler, telldus_interface)

    import app as flask_app
    flask_app.main_handler = main_handler
    flask_app.app.run(host='0.0.0.0')

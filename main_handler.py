import json


class MainHandler:
    def __init__(self, config, device_handler, telldus_interface):
        self.config = config
        self.device_handler = device_handler
        self.telldus_interface = telldus_interface

        self.sensor_dict = {key: value for (key, value) in device_handler.sensor_device_pair()}

    def sensor_data(self, data):
        json_data = json.loads(data)

        if 'event' in json_data:
            event = json_data['event']

            if event['eventType'] == 'touch':
                if event['targetName'] in self.sensor_dict:
                    device = self.sensor_dict[event['targetName']]
                    print(device)

                    device.toggle_state(self.telldus_interface.request_action)

    def get_device(self, identifier):
        device = self.device_handler.get_by_identifier(identifier)
        if device is not None:
            return {device.identifier: {'name': device.name, 'sensors': device.sensors}}
        return None

    def list_devices(self):
        return {'devices': {device.identifier: {'name': device.name, 'sensors': device.sensors}
                for device in self.device_handler.devices}}

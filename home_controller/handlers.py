from home_controller.devices import *
from home_controller.sensors import *
import home_controller.sensors as sensors_module
import home_controller.devices as devices_module


class Handler:
    def __init__(self, data, data_requests):
        """
        :param data: Dictionary of every device
        :param data_requests: Class for discovering new devices as they are added to external systems
        """
        self.data = data
        self.data_requests = data_requests
        self.classes = []

    def is_unique(self, identifier):
        """
        Checks whether the identifier is unique or not
        :param identifier: The identifier in question
        :return: bool - True if unique, False otherwise
        """
        if identifier in self.data.keys():
            return False
        return True

    def remove_by_identifier(self, identifier):
        """
        Removes an item given an identifier
        :param identifier: Unique identification of the item in which is being removed
        :return: Information about the removed device
        """
        if identifier in self.data.keys():
            return self.data.pop(identifier).info_dict()
        return None


class SensorHandler(Handler):
    def discover_sensors(self):
        devices = self.data_requests.request_data()
        for device_identifier in devices:
            if self.data.get(device_identifier) is None:
                self.data[device_identifier] = Sensor('Unnamed', 'Sensor')

    def add_sensor(self, identifier, device_type, name, connections=None):
        if connections is None:
            connections = []
        try:
            self.data[identifier] = getattr(sensors_module, device_type)(name, connections=connections)
            return self.data[identifier].info_dict()
        except AttributeError:
            print('Sensor type is not a valid type')
            return None

    def change_sensor_type(self, identifier, sensor_type):
        return self.add_sensor(identifier, sensor_type, self.data[identifier].name, self.data[identifier].connections)

    def connect(self, identifier, devices):
        sensor = self.data[identifier]
        for device in devices:
            if device not in sensor.connections:
                sensor.connections.append(device)


class DeviceHandler(Handler):
    def __init__(self, data, data_requests, device_interfaces):
        super().__init__(data, data_requests)
        self.device_interfaces = device_interfaces

    def discover_devices(self):
        devices = self.data_requests.request_data()
        for device_identifier in devices:
            if self.data.get(device_identifier) is None:
                self.data[device_identifier] = Device('Unnamed', 'Device')

    def add_device(self, identifier, device_type, name):
        try:
            self.data[identifier] = getattr(devices_module, device_type)(name)
            return self.data[identifier].info_dict()
        except AttributeError:
            print('Device type is not a valid type')
            return None

    def change_device_type(self, identifier, device_type):
        return self.add_device(identifier, device_type, self.data[identifier].name)

    def action(self, identifier):
        self.data[identifier].action(identifier, self.device_interfaces)

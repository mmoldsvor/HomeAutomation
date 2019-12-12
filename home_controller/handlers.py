from home_controller.devices import *
from home_controller.sensors import *


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
        if identifier in [item.identifier for item in self.data]:
            return False
        return True

    def get_by_identifier(self, identifier):
        """
        Gets the data by passing only the identifier
        :param identifier: The identifier of the requested object
        :return: Sensor or Device depending on subclass
        """
        identifiers = [item.identifier for item in self.data]
        if identifier in identifiers:
            return self.data[identifiers.index(identifier)]
        return None

    def remove_by_identifier(self, identifier):
        """
        Removes an item given an identifier
        :param identifier: Unique identification of the item in which is being removed
        :return: Information about the removed device
        """
        identifiers = [item.identifier for item in self.data]
        if identifier in identifiers:
            return self.data.pop(identifiers.index(identifier)).info_dict()
        return None

    def add_data(self, class_name, identifier, name, *args):
        """
        Appends a sensor to the Handler data list
        :param class_name: str - The name of the Class or Subclass of which will be added
        :param identifier: str - Unique identification
        :param name: str -
        :param args: The rest of the data added to the Sensor
        :return: Information about the newly added data if successful, None otherwise
        """
        class_names = [cls.__name__ for cls in self.classes]

        if class_name in class_names:
            data_class = self.classes[class_names.index(class_name)]

            self.data.append(data_class(identifier, name, *args))
            return self.data[-1].info_dict()
        return None


class SensorHandler(Handler):
    def __init__(self, data, sensor_requests, device_handler):
        self.device_handler = device_handler
        super().__init__(data, sensor_requests)

        # All possible Class/Subclasses added to handler
        self.classes = [cls for cls in Sensor.__subclasses__()] + [Sensor]

    def discover_sensors(self):
        devices = self.data_requests.request_data()
        for device_identifier in devices:
            if self.get_by_identifier(device_identifier) is None:
                self.data.append(Sensor(device_identifier, 'Unnamed', []))


class DeviceHandler(Handler):
    def __init__(self, data, device_requests):
        super().__init__(data, device_requests)

        # All possible Class/Subclasses added to handler
        self.classes = [cls for cls in Device.__subclasses__()] + [Device]

    def discover_devices(self):
        devices = self.data_requests.request_data()
        for device_identifier in devices:
            if self.get_by_identifier(device_identifier) is None:
                self.data.append(Device(device_identifier, 'Unnamed'))

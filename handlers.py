from devices import Device, TelldusSocket, TelldusDimmer
from sensors import Sensor


class Handler:
    def __init__(self, data):
        self.data = data
        self.classes = []

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

        # Checks if identifier already exists
        if identifier in [sensor.identifier for sensor in self.data]:
            return None

        class_names = [cls.__name__ for cls in self.classes]

        print(class_names)

        if class_name in class_names:
            data_class = self.classes[class_names.index(class_name)]

            self.data.append(data_class(identifier, name, *args))
            print(self.data[-1])
            return self.data[-1].info_dict()
        return None


class SensorHandler(Handler):
    def __init__(self, data, device_handler):
        self.device_handler = device_handler
        super().__init__(data)

        # All possible Class/Subclasses added to handler
        self.classes = [cls for cls in Sensor.__subclasses__()] + [Sensor]


class DeviceHandler(Handler):
    def __init__(self, data):
        super().__init__(data)

        # All possible Class/Subclasses added to handler
        self.classes = [cls for cls in Device.__subclasses__()] + [Device]

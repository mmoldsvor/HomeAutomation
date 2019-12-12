class Sensor:
    def __init__(self, name, sensor_type='Sensor', connections=None):
        """
        The parent Sensor class
        Does also work as a generic sensor
        :param name: Name of the sensor
        :param connections: A list of all device identifiers connected to the sensor
        """
        if connections is None:
            connections = []

        self.name = name
        self.sensor_type = sensor_type
        self.connections = connections

    def info_dict(self):
        """
        Creates a json-friendly representation of the device
        :return:
        """
        return {'sensor_name': self.name,
                'sensor_type': self.sensor_type,
                'devices': self.connections}

    def remove_connection(self, identifier):
        """
        Removes element of given identifier
        :param identifier: The unique identifier in which is being removed
        :return: Information about the removed device
        """
        identifiers = [device.identifier for device in self.connections]
        if identifier in identifiers:
            return self.connections.pop(identifiers.index(identifier)).info_dict()
        return None

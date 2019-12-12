class Sensor:
    def __init__(self, identifier, name, connections, sensor_type='Sensor'):
        """
        The parent Sensor class
        Does also work as a generic sensor
        :param identifier: Unique identification for each sensor
        :param name: Name of the sensor
        :param connections: A list of all device identifiers connected to the sensor
        """
        self.identifier = identifier
        self.name = name
        self.connections = connections
        self.sensor_type = sensor_type

    def on_event(self, func):
        """
        Perform action on event
        :param func: The function used to send the request (Telldus or Z-wave)
        """
        for connection in self.connections:
            connection.action(func)

    def info_dict(self):
        """
        Creates a json-friendly representation of the device
        :return:
        """
        return {self.identifier: {'sensor_name': self.name,
                                  'sensor_type': self.sensor_type,
                                  'devices': {key: value for device in self.connections
                                              for (key, value) in device.info_dict().items() if device is not None}}}

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


class DisruptiveTemp(Sensor):
    def __init__(self, identifier, name, connections, temp=0):
        super().__init__(identifier, name, connections)
        self.temp = temp

    def on_event(self, func):
        for connection in self.connections:
            raise NotImplemented

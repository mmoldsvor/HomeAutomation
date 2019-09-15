class Sensor:
    def __init__(self, identifier, name, connections):
        self.identifier = identifier
        self.name = name
        self.connections = connections

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
                                  'devices': {key: value for device in self.connections
                                              for (key, value) in device.info_dict().items() if device is not None}}}


class DisruptiveTemp(Sensor):
    def __init__(self, identifier, name, connections, temp=0):
        super().__init__(identifier, name, connections)
        self.temp = temp

    def on_event(self, func):
        for connection in self.connections:
            raise NotImplemented

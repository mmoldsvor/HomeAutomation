class Sensor:
    def __init__(self, identifier, name, connections):
        self.identifier = identifier
        self.name = name
        self.connections = connections

    def on_event(self, func):
        raise NotImplemented

    def info_dict(self):
        """
        Creates a json-friendly representation of the device
        :return:
        """
        return {self.identifier: {'name': self.name, 'devices': {device.identifier: device.name for device in self.connections}}}


class DisruptiveTouch(Sensor):
    def __init__(self, identifier, name, connections):
        super().__init__(identifier, name, connections)

    def on_event(self, func):
        for connection in self.connections:
            connection.action(func)


class DisruptiveTemp(Sensor):
    def __init__(self, identifier, name, connections, temp):
        super().__init__(identifier, name, connections)
        self.temp = temp

    def on_event(self, func):
        for connection in self.connections:
            raise NotImplemented

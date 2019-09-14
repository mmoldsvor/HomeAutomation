class Device:
    def __init__(self, identifier, name, sensors):
        """
        :param identifier: str: An unique identifier for the specific device
        :param name: str: Display name of the device
        :param sensors: tuple: All sensors connected to the device
        """
        self.identifier = identifier
        self.name = name
        self.sensors = sensors


class Socket(Device):
    def __init__(self, identifier, name, sensors, socket_type, state):
        super().__init__(identifier, name, sensors)
        self.socket_type = socket_type
        self.state = state

    def toggle_state(self, func):
        if self.state is True:
            self.state = False
            self.turn_off(func)
        else:
            self.state = True
            self.turn_on(func)

    def turn_on(self, func):
        func('device/turnOn', f'id={self.identifier}')

    def turn_off(self, func):
        func('device/turnOff', f'id={self.identifier}')


class Sensor:
    def __init__(self, identifier):
        self.identifier = identifier


class DeviceHandler:
    def __init__(self):
        self.devices = self.request_devices()

    def request_devices(self):
        return [Socket('5049830', 'Stue Lys', ['projects/blpso805uuabl6lgd3cg/devices/bja0082e27fg00a7fing',
                                               'projects/blpso805uuabl6lgd3cg/devices/bja00677cdlg00ba0epg'], 'socket_type', 0),
                Socket('5049845', 'Test', ['projects/blpso805uuabl6lgd3cg/devices/bja0abj1or1g00e49m7g',], 'socket_type', 0)]

    def get_by_identifier(self, identifier):
        identifiers = [device.identifier for device in self.devices]
        if identifier in identifiers:
            return self.devices[identifiers.index(identifier)]
        return None

    def sensor_device_pair(self):
        """
        Creates a pair with the corresponding device for each sensor, and puts it in a list
        :return: list[str, Device]
        """
        return [(sensor, device) for device in self.devices for sensor in device.sensors]



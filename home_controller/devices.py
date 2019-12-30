class Device:
    def __init__(self, name, device_type='Device'):
        """
        The parent class of all devices
        :param name: str: Display name of the device
        :param device_type:
        """
        self.name = name
        self.device_type = device_type

    def action(self, identifier, device_interfaces):
        """
        The action being executed when some specified criteria has been reached, or a POST request has been received
        :param identifier:
        :param device_interfaces: List of all interfaces communicating with external API's
        """
        print('Device class does not support any device interfaces')

    def info_dict(self):
        """
        Creates a json-friendly representation of the device
        :return:
        """
        return {'device_name': self.name,
                'device_type': self.device_type}


class HueBulbColor(Device):
    def action(self, identifier, device_interfaces):
        device_interfaces['hue'].request_action(identifier)


class TelldusSocket(Device):
    def __init__(self, name, device_type='TelldusSocket', state=False):
        """
        :param state: bool - The state of the outlet, on or off
        """
        super().__init__(name, device_type)
        self.state = state

    def action(self, identifier, device_interfaces):
        interface = device_interfaces['telldus']
        if self.state is True:
            self.state = False
            self.turn_off(identifier, interface.request_action)
        else:
            self.state = True
            self.turn_on(identifier, interface.request_action)

    @staticmethod
    def turn_on(identifier, func):
        func('device/turnOn', f'id={identifier}')

    @staticmethod
    def turn_off(identifier, func):
        func('device/turnOff', f'id={identifier}')

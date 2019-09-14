class Device:
    def __init__(self, identifier, name):
        """
        The parent class of all devices
        :param identifier: str: An unique identifier for the specific device
        :param name: str: Display name of the device
        """
        self.identifier = identifier
        self.name = name

    def action(self, func):
        """
        The action being executed when some specified criteria has been reached, or a POST request has been received
        :param func: The function that is being executed when the criteria has been reached
        """
        raise NotImplemented

    def info_dict(self):
        """
        Creates a json-friendly representation of the device
        :return:
        """
        return {self.identifier: {'name': self.name}}


class TelldusSocket(Device):
    def __init__(self, identifier, name, state):
        super().__init__(identifier, name)
        self.state = state

    def action(self, func):
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



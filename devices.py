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
        return {self.identifier: {'device_name': self.name}}


class TelldusSocket(Device):
    def __init__(self, identifier, name, state):
        """
        :param state: bool - The state of the outlet, on or off
        """
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


class TelldusDimmer(Device):
    def __init__(self, identifier, name, value, direction):
        """
        :param value: int - A value between 0 and 255
        :param direction: int - 0: Next action will value to 255
                                1: Next action will slowly dim downwards
                                2: Next action will stop dimming
                                3: Next action will value to 0
        """
        super().__init__(identifier, name)
        self.value = value
        self.direction = direction

    def action(self, func):
        print(self.direction)
        if self.direction == 0:
            self.value = 255
            func('device/dim', f'id={self.identifier}&level={self.value}')
        elif self.direction == 1:
            raise NotImplemented
        elif self.direction == 2:
            raise NotImplemented
        elif self.direction == 3:
            self.value = 0
            func('device/dim', f'id={self.identifier}&level={self.value}')
        self.direction = self.direction + 1 if self.direction <= 3 else 0



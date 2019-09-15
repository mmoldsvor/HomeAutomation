from devices import TelldusSocket, TelldusDimmer
from sensors import DisruptiveTouch


class Handler:
    def __init__(self):
        self.data = self.request_data()

    def request_data(self):
        raise NotImplemented

    def get_by_identifier(self, identifier):
        identifiers = [item.identifier for item in self.data]
        if identifier in identifiers:
            return self.data[identifiers.index(identifier)]
        return None


class SensorHandler(Handler):
    def __init__(self, device_handler):
        self.device_handler = device_handler
        super().__init__()

    def request_data(self):
        return [DisruptiveTouch('bja0082e27fg00a7fing', 'Stue Vest',
                                [self.device_handler.get_by_identifier('5049852')]),
                DisruptiveTouch('bja00677cdlg00ba0epg', 'Stue Øst',
                                [self.device_handler.get_by_identifier('5049852')]),
                DisruptiveTouch('bja0abj1or1g00e49m7g', 'Lampe',
                                [self.device_handler.get_by_identifier('5049845')])]


class DeviceHandler(Handler):
    def request_data(self):
        return [TelldusDimmer('5049852', 'Stue Lys', 0, 0),
                TelldusSocket('5049845', 'Test', False)]
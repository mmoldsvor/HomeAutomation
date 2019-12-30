import json

import requests


class HueInterface:
    def __init__(self, ip_address, user_key):
        self.ip_address = ip_address
        self.user_key = user_key

    def request_action(self, identifier):
        current_state = requests.get(url=f'http://{self.ip_address}/api/{self.user_key}/lights/{identifier}').json()
        data = json.dumps({'on': not bool(current_state['state']['on'])})

        response = requests.put(url=f'http://{self.ip_address}/api/{self.user_key}/lights/{identifier}/state', data=data)
        return response.json()

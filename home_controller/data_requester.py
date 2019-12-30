import requests
import time
import jwt


class DeviceRequest:
    def __init__(self, data_requests):
        """
        Collection of all device requests
        :param data_requests: List of classes containing method request_devices
        """
        self.data_requests = data_requests

    def request_data(self):
        return [device for data_requester in self.data_requests for device in data_requester.request_devices()]


class HueRequest:
    def __init__(self, ip_address, user_key):
        self.ip_address = ip_address
        self.user_key = user_key

    def request_devices(self):
        project = requests.get(f'http://{self.ip_address}/api/{self.user_key}/lights').json()
        return [device for device in project]


class DTSensorRequest:
    def __init__(self, project_id, service_account_email, service_account_key_id, service_account_key_secret,
                 base_url='https://api.disruptive-technologies.com/v2'):
        self.base_url = base_url
        self.project_id = project_id
        self.service_account_email = service_account_email
        self.service_account_key_id = service_account_key_id
        self.service_account_key_secret = service_account_key_secret

        self.access_token = ''
        self.access_token_timestamp = None
        self.access_token_active = 3600

    def request_access_token(self, time_active=3600):
        """
        Request JWT access token
        :param time_active: number - how long the token should be active for, maximum 1 hour
        """
        if time_active > 3600:
            time_active = 3600

        auth_endpoint = 'https://identity.disruptive-technologies.com/oauth2/token'
        creation_timestamp = round(time.time())
        header = {
            'kid': self.service_account_key_id
        }

        payload = {
            'iat': creation_timestamp,
            'exp': creation_timestamp + time_active,
            'aud': auth_endpoint,
            'iss': self.service_account_email
        }

        jwt_encoded = jwt.encode(payload=payload,
                                 key=self.service_account_key_secret,
                                 algorithm='HS256',
                                 headers=header)

        response = requests.post(auth_endpoint,
                                 data={
                                     'assertion': jwt_encoded,
                                     'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer'
                                 }).json()

        self.access_token = response['access_token']
        self.access_token_timestamp = creation_timestamp
        self.access_token_active = time_active

    def request_devices(self, device_types='touch'):
        """
        Gets all device identifiers available
        :param device_types:
        :return:
        """
        if self.access_token == '' or self.access_token_timestamp is None or \
           self.access_token_timestamp + self.access_token_active > round(time.time()):
            self.request_access_token()

        url = f'{self.base_url}/projects/{self.project_id}/devices'
        project = requests.get(url, params={'device_types': device_types, 'token': self.access_token}).json()

        return [device['name'].split('/')[-1] for device in project['devices']]

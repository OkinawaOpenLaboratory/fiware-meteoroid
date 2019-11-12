import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class OrionSubscriptionClient:
    def __init__(self):
        self.host = os.environ.get('FIWARE_ORION_HOST', '')
        self.endpoint = f'http://{self.host}/v2/subscriptions'
        self.headers = {
            'User-Agent': 'fiware-meteoroid/0.1'
        }

    def set_headers(self, fiware_service, fiware_service_path):
        self.headers['Fiware-Service'] = fiware_service
        self.headers['Fiware-ServicePath'] = fiware_service_path

    def list_subscriptions(self, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        response = requests.get(url=self.endpoint,
                                headers=self.headers,
                                verify=False)
        return response

    def retrieve_subscription(self, subscription_id, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        response = requests.get(url=f'{self.endpoint}/{subscription_id}',
                                headers=self.headers,
                                verify=False)
        return response

    def create_subscription(self, data, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        headers = self.headers.copy()
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url=self.endpoint,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False)
        return response

    def delete_subscription(self, subscription_id, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        response = requests.delete(url=f'{self.endpoint}/{subscription_id}',
                                   headers=self.headers,
                                   verify=False)
        return response

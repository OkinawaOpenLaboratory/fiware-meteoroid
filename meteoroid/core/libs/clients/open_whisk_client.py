import requests
import os
import json
from rest_framework.exceptions import APIException


class OpenWhiskClientException(APIException):
    pass


class OpenWhiskClient:
    def __init__(self):
        self.user = os.environ.get('OPEN_WHISK_USER', '')
        self.password = os.environ.get('OPEN_WHISK_PASSWORD', '')
        self.host = os.environ.get('OPEN_WHISK_HOST', '')
        self.endpoint = f'https://{self.host}'
        self.headers = {
            'User-Agent': 'fiware-meteoroid/0.1'
        }

    def exception_handler(self, response):
        if response.status_code != 200:
            raise OpenWhiskClientException(detail=response.text,
                                           code=response.status_code)

    def list_action(self, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/actions',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response.json()

    def retrieve_action(self, action_name, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response.json()

    def create_action(self, namespace, data):
        self.headers['Content-Type'] = 'application/json'
        action_name = data['name']
        response = requests.put(f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}',
                                headers=self.headers,
                                data=json.dumps(data),
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response.json()

    def update_action(self, namespace, data):
        self.headers['Content-Type'] = 'application/json'
        action_name = data['name']
        response = requests.put(f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}?overwrite=true',
                                headers=self.headers,
                                data=json.dumps(data),
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response.json()

    def delete_action(self, action_name, namespace):
        response = requests.delete(f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}',
                                   headers=self.headers,
                                   auth=(self.user, self.password),
                                   verify=False)
        self.exception_handler(response)
        return response.json()

import requests
import os


class OpenWhiskClient:
    def __init__(self):
        self.user = os.environ.get('OPEN_WHISK_USER', '')
        self.password = os.environ.get('OPEN_WHISK_PASSWORD', '')
        self.host = os.environ.get('OPEN_WHISK_HOST', '')
        self.endpoint = f'https://{self.host}'
        self.headers = {
            'User-Agent': 'fiware-meteoroid/0.1'
        }

    def get_function_list(self, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/actions',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        return response.json()

    def get_function(self, function_id, namespace):
        pass

    def create_or_update_function(self, namespace, data):
        pass

    def delete_function(self, function_id, namespace):
        pass

    def list_activation(self, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/activations',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        return response.json()

    def retrieve_activation(self, activation_id, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/activations/{activation_id}',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        return response.json()

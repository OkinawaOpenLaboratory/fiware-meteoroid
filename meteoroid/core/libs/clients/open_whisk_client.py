import requests
import os


class OpenWhiskClient:
    def __init__(self):
        self.api_key = os.environ.get('OPEN_WHISK_API_KEY', '')
        self.host = os.environ.get('OPEN_WHISK_HOST', '')
        self.endpoint = f'https://{self.host}'
        self.headers = {
            'Authorization': f'Basic {self.api_key}',
            'User-Agent': 'fiware-meteoroid/0.1'
        }

    def get_function_list(self, namespace):
        response = requests.get('{self.endpoint}/api/v1/namespaces/_/actions', headers=self.headers, verify=False)
        return response.json()

    def get_function(self, function_id, namespace):
        pass

    def create_or_update_function(self, namespace, data):
        pass

    def delete_function(self, function_id, namespace):
        pass

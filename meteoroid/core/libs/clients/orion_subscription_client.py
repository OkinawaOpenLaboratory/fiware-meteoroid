import json
import logging
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from rest_framework.exceptions import APIException

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)


class OrionSubscriptionClientException(APIException):
    pass


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

    def exception_handler(self, response):
        if 200 > response.status_code or response.status_code >= 300:
            logger.error(f'status code: {response.status_code}, detail: {response.text}')
            raise OrionSubscriptionClientException(detail=response.text,
                                                   code=response.status_code)
        else:
            logger.info(f'status code: {response.status_code}, detail: {response.text}')

    def list_subscriptions(self, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        response = requests.get(url=self.endpoint,
                                headers=self.headers,
                                verify=False)
        self.exception_handler(response)
        return response

    def retrieve_subscription(self, subscription_id, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        response = requests.get(url=f'{self.endpoint}/{subscription_id}',
                                headers=self.headers,
                                verify=False)
        self.exception_handler(response)
        return response

    def create_subscription(self, data, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        headers = self.headers.copy()
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url=self.endpoint,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False)
        self.exception_handler(response)
        return response

    def delete_subscription(self, subscription_id, fiware_service='', fiware_service_path='/'):
        self.set_headers(fiware_service, fiware_service_path)
        response = requests.delete(url=f'{self.endpoint}/{subscription_id}',
                                   headers=self.headers,
                                   verify=False)
        self.exception_handler(response)
        return response

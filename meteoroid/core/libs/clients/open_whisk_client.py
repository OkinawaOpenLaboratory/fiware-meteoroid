import json
import logging
import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from rest_framework.exceptions import APIException


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)


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
        self.api_query_param = f'accesstoken=DUMMY+TOKEN&spaceguid={self.user}'

    def exception_handler(self, response):
        if response.status_code != 200:
            logger.error(f'status code: {response.status_code}, detail: {response.text}')
            raise OpenWhiskClientException(detail=response.text,
                                           code=response.status_code)
        else:
            logger.info(f'status code: {response.status_code}, detail: {response.text}')

    def list_action(self, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/actions',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response.json()

    def retrieve_action(self, action_name, namespace, code=False):
        code = 'true' if code else 'false'
        response = requests.get(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}?code={code}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def create_action(self, namespace, data):
        self.headers['Content-Type'] = 'application/json'
        action_name = data['name']
        response = requests.put(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}',
            headers=self.headers,
            data=json.dumps(data),
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def update_action(self, action_name, namespace, data):
        self.headers['Content-Type'] = 'application/json'
        response = requests.put(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}?overwrite=true',
            headers=self.headers,
            data=json.dumps(data),
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def delete_action(self, action_name, namespace):
        response = requests.delete(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/actions/{action_name}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def list_api(self, namespace):
        response = requests.get(
            f'{self.endpoint}/api/v1/web/whisk.system/apimgmt/getApi.http?{self.api_query_param}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def retrieve_api(self, api_name, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/web/whisk.system/apimgmt/getApi.http?' +
                                f'{self.api_query_param}&basepath={api_name}',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response.json()

    def create_api(self, namespace, data):
        action_name = data['apidoc']['action']['name']
        backend_url = f'https://{self.host}/api/v1/web/{namespace}/default/{action_name}.http'
        data['apidoc']['action']['backendUrl'] = backend_url
        data['apidoc']['action']['authkey'] = f'{self.user}:{self.password}'
        self.headers['Content-Type'] = 'application/json'
        response = requests.post(
            f'{self.endpoint}/api/v1/web/whisk.system/apimgmt/createApi.http?' +
            f'{self.api_query_param}',
            headers=self.headers,
            data=json.dumps(data),
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def delete_api(self, api_name, namespace):
        response = requests.delete(
            f'{self.endpoint}/api/v1/web/whisk.system/apimgmt/deleteApi.http?' +
            f'{self.api_query_param}&basepath={api_name}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def list_activation(self, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/activations',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response.json()

    def retrieve_activation(self, activation_id, namespace):
        response = requests.get(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/activations/{activation_id}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def retrieve_activation_logs(self, activation_id, namespace):
        response = requests.get(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/activations/{activation_id}/logs',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response.json()

    def list_trigger(self, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/triggers',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response

    def create_trigger(self, namespace, data):
        self.headers['Content-Type'] = 'application/json'
        trigger_name = data.get('name')
        response = requests.put(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/triggers/{trigger_name}',
            headers=self.headers,
            data=json.dumps(data),
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response

    def retrieve_trigger(self, trigger_name, namespace):
        response = requests.get(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/triggers/{trigger_name}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response

    def delete_trigger(self, trigger_name, namespace):
        response = requests.delete(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/triggers/{trigger_name}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response

    def list_rule(self, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/rules',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response

    def create_rule(self, namespace, data):
        self.headers['Content-Type'] = 'application/json'
        rule_name = data.get('name')
        response = requests.put(f'{self.endpoint}/api/v1/namespaces/{namespace}/rules/{rule_name}',
                                headers=self.headers,
                                data=json.dumps(data),
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response

    def retrieve_rule(self, rule_name, namespace):
        response = requests.get(f'{self.endpoint}/api/v1/namespaces/{namespace}/rules/{rule_name}',
                                headers=self.headers,
                                auth=(self.user, self.password),
                                verify=False)
        self.exception_handler(response)
        return response

    def delete_rule(self, rule_name, namespace):
        response = requests.delete(
            f'{self.endpoint}/api/v1/namespaces/{namespace}/rules/{rule_name}',
            headers=self.headers,
            auth=(
                self.user,
                self.password),
            verify=False)
        self.exception_handler(response)
        return response

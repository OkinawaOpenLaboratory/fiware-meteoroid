import os
from abc import ABCMeta, abstractmethod
from .clients.open_whisk_client import OpenWhiskClient
from ..models import Function, Endpoint


class FaaSDriver(metaclass=ABCMeta):
    __instance = None
    @classmethod
    def get_faas_driver(cls):
        faas_name = os.environ.get('FAAS_NAME', 'open_whisk')
        if not cls.__instance:
            if faas_name == 'open_whisk':
                cls.__instance = OpenWhiskDriver()
        return cls.__instance

    @abstractmethod
    def list_function(self, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_function(self, function, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def create_function(self, fiware_service, fiware_service_path, data):
        raise NotImplementedError()

    @abstractmethod
    def update_function(self, function, fiware_service, fiware_service_path, data):
        raise NotImplementedError()

    @abstractmethod
    def delete_function(self, function, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def list_endpoint(self, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_endpoint(self, endpoint, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def create_endpoint(self, fiware_service, fiware_service_path, data):
        raise NotImplementedError()

    @abstractmethod
    def delete_endpoint(self, endpoint, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def list_result(self, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_result(self, result_id, fiware_service, fiware_service_path):
        raise NotImplementedError()


class OpenWhiskDriver(FaaSDriver):
    def escape_fiware_service_path(self, fiware_service_path):
        ESCAPE_TARGET_STR = '/'
        ESCAPE_NEW_STR = '_'
        return fiware_service_path.replace(ESCAPE_TARGET_STR, ESCAPE_NEW_STR)

    def __build_action_request_parameter(self, namespace, data):
        request_parameter = {
            'namespace': namespace,
            'name': data['name'],
            'exec': {
                'kind': data['language'],
                'code': data['code']
            },
            'annotations': [{'key': 'web-export',
                             'value': True}]
        }
        if 'parameters' in data:
            request_parameter['parameters'] = data['parameters']
        if 'binary' in data:
            request_parameter['exec']['binary'] = data['binary']
        return request_parameter

    def __build_api_request_parameter(self, namespace, data):
        base_path = data['name']
        function = Function.objects.get(pk=data['function'])
        request_parameter = {
            'apidoc': {
                'namespace': namespace,
                'gatewayBasePath': base_path,
                'gatewayPath': data['path'],
                'gatewayMethod': data['method'],
                'id': f'API:{namespace}:{base_path}',
                'action': {
                    'name': function.name,
                    'namespace': namespace,
                    'backendMethod': data['method'],
                }
            }
        }
        return request_parameter

    def __build_all_endpoint_list_response(self, api_list):
        endpoint_list = []
        for api in api_list['apis']:
            endpoint = self.__build_endpoint_list_response(api['value'])
            endpoint_list.extend(endpoint)
        return endpoint_list

    def __build_endpoint_list_response(self, api):
        doc = api['apidoc']
        gw_api_url = api['gwApiUrl']
        endpoint_list = []
        for path, path_value in doc['paths'].items():
            for method, method_value in path_value.items():
                action_name = method_value['x-openwhisk']['action']

                endpoint = {
                    'name': doc['basePath'],
                    'path': path,
                    'method': method,
                    'action_name': action_name,
                    'url': f'{gw_api_url}{path}'
                }
                endpoint_list.append(endpoint)
        return endpoint_list

    def list_function(self, fiware_service, fiware_service_path):
        function_list = []
        action_list = OpenWhiskClient().list_action('guest')
        for action in action_list:
            language = ''
            for annotation in action['annotations']:
                if annotation['key'] == 'exec':
                    language = annotation['value']
            function = {
                'namespace': f'{fiware_service}{fiware_service_path}',
                'name': action['name'],
                'language': language,
                'binary': action['exec']['binary'],
                'version': action['version']
            }
            function_list.append(function)
        return function_list

    def retrieve_function(self, function, fiware_service, fiware_service_path, code=False):
        action = OpenWhiskClient().retrieve_action(function.name, 'guest', code=code)
        function = {
            'namespace': f'{fiware_service}{fiware_service_path}',
            'name': action['name'],
            'language': action['exec']['kind'],
            'binary': action['exec']['binary'],
            'version': action['version'],
            'parameters': action['parameters']
        }
        if code:
            function['code'] = action['exec']['code']
        return function

    def create_function(self, fiware_service, fiware_service_path, data):
        response = OpenWhiskClient().create_action('guest',
                                                   self.__build_action_request_parameter('guest', data))
        response['code'] = data['code']
        response['language'] = data['language']
        response['binary'] = data['binary']
        return response

    def update_function(self, function, fiware_service, fiware_service_path, data):
        response = OpenWhiskClient().update_action('guest',
                                                   self.__build_action_request_parameter('guest', data))
        response['code'] = data['code']
        response['language'] = data['language']
        response['binary'] = data['binary']
        return response

    def delete_function(self, function, fiware_service, fiware_service_path):
        return OpenWhiskClient().delete_action(function.name, 'guest')

    def list_endpoint(self, fiware_service, fiware_service_path):
        api_list = OpenWhiskClient().list_api('guest')
        return self.__build_all_endpoint_list_response(api_list)

    def retrieve_endpoint(self, endpoint, fiware_service, fiware_service_path):
        api_list = OpenWhiskClient().list_api('guest')
        for endpoint_data in self.__build_all_endpoint_list_response(api_list):
            if endpoint.equals_faas_data(endpoint_data):
                return endpoint_data
        return {}

    def create_endpoint(self, fiware_service, fiware_service_path, data):
        api = OpenWhiskClient().create_api('guest',
                                           self.__build_api_request_parameter('guest', data))
        function = Function.objects.filter(fiware_service=fiware_service,
                                           fiware_service_path=fiware_service_path).get(pk=data['function'])
        for endpoint_data in self.__build_endpoint_list_response(api):
            if endpoint_data['name'] == data['name'] and\
                    endpoint_data['path'] == data['path'] and\
                    endpoint_data['method'].lower() == data['method'].lower() and\
                    endpoint_data['action_name'] == function.name:
                return endpoint_data

    def delete_endpoint(self, endpoint, fiware_service, fiware_service_path):
        other_endpoints = Endpoint.objects.exclude(id=endpoint.id)\
            .filter(fiware_service=endpoint.fiware_service)\
            .filter(fiware_service_path=endpoint.fiware_service_path)\
            .filter(name=endpoint.name)\
            .filter(path=endpoint.path)
        response = OpenWhiskClient().delete_api(endpoint.name, 'guest')
        # Recreate apis that should not be deleted
        for other_endpoint in other_endpoints:
            self.create_endpoint(fiware_service, fiware_service_path, other_endpoint.get_dict())
        return response

    def list_result(self, fiware_service, fiware_service_path):
        return OpenWhiskClient().list_activation('guest')

    def retrieve_result(self, result_id, fiware_service, fiware_service_path):
        return OpenWhiskClient().retrieve_activation(result_id, 'guest')

import os
from abc import ABCMeta, abstractmethod
from .clients.open_whisk_client import OpenWhiskClient


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
    def list_result(self, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_result(self, result_id, fiware_service, fiware_service_path):
        raise NotImplementedError()


class OpenWhiskDriver(FaaSDriver):
    def escape_fiware_service_path(self, fiware_service_path):
        ESCAPE_TARGET_STR = '/'
        ESCAPE_NEW_STR = 'slash'
        return fiware_service_path.replace(ESCAPE_TARGET_STR, ESCAPE_NEW_STR)

    def __build_function_request_parameter(self, namespace, data):
        request_parameter = {
            'namespace': namespace,
            'name': data['name'],
            'exec': {
                'kind': data['language'],
                'code': data['code']
            }
        }
        if 'parameters' in data:
            request_parameter['parameters'] = data['parameters']
        return request_parameter

    def list_function(self, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        function_list = []
        action_list = OpenWhiskClient().list_action(namespace)
        for action in action_list:
            language = ''
            for annotation in action['annotations']:
                if annotation['key'] == 'exec':
                    language = annotation['value']
            function = {
                'namespace': f'{fiware_service}{fiware_service_path}',
                'name': action['name'],
                'language': language,
                'version': action['version']
            }
            function_list.append(function)
        return function_list

    def retrieve_function(self, function, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        action = OpenWhiskClient().retrieve_action(function.name, namespace)
        language = ''
        for annotation in action['annotations']:
            if annotation['key'] == 'exec':
                language = annotation['value']
        function = {
            'namespace': f'{fiware_service}{fiware_service_path}',
            'name': action['name'],
            'language': language,
            'version': action['version']
        }
        return function

    def create_function(self, fiware_service, fiware_service_path, data):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'

        response = OpenWhiskClient().create_action(namespace,
                                                   self.__build_function_request_parameter(namespace, data))
        response['code'] = data['code']
        response['language'] = data['language']
        return response

    def update_function(self, function, fiware_service, fiware_service_path, data):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'

        response = OpenWhiskClient().update_action(namespace,
                                                   self.__build_function_request_parameter(namespace, data))
        response['code'] = data['code']
        response['language'] = data['language']
        return response

    def delete_function(self, function, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().delete_action(function.name, namespace)

    def list_result(self, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().list_activation(namespace)

    def retrieve_result(self, result_id, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().retrieve_activation(result_id, namespace)

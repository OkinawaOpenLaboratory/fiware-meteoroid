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
    def get_function_list(self, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def get_function(self, function_id, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def create_function(self, fiware_service, fiware_service_path, data):
        raise NotImplementedError()

    @abstractmethod
    def update_function(self, function_id, fiware_service, fiware_service_path, data):
        raise NotImplementedError()

    @abstractmethod
    def delete_function(self, function_id, fiware_service, fiware_service_path):
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
        ESCAPE_NEW_STR = '-'
        return fiware_service_path.replace(ESCAPE_TARGET_STR, ESCAPE_NEW_STR)

    def get_function_list(self, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().get_function_list(namespace)

    def get_function(self, function_id, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().get_function(function_id, namespace)

    def create_function(self, namespace, data, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().create_or_update_function(namespace, data)

    def update_function(self, function_id, fiware_service, fiware_service_path, data):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().create_or_update_function(function_id, namespace, data)

    def delete_function(self, function_id, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().delete_function(function_id, namespace)

    def list_result(self, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().list_activation(namespace)

    def retrieve_result(self, result_id, fiware_service, fiware_service_path):
        escaped_fiware_service_path = self.escape_fiware_service_path(fiware_service_path)
        namespace = f'{fiware_service}{escaped_fiware_service_path}'
        return OpenWhiskClient().retrieve_activation(result_id, namespace)

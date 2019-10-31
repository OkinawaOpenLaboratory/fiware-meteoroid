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


class OpenWhiskDriver(FaaSDriver):
    def get_function_list(self, fiware_service, fiware_service_path):
        return OpenWhiskClient().get_function_list(fiware_service, fiware_service_path)

    def get_function(self, function_id, fiware_service, fiware_service_path):
        return OpenWhiskClient().get_function(function_id, fiware_service, fiware_service_path)

    def create_function(self, fiware_service, fiware_service_path, data):
        return OpenWhiskClient().create_or_update_function(fiware_service, fiware_service_path, data)

    def update_function(self, function_id, fiware_service, fiware_service_path, data):
        return OpenWhiskClient().create_or_update_function(function_id, fiware_service, fiware_service_path, data)

    def delete_function(self, function_id, fiware_service, fiware_service_path):
        return OpenWhiskClient().delete_function(function_id, fiware_service, fiware_service_path)

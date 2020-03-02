import os

from coreapi import Client
from coreapi.transports import HTTPTransport


class BaseClient(object):

    def __init__(self):
        self.schema_endpoint = os.environ.get('METEOROID_SCHEMA_ENDPOINT',
                                              'http://localhost:3000/schema/?format=corejson')

    def _action(self, fiware_service, fiware_service_path, keys, params=None, validate=True):
        headers = {
            'Fiware-Service': fiware_service,
            'Fiware-ServicePath': fiware_service_path
        }
        transport = HTTPTransport(headers=headers)
        client = Client(transports=[transport])
        document = client.get(self.schema_endpoint)
        return client.action(document, keys, params, validate)

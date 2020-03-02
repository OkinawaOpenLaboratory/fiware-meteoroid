from meteoroid.cli.v1.client.base import BaseClient


class EndpointClient(BaseClient):

    def __init__(self):
        super(EndpointClient, self).__init__()

    def retrieve_endpoint(self, id, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['endpoints', 'read'], {'id': id})

    def list_endpoints(self, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['endpoints', 'list'])

    def create_endpoint(self, name, path, method, function_id,
                        fiware_service='', fiware_service_path='/'):
        params = {
            "fiware_service": fiware_service,
            "fiware_service_path": fiware_service_path,
            "name": name,
            "path": path,
            "method": method,
            "function": function_id
        }
        return self._action(fiware_service, fiware_service_path,
                            ['endpoints', 'create'], params)

    def delete_endpoint(self, id, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['endpoints', 'delete'], {'id': id})

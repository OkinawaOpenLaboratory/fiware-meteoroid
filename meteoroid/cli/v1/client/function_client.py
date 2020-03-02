from meteoroid.cli.v1.client.base import BaseClient


class FunctionClient(BaseClient):

    def __init__(self):
        super(FunctionClient, self).__init__()

    def list_function(self, fiware_service, fiware_service_path):
        return self._action(fiware_service,
                            fiware_service_path,
                            ['functions', 'list'])

    def retrieve_function(self, id, fiware_service, fiware_service_path, code=False):
        params = {'id': id}
        if code:
            params['code'] = code
        return self._action(fiware_service,
                            fiware_service_path,
                            ['functions', 'read'],
                            params,
                            validate=not code)

    def create_function(self, fiware_service, fiware_service_path, data):
        return self._action(fiware_service,
                            fiware_service_path,
                            ['functions', 'create'],
                            data,
                            validate=False)

    def update_function(self, fiware_service, fiware_service_path, data):
        return self._action(fiware_service,
                            fiware_service_path,
                            ['functions', 'update'],
                            data,
                            validate=False)

    def delete_function(self, id, fiware_service, fiware_service_path):
        return self._action(fiware_service,
                            fiware_service_path,
                            ['functions', 'delete'],
                            {'id': id},
                            validate=False)

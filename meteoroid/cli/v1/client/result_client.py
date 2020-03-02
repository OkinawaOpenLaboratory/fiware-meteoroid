from meteoroid.cli.v1.client.base import BaseClient


class ResultClient(BaseClient):

    def __init__(self):
        super(ResultClient, self).__init__()

    def retrieve_result(self, id, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['results', 'read'], {'id': id})

    def list_results(self, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['results', 'list'])

from meteoroid.cli.v1.client.base import BaseClient


class ScheduleClient(BaseClient):

    def __init__(self):
        super(ScheduleClient, self).__init__()

    def retrieve_schedule(self, id, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['schedules', 'read'],
                            {'id': id})

    def list_schedules(self, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['schedules', 'list'])

    def create_schedule(self, fiware_service, fiware_service_path, data):
        return self._action(fiware_service, fiware_service_path,
                            ['schedules', 'create'],
                            data,
                            validate=False)

    def delete_schedule(self, id, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['schedules', 'delete'],
                            {'id': id},
                            validate=False)

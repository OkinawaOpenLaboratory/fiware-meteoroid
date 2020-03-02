from meteoroid.cli.v1.client.base import BaseClient


class SubscriptionClient(BaseClient):

    def __init__(self):
        super(SubscriptionClient, self).__init__()

    def retrieve_subscription(self, id, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['subscriptions', 'read'], {'id': id})

    def list_subscriptions(self, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['subscriptions', 'list'])

    def create_subscription(self, endpoint_id, orion_subscription,
                            fiware_service='', fiware_service_path='/'):
        params = {
            "fiware_service": "",
            "fiware_service_path": "/",
            "endpoint_id": endpoint_id,
            "orion_subscription": orion_subscription
        }
        return self._action(fiware_service, fiware_service_path,
                            ['subscriptions', 'create'],
                            params,
                            validate=False)

    def delete_subscription(self, id, fiware_service='', fiware_service_path='/'):
        return self._action(fiware_service, fiware_service_path,
                            ['subscriptions', 'delete'], {'id': id})

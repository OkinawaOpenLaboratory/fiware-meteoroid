import logging

from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


def fiware_headers(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        fiware_service = self.request.META.get('HTTP_FIWARE_SERVICE', '')
        fiware_service_path = self.request.META.get('HTTP_FIWARE_SERVICEPATH', '/')
        return func(*args, **kwargs, fiware_service=fiware_service,
                    fiware_service_path=fiware_service_path)
    return wrapper


def extract_faas_function_param(func):
    def wrapper(*args, **kwargs):
        try:
            request = args[1]
            name = request.data.get('name')
            code = request.data.get('code')
            language = request.data.get('language')
            param = {
                'name': name,
                'code': code,
                'language': language,
            }
            if 'main' in request.data:
                param['main'] = request.data.get('main')

            if 'parameters' in request.data:
                param['parameters'] = request.data.get('parameters')

            if 'binary' in request.data:
                param['binary'] = request.data.get('binary')
        except KeyError as e:
            logger.error(f'Does not exist parameters : {e}')
            raise APIException(detail=f'Does not exist parameters: {e}')

        return func(*args, **kwargs, param=param)
    return wrapper


def extract_faas_subscription_param(func):
    def wrapper(*args, **kwargs):
        try:
            self = args[0]
            endpoint_id = self.request.data['endpoint_id']
            orion_subscription = self.request.data['orion_subscription']
        except KeyError as e:
            logger.error(f'Does not exist parameters : {e}')
            raise APIException(detail=f'Does not exist parameters: {e}')

        return func(*args, **kwargs, endpoint_id=endpoint_id,
                    orion_subscription=orion_subscription)
    return wrapper


def extract_faas_schedule_param(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        function = self.request.data['function']
        name = self.request.data['name']
        schedule = self.request.data['schedule']
        param = {
            'function': function,
            'name': name,
            'schedule': schedule
        }
        if 'trigger_payload' in self.request.data:
            param['trigger_payload'] = self.request.data['trigger_payload']

        if 'startDate' in self.request.data:
            param['startDate'] = self.request.data['startDate']

        if 'stopDate' in self.request.data:
            param['stopDate'] = self.request.data['stopDate']

        return func(*args, **kwargs, function=function,
                    name=name, param=param)
    return wrapper

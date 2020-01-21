import logging
import os
from abc import ABCMeta, abstractmethod

from .clients.open_whisk_client import OpenWhiskClient
from ..models import Endpoint, Function

logger = logging.getLogger(__name__)


class FaaSDriver(metaclass=ABCMeta):
    __instance = None
    @classmethod
    def get_faas_driver(cls):
        faas_name = os.environ.get('FAAS_NAME', 'open_whisk')
        if not cls.__instance:
            if faas_name == 'open_whisk':
                cls.__instance = OpenWhiskDriver()
            else:
                logger.error(f'Does not support {faas_name}')
                raise Exception(f'Does not support {faas_name}')
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
    def list_endpoint(self, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_endpoint(self, endpoint, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def create_endpoint(self, fiware_service, fiware_service_path, data):
        raise NotImplementedError()

    @abstractmethod
    def delete_endpoint(self, endpoint, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def list_result(self, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_result(self, result_id, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_result_logs(self, result_id, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_schedule(self, schedule, fiware_service, fiware_service_path):
        raise NotImplementedError()

    @abstractmethod
    def create_schedule(self, fiware_service, fiware_service_path, data):
        raise NotImplementedError()

    @abstractmethod
    def delete_schedule(self, schedule, fiware_service, fiware_service_path):
        raise NotImplementedError()


class OpenWhiskDriver(FaaSDriver):
    def escape_fiware_service_path(self, fiware_service_path):
        escape_target_str = '/'
        escape_new_str = '_'
        return fiware_service_path.replace(escape_target_str, escape_new_str)

    def __build_action_request_parameter(self, namespace, data):
        request_parameter = {
            'namespace': namespace,
            'name': data['name'],
            'exec': {
                'kind': data['language'],
                'code': data['code']
            },
            'annotations': [{'key': 'web-export',
                             'value': True}]
        }
        if 'main' in data:
            request_parameter['exec']['main'] = data['main']
        if 'parameters' in data:
            request_parameter['parameters'] = data['parameters']
        if 'binary' in data:
            request_parameter['exec']['binary'] = data['binary']
        return request_parameter

    def __build_api_request_parameter(self, namespace, data):
        base_path = data['name']
        function = Function.objects.get(pk=data['function'])
        request_parameter = {
            'apidoc': {
                'namespace': namespace,
                'gatewayBasePath': base_path,
                'gatewayPath': data['path'],
                'gatewayMethod': data['method'],
                'id': f'API:{namespace}:{base_path}',
                'action': {
                    'name': function.name,
                    'namespace': namespace,
                    'backendMethod': data['method'],
                }
            }
        }
        return request_parameter

    def __build_all_endpoint_list_response(self, api_list):
        endpoint_list = []
        for api in api_list['apis']:
            endpoint = self.__build_endpoint_list_response(api['value'])
            endpoint_list.extend(endpoint)
        return endpoint_list

    def __build_endpoint_list_response(self, api):
        doc = api['apidoc']
        gw_api_url = api['gwApiUrl']
        endpoint_list = []
        for path, path_value in doc['paths'].items():
            for method, method_value in path_value.items():
                action_name = method_value['x-openwhisk']['action']

                endpoint = {
                    'name': doc['basePath'],
                    'path': path,
                    'method': method,
                    'action_name': action_name,
                    'url': f'{gw_api_url}{path}'
                }
                endpoint_list.append(endpoint)
        return endpoint_list

    def list_function(self, fiware_service, fiware_service_path):
        function_list = []
        action_list = OpenWhiskClient().list_action('guest')
        for action in action_list:
            language = ''
            for annotation in action['annotations']:
                if annotation['key'] == 'exec':
                    language = annotation['value']
            function = {
                'namespace': f'{fiware_service}{fiware_service_path}',
                'name': action['name'],
                'language': language,
                'binary': action['exec']['binary'],
                'version': action['version']
            }
            function_list.append(function)
        return function_list

    def retrieve_function(self, function, fiware_service, fiware_service_path, code=False):
        action = OpenWhiskClient().retrieve_action(function.name, 'guest', code=code)
        function = {
            'namespace': f'{fiware_service}{fiware_service_path}',
            'name': action['name'],
            'language': action['exec']['kind'],
            'binary': action['exec']['binary'],
            'version': action['version'],
            'parameters': action['parameters']
        }
        if code:
            function['code'] = action['exec']['code']
        return function

    def create_function(self, fiware_service, fiware_service_path, data):
        response = OpenWhiskClient().create_action('guest',
                                                   self.__build_action_request_parameter('guest',
                                                                                         data))
        response['code'] = data['code']
        response['language'] = data['language']
        response['binary'] = response['exec']['binary']
        return response

    def update_function(self, function, fiware_service, fiware_service_path, data):
        builded_data = self.__build_action_request_parameter('guest', data)
        # Function name cannot be changed when updating.
        builded_data['name'] = function.name
        response = OpenWhiskClient().update_action(function.name,
                                                   'guest',
                                                   builded_data)
        response['code'] = data['code']
        response['language'] = data['language']
        response['binary'] = response['exec']['binary']
        return response

    def delete_function(self, function, fiware_service, fiware_service_path):
        return OpenWhiskClient().delete_action(function.name, 'guest')

    def list_endpoint(self, fiware_service, fiware_service_path):
        api_list = OpenWhiskClient().list_api('guest')
        return self.__build_all_endpoint_list_response(api_list)

    def retrieve_endpoint(self, endpoint, fiware_service, fiware_service_path):
        api_list = OpenWhiskClient().list_api('guest')
        for endpoint_data in self.__build_all_endpoint_list_response(api_list):
            if endpoint.equals_faas_data(endpoint_data):
                return endpoint_data
        return {}

    def create_endpoint(self, fiware_service, fiware_service_path, data):
        api = OpenWhiskClient().create_api('guest',
                                           self.__build_api_request_parameter('guest', data))
        function = Function.objects.filter(
            fiware_service=fiware_service,
            fiware_service_path=fiware_service_path).get(
                pk=data['function'])
        for endpoint_data in self.__build_endpoint_list_response(api):
            if endpoint_data['name'] == data['name'] and\
                    endpoint_data['path'] == data['path'] and\
                    endpoint_data['method'].lower() == data['method'].lower() and\
                    endpoint_data['action_name'] == function.name:
                return endpoint_data

    def delete_endpoint(self, endpoint, fiware_service, fiware_service_path):
        other_endpoints = Endpoint.objects.exclude(id=endpoint.id)\
            .filter(fiware_service=endpoint.fiware_service)\
            .filter(fiware_service_path=endpoint.fiware_service_path)\
            .filter(name=endpoint.name)\
            .filter(path=endpoint.path)
        response = OpenWhiskClient().delete_api(endpoint.name, 'guest')
        # Recreate apis that should not be deleted
        for other_endpoint in other_endpoints:
            self.create_endpoint(fiware_service, fiware_service_path, other_endpoint.get_dict())
        return response

    def list_result(self, fiware_service, fiware_service_path):
        return OpenWhiskClient().list_activation('guest')

    def retrieve_result(self, result_id, fiware_service, fiware_service_path):
        return OpenWhiskClient().retrieve_activation(result_id, 'guest')

    def retrieve_result_logs(self, result_id, fiware_service, fiware_service_path):
        return OpenWhiskClient().retrieve_activation_logs(result_id, 'guest')

    def __build_trigger_request_parameter(self, data):
        trigger_name = data['name'] + '-trigger'
        request_parameter = {
            'name': trigger_name,
            'annotations': [{
                'key': 'feed', 'value': '/whisk.system/alarms/alarm'
            }]
        }
        return request_parameter

    def __build_invoke_alarm_action_request_parameter(self, data, lifecycle_event):
        username = os.environ.get('OPEN_WHISK_USER', '')
        password = os.environ.get('OPEN_WHISK_PASSWORD', '')
        trigger_name = data['name'] + '-trigger'
        invoke_data = {}

        if lifecycle_event == 'CREATE':
            schedule = data['schedule']
            invoke_data = {
                'authKey': f'{username}:{password}',
                'cron': schedule,
                'lifecycleEvent': lifecycle_event,
                'triggerName': f'/_/{trigger_name}'
            }
            if data.get('startDate'):
                invoke_data['startDate'] = data['startDate']
            if data.get('stopDate'):
                invoke_data['stopDate'] = data['stopDate']
            if data.get('trigger_payload'):
                invoke_data['trigger_payload'] = data['trigger_payload']
        elif lifecycle_event == 'READ' or lifecycle_event == 'DELETE':
            invoke_data = {
                'authKey': f'{username}:{password}',
                'lifecycleEvent': lifecycle_event,
                'triggerName': trigger_name
            }
        return invoke_data

    def __build_create_rule_request_patameter(self, action_name, data):
        trigger_name = data['name'] + '-trigger'
        rule_name = data['name'] + '-rule'
        rule_data = {
            'name': rule_name,
            'status': data.get('status', ''),
            'trigger': f'/_/{trigger_name}',
            'action': f'/_/{action_name}'
        }
        return rule_data

    def create_schedule(self, fiware_service, fiware_service_path, data):
        function = Function.objects.filter(
                       fiware_service=fiware_service,
                       fiware_service_path=fiware_service_path).get(pk=data['function'])

        schedule = data['schedule']

        trigger_data = self.__build_trigger_request_parameter(data)
        OpenWhiskClient().create_trigger('guest', trigger_data)

        invoke_data = self.__build_invoke_alarm_action_request_parameter(data, 'CREATE')
        OpenWhiskClient().invoke_action_with_package(
            'alarms', 'alarm', 'whisk.system', invoke_data)

        rule_data = self.__build_create_rule_request_patameter(function.name, data)
        OpenWhiskClient().create_rule('guest', rule_data)

        schedule = {
            'trigger_name': trigger_data['name'],
            'rule_name': rule_data['name'],
            'name': data['name'],
            'schedule': data['schedule'],
            'function': function.id,
            'trigger_payload': invoke_data.get('trigger_payload', ''),
            'startDate': invoke_data.get('startDate', ''),
            'stopDate': invoke_data.get('stopDate', '')
        }
        return schedule

    def retrieve_schedule(self, schedule, fiware_service, fiware_service_path):
        invoke_data = self.__build_invoke_alarm_action_request_parameter(
                          {'name': schedule.name}, 'READ')
        invoked = OpenWhiskClient().invoke_action_with_package(
                      'alarms', 'alarm', 'whisk.system', invoke_data)
        config = invoked.json()['response']['result']['config']
        OpenWhiskClient().retrieve_rule(schedule.rule_name, 'guest')
        schedule_details = {
            'schedule': config['cron'],
            'function': schedule.function.id,
            'id': schedule.id,
            'name': schedule.name,
            'startDate': config.get('startDate', ''),
            'stopDate': config.get('stopDate', ''),
            'trigger_payload': config.get('payload', '')
        }
        return schedule_details

    def delete_schedule(self, schedule, fiware_service, fiware_service_path):
        invoke_data = self.__build_invoke_alarm_action_request_parameter(
                          {'name': schedule.name}, 'DELETE')
        OpenWhiskClient().invoke_action_with_package('alarms', 'alarm', 'whisk.system', invoke_data)
        OpenWhiskClient().delete_rule(schedule.rule_name, 'guest')
        response = OpenWhiskClient().delete_trigger(schedule.trigger_name, 'guest')
        return response

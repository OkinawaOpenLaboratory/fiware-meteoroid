from django.test import TestCase

from ..models import Endpoint
from ..models import Function
from ..models import Schedule
from ..serializers import EndpointSerializer, FunctionSerializer, ScheduleSerializer


class TestFunctionSerializer(TestCase):

    def setUp(self):
        faas_function_data = {
            'name': 'test-function',
            'code': 'def main(args): return "test"',
            'language': 'python:3',
            'binary': False,
            'main': '',
            'version': '0.0.1',
            'parameters': []
        }
        self.function = Function.objects.create(name='test-function')
        self.function_serializer = FunctionSerializer(self.function,
                                                      faas_function_data=faas_function_data)

    def test_expected_data(self):
        data = self.function_serializer.data
        expected_data = {
            'id': self.function.id,
            'name': 'test-function',
            'code': 'def main(args): return "test"',
            'language': 'python:3',
            'binary': False,
            'main': '',
            'version': '0.0.1',
            'parameters': [],
            'fiware_service': '',
            'fiware_service_path': '/'
        }
        self.assertEqual(data, expected_data)

    def test_contains_expected_fields(self):
        data = self.function_serializer.data

        expected_keys = set(['id', 'name', 'code', 'language',
                             'main', 'version', 'parameters', 'binary',
                             'fiware_service', 'fiware_service_path'])
        self.assertEqual(set(data.keys()), expected_keys)


class TestFunctionListSerializer(TestCase):

    def setUp(self):
        faas_function_data = [{
            'name': 'test-function1',
            'code': 'def main(args): return "test1"',
            'language': 'python:3',
            'binary': False,
            'main': '',
            'version': '0.0.1',
            'parameters': []
        }, {
            'name': 'test-function2',
            'code': 'def main(args): return "test2"',
            'language': 'python:3',
            'binary': False,
            'main': '',
            'version': '0.0.1',
            'parameters': []
        }]
        self.function1 = Function.objects.create(name='test-function1')
        self.function2 = Function.objects.create(name='test-function2')
        self.function_serializer = FunctionSerializer(Function.objects.all(),
                                                      many=True,
                                                      faas_function_data=faas_function_data)

    def test_expected_data(self):
        data = self.function_serializer.data
        expected_data = [{
            'id': self.function1.id,
            'name': 'test-function1',
            'code': 'def main(args): return "test1"',
            'language': 'python:3',
            'binary': False,
            'main': '',
            'version': '0.0.1',
            'parameters': [],
            'fiware_service': '',
            'fiware_service_path': '/'
        }, {
            'id': self.function2.id,
            'name': 'test-function2',
            'code': 'def main(args): return "test2"',
            'language': 'python:3',
            'binary': False,
            'main': '',
            'version': '0.0.1',
            'parameters': [],
            'fiware_service': '',
            'fiware_service_path': '/'
        }]
        self.assertEqual(data, expected_data)


class TestEndpointSerializer(TestCase):

    def setUp(self):
        self.function = Function.objects.create(name='test-function')
        self.endpoint = Endpoint.objects.create(name='test',
                                                path='path',
                                                method='get',
                                                function=self.function)
        faas_endpoint_data = {
            'url': 'http://test/path'
        }
        self.endpoint_serializer = EndpointSerializer(self.endpoint,
                                                      faas_endpoint_data=faas_endpoint_data)

    def test_expected_data(self):
        data = self.endpoint_serializer.data
        expected_data = {
            'id': self.endpoint.id,
            'name': 'test',
            'path': 'path',
            'method': 'get',
            'function': self.function.id,
            'url': 'http://test/path',
            'fiware_service': '',
            'fiware_service_path': '/'
        }
        self.assertEqual(data, expected_data)

    def test_contains_expected_fields(self):
        data = self.endpoint_serializer.data

        expected_keys = set(['id', 'name', 'path', 'method', 'url', 'function',
                             'fiware_service', 'fiware_service_path'])
        self.assertEqual(set(data.keys()), expected_keys)


class TestEndpointListSerializer(TestCase):

    def setUp(self):
        self.function = Function.objects.create(name='test-function')
        self.endpoint1 = Endpoint.objects.create(name='test1',
                                                 path='path1',
                                                 method='get',
                                                 function=self.function)
        self.endpoint2 = Endpoint.objects.create(name='test2',
                                                 path='path2',
                                                 method='post',
                                                 function=self.function)
        faas_endpoint_data = [{
            'name': 'test1',
            'path': 'path1',
            'method': 'get',
            'action_name': self.function.name,
            'url': 'http://test1/path1'
        }, {
            'name': 'test2',
            'path': 'path2',
            'method': 'post',
            'action_name': self.function.name,
            'url': 'http://test2/path2'
        }]
        self.endpoint_serializer = EndpointSerializer(Endpoint.objects.all(),
                                                      many=True,
                                                      faas_endpoint_data=faas_endpoint_data)

    def test_expected_data(self):
        data = self.endpoint_serializer.data
        expected_data = [{
            'id': self.endpoint1.id,
            'name': 'test1',
            'path': 'path1',
            'method': 'get',
            'function': self.function.id,
            'url': 'http://test1/path1',
            'fiware_service': '',
            'fiware_service_path': '/'
        }, {
            'id': self.endpoint2.id,
            'name': 'test2',
            'path': 'path2',
            'method': 'post',
            'function': self.function.id,
            'url': 'http://test2/path2',
            'fiware_service': '',
            'fiware_service_path': '/'
        }]
        self.assertEqual(data, expected_data)


class TestScheduleSerializer(TestCase):

    def setUp(self):
        self.function = Function.objects.create(name='test-function')
        self.schedule = Schedule.objects.create(trigger_name='test-trigger', rule_name='test-rule',
                                                name='test-schedule', function=self.function)
        self.schedule_serializer = ScheduleSerializer(self.schedule)

    def test_contains_expected_fields(self):
        data = self.schedule_serializer.data

        expected_keys = set(['id', 'function', 'trigger_name', 'rule_name', 'name',
                             'fiware_service', 'fiware_service_path'])
        self.assertEqual(set(data.keys()), expected_keys)

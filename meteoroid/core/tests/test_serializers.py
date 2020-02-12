from django.test import TestCase

from ..models import Function
from ..models import Schedule
from ..serializers import FunctionSerializer, ScheduleSerializer


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

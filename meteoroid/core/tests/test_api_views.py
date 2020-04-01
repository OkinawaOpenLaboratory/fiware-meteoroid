import os
from unittest.mock import patch

from django.test import TestCase

from parameterized import parameterized_class

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory

from ..api_views import ScheduleViewSet
from ..models import Endpoint
from ..models import Function
from ..models import Schedule

DIR = os.path.dirname(os.path.abspath(__file__))


@parameterized_class(('is_binary', 'code'),
                     [(False, open(os.path.join(DIR, 'test_data/python_main.py')).read()),
                      (True, open(os.path.join(DIR, 'test_data/python_binary_main.txt')).read())])
class TestFunctionViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.function = Function.objects.create(name='initial-function')

    class MockDriver:
        def __init__(self, code, is_binary):
            self.code = code
            self.is_binary = is_binary

        def create_function(self, fiware_service, fiware_service_path, param):
            return {'name': 'test-function',
                    'code': self.code,
                    'binary': self.is_binary,
                    'language': 'python:3',
                    'parameters': []}

        def list_function(self, fiware_service, fiware_service_path):
            return [{'name': 'initial-function',
                     'code': self.code,
                     'binary': self.is_binary,
                     'language': 'python:3',
                     'parameters': []}]

        def retrieve_function(self, function, fiware_service, fiware_service_path, code):
            return {'name': 'initial-function',
                    'code': self.code,
                    'binary': self.is_binary,
                    'language': 'python:3',
                    'parameters': []}

        def update_function(self, function, fiware_service, fiware_service_path, param):
            return {'name': 'initial-function',
                    'code': self.code,
                    'binary': self.is_binary,
                    'language': 'python:3',
                    'parameters': []}

        def delete_function(self, function, fiware_service, fiware_service_path):
            return Response()

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_create_function(self, mock):
        mock.return_value = self.MockDriver(self.code, self.is_binary)
        data = {'name': 'test-function',
                'code': self.code,
                'binary': self.is_binary,
                'language': 'python:3',
                'parameters': []}

        response = self.client.post(reverse('function-list'),
                                    data,
                                    HTTP_FIWARE_SERVICE='test',
                                    HTTP_FIWARE_SERVICEPATH='/test')
        last_id = Function.objects.last().id
        expected_data = {'id': last_id,
                         'code': self.code,
                         'language': 'python:3',
                         'binary': self.is_binary,
                         'main': '',
                         'version': '',
                         'parameters': [],
                         'fiware_service': 'test',
                         'fiware_service_path': '/test',
                         'name': 'test-function'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Function.objects.count(), 2)
        self.assertEqual(response.data, expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_update_function(self, mock):
        mock.return_value = self.MockDriver(self.code, self.is_binary)
        data = {'name': 'test-function',
                'code': self.code,
                'binary': self.is_binary,
                'language': 'python:3',
                'parameters': []}
        response = self.client.put(reverse('function-detail',
                                           kwargs={'pk': self.function.id}),
                                   data)
        expected_data = {'id': self.function.id,
                         'code': self.code,
                         'language': 'python:3',
                         'binary': self.is_binary,
                         'main': '',
                         'version': '',
                         'parameters': [],
                         'fiware_service': '',
                         'fiware_service_path': '/',
                         'name': 'initial-function'}
        self.assertEqual(Function.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_list_function(self, mock):
        mock.return_value = self.MockDriver(self.code, self.is_binary)

        response = self.client.get('/api/v1/functions')
        expected_data = [{'id': self.function.id,
                          'code': self.code,
                          'language': 'python:3',
                          'binary': self.is_binary,
                          'main': '',
                          'version': '',
                          'parameters': [],
                          'fiware_service': '',
                          'fiware_service_path': '/',
                          'name': 'initial-function'}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_retrieve_function(self, mock):
        mock.return_value = self.MockDriver(self.code, self.is_binary)
        url = reverse('function-detail', kwargs={'pk': self.function.id})
        response = self.client.get(f'{url}?code=false')
        expected_data = {'id': self.function.id,
                         'code': self.code,
                         'language': 'python:3',
                         'binary': self.is_binary,
                         'main': '',
                         'version': '',
                         'parameters': [],
                         'fiware_service': '',
                         'fiware_service_path': '/',
                         'name': 'initial-function'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_delete_function(self, mock):
        mock.return_value = self.MockDriver(self.code, self.is_binary)
        response = self.client.delete(reverse('function-detail',
                                              kwargs={'pk': self.function.id}))
        self.assertEqual(Function.objects.count(), 0)
        self.assertEqual(response.status_code, 204)

    def tearDown(self):
        Function.objects.all().delete()


class TestEndpointViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.function = Function.objects.create(name='test-function')
        self.endpoint = Endpoint.objects.create(name='test',
                                                path='path',
                                                method='get',
                                                function=self.function)

    class MockDriver:
        def __init__(self, function):
            self.function = function

        def create_endpoint(self, fiware_service, fiware_service_path, param):
            return {'name': 'test',
                    'path': 'path',
                    'method': 'get',
                    'function': self.function.id,
                    'url': 'http://test/path'}

        def list_endpoint(self, fiware_service, fiware_service_path):
            return [{'name': 'test',
                     'path': 'path',
                     'method': 'get',
                     'action_name': self.function.name,
                     'function': self.function.id,
                     'url': 'http://test/path'}]

        def retrieve_endpoint(self, function, fiware_service, fiware_service_path):
            return {'name': 'test',
                    'path': 'path',
                    'method': 'get',
                    'function': self.function.id,
                    'url': 'http://test/path'}

        def delete_endpoint(self, function, fiware_service, fiware_service_path):
            return Response()

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_create_endpoint(self, mock):
        mock.return_value = self.MockDriver(self.function)
        data = {'name': 'test',
                'path': 'path',
                'method': 'get',
                'function': self.function.id}

        response = self.client.post(reverse('endpoints-list'),
                                    data,
                                    HTTP_FIWARE_SERVICE='test',
                                    HTTP_FIWARE_SERVICEPATH='/test')
        last_id = Endpoint.objects.last().id
        expected_data = {'id': last_id,
                         'name': 'test',
                         'path': 'path',
                         'method': 'get',
                         'function': self.function.id,
                         'url': 'http://test/path',
                         'fiware_service': 'test',
                         'fiware_service_path': '/test'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Endpoint.objects.count(), 2)
        self.assertEqual(response.data, expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_list_endpoint(self, mock):
        mock.return_value = self.MockDriver(self.function)

        response = self.client.get(reverse('endpoints-list'))
        expected_data = [{'id': self.endpoint.id,
                          'name': 'test',
                          'path': 'path',
                          'method': 'get',
                          'function': self.function.id,
                          'url': 'http://test/path',
                          'fiware_service': '',
                          'fiware_service_path': '/'}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_retrieve_endpoint(self, mock):
        mock.return_value = self.MockDriver(self.function)
        url = reverse('endpoints-detail', kwargs={'pk': self.endpoint.id})
        response = self.client.get(url)
        expected_data = {'id': self.endpoint.id,
                         'name': 'test',
                         'path': 'path',
                         'method': 'get',
                         'function': self.function.id,
                         'url': 'http://test/path',
                         'fiware_service': '',
                         'fiware_service_path': '/'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_delete_endpoint(self, mock):
        mock.return_value = self.MockDriver(self.function)
        response = self.client.delete(reverse('endpoints-detail',
                                              kwargs={'pk': self.endpoint.id}))
        self.assertEqual(Endpoint.objects.count(), 0)
        self.assertEqual(response.status_code, 204)

    def tearDown(self):
        Function.objects.all().delete()


class TestScheduleViewSet(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.function = Function.objects.create(name='test-function')

    class MockDriver(object):
        def create_schedule(self, fiware_service, fiware_service_path, param):
            return {'trigger_name': 'test-trigger', 'rule_name': 'test-rule',
                    'schedule': '*/20 * * * * *'}

        def list_schedule(self, fiware_service, fiware_service_path):
            return Response()

        def retrieve_schedule(self, schedule, fiware_service, fiware_service_path):
            return Response()

        def delete_schedule(self, schedule, fiware_service, fiware_service_path):
            return Response()

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_create_schedule(self, mock):
        mock.return_value = self.MockDriver()

        data = {
            'name': 'test-schedule',
            'schedule': '*/20 * * * * *',
            'function': self.function.id
        }
        request = self.factory.post('/api/v1/schedules',
                                    data,
                                    fiware_service='',
                                    fiware_service_path='/')
        view = ScheduleViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_list_schedule(self, mock):
        mock.return_value = self.MockDriver()

        request = self.factory.get('/api/v1/schedules')
        view = ScheduleViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_retrieve_schedule(self, mock):
        mock.return_value = self.MockDriver()

        schedule = Schedule.objects.create(trigger_name='test-trigger', rule_name='test-rule',
                                           name='schedule')
        request = self.factory.get('/api/v1/schedules')
        view = ScheduleViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=schedule.id)
        self.assertEqual(response.status_code, 200)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_delete_schedule(self, mock):
        mock.return_value = self.MockDriver()

        schedule = Schedule.objects.create(trigger_name='test-trigger', rule_name='test-rule',
                                           name='schedule2')
        request = self.factory.delete(f'/api/v1/schdules/{schedule.id}')
        view = ScheduleViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=schedule.id)
        self.assertEqual(response.status_code, 204)

    def tearDown(self):
        self.function.delete()

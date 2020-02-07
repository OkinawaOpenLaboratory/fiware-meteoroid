from unittest.mock import patch

from django.test import TestCase

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory

from ..api_views import ScheduleViewSet
from ..models import Function
from ..models import Schedule


class TestFunctionViewSet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.function = Function.objects.create(name='initial-function')

    class MockDriver:
        def create_function(self, fiware_service, fiware_service_path, param):
            return {'name': 'test-function',
                    'code': 'def main(args): return "test"',
                    'language': 'python:3',
                    'parameters': []}

        def list_function(self, fiware_service, fiware_service_path):
            return [{'name': 'initial-function',
                     'code': 'def main(args): return "updated-test"',
                     'language': 'python:3',
                     'parameters': []}]

        def retrieve_function(self, function, fiware_service, fiware_service_path, code):
            return {'name': 'initial-function',
                    'code': 'def main(args): return "updated-test"',
                    'language': 'python:3',
                    'parameters': []}

        def update_function(self, function, fiware_service, fiware_service_path, param):
            return {'name': 'initial-function',
                    'code': 'def main(args): return "updated-test"',
                    'language': 'python:3',
                    'parameters': []}

        def delete_function(self, function, fiware_service, fiware_service_path):
            return Response()

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_create_function(self, mock):
        mock.return_value = self.MockDriver()
        data = {'name': 'test-function',
                'code': 'def main(args): return "updated-test"',
                'language': 'python:3',
                'parameters': []}

        response = self.client.post(reverse('function-list'),
                                    data,
                                    HTTP_FIWARE_SERVICE='test',
                                    HTTP_FIWARE_SERVICEPATH='/test')
        last_id = Function.objects.last().id
        expected_data = {'id': last_id,
                         'code': 'def main(args): return "test"',
                         'language': 'python:3',
                         'binary': False,
                         'main': '',
                         'version': '',
                         'parameters': [],
                         'fiware_service': 'test',
                         'fiware_service_path': '/test',
                         'name': 'test-function'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Function.objects.count(), 2)
        self.assertEqual(response.data,
                         expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_update_function(self, mock):
        mock.return_value = self.MockDriver()
        data = {'name': 'test-function',
                'code': 'def main(args): return "updated-test"',
                'language': 'python:3',
                'parameters': []}
        response = self.client.put(reverse('function-detail',
                                           kwargs={'pk': self.function.id}),
                                   data)
        expected_data = {'id': self.function.id,
                         'code': 'def main(args): return "updated-test"',
                         'language': 'python:3',
                         'binary': False,
                         'main': '',
                         'version': '',
                         'parameters': [],
                         'fiware_service': '',
                         'fiware_service_path': '/',
                         'name': 'initial-function'}
        self.assertEqual(Function.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_list_function(self, mock):
        mock.return_value = self.MockDriver()

        response = self.client.get('/api/v1/functions')
        expected_data = [{'id': self.function.id,
                          'code': 'def main(args): return "updated-test"',
                          'language': 'python:3',
                          'binary': False,
                          'main': '',
                          'version': '',
                          'parameters': [],
                          'fiware_service': '',
                          'fiware_service_path': '/',
                          'name': 'initial-function'}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_retrieve_function(self, mock):
        mock.return_value = self.MockDriver()
        url = reverse('function-detail', kwargs={'pk': self.function.id})
        response = self.client.get(f'{url}?code=false')
        expected_data = {'id': self.function.id,
                         'code': 'def main(args): return "updated-test"',
                         'language': 'python:3',
                         'binary': False,
                         'main': '',
                         'version': '',
                         'parameters': [],
                         'fiware_service': '',
                         'fiware_service_path': '/',
                         'name': 'initial-function'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         expected_data)

    @patch('core.libs.faas_driver.FaaSDriver.get_faas_driver')
    def test_delete_function(self, mock):
        mock.return_value = self.MockDriver()
        response = self.client.delete(reverse('function-detail',
                                              kwargs={'pk': self.function.id}))
        self.assertEqual(Function.objects.count(), 0)
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

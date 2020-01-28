from unittest.mock import patch

from django.test import TestCase

from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from ..api_views import ScheduleViewSet
from ..models import Function
from ..models import Schedule


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

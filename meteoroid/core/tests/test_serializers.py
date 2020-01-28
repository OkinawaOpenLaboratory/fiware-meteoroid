from django.test import TestCase

from ..models import Function
from ..models import Schedule
from ..serializers import ScheduleSerializer


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

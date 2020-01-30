from django.test import TestCase

from ..models import Function
from ..models import Schedule


class TestSchedule(TestCase):

    def test_create_schedule(self):
        function = Function(name='test-function')
        function.save()
        Schedule.objects.create(trigger_name='test-trigger', rule_name='test-rule',
                                name='test-schedule', function=function)
        self.assertEqual(1, len(Schedule.objects.all()))

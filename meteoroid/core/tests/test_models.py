from django.test import TestCase

from ..models import Endpoint
from ..models import Function
from ..models import Schedule
from ..models import Subscription


class TestFunction(TestCase):

    def test_create_function(self):
        function = Function(name='test-function')
        function.save()
        self.assertEqual(1, Function.objects.count())


class TestEndpoint(TestCase):

    def test_create_endpoint(self):
        function = Function.objects.create(name='test-function')
        Endpoint.objects.create(name='test-endpoint', path='/test-function',
                                method='post', function=function)
        self.assertEqual(1, Endpoint.objects.count())


class TestSubscription(TestCase):

    def test_create_subscription(self):
        function = Function.objects.create(name='test-function')
        endpoint = Endpoint.objects.create(name='test-endpoint', path='/test-function',
                                           method='post', function=function)
        Subscription.objects.create(endpoint_id=endpoint, orion_subscription_id='test-id')
        self.assertEqual(1, Subscription.objects.count())


class TestSchedule(TestCase):

    def test_create_schedule(self):
        function = Function(name='test-function')
        function.save()
        Schedule.objects.create(trigger_name='test-trigger', rule_name='test-rule',
                                name='test-schedule', function=function)
        self.assertEqual(1, len(Schedule.objects.all()))

import os

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Function
from .models import Endpoint
from .models import Subscription
from .serializers import FunctionSerializer
from .serializers import SubscriptionSerializer
from django.shortcuts import get_object_or_404
from .libs.faas_driver import FaaSDriver
from .libs.decorators import fiware_headers, extract_faas_function_param
from .libs.decorators import extract_faas_subscription_param
from .libs.clients.orion_subscription_client import OrionSubscriptionClient
from .models import Function, Endpoint
from .serializers import FunctionSerializer, EndpointSerializer
from django.shortcuts import get_object_or_404
from .libs.faas_driver import FaaSDriver
from .libs.decorators import (fiware_headers,
                              extract_faas_function_param)


class FunctionViewSet(viewsets.ModelViewSet):
    serializer_class = FunctionSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'delete']

    @fiware_headers
    def list(self, request, fiware_service, fiware_service_path):
        faas_driver = FaaSDriver.get_faas_driver()
        faas_function_data = faas_driver.list_function(fiware_service, fiware_service_path)
        serializer = self.serializer_class(self.get_queryset(), faas_function_data=faas_function_data, many=True)
        return Response(serializer.data)

    @fiware_headers
    @extract_faas_function_param
    def create(self, request, fiware_service, fiware_service_path, param):
        faas_driver = FaaSDriver.get_faas_driver()
        faas_function_data = faas_driver.create_function(fiware_service, fiware_service_path, param)
        serializer = self.serializer_class(data=request.data, faas_function_data=faas_function_data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    @fiware_headers
    def retrieve(self, request, pk=None, fiware_service='', fiware_service_path='/'):
        function = get_object_or_404(self.get_queryset(), pk=pk)
        faas_driver = FaaSDriver.get_faas_driver()
        faas_function_data = faas_driver.retrieve_function(function, fiware_service, fiware_service_path)
        serializer = self.serializer_class(function, faas_function_data=faas_function_data)
        return Response(serializer.data)

    @fiware_headers
    @extract_faas_function_param
    def update(self, request, pk=None, fiware_service='', fiware_service_path='/', param={}):
        function = get_object_or_404(self.get_queryset(), pk=pk)
        faas_driver = FaaSDriver.get_faas_driver()
        faas_function_data = faas_driver.update_function(function, fiware_service, fiware_service_path, param)
        serializer = self.serializer_class(function, data=request.data, faas_function_data=faas_function_data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    @fiware_headers
    def destroy(self, request, pk=None, fiware_service='', fiware_service_path='/'):
        function = get_object_or_404(self.get_queryset(), pk=pk)
        faas_driver = FaaSDriver.get_faas_driver()
        faas_driver.delete_function(function, fiware_service, fiware_service_path)
        self.perform_destroy(function)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @fiware_headers
    def get_queryset(self, fiware_service, fiware_service_path):
        return Function.objects.filter(fiware_service=fiware_service,
                                       fiware_service_path=fiware_service_path)


class EndpointViewSet(viewsets.ModelViewSet):
    serializer_class = EndpointSerializer
    http_method_names = ['get', 'post', 'head', 'delete']

    @fiware_headers
    def list(self, request, fiware_service, fiware_service_path):
        faas_driver = FaaSDriver.get_faas_driver()
        faas_endpoint_data = faas_driver.list_endpoint(fiware_service, fiware_service_path)
        serializer = self.serializer_class(self.get_queryset(), faas_endpoint_data=faas_endpoint_data, many=True)
        return Response(serializer.data)

    @fiware_headers
    def create(self, request, fiware_service, fiware_service_path):
        faas_driver = FaaSDriver.get_faas_driver()
        faas_endpoint_data = faas_driver.create_endpoint(fiware_service, fiware_service_path, request.data)
        serializer = self.serializer_class(data=request.data, faas_endpoint_data=faas_endpoint_data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    @fiware_headers
    def retrieve(self, request, pk=None, fiware_service='', fiware_service_path='/'):
        endpoint = get_object_or_404(self.get_queryset(), pk=pk)
        faas_driver = FaaSDriver.get_faas_driver()
        faas_endpoint_data = faas_driver.retrieve_endpoint(endpoint, fiware_service, fiware_service_path)
        serializer = self.serializer_class(endpoint, faas_endpoint_data=faas_endpoint_data)
        return Response(serializer.data)

    @fiware_headers
    def destroy(self, request, pk=None, fiware_service='', fiware_service_path='/'):
        endpoint = get_object_or_404(self.get_queryset(), pk=pk)
        faas_driver = FaaSDriver.get_faas_driver()
        faas_driver.delete_endpoint(endpoint, fiware_service, fiware_service_path)
        self.perform_destroy(endpoint)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @fiware_headers
    def get_queryset(self, fiware_service, fiware_service_path):
        return Endpoint.objects.filter(fiware_service=fiware_service,
                                       fiware_service_path=fiware_service_path)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    http_method_names = ['get', 'post', 'delete']

    @fiware_headers
    def list(self, request, fiware_service, fiware_service_path):
        serializer = self.serializer_class(
                         self.get_queryset(),
                         many=True)
        return Response(serializer.data)

    @fiware_headers
    @extract_faas_subscription_param
    def create(self, request, fiware_service, fiware_service_path,
               endpoint_id, orion_subscription):
        endpoint = Endpoint.objects.get(id=endpoint_id)
        host = os.environ.get('OPEN_WHISK_HOST', '')
        url = f'https://{host}{endpoint.path}'
        orion_subscription['notification']['http'] = {'url': url}
        osc = OrionSubscriptionClient()
        location = osc.create_subscription(
                       orion_subscription,
                       fiware_service,
                       fiware_service_path).headers['Location']
        sub_id = location.replace('/v2/subscriptions/', '')
        data = request.data
        data['orion_subscription'] = orion_subscription
        data['orion_subscription_id'] = sub_id
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    @fiware_headers
    def retrieve(self, request, pk=None, fiware_service='',
                 fiware_service_path='/'):
        subscription = get_object_or_404(self.get_queryset(),
                                         pk=pk)
        serializer = self.serializer_class(subscription)
        return Response(serializer.data)

    @fiware_headers
    def destroy(self, request, pk=None, fiware_service='',
                fiware_service_path='/'):
        subscription = get_object_or_404(self.get_queryset(), pk=pk)
        osc = OrionSubscriptionClient()
        osc.delete_subscription(
            subscription.orion_subscription_id,
            fiware_service,
            fiware_service_path)
        self.perform_destroy(subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @fiware_headers
    def get_queryset(self, fiware_service, fiware_service_path):
        return Subscription.objects.filter(
                   fiware_service=fiware_service,
                   fiware_service_path=fiware_service_path)


class ListResultView(APIView):
    @fiware_headers
    def get(self, request, fiware_service, fiware_service_path):
        faas_driver = FaaSDriver.get_faas_driver()
        results = faas_driver.list_result(fiware_service, fiware_service_path)
        return Response(results)


class RetrieveResultView(APIView):
    @fiware_headers
    def get(self, request, pk, fiware_service, fiware_service_path):
        faas_driver = FaaSDriver.get_faas_driver()
        result = faas_driver.retrieve_result(pk, fiware_service, fiware_service_path)
        return Response(result)

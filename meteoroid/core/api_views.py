from .models import Function
from .serializers import FunctionSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .libs.faas_driver import FaaSDriver
from .libs.decorators import fiware_headers, extract_faas_function_param


class FunctionViewSet(viewsets.ModelViewSet):
    serializer_class = FunctionSerializer
    http_method_names = ['get', 'post', 'head', 'put']

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

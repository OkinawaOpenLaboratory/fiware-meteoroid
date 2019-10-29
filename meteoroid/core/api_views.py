from .models import Function
from .models import Result
from .serializers import FunctionSerializer
from .serializers import ResultSerializer
from rest_framework import viewsets


class FunctionViewSet(viewsets.ModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        fiware_service = self.request.META.get('HTTP_FIWARE_SERVICE', '')
        fiware_service_path = self.request.META.get('HTTP_FIWARE_SERVICEPATH', '/')
        return Result.objects.filter(fiware_service=fiware_service,
                                     fiware_service_path=fiware_service_path)

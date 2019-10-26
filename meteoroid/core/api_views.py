from .models import Function
from .serializers import FunctionSerializer
from rest_framework import viewsets


class FunctionViewSet(viewsets.ModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer

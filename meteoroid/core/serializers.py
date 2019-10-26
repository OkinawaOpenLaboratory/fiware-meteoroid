from rest_framework import serializers
from . import models


class FunctionSerializer(serializers.ModelSerializer):
    # TODO: Write fields of FaaS

    class Meta:
        model = models.Function
        fields = '__all__'

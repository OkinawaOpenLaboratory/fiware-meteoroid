from rest_framework import serializers
from .models import Function


class FunctionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    parameters = serializers.SerializerMethodField()
    fiware_service = serializers.CharField(max_length=64, default='')
    fiware_service_path = serializers.CharField(max_length=64, default='/')

    def __init__(self, *args, **kwargs):
        self.faas_functions = kwargs.pop('faas_functions', '')
        super(FunctionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Function
        fields = '__all__'

    # TODO: Get by self.faas_functions
    def get_name(self, obj):
        return 'name'

    def get_code(self, obj):
        return 'code'

    def get_language(self, obj):
        return 'language'

    def get_version(self, obj):
        return 'version'

    def get_parameters(self, obj):
        return [{'key': 'key', 'value': 'value'}]


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Result
        fields = '__all__'

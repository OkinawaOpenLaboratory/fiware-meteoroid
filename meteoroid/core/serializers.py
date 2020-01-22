from rest_framework import serializers

from .models import Endpoint, Function, Subscription


class FunctionSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    binary = serializers.SerializerMethodField()
    main = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    parameters = serializers.SerializerMethodField()
    fiware_service = serializers.CharField(max_length=64, default='', allow_blank=True)
    fiware_service_path = serializers.CharField(max_length=64, default='/')

    def __init__(self, *args, **kwargs):
        self.faas_function_data = kwargs.pop('faas_function_data', '')
        super(FunctionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Function
        fields = '__all__'

    def get_code(self, obj):
        return self.get_value(obj.name, 'code')

    def get_binary(self, obj):
        binary = self.get_value(obj.name, 'binary', default=False)
        return binary

    def get_main(self, obj):
        return self.get_value(obj.name, 'main')

    def get_language(self, obj):
        return self.get_value(obj.name, 'language')

    def get_version(self, obj):
        return self.get_value(obj.name, 'version')

    def get_parameters(self, obj):
        return self.get_value(obj.name, 'parameters')

    def get_value(self, function_name, value_name, default=''):
        if not isinstance(self.faas_function_data, list):
            if value_name in self.faas_function_data:
                return self.faas_function_data[value_name]
            return default
        for function in self.faas_function_data:
            if function['name'] == function_name:
                if value_name in function:
                    return function[value_name]
        return default


class EndpointSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.faas_endpoint_data = kwargs.pop('faas_endpoint_data', '')
        super(EndpointSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Endpoint
        fields = '__all__'

    def get_url(self, obj):
        if not isinstance(self.faas_endpoint_data, list):
            if 'url' in self.faas_endpoint_data:
                return self.faas_endpoint_data['url']
        else:
            for endpoint in self.faas_endpoint_data:
                if obj.equals_faas_data(endpoint):
                    return endpoint['url']
        return ''


class SubscriptionSerializer(serializers.ModelSerializer):
    fiware_service = serializers.CharField(max_length=64, default='', allow_blank=True)
    fiware_service_path = serializers.CharField(max_length=64, default='/')
    endpoint_id = serializers.PrimaryKeyRelatedField(queryset=Endpoint.objects.filter())
    orion_subscription_id = serializers.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(SubscriptionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Subscription
        fields = '__all__'

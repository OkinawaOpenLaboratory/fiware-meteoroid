from django.db import models


class FIWAREBase(models.Model):
    fiware_service = models.CharField(max_length=64, default='', blank=True)
    fiware_service_path = models.CharField(max_length=64, default='/')

    class Meta:
        abstract = True


class Function(FIWAREBase):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.fiware_service}{self.fiware_service_path} {self.name}'

    class Meta:
        unique_together = ('name', 'fiware_service', 'fiware_service_path')


class Endpoint(FIWAREBase):
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=64)
    method = models.CharField(max_length=8)
    function = models.ForeignKey(Function, on_delete=models.CASCADE, related_name='endpoints')

    def __str__(self):
        return f'{self.name}{self.path} {self.function.name} {self.method}'

    class Meta:
        unique_together = ('name', 'path', 'method', 'fiware_service', 'fiware_service_path')

    def get_dict(self):
        return {
            'name': self.name,
            'path': self.path,
            'method': self.method,
            'function': self.function.id
        }

    def equals_faas_data(self, faas_data):
        function = Function.objects.filter(fiware_service=self.fiware_service,
                                           fiware_service_path=self.fiware_service_path).get(name=faas_data['action_name'])
        return self.name == faas_data['name'] and\
            self.path == faas_data['path'] and\
            self.method.lower() == faas_data['method'].lower() and\
            self.function == function


class Subscription(FIWAREBase):
    endpoint_id = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    orion_subscription_id = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.fiware_service}{self.fiware_service_path} {self.endpoint_id}'

    class Meta:
        unique_together = ('orion_subscription_id', 'fiware_service', 'fiware_service_path')

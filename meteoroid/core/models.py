from django.db import models


class FIWAREBase(models.Model):
    fiware_service = models.CharField(max_length=64, default='', blank=True)
    fiware_service_path = models.CharField(max_length=64, default='/')

    class Meta:
        abstract = True


class Function(FIWAREBase):

    def __str__(self):
        return f'{self.fiware_service}{self.fiware_service_path}'


class Result(FIWAREBase):
    function_id = models.CharField(max_length=36)

    def __str__(self):
        return f'{self.fiware_service}{self.fiware_service_path}'

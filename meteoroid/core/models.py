from django.db import models


class FIWAREBase(models.Model):
    fiware_service = models.CharField(max_length=64, default='', blank=True)
    fiware_service_path = models.CharField(max_length=64, default='/')

    class Meta:
        abstract = True


class Function(FIWAREBase):
    pass

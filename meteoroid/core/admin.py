from django.contrib import admin

from . import models

admin.site.register(models.Function)
admin.site.register(models.Endpoint)
admin.site.register(models.Subscription)

from django.urls import path

from rest_framework import routers

from .api_views import (EndpointViewSet, FunctionViewSet, ListResultView,
                        RetrieveResultLogsView, RetrieveResultView,
                        ScheduleViewSet, SubscriptionViewSet)

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'functions', FunctionViewSet, basename='function')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'endpoints', EndpointViewSet, basename='endpoints')
router.register(r'schedules', ScheduleViewSet, basename='schedules')

urlpatterns = router.urls
urlpatterns += [
    path(r'results', ListResultView.as_view()),
    path(r'results/<pk>', RetrieveResultView.as_view()),
    path(r'results/<pk>/logs', RetrieveResultLogsView.as_view()),
]

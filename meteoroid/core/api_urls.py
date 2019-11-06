from django.urls import path
from rest_framework import routers

from .api_views import FunctionViewSet
from .api_views import SubscriptionViewSet
from .api_views import ListResultView
from .api_views import RetrieveResultView
from .api_views import EndpointViewSet


router = routers.SimpleRouter()
router.register(r'functions', FunctionViewSet, base_name='function')
router.register(r'subscriptions', SubscriptionViewSet, base_name='subscription')
router.register(r'endpoints', EndpointViewSet, base_name='endpoints')

urlpatterns = router.urls
urlpatterns += [
    path(r'results', ListResultView.as_view()),
    path(r'results/<pk>', RetrieveResultView.as_view()),
]

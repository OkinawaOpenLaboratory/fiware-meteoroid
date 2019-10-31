from django.urls import path
from rest_framework import routers

from .api_views import FunctionViewSet
from .api_views import ListResultView
from .api_views import RetrieveResultView


router = routers.SimpleRouter()
router.register(r'functions', FunctionViewSet, base_name='function')

urlpatterns = router.urls
urlpatterns += [
    path(r'results', ListResultView.as_view()),
    path(r'results/<pk>', RetrieveResultView.as_view()),
]

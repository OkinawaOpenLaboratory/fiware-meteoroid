from rest_framework import routers
from .api_views import FunctionViewSet
from .api_views import ResultViewSet

router = routers.SimpleRouter()
router.register(r'functions', FunctionViewSet)
router.register(r'results', ResultViewSet)

urlpatterns = router.urls

from rest_framework import routers
from .api_views import FunctionViewSet

router = routers.SimpleRouter()
router.register(r'functions', FunctionViewSet)

urlpatterns = router.urls

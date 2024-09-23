from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls

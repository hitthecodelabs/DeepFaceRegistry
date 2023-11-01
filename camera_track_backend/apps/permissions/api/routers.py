from rest_framework.routers import DefaultRouter
from apps.permissions.api.view.permissions_viewset import PermissionsViewSet

router = DefaultRouter()
router.register(r'permissions', PermissionsViewSet, basename='permissions')
urlpatterns = router.urls

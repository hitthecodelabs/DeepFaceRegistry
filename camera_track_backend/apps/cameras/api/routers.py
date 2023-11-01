from rest_framework.routers import DefaultRouter
from apps.cameras.api.views.cameras_viewset import CameraViewSet

router = DefaultRouter()
router.register(r'cameras', CameraViewSet, basename='cameras')
urlpatterns = router.urls

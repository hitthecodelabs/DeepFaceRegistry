from rest_framework.routers import DefaultRouter
from apps.clips.api.views.clips_viewset import ClipViewSet

router = DefaultRouter()
router.register(r'clips', ClipViewSet, basename='clips')
urlpatterns = router.urls

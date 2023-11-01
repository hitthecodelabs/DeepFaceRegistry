from django.urls import path

from apps.cameras.api.views.cameras_viewset import (
    CameraHistoricChanges,
    CameraHistoricGroupByMonthListView,
    CameraListAPIView,
    TotalCamerasView,
    VideoViewSet,)

urlpatterns = [
    path('camera/<int:pk>/live',
         VideoViewSet.as_view({'get': 'show_video_stream'}),
         name="video_viewset"),
    path('camera/stream_recognition',
         VideoViewSet.as_view({'get': 'show_video_stream_recognition'}),
         name="video_viewset"),
     path('camera/save_recognition_person',
         VideoViewSet.as_view({'post': 'save_recognition_person'}),
         name="video_viewset"),
    path('cameras/', TotalCamerasView.as_view(), name="total_cameras"),
    path('cameras_history/', CameraHistoricChanges.as_view(), name="cameras_history"),
    path('cameras_list/', CameraListAPIView.as_view(), name="cameras_list"),
    path('cameras_per_month/', CameraHistoricGroupByMonthListView.as_view(), name="cameras_per_month")
]

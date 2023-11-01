from django.urls import path

from apps.clips.api.views.clips_viewset import (
    TotalClipsView,
    ClipsCreateAPIView,
    ClipsListAPIView,
    ClipHistoricGroupByMonthListView,
    ClipRetrieveAPIView
)

urlpatterns = [
    path('clips/', TotalClipsView.as_view(), name="total_clips"),
    path('create_clip/', ClipsCreateAPIView.as_view(), name="create_clip"),
    path('get_clip/<int:pk>/', ClipRetrieveAPIView.as_view(), name="get_clip"),
    path('list_clips/', ClipsListAPIView.as_view(), name="list_clips"),
    path('clips_per_month/', ClipHistoricGroupByMonthListView.as_view(), name="clips_per_month")
]

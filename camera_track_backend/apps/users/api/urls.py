from django.urls import path

from apps.users.api.views.users_viewset import (TotalUsersView,
                                                UserHistoricalAPIView,
                                                FaceCaptureCreateAPIView,
                                                FaceCaptureListAPIView)

urlpatterns = [
    path('total_users/', TotalUsersView.as_view(), name='total_users'),
    path('historical_users/', UserHistoricalAPIView.as_view(), name='historical_users'),
    path('save_face_capture/', FaceCaptureCreateAPIView.as_view(), name='save_face_capture'),
    path('get_face_capture/', FaceCaptureListAPIView.as_view(), name='get_face_capture'),
]

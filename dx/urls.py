from django.urls import path

from .views import (
    DiagnosisCodeGetUpdateDeleteAPIView,
    DiagnosisCodeListAPIView,
    DiagnosisCodeUploadAPIView,
    DiagnosisCreateAPIView,
)

urlpatterns = [
    path("list-diagnosis-codes/", DiagnosisCodeListAPIView.as_view(), name="diagnosis-code-list"),
    path("create-diagnosis-code/", DiagnosisCreateAPIView.as_view(), name="diagnosis-code-create"),
    path(
        "diagnosis-code/<int:pk>/",
        DiagnosisCodeGetUpdateDeleteAPIView.as_view(),
        name="diagnosis-code-get-update-delete",
    ),
    path("diagnosis-codes/upload/", DiagnosisCodeUploadAPIView.as_view(), name="diagnosis-code-upload"),
]

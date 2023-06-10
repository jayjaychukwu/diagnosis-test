from django.urls import path

from .views import DiagnosisCodeListAPIView, DiagnosisCreateAPIView

urlpatterns = [
    path("list-diagnosis-codes/", DiagnosisCodeListAPIView.as_view(), name="diagnosis-code-list"),
    path("create-diagnosis-code/", DiagnosisCreateAPIView.as_view(), name="diagnosis-code-create"),
]

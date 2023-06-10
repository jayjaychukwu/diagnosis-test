from django.urls import path

from .views import DiagnosisCodeListCreateAPIView

urlpatterns = [
    path("diagnosis-codes/", DiagnosisCodeListCreateAPIView.as_view(), name="diagnosis-code-list-create"),
]

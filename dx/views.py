from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from rest_framework import generics

from .models import DiagnosisCode
from .serializers import (
    CreateDiagnosisCodeSerializer,
    FullDiagnosisCodeDetailsSerializer,
)


class DiagnosisCodeListAPIView(generics.ListAPIView):
    queryset = DiagnosisCode.objects.order_by("id")
    serializer_class = FullDiagnosisCodeDetailsSerializer

    # cache the list for 20 seconds anf set max-age directive to 30 seconds
    @method_decorator(cache_page(20))
    @method_decorator(cache_control(max_age=30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DiagnosisCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateDiagnosisCodeSerializer


# class DiagnosisCodeRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = DiagnosisCode.objects.all()
#     serializer_class = DiagnosisCodeSerializer

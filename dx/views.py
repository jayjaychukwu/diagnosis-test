from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from rest_framework import generics

from .models import DiagnosisCode
from .serializers import DiagnosisCodeSerializer


class DiagnosisCodeListCreateAPIView(generics.ListCreateAPIView):
    queryset = DiagnosisCode.objects.order_by("id")
    serializer_class = DiagnosisCodeSerializer

    # cache the list for 10 seconds anf set max-age directive to 30 seconds
    @method_decorator(cache_page(10))
    @method_decorator(cache_control(max_age=30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # disable caching for create operation
    @method_decorator(cache_control(no_cache=True, must_revalidate=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

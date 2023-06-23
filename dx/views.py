from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import DiagnosisCode
from .serializers import (
    CreateDiagnosisCodeSerializer,
    DiagnosisCodeCSVSerializer,
    FullDiagnosisCodeDetailsSerializer,
)
from .signals import file_uploaded_signal
from .utils import InvalidCSVFormatError, process_csv_file, save_diagnosis_codes


class DiagnosisCodeListAPIView(generics.ListAPIView):
    queryset = DiagnosisCode.objects.order_by("id")
    serializer_class = FullDiagnosisCodeDetailsSerializer

    # cache the list for 20 seconds and set max-age directive to 30 seconds
    @method_decorator(cache_page(20))
    @method_decorator(cache_control(max_age=30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DiagnosisCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateDiagnosisCodeSerializer


class DiagnosisCodeGetUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiagnosisCode.objects.all()
    serializer_class = FullDiagnosisCodeDetailsSerializer

    @method_decorator(cache_page(20))
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )  # Set partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class DiagnosisCodeUploadAPIView(generics.GenericAPIView):
    serializer_class = DiagnosisCodeCSVSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            csv_file = serializer.validated_data.get("csv_file")
            user_email = serializer.validated_data.get("email")

            try:
                # process the CSV file and create diagnosis code records

                # call the function to process the file
                diagnosis_code_objects = process_csv_file(uploaded_file=csv_file)

                with transaction.atomic():
                    save_diagnosis_codes(diagnosis_codes=diagnosis_code_objects)

                # emit the file_uploaded signal
                file_uploaded_signal.send(
                    sender=self.__class__,
                    user_email=user_email,
                    uploaded_file_name=csv_file.name,
                )
                return Response(
                    {
                        "message": "CSV file uploaded and processed succesfully",
                    },
                    status=status.HTTP_200_OK,
                )

            except InvalidCSVFormatError:
                return Response({"error": "invalid CSV file format"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

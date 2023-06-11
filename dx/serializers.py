from rest_framework import serializers

from .models import DiagnosisCode


class FullDiagnosisCodeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisCode
        fields = "__all__"


class CreateDiagnosisCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisCode
        exclude = [
            "icd_version",
        ]


class DiagnosisCodeCSVSerializer(serializers.Serializer):
    email = serializers.EmailField()
    csv_file = serializers.FileField()

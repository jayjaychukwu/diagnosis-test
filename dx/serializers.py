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

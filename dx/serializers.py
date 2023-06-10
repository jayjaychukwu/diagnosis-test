from rest_framework import serializers

from .models import DiagnosisCode


class DiagnosisCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisCode
        exclude = [
            "icd_version",
        ]

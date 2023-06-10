from django.test import TestCase

from ..models import DiagnosisCode


class DiagnosisCodeTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.diagnosis_code_data = {
            "category_code": "A0",
            "diagnosis_code": "1234",
            "full_code": "A01234",
            "abbreviated_description": "Comma-ind anal ret",
            "full_description": "Comma-induced anal retention",
            "category_title": "Malignant neoplasm of anus and anal canal",
        }
        cls.diagnosis_code = DiagnosisCode.objects.create(**cls.diagnosis_code_data)

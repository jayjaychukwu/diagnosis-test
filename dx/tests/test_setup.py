from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import DiagnosisCode


class DiagnosisCodeTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # diagnosis code data
        cls.diagnosis_code_data = {
            "category_code": "A0",
            "diagnosis_code": "1234",
            "full_code": "A01234",
            "abbreviated_description": "Comma-ind anal ret",
            "full_description": "Comma-induced anal retention",
            "category_title": "Malignant neoplasm of anus and anal canal",
        }

        # diagnosis code object
        cls.diagnosis_code = DiagnosisCode.objects.create(**cls.diagnosis_code_data)

        # set up the client
        cls.client = APIClient()

        # payload update data
        cls.payload = {
            "category_code": "B0",
            "diagnosis_code": "5678",
            "full_code": "B05678",
            "abbreviated_description": "Updated Description",
            "full_description": "Updated Full Description",
            "category_title": "Updated Category Title",
        }

        # urls
        cls.diagnosis_code_list_url = reverse("diagnosis-code-list")
        cls.diagnosis_code_create_url = reverse("diagnosis-code-create")
        cls.diagnosis_code_get_update_delete_url = reverse(
            "diagnosis-code-get-update-delete", kwargs={"pk": cls.diagnosis_code.id}
        )

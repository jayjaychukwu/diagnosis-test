from rest_framework import status

from ..models import DiagnosisCode
from .test_setup import DiagnosisCodeTestSetup


class DiagnosisCodeAPITest(DiagnosisCodeTestSetup):
    def test_create_diagnosis_code(self):
        url = self.diagnosis_code_list_create_url
        response = self.client.post(url, self.diagnosis_code_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiagnosisCode.objects.count(), 2)  # Two records, plus the one from setup

    def test_list_diagnosis_codes(self):
        url = self.diagnosis_code_list_create_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)  # Only one from setup

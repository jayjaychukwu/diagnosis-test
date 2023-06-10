import json

from rest_framework import status

from ..models import DiagnosisCode
from .test_setup import DiagnosisCodeTestSetup


class DiagnosisCodeAPITest(DiagnosisCodeTestSetup):
    def test_create_diagnosis_code(self):
        url = self.diagnosis_code_create_url
        response = self.client.post(url, self.diagnosis_code_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiagnosisCode.objects.count(), 2)  # Two records, plus the one from setup

    def test_list_diagnosis_codes(self):
        url = self.diagnosis_code_list_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)  # Only one from setup

    def test_get_diagnosis_code(self):
        url = self.diagnosis_code_get_update_delete_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.diagnosis_code.id)

    def test_update_diagnosis_code(self):
        url = self.diagnosis_code_get_update_delete_url
        response = self.client.patch(url, data=json.dumps(self.payload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.diagnosis_code.id)
        self.assertEqual(response.data.get("abbreviated_description"), self.payload.get("abbreviated_description"))

        # check if the changes were saved in the database
        updated_diagnosis_code = DiagnosisCode.objects.get(id=self.diagnosis_code.id)
        self.assertEqual(updated_diagnosis_code.abbreviated_description, self.payload.get("abbreviated_description"))

    def test_delete_diagnosis_code(self):
        url = self.diagnosis_code_get_update_delete_url
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the diagnosis code was deleted from the database
        with self.assertRaises(DiagnosisCode.DoesNotExist):
            DiagnosisCode.objects.get(id=self.diagnosis_code.id)

    def test_put_diagnosis_code(self):
        url = self.diagnosis_code_get_update_delete_url
        response = self.client.put(url, data=self.payload)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotEqual(response.data.get("detail"), ["PUT"])

        # Verify that the diagnosis code was not updated
        updated_diagnosis_code = DiagnosisCode.objects.get(id=self.diagnosis_code.id)
        self.assertNotEqual(
            updated_diagnosis_code.abbreviated_description, self.payload.get("abbreviated_description")
        )

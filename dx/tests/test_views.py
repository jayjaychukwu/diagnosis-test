import json
from io import BytesIO

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
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
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotEqual(response.data.get("detail"), ["PUT"])

        # Verify that the diagnosis code was not updated
        updated_diagnosis_code = DiagnosisCode.objects.get(id=self.diagnosis_code.id)
        self.assertNotEqual(
            updated_diagnosis_code.abbreviated_description, self.payload.get("abbreviated_description")
        )


class DiagnosisCodeUploadAPIViewTest(DiagnosisCodeTestSetup):
    def setUp(self) -> None:
        # open the CSV file
        with open(self.valid_csv_file_path, "rb") as file:
            file_content = file.read()

        # create a file-like object using BytesIO
        file_obj = BytesIO(file_content)

        # create a SimpleUploadedFile using the file-like object
        self.valid_uploaded_file = SimpleUploadedFile("valid_test.csv", file_obj.read(), content_type="text/csv")

        return super().setUp()

    def test_post_valid_csv_file(self):
        # data
        data = {"csv_file": self.valid_uploaded_file, "email": "testuser@mail.com"}

        # create a request with the csv file
        response = self.client.post(self.diagnosis_upload_url, data, format="multipart")

        # assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains an error message indicating an invalid CSV file format
        self.assertEqual(response.data, {"message": "CSV file uploaded and processed succesfully"})

    def test_post_invalid_csv_file(self):
        csv_data = b"column1,column2,column3\nvalue1,value2,value3\n"

        file_obj = BytesIO(csv_data)

        # Create a SimpleUploadedFile using the file-like object
        uploaded_file = SimpleUploadedFile("test.csv", file_obj.read(), content_type="text/csv")

        # data
        data = {"csv_file": uploaded_file, "email": "testuser@mail.com"}
        # request
        response = self.client.post(self.diagnosis_upload_url, data, format="multipart")

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that the response contains an error message indicating an invalid CSV file format
        self.assertEqual(response.data, {"error": "invalid CSV file format"})

    def test_send_upload_notification(self):
        # data
        data = {"csv_file": self.valid_uploaded_file, "email": "testuser@mail.com"}

        # create a request with the csv file
        response = self.client.post(self.diagnosis_upload_url, data, format="multipart")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Upload Notification")
        self.assertEqual(
            mail.outbox[0].body, f"Your file '{self.valid_uploaded_file.name}' was successfully uploaded."
        )
        self.assertEqual(
            mail.outbox[0].from_email, "no-reply@pharmaceuticals.com"
        )  # Adjust the expected sender email address
        self.assertEqual(mail.outbox[0].to, [data.get("email")])

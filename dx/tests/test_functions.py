import io

from django.core import mail
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..models import DiagnosisCode
from ..utils import (
    InvalidCSVFormatError,
    process_csv_file,
    save_diagnosis_codes,
    send_upload_notification,
)


class ProcessCSVFileTestCase(TestCase):
    def test_process_csv_file_with_uploaded_file(self):
        # CSV data
        csv_data = "A00,0,A000,Cholera due to Vibrio cholerae 01, biovar cholerae,Cholera\nA00,1,A001,Cholera due to Vibrio cholerae 01, biovar eltor,Cholera"
        csv_file = InMemoryUploadedFile(
            io.BytesIO(csv_data.encode("utf-8")), None, "test.csv", "text/csv", len(csv_data), None
        )

        unsaved_instances = process_csv_file(uploaded_file=csv_file)

        # assert that the DiagnosisCode instances have been created
        self.assertEqual(len(unsaved_instances), 2)

    def test_process_csv_file_with_file_path(self):
        file_path = "dx/tests/test_file.csv"

        unsaved_instances = process_csv_file(file_path=file_path)

        # assert that the DiagnosisCode instances have been created
        self.assertEqual(len(unsaved_instances), 3)

    def test_process_csv_file_with_invalid_csv_format(self):
        csv_data = "A00,0,A000,Cholera due to Vibrio cholerae 01, biovar cholerae,Cholera\nA00,1,A001"  # Invalid number of columns
        csv_file = InMemoryUploadedFile(
            io.BytesIO(csv_data.encode("utf-8")), None, "test.csv", "text/csv", len(csv_data), None
        )

        with self.assertRaises(InvalidCSVFormatError):
            process_csv_file(uploaded_file=csv_file)

    def test_process_csv_file_with_invalid_file_format(self):
        file_path = "dx/tests/invalid_test_file.csv"  # Invalid file format

        with self.assertRaises(InvalidCSVFormatError):
            process_csv_file(file_path=file_path)


class SaveDiagnosisCodesTestCase(TestCase):
    def test_save_diagnosis_codes(self):
        # Create a list of DiagnosisCode instances
        diagnosis_codes = [
            DiagnosisCode(
                category_code="A",
                diagnosis_code="001",
                full_code="A001",
                abbreviated_description="ABCXXDD",
                full_description="abcABCddd",
                category_title="cccddddsss",
            ),
            # DiagnosisCode(category_code='B', diagnosis_code='002', ...),
            # DiagnosisCode(category_code='C', diagnosis_code='003', ...),
        ]

        # Call the save_diagnosis_codes function
        save_diagnosis_codes(diagnosis_codes)

        # Retrieve all DiagnosisCode objects from the database
        saved_instances = DiagnosisCode.objects.all()

        # Assert that the saved_instances count matches the original diagnosis_codes count
        self.assertEqual(saved_instances.count(), len(diagnosis_codes))


class SendUploadNotificationTestCase(TestCase):
    def test_send_upload_notification(self):
        user_email = "user@example.com"
        uploaded_file_name = "diagnosis_codes.csv"

        send_upload_notification(sender=None, user_email=user_email, uploaded_file_name=uploaded_file_name)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Upload Notification")
        self.assertEqual(mail.outbox[0].body, f"Your file '{uploaded_file_name}' was successfully uploaded.")
        self.assertEqual(mail.outbox[0].from_email, "no-reply@pharmaceuticals.com")
        self.assertEqual(mail.outbox[0].to, [user_email])

import io

from django.core import mail
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..models import DiagnosisCode
from ..utils import process_csv_file, send_upload_notification
from .test_setup import DiagnosisCodeTestSetup


class ProcessCSVFileTestCase(TestCase):
    # @override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
    def test_process_csv_file_with_uploaded_file(self):
        # CSV data

        csv_data = "A00,0,A000,Cholera due to Vibrio cholerae 01, biovar cholerae,Cholera\nA00,1,A001,Cholera due to Vibrio cholerae 01, biovar eltor,Cholera"
        csv_file = InMemoryUploadedFile(
            io.BytesIO(csv_data.encode("utf-8")), None, "test.csv", "text/csv", len(csv_data), None
        )
        process_csv_file(uploaded_file=csv_file)

        # assert that the DiagnosisCode instances have been created
        self.assertEqual(DiagnosisCode.objects.count(), 2)

    def test_process_csv_file_with_file_path(self):
        file_path = "dx/tests/test_file.csv"
        process_csv_file(file_path=file_path)

        # assert that the DiagnosisCode instances have been created
        self.assertEqual(DiagnosisCode.objects.count(), 3)


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

import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..models import DiagnosisCode
from ..utils import process_csv_file
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

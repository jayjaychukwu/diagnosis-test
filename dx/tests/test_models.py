from datetime import datetime

from django.test import TestCase

from ..models import DiagnosisCode
from .test_setup import DiagnosisCodeTestSetup


class DiagnosisCodeModelTest(DiagnosisCodeTestSetup):
    def test_icd_version_default(self):
        self.assertEqual(self.diagnosis_code.icd_version, "ICD-10")

    def test_set_icd_version(self):
        new_version = "ICD-11"
        self.diagnosis_code.set_icd_version(new_version)
        self.assertEqual(self.diagnosis_code.icd_version, new_version)

    def test_created_at(self):
        self.assertIsInstance(self.diagnosis_code.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.diagnosis_code.updated_at, datetime)

    def test_string_representation(self):
        expected_string = self.diagnosis_code_data["full_code"]
        self.assertEqual(str(self.diagnosis_code), expected_string)

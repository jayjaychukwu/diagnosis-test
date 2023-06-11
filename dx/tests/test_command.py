from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


class DiagnosisCodeCommandTestCase(TestCase):
    def setUp(self) -> None:
        self.path_to_valid_csv_file = "dx/tests/test_file.csv"
        self.path_to_invalid_csv_file = "dx/tests/invalid_test_file.csv"
        return super().setUp()

    def test_command_with_valid_csv_file(self):
        # Run the command
        with patch("sys.stdout", new=StringIO()) as stdout:
            call_command("createdata", "--file", self.path_to_valid_csv_file)

            # Check the command output
            output = stdout.getvalue().strip()
            self.assertEqual(output, "DiagnosisCode records created successfully")

    def test_command_with_invalid_csv_file(self):
        # Run the command
        with patch("sys.stdout", new=StringIO()) as stdout:
            call_command("createdata", "--file", self.path_to_invalid_csv_file)

            # Check the command output
            output = stdout.getvalue().strip()
            self.assertEqual(output, "Invalid CSV file")

    def test_command_without_csv_file(self):
        # Run the command without providing a CSV file path
        with patch("sys.stdout", new=StringIO()) as stdout:
            call_command("createdata")

            # Check the command output
            output = stdout.getvalue().strip()
            self.assertEqual(output, "Please provide a CSV file path using -f or --file")

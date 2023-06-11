from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from ...utils import InvalidCSVFormatError, process_csv_file


class Command(BaseCommand):
    help = "Creates DiagnosisCode records from a CSV file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-f", "--file", type=str, help="Path to the CSV file")

    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_file_path = options.get("file")

        if not csv_file_path:
            self.stdout.write(self.style.ERROR("Please provide a CSV file path using -f or --file"))
            return

        try:
            process_csv_file(file_path=csv_file_path)
            self.stdout.write(self.style.SUCCESS("DiagnosisCode records created successfully"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("CSV file not found"))
        except InvalidCSVFormatError:
            self.stdout.write(self.style.ERROR("Invalid CSV file"))

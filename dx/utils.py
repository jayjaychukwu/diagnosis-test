import csv
from itertools import islice
from typing import List

from django.core.files.uploadedfile import UploadedFile
from django.core.mail import send_mail
from django.dispatch import receiver

from .models import DiagnosisCode
from .signals import file_uploaded_signal


class InvalidCSVFormatError(Exception):
    pass


import csv
from typing import List, Optional


def process_csv_file(
    uploaded_file: Optional[UploadedFile] = None,
    file_path: Optional[str] = None,
) -> List[DiagnosisCode]:
    """
    Takes in either an uploaded_file or a file_path, processes the CSV file and returns a list of uncommitted DiagnosisCode objects

    Args:
        uploaded_file (Optional[_type_], optional): the uploaded file from a POST request. Defaults to None.
        file_path (Optional[_type_], optional): the directory path to the CSV file. Defaults to None.

    Raises:
        InvalidCSVFormatError: when neither uploaded_file nor file_path was passed to the function. detail: "Either 'uploaded_file' or 'file_path' must be provided."
        InvalidCSVFormatError: when both uploaded file and file path were passed to the function. detail: "Either 'uploaded_file' or 'file_path' must be provided, not both."
        InvalidCSVFormatError: detail: "Invalid number of columns in CSV"
        InvalidCSVFormatError: detail: "Invalid CSV file format"

    Returns:
        List[DiagnosisCode]: A list of DiagnosisCode records that have not been saved to the database
    """
    if uploaded_file is not None and file_path is not None:
        raise InvalidCSVFormatError("Either 'uploaded_file' or 'file_path' must be provided, not both.")
    elif uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
    elif file_path is not None:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    else:
        raise InvalidCSVFormatError("Either 'uploaded_file' or 'file_path' must be provided.")

    try:
        reader = csv.reader(content.splitlines())
        instances = []
        for row in reader:
            if len(row) < 6:
                raise InvalidCSVFormatError("Invalid number of columns in CSV")

            category_code = row[0].strip()
            diagnosis_code = row[1].strip()
            full_code = row[2].strip()
            abbreviated_description = row[3].strip()
            full_description = row[4].strip()
            category_title = row[5].strip()

            # create the diagnosis code record
            instance = DiagnosisCode(
                category_code=category_code,
                diagnosis_code=diagnosis_code,
                full_code=full_code,
                abbreviated_description=abbreviated_description,
                full_description=full_description,
                category_title=category_title,
            )
            instances.append(instance)

        return instances
    except csv.Error:
        raise InvalidCSVFormatError("Invalid CSV file format")


def save_diagnosis_codes(diagnosis_codes: List[DiagnosisCode], batch_size: int | None = None) -> None:
    """
    Saves a list of DiagnosisCode objects to the database using a batch_size in order to save in batches

    Args:
        diagnosis_codes (List[DiagnosisCode]): A list of DiagnosisCode objects
        batch_size (int | None): the batch size to utilize in saving the DiagnosisCode objects, if no value is passed, 200 will be used. Defaults to None.
    """
    if not batch_size:
        batch_size = 200  # number of instances to save in each batch

    for i in range(0, len(diagnosis_codes), batch_size):
        batch = diagnosis_codes[i : i + batch_size]
        DiagnosisCode.objects.bulk_create(batch)


@receiver(file_uploaded_signal)
def send_upload_notification(sender, **kwargs):
    user_email = kwargs.get("user_email")
    uploaded_file_name = kwargs.get("uploaded_file_name")

    subject = "Upload Notification"
    message = f"Your file '{uploaded_file_name}' was successfully uploaded."
    from_email = "no-reply@pharmaceuticals.com"
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

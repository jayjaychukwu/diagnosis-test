import csv

from django.core.mail import send_mail
from django.dispatch import receiver

from .models import DiagnosisCode
from .signals import file_uploaded_signal


class InvalidCSVFormatError(Exception):
    pass


def process_csv_file(uploaded_file=None, file_path=None):
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
    elif file_path is not None:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    elif uploaded_file is None and file_path is None:
        raise ValueError("Either 'uploaded_file' or 'file_path' must be provided.")

    try:
        reader = csv.reader(content.splitlines())
        instances = []
        for row in reader:
            if len(row) >= 6:
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
            else:
                raise InvalidCSVFormatError("Invalid number of columns in CSV")

        DiagnosisCode.objects.bulk_create(instances)
    except csv.Error:
        raise InvalidCSVFormatError("Invalid CSV file format")


@receiver(file_uploaded_signal)
def send_upload_notification(sender, **kwargs):
    user_email = kwargs.get("user_email")
    uploaded_file_name = kwargs.get("uploaded_file_name")

    subject = "Upload Notification"
    message = f"Your file '{uploaded_file_name}' was successfully uploaded."
    from_email = "no-reply@pharmaceuticals.com"
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

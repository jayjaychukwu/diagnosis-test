from django.db import models


class DiagnosisCode(models.Model):
    category_code = models.CharField(max_length=10)
    diagnosis_code = models.CharField(max_length=10)
    full_code = models.CharField(max_length=10)
    abbreviated_description = models.CharField(max_length=255)
    full_description = models.CharField(max_length=255)
    category_title = models.CharField(max_length=255)

    # Additional fields for versioning or tracking
    icd_version = models.CharField(max_length=10, default="ICD-10")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Add any additional constraints or indexes if required
        verbose_name = "Diagnosis Code"
        verbose_name_plural = "Diagnosis Codes"

    def __str__(self):
        return self.full_code

    def set_icd_version(self, version):
        self.icd_version = version
        self.save()

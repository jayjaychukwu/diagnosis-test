from django.contrib import admin

from .models import DiagnosisCode


class DiagnosisCodeAdmin(admin.ModelAdmin):
    list_display = ("category_code", "diagnosis_code", "full_code", "abbreviated_description")
    list_filter = ("category_code", "diagnosis_code")
    search_fields = ("category_code", "diagnosis_code", "full_code", "abbreviated_description")


admin.site.register(DiagnosisCode, DiagnosisCodeAdmin)

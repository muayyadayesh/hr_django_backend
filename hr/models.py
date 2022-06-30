from django.db import models
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError

from hr.storage.storage_backends import PrivateMediaStorage

# allowed choices --hardcoded (should be added as a model in production)
DEPARTMENT_CHOICES = [
    ("IT", "IT"),
    ("HR", "HR"),
    ("Finance", "Finance")
]

# candidate model


class Candidate(models.Model):
    full_name = models.CharField(max_length=250, blank=False)
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=False)
    experience_years = models.PositiveIntegerField(blank=False)
    department_id = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, blank=False)
    resume_file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])], blank=False)
    registration_date = models.DateTimeField(auto_now_add=True, blank=False)

    def clean(self):
        data = self.cleaned_data
        if data['experience_years'] < 1:
            raise ValidationError('experience years must be greater than 1!')

        if data['department_id'] not in DEPARTMENT_CHOICES:
            raise ValidationError('department id is not applicable!')


# S3 storage model
class PrivateDocument(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(storage=PrivateMediaStorage())

    def __str__(self):
        return self.full_name

# Generated by Django 4.0.5 on 2022-06-30 11:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_candidate_registration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='resume_file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]),
        ),
    ]
# Generated by Django 5.0.2 on 2024-04-10 21:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_result2_delete_result'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Result2',
            new_name='Result',
        ),
    ]

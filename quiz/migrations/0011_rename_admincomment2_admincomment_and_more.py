# Generated by Django 5.0.2 on 2024-04-14 20:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_rename_userresponse_userresponse2_admincomment2_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminComment2',
            new_name='AdminComment',
        ),
        migrations.RenameModel(
            old_name='UserResponse2',
            new_name='UserResponse',
        ),
    ]

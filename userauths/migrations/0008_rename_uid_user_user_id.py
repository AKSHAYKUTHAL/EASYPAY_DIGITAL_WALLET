# Generated by Django 4.2.5 on 2023-10-25 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0007_user_uid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='uid',
            new_name='user_id',
        ),
    ]
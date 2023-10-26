# Generated by Django 4.2.5 on 2023-09-16 18:13

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_acccount_id_account_account_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=10, max_length=20, prefix='217', unique=True),
        ),
    ]

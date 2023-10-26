# Generated by Django 4.2.5 on 2023-10-17 06:46

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_creditcard_month_alter_creditcard_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=14, max_length=14, prefix='47'),
        ),
    ]
# Generated by Django 4.2.5 on 2023-10-19 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_notification_card_number_notification_card_tier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='card_tier',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='card_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
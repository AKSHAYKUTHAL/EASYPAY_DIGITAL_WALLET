# Generated by Django 4.2.6 on 2023-10-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_account_credit_card_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='debit_card_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
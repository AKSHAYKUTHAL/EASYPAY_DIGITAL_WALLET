# Generated by Django 4.2.6 on 2023-11-01 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_transaction_transaction_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='forexdebitcard',
            name='card_currency',
            field=models.CharField(choices=[('INR', 'INR'), ('USD', 'USD')], default='USD', max_length=20),
        ),
    ]

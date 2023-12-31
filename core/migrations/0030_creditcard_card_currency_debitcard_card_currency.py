# Generated by Django 4.2.6 on 2023-11-01 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_forexdebitcard_card_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='card_currency',
            field=models.CharField(choices=[('INR', 'INR'), ('USD', 'USD')], default='INR', max_length=20),
        ),
        migrations.AddField(
            model_name='debitcard',
            name='card_currency',
            field=models.CharField(choices=[('INR', 'INR'), ('USD', 'USD')], default='INR', max_length=20),
        ),
    ]

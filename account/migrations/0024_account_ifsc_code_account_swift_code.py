# Generated by Django 4.2.6 on 2023-11-02 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_alter_accountforex_ifsc_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='ifsc_code',
            field=models.CharField(choices=[('EPDW00902', 'EPDW00902')], default='EPDWIN00902', max_length=11),
        ),
        migrations.AddField(
            model_name='account',
            name='swift_code',
            field=models.CharField(choices=[('EPDWINKL902', 'EPDWINKL902')], default='EPDWINKL902', max_length=11),
        ),
    ]

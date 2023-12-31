# Generated by Django 4.2.6 on 2023-11-01 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0027_transactionforeign_ifsc_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_status',
            field=models.CharField(choices=[('none', 'None'), ('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('cancelled', 'Cancelled'), ('processing', 'Processing'), ('request_sent', 'Request Sent'), ('request_processing', 'Request Processing'), ('request_settled', 'Request Settled'), ('request_declined', 'Request Declined'), ('Deposit Processing', 'Deposit Processing'), ('Deposit Completed', 'Deposit Completed'), ('Withdraw Processing', 'Withdraw Processing'), ('Withdraw Completed', 'Withdraw Completed')], default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('none', 'None'), ('transfer', 'Transfer'), ('recieved', 'Recieved'), ('withdraw', 'Withdraw'), ('refund', 'Refund'), ('request', 'Payment Request'), ('forex', 'Forex')], default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='transactionforeign',
            name='transaction_status',
            field=models.CharField(choices=[('none', 'None'), ('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('cancelled', 'Cancelled'), ('processing', 'Processing'), ('request_sent', 'Request Sent'), ('request_processing', 'Request Processing'), ('request_settled', 'Request Settled'), ('request_declined', 'Request Declined'), ('Deposit Processing', 'Deposit Processing'), ('Deposit Completed', 'Deposit Completed'), ('Withdraw Processing', 'Withdraw Processing'), ('Withdraw Completed', 'Withdraw Completed')], default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='transactionforeign',
            name='transaction_type',
            field=models.CharField(choices=[('none', 'None'), ('transfer', 'Transfer'), ('recieved', 'Recieved'), ('withdraw', 'Withdraw'), ('refund', 'Refund'), ('request', 'Payment Request'), ('forex', 'Forex')], default='None', max_length=100),
        ),
        migrations.CreateModel(
            name='ForexDebitCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit_card_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=20, prefix='CARD', unique=True)),
                ('card_pin_number', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=4, prefix='')),
                ('name', models.CharField(max_length=100)),
                ('number', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=14, max_length=16, prefix='47')),
                ('month', models.IntegerField(default=11)),
                ('year', models.IntegerField(default=2028)),
                ('cvv', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=3, max_length=3, prefix='')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('card_type', models.CharField(choices=[('master', 'Master'), ('visa', 'Visa'), ('rupay', 'Rupay')], default='master', max_length=20)),
                ('card_tier', models.CharField(choices=[('classic', 'Classic'), ('gold', 'Gold'), ('platinum', 'Platinum'), ('signature', 'Signature'), ('infinite', 'Infinite')], default='classic', max_length=20)),
                ('card_status', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

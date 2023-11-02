# Generated by Django 4.2.6 on 2023-11-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_transactionforex_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionforex',
            name='account_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_status',
            field=models.CharField(choices=[('none', 'None'), ('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('cancelled', 'Cancelled'), ('processing', 'Processing'), ('request_sent', 'Request Sent'), ('request_processing', 'Request Processing'), ('request_settled', 'Request Settled'), ('request_declined', 'Request Declined'), ('Deposit Processing', 'Deposit Processing'), ('Deposit Completed', 'Deposit Completed'), ('Withdraw Processing', 'Withdraw Processing'), ('Withdraw Completed', 'Withdraw Completed'), ('Forex Sent Processing', 'Forex Sent Processing'), ('Forex Sent Completed', 'Forex Sent Completed'), ('Forex Sent Failed', 'Forex Sent Failed')], default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='transactionforex',
            name='transaction_status',
            field=models.CharField(choices=[('none', 'None'), ('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('cancelled', 'Cancelled'), ('processing', 'Processing'), ('request_sent', 'Request Sent'), ('request_processing', 'Request Processing'), ('request_settled', 'Request Settled'), ('request_declined', 'Request Declined'), ('Deposit Processing', 'Deposit Processing'), ('Deposit Completed', 'Deposit Completed'), ('Withdraw Processing', 'Withdraw Processing'), ('Withdraw Completed', 'Withdraw Completed'), ('Forex Sent Processing', 'Forex Sent Processing'), ('Forex Sent Completed', 'Forex Sent Completed'), ('Forex Sent Failed', 'Forex Sent Failed')], default='None', max_length=100),
        ),
    ]
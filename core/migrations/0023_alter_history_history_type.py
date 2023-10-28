# Generated by Django 4.2.6 on 2023-10-28 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_debitcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='history_type',
            field=models.CharField(choices=[('None', 'None'), ('Transfer', 'Transfer'), ('Credit Alert', 'Credit Alert'), ('Debit Alert', 'Debit Alert'), ('Sent Payment Request', 'Sent Payment Request'), ('Recieved Payment Request', 'Recieved Payment Request'), ('Settled Payment Request To', 'Settled Payment Request To'), ('Settled Payment Request From', 'Settled Payment Request From'), ('Funded Credit Card', 'Funded Credit Card'), ('Withdrew Credit Card Funds', 'Withdrew Credit Card Funds'), ('Deleted Credit Card', 'Deleted Credit Card'), ('Added Credit Card', 'Added Credit Card'), ('Activated Credit Card', 'Activated Credit Card'), ('De-Activated Credit Card', 'De-Activated Credit Card'), ('Deleted Debit Card', 'Deleted Debit Card'), ('Added Debit Card', 'Added Debit Card'), ('Activated Debit Card', 'Activated Debit Card'), ('De-Activated Debit Card', 'De-Activated Debit Card')], default='none', max_length=100),
        ),
    ]

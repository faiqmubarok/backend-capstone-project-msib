# Generated by Django 5.1.3 on 2024-11-28 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_transaction_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(max_length=100),
        ),
    ]

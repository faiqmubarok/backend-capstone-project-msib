# Generated by Django 5.1.3 on 2024-11-27 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_project_invested_amount_portfolio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(max_length=20),
        ),
    ]

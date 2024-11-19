# Generated by Django 5.1.3 on 2024-11-16 17:19

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_userprofile_job_alter_userprofile_no_ktp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='projectLogos/')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('agriculture', 'Pertanian'), ('fishery', 'Perikanan'), ('farm', 'Peternakan')], default='agriculture', max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('total_funds', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('profit', models.DecimalField(decimal_places=2, help_text='Persentase keuntungan dalam rentang 0-100.', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('status', models.CharField(choices=[('ongoing', 'Sedang berlangsung'), ('available', 'Tersedia'), ('not_available', 'Tidak tersedia')], default='not_available', max_length=20)),
                ('description', models.TextField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='api.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='financialReports/')),
                ('file_name', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_reports', to='api.project')),
            ],
        ),
    ]

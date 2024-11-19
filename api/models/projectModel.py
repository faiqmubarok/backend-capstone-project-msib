from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .farmerModel import Farmer

class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Sedang berlangsung'),
        ('available', 'Tersedia'),
        ('not_available', 'Tidak tersedia'),
    ]
    TYPE_PROJECT = [
        ('agriculture', 'Pertanian'),
        ('fishery', 'Perikanan'),
        ('farm', 'Peternakan'),
    ]
    
    logo = models.ImageField(upload_to='projectLogos/', blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_PROJECT, default='agriculture')
    projectImage = models.ImageField(upload_to='projectImages/', blank=True, null=True)
    location = models.CharField(max_length=255)
    total_funds = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    profit = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0),  # Nilai minimal 0%
            MaxValueValidator(100) # Nilai maksimal 100%
        ],
        help_text="Persentase keuntungan dalam rentang 0-100."
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_available')
    description = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name
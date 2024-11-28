from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from .projectModel import Project
from .portfolioModel import Portfolio

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu'),
        ('success', 'Berhasil'),
        ('failed', 'Gagal'),
    ]

    TRANSACTION_TYPE = [
        ('withdraw', 'Tarik Dana'),
        ('deposit', 'Setor Dana'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    transaction_date = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username} - {self.amount} ({self.transaction_type})"

    class Meta:
        ordering = ['-transaction_date']
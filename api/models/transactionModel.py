from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from .projectModel import Project

class Transaction(models.Model):
    PAYMENT_METHODS = [
        ('bank_transfer', 'Bank Transfer'),
        ('e_wallet', 'E-Wallet'),
        ('credit_card', 'Credit Card'),
    ]

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    transaction_date = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username} - {self.amount} ({self.transaction_type})"

    class Meta:
        ordering = ['-transaction_date']
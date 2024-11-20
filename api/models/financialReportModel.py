from django.db import models
from .projectModel import Project
from django.core.validators import MinValueValidator, MaxValueValidator

class FinancialReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="financial_reports")
    file = models.FileField(upload_to='financialReports/')
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    profit = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0),  # Nilai minimal 0%
            MaxValueValidator(100) # Nilai maksimal 100%
        ],
        help_text="Persentase keuntungan dalam rentang 0-100."
    )

    def __str__(self):
        return f"{self.file_name} - {self.project.name}"
from django.db import models
from ..models.userModel import User
from ..models.projectModel import Project

class Portfolio(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='portfolios'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='portfolios'
    )
    ownership_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    invested_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio {self.user.username} - {self.project.name} - {self.invested_amount}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'],
                name='unique_user_project_transaction'
            )
        ]

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models.financialReportModel import FinancialReport
from .models.portfolioModel import Portfolio
from .models.projectModel import Project

@receiver(post_save, sender=FinancialReport)
def update_portfolios_and_project(sender, instance, created, **kwargs):
    if created:  # Hanya ketika report baru dibuat
        project = instance.project
        profit = instance.profit / 100  # Menghitung profit dalam bentuk desimal

        # Gunakan transaksi untuk memastikan data konsisten
        with transaction.atomic():
            # Mengupdate semua portfolio terkait proyek
            portfolios = Portfolio.objects.filter(project=project)
            for portfolio in portfolios:
                # Update invested_amount berdasarkan profit
                portfolio.invested_amount += portfolio.invested_amount * profit
                portfolio.save()

            # Update invested_amount pada proyek setelah update portfolio
            project.update_invested_amount()

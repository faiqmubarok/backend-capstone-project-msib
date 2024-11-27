from django.db import models
from rest_framework import serializers
from ..models.portfolioModel import Portfolio
from ..models.projectModel import Project
from ..models.transactionModel import Transaction

class ProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'logo', 'status_display', 'start_date', 'end_date']

    def get_status_display(self, obj):
        return obj.get_status_display()

class PortfolioSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    profit = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ['project', 'invested_amount', 'profit']

    def get_profit(self, obj):
        # Ambil transaksi yang terkait dengan portfolio dan project dari user yang sama
        transactions = Transaction.objects.filter(
            # portfolio=obj,
            project=obj.project,
            user=obj.user
        )

        # Hitung pemasukan (deposit) dan pengeluaran (withdraw)
        income = transactions.filter(transaction_type='deposit').aggregate(total_income=models.Sum('amount'))['total_income'] or 0
        expenses = transactions.filter(transaction_type='withdraw').aggregate(total_expenses=models.Sum('amount'))['total_expenses'] or 0

        # Hitung keuntungan = pemasukan - pengeluaran
        profit = income - expenses

        # Hitung keuntungan bersih = nilai investasi - keuntungan
        net_profit = obj.invested_amount - profit 

        return {
            'net_profit': net_profit,  # Keuntungan bersih
        }

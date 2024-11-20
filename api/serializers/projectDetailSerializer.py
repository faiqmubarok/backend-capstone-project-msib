from rest_framework import serializers
from ..models.farmerModel import Farmer
from ..models.financialReportModel import FinancialReport
from ..models.projectModel import Project
from django.db.models import Avg

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'name', 'photoProfile']

# Dalam FinancialReportSerializer
class FinancialReportSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = FinancialReport
        fields = ['id', 'file_name', 'profit', 'file_url']

    def get_file_url(self, obj):
        return obj.file.url  # Mengambil URL file dari ImageField/FileField


class ProjectDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'logo', 'type_display', 'location', 'target_funds', 'status_display', 'description', 'start_date', 'end_date', 'projectImage', 'profit']
    
    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_type_display(self, obj):
        return obj.get_type_display() 
    
    def get_profit(self, obj):
        # Menghitung rata-rata profit dari laporan keuangan terkait
        average_profit = obj.financial_reports.aggregate(Avg('profit'))['profit__avg']
        return round(average_profit, 2) if average_profit is not None else 0.0

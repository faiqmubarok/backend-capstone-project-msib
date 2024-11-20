from rest_framework import serializers
from ..models.projectModel import Project
from django.db.models import Avg

class ProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()


    class Meta:
        model = Project
        fields = ['id', 'logo', 'name', 'type_display', 'location','status_display', 'profit']

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_type_display(self, obj):
        return obj.get_type_display() 
    
    def get_profit(self, obj):
        # Menghitung rata-rata profit dari laporan keuangan terkait
        average_profit = obj.financial_reports.aggregate(Avg('profit'))['profit__avg']
        return round(average_profit, 2) if average_profit is not None else 0.0

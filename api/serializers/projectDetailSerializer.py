from rest_framework import serializers
from ..models.farmerModel import Farmer
from ..models.financialReportModel import FinancialReport
from ..models.projectModel import Project

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'name', 'phone', 'email', 'address']

# Dalam FinancialReportSerializer
class FinancialReportSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = FinancialReport
        fields = ['id', 'file_name', 'file_url', 'uploaded_at']

    def get_file_url(self, obj):
        return obj.file.url  # Mengambil URL file dari ImageField/FileField


class ProjectDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'logo', 'type_display', 'location', 'total_funds', 'profit', 'status_display', 'description', 'start_date', 'end_date', 'projectImage']
    
    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_type_display(self, obj):
        return obj.get_type_display() 

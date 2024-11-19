from rest_framework import serializers
from ..models.projectModel import Project

class ProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'logo', 'name', 'type_display', 'location', 'total_funds', 'status_display', 'profit']

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_type_display(self, obj):
        return obj.get_type_display() 

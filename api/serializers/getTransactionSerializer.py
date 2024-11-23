from rest_framework import serializers
from ..models.projectModel import Project
from ..models.transactionModel import Transaction

class ProjectSerializer(serializers.ModelSerializer):
    type_display = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'logo', 'name', 'type_display']

    def get_type_display(self, obj):
        return obj.get_type_display()

class GetTransactionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    payment_method_display = serializers.SerializerMethodField()
    transaction_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id', 
            'project', 
            'amount', 
            'payment_method_display', 
            'transaction_type_display', 
            'status_display', 
            'transaction_date'
        ]

    def get_payment_method_display(self, obj):
        return obj.get_payment_method_display()

    def get_transaction_type_display(self, obj):
        return obj.get_transaction_type_display()
    
    def get_status_display(self, obj):
        return obj.get_status_display()

from rest_framework import serializers
from ..models.transactionModel import Transaction

class TopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user_id', 'project_id', 'amount', 'payment_method', 'transaction_type', 'status', 'transaction_date']
        read_only_fields = ['id', 'transaction_type', 'status', 'transaction_date']




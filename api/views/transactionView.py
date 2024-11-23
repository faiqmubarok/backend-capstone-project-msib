from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..serializers.topupSerializer import TopupSerializer
from django.contrib.auth.models import User
from ..models.projectModel import Project
from ..models.transactionModel import Transaction
from ..serializers.getTransactionSerializer import GetTransactionSerializer

class TopUpView(APIView):
    def post(self, request):
        serializer = TopupSerializer(data=request.data)

        if serializer.is_valid():
            # Mendapatkan data dari request
            user_id = request.data.get('user_id')
            project_id = request.data.get('project_id')
            amount = request.data.get('amount')
            payment_method = request.data.get('payment_method')

            try:
                user = User.objects.get(id=user_id)
                project = Project.objects.get(id=project_id)
            except (User.DoesNotExist, Project.DoesNotExist):
                return Response({"error": "User or Project not found."}, status=status.HTTP_404_NOT_FOUND)

            # Buat transaksi dengan status 'success'
            transaction = Transaction(
                user=user,
                project=project,
                amount=amount,
                payment_method=payment_method,
                transaction_type='deposit', 
                status='success',
            )
            transaction.save()

            return Response({
                "message": "Top-up transaction created successfully.",
                "transaction": TopupSerializer(transaction).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def userTransactions(request, userId):
    try:
        # Ambil transaksi user dengan optimalisasi query
        transactions = Transaction.objects.filter(user_id=userId).select_related('project').order_by('-transaction_date')

        # Jika tidak ada transaksi, kembalikan pesan
        if not transactions.exists():
            return Response({"message": "No transactions found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize data transaksi
        serializer = GetTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # Tangani error dengan pesan error generik
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
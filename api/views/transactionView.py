from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..serializers.topupSerializer import TopupSerializer
from django.contrib.auth.models import User
from ..models.projectModel import Project
from ..models.transactionModel import Transaction
from ..serializers.getTransactionSerializer import GetTransactionSerializer
from django.db.models import Sum
from django.utils.timezone import now
from ..models.portfolioModel import Portfolio

class TopUpView(APIView):
    def post(self, request):
        serializer = TopupSerializer(data=request.data)

        if serializer.is_valid():
            user_id = request.data.get('user_id')
            project_id = request.data.get('project_id')
            amount = request.data.get('amount')
            payment_method = request.data.get('payment_method')

            try:
                user = User.objects.get(id=user_id)
                project = Project.objects.get(id=project_id)
            except (User.DoesNotExist, Project.DoesNotExist):
                return Response({"error": "User or Project not found."}, status=status.HTTP_404_NOT_FOUND)

            # Update total dana terkumpul di Project
            total_funds = Portfolio.objects.filter(project=project).aggregate(Sum('invested_amount'))['invested_amount__sum'] or 0
            total_funds += amount

            portfolio = None
            # Buat atau update Portfolio
            try:
                portfolio = Portfolio.objects.get(user=user, project=project)
                portfolio.invested_amount += amount
                portfolio.last_updated = now()
                portfolio.ownership_percentage = ((portfolio.invested_amount + amount) / total_funds) * 100
                portfolio.save()
            except Portfolio.DoesNotExist:
                portfolio = Portfolio.objects.create(
                    user=user,
                    project=project,
                    invested_amount=amount,
                    ownership_percentage= (amount / total_funds) * 100
                )
            
            # Update ownership_percentage untuk semua portfolio di proyek ini
            for p in Portfolio.objects.filter(project=project):
                p.ownership_percentage = (p.invested_amount / total_funds) * 100
                p.save()
            
            project.update_invested_amount()
            
            # Buat transaksi baru
            transaction = Transaction.objects.create(
                user=user,
                project=project,
                portfolio=portfolio,
                amount=amount,
                payment_method=payment_method,
                transaction_type='deposit',
                status='success',
            )
            
            return Response({
                "message": "Top-up transaction and portfolio updated successfully.",
                "transaction": TopupSerializer(transaction).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawView(APIView):
    def post(self, request):
        serializer = TopupSerializer(data=request.data)

        if serializer.is_valid():
            user_id = request.data.get('user_id')
            project_id = request.data.get('project_id')
            amount = request.data.get('amount')
            payment_method = request.data.get('payment_method')

            try:
                user = User.objects.get(id=user_id)
                project = Project.objects.get(id=project_id)
            except (User.DoesNotExist, Project.DoesNotExist):
                return Response({"error": "User or Project not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # Update total dana / kurangi di Project
            total_funds = Portfolio.objects.filter(project=project).aggregate(Sum('invested_amount'))['invested_amount__sum'] or 0
            total_funds -= amount

            try:
                portfolio = Portfolio.objects.get(user=user, project=project)
                
                portfolio.invested_amount -= amount
                if portfolio.invested_amount <= 0:
                    portfolio.delete()
                    portfolio = None
                else:
                    portfolio.ownership_percentage = (portfolio.invested_amount / total_funds) * 100
                    portfolio.last_updated = now()
                    portfolio.save()
            except Portfolio.DoesNotExist:
                raise ValueError("Portfolio tidak ditemukan untuk pengguna dan proyek ini.")
            
            # Update ownership_percentage untuk semua portfolio di proyek ini
            for p in Portfolio.objects.filter(project=project):
                p.ownership_percentage = (p.invested_amount / total_funds) * 100
                p.save()
            
            project.update_invested_amount()

            # Buat transaksi baru
            transaction = Transaction.objects.create(
                user=user,
                project=project,
                portfolio=portfolio,
                amount=amount,
                payment_method=payment_method,
                transaction_type='withdraw',
                status='success',
            )
            
            return Response({
                "message": "Withdraw transaction and portfolio updated successfully.",
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
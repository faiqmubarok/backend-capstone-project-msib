from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from ..models.portfolioModel import Portfolio
from ..models.transactionModel import Transaction
from ..models.projectModel import Project
from django.db.models.functions import TruncMonth
from datetime import datetime
from ..serializers.portfolioSerializer import PortfolioSerializer

class InvestmentStatsView(APIView):
    def get(self, request, userId):
        try:
            # Ambil semua portfolio milik user
            portfolios = Portfolio.objects.filter(user_id=userId)
            
            # Hitung jumlah proyek
            project_count = portfolios.count()

            # Hitung nilai portfolio total
            total_portfolio_value = portfolios.aggregate(
                total_value=Sum('invested_amount')
            )['total_value'] or 0

            # Ambil semua ID portfolio milik user
            portfolio_ids = portfolios.values_list('id', flat=True)

            # Hitung total transaksi masuk (deposit) sesuai dengan portfolio user
            total_deposit = Transaction.objects.filter(
                portfolio_id__in=portfolio_ids, transaction_type='deposit'
            ).aggregate(
                total_amount=Sum('amount')
            )['total_amount'] or 0

            # Hitung total transaksi keluar (withdraw) sesuai dengan portfolio user
            total_withdrawal = Transaction.objects.filter(
                portfolio_id__in=portfolio_ids, transaction_type='withdraw'
            ).aggregate(
                total_amount=Sum('amount')
            )['total_amount'] or 0

            # Hitung total modal (deposit - withdrawal)
            total_modal = total_deposit - total_withdrawal

            # Hitung keuntungan
            profit = total_portfolio_value - total_modal

            # Hitung Persentase keuntungan
            persentage_profit = (profit / total_modal * 100) if total_modal > 0 else 0

            # Ambil semua kategori default
            project_categories = dict(Project.TYPE_PROJECT)

            # Hitung distribusi portfolio (dibagi berdasarkan kategori proyek)
            portfolio_distribution = portfolios.values('project__type').annotate(
                total_investment=Sum('invested_amount')
            )

            # Buat dictionary distribusi dengan nilai default 0
            distribution_dict = {key: 0 for key in project_categories.keys()}

            # Perbarui nilai distribusi berdasarkan hasil query
            for entry in portfolio_distribution:
                distribution_dict[entry['project__type']] = entry['total_investment']

            # Format distribusi menjadi list dengan label
            distribution_data = [
                {"label": project_categories[key], "total_investment": value}
                for key, value in distribution_dict.items()
            ]

            # Data untuk grafik investasi bulanan
            monthly_investment = Transaction.objects.filter(
                user_id=userId, transaction_type='deposit'
            ).annotate(month=TruncMonth("transaction_date")).values("month").annotate(
                total_investment=Sum("amount")
            ).order_by("month")

            # Format data untuk grafik
            investment_chart_data = [
                {
                    "bulan": entry["month"].strftime("%b"),  # Nama bulan singkat (Jan, Feb, dst.)
                    "investasi": entry["total_investment"]
                }
                for entry in monthly_investment
            ]

            # investment_chart_data.extend([
            #     {"bulan": "Feb", "investasi": 2000000},
            #     {"bulan": "Mar", "investasi": 5000000},
            #     {"bulan": "Apr", "investasi": 7500000},
            # ])

            # Jika tidak ada data untuk grafik, set ke bulan sekarang
            if not investment_chart_data:
                current_month = datetime.now().strftime("%b")  # Nama bulan singkat (misal: "Jan")
                # Atur data grafik dengan bulan sekarang
                investment_chart_data = [{"bulan": current_month, "investasi": 0}]

            # Response
            return Response({
                "project_count": project_count,
                "total_portfolio_value": total_portfolio_value,
                "total_modal": total_modal,
                "profit": profit,
                "portfolio_distribution": distribution_data,
                "persentage_profit" : persentage_profit,
                "investment_chart_data": investment_chart_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PortfolioView(APIView):
    def get(self, request, userId):
        # Ambil portfolio berdasarkan user_id
        portfolios = Portfolio.objects.filter(user_id=userId).select_related('project')
        
        # Jika tidak ada data portfolio untuk user_id
        if not portfolios.exists():
            return Response(
                {
                    "success": True,  # Jangan gunakan False, karena tidak ada error
                    "message": "User ini belum memiliki portfolio atau investasi.",
                    "data": []  # Kirim data kosong
                },
                status=status.HTTP_200_OK  # Gunakan status 200 OK, karena bukan error
            )
        
        # Jika data ditemukan
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(
            {
                "success": True,
                "message": "Data portfolio berhasil diambil.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
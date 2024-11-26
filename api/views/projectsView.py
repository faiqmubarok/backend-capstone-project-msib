from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from rest_framework.response import Response
from ..models.projectModel import Project
from ..serializers.projectsSerializer import ProjectSerializer
from ..serializers.projectDetailSerializer import ProjectDetailSerializer, FarmerSerializer, FinancialReportSerializer

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Ambil semua data dari model
        serializer = self.get_serializer(queryset, many=True)  # Serialize data

        # Tambahkan metadata tambahan ke response
        response_data = {
            "status": "success",  # Status API
            "total_data": queryset.count(),  # Total jumlah proyek
            "data": serializer.data  # Data proyek
        }

        return Response(response_data)  # Kirim response dengan metadata

from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UpcomingProjectView(APIView):
    def get(self, request):
        # Mengambil 6 proyek yang akan dimulai (available dan start_date di masa depan atau hari ini)
        projects = Project.objects.filter(
            status='available', 
            start_date__gte=date.today()
        ).order_by('start_date')[:6]  

        # Serialisasi data proyek
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopFundsProjectView(APIView):
    def get(self, request):
        # Mengambil 6 proyek dengan dana kelola terbesar yang statusnya tersedia
        projects = Project.objects.filter(status__in=['available', 'ongoing']).order_by('-invested_amount')[:6]
        # Serialisasi data proyek
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TopProfitProjectView(APIView):
    def get(self, request):
        # Mengambil proyek dengan keuntungan tertinggi yang statusnya aktif
        # Menghitung keuntungan berdasarkan financial report
        projects_with_profit = Project.objects.filter(status__in=['available', 'ongoing']).annotate(
            total_profit=Sum('financial_reports__profit')
        ).order_by('-total_profit')[:6]
        
        # Serialisasi data proyek
        serializer = ProjectSerializer(projects_with_profit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectDetailView(APIView):
    def get(self, request, projectId):
        try:
            # Ambil project berdasarkan id
            project = Project.objects.get(pk=projectId)
            
            # Serialize data project
            project_data = ProjectDetailSerializer(project).data

            # Serialize data farmer yang terkait dengan project
            farmer_data = FarmerSerializer(project.farmer).data
            
            # Ambil 5 laporan keuangan terbaru yang terkait dengan project
            latest_financial_reports = project.financial_reports.order_by('-uploaded_at')
            financial_reports_data = FinancialReportSerializer(latest_financial_reports, many=True).data
            
            # Gabungkan semua data dalam satu response
            response_data = {
                'project': project_data,
                'farmer': farmer_data,
                'financial_reports': financial_reports_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
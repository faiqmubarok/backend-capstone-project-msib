from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
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

class ProjectDetailView(APIView):
    def get(self, request, projectId):
        try:
            # Ambil project berdasarkan id
            project = Project.objects.get(pk=projectId)

            
            # Serialize data project
            project_data = ProjectDetailSerializer(project).data

            # Serialize data farmer yang terkait dengan project
            farmer_data = FarmerSerializer(project.farmer).data
            
            # Serialize financial reports yang terkait dengan project
            financial_reports_data = FinancialReportSerializer(project.financial_reports.all(), many=True).data
            
            # Gabungkan semua data dalam satu response
            response_data = {
                'project': project_data,
                'farmer': farmer_data,
                'financial_reports': financial_reports_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
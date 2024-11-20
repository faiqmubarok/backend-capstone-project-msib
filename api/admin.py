from django.contrib import admin
from django.contrib.auth.models import User
from .models.userModel import Address, Finance, UserProfile
from .models.projectModel import Project
from .models.farmerModel import Farmer
from .models.financialReportModel import FinancialReport

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'province', 'city', 'district', 'sub_district', 'postal_code']

@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank', 'no_rekening']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone', 'job', 'last_update']
    search_fields = ['user__email', 'name', 'phone']
    list_filter = ['last_update']

    def save_model(self, request, obj, form, change):
        # Pastikan user_profile mengupdate User yang terkait
        obj.save()

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'farmer', 'status', 'report_count'
    )
    list_filter = ('type', 'status', 'farmer')  # Filter berdasarkan tipe proyek, status, dan petani
    search_fields = ('name', 'location', 'farmer__name')  # Pencarian berdasarkan nama proyek, lokasi, dan nama petani
    ordering = ('-start_date',)  # Urutkan berdasarkan tanggal mulai terbaru

    # Hitung jumlah laporan keuangan
    def report_count(self, obj):
        return obj.financial_reports.count()
    report_count.short_description = 'Jumlah Laporan'

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address', 'project_count')
    search_fields = ('name', 'email')  # Pencarian berdasarkan nama dan email

    # Hitung jumlah proyek yang dimiliki oleh petani
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Jumlah Proyek'

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'project', 'uploaded_at')
    list_filter = ('project',)  # Filter berdasarkan proyek
    search_fields = ('file_name', 'project__name')  # Pencarian berdasarkan nama file dan proyek

# Custom admin untuk User Django
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    list_filter = ['is_active', 'is_staff']
    
    def save_model(self, request, obj, form, change):
        # Anda bisa menambahkan logika tambahan di sini jika diperlukan
        obj.set_password(obj.password)  # Mengatur password menggunakan set_password
        obj.save()

# Registrasi Model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
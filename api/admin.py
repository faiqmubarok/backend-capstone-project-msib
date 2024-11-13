from django.contrib import admin
from django.contrib.auth.models import User
from .models.userModel import Address, Finance, UserProfile
from .serializers.registerSerializer import UserProfileSerializer

class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'province', 'city', 'district', 'sub_district', 'postal_code']

class FinanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank', 'no_rekening']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone', 'job', 'last_update']
    search_fields = ['user__email', 'name', 'phone']
    list_filter = ['last_update']

    def save_model(self, request, obj, form, change):
        # Pastikan user_profile mengupdate User yang terkait
        obj.save()


# Custom admin untuk User Django
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    list_filter = ['is_active', 'is_staff']
    
    def save_model(self, request, obj, form, change):
        # Anda bisa menambahkan logika tambahan di sini jika diperlukan
        obj.set_password(obj.password)  # Mengatur password menggunakan set_password
        obj.save()

# Registrasi Model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Address, AddressAdmin)
admin.site.register(Finance, FinanceAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

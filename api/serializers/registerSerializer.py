from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.userModel import Address, Finance, UserProfile

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['province', 'city', 'district', 'sub_district', 'postal_code']

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ['bank', 'no_rekening']

class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    finance = FinanceSerializer()

    class Meta:
        model = UserProfile
        fields = ['name', 'no_ktp', 'phone', 'job', 'address', 'finance', 'photoProfile']

class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'user_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Ambil data untuk user_profile
        user_profile_data = validated_data.pop('user_profile', None)

        # Membuat User terlebih dahulu
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        # Setelah User berhasil dibuat, baru kita buat UserProfile
        if user_profile_data:
            # Ambil data address dan finance dari user_profile
            address_data = user_profile_data.pop('address', None)
            finance_data = user_profile_data.pop('finance', None)

            # Membuat Address dan Finance
            address = Address.objects.create(**address_data) if address_data else None
            finance = Finance.objects.create(**finance_data) if finance_data else None

            # Membuat UserProfile dan menghubungkannya dengan User yang baru dibuat
            user_profile = UserProfile.objects.create(
                user=user,
                address=address,
                finance=finance,
                **user_profile_data
            )
        
        return user


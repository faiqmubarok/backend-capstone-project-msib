from rest_framework import serializers
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

    def update(self, instance, validated_data):
        # Update Address nested field
        address_data = validated_data.pop('address', None)
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        # Update Finance nested field
        finance_data = validated_data.pop('finance', None)
        if finance_data:
            for attr, value in finance_data.items():
                setattr(instance.finance, attr, value)
            instance.finance.save()

        # Tangani photoProfile
        photo_profile = validated_data.get('photoProfile', None)
        if photo_profile is None:
            # Jika photoProfile bernilai null, hapus file lama jika ada
            if instance.photoProfile:
                instance.photoProfile.delete(save=False)
            instance.photoProfile = None
        elif photo_profile != instance.photoProfile:
            # Jika ada photoProfile baru, ganti file lama
            if instance.photoProfile:
                instance.photoProfile.delete(save=False)
            instance.photoProfile = photo_profile

        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


from rest_framework import serializers
from ..models.userModel import  UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'no_ktp', 'phone', 'job', 'photoProfile']

    def update(self, instance, validated_data):
        # Tangani photoProfile jika ada
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

        # Update field lainnya pada UserProfile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


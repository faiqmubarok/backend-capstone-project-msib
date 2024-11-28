from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ..serializers.registerSerializer import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.loginSerializer import LoginSerializer
from ..models.userModel import UserProfile
from django.contrib.auth.models import User

from ..serializers.updateSerializer import UserProfileSerializer

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Membuat RefreshToken untuk user
        refresh = RefreshToken.for_user(user)

        # Mengambil data dari UserProfile yang berelasi dengan user
        try:
            user_profile = UserProfile.objects.get(user=user)
            user_profile_data = {
                'name': user_profile.name,
                'job': user_profile.job,
                'photoProfile': user_profile.photoProfile.url if user_profile.photoProfile else None,
            }
        except UserProfile.DoesNotExist:
            user_profile_data = {}

        return Response({
            'user': {
                'user_id': user.id,
                'email': user.email,
            },
            'user_profile': user_profile_data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUser(request, userId):
    try:
        user = User.objects.get(id=userId)

        user_data = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined
        }

        # Jika ada UserProfile, tambahkan data profil ke response
        try:
            user_profile = UserProfile.objects.get(user=user)
            user_data.update({
                "name": user_profile.name,
                "no_ktp": user_profile.no_ktp,
                "phone": user_profile.phone,
                "job": user_profile.job,
                "last_update": user_profile.last_update,
                "photoProfile": user_profile.photoProfile.url if user_profile.photoProfile else None,
            })

            if user_profile.address:
                user_data.update({
                    "address": {
                        "province": user_profile.address.province,
                        "city": user_profile.address.city,
                        "district": user_profile.address.district,
                        "sub_district": user_profile.address.sub_district,
                        "postal_code": user_profile.address.postal_code,
                    }
                })
            if user_profile.finance:
                user_data.update({
                    "finance": {
                        "bank": user_profile.finance.bank,
                        "no_rekening": user_profile.finance.no_rekening,
                    }
                })

        except UserProfile.DoesNotExist:
            pass

        return Response(user_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"detail": "Pengguna tidak ditemukan."},
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['PUT', 'PATCH'])
def updateUser(request, userId):
    try:
        # Ambil UserProfile berdasarkan userId
        user_profile = UserProfile.objects.get(user_id=userId)

        # Update user profile (misalnya: name, no_ktp, phone, job, etc.)
        name = request.data.get('name', None)
        no_ktp = request.data.get('no_ktp', None)
        phone = request.data.get('phone', None)
        job = request.data.get('job', None)
        
        # Update jika ada data yang dikirim
        if name:
            user_profile.name = name
        if no_ktp:
            user_profile.no_ktp = no_ktp
        if phone:
            user_profile.phone = phone
        if job:
            user_profile.job = job

        # Tangani photoProfile jika ada
        photo_profile = request.data.get('photoProfile', None)
        if photo_profile is None:
            # Jika photoProfile bernilai null, hapus file lama jika ada
            if user_profile.photoProfile:
                user_profile.photoProfile.delete(save=False)
            user_profile.photoProfile = None
        elif isinstance(photo_profile, str):
            pass
        else:
            # Jika ada photoProfile baru (file), ganti file lama
            if user_profile.photoProfile:
                user_profile.photoProfile.delete(save=False)
            user_profile.photoProfile = photo_profile

        # Parsing address dan finance yang ada dalam request.data
        address_data = {
            "province": request.data.get('address[province]', None),
            "city": request.data.get('address[city]', None),
            "district": request.data.get('address[district]', None),
            "sub_district": request.data.get('address[sub_district]', None),
            "postal_code": request.data.get('address[postal_code]', None),
        }

        finance_data = {
            "bank": request.data.get('finance[bank]', None),
            "no_rekening": request.data.get('finance[no_rekening]', None),
        }

        # Update Address jika ada data untuk address
        if any(address_data.values()):
            address = user_profile.address
            for attr, value in address_data.items():
                if value:  # hanya update jika ada nilai baru
                    setattr(address, attr, value)
            address.save()

        # Update Finance jika ada data untuk finance
        if any(finance_data.values()):
            finance = user_profile.finance
            for attr, value in finance_data.items():
                if value:  # hanya update jika ada nilai baru
                    setattr(finance, attr, value)
            finance.save()

        # Simpan perubahan user profile
        user_profile.save()

        # Kembalikan response
        return Response({
            'name': user_profile.name,
            'no_ktp': user_profile.no_ktp,
            'phone': user_profile.phone,
            'job': user_profile.job,
            'photoProfile': (
                user_profile.photoProfile.url 
                if user_profile.photoProfile else None
            ),
            'address': {
                'province': user_profile.address.province,
                'city': user_profile.address.city,
                'district': user_profile.address.district,
                'sub_district': user_profile.address.sub_district,
                'postal_code': user_profile.address.postal_code,
            },
            'finance': {
                'bank': user_profile.finance.bank,
                'no_rekening': user_profile.finance.no_rekening,
            }
        }, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({'detail': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ..serializers.registerSerializer import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.loginSerializer import LoginSerializer
from ..models.userModel import UserProfile
from django.contrib.auth.models import User

from ..serializers.updateSerializer import UserProfileSerializer, AddressSerializer, FinanceSerializer

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
        user_profile = UserProfile.objects.get(user_id=userId)

        address_data = request.data.get('address', None)
        finance_data = request.data.get('finance', None)

        # Jika ada data address, update atau buat address baru
        if address_data:
            address_serializer = AddressSerializer(user_profile.address, data=address_data, partial=True)
            if address_serializer.is_valid():
                address_serializer.save()
            else:
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Jika ada data finance, update atau buat finance baru
        if finance_data:
            finance_serializer = FinanceSerializer(user_profile.finance, data=finance_data, partial=True)
            if finance_serializer.is_valid():
                finance_serializer.save()
            else:
                return Response(finance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Memproses user_profile
        user_profile_serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if user_profile_serializer.is_valid():
            user_profile_serializer.save()
            return Response(user_profile_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except UserProfile.DoesNotExist:
        return Response({'detail': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

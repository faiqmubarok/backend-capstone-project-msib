from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ..serializers.registerSerializer import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.loginSerializer import LoginSerializer
from ..models.userModel import UserProfile

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

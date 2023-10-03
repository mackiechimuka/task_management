from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenVerifyView,TokenRefreshView
from rest_framework import status


from .models import User,UserManager
from .serializers import UserSerializer,TokenObtainPairSerializer


# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if 'refresh' not in request.data:
            return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(request.data['refresh'])
            token_payload = token.payload

            # Store the invalidated refresh token in your backend
            # You can use a model to store invalidated tokens and check against them during token verification

            return Response({'detail': 'Token successfully invalidated.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationSuperuserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserManager().create_superuser(**serializer.validated_data)
            return Response({'message': 'Superuser created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
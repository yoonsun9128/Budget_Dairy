from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
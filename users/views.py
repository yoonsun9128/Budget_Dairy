from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from users.models import User
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema

class UserSignupView(APIView):
    @swagger_auto_schema(
        operation_description="회원가입",
        operation_summary="회원가입",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
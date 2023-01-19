from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from accounts.models import Account
from users.models import User
from accounts.serializers import AccountSerializer, AccountDetailSerializer, AddAccountSerializer

class AccountAllView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        account_list = Account.objects.all()
        serializer = AccountSerializer(account_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)

class AccountDetailView(APIView):
    def get(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from accounts.models import Account
from users.models import User
from accounts.serializers import AccountSerializer

# Create your views here.
class AccountAllView(APIView):
    def get(self, request):
        account_list = Account.objects.all()
        serializer = AccountSerializer(account_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


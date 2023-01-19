from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from accounts.models import Account
from users.models import User
from accounts.serializers import AccountSerializer, AccountDetailSerializer, AddAccountSerializer, AccountEditSerializer

class AccountAllView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        account_list = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(account_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetailView(APIView):
    def get(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        data = request.data
        if request.user == account.user:
            if data['memo'] =="":
                data = dict({key:value for key, value in data.items() if value !=""})
                serializer = AccountEditSerializer(account, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = AccountEditSerializer(account, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        if request.user == account.user:
            account.delete()
            return Response({"message":"삭제완료"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)


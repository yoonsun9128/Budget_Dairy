from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from accounts.models import Account
from users.models import User
from accounts.serializers import AccountSerializer, AccountDetailSerializer, AddAccountSerializer, AccountEditSerializer
from drf_yasg.utils import swagger_auto_schema

class AccountAllView(APIView):
    @swagger_auto_schema(
        operation_description="가계부 전체 리스트",
        operation_summary="가계부 전체 리스트",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        payment = request.GET.get('payment_method')
        if payment == None:
            account_list = Account.objects.filter(user=request.user)
        elif payment:
            account_list = Account.objects.filter(user=request.user,method=payment )
        serializer = AccountSerializer(account_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="가계부 등록",
        operation_summary="가계부 등록",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetailView(APIView):
    @swagger_auto_schema(
        operation_description="가계부 상세페이지",
        operation_summary="가계부 상세페이지",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def get(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="가계부 상세페이지 수정",
        operation_summary="가계부 상세페이지 수정",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
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

    @swagger_auto_schema(
        operation_description="가계부 상세페이지 삭제",
        operation_summary="가계부 상세페이지 삭제",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def delete(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        if request.user == account.user:
            account.delete()
            return Response({"message":"삭제완료"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)

class AccountDetailCopyView(APIView):
    @swagger_auto_schema(
        operation_description="가계부 복사",
        operation_summary="가계부 복사",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def post (self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        account.pk = None
        serializer = AddAccountSerializer(data=account.__dict__)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareUrlView(APIView):
    @swagger_auto_schema(
        operation_description="가계부 공유 url 제공",
        operation_summary="가계부 공유 url 제공",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def get (self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        print(account.get_absolute_url)
        url = account.get_absolute_url
        return render(request, 'share.html', {'url':url} )
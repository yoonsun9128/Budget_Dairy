from rest_framework import serializers
from accounts.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('amount',)

class AccountDetailSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_create_at(self, obj):
        return obj.create_at.strftime('%Y-%m-%d')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d')

    class Meta:
        model = Account
        fields = '__all__'

class AddAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('amount','memo','method')
    # def validate(self,data):
        # print(Account.Payment_Method[0][0])
    #     print(data)
    #     if not data['method'] in ['카드','현금','이체','입금']:
    #         raise serializers.ValidationError("현금,카드,이체,입금을 입력해주세요.")
    #     return data
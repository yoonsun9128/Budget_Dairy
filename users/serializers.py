from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, required=False)

    class Meta:
        model = User
        fields = ('email','name' ,'password','passwordcheck')

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, obj, validated_data):
        obj.username = validated_data.get('name', obj.username)
        obj.password = validated_data.get('password', obj.password)
        obj.set_password(obj.password)
        obj.save()
        return obj

    def validate(self, data):
        password=data.get('password')
        passwordcheck=data.pop('passwordcheck')

        if password != passwordcheck:
            raise serializers.ValidationError(
                detail={"error":"비밀번호가 맞지 않습니다"}
            )

        if not len(data.get("password", "")) >= 5:
            raise serializers.ValidationError(
                detail={"error": "password의 길이는 5자리 이상이어야합니다."}
            )

        if not any(i.isdigit() for i in password):
            raise serializers.ValidationError(
                detail=("password는 영문 숫자 조합으로 구성되어야 합니다.")
            )

        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("이메일이 이미 존재합니다.")

        if User.objects.filter(name=data).exists():
            raise serializers.ValidationError("Username이 이미 존재합니다.")

        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
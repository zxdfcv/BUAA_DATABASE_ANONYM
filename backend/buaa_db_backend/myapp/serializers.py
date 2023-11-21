from datetime import datetime
from django.utils import timezone

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group

from .models import LoginLog, OpLog, ErrorLog

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        # token['nickname'] = user.nickname
        # token['avatar'] = user.avatar
        # 可以加点其他想要包含的信息，token可解析
        return token

    def validate(self, attrs):
        # 实现邮箱和手机号登入:待定
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        user.last_login = timezone.now()
        user.save()
        data = super().validate(attrs)
        refresh = self.get_token(user)
        data['token'] = data['access']
        del data['access']
        expiration_timestamp = refresh.access_token.payload['exp']
        expiration_datetime_utc = datetime.utcfromtimestamp(expiration_timestamp).replace(tzinfo=timezone.utc)
        expiration_datetime_local = timezone.localtime(expiration_datetime_utc)

        # 将日期时间对象格式化为字符串
        data['expire'] = expiration_datetime_local.strftime('%Y-%m-%d %H:%M:%S')

        data['username'] = user.username
        data['email'] = user.email
        data['phone'] = user.phone
        # 可以包含其他想要包含的信息
        # login(attrs, user)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group = Group.objects.get(name='普通用户')
        user.groups.add(group)
        return user


class LoginLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = LoginLog
        fields = '__all__'


class OpLogSerializer(serializers.ModelSerializer):
    re_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = OpLog
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = ErrorLog
        fields = '__all__'

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework import serializers
# from .models import User
#
#
#
# # class LoginSerializer(serializers.ModelSerializer):
# #
# #     class Meta:
# #         model = User
# #         fields = ['username', 'email', 'phone']
# #         extra_kwargs = {
# #             "username": {
# #                 "read_only": True
# #             },
# #             "email": {
# #                 "read_only": True
# #             },
# #             "phone": {
# #                 "read_only": True
# #             }
# #         }
#
#
# class TokenObtainPairSerializer(TokenObtainPairSerializer):
#     """
#     自定义登录认证，使用自有用户表
#     username、password这两个字段为必传字段因为 DRF 要检查这些字段是否有效
#     username_field = 'phone_number'  这是重命名了，username必传字段设置为了phone_number字段必传
#     phone_number = serializers.CharField(required=False) # 这个是设置了自定义的字段是否必传
#     """
#     def validate(self, attrs):
#         username = attrs.get("username")
#         password = attrs.get("password")
#
#         if not username or not password:
#             raise serializers.ValidationError("phone_number and password are required")
#
#         try:
#             user = User.objects.get(username=username, password=password)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("No user found with this username and password.")
#         print(user)
#         refresh = self.get_token(user)
#         data = {"userId": user.id, "token": str(refresh.access_token), "refresh": str(refresh),
#                 'is_vip': user.is_vip}
#         return data
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
from datetime import datetime
from django.utils import timezone

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
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

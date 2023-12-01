from datetime import datetime
from django.utils import timezone

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group

from .models import LoginLog, OpLog, ErrorLog, Classification1, Classification2, Follow

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
        login_type = self.initial_data.get("type",0)

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        if (not user.is_staff) and (login_type == "1"):
            raise serializers.ValidationError("普通用户无法登入管理平台")
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

        data['id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['phone'] = user.phone
        # 可以包含其他想要包含的信息
        # login(attrs, user)
        return data


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group, created = Group.objects.get_or_create(name='普通用户')
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


class UserDetailSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'nickname', 'gender', 'avatar',
                  'description', 'date_joined']

    # def update(self, instance, validated_data):
    #     # 自定义 update 方法，处理更新逻辑
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.nickname = validated_data.get('nickname', instance.nickname)
    #     instance.gender = validated_data.get('gender', instance.gender)
    #     instance.avatar = validated_data.get('avatar', instance.avatar)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save()
    #     return instance


class UserAllDetailSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        exclude = ('password', 'is_superuser', 'user_permissions')
        extra_kwargs = {'id': {'read_only': True},
                        'last_login': {'read_only': True},
                        }


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'is_active', 'is_staff', 'date_joined']


class Classification1Serializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    class Meta:
        model = Classification1
        fields = '__all__'


class Classification2Serializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    classification_1_name = serializers.ReadOnlyField(source='classification_1.name')

    class Meta:
        model = Classification2
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    follower_name=serializers.ReadOnlyField(source='follower.username')
    following_name=serializers.ReadOnlyField(source='following.username')
    class Meta:
        model = Follow
        fields = ['follower', 'following', 'create_time']
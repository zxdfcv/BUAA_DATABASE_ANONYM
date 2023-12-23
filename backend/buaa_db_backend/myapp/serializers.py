from datetime import datetime
from django.utils import timezone

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission

from .models import LoginLog, OpLog, ErrorLog, Classification1, Classification2, Follow, ProductImage, Product, Comment, \
    Reply, Order, Chat, Tag

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
        login_type = self.initial_data.get("type", '0')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        if (not user.is_staff) and (login_type == '1'):
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


class AdminUserCreateSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        exclude = ('is_superuser', 'user_permissions')
        extra_kwargs = {'id': {'read_only': True},
                        'last_login': {'read_only': True},
                        'password': {'write_only': True}
                        }

    def create(self, validated_data):
        group_names = validated_data.pop('groups', [])  # 取出组名列表
        user = super().create(validated_data)  # 先创建用户对象

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)  # 获取或创建组对象
            user.groups.add(group)  # 将用户添加到组中

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
    following_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        # 返回该用户关注的人数
        return obj.following.count()

    def get_follower_count(self, obj):
        # 返回关注该用户的人数
        return obj.follower.count()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'nickname', 'gender', 'avatar',
                  'description', 'date_joined', 'following_count', 'follower_count', 'is_active']

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


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')
        # read_only_fields = ('id',)


class GroupWithPermissionsSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')

    # def create(self, validated_data):
    #     print("create - validated_data:", validated_data)
    #     permissions_data = validated_data.pop('permissions', [])  # 获取 permissions 字段
    #     group = Group.objects.create(**validated_data)
    #
    #     # 转换权限ID为整数
    #     permission_ids = [int(permission['id']) for permission in permissions_data]
    #
    #     # 添加权限到组中
    #     if permission_ids:
    #         permissions = Permission.objects.filter(id__in=permission_ids)
    #         group.permissions.set(permissions)
    #
    #     return group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


# class PermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permission
#         fields = ('id', 'name')


class UserAllDetailAndPermissionSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    groups = GroupSerializer(many=True)
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        # 获取用户的所有权限
        permissions = []
        for group in obj.groups.all():
            for permission in group.permissions.all():
                permissions.append({'id': permission.id, 'name': permission.name})
        return permissions

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        exclude = ('password', 'is_superuser', 'user_permissions')
        extra_kwargs = {'id': {'read_only': True},
                        'last_login': {'read_only': True},
                        # 'user_permissions': {'read_only': True},
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
    follower_name = serializers.ReadOnlyField(source='follower.username')
    following_name = serializers.ReadOnlyField(source='following.username')
    follower_nickname = serializers.ReadOnlyField(source='follower.nickname')
    following_nickname = serializers.ReadOnlyField(source='following.nickname')
    follower_avatar = serializers.SerializerMethodField()
    following_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = '__all__'

    def get_follower_avatar(self, obj):
        return str(obj.follower.avatar) if obj.follower.avatar else ''

    def get_following_avatar(self, obj):
        return str(obj.following.avatar) if obj.following.avatar else ''


class ProductImageSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = ProductImage
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class ProductListSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = [
        ('A', '全新'),
        ('B', '几乎全新'),
        ('C', '轻微使用痕迹'),
        ('D', '明显使用痕迹'),
        ('E', '有一定问题'),
    ]
    ADDR_CHOICES = [
        ('1', '学院路校区'),
        ('2', '沙河校区'),
        ('3', '两校区均可')
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES, source='get_status_display')
    addr = serializers.ChoiceField(choices=ADDR_CHOICES, source='get_addr_display')
    # images = ProductImageSerializer(many=True, read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    merchant_name = serializers.ReadOnlyField(source='merchant.username')
    merchant_avatar = serializers.SerializerMethodField()
    classification_1_name = serializers.ReadOnlyField(source='classification_1.name')
    classification_2_name = serializers.ReadOnlyField(source='classification_2.name')
    collectors_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('collectors',)
        extra_kwargs = {'id': {'read_only': True}}

    def get_collectors_count(self, obj):
        return obj.collectors.count()

    def get_merchant_avatar(self, obj):
        return str(obj.merchant.avatar) if obj.merchant.avatar else ''


class ProductCreateSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True, read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    class Meta:
        model = Product
        exclude = ('views', 'wants', 'is_sold', 'off_shelve', 'collectors')
        extra_kwargs = {'id': {'read_only': True}}


class ProductUpdateSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True, read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    class Meta:
        model = Product
        exclude = ('views', 'wants', 'collectors')
        extra_kwargs = {'id': {'read_only': True}}


class ProductAllDetailSerializer(serializers.ModelSerializer):
    # STATUS_CHOICES = [
    #     ('A', '全新'),
    #     ('B', '几乎全新'),
    #     ('C', '轻微使用痕迹'),
    #     ('D', '明显使用痕迹'),
    #     ('E', '有一定问题'),
    # ]
    # ADDR_CHOICES = [
    #     ('1', '学院路校区'),
    #     ('2', '沙河校区'),
    #     ('3', '两校区均可')
    # ]
    # status = serializers.ChoiceField(choices=STATUS_CHOICES, source='get_status_display')
    # addr = serializers.ChoiceField(choices=ADDR_CHOICES, source='get_addr_display')
    # images = ProductImageSerializer(many=True, read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    merchant_name = serializers.ReadOnlyField(source='merchant.username')
    classification_1_name = serializers.ReadOnlyField(source='classification_1.name')
    classification_2_name = serializers.ReadOnlyField(source='classification_2.name')

    # collectors_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}, }


class CommentListSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source="user.nickname")
    user_avatar = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('is_read', 'likes')
        extra_kwargs = {'id': {'read_only': True},
                        # 'likes': {'read_only': True},
                        }

    def get_user_avatar(self, obj):
        return str(obj.user.avatar) if obj.user.avatar else ''

    def get_likes_count(self, obj):
        return obj.likes.count()


class CommentLikesListSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source="user.nickname")
    user_avatar = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('is_read', 'likes')
        extra_kwargs = {'id': {'read_only': True},
                        # 'likes': {'read_only': True},
                        }

    def get_user_avatar(self, obj):
        return str(obj.user.avatar) if obj.user.avatar else ''

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            # 检查用户是否点赞了评论
            return obj.likes.filter(id=request.user.id).exists()
        return False


class CommentNoticeSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source="user.nickname")
    user_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('likes',)

    def get_user_avatar(self, obj):
        return str(obj.user.avatar) if obj.user.avatar else ''


class CommentAllDetailSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = '__all__'


# class MentionedUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'nickname')


class ReplyListSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    comment_content = serializers.ReadOnlyField(source='comment.content')
    product_id = serializers.ReadOnlyField(source='comment.product.id')
    product_name = serializers.ReadOnlyField(source='comment.product.name')

    user_name = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source="user.nickname")
    user_avatar = serializers.SerializerMethodField()

    mentioned_name = serializers.ReadOnlyField(source="mentioned_user.username")
    mentioned_nickname = serializers.ReadOnlyField(source="mentioned_user.nickname")
    likes_count = serializers.SerializerMethodField()

    # mentioned_users_detail = MentionedUserSerializer(many=True, read_only=True)

    class Meta:
        model = Reply
        exclude = ('is_read', 'comment_read', 'likes')
        extra_kwargs = {'id': {'read_only': True},
                        # 'likes': {'read_only': True},
                        }

    def get_user_avatar(self, obj):
        return str(obj.user.avatar) if obj.user.avatar else ''

    def get_likes_count(self, obj):
        return obj.likes.count()


class ReplyLikesListSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    comment_content = serializers.ReadOnlyField(source='comment.content')
    product_id = serializers.ReadOnlyField(source='comment.product.id')
    product_name = serializers.ReadOnlyField(source='comment.product.name')

    user_name = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source="user.nickname")
    user_avatar = serializers.SerializerMethodField()

    mentioned_name = serializers.ReadOnlyField(source="mentioned_user.username")
    mentioned_nickname = serializers.ReadOnlyField(source="mentioned_user.nickname")
    likes_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    # mentioned_users_detail = MentionedUserSerializer(many=True, read_only=True)

    class Meta:
        model = Reply
        exclude = ('is_read', 'comment_read', 'likes')
        extra_kwargs = {'id': {'read_only': True},
                        # 'likes': {'read_only': True},
                        }

    def get_user_avatar(self, obj):
        return str(obj.user.avatar) if obj.user.avatar else ''

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            # 检查用户是否点赞了评论
            return obj.likes.filter(id=request.user.id).exists()
        return False


class ReplyNoticeSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    comment_content = serializers.ReadOnlyField(source='comment.content')
    product_id = serializers.ReadOnlyField(source='comment.product.id')
    product_name = serializers.ReadOnlyField(source='comment.product.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source="user.nickname")
    user_avatar = serializers.SerializerMethodField()
    mentioned_name = serializers.ReadOnlyField(source="mentioned_user.username")
    mentioned_nickname = serializers.ReadOnlyField(source="mentioned_user.nickname")

    # mentioned_users = MentionedUserSerializer(many=True, read_only=True)

    class Meta:
        model = Reply
        exclude = ('likes', 'comment_read')

    def get_user_avatar(self, obj):
        return str(obj.user.avatar) if obj.user.avatar else ''


class MentionNoticeSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    comment_content = serializers.ReadOnlyField(source='comment.content')
    product_id = serializers.ReadOnlyField(source='comment.product.id')
    product_name = serializers.ReadOnlyField(source='comment.product.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    user_nickname = serializers.ReadOnlyField(source="user.nickname")
    user_avatar = serializers.SerializerMethodField()
    mentioned_name = serializers.ReadOnlyField(source="mentioned_user.username")
    mentioned_nickname = serializers.ReadOnlyField(source="mentioned_user.nickname")

    # mentioned_users = MentionedUserSerializer(many=True, read_only=True)

    class Meta:
        model = Reply
        exclude = ('likes', 'is_read')

    def get_user_avatar(self, obj):
        return str(obj.user.avatar) if obj.user.avatar else ''


class ReplyAllDetailSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    comment_content = serializers.ReadOnlyField(source='comment.content')
    product_id = serializers.ReadOnlyField(source='comment.product.id')
    product_name = serializers.ReadOnlyField(source='comment.product.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    mentioned_name = serializers.ReadOnlyField(source="mentioned_user.username")

    class Meta:
        model = Reply
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    merchant_name = serializers.ReadOnlyField(source='merchant.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')
    pay_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    sender_name = serializers.ReadOnlyField(source='sender.username')
    sender_nickname = serializers.ReadOnlyField(source="sender.nickname")
    sender_avatar = serializers.SerializerMethodField()
    recipient_name = serializers.ReadOnlyField(source='recipient.username')
    recipient_nickname = serializers.ReadOnlyField(source="recipient.nickname")
    recipient_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}

    def get_sender_avatar(self, obj):
        return str(obj.sender.avatar) if obj.sender.avatar else ''

    def get_recipient_avatar(self, obj):
        return str(obj.recipient.avatar) if obj.recipient.avatar else ''


class ChatAllDetailsSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    sender_name = serializers.ReadOnlyField(source='sender.username')
    recipient_name = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = Chat
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}


class TagSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'
        # exclude = ('id',)
        extra_kwargs = {'id': {'read_only': True}}

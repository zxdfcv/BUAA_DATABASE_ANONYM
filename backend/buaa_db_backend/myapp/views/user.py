from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from ..models import Follow
from ..permissions import CanEditUserPermission, CanFollowPermission
from ..serializers import MyTokenObtainPairSerializer, UserLoginSerializer, UserDetailSerializer, FollowSerializer
from ..utils import APIResponse, make_login_log, make_error_log

User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return APIResponse(code=1, msg='用户名或密码错误', data=serializer.errors)
        make_login_log(request)
        return APIResponse(code=0, msg='登录成功', data=serializer.validated_data)


class TestView(APIView):

    def post(self, request, *args, **kwargs):
        s = str(request.user.__dict__)
        return APIResponse(code=0, msg='测试成功', data=s)


class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        email = request.data.get('email')
        if not username or not password:
            return APIResponse(code=1, msg='用户名或密码不能为空')
        if not confirm_password or password != confirm_password:
            return APIResponse(code=1, msg='密码不一致')
        if not email:
            return APIResponse(code=1, msg='邮箱不能为空')
        if User.objects.filter(username=username).exists():
            return APIResponse(code=1, msg='该用户名已存在')

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            print(serializer.errors)
            return APIResponse(code=1, msg='创建失败', data=serializer.errors)

        refresh = RefreshToken.for_user(user)

        expiration_timestamp = refresh.access_token.payload['exp']
        expiration_datetime_utc = datetime.utcfromtimestamp(expiration_timestamp).replace(tzinfo=timezone.utc)
        expiration_datetime_local = timezone.localtime(expiration_datetime_utc)
        response_data = {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'expire': expiration_datetime_local.strftime('%Y-%m-%d %H:%M:%S'),
            'user': UserLoginSerializer(user).data,
        }
        user.last_login = timezone.now()
        user.save()
        make_login_log(request)
        return APIResponse(code=0, msg='创建成功', data=response_data)


@permission_classes([CanEditUserPermission])
class EditUserView(APIView):
    # 必能找到该用户，不然的话过不了权限验证（？）
    def post(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.get(pk=user_id)
        data = request.data.copy()

        excluded_fields = ['is_active', 'id']
        for field in excluded_fields:
            data.pop(field, None)
        serializer = UserDetailSerializer(user, data=data,
                                          # partial=True
                                          )
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        make_error_log(request, '用户更新失败')
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)

    def delete(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()
        return APIResponse(code=0, msg='注销成功')


class UserDetailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.GET.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            make_error_log(request, '用户不存在')
            return APIResponse(code=1, msg='用户不存在')

        serializer = UserDetailSerializer(user)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@permission_classes([CanEditUserPermission])
class UserChangePasswordView(APIView):
    def post(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.get(pk=user_id)
        form = PasswordChangeForm(user, request.data)
        if form.is_valid():
            form.save()
            return APIResponse(code=0, msg='密码更新成功')
        make_error_log(request, '用户密码更新失败')
        return APIResponse(code=1, msg='密码更新失败', data=form.errors)


# @permission_classes([CanFollowPermission])
# class EditFollowView(APIView):
#     def put(self, request):
@permission_classes([CanFollowPermission])
class EditFollowerView(APIView):

    def post(self, request):
        user = request.user
        follower_id = request.GET.get('follower_id')
        try:
            following = User.objects.get(pk=follower_id)
        except User.DoesNotExist:
            make_error_log(request, '关注的用户不存在')
            return APIResponse(code=1, msg='用户不存在')
        if Follow.objects.filter(following=following, follower=user).exists():
            make_error_log(request, '重复关注同一个用户')
            return APIResponse(code=1, msg='你已经关注过该用户')

        following_id = str(following.id, 'utf-8') if isinstance(following.id, bytes) else str(following.id)
        user_id = str(user.id, 'utf-8') if isinstance(user.id, bytes) else str(user.id)
        serializer = FollowSerializer(data={'follower': user_id, 'following': following_id})

        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='关注成功', data=serializer.data)

        make_error_log(request, '关注失败')
        return APIResponse(code=1, msg='关注失败', data=serializer.errors)

    def delete(self, request):
        user = request.user
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        follows = Follow.objects.filter(id__in=ids_arr)
        if follows.count() != len(ids_arr):
            make_error_log(request, '取消的关注不存在')
            return APIResponse(code=1, msg='关注不存在')
        follows = follows.filter(follower=user)
        if follows.count() != len(ids_arr):
            make_error_log(request, '取消的关注不是用户的关注')
            return APIResponse(code=1, msg='该关注不是你的关注')

        follows.delete()
        return APIResponse(code=0, msg='取消成功')


class FollowingListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            make_error_log(request, '用户不存在')
            return APIResponse(code=1, msg='用户不存在')
        followings = Follow.objects.filter(following=user).order_by('-create_time')
        page = self.paginate_queryset(followings)

        if page is not None:
            serializer = FollowSerializer(page, many=True)
            return APIResponse(
                code=0,
                msg='查询成功',
                data={
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data,
                }
            )
        serializer = FollowSerializer(followings, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


class FollowerListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            make_error_log(request, '用户不存在')
            return APIResponse(code=1, msg='用户不存在')
        followers = Follow.objects.filter(follower=user).order_by('-create_time')
        page = self.paginate_queryset(followers)

        if page is not None:
            serializer = FollowSerializer(page, many=True)
            return APIResponse(
                code=0,
                msg='查询成功',
                data={
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data,
                }
            )
        serializer = FollowSerializer(followers, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

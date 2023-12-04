from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from ..permissions import CanEditUserPermission, CanFollowPermission
from ..serializers import MyTokenObtainPairSerializer, UserLoginSerializer, UserDetailSerializer
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
        # # 用户名唯一且不准改，邮箱和电话也唯一，但是能改
        # excluded_fields = ['username', ]
        # for field in excluded_fields:
        #     data.pop(field, None)
        serializer = UserDetailSerializer(user, data=data,
                                          # partial=True
                                          )
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        make_error_log(request, '用户更新失败')
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.get(pk=user_id)
        serializer = UserDetailSerializer(user)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def delete(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()
        return APIResponse(code=0, msg='注销成功')


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

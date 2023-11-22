from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers import MyTokenObtainPairSerializer, UserSerializer
from ..utils import APIResponse, make_login_log

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

        serializer = UserSerializer(data=request.data)
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
            'user': UserSerializer(user).data,
        }
        user.last_login = timezone.now()
        user.save()
        make_login_log(request)
        return APIResponse(code=0, msg='创建成功', data=response_data)

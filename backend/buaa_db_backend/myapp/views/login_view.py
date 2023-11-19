# from django.contrib.auth import get_user_model
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenViewBase
#
# from ..serializers import MyTokenSerializer
#
# User = get_user_model()
#
#
# class LoginView(TokenViewBase):
#     serializer_class = MyTokenSerializer
#
#     def post(self, request, *args, **kwargs):
#         # 使用刚刚编写时序列化处理登陆验证及数据响应
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except Exception as e:
#             raise ValueError(f'验证失败： {e}')
#
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)

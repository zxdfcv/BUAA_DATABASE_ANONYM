from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from ..models import User
from ..serializers import UserAllDetailSerializer, UserListSerializer
from ..utils import APIResponse, make_error_log


class UserAllDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            user_id = request.GET.get('user_id', -1)
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            make_error_log(request, '用户不存在')
            return APIResponse(code=1, msg='用户不存在')
        serializer = UserAllDetailSerializer(user)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def put(self, request):
        try:
            user_id = request.GET.get('user_id', -1)
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            make_error_log(request, '用户不存在')
            return APIResponse(code=1, msg='用户不存在')
        data = request.data.copy()
        serializer = UserAllDetailSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        make_error_log(request, '用户更新失败')
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)


class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        keyword = request.GET.get("keyword", '')
        users = User.objects.filter(username__contains=keyword).order_by('-date_joined')
        serializer = UserListSerializer(users, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        users = User.objects.filter(id__in=ids_arr)
        if users.count() != len(ids_arr):
            make_error_log(request, '注销的用户不存在')
            return APIResponse(code=1, msg='注销的用户不存在')
        for user in users:
            user.is_active = False
            user.save()
        return APIResponse(code=0, msg='用户注销成功')

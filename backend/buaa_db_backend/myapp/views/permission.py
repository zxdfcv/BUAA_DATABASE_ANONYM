from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.permissions import IsAdminUser

from rest_framework.views import APIView

from ..serializers import GroupWithPermissionsSerializer, PermissionSerializer
from ..utils import APIResponse, make_error_log

User = get_user_model()


class GroupView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        groups = Group.objects.all().order_by('id')
        serializer = GroupWithPermissionsSerializer(groups, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def put(self, request):
        permissions_data = request.data.getlist('permissions', [])
        group_data = request.data.copy()
        group_data.pop('permissions', None)

        serializer = GroupWithPermissionsSerializer(data=group_data)
        if serializer.is_valid():
            group = serializer.save()

            # 设置组的权限
            if permissions_data:
                permission_ids = [int(perm_id) for perm_id in permissions_data]
                permissions = Permission.objects.filter(id__in=permission_ids)
                group.permissions.set(permissions)

            return APIResponse(code=0, msg='创建成功', data=serializer.data)

        make_error_log(request, '权限组创建失败')
        return APIResponse(code=1, msg='创建失败', data=serializer.errors)

    def post(self, request):
        try:
            group_id = request.GET.get('group_id', -1)
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            make_error_log(request, '权限组不存在')
            return APIResponse(code=1, msg='权限组不存在')
        # serializer = PermissionSerializer(data=request.data, many=True)
        # if serializer.is_valid():
        #     permissions = serializer.validated_data
        #     group.permissions.set(permissions)
        #     return APIResponse(code=0, msg='设置成功', data=serializer.data)
        # make_error_log(request, '权限组设置失败')
        # return APIResponse(code=1, msg='设置失败', data=serializer.errors)
        permissions_data = request.data.getlist('permissions', [])
        group_data = request.data.copy()
        group_data.pop('permissions', None)

        serializer = GroupWithPermissionsSerializer(group,data=group_data)
        if serializer.is_valid():
            group = serializer.save()
            if permissions_data:
                permission_ids = [int(perm_id) for perm_id in permissions_data]
                permissions = Permission.objects.filter(id__in=permission_ids)
                group.permissions.set(permissions)
            else:
                group.permissions.clear()

            return APIResponse(code=0, msg='修改成功', data=serializer.data)

        make_error_log(request, '权限组修改失败')
        return APIResponse(code=1, msg='修改失败', data=serializer.errors)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        groups = Group.objects.filter(id__in=ids_arr)
        if groups.count() != len(ids_arr):
            make_error_log(request, '删除的权限组不存在')
            return APIResponse(code=1, msg='删除的权限组不存在')
        groups.delete()
        return APIResponse(code=0, msg='权限组删除成功')


class PermissionListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        permissions = Permission.objects.all().order_by('id')
        page = self.paginate_queryset(permissions)
        if page is not None:
            serializer = PermissionSerializer(page, many=True)
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
        serializer = PermissionSerializer(permissions, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

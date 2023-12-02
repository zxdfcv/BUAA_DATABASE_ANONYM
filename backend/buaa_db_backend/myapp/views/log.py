from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import APIView

from ..models import LoginLog, OpLog, ErrorLog
from ..permissions import HasLoginLogVDPermission, HasOpLogVDPermission, HasErrorLogVDPermission
from ..serializers import LoginLogSerializer, OpLogSerializer, ErrorLogSerializer
from ..utils import APIResponse, make_error_log


@permission_classes([HasLoginLogVDPermission])
class LoginLogView(generics.ListAPIView):
    # def get(self, request):
    #     login_logs = LoginLog.objects.all().order_by('-log_time')
    #     serializer = LoginLogSerializer(login_logs, many=True)
    #     return APIResponse(code=0, msg='查询成功', data=serializer.data)
    # queryset = LoginLog.objects.all().order_by('-log_time')
    # serializer_class = LoginLogSerializer
    # pagination_class = PageNumberPagination
    # permission_classes = [HasLoginLogVDPermission]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        login_logs = LoginLog.objects.all().order_by('-log_time')
        page = self.paginate_queryset(login_logs)
        if page is not None:
            serializer = LoginLogSerializer(page, many=True)
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
        serializer = LoginLogSerializer(login_logs, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        login_logs = LoginLog.objects.filter(id__in=ids_arr)
        if login_logs.count() != len(ids_arr):
            make_error_log(request, '删除的登入日志对象不存在')
            return APIResponse(code=1, msg='删除的登入日志对象不存在')
        login_logs.delete()
        return APIResponse(code=0, msg='删除成功')


@permission_classes([HasOpLogVDPermission])
class OpLogView(generics.ListAPIView):
    # def get(self, request):
    #     op_logs = OpLog.objects.all().order_by('-re_time')[:100]
    #     serializer = OpLogSerializer(op_logs, many=True)
    #     return APIResponse(code=0, msg='查询成功', data=serializer.data)
    # queryset = OpLog.objects.all().order_by('-re_time')
    # serializer_class = OpLogSerializer
    # pagination_class = PageNumberPagination
    # permission_classes = [HasOpLogVDPermission]

    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        op_logs = OpLog.objects.all().order_by('-re_time')
        page = self.paginate_queryset(op_logs)
        if page is not None:
            serializer = OpLogSerializer(page, many=True)
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
        serializer = OpLogSerializer(op_logs, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        op_logs = OpLog.objects.filter(id__in=ids_arr)
        if op_logs.count() != len(ids_arr):
            make_error_log(request, '删除的操作日志对象不存在')
            return APIResponse(code=1, msg='删除的操作日志对象不存在')
        op_logs.delete()
        return APIResponse(code=0, msg='删除成功')


@permission_classes([HasErrorLogVDPermission])
class ErrorLogView(generics.ListAPIView):
    # def get(self, request):
    #     error_logs = ErrorLog.objects.all().order_by('-log_time')
    #     serializer = ErrorLogSerializer(error_logs, many=True)
    #     return APIResponse(code=0, msg='查询成功', data=serializer.data)
    #
    # queryset = ErrorLog.objects.all().order_by('-log_time')
    # serializer_class = ErrorLogSerializer
    # pagination_class = PageNumberPagination
    # permission_classes = [HasErrorLogVDPermission]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        error_logs = ErrorLog.objects.all().order_by('-log_time')
        page = self.paginate_queryset(error_logs)
        if page is not None:
            serializer = ErrorLogSerializer(page, many=True)
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
        serializer = ErrorLogSerializer(error_logs, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        error_logs = ErrorLog.objects.filter(id__in=ids_arr)
        if error_logs.count() != len(ids_arr):
            make_error_log(request, '删除的错误日志对象不存在')
            return APIResponse(code=1, msg='删除的错误日志对象不存在')
        error_logs.delete()
        return APIResponse(code=0, msg='删除成功')

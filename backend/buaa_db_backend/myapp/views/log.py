from rest_framework.decorators import permission_classes
from rest_framework.views import APIView

from ..models import LoginLog, OpLog, ErrorLog
from ..permissions import HasLoginLogVDPermission, HasOpLogVDPermission, HasErrorLogVDPermission
from ..serializers import LoginLogSerializer, OpLogSerializer, ErrorLogSerializer
from ..utils import APIResponse, make_error_log


@permission_classes([HasLoginLogVDPermission])
class LoginLogView(APIView):
    def get(self, request):
        login_logs = LoginLog.objects.all().order_by('-log_time')
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
class OpLogView(APIView):
    def get(self, request):
        op_logs = OpLog.objects.all().order_by('-re_time')[:100]
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
class ErrorLogView(APIView):
    def get(self, request):
        error_logs = ErrorLog.objects.all().order_by('-log_time')
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

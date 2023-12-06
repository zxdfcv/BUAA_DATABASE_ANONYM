from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView

from ..models import Classification1, Classification2
from ..permissions import CanViewClassificationPermission
from ..serializers import Classification1Serializer, Classification2Serializer
from ..utils import APIResponse, make_error_log


# @permission_classes([CanViewClassificationPermission])
class Classification1ListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    # def get(self, request):
    #     classifications = Classification1.objects.all().order_by('-create_time')
    #     serializer = Classification1Serializer(classifications, many=True)
    #     return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", None)
        classifications = Classification1.objects.all().order_by('-create_time')
        if keyword:
            classifications = classifications.filter(name__contains=keyword)
        page = self.paginate_queryset(classifications)
        if page is not None:
            serializer = Classification1Serializer(page, many=True)
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
        serializer = Classification1Serializer(classifications, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


# @permission_classes([CanViewClassificationPermission])
class Classification2ListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    # def get(self, request):
    #     classifications = Classification2.objects.all().order_by('-create_time')
    #     serializer = Classification2Serializer(classifications, many=True)
    #     return APIResponse(code=0, msg='查询成功', data=serializer.data)
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", None)
        c_1 = request.GET.get("classification1", None)
        classifications = Classification2.objects.all().order_by('-create_time')
        if c_1:
            if not Classification1.objects.filter(id=c_1).exists():
                make_error_log(request, "查询二级分类时指定一级分类不存在")
                return APIResponse(code=1, msg='一级分类不存在')
            classifications = classifications.filter(classification_1_id=c_1)
        if keyword:
            classifications = classifications.filter(name__contains=keyword)
        page = self.paginate_queryset(classifications)
        if page is not None:
            serializer = Classification2Serializer(page, many=True)
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
        serializer = Classification2Serializer(classifications, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


class EditClassification1View(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request):
        classification1 = Classification1.objects.filter(name=request.data['name'])
        if len(classification1) > 0:
            make_error_log(request, '创建的一级分类已存在')
            return APIResponse(code=1, msg='该名称的一级分类已存在')
        serializer = Classification1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        make_error_log(request, '一级分类创建失败')
        return APIResponse(code=1, msg='创建失败', data=serializer.data)

    def post(self, request):
        try:
            pk = request.GET.get('id', -1)
            classification1 = Classification1.objects.get(pk=pk)
        except Classification1.DoesNotExist:
            make_error_log(request, '更新的一级分类不存在')
            return APIResponse(code=1, msg='一级分类对象不存在')
        serializer = Classification1Serializer(classification1, data=request.data,
                                               # partial=True
                                               )
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        make_error_log(request, '更新一级分类失败')
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        classifications = Classification1.objects.filter(id__in=ids_arr)
        if classifications.count() != len(ids_arr):
            make_error_log(request, '删除的一级分类对象不存在')
            return APIResponse(code=1, msg='删除的一级分类对象不存在')
        classifications.delete()
        return APIResponse(code=0, msg='删除成功', )


class EditClassification2View(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request):
        classification2 = Classification2.objects.filter(name=request.data['name'])
        if len(classification2) > 0:
            make_error_log(request, '创建的二级分类已存在')
            return APIResponse(code=1, msg='该名称的二级分类已存在')
        serializer = Classification2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        make_error_log(request, '二级分类创建失败')
        return APIResponse(code=1, msg='创建失败', data=serializer.data)

    def post(self, request):
        try:
            pk = request.GET.get('id', -1)
            classification2 = Classification2.objects.get(pk=pk)
        except Classification2.DoesNotExist:
            make_error_log(request, '更新的二级分类不存在')
            return APIResponse(code=1, msg='二级分类对象不存在')
        serializer = Classification2Serializer(classification2, data=request.data,
                                               # partial=True
                                               )
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        make_error_log(request, '更新二级分类失败')
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        classifications = Classification2.objects.filter(id__in=ids_arr)
        if classifications.count() != len(ids_arr):
            make_error_log(request, '删除的二级分类对象不存在')
            return APIResponse(code=1, msg='删除的二级分类对象不存在')
        classifications.delete()
        return APIResponse(code=0, msg='删除成功')

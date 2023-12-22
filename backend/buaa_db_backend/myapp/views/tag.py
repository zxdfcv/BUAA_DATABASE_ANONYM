from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from ..models import Tag
from ..serializers import TagSerializer
from ..utils import APIResponse, make_error_log


class TagListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", None)
        tags = Tag.objects.all().order_by('-create_time')
        if keyword:
            tags = tags.filter(name__contains=keyword)
        page = self.paginate_queryset(tags)
        if page is not None:
            serializer = TagSerializer(page, many=True)
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
        serializer = TagSerializer(tags, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


class EditTagView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request):
        tag = Tag.objects.filter(name=request.data['name'])
        if len(tag) > 0:
            make_error_log(request, 'tag已经存在')
            return APIResponse(code=1, msg='tag已经存在')
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        make_error_log(request, 'tag创建失败')
        return APIResponse(code=1, msg='创建失败', data=serializer.data)

    def post(self, request):
        try:
            pk = request.GET.get('id', -1)
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            make_error_log(request, '更新的tag不存在')
            return APIResponse(code=1, msg='tag不存在')
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        make_error_log(request, '更新tag失败')
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        tags = Tag.objects.filter(id__in=ids_arr)
        if tags.count() != len(ids_arr):
            make_error_log(request, '删除的tag不存在')
            return APIResponse(code=1, msg='删除的tag不存在')
        tags.delete()
        return APIResponse(code=0, msg='删除成功')

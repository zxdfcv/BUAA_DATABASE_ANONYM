from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from ..models import Product, Comment, Reply
from ..permissions import CanEditCommentPermission
from ..serializers import CommentListSerializer, CommentNoticeSerializer
from ..utils import APIResponse, make_error_log, send_notification


class CommentListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        sort = request.GET.get('sort', 'create_time')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            make_error_log(request, '商品不存在')
            return APIResponse(code=1, msg='商品不存在')

        comments = Comment.objects.filter(product=product)
        if sort == 'hot':
            comments = comments.annotate(likes_count=Count('likes')).order_by('-likes_count')
        # elif sort == 'create_time':
        else:
            comments = comments.order_by('-create_time')
        # else:
        #     make_error_log(request, '评论查询sort参数不正确')
        #     return APIResponse(code=1, msg='sort参数不正确')
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentListSerializer(page, many=True)
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
        serializer = CommentListSerializer(comments, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@permission_classes([CanEditCommentPermission])
class MyCommentsView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        comments = Comment.objects.filter(user=user).order_by('-create_time')
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentListSerializer(page, many=True)
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
        serializer = CommentListSerializer(comments, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def put(self, request):
        user_id = request.data.get('user')
        product_id = request.data.get('product')

        if user_id != str(request.user.id):
            make_error_log(request, '评论时用户id不匹配')
            return APIResponse(code=1, msg='评论的不是你自己')

        if not Product.objects.filter(pk=product_id).exists():
            make_error_log(request, '评论商品时商品不存在')
            return APIResponse(code=1, msg='商品不存在')

        data = request.data.copy()
        excluded_fields = ['id', 'likes_count', 'reply_count', 'is_read']
        for field in excluded_fields:
            data.pop(field, None)
        serializer = CommentListSerializer(data=data)
        if serializer.is_valid():
            # serializer.save()
            # comment = serializer.save()

            # 在评论成功后调用 send_comment_notification 函数
            # send_comment_notification(comment.id, product_id)
            comment = serializer.save()
            # send_notification(comment.user, "comment", comment.content)
            # send_comment_notification(serializer.instance.id, Product.objects.get(pk=product_id).merchant_id)
            # self.send_notification_to_merchant(serializer.instance)
            return APIResponse(code=0, msg='评论成功', data=serializer.data)

        make_error_log(request, '评论失败')
        return APIResponse(code=1, msg='评论失败', data=serializer.errors)

    def delete(self, request):
        user = request.user
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        comments = Comment.objects.filter(id__in=ids_arr)
        if comments.count() != len(ids_arr):
            make_error_log(request, '删除的评论不存在')
            return APIResponse(code=1, msg='评论不存在')
        comments = comments.filter(user=user)
        if comments.count() != len(ids_arr):
            make_error_log(request, '删除的评论与用户不匹配')
            return APIResponse(code=1, msg='该评论不是你的评论')

        for comment in comments:
            replies = Reply.objects.filter(comment=comment)
            replies.delete()

        comments.delete()
        return APIResponse(code=0, msg='评论删除成功')

    def send_notification_to_merchant(self, comment):
        merchant_id = comment.product.merchant_id
        comment_id = comment.id
        message = f"New comment added with ID {comment_id}."

        # 向 NotificationConsumer 发送消息
        channel_layer = get_channel_layer()
        merchant_notification_channel = "notification"
        async_to_sync(channel_layer.group_send)(
            merchant_notification_channel,
            {
                "type": "comment.notification",
                "message": message,
            },
        )


# 暂定:关于点赞？评论消息？
class CommentNoticeView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        user_products = Product.objects.filter(merchant=user)
        comments = Comment.objects.filter(product__in=user_products).order_by('-create_time')
        get_all = request.GET.get('get_all', '0')
        if not get_all == '1':
            comments = comments.filter(is_read=False)
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentNoticeSerializer(page, many=True)
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
        serializer = CommentNoticeSerializer(comments, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def post(self, request):
        user = request.user
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        comments = Comment.objects.filter(id__in=ids_arr)
        if comments.count() != len(ids_arr):
            make_error_log(request, '已读的评论不存在')
            return APIResponse(code=1, msg='评论不存在')

        user_products = Product.objects.filter(merchant=user)
        comment_all = Comment.objects.filter(product__in=user_products)

        comments_set = set(comments)
        comment_all_set = set(comment_all)
        if not comments_set.issubset(comment_all_set):
            make_error_log(request, '已读的评论与用户不匹配')
            return APIResponse(code=1, msg='该评论你不用已读')
        for comment in comments:
            comment.is_read = True
            comment.save()
        return APIResponse(code=0, msg='操作成功')


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def comment_like(request):
#     try:
#         comment_id = request.GET.get('comment_id')
#         comment = Comment.objects.get(pk=comment_id)
#         comment.like_count += 1
#         comment.save()
#     except Comment.DoesNotExist:
#         make_error_log(request, '点赞的评论不存在')
#         return APIResponse(code=1, msg='评论不存在')
#     serializer = CommentListSerializer(comment)
#     return APIResponse(code=0, msg='点赞成功', data=serializer.data)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def comment_dislike(request):
#     try:
#         comment_id = request.GET.get('comment_id')
#         comment = Comment.objects.get(pk=comment_id)
#         if comment.like_count > 0:
#             comment.like_count -= 1
#             comment.save()
#     except Comment.DoesNotExist:
#         make_error_log(request, '点踩的评论不存在')
#         return APIResponse(code=1, msg='评论不存在')
#     serializer = CommentListSerializer(comment)
#     return APIResponse(code=0, msg='点踩成功', data=serializer.data)

class EditLikesView(APIView):
    def post(self, request):
        user = request.user
        try:
            comment_id = request.GET.get('comment_id')
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            make_error_log(request, '点赞的评论不存在')
            return APIResponse(code=1, msg='评论不存在')
        if comment.likes.filter(id=user.id).exists():
            make_error_log(request, '重复点赞该评论')
            return APIResponse(code=1, msg='你已经点赞过该评论')
        comment.likes.add(user)
        comment.save()
        serializer = CommentListSerializer(comment)
        return APIResponse(code=0, msg='点赞成功', data=serializer.data)

    def delete(self, request):
        user = request.user
        try:
            comment_id = request.GET.get('comment_id')
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            make_error_log(request, '取消点赞的评论不存在')
            return APIResponse(code=1, msg='评论不存在')
        if not comment.likes.filter(id=user.id).exists():
            make_error_log(request, '没有点赞该评论')
            return APIResponse(code=1, msg='你没有点赞过该评论')
        comment.likes.remove(user)
        comment.save()
        serializer = CommentListSerializer(comment)
        return APIResponse(code=0, msg='取消点赞成功', data=serializer.data)

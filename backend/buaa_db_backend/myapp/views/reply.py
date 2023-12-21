from django.db.models import Count
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ..models import Comment, Reply
from ..permissions import CanEditReplyPermission
from ..serializers import ReplyListSerializer, ReplyNoticeSerializer, MentionNoticeSerializer
from ..utils import make_error_log, APIResponse, send_notification


class ReplyListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        comment_id = request.GET.get('comment_id')
        sort = request.GET.get('sort', 'create_time')
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            make_error_log(request, '评论不存在')
            return APIResponse(code=1, msg='评论不存在')

        replies = Reply.objects.filter(comment=comment)
        if sort == 'hot':
            replies = replies.annotate(likes_count=Count('likes')).order_by('-likes_count')
        # elif sort == 'create_time':
        else:
            replies = replies.order_by('-create_time')
        # else:
        #     make_error_log(request, '评论查询sort参数不正确')
        #     return APIResponse(code=1, msg='sort参数不正确')
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = ReplyListSerializer(page, many=True)
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
        serializer = ReplyListSerializer(replies, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@permission_classes([CanEditReplyPermission])
class MyRepliesView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        replies = Reply.objects.filter(user=user).order_by('-create_time')
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = ReplyListSerializer(page, many=True)
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
        serializer = ReplyListSerializer(replies, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def put(self, request):
        user_id = request.data.get('user')
        comment_id = request.data.get('comment')

        if user_id != str(request.user.id):
            make_error_log(request, '回复时用户id不匹配')
            return APIResponse(code=1, msg='回复的不是你自己')

        if not Comment.objects.filter(pk=comment_id).exists():
            make_error_log(request, '回复评论时评论不存在')
            return APIResponse(code=1, msg='评论不存在')

        data = request.data.copy()
        excluded_fields = ['id', 'likes_count', ]
        for field in excluded_fields:
            data.pop(field, None)

        # user_ids = data.getlist('mentioned_users', [])
        # if not user_ids or all(not user_id for user_id in user_ids):
        #     data.pop('mentioned_users', None)

        serializer = ReplyListSerializer(data=data)
        if serializer.is_valid():
            reply=serializer.save()
            comment = Comment.objects.get(pk=comment_id)
            comment.reply_count += 1
            comment.save()
            send_notification(comment.user,"reply_notice",serializer.data)
            if reply.mentioned_user is not None:
                send_notification(reply.mentioned_user, "mentioned_notice", serializer.data)
            return APIResponse(code=0, msg='回复成功', data=serializer.data)
        make_error_log(request, '回复失败')
        return APIResponse(code=1, msg='回复失败', data=serializer.errors)

    def delete(self, request):
        user = request.user
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        replies = Reply.objects.filter(id__in=ids_arr)
        if replies.count() != len(ids_arr):
            make_error_log(request, '删除的回复不存在')
            return APIResponse(code=1, msg='回复不存在')
        replies = replies.filter(user=user)
        if replies.count() != len(ids_arr):
            make_error_log(request, '删除的回复与用户不匹配')
            return APIResponse(code=1, msg='该回复不是你的回复')
        for reply in replies:
            comment = reply.comment
            comment.reply_count -= 1
            comment.save()
        replies.delete()
        return APIResponse(code=0, msg='回复删除成功')


class ReplyNoticeView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        user_comments = Comment.objects.filter(user=user)
        replies = Reply.objects.filter(comment__in=user_comments).order_by('-create_time')
        get_all = request.GET.get('get_all', '0')
        if not get_all == '1':
            replies = replies.filter(is_read=False)
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = ReplyNoticeSerializer(page, many=True)
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
        serializer = ReplyNoticeSerializer(replies, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def post(self, request):
        user = request.user
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        replies = Reply.objects.filter(id__in=ids_arr)
        if replies.count() != len(ids_arr):
            make_error_log(request, '已读的回复不存在')
            return APIResponse(code=1, msg='回复不存在')

        user_comments = Comment.objects.filter(user=user)
        reply_all = Reply.objects.filter(comment__in=user_comments)

        replies_set = set(replies)
        reply_all_set = set(reply_all)
        if not replies_set.issubset(reply_all_set):
            make_error_log(request, '已读的回复与用户不匹配')
            return APIResponse(code=1, msg='该回复你不用已读')
        for reply in replies:
            reply.is_read = True
            reply.save()
        return APIResponse(code=0, msg='操作成功')


class EditLikesView(APIView):
    def post(self, request):
        user = request.user
        try:
            reply_id = request.GET.get('reply_id')
            reply = Reply.objects.get(pk=reply_id)
        except Reply.DoesNotExist:
            make_error_log(request, '点赞的回复不存在')
            return APIResponse(code=1, msg='回复不存在')
        if reply.likes.filter(id=user.id).exists():
            make_error_log(request, '重复点赞该回复')
            return APIResponse(code=1, msg='你已经点赞过该回复')
        reply.likes.add(user)
        reply.save()
        serializer = ReplyListSerializer(reply)
        return APIResponse(code=0, msg='点赞成功', data=serializer.data)

    def delete(self, request):
        user = request.user
        try:
            reply_id = request.GET.get('reply_id')
            reply = Reply.objects.get(pk=reply_id)
        except Reply.DoesNotExist:
            make_error_log(request, '取消点赞的回复不存在')
            return APIResponse(code=1, msg='回复不存在')
        if not reply.likes.filter(id=user.id).exists():
            make_error_log(request, '没有点赞该回复')
            return APIResponse(code=1, msg='你没有点赞过该回复')
        reply.likes.remove(user)
        reply.save()
        serializer = ReplyListSerializer(reply)
        return APIResponse(code=0, msg='取消点赞成功', data=serializer.data)


class MentionNoticeView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        replies = Reply.objects.filter(mentioned_user=user).order_by('-create_time')
        get_all = request.GET.get('get_all', '0')
        # print(get_all)
        if not get_all == '1':
            replies = replies.filter(comment_read=False)
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = MentionNoticeSerializer(page, many=True)
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
        serializer = MentionNoticeSerializer(replies, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def post(self, request):
        user = request.user
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        replies = Reply.objects.filter(id__in=ids_arr)
        if replies.count() != len(ids_arr):
            make_error_log(request, '已读的@不存在')
            return APIResponse(code=1, msg='@不存在')

        reply_all = Reply.objects.filter(mentioned_user=user)

        replies_set = set(replies)
        reply_all_set = set(reply_all)
        if not replies_set.issubset(reply_all_set):
            make_error_log(request, '已读的@与用户不匹配')
            return APIResponse(code=1, msg='该@你不用已读')
        for reply in replies:
            reply.comment_read = True
            reply.save()
        return APIResponse(code=0, msg='操作成功')

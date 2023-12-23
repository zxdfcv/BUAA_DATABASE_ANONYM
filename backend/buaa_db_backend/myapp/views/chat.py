from django.db.models import Max, Q
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.pagination import LimitOffsetPagination

from ..models import User, Product, Chat
from ..permissions import CanChatPermission
from ..serializers import ChatSerializer
from ..utils import make_error_log, APIResponse, send_notification


@permission_classes([CanChatPermission])
class ChatView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        product_id = request.GET.get('product_id')
        other_id = request.GET.get('other_id')
        try:
            other = User.objects.get(pk=other_id)
        except:
            make_error_log(request, "私聊另一方不存在")
            return APIResponse(code=1, msg='另一方不存在')

        try:
            product = Product.objects.get(pk=product_id)
        except:
            make_error_log(request, "私聊商品不存在")
            return APIResponse(code=1, msg='商品不存在')

        chat_query_1 = Chat.objects.filter(
            product=product,
            sender=user,
            recipient=other
        )
        chat_query_2 = Chat.objects.filter(
            product=product,
            sender=other,
            recipient=user
        )
        chat_query_2.update(is_read=True)
        merged_chats = (chat_query_1 | chat_query_2).order_by('-create_time')
        page = self.paginate_queryset(merged_chats)
        if page is not None:
            serializer = ChatSerializer(page, many=True)
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
        serializer = ChatSerializer(merged_chats, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def put(self, request):
        sender = request.user
        # data = request.data.copy()
        product_id = request.data.get('product', None)
        recipient_id = request.data.get('recipient', None)
        if product_id is None or recipient_id is None:
            make_error_log(request, '私聊参数不全')
            return APIResponse(code=1, msg='请传入商品和接收者')

        try:
            recipient = User.objects.get(pk=recipient_id)
        except:
            make_error_log(request, "私聊接收者不存在")
            return APIResponse(code=1, msg='接收者不存在')

        try:
            product = Product.objects.get(pk=product_id)
        except:
            make_error_log(request, "私聊商品不存在")
            return APIResponse(code=1, msg='商品不存在')

        if product.merchant.id != sender.id and product.merchant.id != recipient.id:
            make_error_log(request, "私聊商品与用户不匹配")
            return APIResponse(code=1, msg='私聊商品与用户不匹配')

        excluded_fields = ['id', 'is_read']
        for field in excluded_fields:
            request.data.pop(field, None)
            # request.data._mutable = True
            # request.data.pop(field, None)
            # request.data._mutable = False
        request.data['sender'] = str(sender.id)
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_notification(recipient, "chat_notice", serializer.data)
            return APIResponse(code=0, msg='私聊成功', data=serializer.data)
        make_error_log(request, '私聊失败')
        return APIResponse(code=1, msg='私聊失败', data=serializer.errors)


class ChatNoticeView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    # def get(self, request, *args, **kwargs):
    #     recipient = request.user
    #     latest_chats = (
    #         Chat.objects
    #         .filter(recipient=recipient)
    #         .values('product', 'sender')
    #         .annotate(latest_chat_time=Max('create_time'))
    #         .order_by('product', 'sender')
    #     )
    #     chat_ids = []
    #     for chat_info in latest_chats:
    #         chat = Chat.objects.filter(
    #             recipient=recipient,
    #             product=chat_info['product'],
    #             sender=chat_info['sender'],
    #             create_time=chat_info['latest_chat_time']
    #         ).first()
    #         if chat:
    #             chat_ids.append(chat.id)
    #     final_chats = Chat.objects.filter(id__in=chat_ids).order_by('-create_time')
    #     page = self.paginate_queryset(final_chats)
    #     if page is not None:
    #         serializer = ChatSerializer(page, many=True)
    #         return APIResponse(
    #             code=0,
    #             msg='查询成功',
    #             data={
    #                 'count': self.paginator.count,
    #                 'next': self.paginator.get_next_link(),
    #                 'previous': self.paginator.get_previous_link(),
    #                 'results': serializer.data,
    #             }
    #         )
    #     serializer = ChatSerializer(final_chats, many=True)
    #     return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def get(self, request, *args, **kwargs):
        user = request.user
        chat_ids = get_chats_ids(user)
        print(chat_ids)
        final_chats = (
            Chat.objects
            .filter(id__in=chat_ids)
            .order_by('-create_time')
        )
        page = self.paginate_queryset(final_chats)
        if page is not None:
            serializer = ChatSerializer(page, many=True)
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
        serializer = ChatSerializer(final_chats, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


def get_chats_ids(user):
    recipient_chats = (
        Chat.objects
        .filter(Q(sender=user) | Q(recipient=user))
        .values('id', 'product', 'sender', 'recipient', 'create_time')
    )

    chat_categories = {}
    for chat_info in recipient_chats:
        id = chat_info['id']
        product = chat_info['product']
        sender = chat_info['sender']
        recipient = chat_info['recipient']
        create_time = chat_info['create_time']

        if product not in chat_categories:
            chat_categories[product] = {}
        # print(sender)
        # print(user)
        if sender != user.id:
            key = sender
        else:
            key = recipient

        if key not in chat_categories[product]:
            chat_categories[product][key] = {
                'chats': [],
                'latest_chat_time': None
            }
        chat_categories[product][key]['chats'].append({
            'id': id,
            'sender': sender,
            'recipient': recipient,
            'create_time': create_time,
        })
        if chat_categories[product][key]['latest_chat_time'] is None or create_time > chat_categories[product][key][ \
                'latest_chat_time']:
            chat_categories[product][key]['latest_chat_time'] = create_time

    final_chat_ids = []
    for product, product_categories in chat_categories.items():
        for key, category_info in product_categories.items():
            latest_chat_time = category_info['latest_chat_time']
            for chat_info in category_info['chats']:
                if chat_info['create_time'] == latest_chat_time:
                    final_chat_ids.append(chat_info['id'])

    return final_chat_ids

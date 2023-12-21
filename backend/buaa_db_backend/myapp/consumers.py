import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework_simplejwt.tokens import AccessToken

from .models import Product
from .utils import make_error_log

User = get_user_model()


class WebSocketJWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # 在连接建立时获取用户信息
        scope['user'] = await self.get_user(scope)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, scope):
        try:
            query_string = scope.get("query_string", b"").decode("utf-8")
            token_param = None

            for param in query_string.split("&"):
                key, value = param.split("=")
                if key == "token":
                    token_param = value

            if token_param:
                # print(token_param)
                decoded_data = AccessToken(token_param).payload
                user_id = decoded_data.get('user_id')
                return User.objects.get(id=user_id)
        except (ExpiredSignatureError, InvalidTokenError, KeyError, IndexError, User.DoesNotExist):
            return AnonymousUser()


# class WebSocketJWTAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         # 在连接建立时获取用户信息
#         scope['user'] = await self.get_user(scope)
#         return await super().__call__(scope, receive, send)
#
#     @database_sync_to_async
#     def get_user(self, scope):
#         try:
#             query_string = scope.get("query_string", b"").decode("utf-8")
#             token_param = None
#
#             for param in query_string.split("&"):
#                 key, value = param.split("=")
#                 if key == "token":
#                     token_param = value
#
#             if token_param:
#                 print(token_param)
#                 access_token = AccessToken(token_param)
#                 user = access_token.user
#                 return user
#         except (ExpiredSignatureError, InvalidTokenError, KeyError, IndexError):
#             return AnonymousUser()

# class NotificationConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         # 在连接断开时执行清理工作，比如将连接从群组中移除
#         async_to_sync(self.channel_layer.group_discard)(
#             "notification",
#             self.channel_name
#         )
#
#     def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#
#         # 接收到消息后，发送给商家客户端
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
# class ChatConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#
#         if self.scope['user'].is_anonymous:
#             await self.close()
#
#         else:
#
#             self.group_name = self.scope['user'].username
#
#             await self.channel_layer.group_add(
#                 self.group_name, self.channel_name
#             )
#
#             await self.accept()
#
#     # 离开聊天组
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name, self.channel_name
#         )
#
#         await self.close()
#
#     # 接收前端发来的私信消息
#     async def receive(self, text_data=None, bytes_data=None):
#         print('打印下消息', text_data)
#         await self.send(text_data=json.dumps(text_data))
#

# class NotificationConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         self.accept()
#         # if self.scope['user'].is_anonymous:
#         #     await self.close()
#         # else:
#         #     self.group_name = self.scope['user'].username
#         #     await self.channel_layer.group_add(
#         #         self.group_name, self.channel_name
#         #     )
#         #     await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name, self.channel_name
#         )
#
#         await self.close()
#
#     # 接收前端发来的消息
#     async def receive(self, text_data=None, bytes_data=None):
#         print('打印下消息', text_data)
#         await self.send(text_data=json.dumps(text_data))
class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        # 发起请求之后自动创建连接
        print("正在常见连接")
        self.accept()

    def websocket_receive(self, message):
        print("接受消息", message)
        self.send(text_data='OK')  # 返回给客户端的消息

    def websocket_disconnect(self, message):
        raise StopConsumer()


# class WebSocketJWTAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         query_string = scope.get("query_string", b"").decode("utf-8")
#         token = parse_qs(query_string).get("token", [None])[0]
#
#         if token:
#             scope["user"] = await self.get_user_from_token(token)
#         else:
#             scope["user"] = AnonymousUser()
#
#         return await super().__call__(scope, receive, send)
#
#     @database_sync_to_async
#     def get_user_from_token(self, token):
#         try:
#             decoded_data = AccessToken(token).payload
#             user_id = decoded_data.get('user_id')
#             return User.objects.get(id=user_id)
#         except Exception as e:
#             return AnonymousUser()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            # 用户未认证
            await self.close()
        else:
            # 用户已认证，可以处理连接
            # self.group_name = self.scope['user'].username
            user_id = str(self.scope['user'].id)
            self.group_name = f"user_{user_id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # 处理断开连接的逻辑
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.close()
        # pass

    # async def receive(self, text_data):
    #     print("接受消息", text_data)
    #     # self.send(text_data='OK')
    #     # 处理收到的消息
    #     pass
    async def receive(self, text_data=None, bytes_data=None):
        print('打印下消息', text_data)
        await self.send(text_data=json.dumps(text_data, ensure_ascii=False))

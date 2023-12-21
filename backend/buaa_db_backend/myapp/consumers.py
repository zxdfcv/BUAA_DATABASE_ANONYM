import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from .models import Product
from .utils import make_error_log

User = get_user_model()

# @database_sync_to_async
# def get_user(scope):
#     # 从 scope 中获取用户信息，此处以 SimpleJWT 为例
#     try:
#         token = scope["query_string"].decode("utf-8").split("=")[1]
#         access_token = AccessToken(token)
#         user = access_token.user
#         return user
#     except (KeyError, AccessToken.DoesNotExist, IndexError):
#         return AnonymousUser()
#
# class AuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         # 在连接建立时获取用户信息
#         scope['user'] = await get_user(scope)
#         return await super().__call__(scope, receive, send)


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

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.accept()
        # if self.scope['user'].is_anonymous:
        #     await self.close()
        # else:
        #     self.group_name = self.scope['user'].username
        #     await self.channel_layer.group_add(
        #         self.group_name, self.channel_name
        #     )
        #     await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

        await self.close()

    # 接收前端发来的消息
    async def receive(self, text_data=None, bytes_data=None):
        print('打印下消息', text_data)
        await self.send(text_data=json.dumps(text_data))

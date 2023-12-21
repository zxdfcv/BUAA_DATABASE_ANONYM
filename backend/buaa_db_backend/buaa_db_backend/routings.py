import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from django.urls import path, re_path
from myapp.consumers import  NotificationConsumer

websocket_urlpatterns = [
    # path("ws/merchant_notifications/", NotificationConsumer.as_asgi()),
    # path('ws/chat/', ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P\w+)/$', ChatConsumer.as_asgi()),
    path('ws/notification/', NotificationConsumer.as_asgi()),
]

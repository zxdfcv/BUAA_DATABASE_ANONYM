"""
ASGI config for buaa_db_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys

import django

django.setup()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from myapp.consumers import WebSocketJWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buaa_db_backend.settings")
from .routings import websocket_urlpatterns

# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": WebSocketJWTAuthMiddleware(URLRouter(websocket_urlpatterns)),  # websocket走channels
        # "websocket": URLRouter(websocket_urlpatterns),
    }
)


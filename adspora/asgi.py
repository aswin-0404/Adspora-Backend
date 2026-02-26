"""
ASGI config for adspora project.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adspora.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        OriginValidator(
            AuthMiddlewareStack(
                URLRouter(chat.routing.websocket_urlpatterns)
            ),
            [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "https://your-frontend.onrender.com",
            ],
        )
    ),
})
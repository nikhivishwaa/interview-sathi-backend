import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "interviewsathi.settings")  # ✅ First

import django
django.setup()  # ✅ Must happen before importing models

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from interview.routing import websocket_urlpatterns  # ✅ After setup

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})

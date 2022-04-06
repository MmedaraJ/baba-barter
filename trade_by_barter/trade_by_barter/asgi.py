import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import apps.baba_barter.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trade_by_barter.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.baba_barter.routing.websocket_urlpatterns
        )
    ),
})
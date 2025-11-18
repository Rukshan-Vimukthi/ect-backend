from django.urls import path
from . import consumers


websocket_url_patterns = [
    path("notifications", consumers.NotificationConsumer.as_asgi())
]

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter,ProtocolTypeRouter
from django.urls import path
from chat import consumer


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/chat/',consumer.ChatConsumer.as_asgi())
            ]
        )
    )
})